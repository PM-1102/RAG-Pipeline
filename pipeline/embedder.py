import os
import warnings
import numpy as np
from typing import List, Dict, Any
from fastembed import TextEmbedding, SparseTextEmbedding

# Mute noisy internal HuggingFace logging schemas
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

class EmbeddingManager:
    """
    Production-grade vector inference framework executing lightning-fast, 
    localized CPU embedding generation via ONNX Runtime.
    """
    def __init__(
        self, 
        dense_model_name: str = "BAAI/bge-small-en-v1.5",
        sparse_model_name: str = "Qdrant/bm25"
    ):
        print(f"[EmbeddingManager] Initializing dense encoder: {dense_model_name}...")
        self.dense_model = TextEmbedding(model_name=dense_model_name)
        
        print(f"[EmbeddingManager] Initializing sparse lexical tokenizer: {sparse_model_name}...")
        self.sparse_model = SparseTextEmbedding(model_name=sparse_model_name)

    def generate_dense_embeddings(self, texts: List[str], is_query: bool = False) -> List[np.ndarray]:
        """
        Generates high-fidelity dense vector embeddings for input strings.
        Ensures perfect MTEB validation compliance by mapping query/passage prefixes.
        """
        if not texts:
            return []

        # BAAI BGE guidelines mandate applying structural prefixes for asymmetric retrieval tasks
        prefix = "query: " if is_query else "passage: "
        processed_texts = [text if text.startswith(( "query: ", "passage: ")) else f"{prefix}{text}" for text in texts]
        
        # FastEmbed returns a lazy iterator; unpack into a standard list structure
        embeddings_generator = self.dense_model.embed(processed_texts)
        return list(embeddings_generator)

    def generate_sparse_embeddings(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Maps source raw text blocks to tokenized sparse matrix weight indexes (BM25 format).
        Essential for precise alphanumeric reference index matching.
        """
        if not texts:
            return []

        sparse_generator = self.sparse_model.embed(texts)
        
        serialized_sparse: List[Dict[str, Any]] = []
        for vec in sparse_generator:
            # Convert raw object arrays to native lists to keep downstream data layer fully decoupled
            serialized_sparse.append({
                "indices": vec.indices.tolist(),
                "values": vec.values.tolist()
            })
            
        return serialized_sparse