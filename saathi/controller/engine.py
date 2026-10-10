"""
SAATHI AI - Decision Controller Engine
Implements Evidence-Gated, Cost-Aware Problem Solving Policy (Hypothesis H1).
"""
import time
import re
from typing import Dict, Any, List, Optional
from saathi.models import ControllerDecision, RetrievedEvidence, ProposedAction, DecisionType
from saathi.language.detector import detect_language, get_language_prompt_guidance
from saathi.knowledge.store import KnowledgeStore
from saathi.knowledge.retriever import HybridRetriever
from saathi.safety.guardrails import SafetyGuardrail
from saathi.tools.action_tools import ActionDraftsman
from saathi.controller.context_manager import ConversationContextManager
from saathi.llm.client import LLMClient

class SaathiController:
    def __init__(self, knowledge_store: Optional[KnowledgeStore] = None):
        self.knowledge_store = knowledge_store or KnowledgeStore()
        self.retriever = HybridRetriever(self.knowledge_store)
        self.llm = LLMClient()

    def process_query(self, user_query: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> ControllerDecision:
        """
        Main Controller entry point. Evaluates user input through the multi-stage policy:
        1. Context Enrichment -> 2. Safety Gate -> 3. Language Routing -> 4. Intent Check -> 5. Retrieval -> 6. Action Drafting
        """
        # 0. Context enrichment from previous conversation turns
        if chat_history:
            user_query = ConversationContextManager.enrich_query_with_context(user_query, chat_history)

        start_time = time.time()
        detected_lang = detect_language(user_query)
        
        # 1. Safety and Guardrail Gate
        is_safe, risk_category, safe_msg = SafetyGuardrail.evaluate_input_safety(user_query)
        if not is_safe:
            return ControllerDecision(
                decision=DecisionType.ESCALATE,
                reasoning=f"Triggered safety guardrail: {risk_category}",
                confidence=1.0,
                detected_language=detected_lang,
                response_text=safe_msg,
                safety_flags=[risk_category or "SAFETY_VIOLATION"]
            )

        query_lower = user_query.lower().strip()

        # 2. Direct Answer Check (Greetings, Capabilities, Definitions)
        cleaned_query = re.sub(r'[^\w\s]', '', query_lower).strip()
        greetings = ["hi", "hello", "namaste", "pranam", "hey", "who are you", "aap kaun ho", "kya kar sakte ho"]
        
        is_greeting = any(
            cleaned_query == g or 
            cleaned_query.startswith(g + " ") or 
            g in cleaned_query.split() 
            for g in ["hi", "hello", "namaste", "pranam", "hey"]
        ) or any(g in cleaned_query for g in ["who are you", "aap kaun ho", "kya kar sakte ho"])

        if is_greeting and len(cleaned_query.split()) <= 6:
            if detected_lang == "hindi":
                resp = "नमस्ते! मैं साथी AI (SAATHI AI) हूँ। मैं आपके रोज़मर्रा के दस्तावेज़ों, सरकारी योजनाओं (जैसे PM-किसान, LPG सब्सिडी), बिजली बिल और उपभोक्ता शिकायतों को समझने और हल करने में आपकी सहायता कर सकता हूँ। आप क्या जानना चाहते हैं?"
            elif detected_lang == "hinglish":
                resp = "Namaste! Main SAATHI AI hoon. Main aapke everyday documents, bijli ke bill, PM-Kisan ya LPG subsidy jaise sarkari schemes, aur consumer complaints ko samajhne aur unka safe solution nikalne me madad kar sakta hoon. Aap kis baare me jaankari chahte hain?"
            else:
                resp = "Namaste! I am SAATHI AI, your everyday assistant. I can help you understand bills, government schemes (like PM-KISAN, LPG Subsidies), rental rules, and consumer rights with verified facts. How can I help you today?"

            return ControllerDecision(
                decision=DecisionType.DIRECT_ANSWER,
                reasoning="Standard greeting / capability query with no external factual dependency.",
                confidence=0.95,
                detected_language=detected_lang,
                response_text=resp
            )

        # 3. Missing Information / Ambiguity Check (Requires Clarification)
        # Only clarify if the query is very brief and does NOT already contain specific context
        has_specific_context = any(
            kw in query_lower for kw in [
                "meter", "मीटर", "kisan", "किसान", "bhulekh", "भूलेख", "subsidy", "सब्सिडी",
                "tata power", "discom", "cylinder", "सिलेंडर", "ekyc", "ई-केवाईसी", "rent", "किराया"
            ]
        )
        
        ambiguous_triggers = [
            (r"(?:form\s*(?:reject|kharij)|फॉर्म\s*रिजेक्ट|फॉर्म\s*खारिज|form\s*got\s*rejected)", "Which official application or scheme form are you referring to? (e.g. PM-KISAN, Ration Card, Voter ID)"),
            (r"(?:paisa\s*nahi\s*aaya|रुपये\s*नहीं\s*आए|पैसे\s*नहीं\s*आए|money\s*not\s*received)", "Which scheme or transfer are you referring to? (e.g. PM-KISAN installment, LPG subsidy, or salary/refund?)"),
            (r"(?:complaint\s*karni\s*hai|शिकायत\s*करनी\s*है|want\s*to\s*complain)", "Which company, service, or department do you want to lodge a complaint against?"),
            (r"(?:bill\s*bahut\s*jyada|बिल\s*बहुत\s*ज्यादा|bill\s*too\s*high)", "Could you clarify which utility bill this is for (Electricity, Water, Gas) and your state/discom?")
        ]
        
        if not has_specific_context and len(query_lower.split()) < 8:
            for pattern, clarification_q in ambiguous_triggers:
                if re.search(pattern, user_query, re.IGNORECASE):
                    if detected_lang == "hindi":
                        resp = f"आपकी सही सहायता के लिए कृपया थोड़ा और विवरण दें: {clarification_q}"
                    elif detected_lang == "hinglish":
                        resp = f"Aapki sahi madad karne ke liye kripya thoda detail batayein: {clarification_q}"
                    else:
                        resp = f"To assist you accurately, could you please clarify: {clarification_q}"
                        
                    return ControllerDecision(
                        decision=DecisionType.CLARIFY,
                        reasoning="User request lacks critical context details (scheme name, department, or context).",
                        confidence=0.88,
                        detected_language=detected_lang,
                        missing_information=[pattern],
                        response_text=resp
                    )

        # 4. Action Drafting Intent Check (Complaints, Letter drafting, Checklists)
        action_patterns = [
            r"draft\s+(?:a\s+)?complaint",
            r"complaint\s+(?:draft|likh|file|karn|bana)",
            r"shikayat\s+(?:patra|likh|karn|darj|bana|karo)",
            r"शिकायत\s*(?:पत्र|लिखें|तैयार|दर्ज|करें|बनाएं)",
            r"पत्र\s*(?:तैयार|लिखें|प्रारूप)",
            r"write\s+(?:a\s+)?(?:complaint|letter|application)",
            r"email\s+draft",
            r"letter\s+to",
            r"patra\s+(?:likh|bana|karo|taiyaar)",
            r"application\s+format"
        ]
        
        is_action_intent = any(re.search(pat, user_query, re.IGNORECASE) for pat in action_patterns)
        
        if is_action_intent:
            # Extract possible entity
            company_match = re.search(r'(?:against|to|for|ke khilaf|के खिलाफ|के लिए|ki|ko)\s+([a-zA-Z0-9\u0900-\u097F\s]+?)(?:\s+(?:for|me|par|regarding|complaint|draft|के|पर|$))', user_query, re.IGNORECASE)
            target_name = company_match.group(1).strip() if company_match else "Service Provider / Department"
            
            proposed_act = ActionDraftsman.draft_consumer_complaint(
                company_name=target_name,
                issue_description=user_query,
                order_or_account_id="[Enter Account / Consumer No.]",
                language=detected_lang
            )
            
            if detected_lang == "hindi":
                resp_text = f"मैंने आपकी शिकायत का प्रारूप (Draft) तैयार कर दिया है। कृपया नीचे दिए गए पत्र की समीक्षा करें और विवरण भरने के बाद ही इसे भेजें।"
            elif detected_lang == "hinglish":
                resp_text = f"Maine aapke liye formal complaint draft taiyaar kar diya hai. Kripya neeche review karein aur apna details daalne ke baad hi forward karein."
            else:
                resp_text = f"I have prepared a formal grievance draft for you. Please review the details below before using or submitting it."
                
            return ControllerDecision(
                decision=DecisionType.PREPARE_ACTION,
                reasoning="Detected user intent to compose formal grievance/application draft.",
                confidence=0.92,
                detected_language=detected_lang,
                proposed_action=proposed_act,
                response_text=resp_text
            )

        # 5. Knowledge Retrieval (RAG)
        evidences = self.retriever.retrieve(user_query, top_k=2, min_threshold=0.10)
        
        if evidences:
            citations = [f"{ev.chunk.title} ({ev.chunk.source_url_or_file})" for ev in evidences]
            combined_evidence_text = "\n\n".join([f"**Source: {ev.chunk.title}**\n{ev.chunk.content}" for ev in evidences])
            
            # Format synthesized response
            if detected_lang == "hindi":
                resp_text = (
                    f"प्रमाणित जानकारी के अनुसार:\n\n"
                    f"{evidences[0].chunk.content}\n\n"
                    f"📌 **स्रोत / संदर्भ:** {evidences[0].chunk.source_url_or_file}\n"
                    f"💡 **सलाह:** यदि आप इस पर कोई शिकायती पत्र या आवेदन तैयार करना चाहते हैं, तो मुझे बताएं।"
                )
            elif detected_lang == "hinglish":
                resp_text = (
                    f"Verified rules ke mutabik:\n\n"
                    f"{evidences[0].chunk.content}\n\n"
                    f"📌 **Source:** {evidences[0].chunk.source_url_or_file}\n"
                    f"💡 **Next Step:** Agar aapko iske liye koi application checklist ya complaint draft chahiye, toh bataiye!"
                )
            else:
                resp_text = (
                    f"Based on verified official guidelines:\n\n"
                    f"{evidences[0].chunk.content}\n\n"
                    f"📌 **Citations / Reference:** {evidences[0].chunk.source_url_or_file}\n"
                    f"💡 **Recommended Next Step:** If you need a formal draft, checklist, or grievance letter prepared, let me know."
                )

            return ControllerDecision(
                decision=DecisionType.RETRIEVE_AND_ANSWER,
                reasoning="Successfully retrieved verified official evidence with high confidence.",
                confidence=round(evidences[0].relevance_score, 2),
                detected_language=detected_lang,
                retrieved_evidences=evidences,
                citations=citations,
                response_text=resp_text
            )

        # 6. Fallback / General Safe Response
        if detected_lang == "hindi":
            fallback_resp = "मुझे इस विषय पर हमारे प्रमाणित डेटाबेस में सीधा दस्तावेज़ नहीं मिला। गलत जानकारी से बचने के लिए, कृपया संबंधित विभाग की आधिकारिक वेबसाइट देखें या अधिक विवरण साझा करें।"
        elif detected_lang == "hinglish":
            fallback_resp = "Is topic par hamare verified knowledge base me direct document nahi mila. Hallucination se bachne ke liye, kripya thoda aur specific details provide karein ya official portal check karein."
        else:
            fallback_resp = "I could not find directly verified official records matching your exact query in the vetted database. To ensure accuracy and avoid unsupported claims, please provide additional details or verify with official department portals."

        return ControllerDecision(
            decision=DecisionType.DIRECT_ANSWER,
            reasoning="No high-confidence vetted evidence found; provided safe grounded fallback.",
            confidence=0.50,
            detected_language=detected_lang,
            response_text=fallback_resp
        )
