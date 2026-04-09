from sentence_transformers import SentenceTransformer
import os
import warnings
from transformers import logging as tf_logging

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Suppress verbose model loading
tf_logging.set_verbosity_error()
warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Create cached loader function at module level for efficiency
if HAS_STREAMLIT:
    @st.cache_resource
    def _get_model(model_name):
        return SentenceTransformer(model_name)
else:
    def _get_model(model_name):
        return SentenceTransformer(model_name)

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = _get_model(model_name)

    def generate_embeddings(self, texts):
        return self.model.encode(texts)