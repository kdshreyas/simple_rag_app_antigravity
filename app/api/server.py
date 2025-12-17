from fastapi import FastAPI, HTTPException, APIRouter
from app.core.models import QueryRequest, QueryResponse, DocumentSource, IngestResponse
from app.services.ingestion import process_ingestion
from app.services.vector_store import vector_store_service
from app.services.rag_engine import rag_engine

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents():
    try:
        chunks = process_ingestion()
        if not chunks:
             return IngestResponse(message="No documents found or processed.", chunks_count=0)
        
        vector_store_service.add_documents(chunks)
        return IngestResponse(message="Ingestion successful", chunks_count=len(chunks))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_index(payload: QueryRequest):
    try:
        # Check if index exists
        if vector_store_service.vector_store is None:
             raise HTTPException(status_code=400, detail="Index not initialized. Please ingest documents first.")

        answer, docs = rag_engine.query(payload.query)
        
        sources = [
            DocumentSource(
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page", 0),
                content=doc.page_content[:200] + "..."
            ) for doc in docs
        ]
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        # raise e # for debugging
        raise HTTPException(status_code=500, detail=str(e))
