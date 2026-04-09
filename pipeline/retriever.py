class RAGRetriever:
    def __init__(self, vectorstore, embedder):
        self.vectorstore = vectorstore
        self.embedder = embedder

    def retrieve(self, query, top_k=5):
        query_embedding = self.embedder.generate_embeddings([query])[0]

        results = self.vectorstore.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        docs = results['documents'][0]
        distances = results['distances'][0]

        # Convert distances to similarity scores [0, 1]
        # ChromaDB returns cosine distances in [0, 2], so we normalize properly
        scores = [max(0, 1 - dist) for dist in distances]

        return list(zip(docs, scores))