"""
Safety, Risk Classification, High-Stakes Escalation & Guardrails
Adheres strictly to SAATHI AI Safety & Governance Blueprint.
Enforces Constitutional AI: strictly refuses illegal actions (meter tampering,
forged documents, bribery, hacking) and directs citizens to lawful remedies.
"""
import re
from typing import Tuple, List, Optional

# High-stakes medical / suicide / emergency keywords (English, Hinglish, Devanagari Hindi)
EMERGENCY_KEYWORDS = [
    "suicide", "kill myself", "chest pain", "heart attack", "poison", "overdose",
    "emergency police", "domestic violence", "bachao", "jaan khatre me", "court warrant arrest",
    "सीने में दर्द", "तेज दर्द", "सांस लेने में", "दवा लूँ", "आत्महत्या", "जान खतरे में", "एंबुलेंस", "पुलिस आपातकाल"
]

# Illegal activities that must be strictly refused with legal consequences & safe alternatives
ILLEGAL_INTENT_PATTERNS = [
    # 1. Utility theft & Meter tampering
    (
        r"(?i)\b(bypass|slow\s*kare|tamper|meter\s*slow|meter\s*bypass|bijli\s*chori|electricity\s*theft|seal\s*todna|magnet\s*lagaye)\b",
        "UTILITY_THEFT_TAMPERING",
        "🚫 **STRICT REFUSAL: METER TAMPERING IS A PUNISHABLE OFFENCE**\n\n"
        "Electricity meter bypass karna, slow karna ya seal todna **Electricity Act 2003 ki Section 135 aur 138 ke tahat gair-kanooni aur sangin jurm (cognizable offence)** hai.\n\n"
        "**Kanooni Parinaam:**\n"
        "- 3 saal tak ki jail aur bhari compounding penalty.\n"
        "- DISCOM dwara 3 guna assessment fine aur connection permanent cut.\n\n"
        "**Surakshit aur Kanooni Tarike Bill Kam Karne Ke:**\n"
        "1. **PM Surya Ghar Muft Bijli Yojana:** Apni chhat par solar lagwayein (Govt ₹78,000 tak ki subsidy deti hai aur 300 units tak bijli muft hoti hai).\n"
        "2. **Official Check Meter Test:** Agar meter fast chal raha hai, toh DISCOM SDO office me legal Check Meter test ki application dein."
    ),
    # 2. Forgery & Fake Government Documents
    (
        r"(?i)\b(fake\s*aadhaar|fake\s*certificate|nakli\s*praman\s*patra|fake\s*income\s*certificate|nakli\s*khatoni|fake\s*pan|forged\s*signature|nakli\s*stamp|fake\s*caste\s*certificate)\b",
        "DOCUMENT_FORGERY",
        "🚫 **STRICT REFUSAL: DOCUMENT FORGERY IS A SERIOUS CRIME**\n\n"
        "Nakli (fake) sarkari documents, Aadhaar, Income certificate ya Caste certificate banana aur use karna **Bharatiya Nyaya Sanhita (BNS) Section 336 / 338 (IPC Section 465/468/471) ke tahat 7 saal tak ki gair-jamanati jail aur jurmana** ka pravdhan hai.\n\n"
        "**Kanooni Tarika:**\n"
        "- Asli documents ke liye apne nazdeeki **CSC / Jan Seva Kendra** ya [edistrict.gov.in](https://edistrict.gov.in) par online legitimate application darj karein."
    ),
    # 3. Bribery & Corruption Assistance
    (
        r"(?i)\b(ghoos\s*kaise\s*de|bribe\s*officer|corruption\s*tip|rishi\s*dena|lekhpal\s*ko\s*ghoos)\b",
        "BRIBERY_CORRUPTION",
        "🚫 **STRICT REFUSAL: BRIBERY IS AN OFFENCE UNDER ANTI-CORRUPTION LAWS**\n\n"
        "Kisi bhi sarkari karmchari ko ghoos (bribe) dena aur lena **Prevention of Corruption Act 1988 (Section 7 & 8) ke tahat gair-kanooni hai (7 saal tak ki jail)**.\n\n"
        "**Kanooni Action:**\n"
        "- Agar koi karmchari ghoos maange, toh **Anti-Corruption Bureau (ACB) Toll-Free 1064** par complaint darj karein ya **CVC (Central Vigilance Commission)** portal par whistle-blower report karein."
    ),
    # 4. Cyber Cracking / Phishing / Hacking
    (
        r"(?i)\b(hack\s*account|wifi\s*hack|phishing\s*link\s*banaye|password\s*crack|otp\s*bypass\s*tool|card\s*cloning)\b",
        "CYBER_CRIME_EXPLOIT",
        "🚫 **STRICT REFUSAL: UNAUTHORIZED ACCESS & CYBER ATTACKS ARE ILLEGAL**\n\n"
        "Kisi ka account hack karna, phishing link banana ya unauthorized system access karna **Information Technology Act 2000 ki Section 43, 66 aur 66D ke tahat dandaney apradh (3 se 5 saal ki jail)** hai.\n\n"
        "SAATHI AI cybersecurity aur lawful citizen protection ke liye banaya gaya hai."
    )
]

