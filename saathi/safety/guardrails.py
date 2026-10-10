"""
Safety, Risk Classification, High-Stakes Escalation & Guardrails
Adheres strictly to SAATHI AI Safety & Governance Blueprint.
"""
import re
from typing import Tuple, List, Optional

# High-stakes medical / suicide / emergency keywords (English, Hinglish, Devanagari Hindi)
EMERGENCY_KEYWORDS = [
    "suicide", "kill myself", "chest pain", "heart attack", "poison", "overdose",
    "emergency police", "domestic violence", "bachao", "jaan khatre me", "court warrant arrest",
    "सीने में दर्द", "तेज दर्द", "सांस लेने में", "दवा लूँ", "आत्महत्या", "जान खतरे में", "एंबुलेंस", "पुलिस आपातकाल"
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
        Evaluates input text for safety.
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
                    "- **KIRAN Mental Health Helpline:** 1800-599-0019\n\n"
                    "SAATHI AI cannot make medical or emergency decisions."
                )
                
        # 2. Check for Prompt Injections
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                return (
                    False,
                    "PROMPT_INJECTION_ATTEMPT",
                    "🔒 **Security Notice:** SAATHI AI processes instructions strictly according to verified safety rules and cannot override core system governance."
                )
                
        # 3. Check for sensitive credential leakage
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
