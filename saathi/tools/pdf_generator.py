"""
SAATHI AI - Official PDF Document & Legal Letter Generator
Generates clean, printable, professional PDF documents for citizen grievances,
utility audit certificates, and formal tenancy deposit demand notices.
Supports full Unicode, Devanagari (Hindi), Indian Rupee (₹) symbol, and text shaping via fpdf2 & uharfbuzz.
"""
import os
import time
import re
from typing import Optional, Dict, Any, Tuple
from fpdf import FPDF, XPos, YPos

def _setup_pdf_fonts(pdf: FPDF) -> Tuple[str, bool]:
    """
    Configures embedded Unicode and Indic fonts with text shaping when available on the system.
    Falls back gracefully to core Helvetica fonts if custom TTFs are unavailable.
    """
    # Candidate font paths for Devanagari & Latin Unicode
    dejavu_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    dejavu_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    noto_dev_reg = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
    noto_dev_bold = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"

    has_dejavu = os.path.exists(dejavu_reg) and os.path.exists(dejavu_bold)
    has_noto_dev = os.path.exists(noto_dev_reg) and os.path.exists(noto_dev_bold)

    if has_dejavu:
        pdf.add_font("DejaVu", "", dejavu_reg)
        pdf.add_font("DejaVu", "B", dejavu_bold)
        fallback_list = ["DejaVu"]

        if has_noto_dev:
            pdf.add_font("NotoDevanagari", "", noto_dev_reg)
            pdf.add_font("NotoDevanagari", "B", noto_dev_bold)
            fallback_list.insert(0, "NotoDevanagari")

        try:
            pdf.set_fallback_fonts(fallback_list)
        except Exception:
            pass

        # Enable text shaping for Indic complex scripts / conjuncts
        try:
            pdf.set_text_shaping(True)
        except Exception:
            pass

        return "DejaVu", True

    return "Helvetica", False

