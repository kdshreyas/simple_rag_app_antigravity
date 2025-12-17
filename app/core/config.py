import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Local RAG API"
    VERSION: str = "1.0.0"
    
    # Paths
    DATA_DIR: str = "data"
    INDEX_DIR: str = os.path.join("data", "index")
    INDEX_NAME: str = "faiss_index"

    # Model Settings (Defaults)
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "llama3.2:1b" # A smaller, faster model
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.INDEX_DIR, exist_ok=True)
