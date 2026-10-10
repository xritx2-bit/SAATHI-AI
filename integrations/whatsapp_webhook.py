"""
SAATHI AI - WhatsApp Business Cloud Webhook Integration
Receives WhatsApp incoming message webhooks from Meta Cloud API and responds
with structured, verified guidance, scheme eligibility cards, and helpline numbers.
"""
import os
import sys
import json
import requests
from typing import Dict, Any, Optional

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from saathi.controller.engine import SaathiController
from saathi.knowledge.store import KnowledgeStore

class WhatsAppCloudWebhookService:
    def __init__(
        self,
        access_token: Optional[str] = None,
        phone_number_id: Optional[str] = None,
        verify_token: Optional[str] = None
    ):
        self.access_token = access_token or os.environ.get("WHATSAPP_ACCESS_TOKEN", "MOCK_WA_TOKEN")
        self.phone_number_id = phone_number_id or os.environ.get("WHATSAPP_PHONE_ID", "1029384756")
        self.verify_token = verify_token or os.environ.get("WHATSAPP_VERIFY_TOKEN", "saathi_ai_token_2026")
        self.store = KnowledgeStore()
        self.controller = SaathiController(self.store)

    def process_webhook_payload(self, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parses Meta WhatsApp Webhook JSON payload and invokes the SAATHI Decision Controller.
        """
        try:
            entry = body.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None

            msg = messages[0]
            from_phone = msg.get("from")
            text = msg.get("text", {}).get("body", "")

            # Execute Decision Controller
            decision = self.controller.process_query(text)
            reply = decision.response_text
            if decision.citations:
                reply += f"\n\n📌 Official Sources:\n" + "\n".join([f"• {c}" for c in decision.citations])

            return {
                "to_phone": from_phone,
                "reply_message": reply,
                "decision": decision.decision,
                "detected_language": decision.detected_language
            }
        except Exception as e:
            return {"error": str(e)}

    def send_whatsapp_message(self, to_phone: str, text: str) -> bool:
        """Sends WhatsApp text message via Meta Graph API."""
        if self.access_token == "MOCK_WA_TOKEN":
            print(f"[WhatsApp Mock Dispatch to +{to_phone}]:\n{text}")
            return True

        url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": text}
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            return r.status_code == 200
        except Exception:
            return False

if __name__ == "__main__":
    svc = WhatsAppCloudWebhookService()
    sample_webhook = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "919876543210",
                        "text": {"body": "PM kisan ka 2000 rupaye nahi aaya kya karein?"}
                    }]
                }
            }]
        }]
    }
    out = svc.process_webhook_payload(sample_webhook)
    print("WhatsApp Webhook Processed:\n", out)
