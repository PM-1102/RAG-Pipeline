# pipeline/vectorstore.py
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client import models
from pipeline.contracts import DocumentChunk

load_dotenv()

class ScamShieldVectorStore:
    """
    Production-grade Qdrant Database orchestrator managing named dual-vector 
    dense + sparse layout configurations for unified hybrid indexing operations.
    """
    def __init__(self, collection_name: str = "scamshield_intelligence", client: Optional[QdrantClient] = None):
        self.collection_name = collection_name
        
        # Enable flexible runtime injection for local memory-isolated prototyping pipelines
        if client:
            self.client = client
        else:
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")
            
            if qdrant_url and qdrant_api_key:
                print(f"[VectorStore] Connecting to secure remote Qdrant Cloud Cluster: {qdrant_url}...")
                self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                print("[VectorStore] API configurations missing. Spanning local persistent storage engine space...")
                self.client = QdrantClient(path="data/qdrant_storage")

        self._ensure_hybrid_collection_exists()

    def _ensure_hybrid_collection_exists(self):
        """Validates index presence; builds out named sparse/dense schemas automatically."""
        if self.client.collection_exists(collection_name=self.collection_name):
            return

        print(f"[VectorStore] Constructing specialized named hybrid vectors schemas for collection: {self.collection_name}...")
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "dense": models.VectorParams(
                    size=384,  # Exactly scales to match BAAI/bge-small-en-v1.5 widths
                    distance=models.Distance.COSINE
                )
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(
                    modifier=models.Modifier.IDF  # Inject server-side Inverse Document Frequency for keyword matching
                )
            }
        )
        print("✅ [VectorStore] Named hybrid vector store collection materialized successfully.")

    def add_document_chunks(
        self, 
        chunks: List[DocumentChunk], 
        dense_embeddings: List[Any], 
        sparse_embeddings: List[Dict[str, Any]],
        tenant_id: str = "default_compliance_tenant"
    ):
        """
        Transforms parsed structural pieces into formal database points.
        Enforces tenancy boundaries within structural payload fields.
        """
        if not chunks:
            return

        assert len(chunks) == len(dense_embeddings) == len(sparse_embeddings), "Input data processing arrays dimensions misaligned."

        points = []
        for i, chunk in enumerate(chunks):
            # Parse payload data configurations
            payload_metadata = chunk.metadata.copy()
            payload_metadata.update({
                "text_content": chunk.content,
                "document_id": chunk.document_id,
                "tenant_id": tenant_id
            })

            # Reconstruct sparse vector dictionary items into structural parameters
            sparse_vector_object = models.SparseVector(
                indices=sparse_embeddings[i]["indices"],
                values=sparse_embeddings[i]["values"]
            )

            # Build Point structure layout parameters
            points.append(
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector={
                        "dense": dense_embeddings[i].tolist() if hasattr(dense_embeddings[i], "tolist") else dense_embeddings[i],
                        "sparse": sparse_vector_object
                    },
                    payload=payload_metadata
                )
            )

        print(f"[VectorStore] Injecting {len(points)} dual-vector points into collection '{self.collection_name}'...")
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print("✅ [VectorStore] Upsert operations completed.")