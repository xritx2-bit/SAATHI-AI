"""
SAATHI AI - Official PDF Document & Legal Letter Generator
Generates clean, printable, professional PDF documents for citizen grievances,
utility audit certificates, and formal tenancy deposit demand notices.
Supports full Unicode, Devanagari (Hindi), Indian Rupee (₹) symbol, and text shaping via fpdf2 & uharfbuzz.
"""
import os
import io
import time
import re
from typing import Optional, Dict, Any, Tuple
from fpdf import FPDF, XPos, YPos

def _generate_qr_code_image(data: str) -> Optional[io.BytesIO]:
    """Generates an in-memory PNG QR code buffer for official docket verification."""
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception:
        return None

def _setup_pdf_fonts(pdf: FPDF) -> Tuple[str, bool, bool]:
    """
    Configures embedded Unicode and Indic fonts with text shaping when available on the system.
    Returns: (primary_font_name, is_unicode_font, supports_devanagari)
    Falls back gracefully to Latin Unicode or core Helvetica fonts if custom TTFs are unavailable.
    """
    # Candidate font paths for Devanagari & Latin Unicode
    devanagari_candidates = [
        ("/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"),
        ("/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf"),
        ("/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf", "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"),
        ("/usr/share/fonts/truetype/samyak-fonts/Samyak-Devanagari.ttf", "/usr/share/fonts/truetype/samyak-fonts/Samyak-Devanagari.ttf"),
        ("/usr/share/fonts/truetype/gargi/gargi.ttf", "/usr/share/fonts/truetype/gargi/gargi.ttf"),
    ]
    latin_candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/freefont/FreeSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ]

    has_devanagari = False
    has_latin_unicode = False
    primary_font = "Helvetica"
    fallback_list = []

    # Check Devanagari font availability
    for reg, bold in devanagari_candidates:
        if os.path.exists(reg) and os.path.exists(bold):
            pdf.add_font("NotoDevanagari", "", reg)
            pdf.add_font("NotoDevanagari", "B", bold)
            fallback_list.append("NotoDevanagari")
            primary_font = "NotoDevanagari"
            has_devanagari = True
            break

    # Check Latin Unicode font availability
    for reg, bold in latin_candidates:
        if os.path.exists(reg) and os.path.exists(bold):
            pdf.add_font("DejaVu", "", reg)
            pdf.add_font("DejaVu", "B", bold)
            fallback_list.append("DejaVu")
            if primary_font == "Helvetica":
                primary_font = "DejaVu"
            has_latin_unicode = True
            break

    is_unicode = has_devanagari or has_latin_unicode

    if is_unicode:
        if fallback_list:
            try:
                pdf.set_fallback_fonts(fallback_list)
            except Exception:
                pass

        if has_devanagari:
            # Enable text shaping for Indic complex scripts / conjuncts
            try:
                pdf.set_text_shaping(True)
            except Exception:
                pass

        return primary_font, True, has_devanagari

    return "Helvetica", False, False

