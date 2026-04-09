# 🧠 RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) application that enables intelligent Q&A on PDF documents using semantic search and large language models.

🚀 **Live Demo:** https://your-app-url.streamlit.app

An end-to-end Retrieval-Augmented Generation (RAG) system that enables users to upload PDF documents and interact with them through an explainable AI interface.

Unlike basic chatbots, this system:
- Grounds responses strictly in document context (no hallucination)
- Provides source attribution with relevance scores
- Displays confidence levels based on retrieval quality

## 🔑 Key Highlights

- Built a modular RAG pipeline (Loader → Chunker → Embedder → Retriever → LLM)
- Implemented semantic search using ChromaDB with similarity scoring
- Designed hallucination-controlled prompting for reliable answers
- Developed explainable UI with source transparency and confidence metrics
- Deployed on Streamlit Cloud with dependency optimization and compatibility fixes


## Features

✨ **Core Capabilities**
- 📄 Upload and process PDF documents
- 🔍 Semantic search with relevance scoring (0.0-1.0)
- 💬 Interactive chat with document context
- 📊 Confidence indicators based on retrieval quality
- 🎯 Source attribution with relevance scores
- 🔄 Auto-summarization of documents
- 💾 Chat history tracking

## Tech Stack

- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **LLM**: Groq (llama-3.1-8b-instant)
- **Framework**: Streamlit
- **PDF Processing**: LangChain PyPDFLoader

## Architecture

```
PDF Upload
    ↓
Split into Chunks → Generate Embeddings → Store in Vector DB
    ↓
User Query → Retrieve Relevant Chunks → Generate LLM Response
    ↓
Display Answer + Sources + Confidence Score
```


## ⚙️ Challenges & Solutions

- **Dependency Conflicts (ChromaDB + Protobuf)**  
  Resolved deployment failure by pinning compatible protobuf version

- **Hallucination Control**  
  Implemented strict prompt constraints to ensure answers are grounded in retrieved context

- **Efficient Embedding Loading**  
  Used caching to avoid repeated model loading in Streamlit sessions

## Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/RAG.git
cd RAG
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API key**
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from [console.groq.com](https://console.groq.com)

## Usage

### Web Interface (Recommended)
```bash
streamlit run app/streamlit_app.py
```
Visit `http://localhost:8501` in your browser

### Command Line
```bash
python main.py
```

## Deployment

### Streamlit Cloud
1. Push repository to GitHub (without `.env` file)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Add `GROQ_API_KEY` secret in Settings
5. Deploy!

### Environment Variables
Streamlit Cloud uses Secrets Management. Set `GROQ_API_KEY` in the Streamlit Cloud dashboard.

## Project Structure

```
RAG/
├── app/
│   ├── __init__.py
│   └── streamlit_app.py        # Main UI
├── pipeline/
│   ├── __init__.py
│   ├── rag_pipeline.py         # Main orchestrator
│   ├── loader.py               # PDF loading
│   ├── chunker.py              # Text splitting
│   ├── embedder.py             # Embeddings
│   ├── vectorstore.py          # ChromaDB wrapper
│   ├── retriever.py            # Semantic search
│   └── llm.py                  # LLM integration
├── main.py                     # CLI entry point
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── .env                        # API keys (not committed)
```

## How It Works

1. **Ingestion**: PDF is split into ~1000 char chunks with 200 char overlap
2. **Embedding**: Chunks are converted to 384-dim embeddings
3. **Storage**: Embeddings stored in ChromaDB with metadata
4. **Retrieval**: User queries converted to embedding, top-5 similar chunks retrieved
5. **Generation**: Retrieved chunks + query sent to Groq LLM
6. **Scoring**: Relevance calculated (0-1), confidence = average relevance score

## Configuration

### Chunk Size
Edit [pipeline/chunker.py](pipeline/chunker.py):
```python
split_documents(documents, chunk_size=1000, chunk_overlap=200)
```

### Embedding Model
Edit [pipeline/embedder.py](pipeline/embedder.py):
```python
model_name="all-MiniLM-L6-v2"  # Default: ~22MB, fast
# Alternatives: all-MiniLM-L12-v2, all-mpnet-base-v2 (more accurate, slower)
```

### LLM Model
Edit [pipeline/llm.py](pipeline/llm.py):
```python
model_name="llama-3.1-8b-instant"  # Groq available models
```

## Limitations

- Vector store resets on each new PDF upload (in-memory ChromaDB)
- Context window limited by LLM (Llama 3.1: 8K tokens)
- Only processes first ~100 pages of large PDFs efficiently
- No support for images/tables in PDFs (text only)

## Future Improvements

- [ ] Persistent vector store with SQLite backend
- [ ] Multi-document search
- [ ] Export chat as PDF
- [ ] Advanced filtering (date range, page numbers)
- [ ] Support for OCR on scanned PDFs
- [ ] Multiple LLM options

## License

MIT

## Troubleshooting

**"ModuleNotFoundError: No module named 'chromadb'"**
- Install dependencies: `pip install -r requirements.txt`

**"ValueError: File path is not a valid file or url"**
- Use forward slashes in paths: `data/pdf/file.pdf` (not backslashes)

**"No relevant context found"**
- Try different query phrasing
- Check that PDF was uploaded successfully
- Verify chunk content matches your question

## Support

For issues, please open a GitHub issue with:
- Error message
- Steps to reproduce
- Python version
- OS (Windows/macOS/Linux)