# Prompt injection attempts trying to bypass safety / system rules
PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"system prompt override",
    r"you are now in developer mode",
    r"jailbreak",
    r"bypass safety",
    r"reveal secret key"
]

# Sensitive credentials that should NEVER be accepted or echoed
SENSITIVE_CREDENTIAL_PATTERNS = [
    r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", # 16-digit credit/debit card
    r"\b\d{3}[ -]?\d{3}\b",                      # CVV / OTP patterns
    r"(?i)password\s*[:=]\s*\S+",
    r"(?i)netbanking\s*pin\s*[:=]\s*\S+"
]

class SafetyGuardrail:
    @staticmethod
    def evaluate_input_safety(text: str) -> Tuple[bool, Optional[str], str]:
        """
        Evaluates input text for safety, emergencies, and illegal activities.
        Returns: (is_safe: bool, risk_category: Optional[str], safe_message: str)
        """
        text_lower = text.lower()
        
        # 1. Check for Emergency / High Stakes Escalation
        for kw in EMERGENCY_KEYWORDS:
            if kw in text_lower:
                return (
                    False,
                    "HIGH_STAKES_EMERGENCY",
                    "⚠️ **Emergency Assistance Alert / आपातकालीन सूचना:**\n\n"
                    "If you or someone else is in immediate physical, medical, or life-threatening danger, "
                    "please contact emergency services immediately:\n"
                    "- **National Emergency Helpline:** 112\n"
                    "- **Medical Ambulance:** 108 / 102\n"
                    "- **Police Assistance:** 100\n"
                    "- **KIRAN Mental Health Helpline:** 1800-599-0019\n"
                    "- **Tele-MANAS:** 14416\n\n"
                    "SAATHI AI cannot make emergency or medical decisions."
                )

        # 2. Check for Illegal Requests (Utility Theft, Forgery, Bribery, Hacking)
        for pattern, category, response_text in ILLEGAL_INTENT_PATTERNS:
            if re.search(pattern, text_lower):
                return (
                    False,
                    category,
                    response_text
                )
                
        # 3. Check for Prompt Injections
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                return (
                    False,
                    "PROMPT_INJECTION_ATTEMPT",
                    "🔒 **Security Notice:** SAATHI AI processes instructions strictly according to verified safety rules and cannot override core system governance."
                )
                
        # 4. Check for sensitive credential leakage
        for pattern in SENSITIVE_CREDENTIAL_PATTERNS:
            if re.search(pattern, text):
                return (
                    False,
                    "SENSITIVE_CREDENTIAL_LEAK",
                    "🛡️ **Privacy Warning / गोपनीयता सूचना:** Please do not enter sensitive private data like bank passwords, ATM PINs, OTPs, or full credit card numbers. SAATHI AI will never ask for your confidential banking credentials."
                )
                
        return (True, None, "")

    @staticmethod
    def verify_action_permission(action_type: str, user_explicit_approval: bool) -> Tuple[bool, str]:
        """
        Strict Gate: No real-world action or submission is ever performed without explicit human approval.
        """
        if not user_explicit_approval:
            return (
                False,
                f"🛑 **Action Blocked / अनुमति आवश्यक:** Action '{action_type}' is prepared as a draft. You must explicitly review and approve it before any execution."
            )
        return (True, "Action approved by user.")
