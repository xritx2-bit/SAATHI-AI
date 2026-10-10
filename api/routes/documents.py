"""
SAATHI AI - Document Parser & Official PDF Export API Routes
"""
import time
from fastapi import APIRouter, Response, HTTPException
from api.schemas import DocumentParseRequest, DocumentParseResponse, PDFExportRequest
from saathi.knowledge.doc_parser import DocumentParser
from saathi.tools.pdf_generator import SaathiPDFGenerator

router = APIRouter(prefix="/documents", tags=["Document Parser & PDF Generator"])

@router.post("/parse", response_model=DocumentParseResponse, summary="Extract Structured Operational Fields from Unstructured Bill / Notice Text")
async def parse_document(req: DocumentParseRequest):
    """
    Extracts Account numbers, Units, Surcharge, Due Dates, and Gas IDs using pattern matchers across:
    1. Electricity Bills (CA No, Units, Amount, IDF Flag)
    2. LPG Gas Subsidies (17-digit ID, Agency, Ref No)
    3. Tenancy Agreements (Monthly Rent, Deposit)
    """
    elec = DocumentParser.extract_electricity_bill_fields(req.raw_text)
    lpg = DocumentParser.extract_lpg_receipt_fields(req.raw_text)
    rent = DocumentParser.extract_rent_fields(req.raw_text)

    return DocumentParseResponse(
        electricity_fields=elec,
        lpg_fields=lpg,
        tenancy_fields=rent
    )

@router.post("/export-pdf", summary="Generate Downloadable Official Letterhead PDF")
async def export_pdf(req: PDFExportRequest):
    """
    Generates a formatted PDF legal letter with official letterhead, docket number, date, and signature box.
    Returns binary `application/pdf` stream directly downloadable in browsers and mobile apps.
    """
    try:
        pdf_bytes = SaathiPDFGenerator.generate_complaint_letter_pdf(
            title=req.title,
            content=req.content,
            author_name=req.applicant_name,
            ref_id=req.reference_docket_id
        )
        filename = f"SAATHI_Letter_{int(time.time())}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
