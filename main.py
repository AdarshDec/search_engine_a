"""
FastAPI Backend for Search Engine
==================================
REST API endpoints to interact with the search engine
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from search_engine import SearchEngine

# Initialize FastAPI app
app = FastAPI(
    title="Search Engine MVP",
    description="A simple search engine with TF-IDF ranking",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing) for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = SearchEngine()


# Request/Response Models
class DocumentRequest(BaseModel):
    """Request model for adding a document"""
    title: str
    content: str


class DocumentResponse(BaseModel):
    """Response model for document operations"""
    id: int
    title: str
    content: str
    snippet: Optional[str] = None
    score: Optional[float] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint - serves the frontend"""
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Search Engine API", "docs": "/docs"}


@app.post("/documents", response_model=dict)
async def add_document(doc: DocumentRequest):
    """
    Add a new document to the search index
    
    This endpoint:
    1. Receives a document (title + content)
    2. Indexes it (builds inverted index, calculates statistics)
    3. Returns the document ID
    """
    doc_id = search_engine.add_document(doc.title, doc.content)
    return {
        "id": doc_id,
        "message": "Document indexed successfully",
        "title": doc.title
    }


@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(10, description="Number of results to return")
):
    """
    Search for documents matching a query
    
    This endpoint:
    1. Takes a search query
    2. Finds matching documents using inverted index
    3. Ranks them by TF-IDF score
    4. Returns top results
    
    Example: /search?q=python&top_k=5
    """
    if not q.strip():
        return {"results": [], "query": q, "message": "Empty query"}
    
    results = search_engine.search(q, top_k=top_k)
    return {
        "results": results,
        "query": q,
        "count": len(results)
    }


@app.get("/documents")
async def get_all_documents():
    """Get all indexed documents"""
    documents = search_engine.get_all_documents()
    return {
        "documents": documents,
        "count": len(documents)
    }


@app.get("/stats")
async def get_stats():
    """
    Get search engine statistics
    
    Returns:
    - Total documents indexed
    - Total words indexed
    - Unique words in vocabulary
    - Average words per document
    """
    stats = search_engine.get_stats()
    return stats


# Load sample documents on startup
@app.on_event("startup")
async def load_sample_documents():
    """Load sample documents when the server starts"""
    try:
        from sample_documents import SAMPLE_DOCUMENTS
        
        print("Loading sample documents...")
        for doc in SAMPLE_DOCUMENTS:
            search_engine.add_document(doc["title"], doc["content"])
        
        stats = search_engine.get_stats()
        print(f"✓ Loaded {stats['total_documents']} sample documents")
        print(f"✓ Indexed {stats['total_words_indexed']} words")
        print(f"✓ Found {stats['unique_words']} unique words")
    except ImportError:
        print("No sample documents found. Start indexing documents via API!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

