import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import settings

def load_documents(directory: str) -> List[Document]:
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith(".txt"):
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    return documents

def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)

def process_ingestion() -> List[Document]:
    """Loads and chunks all documents from the raw data directory."""
    raw_docs = load_documents(settings.DATA_DIR)
    if not raw_docs:
        print("No documents found to ingest.")
        return []
    
    chunks = chunk_documents(raw_docs)
    print(f"Propessed {len(raw_docs)} documents into {len(chunks)} chunks.")
    return chunks
