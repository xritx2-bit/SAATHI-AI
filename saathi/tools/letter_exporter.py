"""
SAATHI AI - Formal Letter & Notice Formatter
Produces formatted, printable HTML/Text grievance letters with official citizen formatting.
"""
from datetime import datetime
from typing import Dict, Any

class LetterExporter:
    @staticmethod
    def generate_printable_html_letter(
        title: str,
        recipient: str,
        subject: str,
        body_content: str,
        applicant_name: str = "[Your Name]",
        contact_number: str = "[Mobile Number]",
        reference_id: str = "[Ref / Consumer No.]"
    ) -> str:
        """
        Generates a clean, professional, printable HTML document suitable for physical submission
        or email attachment to Indian public authorities, Discoms, and Consumer Grievance Cells.
        """
        current_date = datetime.now().strftime("%d %B %Y")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
                body {{
                    font-family: 'Times New Roman', Times, serif;
                    line-height: 1.6;
                    color: #111827;
                    padding: 40px;
                    max-width: 800px;
                    margin: auto;
                    background: #FFFFFF;
                }}
                .letterhead {{
                    text-align: center;
                    border-bottom: 2px solid #1E3A8A;
                    padding-bottom: 12px;
                    margin-bottom: 24px;
                }}
                .letter-date {{
                    text-align: right;
                    margin-bottom: 20px;
                    font-weight: bold;
                }}
                .recipient-box {{
                    margin-bottom: 20px;
                }}
                .subject-line {{
                    font-weight: bold;
                    text-decoration: underline;
                    margin: 18px 0;
                }}
                .letter-body {{
                    white-space: pre-line;
                    text-align: justify;
                    margin-bottom: 30px;
                }}
                .signature-box {{
                    margin-top: 40px;
                    float: right;
                    text-align: left;
                }}
                .footer-notice {{
                    clear: both;
                    font-size: 0.75rem;
                    color: #6B7280;
                    border-top: 1px solid #E5E7EB;
                    padding-top: 10px;
                    margin-top: 60px;
                }}
            </style>
        </head>
        <body>
            <div class="letterhead">
                <h2 style="margin: 0; color: #1E3A8A;">FORMAL CITIZEN GRIEVANCE / NOTICE</h2>
                <div style="font-size: 0.85rem; color: #4B5563;">Prepared via SAATHI AI Citizen Empowerment Portal</div>
            </div>

            <div class="letter-date">Date: {current_date}</div>

            <div class="recipient-box">
                <strong>To,</strong><br>
                {recipient}<br>
                Grievance Redressal Division
            </div>

            <div class="subject-line">
                SUBJECT: {subject} (Ref: {reference_id})
            </div>

            <div class="letter-body">
                {body_content}
            </div>

            <div class="signature-box">
                Yours Sincerely,<br><br><br>
                _______________________<br>
                <strong>{applicant_name}</strong><br>
                Contact: {contact_number}
            </div>

            <div class="footer-notice">
                * Note: This document has been reviewed and approved by the citizen. Certified copy for official correspondence.
            </div>
        </body>
        </html>
        """
        return html