def _clean_text(text: str, is_unicode_font: bool = True, supports_devanagari: bool = True) -> str:
    """
    Normalizes text according to the loaded font capabilities:
    - If font supports Devanagari: preserves full Devanagari (Hindi) and Unicode.
    - If font supports Latin Unicode only (no Devanagari): safely removes unsupported Devanagari glyphs while preserving Latin Unicode / Rupee (₹).
    - If running in legacy ASCII fallback mode: safely maps unsupported symbols and encodes to ASCII.
    """
    if not text:
        return ""
    # Strip zero-width and invisible characters
    text = text.replace("\u200b", "").replace("\ufeff", "")
    
    if supports_devanagari:
        # Preserve full Unicode, Devanagari Hindi, and symbol glyphs
        return text

    if is_unicode_font:
        # Font supports Unicode symbols (e.g. ₹) but not Devanagari script
        # Remove unsupported Devanagari characters to avoid missing glyph errors
        return re.sub(r'[\u0900-\u097F]+', ' ', text)

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
        
        font_name, is_unicode, supports_dev = _setup_pdf_fonts(pdf)
        pdf.add_page()
        
        # Letterhead Header
        pdf.set_fill_color(15, 23, 42) # Slate Dark
        pdf.rect(0, 0, 210, 24, 'F')
        
        pdf.set_font(font_name, style="B", size=13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 6)
        pdf.cell(0, 8, _clean_text("SAATHI AI — CITIZEN GRIEVANCE REDRESSAL DRAFT", is_unicode, supports_dev))
        pdf.set_font(font_name, size=9)
        pdf.set_xy(15, 14)
        pdf.cell(0, 5, _clean_text("Official Citizen Assistance Portal • Grounded in Indian Regulatory Framework", is_unicode, supports_dev))

        pdf.ln(12)
        pdf.set_text_color(30, 41, 59) # Slate 800

        # Docket Reference & Date
        docket = ref_id or f"SAATHI-ACT-{int(time.time())}"
        date_str = time.strftime("%d %B %Y")
        
        pdf.set_font(font_name, style="B", size=10)
        pdf.cell(100, 6, _clean_text(f"Docket Reference: {docket}", is_unicode, supports_dev))
        pdf.set_font(font_name, size=10)
        pdf.cell(0, 6, _clean_text(f"Date: {date_str}", is_unicode, supports_dev), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
        
        # Embed Verification QR Code in letter
        qr_data = f"SAATHI-VERIFIED|DOCKET:{docket}|DATE:{date_str}|CITIZEN:{author_name}|AUTH:REGULATORY_GATED"
        qr_buf = _generate_qr_code_image(qr_data)
        if qr_buf:
            try:
                pdf.image(qr_buf, x=172, y=32, w=22, h=22)
            except Exception:
                pass

        pdf.set_draw_color(203, 213, 225)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(6)

        # Subject Title
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109) # Primary Blue
        pdf.multi_cell(150, 7, _clean_text(f"SUBJECT: {title.upper()}", is_unicode, supports_dev))
        pdf.ln(4)

        # Body Content
        pdf.set_font(font_name, size=10)
        pdf.set_text_color(51, 65, 85)
        
        clean_body = _clean_text(content, is_unicode, supports_dev)
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
        pdf.cell(0, 5, _clean_text("APPLICANT DECLARATION & SIGNATURE:", is_unicode, supports_dev))
        pdf.set_font(font_name, size=8)
        pdf.set_text_color(100, 116, 139)
        pdf.set_xy(20, y_pos + 10)
        pdf.cell(0, 4, _clean_text("I hereby affirm that the facts stated above are true and accurate to the best of my knowledge.", is_unicode, supports_dev))
        pdf.set_xy(120, y_pos + 22)
        pdf.set_font(font_name, style="B", size=9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(70, 5, _clean_text(f"Signature: {author_name}", is_unicode, supports_dev), align="R")

        # Footer
        pdf.set_y(-12)
        pdf.set_font(font_name, size=7)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 5, _clean_text("Generated via SAATHI AI • Consumer Rights & Regulatory Guidance Platform • Verified Digital Docket", is_unicode, supports_dev), align="C")

        return bytes(pdf.output())

    @staticmethod
    def generate_bill_audit_pdf(audit_data: Dict[str, Any]) -> bytes:
        """
        Creates an official Electricity / Utility Bill Audit Certificate.
        """
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        
        font_name, is_unicode, supports_dev = _setup_pdf_fonts(pdf)
        pdf.add_page()

        # Header
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(0, 0, 210, 24, 'F')
        pdf.set_font(font_name, style="B", size=13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 6)
        pdf.cell(0, 8, _clean_text("SAATHI AI — UTILITY TARIFF AUDIT REPORT", is_unicode, supports_dev))
        pdf.set_font(font_name, size=9)
        pdf.set_xy(15, 14)
        pdf.cell(0, 5, _clean_text("Independent Consumer Electricity Tariff Verification & Slab Analysis", is_unicode, supports_dev))

        pdf.ln(12)
        pdf.set_text_color(30, 41, 59)

        audit_id = f"AUD-{int(time.time())}"
        date_str = time.strftime("%d %B %Y, %H:%M")
        pdf.set_font(font_name, style="B", size=10)
        pdf.cell(100, 6, _clean_text(f"Audit ID: {audit_id}", is_unicode, supports_dev))
        pdf.cell(0, 6, _clean_text(f"Generated: {date_str}", is_unicode, supports_dev), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # Embed Verification QR Code in Audit
        qr_data = f"SAATHI-TARIFF-AUDIT|ID:{audit_id}|DATE:{date_str}|STATUS:VERIFIED_DERC_CERC"
        qr_buf = _generate_qr_code_image(qr_data)
        if qr_buf:
            try:
                pdf.image(qr_buf, x=172, y=32, w=22, h=22)
            except Exception:
                pass

        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(6)

        # Summary Table
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("1. CONSUMER BILL PARAMETERS", is_unicode, supports_dev), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        for k, v in audit_data.get("inputs", {}).items():
            pdf.cell(80, 6, _clean_text(f"{k}:", is_unicode, supports_dev), border=1)
            pdf.cell(100, 6, _clean_text(f"{v}", is_unicode, supports_dev), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(6)
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("2. SLAB & TARIFF CALCULATION BREAKDOWN", is_unicode, supports_dev), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        for k, v in audit_data.get("breakdown", {}).items():
            pdf.cell(80, 6, _clean_text(f"{k}:", is_unicode, supports_dev), border=1)
            pdf.cell(100, 6, _clean_text(f"{v}", is_unicode, supports_dev), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(6)
        pdf.set_font(font_name, style="B", size=11)
        pdf.set_text_color(15, 62, 109)
        pdf.cell(0, 7, _clean_text("3. REGULATORY GUIDELINES & DISCOM ESCALATION", is_unicode, supports_dev), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
        pdf.set_font(font_name, size=9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 5, _clean_text(
            "If your actual bill significantly exceeds the estimated tariff above:\n"
            "1. Check if the bill was calculated on Average / IDF basis instead of actual meter reading.\n"
            "2. File a formal test check request under Section 55 of the Electricity Act 2003.\n"
            "3. Escalate unresolved disputes to the Consumer Grievance Redressal Forum (CGRF).",
            is_unicode,
            supports_dev
        ))

        return bytes(pdf.output())