def _clean_text(text: str, is_unicode_font: bool = True) -> str:
    """
    Normalizes text without stripping non-ASCII characters when Unicode fonts are loaded.
    If running in legacy ASCII fallback mode, safely maps unsupported symbols.
    """
    if not text:
        return ""
    # Strip zero-width and invisible characters
    text = text.replace("\u200b", "").replace("\ufeff", "")
    
    if is_unicode_font:
        # Preserve full Unicode, Devanagari Hindi, and symbol glyphs
        return text

    # Legacy ASCII fallback mapping
    replacements = {
        "—": "-",
        "–": "-",
        "•": "*",
        "₹": "Rs. ",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return text.encode("ascii", "replace").decode("ascii")

class SaathiPDFGenerator:
    @staticmethod
    def generate_complaint_letter_pdf(
        title: str,
        content: str,
        author_name: str = "Citizen Applicant",
        ref_id: Optional[str] = None
    ) -> bytes:
        """
        Creates an official formatted PDF letter with letterhead, reference docket, and signature box.
        """
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        
        font_name, is_unicode = _setup_pdf_fonts(pdf)
        pdf.add_page()
        
        # Letterhead Header
        pdf.set_fill_color(15, 23, 42) # Slate Dark
        pdf.rect(0, 0, 210, 24, 'F')
        
        pdf.set_font(font_name, style="B", size=13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 6)
        pdf.cell(0, 8, _clean_text("SAATHI AI — CITIZEN GRIEVANCE REDRESSAL DRAFT", is_unicode))
        pdf.set_font(font_name, size=9)
        pdf.set_xy(15, 14)
        pdf.cell(0, 5, _clean_text("Official Citizen Assistance Portal • Grounded in Indian Regulatory Framework", is_unicode))

        pdf.ln(12)
        pdf.set_text_color(30, 41, 59) # Slate 800

        # Docket Reference & Date
        docket = ref_id or f"SAATHI-ACT-{int(time.time())}"
        date_str = time.strftime("%d %B %Y")
        
        pdf.set_font(font_name, style="B", size=10)
        pdf.cell(100, 6, _clean_text(f"Docket Reference: {docket}", is_unicode))
        pdf.set_font(font_name, size=10)
        pdf.cell(0, 6, _clean_text(f"Date: {date_str}", is_unicode), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
        
        pdf.set_draw_color(203, 213, 225)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(6)

        # Subject Title
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109) # Primary Blue
        pdf.multi_cell(0, 7, _clean_text(f"SUBJECT: {title.upper()}", is_unicode))
        pdf.ln(4)

        # Body Content
        pdf.set_font(font_name, size=10)
        pdf.set_text_color(51, 65, 85)
        
        clean_body = _clean_text(content, is_unicode)
        for line in clean_body.split('\n'):
            pdf.multi_cell(0, 6, line)
            pdf.ln(1)

        pdf.ln(8)

        # Verification & Signature Box
        pdf.set_draw_color(226, 232, 240)
        pdf.set_fill_color(248, 250, 252)
        y_pos = pdf.get_y()
        if y_pos > 230:
            pdf.add_page()
            y_pos = pdf.get_y()
            
        pdf.rect(15, y_pos, 180, 32, 'DF')
        pdf.set_xy(20, y_pos + 4)
        pdf.set_font(font_name, style="B", size=9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 5, _clean_text("APPLICANT DECLARATION & SIGNATURE:", is_unicode))
        pdf.set_font(font_name, size=8)
        pdf.set_text_color(100, 116, 139)
        pdf.set_xy(20, y_pos + 10)
        pdf.cell(0, 4, _clean_text("I hereby affirm that the facts stated above are true and accurate to the best of my knowledge.", is_unicode))
        pdf.set_xy(120, y_pos + 22)
        pdf.set_font(font_name, style="B", size=9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(70, 5, _clean_text(f"Signature: {author_name}", is_unicode), align="R")

        # Footer
        pdf.set_y(-12)
        pdf.set_font(font_name, size=7)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 5, _clean_text("Generated via SAATHI AI • Consumer Rights & Regulatory Guidance Platform • https://github.com/xritx2-bit/SAATHI-AI", is_unicode), align="C")

        return bytes(pdf.output())

    @staticmethod
    def generate_bill_audit_pdf(audit_data: Dict[str, Any]) -> bytes:
        """
        Creates an official Electricity / Utility Bill Audit Certificate.
        """
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        
        font_name, is_unicode = _setup_pdf_fonts(pdf)
        pdf.add_page()

        # Header
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(0, 0, 210, 24, 'F')
        pdf.set_font(font_name, style="B", size=13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 6)
        pdf.cell(0, 8, _clean_text("SAATHI AI — UTILITY TARIFF AUDIT REPORT", is_unicode))
        pdf.set_font(font_name, size=9)
        pdf.set_xy(15, 14)
        pdf.cell(0, 5, _clean_text("Independent Consumer Electricity Tariff Verification & Slab Analysis", is_unicode))

        pdf.ln(12)
        pdf.set_text_color(30, 41, 59)

        date_str = time.strftime("%d %B %Y, %H:%M")
        pdf.set_font(font_name, style="B", size=10)
        pdf.cell(100, 6, _clean_text(f"Audit ID: AUD-{int(time.time())}", is_unicode))
        pdf.cell(0, 6, _clean_text(f"Generated: {date_str}", is_unicode), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(6)

        # Summary Table
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("1. CONSUMER BILL PARAMETERS", is_unicode), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        for k, v in audit_data.get("inputs", {}).items():
            pdf.cell(80, 6, _clean_text(f"{k}:", is_unicode), border=1)
            pdf.cell(100, 6, _clean_text(f"{v}", is_unicode), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(6)
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("2. SLAB & TARIFF CALCULATION BREAKDOWN", is_unicode), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        for k, v in audit_data.get("breakdown", {}).items():
            pdf.cell(80, 6, _clean_text(f"{k}:", is_unicode), border=1)
            pdf.cell(100, 6, _clean_text(f"{v}", is_unicode), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(6)
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("3. REGULATORY GUIDELINES & DISCOM ESCALATION", is_unicode), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 5, _clean_text(
            "If your actual bill significantly exceeds the estimated tariff above:\n"
            "1. Check if the bill was calculated on Average / IDF basis instead of actual meter reading.\n"
            "2. File a formal test check request under Section 55 of the Electricity Act 2003.\n"
            "3. Escalate unresolved disputes to the Consumer Grievance Redressal Forum (CGRF).",
            is_unicode
        ))

        return bytes(pdf.output())
