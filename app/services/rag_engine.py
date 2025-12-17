from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.services.vector_store import vector_store_service

class RAGEngine:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the following context:
            {context}

            Question: {question}
            """
        )

    def get_chain(self):
        retriever = vector_store_service.as_retriever()
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def query(self, question: str):
        # We also want the sources, so we might need a custom chain or just retrieve explicitly first
        retriever = vector_store_service.as_retriever()
        docs = retriever.invoke(question)
        
        # Simple RAG chain run
        chain = self.get_chain()
        answer = chain.invoke(question)
        
        return answer, docs

rag_engine = RAGEngine()
