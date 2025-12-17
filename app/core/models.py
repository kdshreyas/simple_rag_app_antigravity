from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: int = 4

class DocumentSource(BaseModel):
    source: str
    page: int
    content: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[DocumentSource]

class IngestResponse(BaseModel):
    message: str
    chunks_count: int
