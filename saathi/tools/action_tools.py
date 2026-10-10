"""
Action Generation Tools for SAATHI AI
Produces structured drafts (letters, complaints, checklists, calculation summaries).
All tools operate in sandbox mode and return drafts requiring explicit human approval.
"""
import uuid
from typing import Dict, Any, Optional
from saathi.models import ProposedAction

class ActionDraftsman:
    @staticmethod
    def draft_consumer_complaint(
        company_name: str,
        issue_description: str,
        order_or_account_id: str,
        expected_relief: str = "Full refund and prompt resolution",
        language: str = "english"
    ) -> ProposedAction:
        """Drafts a formal consumer grievance letter for NCH / company support."""
        action_id = f"act_{uuid.uuid4().hex[:8]}"
        
        if language == "hindi":
            draft = (
                f"सेवा में,\n"
                f"शिकायत निवारण अधिकारी (Grievance Officer)\n"
                f"{company_name}\n\n"
                f"विषय: अनुचित सेवा / समस्या के संबंध में शिकायत - खाता/ऑर्डर संख्या: {order_or_account_id}\n\n"
                f"महोदय/महोदया,\n\n"
                f"मैं आपका ध्यान अपनी समस्या की ओर आकर्षित करना चाहता हूँ। विवरण निम्न प्रकार है:\n"
                f"- खाता / ऑर्डर संख्या: {order_or_account_id}\n"
                f"- समस्या का विवरण: {issue_description}\n\n"
                f"अतः आपसे सादर अनुरोध है कि कृपया मामले की जांच कर शीघ्र {expected_relief} प्रदान करें। "
                f"यदि यह समस्या 7 दिनों के भीतर हल नहीं होती है, तो मुझे राष्ट्रीय उपभोक्ता हेल्पलाइन (NCH - 1915) पर शिकायत दर्ज करनी होगी।\n\n"
                f"सधन्यवाद,\n"
                f"[आपका नाम]\n[मोबाइल नंबर]"
            )
        else:
            draft = (
                f"To,\n"
                f"The Grievance Redressal Officer / Customer Support Team\n"
                f"{company_name}\n\n"
                f"Subject: Formal Grievance regarding {issue_description[:60]} - Ref: {order_or_account_id}\n\n"
                f"Dear Sir/Madam,\n\n"
                f"I am writing to formally log a grievance regarding the following issue:\n"
                f"• Reference / Account / Order ID: {order_or_account_id}\n"
                f"• Issue Description: {issue_description}\n\n"
                f"I request your immediate intervention to provide: {expected_relief}.\n\n"
                f"Please acknowledge receipt of this grievance with a formal tracking ticket. If not resolved satisfactorily within 7 business days, I reserve the right to escalate this matter to the National Consumer Helpline (1915) and District Consumer Forum.\n\n"
                f"Sincerely,\n"
                f"[Your Name]\n[Contact Phone Number]"
            )
            
        return ProposedAction(
            action_id=action_id,
            action_type="draft_complaint",
            title=f"Draft Grievance Letter for {company_name}",
            draft_content=draft,
            requires_approval=True,
            is_approved=False,
            warning_or_disclaimer="⚠️ Review the draft carefully. Add your exact name, phone number, and transaction details before sending."
        )

    @staticmethod
    def draft_scheme_checklist(scheme_name: str, eligibility_criteria: list, required_docs: list) -> ProposedAction:
        """Generates an actionable step-by-step checklist for official schemes."""
        action_id = f"act_{uuid.uuid4().hex[:8]}"
        
        content = (
            f"📋 **Action Checklist: Applying for {scheme_name}**\n\n"
            f"**Step 1: Check Eligibility Checklist**\n" +
            "\n".join([f"  [ ] {crit}" for crit in eligibility_criteria]) +
            f"\n\n**Step 2: Collect Required Documents**\n" +
            "\n".join([f"  [ ] {doc}" for doc in required_docs]) +
            f"\n\n**Step 3: Verification & Next Step**\n"
            f"  [ ] Verify Aadhaar-linked mobile OTP is active.\n"
            f"  [ ] Ensure Bank Account has active NPCI DBT Seeding.\n"
            f"  [ ] Submit application online at official portal or nearest CSC/Jan Seva Kendra."
        )
        
        return ProposedAction(
            action_id=action_id,
            action_type="generate_checklist",
            title=f"Application Checklist: {scheme_name}",
            draft_content=content,
            requires_approval=True,
            is_approved=False,
            warning_or_disclaimer="Ensure all document photocopies are self-attested before submission."
        )
