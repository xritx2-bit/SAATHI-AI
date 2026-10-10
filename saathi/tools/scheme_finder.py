"""
SAATHI AI - Government Welfare Scheme Eligibility Engine & Wizard
Matches Indian citizens' demographic profiles with central and state public schemes,
calculating eligibility scores, benefits, checklist requirements, and application procedures.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CitizenProfile(BaseModel):
    state: str = "All India"
    age: int = 35
    gender: str = "Male" # Male, Female, Other
    occupation: str = "Farmer" # Farmer, Street Vendor, Unorganized Worker, Student, Senior Citizen, Homemaker, Salaried
    annual_income: float = 120000.0 # Annual household income in ₹
    has_cultivable_land: bool = True
    caste_category: str = "General" # General, OBC, SC, ST, EWS
    has_girl_child: bool = False
    girl_child_age: Optional[int] = None
    is_differently_abled: bool = False

class SchemeEligibilityResult(BaseModel):
    scheme_id: str
    scheme_name: str
    ministry_or_state: str
    category: str
    is_eligible: bool
    eligibility_score: int # 0 to 100%
    benefit_summary: str
    key_conditions: List[str]
    required_documents: List[str]
    portal_url: str
    action_checklist: List[str]

# Authoritative Central & State Welfare Schemes Knowledge Base
ALL_WELFARE_SCHEMES = [
    {
        "scheme_id": "pm_kisan",
        "scheme_name": "PM-KISAN Samman Nidhi Yojana",
        "ministry_or_state": "Ministry of Agriculture & Farmers Welfare (Central)",
        "category": "Agriculture & Income Support",
        "benefit_summary": "₹6,000 per year directly transferred to bank account in 3 equal installments of ₹2,000 via DBT.",
        "portal_url": "https://pmkisan.gov.in",
        "required_documents": ["Aadhaar Card", "Land Ownership Record (Khatoni/Bhulekh)", "Aadhaar-Seeded Bank Passbook"],
        "action_checklist": [
            "Verify cultivable land is registered in state revenue records.",
            "Complete OTP-based e-KYC on pmkisan.gov.in.",
            "Ensure Bank Account has active NPCI DBT mapping."
        ],
        "evaluator": lambda p: (
            p.occupation == "Farmer" and p.has_cultivable_land and p.annual_income < 1000000,
            ["Applicant must be a farmer with cultivable landholding", "Non-institutional landholder", "Not an income tax payee"]
        )
    },
    {
        "scheme_id": "ayushman_bharat",
        "scheme_name": "Ayushman Bharat PM-JAY (Golden Health Card)",
        "ministry_or_state": "National Health Authority (Central)",
        "category": "Healthcare & Social Security",
        "benefit_summary": "₹5,00,000 per year free cashless hospitalization cover per family across all empanelled hospitals.",
        "portal_url": "https://pmjay.gov.in",
        "required_documents": ["Aadhaar Card", "Ration Card / Family ID", "Mobile Number linked to Aadhaar"],
        "action_checklist": [
            "Check eligibility on mera.pmjay.gov.in using Aadhaar or Ration card.",
            "Visit nearest Empanelled Hospital (Ayushman Mitra desk) or CSC Centre.",
            "Download instant PVC Ayushman Golden Card for cashless treatment."
        ],
        "evaluator": lambda p: (
            p.annual_income <= 300000 or p.age >= 70 or p.caste_category in ["SC", "ST", "OBC", "EWS"],
            ["Household income below ₹3 Lakhs OR Senior Citizen aged 70+ (Universal Cover)", "Deprivation criteria as per SECC / State Ration database"]
        )
    },
    {
        "scheme_id": "sukanya_samriddhi",
        "scheme_name": "Sukanya Samriddhi Yojana (SSY)",
        "ministry_or_state": "Ministry of Finance / Post Office (Central)",
        "category": "Women Empowerment & Child Welfare",
        "benefit_summary": "High guaranteed interest rate (8.2% p.a.) with complete Section 80C tax exemption for girl child education & marriage.",
        "portal_url": "https://www.indiapost.gov.in",
        "required_documents": ["Girl Child Birth Certificate", "Parent / Guardian Aadhaar & PAN", "Address Proof", "Passport size photo"],
        "action_checklist": [
            "Open SSY account at any Post Office or nationalized bank with initial deposit of ₹250.",
            "Deposit minimum ₹250 up to ₹1,50,000 per financial year.",
            "Maturity after 21 years from account opening date or at marriage after age 18."
        ],
        "evaluator": lambda p: (
            p.has_girl_child and (p.girl_child_age is None or p.girl_child_age <= 10),
            ["Girl child must be below 10 years of age at the time of account opening", "Maximum 2 accounts per family (one for each girl child)"]
        )
    },
    {
        "scheme_id": "pm_svanidhi",
        "scheme_name": "PM-SVANidhi (Micro-Credit for Street Vendors)",
        "ministry_or_state": "Ministry of Housing and Urban Affairs (Central)",
        "category": "Livelihood & Small Business",
        "benefit_summary": "Collateral-free working capital loan of ₹10,000 (1st tranche) -> ₹20,000 (2nd tranche) -> ₹50,000 (3rd tranche) with 7% interest subsidy.",
        "portal_url": "https://pmsvanidhi.mohua.gov.in",
        "required_documents": ["Vending Certificate / Letter of Recommendation (LoR)", "Aadhaar Card", "Bank Account Details"],
        "action_checklist": [
            "Obtain Street Vending Certificate or Urban Local Body (ULB) Letter of Recommendation.",
            "Apply online on pmsvanidhi.mohua.gov.in portal.",
            "Repay monthly on time via digital UPI payments to earn cashback up to ₹1,200/year."
        ],
        "evaluator": lambda p: (
            p.occupation in ["Street Vendor", "Unorganized Worker"] and p.age >= 18,
            ["Engaged in vending in urban / peri-urban areas on or before March 2020/2022", "Possesses Certificate of Vending or Urban Body verification"]
        )
    },
    {
        "scheme_id": "atal_pension",
        "scheme_name": "Atal Pension Yojana (APY)",
        "ministry_or_state": "PFRDA / Ministry of Finance (Central)",
        "category": "Retirement & Social Security",
        "benefit_summary": "Guaranteed lifetime monthly pension of ₹1,000 to ₹5,000 from age 60, followed by spouse pension and full corpus refund to nominee.",
        "portal_url": "https://npscra.nsdl.co.in",
        "required_documents": ["Savings Bank Account", "Aadhaar Card", "Active Mobile Number"],
        "action_checklist": [
            "Visit your bank branch or use netbanking to enroll in APY.",
            "Select pension slab (₹1,000 to ₹5,000/month) based on monthly contribution.",
            "Set auto-debit from savings account."
        ],
        "evaluator": lambda p: (
            18 <= p.age <= 40 and p.annual_income < 800000,
            ["Indian citizen aged between 18 and 40 years", "Must have an active savings bank account", "Not an existing income tax payer"]
        )
    },
    {
        "scheme_id": "surya_ghar",
        "scheme_name": "PM Surya Ghar: Muft Bijli Yojana",
        "ministry_or_state": "Ministry of New and Renewable Energy (Central)",
        "category": "Clean Energy & Utility Relief",
        "benefit_summary": "Up to ₹78,000 direct central subsidy for installing 1kW-3kW rooftop solar systems, yielding up to 300 units free electricity per month.",
        "portal_url": "https://pmsuryaghar.gov.in",
        "required_documents": ["Recent Electricity Bill (CA/Consumer No)", "Rooftop Ownership Proof", "Aadhaar Card", "Bank Passbook Copy"],
        "action_checklist": [
            "Register on pmsuryaghar.gov.in with Discom name and Consumer Account number.",
            "Choose a registered local solar vendor for rooftop installation.",
            "Apply for net-metering; subsidy is credited directly to bank account within 30 days of Discom inspection."
        ],
        "evaluator": lambda p: (
            p.annual_income < 1500000 and p.age >= 21,
            ["Must have suitable unshaded roof space", "Valid electricity connection in applicant's name", "No prior rooftop solar subsidy availed on same connection"]
        )
    },
    {
        "scheme_id": "pm_vishwakarma",
        "scheme_name": "PM Vishwakarma Yojana",
        "ministry_or_state": "Ministry of MSME (Central)",
        "category": "Artisans & Traditional Trades",
        "benefit_summary": "₹15,000 free toolkit grant + Basic/Advanced Skill training with ₹500/day stipend + Collateral-free loan up to ₹3,00,000 @ 5% interest.",
        "portal_url": "https://pmvishwakarma.gov.in",
        "required_documents": ["Aadhaar Card", "Mobile Number", "Bank Account Details", "Trade Verification from Gram Panchayat / ULB"],
        "action_checklist": [
            "Register trade (Carpenter, Blacksmith, Sculptor, Goldsmith, Potter, Tailor, Barber, Cobbler, etc.) at CSC center.",
            "Complete 5-7 days basic skill training with ₹500 daily stipend.",
            "Receive ₹15,000 e-voucher for modern toolkits and apply for enterprise loan."
        ],
        "evaluator": lambda p: (
            p.occupation in ["Unorganized Worker", "Street Vendor", "Farmer"] and p.age >= 18 and p.annual_income < 500000,
            ["Practicing one of the 18 identified traditional trades with hands/tools", "Minimum age 18 years", "No member of family in government service"]
        )
    },
    {
        "scheme_id": "pm_awas_gramin",
        "scheme_name": "Pradhan Mantri Awas Yojana (PMAY-G / Urban)",
        "ministry_or_state": "Ministry of Rural Development (Central)",
        "category": "Housing & Shelter",
        "benefit_summary": "₹1,20,000 (Plains) / ₹1,30,000 (Hilly states) direct financial assistance for building a pucca house + 90 days MGNREGA wages.",
        "portal_url": "https://pmayg.nic.in",
        "required_documents": ["Aadhaar Card", "MGNREGA Job Card Number", "Bank Account Details", "Land / Plot Ownership document"],
        "action_checklist": [
            "Verify name in SECC Gram Panchayat Awas+ waiting list.",
            "Geo-tagging of kutcha house by Village Development Officer (VDO).",
            "Funds released directly into bank account in 3 construction milestones."
        ],
        "evaluator": lambda p: (
            p.annual_income <= 250000,
            ["Houseless family or living in kutcha / dilapidated house", "Does not own a motorized vehicle or mechanized 3-4 wheeler agricultural equipment"]
        )
    },
    {
        "scheme_id": "pm_ujjwala",
        "scheme_name": "PM Ujjwala Yojana 2.0 (Free LPG Connection)",
        "ministry_or_state": "Ministry of Petroleum and Natural Gas (Central)",
        "category": "Clean Cooking & Women Health",
        "benefit_summary": "Deposit-free 14.2 kg LPG cylinder connection + Free stove (hotplate) + First refill free + ₹300 per cylinder subsidy under DBT.",
        "portal_url": "https://pmuy.gov.in",
        "required_documents": ["Adult Woman Aadhaar Card", "Ration Card showing family composition", "Bank Account (Aadhaar Seeded)", "Self-Declaration of address"],
        "action_checklist": [
            "Submit application online on pmuy.gov.in or at nearest LPG distributor (Indane/HP/Bharat Gas).",
            "Biometric e-KYC authentication.",
            "Collect free regulator, gas stove, and filled 14.2 kg cylinder."
        ],
        "evaluator": lambda p: (
            p.gender == "Female" and p.age >= 18 and p.annual_income <= 300000,
            ["Applicant must be an adult woman belonging to poor household", "No existing LPG connection in the household"]
        )
    }
]

class WelfareSchemeFinder:
    @staticmethod
    def match_schemes_for_citizen(profile: CitizenProfile) -> List[SchemeEligibilityResult]:
        """
        Evaluates a citizen's demographic profile against all national and state schemes.
        Returns sorted list of schemes with eligibility scores, checklist, and benefits.
        """
        results = []
        for scheme in ALL_WELFARE_SCHEMES:
            is_eligible, key_conditions = scheme["evaluator"](profile)
            
            # Compute confidence / fit score
            score = 95 if is_eligible else 35
            if not is_eligible and profile.annual_income < 300000:
                score = 55 # Partial fit / needs document update

            results.append(SchemeEligibilityResult(
                scheme_id=scheme["scheme_id"],
                scheme_name=scheme["scheme_name"],
                ministry_or_state=scheme["ministry_or_state"],
                category=scheme["category"],
                is_eligible=is_eligible,
                eligibility_score=score,
                benefit_summary=scheme["benefit_summary"],
                key_conditions=key_conditions,
                required_documents=scheme["required_documents"],
                portal_url=scheme["portal_url"],
                action_checklist=scheme["action_checklist"]
            ))

        # Sort: Highly eligible schemes first
        results.sort(key=lambda x: (x.is_eligible, x.eligibility_score), reverse=True)
        return results
