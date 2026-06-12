# Use an official, secure, and lightweight Python runtime base
FROM python:3.10-slim

# Force stdin/stdout streams to stay completely unbuffered for real-time logging output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false

WORKDIR /workspace

# Install minimal OS-level system dependencies required for compilation and networking
# CORRECTION: Removed 'software-properties-common' to clear Debian package tracking errors
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Layer Optimization: Copy requirements first to leverage Docker's installation caching mechanics
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create structured data directories with explicit read/write privileges for ONNX cache writes
RUN mkdir -p data/qdrant_storage data/flashrank_cache && \
    chmod -R 777 data

# Transfer the remaining core application asset layers to the image workspace
COPY app/ app/
COPY pipeline/ pipeline/

# Document the default network communication gateway used by Streamlit web instances
EXPOSE 8501

# Add a health check mechanism to verify operational health inside production clusters
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the platform instance automatically on container boot
CMD ["streamlit", "run", "app/streamlit_app.py"]