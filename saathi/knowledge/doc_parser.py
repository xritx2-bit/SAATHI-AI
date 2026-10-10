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

    @staticmethod
    def extract_lpg_receipt_fields(text: str) -> Dict[str, Any]:
        """Extracts structured fields from LPG cylinder booking / subsidy cash memos."""
        data = {
            "consumer_id_17_digit": None,
            "distributor_name": None,
            "order_number": None,
            "subsidy_amount": None,
            "total_amount": None
        }
        lpg_id = re.search(r'(?:LPG\s*ID|Consumer\s*ID)[:.\s]*([0-9]{16,17})', text, re.IGNORECASE)
        if lpg_id:
            data["consumer_id_17_digit"] = lpg_id.group(1).strip()

        order_no = re.search(r'(?:Order\s*No|Booking\s*Ref|Ref\s*No)[:.\s]*([A-Z0-9]+)', text, re.IGNORECASE)
        if order_no:
            data["order_number"] = order_no.group(1).strip()

        dist = re.search(r'(?:Agency|Distributor|Gas\s*Agency)[:.\s]*([A-Za-z\s]+)', text, re.IGNORECASE)
        if dist:
            data["distributor_name"] = dist.group(1).strip()

        return data

    @staticmethod
    def extract_rent_fields(text: str) -> Dict[str, Any]:
        """Extracts structured fields from rental agreements and security deposit receipts."""
        data = {
            "monthly_rent": None,
            "security_deposit": None,
            "property_type": "residential",
            "notice_period_months": 1
        }
        rent_match = re.search(r'(?:Monthly\s*Rent|Rent)[:.\s]*(?:Rs\.?|₹)?\s*([0-9,]+)', text, re.IGNORECASE)
        if rent_match:
            try:
                data["monthly_rent"] = float(rent_match.group(1).replace(",", ""))
            except ValueError:
                pass

        dep_match = re.search(r'(?:Security\s*Deposit|Deposit\s*Amount)[:.\s]*(?:Rs\.?|₹)?\s*([0-9,]+)', text, re.IGNORECASE)
        if dep_match:
            try:
                data["security_deposit"] = float(dep_match.group(1).replace(",", ""))
            except ValueError:
                pass

        return data
