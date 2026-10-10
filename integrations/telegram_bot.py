"""
SAATHI AI - Telegram Bot Integration Service
Connects SAATHI AI Decision Controller to Telegram, allowing citizens across India
to get instant, verified answers, utility bill audits, and legal drafts via mobile chat.
"""
import os
import sys
import requests
from typing import Dict, Any, Optional

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from saathi.controller.engine import SaathiController
from saathi.knowledge.store import KnowledgeStore
from saathi.tools.calculators import UtilityCalculators

class SaathiTelegramBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("TELEGRAM_BOT_TOKEN", "MOCK_TELEGRAM_BOT_TOKEN")
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.store = KnowledgeStore()
        self.controller = SaathiController(self.store)

    def handle_incoming_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes an incoming Telegram message payload and generates the verified reply.
        """
        chat_id = message.get("chat", {}).get("id", "0")
        text = message.get("text", "").strip()

        if text.startswith("/start"):
            reply = (
                "🙏 **Namaste! Welcome to SAATHI AI (साथी)**\n\n"
                "I am your safe, multilingual Indian public assistant. I can help you with:\n"
                "• ⚡ Electricity bill disputes & meter checks\n"
                "• 🌾 PM-KISAN, Ayushman Bharat & government schemes\n"
                "• 🛡️ Cyber fraud 1930 & consumer complaints\n"
                "• 🏠 Rent security deposit rules\n\n"
                "Type your question in Hindi, English, or Hinglish!"
            )
            return {"chat_id": chat_id, "reply_text": reply}

        if text.startswith("/elec"):
            # Example /elec 280
            parts = text.split()
            units = float(parts[1]) if len(parts) > 1 and parts[1].replace(".", "").isdigit() else 250.0
            calc = UtilityCalculators.calculate_electricity_bill(units)
            reply = (
                f"⚡ **Electricity Bill Audit ({units:.0f} kWh):**\n"
                f"• Energy Charges: ₹{calc['energy_charge']:.2f}\n"
                f"• Fixed Charges: ₹{calc['fixed_charge']:.2f}\n"
                f"• Total Estimated Bill: ₹{calc['total_estimated_bill']:.2f}\n"
                f"• Status: Verified under DERC/DISCOM benchmark."
            )
            return {"chat_id": chat_id, "reply_text": reply}

        # Process through Decision Controller
        decision = self.controller.process_query(text)
        reply = decision.response_text
        if decision.citations:
            reply += "\n\n📌 **Official Sources:**\n" + "\n".join([f"• {c}" for c in decision.citations])

        return {
            "chat_id": chat_id,
            "reply_text": reply,
            "decision": decision.decision,
            "language": decision.detected_language
        }

    def send_message(self, chat_id: str, text: str) -> bool:
        """Sends a text message back to the Telegram chat."""
        if self.token == "MOCK_TELEGRAM_BOT_TOKEN":
            print(f"[Telegram Simulation to Chat {chat_id}]:\n{text}")
            return True

        url = f"{self.api_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            r = requests.post(url, json=payload, timeout=8)
            return r.status_code == 200
        except Exception:
            return False

if __name__ == "__main__":
    bot = SaathiTelegramBot()
    sample_msg = {"chat": {"id": "12345678"}, "text": "Mera bijli ka bill bahut jyada aaya hai"}
    res = bot.handle_incoming_message(sample_msg)
    print("Telegram Bot Test Response:\n", res["reply_text"])
