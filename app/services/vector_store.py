import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List
from app.core.config import settings

class VectorStoreService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.vector_store = self._load_or_create_index()

    def _load_or_create_index(self):
        index_path = settings.INDEX_DIR
        index_file = os.path.join(index_path, "index.faiss")
        
        if os.path.exists(index_file):
            print("Loading existing FAISS index...")
            return FAISS.load_local(
                settings.INDEX_DIR, 
                self.embeddings,
                allow_dangerous_deserialization=True 
            )
        else:
            print("Index not found. attempting to create from data folder...")
            from app.services.ingestion import process_ingestion
            
            # Auto-ingest documents
            chunks = process_ingestion()
            if chunks:
                print(f"Creating index with {len(chunks)} chunks...")
                return FAISS.from_documents(chunks, self.embeddings)
            else:
                print("No documents found in data folder. Index initiated as None.")
                return None

    def add_documents(self, documents: List[Document]):
        if not documents:
            return
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        
        self.vector_store.save_local(settings.INDEX_DIR)
        print("Index saved.")

    def as_retriever(self, k: int = 4):
        if self.vector_store is None:
             raise ValueError("Vector store is empty. Please ingest documents first.")
        return self.vector_store.as_retriever(search_kwargs={"k": k})

vector_store_service = VectorStoreService()
