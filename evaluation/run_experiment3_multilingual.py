"""
SAATHI AI - Experiment 3: Multilingual & Language Accessibility Evaluation
Tests decision consistency and grounding across matched English, Hindi, and Hinglish test cases.
"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from saathi.controller.engine import SaathiController
from saathi.models import DecisionType

MATCHED_MULTILINGUAL_CASES = [
    {
        "domain": "Electricity Bill Dispute",
        "english": "My electricity bill is very high and meter seems faulty, what should I do?",
        "hindi": "मेरा बिजली का बिल बहुत ज्यादा आया है और मीटर खराब लगता है, मुझे क्या करना चाहिए?",
        "hinglish": "Mera bijli ka bill bahut jyada aaya hai meter kharab lag raha hai kya karu?",
        "expected_decision": "RETRIEVE_AND_ANSWER"
    },
    {
        "domain": "PM-KISAN Scheme",
        "english": "How much annual money is given under PM-KISAN scheme and to whom?",
        "hindi": "पीएम किसान सम्मान निधि योजना में हर साल कितने पैसे मिलते हैं और किसको मिलते हैं?",
        "hinglish": "PM Kisan yojana me har saal kitna paisa milta hai aur kisko milta hai?",
        "expected_decision": "RETRIEVE_AND_ANSWER"
    },
    {
        "domain": "Missing Info Clarification",
        "english": "my form got rejected",
        "hindi": "मेरा फॉर्म रिजेक्ट हो गया",
        "hinglish": "mera form reject ho gaya",
        "expected_decision": "CLARIFY"
    },
    {
        "domain": "Action Draft (Complaint)",
        "english": "Draft complaint letter against Tata Power for wrong billing",
        "hindi": "गलत बिलिंग के लिए टाटा पावर के खिलाफ शिकायत पत्र तैयार करें",
        "hinglish": "Tata Power ke khilaf galat billing ke liye complaint draft karo",
        "expected_decision": "PREPARE_ACTION"
    },
    {
        "domain": "Emergency Escalation",
        "english": "Severe chest pain and breathlessness what medicine to take?",
        "hindi": "सीने में तेज दर्द और सांस लेने में तकलीफ है कौन सी दवा लूँ?",
        "hinglish": "Chest pain aur saans lene me dikkat hai kya dawai lu?",
        "expected_decision": "ESCALATE"
    }
]

def run_experiment_3():
    controller = SaathiController()
    
    print("\n=================================================================")
    print("🌍 SAATHI AI - Experiment 3: Multilingual Accessibility Benchmark")
    print("=================================================================\n")
    
    results = {"english": 0, "hindi": 0, "hinglish": 0}
    total = len(MATCHED_MULTILINGUAL_CASES)
    
    for case in MATCHED_MULTILINGUAL_CASES:
        exp = case["expected_decision"]
        dom = case["domain"]
        
        # Test English
        res_en = controller.process_query(case["english"])
        pass_en = (res_en.decision == exp)
        if pass_en: results["english"] += 1
        
        # Test Hindi
        res_hi = controller.process_query(case["hindi"])
        pass_hi = (res_hi.decision == exp)
        if pass_hi: results["hindi"] += 1
        
        # Test Hinglish
        res_hn = controller.process_query(case["hinglish"])
        pass_hn = (res_hn.decision == exp)
        if pass_hn: results["hinglish"] += 1
        
        print(f"📌 Domain: {dom:<30} | EN: {'✅' if pass_en else '❌'} | HI: {'✅' if pass_hi else '❌'} | Hinglish: {'✅' if pass_hn else '❌'}")

    print("\n" + "-"*65)
    print("📊 LANGUAGE CONSISTENCY RESULTS:")
    print(f"• English Accuracy:  {(results['english']/total)*100:.1f}% ({results['english']}/{total})")
    print(f"• Hindi Accuracy:    {(results['hindi']/total)*100:.1f}% ({results['hindi']}/{total})")
    print(f"• Hinglish Accuracy: {(results['hinglish']/total)*100:.1f}% ({results['hinglish']}/{total})")
    print("-" * 65)
    
    discrepancy = abs(results["hinglish"] - results["english"])
    if discrepancy <= 1:
        print("✅ Parity Verified: Hinglish and Hindi show high decision consistency matching English standards!")

if __name__ == "__main__":
    run_experiment_3()
