# pipeline/loader.py
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

def load_document_to_markdown(file_path: str) -> str:
    """
    Ingests a document asset and outputs a clean, structural markdown string.
    Utilizes LlamaParse if keys exist; falls back to an layout-aware structural 
    text extractor for local zero-budget stability.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target document asset not found at: {file_path}")

    llama_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    file_extension = os.path.splitext(file_path)[1].lower()

    if llama_api_key and file_extension == ".pdf":
        print(f"[Loader] Advanced LlamaParse Cloud detected. Processing visual layout for: {file_path}...")
        try:
            from llama_parse import LlamaParse
            
            parser = LlamaParse(
                api_key=llama_api_key,
                result_type="markdown",
                num_workers=4,
                verbose=False
            )
            extractions = parser.load_data(file_path)
            # Combine multi-page markdown string outputs holistically
            return "\n\n---PAGE-BREAK---\n\n".join([doc.text for doc in extractions])
        except Exception as e:
            print(f"[Loader] LlamaParse execution hit a snag: {str(e)}. Defaulting to structural loader fallback...")

    # Strict $0 Budget Local Fallback Path
    print(f"[Loader] Utilizing local structural parser layout extraction for: {file_path}")
    
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        markdown_pages = []
        for i, page in enumerate(pages):
            # Inject structural markdown headers to signify physical document page steps
            page_text = page.page_content
            markdown_pages.append(f"## PAGE_MARKER_{i+1}\n{page_text}")
        return "\n\n".join(markdown_pages)
    
    else:
        # Standard fallback for .txt or .md files
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()