"""
SAATHI AI - Citizen Dispatch & Notification Simulator
Simulates WhatsApp, SMS, and Email delivery of verified action drafts, 
grievance tracking IDs, and scheme reminders for Indian rural & urban citizens.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List

class CitizenDispatcher:
    @staticmethod
    def simulate_whatsapp_dispatch(
        phone_number: str,
        message_body: str,
        recipient_name: str = "Citizen"
    ) -> Dict[str, Any]:
        """
        Simulates sending a formal notification / grievance draft via WhatsApp Business API.
        """
        dispatch_id = f"wa_{uuid.uuid4().hex[:10]}"
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        
        preview = (
            f"📱 **WhatsApp Notification [To: {phone_number}]**\n\n"
            f"Namaste {recipient_name}! 🙏\n"
            f"Your SAATHI AI verified citizen update:\n\n"
            f"{message_body[:300]}...\n\n"
            f"📌 Tracking ID: `{dispatch_id.upper()}`\n"
            f"⏰ Sent on: {timestamp}\n"
            f"🛡️ *Verified & Permission-Gated by SAATHI AI*"
        )
        
        return {
            "status": "DELIVERED",
            "dispatch_id": dispatch_id,
            "channel": "WhatsApp",
            "recipient": phone_number,
            "timestamp": timestamp,
            "preview_card": preview
        }

    @staticmethod
    def simulate_sms_alert(
        phone_number: str,
        scheme_or_service: str,
        status_message: str
    ) -> Dict[str, Any]:
        """
        Simulates sending a concise SMS alert (e.g. for low-literacy or feature phones).
        """
        sms_id = f"sms_{uuid.uuid4().hex[:8]}"
        sms_text = f"SAATHI-GOV: {scheme_or_service} Update - {status_message}. Ref: {sms_id.upper()}"
        
        return {
            "status": "SENT",
            "dispatch_id": sms_id,
            "channel": "SMS (CDAC / NIC Gateway)",
            "recipient": phone_number,
            "sms_text": sms_text
        }
