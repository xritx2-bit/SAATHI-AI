"""
SAATHI AI - Multi-Turn Conversational Context Manager
Maintains conversational state, resolves coreferences, and completes missing-information
loops when a user responds to a clarification question.
"""
from typing import List, Dict, Any, Optional

class ConversationContextManager:
    @staticmethod
    def enrich_query_with_context(current_query: str, session_messages: List[Dict[str, Any]]) -> str:
        """
        If the immediately preceding assistant message was a CLARIFICATION prompt,
        combines the user's brief reply with the prior context to enable seamless retrieval.
        E.g.:
        Turn 1 User: "mera form reject ho gaya" (Triggered CLARIFY: scheme_name)
        Turn 2 User: "PM Kisan" -> Enriched Query: "PM Kisan mera form reject ho gaya"
        """
        if not session_messages or len(session_messages) < 2:
            return current_query

        # Look at last assistant message
        last_assistant_msg = None
        last_user_msg = None
        
        for msg in reversed(session_messages):
            if msg.get("role") == "assistant" and last_assistant_msg is None:
                last_assistant_msg = msg
            elif msg.get("role") == "user" and last_user_msg is None:
                last_user_msg = msg
                
        if not last_assistant_msg or not last_user_msg:
            return current_query

        dec = last_assistant_msg.get("decision")
        if not dec:
            return current_query
            
        d_type = dec.get("decision") if isinstance(dec, dict) else getattr(dec, "decision", "")
        
        # If last turn was a CLARIFY decision and current query is short (a clarification reply)
        if d_type == "CLARIFY" and len(current_query.split()) <= 5:
            prior_text = last_user_msg.get("content", "")
            enriched = f"{current_query} {prior_text}".strip()
            return enriched

        return current_query
