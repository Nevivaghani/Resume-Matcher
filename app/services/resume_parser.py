from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document

def load_resume(file_path: str) -> list[Document]:
    loader = PyMuPDFLoader(file_path)
    return loader.load()
    