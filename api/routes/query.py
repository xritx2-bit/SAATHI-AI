"""
SAATHI AI - Query & Decision Policy API Routes
"""
import time
from fastapi import APIRouter, HTTPException, Depends
from api.schemas import QueryRequest, QueryResponse, ProposedActionResponse
from saathi.controller.engine import SaathiController
from saathi.knowledge.store import KnowledgeStore

router = APIRouter(prefix="/query", tags=["Decision Controller & Chat"])

_CONTROLLER_INSTANCE = None

def get_controller():
    global _CONTROLLER_INSTANCE
    if _CONTROLLER_INSTANCE is None:
        store = KnowledgeStore()
        _CONTROLLER_INSTANCE = SaathiController(store)
    return _CONTROLLER_INSTANCE

@router.post("", response_model=QueryResponse, summary="Process Citizen Query through Evidence-Gated Decision Controller")
async def process_query(req: QueryRequest, controller: SaathiController = Depends(get_controller)):
    """
    Evaluates citizen input through the multi-stage policy:
    1. Context Enrichment -> 2. Safety Gate (112/108/1930/Self-Harm) -> 3. Language Routing -> 4. Ambiguity Clarification -> 5. Hybrid RAG Retrieval -> 6. Strict Human Action Drafting Gate.
    """
    t_start = time.time()
    
    # Format chat history dicts
    history_dicts = [{"role": t.role, "content": t.content} for t in req.chat_history] if req.chat_history else None

    try:
        decision_res = controller.process_query(
            user_query=req.user_query,
            chat_history=history_dicts,
            llm_provider=req.engine
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Controller processing failed: {str(e)}")

    latency = round((time.time() - t_start) * 1000, 2)

    prop_action = None
    if decision_res.proposed_action:
        act = decision_res.proposed_action
        prop_action = ProposedActionResponse(
            action_id=act.action_id,
            action_type=act.action_type,
            title=act.title,
            requires_approval=act.requires_approval,
            draft_content=act.draft_content,
            warning_or_disclaimer=act.warning_or_disclaimer
        )

    return QueryResponse(
        decision=str(decision_res.decision),
        response_text=decision_res.response_text,
        reasoning=decision_res.reasoning,
        confidence=decision_res.confidence,
        detected_language=decision_res.detected_language,
        citations=decision_res.citations,
        proposed_action=prop_action,
        safety_flags=decision_res.safety_flags,
        latency_ms=latency
    )
