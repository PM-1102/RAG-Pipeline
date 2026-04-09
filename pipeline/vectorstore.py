import chromadb
import uuid

class VectorStore:
    def __init__(self, collection_name="temp_docs"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.doc_count = 0

    def add_documents(self, documents, embeddings):
        # Use UUID for robust unique ID generation
        ids = [f"doc_{self.doc_count}_{uuid.uuid4().hex[:8]}" for _ in range(len(documents))]
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas
        )
        self.doc_count += len(documents)