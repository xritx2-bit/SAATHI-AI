"""
SAATHI AI - Knowledge Base & Hybrid Retrieval API Routes
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from api.schemas import KnowledgeChunkResponse, RetrieveRequest, RetrieveResponse
from saathi.knowledge.store import KnowledgeStore
from saathi.knowledge.retriever import HybridRetriever

router = APIRouter(prefix="/knowledge", tags=["Vetted Knowledge Base & RAG"])

_STORE_INSTANCE = None
_RETRIEVER_INSTANCE = None

def get_store_and_retriever():
    global _STORE_INSTANCE, _RETRIEVER_INSTANCE
    if _STORE_INSTANCE is None:
        _STORE_INSTANCE = KnowledgeStore()
        _RETRIEVER_INSTANCE = HybridRetriever(_STORE_INSTANCE)
    return _STORE_INSTANCE, _RETRIEVER_INSTANCE

@router.get("/chunks", response_model=List[KnowledgeChunkResponse], summary="List All Indexed Official Government Guidelines & Regulations")
async def list_chunks(category: Optional[str] = None, deps=Depends(get_store_and_retriever)):
    """
    Returns all vetted public guidelines indexed in SAATHI AI with official citations, authority levels, and timestamps.
    """
    store, _ = deps
    chunks = store.get_all_chunks()
    if category:
        chunks = [c for c in chunks if c.metadata.get("category", "").lower() == category.lower()]
    
    return [
        KnowledgeChunkResponse(
            id=c.id,
            title=c.title,
            content=c.content,
            source_url_or_file=c.source_url_or_file,
            authority_level=c.authority_level,
            last_updated=c.last_updated,
            category=c.metadata.get("category", "General")
        )
        for c in chunks
    ]

@router.post("/retrieve", response_model=RetrieveResponse, summary="Retrieve Top Vetted Evidences using BM25 & Semantic Match")
async def retrieve_evidence(req: RetrieveRequest, deps=Depends(get_store_and_retriever)):
    """
    Executes hybrid RAG retrieval against vetted Indian government documents.
    """
    _, retriever = deps
    results = retriever.retrieve(req.query, top_k=req.top_k, min_threshold=0.10)
    
    formatted = []
    for r in results:
        formatted.append({
            "chunk_id": r.chunk.id,
            "title": r.chunk.title,
            "content": r.chunk.content,
            "source": r.chunk.source_url_or_file,
            "authority_level": r.chunk.authority_level,
            "relevance_score": round(r.relevance_score, 4),
            "match_reasons": r.match_reasons
        })

    return RetrieveResponse(
        query=req.query,
        total_retrieved=len(formatted),
        results=formatted
    )
