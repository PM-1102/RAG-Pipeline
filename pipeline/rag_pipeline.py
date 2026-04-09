from .loader import load_pdf
from .chunker import split_documents
from .embedder import EmbeddingManager
from .vectorstore import VectorStore
from .retriever import RAGRetriever
from .llm import GroqLLM

class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingManager()
        self.vectorstore = VectorStore()
        self.llm = GroqLLM()
        self.retriever = RAGRetriever(self.vectorstore, self.embedder)

    def ingest(self, file_path):
        # RESET vector store for new file
        self.vectorstore = VectorStore()
        self.retriever = RAGRetriever(self.vectorstore, self.embedder)

        docs = load_pdf(file_path)
        chunks = split_documents(docs)

        texts = [doc.page_content for doc in chunks]
        embeddings = self.embedder.generate_embeddings(texts)

        self.vectorstore.add_documents(chunks, embeddings)
        
        # Store chunk count for reference
        self.chunk_count = len(chunks)

    def query(self, question):
        docs_with_scores = self.retriever.retrieve(question)

        if not docs_with_scores:
            return "No relevant context found in the document."

        # Extract just the documents (scores not needed for LLM context)
        docs = [doc for doc, _ in docs_with_scores]
        context = "\n\n".join(docs)

        return self.llm.generate(question, context)
    
    def get_summary(self):
        """Get summary of the ingested document using all chunks."""
        try:
            # Retrieve enough chunks to cover the document
            all_chunks = self.retriever.retrieve("document content overview", top_k=20)
            if not all_chunks:
                return "Unable to generate summary - no chunks found."
            
            docs = [doc for doc, _ in all_chunks]
            context = "\n\n".join(docs)
            return self.llm.generate("Provide a concise summary of this document in 3-4 sentences.", context)
        except Exception as e:
            return f"Error generating summary: {str(e)}"