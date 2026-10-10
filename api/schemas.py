"""
SAATHI AI - REST API Request & Response Schemas (Pydantic v2)
Provides full type validation and interactive OpenAPI/Swagger documentation.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ----------------- Query / Chat Schemas -----------------
class ChatTurn(BaseModel):
    role: str = Field(..., description="Role of the speaker: 'user' or 'assistant'")
    content: str = Field(..., description="Text content of the message")

class QueryRequest(BaseModel):
    user_query: str = Field(
        ...,
        description="The citizen's query in English, Hindi, or Hinglish",
        examples=["Mera bijli ka bill bahut jyada aaya hai meter kharab lagta hai", "What is the procedure for PM Kisan land seeding?"]
    )
    chat_history: Optional[List[ChatTurn]] = Field(
        default=None,
        description="Optional list of previous conversation turns for multi-turn context resolution"
    )
    engine: Optional[str] = Field(
        default="auto",
        description="Inference brain: 'auto', 'local_lora' (RTX 4050 GPU), or 'gemini' (Cloud API)"
    )

class ProposedActionResponse(BaseModel):
    action_id: str
    action_type: str
    title: str
    requires_approval: bool
    draft_content: str
    warning_or_disclaimer: Optional[str] = None

class QueryResponse(BaseModel):
    decision: str = Field(..., description="Policy decision: DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE")
    response_text: str = Field(..., description="Synthesized, safe, and dialect-tailored answer")
    reasoning: str = Field(..., description="Explanation of why this policy was chosen")
    confidence: float = Field(..., description="Confidence score [0.0 - 1.0]")
    detected_language: str = Field(..., description="Detected language / dialect: 'english', 'hindi', or 'hinglish'")
    citations: List[str] = Field(default=[], description="Official regulatory sources and documents cited")
    proposed_action: Optional[ProposedActionResponse] = Field(default=None, description="Prepared formal action draft (if applicable)")
    safety_flags: List[str] = Field(default=[], description="Triggered safety or escalation guardrail tags")
    latency_ms: float = Field(..., description="Server execution time in milliseconds")

# ----------------- Utility Calculator Schemas -----------------
class ElectricityCalcRequest(BaseModel):
    units_consumed: float = Field(..., ge=0, description="Monthly electricity consumption in kWh / Units", examples=[280.0])
    sanctioned_load_kw: float = Field(default=2.0, ge=0.5, description="Sanctioned connected load in kW", examples=[2.0])
    is_average_or_idf: bool = Field(default=False, description="Whether bill is marked Defective Meter / IDF Average assessment")
    state: str = Field(default="Delhi (Standard DERC Benchmark)", description="State tariff framework")

class ElectricityCalcResponse(BaseModel):
    units: float
    sanctioned_load_kw: float
    energy_charge: float
    fixed_charge: float
    electricity_duty: float
    total_estimated_bill: float
    slab_breakdown: List[str]
    is_average_or_idf: bool
    warning: Optional[str]

class TenancyCalcRequest(BaseModel):
    monthly_rent: float = Field(..., ge=1000, description="Agreed monthly rent amount in ₹", examples=[15000.0])
    security_deposit_paid: float = Field(..., ge=0, description="Total deposit paid by tenant in ₹", examples=[45000.0])
    property_type: str = Field(default="residential", description="'residential' (max 2 months) or 'commercial' (max 6 months)")
    actual_damages: float = Field(default=0.0, ge=0, description="Genuine documented structural damage costs in ₹")
    unpaid_bills: float = Field(default=0.0, ge=0, description="Pending electricity / water dues in ₹")

class TenancyCalcResponse(BaseModel):
    legal_max_deposit: float
    excess_held_by_landlord: float
    total_allowable_deductions: float
    refundable_amount: float
    statutory_deadline_days: int
    notes: List[str]

class PFAdvanceCalcRequest(BaseModel):
    employee_pf_share: float = Field(..., ge=1000, description="Employee's total accumulated PF contribution in ₹", examples=[120000.0])
    employer_pf_share: float = Field(..., ge=0, description="Employer's total accumulated PF contribution in ₹", examples=[40000.0])
    basic_plus_da: float = Field(..., ge=1000, description="Monthly basic salary plus Dearness Allowance (DA) in ₹", examples=[25000.0])
    purpose: str = Field(default="Illness / Medical", description="'Illness / Medical', 'Marriage', 'House Purchase / Construction', 'General Emergency'")
    service_years: float = Field(default=3.5, ge=0.0, description="Total continuous service in years", examples=[3.5])

class PFAdvanceCalcResponse(BaseModel):
    max_withdrawable_amount: float
    status: str
    purpose: str
    notes: List[str]

# ----------------- Document Parser & Export Schemas -----------------
class DocumentParseRequest(BaseModel):
    raw_text: str = Field(..., description="Raw text of utility bill, rent agreement, or subsidy receipt", examples=["CA No: 102938475, Units: 420 kWh, Total Amount: Rs 3450, Due Date: 25/11/2026, IDF Defective Reading"])

class DocumentParseResponse(BaseModel):
    electricity_fields: Dict[str, Any]
    lpg_fields: Dict[str, Any]
    tenancy_fields: Dict[str, Any]

class PDFExportRequest(BaseModel):
    title: str = Field(..., description="Title of the complaint or notice", examples=["Formal Complaint to Tata Power for Excessive Meter Billing"])
    content: str = Field(..., description="Body of the formal letter")
    applicant_name: str = Field(default="Citizen Applicant", description="Name of the applicant for signature box")
    reference_docket_id: Optional[str] = Field(default=None, description="Optional custom docket number")

# ----------------- Knowledge Base Schemas -----------------
class KnowledgeChunkResponse(BaseModel):
    id: str
    title: str
    content: str
    source_url_or_file: str
    authority_level: str
    last_updated: str
    category: str

class RetrieveRequest(BaseModel):
    query: str = Field(..., description="Search query across vetted government guidelines", examples=["PM Kisan land seeding eKYC procedure"])
    top_k: int = Field(default=3, ge=1, le=10, description="Number of relevant chunks to retrieve")

class RetrieveResponse(BaseModel):
    query: str
    total_retrieved: int
    results: List[Dict[str, Any]]
