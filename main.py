import uvicorn
from fastapi import FastAPI
from app.api.server import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "RAG API is running. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
