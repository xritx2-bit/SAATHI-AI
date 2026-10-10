"""
Language & Dialect Identification for Indian Multilingual Contexts
Supports English, Hindi (Devanagari), and Hinglish (Latin script).
"""
import re
from typing import Tuple

HINGLISH_KEYWORDS = {
    "mera", "meri", "mere", "kaise", "kare", "karna", "karega", "hai", "hain",
    "hota", "hoti", "hote", "bhi", "nahi", "nahin", "kya", "kyu", "kyun",
    "shikayat", "bijli", "bill", "paise", "kisan", "yojana", "aavedan",
    "madad", "chahiye", "batao", "samjhao", "kaagaz", "dastavej", "naukri",
    "sahayata", "subsidy", "vibhag", "adhikari", "patra", "khata", "aadhaar"
}

def detect_language(text: str) -> str:
    """
    Detects whether the input text is:
    - 'hindi' (Devanagari script)
    - 'hinglish' (Latin script with Hindi words/patterns)
    - 'english' (Default English)
    """
    if not text or not text.strip():
        return "english"
    
    # Check for Devanagari Unicode block (\u0900-\u097F)
    devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
    total_letters = len(re.findall(r'[a-zA-Z\u0900-\u097F]', text))
    
    if total_letters > 0 and (devanagari_chars / total_letters) > 0.25:
        return "hindi"
    
    # Check for Hinglish using vocabulary matches and token patterns
    tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not tokens:
        return "english"
        
    hinglish_match_count = sum(1 for token in tokens if token in HINGLISH_KEYWORDS)
    hinglish_ratio = hinglish_match_count / len(tokens)
    
    if hinglish_match_count >= 1 and (hinglish_ratio >= 0.15 or hinglish_match_count >= 2):
        return "hinglish"
        
    return "english"

def get_language_prompt_guidance(lang: str) -> str:
    """
    Provides explicit system prompt guidance to keep tone respectful, 
    plain, and culturally accurate for Indian users.
    """
    if lang == "hindi":
        return "उपयोगकर्ता से सरल, स्पष्ट और सम्मानजनक हिंदी में बात करें। कठिन शब्दों से बचें।"
    elif lang == "hinglish":
        return "Respond in clear, natural Hinglish (conversational Hindi written in Roman English script) that is easy for everyday Indian users to understand. Avoid overly complex technical jargon."
    else:
        return "Respond in simple, clear, and supportive English. Keep sentences direct and easy to follow."
