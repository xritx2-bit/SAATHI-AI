"""
SAATHI AI - Comprehensive Training Dataset Generator
Converts vetted knowledge chunks, test cases, and conversation templates 
into standard Instruction-Tuning (Alpaca / ChatML) JSONL datasets for LoRA / QLoRA training.
"""
import os
import json
import random

def generate_saathi_training_dataset(output_dir="data/training_data"):
    os.makedirs(output_dir, exist_ok=True)

    samples = [
        # 1. Decision Policy & Routing Samples
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Mera bijli ka bill bahut jyada aaya hai meter kharab lagta hai",
            "output": "DECISION: RETRIEVE_AND_ANSWER\nREASONING: The user is asking about an abnormally high electricity bill and faulty meter procedure. Needs factual guidance on checking meter reading, filing SDO complaint, and CGRF escalation."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "mera form reject ho gaya",
            "output": "DECISION: CLARIFY\nREASONING: Missing necessary details. Ask the user which specific application or government scheme form they are referring to."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Draft complaint letter to Tata Power for faulty meter reading",
            "output": "DECISION: PREPARE_ACTION\nREASONING: User explicitly requested a formal complaint draft. Action must be drafted with placeholder tags and require user approval before sending."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "I have severe chest pain what medicine to take?",
            "output": "DECISION: ESCALATE\nREASONING: High-stakes medical emergency. Refuse diagnosis and provide immediate emergency numbers (112, 108)."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Namaste, who are you?",
            "output": "DECISION: DIRECT_ANSWER\nREASONING: Standard greeting and capability request."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Bank account se 50000 kat gaye scammer ne OTP le liya",
            "output": "DECISION: RETRIEVE_AND_ANSWER\nREASONING: Cyber financial fraud. Guide immediately to call 1930 within the Golden Hour and report on cybercrime.gov.in."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "Mujhe e-commerce company ke against NCH par grievance darj karne ka letter bana do",
            "output": "DECISION: PREPARE_ACTION\nREASONING: Formal complaint draft requested for consumer grievance. Needs human approval gate."
        },
        {
            "instruction": "You are SAATHI AI. Classify the user query into the appropriate decision action: [DIRECT_ANSWER, RETRIEVE_AND_ANSWER, CLARIFY, PREPARE_ACTION, ESCALATE].",
            "input": "I am feeling hopeless and want to end my life",
            "output": "DECISION: ESCALATE\nREASONING: Severe self-harm emergency. Escalate immediately to Tele-MANAS (14416 / 1800-891-4416) and 112."
        },

        # 2. PM-KISAN Scheme Grounded Answers
        {
            "instruction": "Explain how PM-KISAN Samman Nidhi installment errors (like land seeding or eKYC) can be fixed.",
            "input": "PM kisan ka 2000 rupaye nahi aaya, land seeding NO dikha raha hai, kya karein?",
            "output": "Agar PM-KISAN portal par Land Seeding 'NO' hai, toh yeh steps follow karein:\n1) Apne zameen ke dastawez (Khatoni/Bhulekh) aur Aadhaar card ki photocopy lein.\n2) Apne Halka Patwari ya District Agriculture Office (Kisan Sahayak) ke paas submit karein.\n3) Portal par apna e-KYC (OTP ya biometric) complete karein.\n4) Bank me jaakar NPCI Aadhaar Seeding verify karein."
        },
        {
            "instruction": "Explain PM-KISAN scheme eligibility and benefits in Hindi.",
            "input": "PM किसान योजना में कितने पैसे मिलते हैं और किसे मिलते हैं?",
            "output": "पीएम-किसान योजना के तहत:\n1) पात्र किसान परिवारों को प्रति वर्ष ₹6,000 की आर्थिक सहायता मिलती है।\n2) यह राशि ₹2,000 की तीन समान किस्तों में सीधे आधार-सीडेड बैंक खाते में भेजी जाती है।\n3) पात्रता: जिन किसानों के नाम राजस्व रिकॉर्ड में कृषि भूमि है। (सरकारी कर्मचारी, टैक्सपेयर्स और पेशेवर इसके पात्र नहीं हैं)।"
        },
        {
            "instruction": "How to check PM Kisan beneficiary status online?",
            "input": "How can I check if my name is in PM Kisan list online?",
            "output": "To check your PM-KISAN status:\n1) Visit the official website: pmkisan.gov.in\n2) Click on 'Know Your Status' in the Farmers Corner.\n3) Enter your Registration Number or Registered Mobile Number and Captcha.\n4) Check the status of 'e-KYC Done', 'Eligibility', and 'Land Seeding' (all three must say YES)."
        },

        # 3. Electricity Bill & DISCOM
        {
            "instruction": "Explain how to challenge an abnormally high electricity bill and request a meter accuracy test.",
            "input": "My electricity bill came 3 times higher than usual. How to complain?",
            "output": "To resolve an abnormally high electricity bill:\n1) Verify your physical meter reading against the current reading printed on your bill.\n2) Check if your bill was calculated on 'Actual' or 'Average / Provisional' basis.\n3) Submit a written complaint to your local SDO / DISCOM office requesting a check meter installation under the Electricity Supply Code.\n4) If unresolved within 30 days, escalate to the Consumer Grievance Redressal Forum (CGRF) and Ombudsman."
        },
        {
            "instruction": "Explain electricity billing slab calculation.",
            "input": "Bijli bill me slab rate kaise calculate hota hai?",
            "output": "Bijli bill me telescopic slab system hota hai:\n1) Har slab ki units ka alag rate hota hai (jaise pehle 100 units ka sasta rate, aur usse upar ka rate jyada hota hai).\n2) Total bill = (Units * Slab Rate) + Fixed Charge + Energy Duty/Surcharge.\n3) Subsidy wale states (jaise Delhi ya Punjab) me nirdharit units tak zero bill ya subsidy amount deduct hota hai."
        },

        # 4. Tenancy & Security Deposit
        {
            "instruction": "Explain the rights of a tenant regarding security deposit refund under standard Indian tenancy rules.",
            "input": "What should I do if my landlord is refusing to return my security deposit without valid reason?",
            "output": "Under Indian tenancy norms and Model Tenancy guidelines:\n1) Landlords can only deduct genuine unpaid utility bills or structural damage beyond normal wear-and-tear.\n2) Send a written notice quoting your tenancy agreement, key handover date, and requesting the itemized deduction statement.\n3) If unresolved, file a consumer grievance on National Consumer Helpline (1915) or approach the Rent Authority."
        },
        {
            "instruction": "Makan malik bina notice ke rent badha sakta hai kya?",
            "input": "Makan malik ne achanak rent badha diya bina kisi notice ke, kya karein?",
            "output": "Kirayedari niyam ke anusaar:\n1) Makan malik agreement period ke dauran achanak rent nahi badha sakta.\n2) Model Tenancy Act ke mutabik rent badhane ke liye kam se kam 3 mahine pehle likhit notice dena zaroori hai.\n3) Agar agreement me koi clause mention hai toh usi ke hisaab se hike lagu hoga."
        },

        # 5. LPG Subsidy & PAHEL Scheme
        {
            "instruction": "Explain how LPG subsidy works under the PAHEL scheme and what to do if subsidy is not credited.",
            "input": "LPG gas cylinder ka subsidy nahi mila, complaint kaise karein?",
            "output": "PAHEL scheme ke tahat subsidy na milne par:\n1) Cash memo par 17-digit LPG ID check karein.\n2) mylpg.in portal par subsidy transfer status dekhein.\n3) Ensure karein ki saal ka 12 cylinder quota khatam na hua ho.\n4) Toll-Free number 1800-2333-555 par complaint register karein ya distributor se sampark karein."
        },

        # 6. Cyber Fraud & Financial Safety
        {
            "instruction": "Explain how to report cyber financial fraud and recover stolen money.",
            "input": "Online fraud ho gaya paise kat gaye, helpline number kya hai?",
            "output": "Agar bank ya UPI se online fraud hua hai:\n1) Turant National Cyber Crime Helpline '1930' par call karein (Golden Hour ke andar call karne par bank transaction freeze ho sakta hai).\n2) cybercrime.gov.in portal par complaint darj karein (SMS aur transaction screenshot ke sath).\n3) Apne bank ko 3 din ke andar inform karein (RBI Zero Liability rule)."
        },
        {
            "instruction": "What is the RBI Zero Liability policy for unauthorized electronic banking transactions?",
            "input": "What is RBI guideline on unauthorized bank fraud refund?",
            "output": "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18:\n1) Zero Liability applies if the customer reports the unauthorized transaction within 3 working days and the fraud is not due to customer negligence (like sharing OTP/PIN).\n2) Limited Liability (up to ₹10,000) applies if reported within 4-7 working days.\n3) The bank must credit the shadow reversal/amount back within 10 working days."
        },

        # 7. Ayushman Bharat & Healthcare
        {
            "instruction": "Explain Ayushman Bharat PM-JAY hospital treatment rules and helpline.",
            "input": "Ayushman card se free ilaj kaise karwaye hospital paise maang raha hai?",
            "output": "Ayushman Bharat PM-JAY ke tahat empanelled hospital me ilaj 100% cashless hota hai (up to Rs 5 Lakh/year):\n1) Hospital me 'Ayushman Mitra' desk par card dikhayein.\n2) Koi bhi cash advance ya medicine charge nahi lagta.\n3) Agar hospital paise maange ya manaa kare, toh turant Toll-Free helpline '14555' par call karein ya cgrms.pmjay.gov.in par complaint darj karein."
        },

        # 8. EPFO & PF Withdrawal
        {
            "instruction": "Explain online PF withdrawal process and Form 31 for advance.",
            "input": "How to withdraw PF advance online from EPFO for medical emergencies?",
            "output": "To withdraw PF advance online from EPFO:\n1) Login to Unified Member Portal (epfindia.gov.in) with UAN and password.\n2) Go to Online Services -> Claim (Form-31, 19, 10C).\n3) Select Form 31 (PF Advance) and select 'Illness/Medical emergency' as the reason (no minimum service requirement).\n4) Upload scanned cancelled cheque / passbook copy and verify via Aadhaar OTP."
        },

        # 9. Consumer Grievance & E-commerce
        {
            "instruction": "How to file a consumer grievance against defective goods or denied refunds in India?",
            "input": "Flipkart/Amazon defective product refund nahi de raha, consumer court kaise jaye?",
            "output": "Consumer grievance redressal ke liye:\n1) Pehle company ke grievance officer ko written email bhejein.\n2) Agar 48 hours me resolution na mile, toh National Consumer Helpline '1915' par call karein ya consumerhelpline.gov.in (NCH app) par docket number generate karein.\n3) Badi amount ke dispute ke liye e-Daakhil portal (edaakhil.nic.in) ke through District Consumer Commission me case file karein."
        },

        # 10. Ration Card & ONORC
        {
            "instruction": "Explain One Nation One Ration Card (ONORC) for migrant workers.",
            "input": "Kya dusre rajya me ration mil sakta hai ONORC se?",
            "output": "Haan, 'One Nation One Ration Card (ONORC)' ke tahat eligible ration card holder pure desh me kisi bhi Fair Price Shop (ration ki dukaan) se biometric Aadhaar authentication ke zariye apna muft ration le sakte hain. Iske liye naya ration card banane ki zarurat nahi hoti."
        }
    ]

    # Expand dataset with casing and formatting variations
    expanded = []
    for s in samples:
        expanded.append(s)
        # Variation with lowercase query
        expanded.append({
            "instruction": s["instruction"],
            "input": s["input"].lower(),
            "output": s["output"]
        })

    random.seed(42)
    random.shuffle(expanded)

    split_idx = int(len(expanded) * 0.8)
    train_data = expanded[:split_idx]
    val_data = expanded[split_idx:]

    train_path = os.path.join(output_dir, "train.jsonl")
    val_path = os.path.join(output_dir, "val.jsonl")

    with open(train_path, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Generated {len(train_data)} training samples -> {train_path}")
    print(f"✅ Generated {len(val_data)} validation samples -> {val_path}")

if __name__ == "__main__":
    generate_saathi_training_dataset()
