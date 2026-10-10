"""
SAATHI AI - Document Parser & Field Extractor
Parses everyday Indian utility bills, receipts, and notice text to extract key operational fields.
"""
import re
from typing import Dict, Any, Optional

class DocumentParser:
    @staticmethod
    def extract_electricity_bill_fields(text: str) -> Dict[str, Any]:
        """
        Extracts structured fields from electricity bill text:
        - Consumer / Account Number (CA No)
        - Units Consumed / kWh
        - Sanctioned Load (kW)
        - Total Bill Amount (₹)
        - Due Date
        - Reading Type (Actual vs Average/IDF)
        """
        data = {
            "consumer_number": None,
            "units_consumed": None,
            "sanctioned_load_kw": 2.0,
            "total_amount": None,
            "due_date": None,
            "is_average_or_idf": False
        }

        # Consumer number patterns
        ca_match = re.search(r'(?:CA\s*No|Consumer\s*No|Account\s*ID|K\s*No|Connection\s*No)[:.\s]*([A-Z0-9\-]+)', text, re.IGNORECASE)
        if ca_match:
            data["consumer_number"] = ca_match.group(1).strip()

        # Units consumed
        units_match = re.search(r'(?:Units|Consumption|kWh|Billed\s*Units)[:.\s]*([0-9]+(?:\.[0-9]+)?)', text, re.IGNORECASE)
        if units_match:
            try:
                data["units_consumed"] = float(units_match.group(1))
            except ValueError:
                pass

        # Sanctioned load
        load_match = re.search(r'(?:Sanctioned\s*Load|Connected\s*Load|Load)[:.\s]*([0-9]+(?:\.[0-9]+)?)\s*(?:kW|KW|HP)?', text, re.IGNORECASE)
        if load_match:
            try:
                data["sanctioned_load_kw"] = float(load_match.group(1))
            except ValueError:
                pass

        # Total amount
        amt_match = re.search(r'(?:Total\s*Amount|Net\s*Payable|Bill\s*Amount|Payable\s*Amount)[:.\s]*(?:Rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]+)?)', text, re.IGNORECASE)
        if amt_match:
            clean_amt = amt_match.group(1).replace(",", "")
            try:
                data["total_amount"] = float(clean_amt)
            except ValueError:
                pass

        # Due Date
        date_match = re.search(r'(?:Due\s*Date|Pay\s*by)[:.\s]*([0-9]{1,2}[-/.][0-9]{1,2}[-/.][0-9]{2,4})', text, re.IGNORECASE)
        if date_match:
            data["due_date"] = date_match.group(1).strip()

        # IDF or Average check
        if re.search(r'\b(IDF|Defective|Average\s*Reading|Estimated|Provisional)\b', text, re.IGNORECASE):
            data["is_average_or_idf"] = True

        return data
