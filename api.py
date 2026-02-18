from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

from src.search import RAGSearch, AdvancedRAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Build FAISS index on startup if it doesn't exist
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build FAISS index on startup if needed, then start serving."""
    faiss_index = "faiss_store/faiss.index"
    faiss_meta = "faiss_store/metadata.pkl"
    if not (os.path.exists(faiss_index) and os.path.exists(faiss_meta)):
        logger.info("FAISS index not found. Building from documents in data/...")
        try:
            from src.data_loader import load_all_documents
            from src.vectorstore import FaissVectorStore
            docs = load_all_documents("data")
            store = FaissVectorStore("faiss_store")
            store.build_from_documents(docs)
            logger.info("FAISS index built successfully!")
        except Exception as e:
            logger.error(f"Failed to build FAISS index: {e}")
    else:
        logger.info("FAISS index found. Skipping rebuild.")
    yield  # Server is now running

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Advanced RAG Pipeline API with citations, history, and summarization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipelines (singleton pattern)
basic_rag = None
advanced_rag = None

def get_basic_rag():
    """Get or create BasicRAG instance."""
    global basic_rag
    if basic_rag is None:
        logger.info("Initializing BasicRAG pipeline...")
        basic_rag = RAGSearch()
    return basic_rag

def get_advanced_rag():
    """Get or create AdvancedRAG instance."""
    global advanced_rag
    if advanced_rag is None:
        logger.info("Initializing AdvancedRAG pipeline...")
        advanced_rag = AdvancedRAGPipeline()
    return advanced_rag

# Pydantic models for request/response validation
class BasicQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's question")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of documents to retrieve")

class AdvancedQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's question")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of documents to retrieve")
    min_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum similarity score")
    stream: bool = Field(default=False, description="Enable streaming (demonstration)")
    summarize: bool = Field(default=False, description="Generate 2-sentence summary")

class BasicQueryResponse(BaseModel):
    question: str
    answer: str
    timestamp: str

class SourceInfo(BaseModel):
    source: str
    page: Any
    score: float
    preview: str

class AdvancedQueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceInfo]
    summary: Optional[str]
    timestamp: str

class HistoryResponse(BaseModel):
    history: List[Dict[str, Any]]
    count: int

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: str

# Error handler middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Basic RAG endpoint
@app.post("/api/query/basic", response_model=BasicQueryResponse, tags=["Query"])
async def query_basic(request: BasicQueryRequest):
    """
    Basic RAG query endpoint - returns simple answer.
    
    - **question**: The user's question
    - **top_k**: Number of documents to retrieve (1-10)
    """
    try:
        logger.info(f"Basic query received: {request.question}")
        
        rag = get_basic_rag()
        answer = rag.search_and_summarize(request.question, top_k=request.top_k)
        
        return {
            "question": request.question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error in basic query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Advanced RAG endpoint
@app.post("/api/query/advanced", response_model=AdvancedQueryResponse, tags=["Query"])
async def query_advanced(request: AdvancedQueryRequest):
    """
    Advanced RAG query endpoint - returns answer with citations, sources, and optional summary.
    
    - **question**: The user's question
    - **top_k**: Number of documents to retrieve (1-10)
    - **min_score**: Minimum similarity score threshold (0.0-1.0)
    - **stream**: Enable streaming demonstration
    - **summarize**: Generate 2-sentence summary
    """
    try:
        logger.info(f"Advanced query received: {request.question}")
        
        rag = get_advanced_rag()
        result = rag.query(
            question=request.question,
            top_k=request.top_k,
            min_score=request.min_score,
            stream=request.stream,
            summarize=request.summarize
        )
        
        return {
            "question": result['question'],
            "answer": result['answer'],
            "sources": result['sources'],
            "summary": result['summary'],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error in advanced query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Get history endpoint
@app.get("/api/history", response_model=HistoryResponse, tags=["History"])
async def get_history():
    """
    Get complete query history from Advanced RAG pipeline.
    """
    try:
        rag = get_advanced_rag()
        history = rag.get_history()
        
        return {
            "history": history,
            "count": len(history)
        }
    
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Clear history endpoint
@app.delete("/api/history", tags=["History"])
async def clear_history():
    """
    Clear all query history from Advanced RAG pipeline.
    """
    try:
        rag = get_advanced_rag()
        rag.clear_history()
        
        return {
            "message": "History cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize RAG pipelines on startup.
    """
    logger.info("Starting RAG Chatbot API...")
    # Pre-load pipelines for faster first request
    get_basic_rag()
    get_advanced_rag()
    logger.info("RAG pipelines initialized successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on shutdown.
    """
    logger.info("Shutting down RAG Chatbot API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
