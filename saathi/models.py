"""
SAATHI AI - Core Data Models and Schema
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class DocumentChunk(BaseModel):
    id: str
    title: str
    content: str
    source_url_or_file: str
    authority_level: Literal["official_government", "public_utility", "standard_guideline", "user_uploaded"]
    last_updated: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RetrievedEvidence(BaseModel):
    chunk: DocumentChunk
    relevance_score: float
    matched_snippet: str

class DecisionType(str):
    DIRECT_ANSWER = "DIRECT_ANSWER"           # Simple conversation or common knowledge
    RETRIEVE_AND_ANSWER = "RETRIEVE_AND_ANSWER" # Needs factual proof from knowledge base
    CLARIFY = "CLARIFY"                       # Missing necessary information to proceed
    PREPARE_ACTION = "PREPARE_ACTION"         # Draft an official letter, checklist, or calculation
    ESCALATE = "ESCALATE"                     # High-stakes medical/legal emergency or out of scope

class ProposedAction(BaseModel):
    action_id: str
    action_type: Literal["draft_complaint", "generate_checklist", "calculate_estimate", "fill_mock_form"]
    title: str
    draft_content: str
    requires_approval: bool = True
    is_approved: bool = False
    warning_or_disclaimer: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class ControllerDecision(BaseModel):
    decision: str  # DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE
    reasoning: str
    confidence: float
    detected_language: str  # "english", "hindi", "hinglish"
    missing_information: List[str] = Field(default_factory=list)
    retrieved_evidences: List[RetrievedEvidence] = Field(default_factory=list)
    proposed_action: Optional[ProposedAction] = None
    response_text: str
    citations: List[str] = Field(default_factory=list)
    safety_flags: List[str] = Field(default_factory=list)

class EvaluationRecord(BaseModel):
    test_id: str
    query: str
    language: str
    expected_decision: str
    actual_decision: str
    decision_correct: bool
    grounded_evidence: bool
    hallucination_detected: bool
    missing_info_handled: bool
    unapproved_action_count: int = 0
    latency_ms: float
    notes: str = ""
