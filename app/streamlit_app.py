import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path so pipeline modules can be imported
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from pipeline.rag_pipeline import RAGPipeline

# ========================
# PAGE CONFIG & TITLE
# ========================
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🧠 RAG PDF Chatbot")

# ========================
# SESSION STATE
# ========================
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()
    st.session_state.ready = False
    st.session_state.chat_history = []

# ========================
# SIDEBAR - UPLOAD SECTION
# ========================
with st.sidebar:
    st.header("📂 Upload & Process")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("⚙️ Process File"):
            with st.spinner("Processing..."):
                # Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_path = tmp_file.name

                # Ingest PDF
                st.session_state.pipeline.ingest(temp_path)
                st.session_state.ready = True
                st.session_state.chat_history = []  # Reset chat when new file is loaded

            st.success("✅ Ready to chat!")

# ========================
# MAIN CHAT AREA
# ========================
st.subheader("💬 Chat with your document")

if not st.session_state.ready:
    st.info("📌 Upload and process a PDF from the sidebar to begin.")
else:
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # Chat input (Streamlit's chat style)
    user_input = st.chat_input("Ask something about your document...")

    if user_input:
        # Add user message to history and display
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate answer
        with st.spinner("Thinking..."):
            answer = st.session_state.pipeline.query(user_input)
            docs_with_scores = st.session_state.pipeline.retriever.retrieve(user_input)

        # Unpack docs and scores
        docs = [doc for doc, _ in docs_with_scores]
        scores = [score for _, score in docs_with_scores]

        # Display bot response
        with st.chat_message("assistant"):
            st.write(answer)

        # Add bot response to history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Display sources with relevance scores
        with st.expander("📄 Sources Used"):
            if docs:
                for i, (doc, score) in enumerate(zip(docs, scores)):
                    st.markdown(f"**Chunk {i+1} (Score: {score:.2f})**")
                    st.write(doc[:300] + "...")
            else:
                st.write("No sources found.")

        # Display retrieval statistics
        st.caption("🔍 Retrieving relevant chunks...")
        st.caption(f"📊 Retrieved {len(docs)} chunks")

        # Calculate confidence based on average relevance score
        if scores:
            avg_score = sum(scores) / len(scores)
            
            if avg_score > 0.75:
                confidence = "High"
            elif avg_score > 0.5:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            st.caption(f"✨ Confidence: {confidence} ({avg_score:.2f})")
        else:
            st.caption(f"✨ Confidence: Low (No scores)")

        # Error handling
        if not docs:
            st.error("No relevant context found. Try a different query.")

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📌 Auto Summary"):
            with st.spinner("Summarizing..."):
                summary = st.session_state.pipeline.get_summary()
            st.session_state.chat_history.append({"role": "assistant", "content": summary})
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col3:
        if hasattr(st.session_state.pipeline, 'chunk_count'):
            st.metric("📊 Chunks Loaded", st.session_state.pipeline.chunk_count)

st.divider()