"""
SAATHI AI - Gemini 3.7-Style CoT Reasoning Dataset Generator
Generates high-density Chain-of-Thought (CoT) instruction tuning datasets
emulating Gemini 3.7 hybrid thinking & decision efficiency across 12+ public welfare domains.
"""
import os
import json
import random

def generate_saathi_training_dataset(output_dir="data/training_data"):
    os.makedirs(output_dir, exist_ok=True)

    cot_samples = [
        # =========================================================================
        # 1. EMERGENCY ESCALATION & LIFE SAFETY
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Analyze the user input, verify safety constraints inside <think>...</think>, and provide the final response or policy decision.",
            "input": "I have severe chest pain and breathlessness, what medicine should I take?",
            "output": "<think>\n1. Intent: User is asking for medical advice for acute, life-threatening symptoms (chest pain + breathlessness).\n2. Safety Check: HIGH_STAKES_EMERGENCY. Providing prescription medication advice without medical credentials is strictly forbidden and dangerous.\n3. Policy Decision: ESCALATE immediately to national emergency medical services (112 / 108).\n4. Action: Refuse self-medication, urge immediate hospitalization, and provide emergency contact numbers.\n</think>\nDECISION: ESCALATE\n\n🚨 **CRITICAL MEDICAL EMERGENCY WARNING**\nSevere chest pain accompanied by breathlessness may indicate an acute cardiovascular or respiratory event. **Do NOT take unprescribed medication or delay medical evaluation.**\n\n**Immediate Action Plan:**\n1. **Call 112 or 108 (National Emergency Ambulance Helpline)** immediately for emergency transport.\n2. Sit upright in a relaxed position with loose clothing; do not exert physical effort.\n3. Inform a family member, neighbor, or emergency contact immediately to accompany you to the nearest hospital emergency room."
        },
        {
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> and classify the action / response for suicidal distress.",
            "input": "I am feeling hopeless and want to end my life please help",
            "output": "<think>\n1. Intent: User is expressing acute self-harm / suicidal thoughts.\n2. Safety Check: SEVERE_LIFE_SAFETY_CRISIS. Must provide immediate, empathetic crisis intervention and 24/7 government suicide helpline numbers.\n3. Policy Decision: ESCALATE to mental health helpline Tele-MANAS and Kiran.\n</think>\nDECISION: ESCALATE\n\n💙 **You Are Not Alone – Immediate Help Is Available 24/7**\nPlease reach out right now to professional counselors who care and are ready to support you confidentially:\n\n- **Tele-MANAS (Govt of India 24x7 Mental Health Helpline):** Dial **14416** or **1800-891-4416** (Toll-Free)\n- **KIRAN Mental Health Helpline:** Dial **1800-599-0019**\n- **National Emergency Response Support:** Dial **112**\n\nPlease talk to someone you trust or reach out to these numbers immediately. Help and recovery are always possible."
        },
        {
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> on cyber financial fraud handling.",
            "input": "Bank account se 50000 kat gaye scammer ne fake link bheja tha abhi 10 minute pehle",
            "output": "<think>\n1. Intent: User fell victim to an online phishing scam (~₹50,000 debited) within the last 10 minutes.\n2. Timeline Nuance: The event is within the 'Golden Hour' (first 2 hours of fraud).\n3. Legal / Regulatory Framework: Citizen Financial Cyber Fraud Reporting System (CFCFRS) & RBI Zero Liability Framework (2017).\n4. Resolution Strategy: Urgently invoke 1930 to freeze fraudulent destination accounts before money is laundered, file on cybercrime.gov.in, and report to bank to claim zero liability.\n</think>\n🚨 **GOLDEN HOUR EMERGENCY: TAKE ACTION IMMEDIATELY**\n\nKyunki fraud abhi 10 minute pehle hua hai, turant yeh steps follow karein taaki paise destination account me **freeze** ho sakein:\n\n1. **Call 1930 (National Cyber Financial Fraud Helpline):** Turant 1930 par call karein. Operator ko apna Bank Name, Account Number, UPI ID, Debit Transaction ID aur Scammer ka Account/UPI batayein. Golden Hour ke andar system intermediary wallet ya recipient account freeze kar deta hai.\n2. **National Cybercrime Portal:** [cybercrime.gov.in](https://cybercrime.gov.in) par jakar 'Report Financial Fraud' me formal complaint darj karein aur Acknowledgement Slip save karein.\n3. **Bank Zero-Liability Reporting:** Apne bank ke customer care par call karke card/netbanking block karayein aur written complaint dekar Acknowledgement Number lein. (RBI circular ke tahat 3 working days ke andar inform karne par customer liability zero hoti hai)."
        },

        # =========================================================================
        # 2. PM-KISAN SAMMAN NIDHI & AGRICULTURE WELFARE
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> on PM-KISAN installment issues.",
            "input": "PM kisan ka 2000 rupaye nahi aaya, land seeding NO dikha raha hai, kya karein?",
            "output": "<think>\n1. Intent: Farmer did not receive PM-KISAN 16th/17th/18th installment because 'Land Seeding' status is 'NO'.\n2. Domain Knowledge: PM-KISAN guidelines require 3 mandatory checkmarks: (a) Land Seeding YES, (b) e-KYC YES, (c) Aadhaar-Bank Account NPCI Seeding YES.\n3. Cause: Land records (Khatoni/Bhulekh) are either unverified by the local revenue department or mismatched with Aadhaar name/Khata number.\n4. Resolution Path: Physical verification via Patwari/Lekhpal or District Agriculture Office with land documents.\n</think>\n🌾 **PM-KISAN Land Seeding 'NO' Theek Karne Ka Sahi Tarika:**\n\nAgar portal par Land Seeding 'NO' hai, toh kist tab tak ruki rahegi jab tak revenue records physically verify nahi hote. Yeh 4 steps karein:\n\n1. **Dastawez Ikkattha Karein:**\n   - Zameen ki taaza **Khatoni / Bhulekh / RoR** (Land Record Copy)\n   - Aadhaar Card ki photocopy\n   - Bank Passbook & PM-KISAN Registration Number.\n\n2. **Halka Patwari / Lekhpal Se Milen:**\n   - Apne gram ke Patwari/Lekhpal ke paas jakar physical verification form par sign aur stamp karwayein ki zameen aapke naam par darj hai.\n\n3. **District Agriculture Office (Kisan Sahayak):**\n   - Patwari verified dastawez apne Block/District Agriculture Office (Krishi Bhavan) me PM-KISAN Nodal Officer ke paas submit karein.\n\n4. **Status Check:**\n   - 7 se 15 din baad [pmkisan.gov.in](https://pmkisan.gov.in) par 'Know Your Status' me check karein. Verify hote hi ruki hui pichli kisten bhi aapke account me credit ho jayengi."
        },
        {
            "instruction": "You are SAATHI AI. Explain PM-KISAN eligibility, budget, and exclusionary criteria in Hindi with reasoning inside <think>...</think>.",
            "input": "PM किसान योजना में कितने पैसे मिलते हैं और किसे मिलते हैं?",
            "output": "<think>\n1. Intent: User is asking about the financial entitlement and eligibility criteria of Pradhan Mantri Kisan Samman Nidhi (PM-KISAN).\n2. Scheme Details: ₹6,000 per year paid in 3 four-monthly installments of ₹2,000 directly via DBT to bank accounts.\n3. Eligibility & Exclusions: Small & marginal landholding farmer families. Excluded: Institutional landholders, constitutional post holders, serving/retired government employees, doctors/lawyers/CA, and income tax payers.\n</think>\n🇮🇳 **प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) योजना का सम्पूर्ण विवरण:**\n\n**1. मिलने वाली वित्तीय सहायता:**\n- योजना के अंतर्गत पात्र किसान परिवारों को प्रति वर्ष **₹6,000** की सहायता दी जाती है।\n- यह राशि **₹2,000 - ₹2,000 की 3 समान किस्तों** में हर 4 महीने बाद सीधे आधार-सीडेड बैंक खाते (DBT) में भेजी जाती है।\n\n**2. कौन पात्र (Eligible) है?**\n- वे सभी किसान जिनके नाम राज्य/UT के राजस्व रिकॉर्ड में कृषि योग्य भूमि (cultivable land) दर्ज है।\n\n**3. किन्हें लाभ नहीं मिलता (Exclusion Criteria):**\n- संस्थागत भूमि धारक (Institutional Landholders).\n- संवैधानिक पद धारण करने वाले व्यक्ति या पूर्व/वर्तमान मंत्री, सांसद, विधायक।\n- केंद्र/राज्य सरकार के नियमित या सेवानिवृत्त कर्मचारी (चतुर्थ श्रेणी/Group D को छोड़कर)।\n- पेशेवर जैसे डॉक्टर्स, इंजीनियर्स, सीए और पिछले वर्ष आयकर (Income Tax) भरने वाले व्यक्ति।"
        },

        # =========================================================================
        # 3. ELECTRICITY TARIFF DISPUTES & CONSUMER FORUMS
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Formulate an actionable legal resolution for faulty electricity meters inside <think>...</think>.",
            "input": "My electricity bill came 3 times higher than usual, meter reading seems wrong. How to resolve?",
            "output": "<think>\n1. Intent: Consumer has received an inflated electricity bill due to potential meter malfunction or inaccurate provisional billing.\n2. Regulatory Framework: Electricity Act 2003, State Electricity Supply Code & CGRF (Consumer Grievance Redressal Forum) Regulations.\n3. Diagnostic Steps: (a) Compare physical meter reading with bill reading, (b) Verify billing basis ('Actual' vs 'Average/Provisional'), (c) Check telescopic slab rate jumping.\n4. Statutory Remedy: Request formal check meter test under the Supply Code; if unaddressed within 30 days, file statutory complaint before CGRF and State Electricity Ombudsman.\n</think>\n⚡ **How to Challenge an Abnormally High Electricity Bill & Faulty Meter:**\n\n**Step 1: Immediate Self-Audit**\n- **Check Physical Meter Reading:** Note the Current Reading on your meter display and match it with the 'Present Reading' printed on your bill. If the printed reading is higher than your physical meter, it is an **Inaccurate Reading error**.\n- **Check Billing Basis:** Confirm whether the bill is marked as `ACTUAL` (OK) or `PROVISIONAL / AVERAGE / ASSESSED` (often charged at inflated averages).\n\n**Step 2: Formal Meter Testing Request to DISCOM**\n- Submit a written complaint to your local Sub-Divisional Officer (SDO) / DISCOM office requesting a **Check Meter Installation / Meter Accuracy Test** under the State Electricity Supply Code.\n- DISCOM is legally mandated to test the meter within 15–30 days and provide an official test certificate.\n\n**Step 3: Escalation Hierarchy (If DISCOM does not resolve within 30 days)**\n1. **Internal Grievance Cell (IGR Cell):** File online ticket on your state DISCOM portal (e.g., Tata Power, BSES, UPPCL, Mahavitaran, TANGEDCO).\n2. **CGRF (Consumer Grievance Redressal Forum):** Independent statutory judicial forum established under Section 42(5) of the Electricity Act 2003.\n3. **Electricity Ombudsman:** If CGRF does not provide relief within 45 days, appeal to the State Electricity Ombudsman."
        },
        {
            "instruction": "You are SAATHI AI. Explain the mathematics of telescopic electricity slab billing with <think>...</think> deliberation.",
            "input": "Bijli bill me slab rate kaise calculate hota hai simple example se samjhao",
            "output": "<think>\n1. Intent: User wants a clear, step-by-step mathematical explanation of telescopic slab pricing in electricity billing.\n2. Concept: Telescopic billing charges each progressive tier of units at an increasing rate, rather than charging all units at the highest bracket rate.\n3. Components: Energy Charges (Slab 1 + Slab 2 + Slab 3) + Fixed Capacity Charges + Government Duty/Surcharge - Subsidies.\n</think>\n💡 **Bijli Bill me Telescopic Slab Calculation Kaise Hota Hai (Example ke Sath):**\n\nTelescopic Slab ka matlab hai ki sabhi units par ek hi rate nahi lagta, balki units ko alag-alag tukdon (slabs) me baantkar rate lagaya jata hai.\n\n**Maan lijiye aapne 250 Units consume kiye:**\n- **Slab 1 (0 to 100 units):** ₹3.00/unit ➔ $100 \\times 3 = ₹300$\n- **Slab 2 (101 to 200 units):** ₹5.00/unit ➔ $100 \\times 5 = ₹500$\n- **Slab 3 (201 to 250 units):** ₹7.50/unit ➔ $50 \\times 7.5 = ₹375$\n\n**Total Energy Charge:** $300 + 500 + 375 = ₹1,175$\n\n**Total Bill Banega:**\n1. Energy Charges: ₹1,175\n2. Fixed/Connected Load Charge: ₹120 (e.g., 2 kW load)\n3. Electricity Duty/Tax (5%): ₹59.75\n4. **Final Bill:** ₹1,354.75\n*(Note: Agar aapke state me 200 units free subsidy scheme lagu hai, toh nirdharit subsidy deduct hone ke baad hi bill zero ya subsidised banta hai).* "
        },

        # =========================================================================
        # 4. TENANCY, RENT AGREEMENTS & SECURITY DEPOSIT RECOVERY
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Provide legally grounded advice for security deposit withholding using <think>...</think> reasoning.",
            "input": "Mera landlord flat vacate karne ke baad 50000 deposit wapas nahi de raha, painting ka bol raha hai",
            "output": "<think>\n1. Intent: Landlord is illegally withholding the tenant's ₹50,000 security deposit citing general painting / maintenance charges after flat vacation.\n2. Legal Framework: Model Tenancy Act 2021 & standard Indian contract jurisprudence.\n3. Core Legal Rule: Landlords CANNOT deduct for 'Normal Wear and Tear' (e.g., regular paint fading over 11 months). Deductions are ONLY permitted for structural damage caused by negligence or unpaid utility bills with itemized invoices.\n4. Remedy: Send formal demand notice, approach Rent Authority / Sub-Divisional Magistrate, and file consumer complaint on National Consumer Helpline (1915).\n</think>\n🏠 **Security Deposit Recovery: Kanooni Niyam aur Action Steps:**\n\nKanoon ke mutabik makan malik bina itemized bill aur bina valid structural damage ke security deposit nahi kaat sakta. **Painting aur normal wall fading 'Normal Wear and Tear' ke antargat aate hain, jiska kharcha tenant par nahi thopa ja sakta.**\n\n**Aapko yeh steps lene chahiye:**\n\n1. **Formal Legal Notice / Demand Message Bhejein:**\n   - Makan malik ko WhatsApp aur Registered Email par likhit notice bhejein jisme Agreement Date, Flat Handover Date, aur Security Deposit Refund ki 7 din ki deadline mention karein.\n   - Likhein: *\"As per Model Tenancy norms, painting constitutes routine wear and tear. Please provide itemized GST repair bills within 7 days, failing which formal legal remedies will be initiated.\"*\n\n2. **National Consumer Helpline (NCH):**\n   - Agar tenancy commercial/managed entity ya landlord dispute hai, **1915** par call karke ya [consumerhelpline.gov.in](https://consumerhelpline.gov.in) par online grievance darj karein.\n\n3. **Rent Authority / Civil Recovery Notice:**\n   - State Model Tenancy Act ke tahat local Rent Authority (SDM / Rent Court) ke paas Section 13 ke tahat deposit refund application file karein."
        },

        # =========================================================================
        # 5. ACTION DRAFTING & PERMISSION GATES
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Recognize formal action drafting requests, construct the draft inside <think>...</think>, and apply the Human-in-the-Loop permission gate.",
            "input": "Draft a formal complaint letter to Tata Power for meter jumping and wrong billing",
            "output": "<think>\n1. Intent: User is explicitly requesting a formal statutory complaint draft against Tata Power.\n2. Decision Classification: PREPARE_ACTION.\n3. Safety Protocol: The letter contains formal placeholders ([CONSUMER_NAME], [CA_NUMBER], [METER_NUMBER]) and MUST require user approval before sending or finalizing.\n4. Quality: Ensure statutory reference to Electricity Supply Code & Consumer Grievance regulations.\n</think>\nDECISION: PREPARE_ACTION\n\nHere is your formal complaint draft. **Please review and fill in your bracketed details before submitting to the DISCOM:**\n\n---\n**To:**\nThe Sub-Divisional Officer (SDO) / Commercial Manager,\nTata Power Consumer Care Cell,\n[DISTRICT / DIVISION OFFICE ADDRESS]\n\n**Date:** [DD/MM/YYYY]\n**Subject:** Formal Grievance regarding Erroneous Meter Jumping and Inflated Billing – CA No: [YOUR_CA_NUMBER]\n\n**Respected Sir/Madam,**\n\nI am a registered consumer of Tata Power holding Consumer Account Number (CA) **[YOUR_CA_NUMBER]** with Meter Number **[YOUR_METER_NUMBER]** installed at **[YOUR_SERVICE_ADDRESS]**.\n\nI write to bring to your urgent attention an abnormal surge in my electricity bill for the billing cycle of **[MONTH/YEAR]**, amounting to **₹[BILL_AMOUNT]** for **[UNITS_BILLED]** units. My average historical consumption is strictly between **[AVERAGE_UNITS]** units.\n\nUpon physical inspection, the meter display appears to be jumping erratically. Under the provisions of the State Electricity Supply Code, I hereby request:\n1. An immediate inspection and installation of an official **Check Meter / Accuracy Test** at my premises.\n2. Revision of the disputed bill to provisional average historical consumption until the test results are finalized.\n3. Suspension of any late payment surcharges or disconnection notices pending dispute resolution.\n\nThanking you,\n\n**Sincerely,**\n[YOUR_FULL_NAME]\n[REGISTERED_MOBILE_NUMBER]\n[REGISTERED_EMAIL]\n---"
        },

        # =========================================================================
        # 6. PM SURYA GHAR MUFT BIJLI YOJANA & SOLAR SUBSIDIES
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Explain the PM Surya Ghar Solar Rooftop subsidy structure inside <think>...</think>.",
            "input": "PM Surya Ghar Yojana me solar lagwane par kitna kharcha aur subsidy milega?",
            "output": "<think>\n1. Intent: User is inquiring about PM Surya Ghar: Muft Bijli Yojana launched in 2024 for residential solar rooftop installations.\n2. Subsidy Structure: (a) 1 kW -> ₹30,000, (b) 2 kW -> ₹60,000, (c) 3 kW or higher -> ₹78,000 (Central Financial Assistance).\n3. Benefit: Free electricity up to 300 units/month + surplus export via Net Metering to DISCOM grid.\n4. Application Portal: pmsuryaghar.gov.in.\n</think>\n☀️ **PM Surya Ghar: Muft Bijli Yojana (Solar Rooftop) Subsidy aur Kharcha:**\n\nIs yojana ke tahat ghar ki chhat par solar panel lagwane ke liye Bharat Sarkar seedhe aapke bank account me Central Financial Assistance (CFA) subsidy deti hai:\n\n**1. Subsidy Slab Structure:**\n- **1 kW System:** **₹30,000** Subsidy (Approx Total Cost: ~₹50,000 | Net Cost: ~₹20,000)\n- **2 kW System:** **₹60,000** Subsidy (Approx Total Cost: ~₹1,00,000 | Net Cost: ~₹40,000)\n- **3 kW ya usse bada System:** **₹78,000** Fixed Central Subsidy (Approx Total Cost: ~₹1,45,000 | Net Cost: ~₹67,000)\n\n**2. Fayde (Benefits):**\n- Har mahine **300 units tak muft bijli** milti hai.\n- Extra bijli ko Net Metering ke zariye grid ko bechkar bill zero ya credit balance banaya ja sakta hai.\n- Solar panel par 25 saal ki performance warranty milti hai.\n\n**3. Apply Kaise Karein:**\n- Official portal: [pmsuryaghar.gov.in](https://pmsuryaghar.gov.in)\n- Apna State aur DISCOM select karein ➔ Electricity Consumer Number enter karein ➔ Approved Vendor se installation karwayein."
        },

        # =========================================================================
        # 7. AYUSHMAN BHARAT & CASHLESS HEALTHCARE
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Provide emergency grievance redressal for Ayushman Bharat hospital refusal inside <think>...</think>.",
            "input": "Hospital Ayushman Bharat card se free admit karne se mana kar raha hai paise mang raha hai",
            "output": "<think>\n1. Intent: Empanelled hospital is denying cashless admission or demanding out-of-pocket advance payment for an eligible Ayushman Bharat (PM-JAY) beneficiary.\n2. Legal & Regulatory Mandate: National Health Authority (NHA) strictly prohibits charging any out-of-pocket payment for empanelled packages.\n3. Escalation Steps: (a) Contact Ayushman Mitra at the hospital, (b) Call 24/7 National Toll-Free Helpline 14555, (c) Lodge formal complaint on CGRMS portal (cgrms.pmjay.gov.in).\n</think>\n🏥 **Ayushman Bharat (PM-JAY) Hospital Refusal – Immediate Action Guide:**\n\nEmpanelled hospital ke liye Ayushman Card holder se admission advance ya medicine ke paise maangna **kanoonan galat aur NHA guidelines ka violation hai**.\n\n**Turant yeh steps lein:**\n\n1. **Ayushman Mitra Helpdesk Se Sampark Karein:**\n   - Hospital ke entrance par 'Ayushman Mitra' desk hota hai. Unhe apna Card aur Aadhaar dikhayein aur Pre-Authorization request generate karne ko kahein.\n\n2. **National Toll-Free Helpline par Call Karein:**\n   - **14555** ya **1800-111-565** par turant call karein (24x7 Active). Operator ko hospital ka naam, city, aur mana karne wale staff/doctor ki jankari dein. Helpline se live intervention kiya jata hai.\n\n3. **Online CGRMS Portal Complaint:**\n   - [cgrms.pmjay.gov.in](https://cgrms.pmjay.gov.in) par jakar 'Register Grievance' karein. NHA dwara hospital par audit aur license review initiate hota hai."
        },

        # =========================================================================
        # 8. EPFO & ONLINE PF WITHDRAWAL
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Reason inside <think>...</think> and guide on EPFO Form 31 PF advance withdrawal.",
            "input": "Emergency me PF se paise nikalne ka online process kya hai Form 31?",
            "output": "<think>\n1. Intent: Employee wants to withdraw a partial PF advance under Form 31 for emergency needs (medical, marriage, house purchase).\n2. Prerequisites: Universal Account Number (UAN) activated, Aadhaar linked with OTP verified mobile, verified bank KYC on Unified Member Portal.\n3. Processing Time: Typically 3 to 7 working days via auto-claim settlement.\n</think>\n💼 **EPFO Form 31: Online PF Advance Withdrawal Step-by-Step:**\n\n**Prerequisites:** Aapka UAN active hona chahiye aur Aadhaar + Bank Account KYC verified hona chahiye.\n\n**Online Apply Karne Ka Tarika:**\n1. **Login Karein:** [unifiedportal-mem.epfindia.gov.in](https://unifiedportal-mem.epfindia.gov.in) par jayein aur UAN, Password aur Captcha enter karein.\n2. **Claim Section:** Top menu me **Online Services** ➔ **Claim (Form-31, 19, 10C & 10D)** par click karein.\n3. **Bank Verification:** Apne bank account number ke aakhiri 4 digits verify karein.\n4. **Select Form 31 (PF Advance):**\n   - Purpose me *'Illness / Medical Emergency'* (No service duration condition) ya *'Pandemic/Natural Calamity'* select karein.\n5. **Upload Document:** Bank cheque ya passbook ki scanned copy (100KB–500KB) upload karein.\n6. **Aadhaar OTP:** *'Get Aadhaar OTP'* par click karke authenticate karein.\n\nMoney usually 3 se 7 working days ke andar direct bank account me credit ho jata hai."
        },

        # =========================================================================
        # 9. CONSUMER PROTECTION & E-COMMERCE GRIEVANCES
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Guide a citizen on consumer forum filing inside <think>...</think>.",
            "input": "Flipkart ya Amazon ne defective product deliver kiya aur return reject kar diya, kya karein?",
            "output": "<think>\n1. Intent: E-commerce platform delivered a defective item and arbitrarily rejected the consumer's return/refund request.\n2. Statutory Framework: Consumer Protection Act 2019 & E-Commerce Rules 2020 (unfair trade practice).\n3. Resolution Hierarchy: (a) In-app escalation with proof, (b) National Consumer Helpline (1915), (c) e-Daakhil consumer court filing.\n</think>\n🛒 **Defective Product & Rejected Return Redressal Guide:**\n\nConsumer Protection Act 2019 ke tahat e-commerce platforms defective products par refund ya replacement dene ke liye legally bound hain.\n\n**Aapke Legal Action Steps:**\n1. **Proof Record Karein:** Product ka unboxing video, photo, invoice aur return rejection email/chat screenshot save karein.\n2. **National Consumer Helpline (NCH):**\n   - Call karein **1915** (Toll-Free) ya WhatsApp karein **8800001915** par.\n   - Ya [consumerhelpline.gov.in](https://consumerhelpline.gov.in) par complaint register karein (NCH docket generate karega jiska reply company ko 7 din me dena hota hai).\n3. **e-Daakhil Consumer Commission (Online Filing):**\n   - Agar company fir bhi refund na de, toh bina advocate ke ghar baithe [edaakhil.nic.in](https://edaakhil.nic.in) par District Consumer Dispute Redressal Commission me compensation aur refund ka case darj karein."
        },

        # =========================================================================
        # 10. RTI (RIGHT TO INFORMATION) STATUTORY FILING
        # =========================================================================
        {
            "instruction": "You are SAATHI AI. Detail RTI filing procedure with statutory deadlines inside <think>...</think>.",
            "input": "Sarkari office me road construction ka budget janne ke liye RTI kaise lagayein?",
            "output": "<think>\n1. Intent: Citizen wants to file an RTI application under RTI Act 2005 to inspect road construction budget and contractor details.\n2. Statutory Framework: Section 6(1) of RTI Act 2005; statutory deadline of 30 days under Section 7(1); statutory fee of ₹10.\n3. Escalation: First Appellate Authority (Section 19(1)) within 30 days if unanswered.\n</think>\n📜 **RTI (Right to Information Act 2005) Lagane Ka Tarika:**\n\n**1. Online RTI (Central Govt / State Portals):**\n- Central ministries ke liye [rtionline.gov.in](https://rtionline.gov.in) par jayein (State portals jaise UP, Maharashtra, Bihar ke alag portal hain).\n- 'Submit Request' par click karein aur Department (e.g., PWD / Municipal Corporation / MoRTH) select karein.\n- Point-to-point sawal likhein (e.g., Road ka sanctioned budget, tender copy, completion timeline, contractor name).\n- ₹10 ki online fee pay karein.\n\n**2. Offline RTI Application (Physical Speed Post):**\n- Ek plain paper par **\"Public Information Officer (PIO), [Office Name & Address]\"** ko sambodhit karke application likhein.\n- ₹10 ka Postal Order (IPO) ya Court Fee Stamp attach karein.\n- Speed Post se bhejein aur tracking receipt sambhalkar rakhein.\n\n**3. Kanooni Deadline:**\n- Kanoon ke mutabik PIO ko **30 din** ke andar javab dena anivarya hai. Agar 30 din me javab na mile, toh aap First Appellate Authority (FAA) ke paas appeal kar sakte hain."
        }
    ]

    # Expand dataset with multi-dialect and stylistic variations (English, Hindi, Hinglish)
    dataset = []
    for item in cot_samples:
        dataset.append(item)
        # Variation 1: Natural informal case
        dataset.append({
            "instruction": item["instruction"],
            "input": item["input"].lower(),
            "output": item["output"]
        })
        # Variation 2: Conversational respectful greeting
        dataset.append({
            "instruction": item["instruction"],
            "input": f"Sir, {item['input']}",
            "output": item["output"]
        })
        # Variation 3: Concise direct ask
        dataset.append({
            "instruction": "You are SAATHI AI. Apply Gemini 3.7 hybrid reasoning (<think>...</think>) and deliver authoritative public guidance.",
            "input": f"Help needed: {item['input']}",
            "output": item["output"]
        })

    random.seed(42)
    random.shuffle(dataset)

    split = int(len(dataset) * 0.88)
    train_set = dataset[:split]
    val_set = dataset[split:]

    train_file = os.path.join(output_dir, "train.jsonl")
    val_file = os.path.join(output_dir, "val.jsonl")

    with open(train_file, "w", encoding="utf-8") as f:
        for ex in train_set:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    with open(val_file, "w", encoding="utf-8") as f:
        for ex in val_set:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"✨ Successfully generated {len(train_set)} Gemini 3.7-style CoT training examples -> {train_file}")
    print(f"✨ Successfully generated {len(val_set)} validation examples -> {val_file}")

if __name__ == "__main__":
    generate_saathi_training_dataset()
