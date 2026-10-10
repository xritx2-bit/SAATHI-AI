"""
SAATHI AI - Production REST API Server (FastAPI)
Provides enterprise-grade, evidence-gated, multilingual public assistance endpoints
for mobile apps, WhatsApp chatbots, civic portals, and external developer integrations.
"""
import time
import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes.query import router as query_router
from api.routes.tools import router as tools_router
from api.routes.documents import router as documents_router
from api.routes.knowledge import router as knowledge_router
from saathi.llm.local_model import LocalFineTunedModel

app = FastAPI(
    title="SAATHI AI (साथी) — Public Assistance REST API",
    description="""
    # 🇮🇳 SAATHI AI — Next-Generation Public Assistance & Regulatory Intelligence API
    
    An evidence-gated, safe, multilingual REST API designed to solve everyday Indian civic, utility, and legal challenges.
    
    ### 🚀 Key Capabilities:
    * **🧠 Evidence-Gated Decision Controller:** Routes inputs between Direct Answers, Multi-turn Clarifications, Hybrid RAG, and Human Approval Action Gates.
    * **🛡️ Zero-Trust Safety:** Intercepts 112/108/1930 emergencies, suicidal crisis protocols (Tele-MANAS), and sensitive financial data leakage.
    * **🗣️ Multilingual Dialect Support:** 100% decision consistency across **English**, **हिंदी (Hindi)**, and **Hinglish**.
    * **🧮 Indian Utility Calculators:** Electricity slab tariffs (DERC/DISCOM), Model Tenancy security deposit limits, and EPFO Form 31 PF advances.
    * **📄 Document Field Parser & Official PDF Export:** Extracts structured bill fields and generates official legal grievance PDF letterheads.
    * **💻 Fine-Tuned Model Support:** Integrated local QLoRA inference on NVIDIA RTX 4050 GPU.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "SAATHI AI Engineering & Research Team",
        "url": "https://github.com/xritx2-bit/SAATHI-AI",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Enable CORS for all frontends (React, Flutter, Vue, Streamlit, Mobile apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# Mount API Routers under /api/v1
app.include_router(query_router, prefix="/api/v1")
app.include_router(tools_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    """Root landing endpoint with interactive documentation links."""
    return {
        "service": "SAATHI AI REST API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_spec": "/openapi.json"
        },
        "endpoints": {
            "query": "POST /api/v1/query",
            "electricity_calc": "POST /api/v1/tools/calculate-electricity",
            "tenancy_calc": "POST /api/v1/tools/calculate-tenancy-deposit",
            "pf_advance_calc": "POST /api/v1/tools/calculate-pf-advance",
            "document_parser": "POST /api/v1/documents/parse",
            "pdf_generator": "POST /api/v1/documents/export-pdf",
            "knowledge_chunks": "GET /api/v1/knowledge/chunks",
            "knowledge_retrieve": "POST /api/v1/knowledge/retrieve",
            "health": "GET /api/v1/health"
        }
    }

@app.get("/api/v1/health", tags=["System Health"])
async def health_check():
    """System health check and GPU / LoRA adapter status."""
    import torch
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else "CPU"
    adapter_ready = LocalFineTunedModel.is_available()

    return {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hardware": {
            "cuda_available": cuda_available,
            "device": gpu_name,
            "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2) if cuda_available else 0.0
        },
        "fine_tuned_model": {
            "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
            "adapter_status": "READY" if adapter_ready else "NOT_LOADED",
            "adapter_path": "training/saathi_lora_adapter"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
