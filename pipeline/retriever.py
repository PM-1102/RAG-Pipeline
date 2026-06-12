# pipeline/retriever.py
import os
from typing import List, Dict, Any, Optional
from qdrant_client import models
from flashrank import Ranker, RerankRequest
from pipeline.embedder import EmbeddingManager
from pipeline.vectorstore import ScamShieldVectorStore

class ScamShieldRetriever:
    """
    High-precision retrieval orchestration layer executing dual-vector 
    Qdrant prefetching, RRF score fusion, and localized CPU cross-encoder reranking.
    """
    def __init__(self, vectorstore: ScamShieldVectorStore, embedder: EmbeddingManager):
        self.vectorstore = vectorstore
        self.embedder = embedder
        
        print("[Retriever] Loading localized ultra-lightweight FlashRank Cross-Encoder Engine...")
        # Instantiates a highly optimized 12-layer ONNX cross-encoder model running entirely on CPU
        self.ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir="data/flashrank_cache")

    def retrieve_relevant_context(
        self, 
        query_text: str, 
        tenant_id: str = "default_compliance_tenant",
        candidate_pool_limit: int = 20,
        final_top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Executes unified hybrid prefetching across dense + sparse planes, 
        fuses ranks via server-side RRF, and applies local Cross-Encoder pruning.
        """
        # Generate query representation arrays
        dense_query_vector = self.embedder.generate_dense_embeddings([query_text], is_query=True)[0]
        sparse_query_vector = self.embedder.generate_sparse_embeddings([query_text])[0]

        # Convert sparse primitives directly into type-safe Qdrant structures
        qdrant_sparse_object = models.SparseVector(
            indices=sparse_query_vector["indices"],
            values=sparse_query_vector["values"]
        )

        # Build an explicit, reuseable tenant filter contract block
        tenant_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id", 
                    match=models.MatchValue(value=tenant_id)
                )
            ]
        )

        # Execute multi-stage lookup using Qdrant's Universal Query API
        search_response = self.vectorstore.client.query_points(
            collection_name=self.vectorstore.collection_name,
            prefetch=[
                models.Prefetch(
                    query=dense_query_vector.tolist(),
                    using="dense",
                    filter=tenant_filter,
                    limit=candidate_pool_limit
                ),
                models.Prefetch(
                    query=qdrant_sparse_object,
                    using="sparse",
                    filter=tenant_filter,
                    limit=candidate_pool_limit
                )
            ],
            # Apply Reciprocal Rank Fusion to synthesize parallel scoring tracks natively
            query=models.RrfQuery(rrf=models.Rrf()),
            query_filter=tenant_filter,
            limit=candidate_pool_limit,
            with_payload=True
        )

        if not search_response.points:
            return []

        # Map Qdrant output points to standard dictionary lists expected by FlashRank
        flashrank_passages = []
        for point in search_response.points:
            
            # 🛡️ DEFENSE-IN-DEPTH GUARDRAIL: Intercept driver leakage or mock-engine anomalies
            if point.payload.get("tenant_id") != tenant_id:
                print(f"⚠️ [SECURITY GUARDRAIL] Intercepted cross-tenant leak from data layer! Blocked point belonging to tenant: '{point.payload.get('tenant_id')}'")
                continue
                
            flashrank_passages.append({
                "id": point.id,
                "text": point.payload.get("text_content", ""),
                "meta": {k: v for k, v in point.payload.items() if k != "text_content"}
            })

        # If security filtering stripped away all points, abort processing early
        if not flashrank_passages:
            return []

        # Pack cross-attention inference criteria
        rerank_request = RerankRequest(
            query=query_text,
            passages=flashrank_passages
        )
        
        # Execute local CPU cross-encoder reranking
        reranked_results = self.ranker.rerank(rerank_request)

        # Slice down to final top_k targets and reconstruct clean context outputs
        final_context_payloads = []
        for item in reranked_results[:final_top_k]:
            final_context_payloads.append({
                "chunk_id": item["id"],
                "content": item["text"],
                "score": float(item["score"]),
                "document_id": item["meta"].get("document_id", "unknown"),
                "page_number": item["meta"].get("page_number", 1),
                "section_path": item["meta"].get("section_path", "")
            })

        return final_context_payloads