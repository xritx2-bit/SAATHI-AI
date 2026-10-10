"""
SAATHI Knowledge Store & Document Ingestion Engine
Handles document loading, chunking, source tracking, and metadata tagging.
"""
import os
import json
import glob
from typing import List, Dict, Any, Optional
from saathi.models import DocumentChunk

class KnowledgeStore:
    def __init__(self, data_dir: str = "data/sample_docs"):
        self.data_dir = data_dir
        self.chunks: List[DocumentChunk] = []
        self._load_all_documents()

    def _load_all_documents(self):
        """Loads vetted documents from JSON, Markdown, or text files in the data directory."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            self._create_default_vetted_docs()

        # Load JSON format docs
        for file_path in glob.glob(os.path.join(self.data_dir, "*.json")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            self.chunks.append(DocumentChunk(**item))
                    elif isinstance(data, dict):
                        if "chunks" in data:
                            for item in data["chunks"]:
                                self.chunks.append(DocumentChunk(**item))
                        else:
                            self.chunks.append(DocumentChunk(**data))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        # Load Markdown/Text format docs
        for file_path in glob.glob(os.path.join(self.data_dir, "*.md")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    filename = os.path.basename(file_path)
                    title = filename.replace(".md", "").replace("_", " ").title()
                    
                    # Split markdown into sections by '## '
                    sections = content.split("## ")
                    for idx, sec in enumerate(sections):
                        sec_text = sec.strip()
                        if not sec_text:
                            continue
                        lines = sec_text.split("\n", 1)
                        sec_title = lines[0].strip() if len(lines) > 0 else f"Section {idx}"
                        body = lines[1].strip() if len(lines) > 1 else sec_text
                        
                        chunk = DocumentChunk(
                            id=f"{filename}_{idx}",
                            title=f"{title} - {sec_title}",
                            content=body,
                            source_url_or_file=file_path,
                            authority_level="standard_guideline",
                            last_updated="2026-10-01",
                            metadata={"filename": filename, "section": sec_title}
                        )
                        self.chunks.append(chunk)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    def add_user_document(self, filename: str, content: str) -> List[DocumentChunk]:
        """Allows users to upload their own bill, notice, or document dynamically."""
        new_chunks = []
        paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 30]
        if not paragraphs:
            paragraphs = [content.strip()]

        for idx, p in enumerate(paragraphs):
            chunk = DocumentChunk(
                id=f"user_{filename}_{idx}",
                title=f"Uploaded Document: {filename} (Part {idx+1})",
                content=p,
                source_url_or_file=filename,
                authority_level="user_uploaded",
                last_updated="Just now",
                metadata={"user_doc": True, "filename": filename}
            )
            self.chunks.append(chunk)
            new_chunks.append(chunk)
        return new_chunks

    def _create_default_vetted_docs(self):
        """Creates authoritative default knowledge files if directory is empty."""
        default_docs = [
            {
                "id": "elec_bill_01",
                "title": "Electricity Bill Components & Slab Tariffs (India)",
                "content": "An electricity bill in India consists of: 1) Fixed Demand Charges (Rs/kW based on sanctioned load), 2) Energy Charges (calculated per kWh/unit consumed based on telescopic slabs, e.g. 0-100 units @ Rs 3.50, 101-300 units @ Rs 6.00), 3) Fuel Surcharge / PPAC, 4) Electricity Duty & State Tax, and 5) Late Payment Surcharge (typically 1.25% to 1.5% per month if unpaid by due date). If reading is marked 'Average' or 'Defective Meter (IDF)', the bill is estimated and must be corrected by applying for meter testing.",
                "source_url_or_file": "National Electricity Regulatory Advisory Guide 2026",
                "authority_level": "public_utility",
                "last_updated": "2026-08-15",
                "metadata": {"category": "utilities", "topic": "electricity"}
            },
            {
                "id": "elec_bill_02",
                "title": "Disputing a High Electricity Bill / Faulty Meter",
                "content": "If you receive an abnormally high electricity bill: Step 1: Verify the current meter reading against the reading printed on the bill. Step 2: Check if Sanctioned Load has been arbitrarily increased (MDI Penalty). Step 3: If reading is wrong or meter is running fast, file a grievance with the Sub-Divisional Office (SDO/AE) or online portal. Step 4: Pay undisputed base amount under protest to avoid disconnection while the complaint is pending. Step 5: If unresolved in 30 days, escalate to the Consumer Grievance Redressal Forum (CGRF) and Electricity Ombudsman.",
                "source_url_or_file": "Electricity Regulatory Commission Grievance Redressal Regulations",
                "authority_level": "official_government",
                "last_updated": "2026-09-01",
                "metadata": {"category": "utilities", "topic": "dispute_process"}
            },
            {
                "id": "pmkisan_01",
                "title": "PM-KISAN Samman Nidhi Yojana: Eligibility & Benefit",
                "content": "Under PM-KISAN, eligible landholding farmer families receive an income support of Rs 6,000 per year, payable in three equal four-monthly installments of Rs 2,000 directly into Aadhaar-seeded bank accounts (DBT). Eligibility requires cultivable landholding in revenue records. Ineligible persons: institutional landholders, farmer families holding constitutional posts, serving/retired government officers, income tax payees of last assessment year, and professionals (doctors, engineers, lawyers, CAs).",
                "source_url_or_file": "Ministry of Agriculture & Farmers Welfare (pmkisan.gov.in)",
                "authority_level": "official_government",
                "last_updated": "2026-09-20",
                "metadata": {"category": "government_schemes", "topic": "pm_kisan"}
            },
            {
                "id": "pmkisan_02",
                "title": "PM-KISAN: Solving Pending Installment / eKYC / Land Seeding Errors",
                "content": "If PM-KISAN 2,000 installment is stopped or pending: 1) eKYC Mandatory: Complete OTP-based eKYC on pmkisan.gov.in using Aadhaar mobile number, or biometric eKYC at CSC center. 2) Land Seeding (Bhulekh): Check 'Know Your Status' on portal; if Land Seeding is 'NO', submit copy of Khatoni / Land Record to Local Patwari or District Agriculture Office. 3) Bank Aadhaar Seeding: Check NPCI / DBT status at your bank branch to ensure Aadhaar is mapped to your active bank account. 4) Correction: Update spelling errors in Aadhaar name online.",
                "source_url_or_file": "PM-KISAN Portal Operational SOP",
                "authority_level": "official_government",
                "last_updated": "2026-10-01",
                "metadata": {"category": "government_schemes", "topic": "pm_kisan_troubleshooting"}
            },
            {
                "id": "lpg_pahel_01",
                "title": "PAHEL (DBTL) LPG Cylinder Subsidy Rules",
                "content": "Under PAHEL (DBTL), domestic LPG consumers pay the non-subsidized price when booking a cylinder (14.2 kg), and the eligible government subsidy is transferred directly to their Aadhaar-linked bank account within 2-3 business days. Quota is up to 12 subsidized cylinders per financial year per household. Aadhaar seeding in both LPG 17-digit Consumer ID and Bank account is mandatory for DBT transfers.",
                "source_url_or_file": "Ministry of Petroleum and Natural Gas (myLPG.in)",
                "authority_level": "official_government",
                "last_updated": "2026-07-10",
                "metadata": {"category": "subsidies", "topic": "lpg"}
            },
            {
                "id": "lpg_pahel_02",
                "title": "LPG Subsidy Not Credited: Redressal Steps",
                "content": "If LPG subsidy is not received after cylinder delivery: Step 1: Check cylinder cash memo for 17-digit LPG ID and payment status. Step 2: Check cylinder subsidy transfer history on mylpg.in or distributor portal. Step 3: Check if annual quota of 12 cylinders has exceeded. Step 4: Verify bank account linkage status (NPCI mapping). Step 5: Call Toll-Free helpline 1800-2333-555 or file a complaint on MoP&NG e-Sewa / Umang app.",
                "source_url_or_file": "MoP&NG Citizen Charter",
                "authority_level": "official_government",
                "last_updated": "2026-08-01",
                "metadata": {"category": "subsidies", "topic": "lpg_complaint"}
            },
            {
                "id": "tenant_01",
                "title": "Tenant Rights & Security Deposit Refund Rules",
                "content": "Under Model Tenancy guidelines and standard Indian rental agreements: 1) Security deposit for residential premises is typically 1 to 2 months' rent (varies by city). 2) Landlord must refund the security deposit upon tenant vacating and handover of keys, deducting only verified unpaid utility bills or structural damage beyond reasonable wear-and-tear. 3) Notice Period: Standard notice period is 30 days as specified in the agreement. 4) Rent Increment: Cannot be increased mid-tenure unless expressly stated in the written agreement (standard is 5-10% annually upon renewal). 5) Essential Services: Landlord cannot cut off electricity or water supply under any dispute.",
                "source_url_or_file": "Ministry of Housing and Urban Affairs Model Tenancy Guidelines",
                "authority_level": "standard_guideline",
                "last_updated": "2026-06-15",
                "metadata": {"category": "housing", "topic": "tenancy"}
            },
            {
                "id": "consumer_01",
                "title": "National Consumer Helpline (NCH) & Filing Consumer Grievances",
                "content": "Under Consumer Protection Act 2019, consumers have the right to seek replacement, refund, or compensation for defective goods, deficient services, misleading ads, and unfair trade practices (like non-refund from e-commerce companies or airlines). Redressal Hierarchy: 1) Tier 1: File pre-litigation grievance on National Consumer Helpline (NCH) via Toll-Free 1915, SMS, WhatsApp (8800001915), or consumerhelpline.gov.in. 2) Tier 2: If company does not resolve via NCH, file formal case on e-Daakhil portal (District Consumer Commission for claims up to Rs 50 Lakhs). No lawyer is mandatory for consumer commissions.",
                "source_url_or_file": "Department of Consumer Affairs (consumerhelpline.gov.in)",
                "authority_level": "official_government",
                "last_updated": "2026-09-10",
                "metadata": {"category": "consumer_rights", "topic": "grievance"}
            }
        ]
        
        with open(os.path.join(self.data_dir, "default_vetted_knowledge.json"), "w", encoding="utf-8") as f:
            json.dump(default_docs, f, indent=2, ensure_ascii=False)
            
        for d in default_docs:
            self.chunks.append(DocumentChunk(**d))

    def get_all_chunks(self) -> List[DocumentChunk]:
        return self.chunks
