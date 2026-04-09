from pipeline.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
pipeline.ingest("data/pdf/AI In HealthCare Final.pdf")

questions = [
    "What is AI in healthcare?",
    "List applications of AI in healthcare",
    "What are risks mentioned?",
    "Explain something NOT in document (test hallucination)",
    "Summarize the document"
]

for q in questions:
    print("\nQUESTION:", q)
    print("ANSWER:", pipeline.query(q))