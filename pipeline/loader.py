from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    for doc in documents:
        doc.metadata['source_file'] = file_path
        doc.metadata['file_type'] = 'pdf'

    return documents