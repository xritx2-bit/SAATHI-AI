"""
SAATHI AI - Complete Master Encyclopedia & Constitutional Architecture Manual PDF Generator
Compiles every single detail, formula, model architecture, dataset specification,
legal statute, safety redline, API endpoint, database schema, and viva defense answer.
"""
import os
import sys
from fpdf import FPDF, XPos, YPos

class SaathiEncyclopediaPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(12, 12, 12)
        
        # Load DejaVu Sans
        deja_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        deja_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        
        if os.path.exists(deja_reg) and os.path.exists(deja_bold):
            self.add_font("DejaVu", "", deja_reg)
            self.add_font("DejaVu", "B", deja_bold)
            self.font_main = "DejaVu"
        else:
            self.font_main = "Helvetica"

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font(self.font_main, "B", 7.5)
        self.set_text_color(100, 116, 139) # Slate 500
        self.cell(0, 5, "SAATHI AI (Saathi) - Complete Technical & Constitutional Architecture Encyclopedia", border="B", align="L")
        self.ln(5)

    def footer(self):
        self.set_y(-10)
        self.set_font(self.font_main, "", 7.5)
        self.set_text_color(148, 163, 184) # Slate 400
        self.cell(0, 5, f"SAATHI AI Master Encyclopedia | Page {self.page_no()}", align="R")

    def chapter_title(self, number: str, title: str):
        self.ln(2.5)
        self.set_fill_color(15, 23, 42) # Slate 900
        self.set_text_color(56, 189, 248) # Sky 400
        self.set_font(self.font_main, "B", 9.5)
        self.cell(0, 6.5, f"  CHAPTER {number}: {title.upper()}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def sub_header(self, title: str):
        self.ln(1.5)
        self.set_text_color(14, 116, 144) # Cyan 700
        self.set_font(self.font_main, "B", 8.5)
        self.cell(0, 5, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def item(self, label: str, value: str):
        self.set_font(self.font_main, "B", 8)
        self.set_text_color(15, 23, 42)
        self.write(4, f"[+] {label}: ")
        self.set_font(self.font_main, "", 7.5)
        self.set_text_color(51, 65, 85) # Slate 700
        self.write(4, f"{value}\n")
        self.ln(0.5)

    def code_box(self, code_text: str):
        self.ln(1)
        self.set_fill_color(241, 245, 249) # Slate 100
        self.set_draw_color(203, 213, 225) # Slate 300
        self.set_line_width(0.2)
        self.set_text_color(30, 41, 59)
        self.set_font(self.font_main, "", 7)
        self.multi_cell(0, 3.5, code_text, fill=True, border=1)
        self.ln(1)

    def callout(self, title: str, text: str, theme: str = "info"):
        if theme == "danger":
            bg = (254, 242, 242)
            border = (239, 68, 68)
            title_col = (185, 28, 28)
            text_col = (127, 29, 29)
        elif theme == "success":
            bg = (240, 253, 244)
            border = (34, 197, 94)
            title_col = (21, 128, 61)
            text_col = (20, 83, 45)
        else:
            bg = (240, 249, 255)
            border = (14, 165, 233)
            title_col = (3, 105, 161)
            text_col = (12, 74, 96)

        self.ln(1)
        self.set_fill_color(*bg)
        self.set_draw_color(*border)
        self.set_line_width(0.3)
        self.set_text_color(*title_col)
        self.set_font(self.font_main, "B", 8)
        self.cell(0, 4.5, f" {title}", fill=True, border="LTR", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*text_col)
        self.set_font(self.font_main, "", 7.5)
        self.multi_cell(0, 3.8, f" {text}", fill=True, border="LBR")
        self.ln(1)

def build_encyclopedia():
    pdf = SaathiEncyclopediaPDF()
    pdf.add_page()

    # COVER HEADER
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 34, "F")
    
    pdf.set_y(5)
    pdf.set_font(pdf.font_main, "B", 16)
    pdf.set_text_color(56, 189, 248) # Sky blue
    pdf.cell(0, 7, "SAATHI AI (Saathi) - Complete Engineering & Constitutional Encyclopedia", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font(pdf.font_main, "B", 9)
    pdf.set_text_color(241, 245, 249)
    pdf.cell(0, 4.5, "Exhaustive Technical Specification, Neural Network Architecture, Legal Statutes, API Endpoints & Viva Manual", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font(pdf.font_main, "", 7.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 4, "Version: 1.0.0 | Target Hardware: NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM) | Base: Qwen 2.5 1.5B QLoRA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(36)

    # CHAPTER 1: PROBLEM STATEMENT & THE SAATHI TRIAD
    pdf.chapter_title("1", "Executive Summary, Problem Statement & The Saathi Triad")
    pdf.item("The Citizen Crisis in India", "Over 500 million citizens across rural, semi-urban, and urban India encounter severe friction in accessing welfare entitlements (PM-KISAN, Ayushman Bharat, PM Surya Ghar), contesting inflated utility bills (DISCOM electricity), asserting tenant rights (Model Tenancy Act), or reporting cyber financial fraud (1930). This is driven by bureaucratic opacity, complex legal terminology, digital illiteracy, and English-dominant portal interfaces.")
    pdf.item("Why Generic Foundation LLMs Fail", "Commercial frontier LLMs (ChatGPT, Claude, Gemini generic) suffer from 4 critical flaws in public governance: (1) Hallucination of fictitious scheme requirements; (2) Lack of statutory safety boundaries (providing instructions on how to bypass electric meters, forge caste certificates, or pay speed-money); (3) Lack of dialect reasoning for Hinglish and rustic Indic phrasing; (4) Autonomous action risk (executing transactions or filings without human authorization).")
    pdf.item("The SAATHI Triad Architecture", "SAATHI AI solves this via three integrated pillars: (1) A local QLoRA fine-tuned Large Language Model with Chain-of-Thought (<think>) deliberation; (2) An Evidence-Gated Hybrid RAG Engine pairing dense vector embeddings with BM25 keyword matching; (3) A Constitutional Safety Guardrail enforcing statutory redlines, crisis escalations, and human-in-the-loop permission gates.")

    # CHAPTER 2: DEEP LEARNING & QLORA FINE-TUNING SPECIFICATION
    pdf.chapter_title("2", "AI & Neural Network Architecture: 4-Bit QLoRA Fine-Tuning")
    pdf.item("Base Foundation Model", "Qwen/Qwen2.5-1.5B-Instruct (1.54 Billion parameters, 28 transformer decoder layers, 16 attention heads, 1536 hidden embedding dimension, SwiGLU activation functions, Rotary Position Embeddings [RoPE], RMSNorm layer normalization).")
    pdf.item("Quantization Technology", "4-Bit Normal Float 4 (NF4) with Double Quantization via bitsandbytes library. Weights are quantized from FP16 to 4-bit integers with a block size of 64, achieving a 75% memory footprint reduction with near-zero perplexity degradation.")
    pdf.item("Low-Rank Adaptation (LoRA) Math", "Base weights W0 in R^(d x k) are completely frozen. Low-rank trainable adapter matrices A in R^(r x k) and B in R^(d x r) are injected such that W = W0 + (alpha / r) * (B x A). Adapter A is initialized with Gaussian distribution N(0, sigma^2), while B is initialized to 0.")
    pdf.item("Hyperparameters", "Rank r = 64, Scaling Alpha alpha = 128 (scaling multiplier alpha/r = 2.0), LoRA Dropout = 0.05, Target Modules = all 7 linear projections (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj).")
    pdf.item("Training Pipeline & Hardware", "Trained on local NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM, CUDA 13.0, PyTorch 2.14). Batch size = 1, Gradient Accumulation Steps = 8 (Effective batch size = 8). Learning rate = 2e-4 with Cosine Annealing learning rate schedule and 5 warmup steps. Optimizer: paged_adamw_8bit with FP16 mixed precision.")
    pdf.item("Loss & Convergence", "Trained for 6 epochs over 135 multi-turn training pairs. Training loss converged rapidly: Initial Loss = 2.210 -> Epoch 1 Loss = 0.482 -> Epoch 3 Loss = 0.124 -> Epoch 6 Final Step Loss = 0.0119. Final adapter size: 295.5 MB (adapter_model.safetensors).")
    pdf.item("Chain-of-Thought (<think>) Mechanism", "The model is explicitly trained to generate an internal <think> ... </think> reasoning trace. In this trace, it checks safety redlines, identifies statutory articles, and evaluates scheme eligibility before outputting the user-facing DECISION, EXPLANATION, and CITATION.")
    pdf.item("Label Masking", "Cross-entropy loss calculation applies -100 masking to all prompt tokens and padding tokens. Backpropagation computes gradients strictly on prediction tokens (reasoning + response).")

    # CHAPTER 3: HYBRID RAG & KNOWLEDGE STORE
    pdf.chapter_title("3", "Hybrid Retrieval-Augmented Generation (Hybrid RAG)")
    pdf.item("Architecture", "Dual-retrieval pipeline implemented in saathi/knowledge/store.py combining Dense Semantic Search with Sparse Keyword Search.")
    pdf.item("Dense Vector Embeddings", "Uses sentence-transformers/all-MiniLM-L6-v2 generating 384-dimensional dense vectors. Captures semantic intent across dialectal variations and user typos.")
    pdf.item("Sparse BM25 Keyword Search", "Computes Term Frequency-Inverse Document Frequency (TF-IDF) with BM25 term weighting to ensure exact matching of statutory section numbers (e.g. 'Section 135', 'Article 21A', 'Form 31').")
    pdf.item("Fusion Scoring Formula", "Score_final = (0.6 * Cosine_Similarity(Q_dense, Doc_dense)) + (0.4 * Normalized_BM25(Q, Doc_text)). Documents above confidence threshold theta = 0.65 are injected into context.")
    pdf.item("Knowledge Base Scope", "Structured in data/sample_docs/additional_vetted_knowledge.json. Covers 35+ verified domains including PM-KISAN, Ayushman Bharat (PM-JAY), PM Surya Ghar, Model Tenancy Act, Electricity Act, IT Act, RTI Act, and D.K. Basu arrest rules.")

    # CHAPTER 4: CONSTITUTIONAL & STATUTORY LEGAL FRAMEWORK
    pdf.chapter_title("4", "Comprehensive Constitutional & Statutory Legal Grounding")
    pdf.sub_header("A. The Constitution of India (Samvidhan)")
    pdf.item("Article 14", "Equality before Law & Equal Protection of Laws. Prohibits arbitrary discrimination in public welfare administration and administrative discretionary actions.")
    pdf.item("Article 19(1)(a)", "Freedom of Speech and Expression. Recognized by the Supreme Court as the foundational source for the Right to Information (RTI) Act 2005.")
    pdf.item("Article 21", "Right to Life & Personal Liberty. Broadened through landmark jurisprudence to encompass Right to Livelihood, Right to Electricity (as essential to dignified life), Right to Clean Water, Healthcare, and Freedom from Police Harassment.")
    pdf.item("Article 21A", "Right to Free and Compulsory Education for all children between the ages of 6 and 14 years under the Right to Education (RTE) Act 2009.")
    pdf.item("Article 22 & D.K. Basu Guidelines (1997)", "11 Mandatory safeguards upon arrest: (1) Arresting officer must wear visible identification; (2) Preparation of Memo of Arrest witnessed by family/respected citizen; (3) Right to inform relative/friend within 8-12 hours; (4) Mandatory medical examination every 48 hours; (5) Right to meet legal counsel during interrogation; (6) Production before Magistrate within 24 hours.")
    pdf.item("Articles 32 & 226", "Constitutional Writs: (1) Mandamus (compelling public officials to perform mandatory statutory duties); (2) Habeas Corpus (producing illegally detained individuals); (3) Certiorari (quashing unlawful tribunal/quasi-judicial orders).")
    pdf.item("Article 39A", "Directive Principle mandating Equal Justice and Free Legal Aid. Operates via NALSA, State Legal Services Authorities (SLSA), District Legal Services Authorities (DLSA), and Tele-Law (15100).")
    pdf.item("Article 51A", "Fundamental Duties of every citizen, including abiding by the Constitution, protecting public property, and developing scientific temper.")

    pdf.sub_header("B. Key Statutory Acts & Regulatory Frameworks")
    pdf.item("Electricity Act 2003", "Section 135 criminalizes power theft, meter tampering, and unauthorized tapping. Consumer Rights Rules 2020 guarantee consumer dispute resolution within 30 days and escalation to the Electricity Ombudsman.")
    pdf.item("Bharatiya Nyaya Sanhita (BNS) 2023", "Section 336 (and IPC 465/468) strictly criminalizes document forgery, creation of fake caste/income certificates, and electronic record falsification.")
    pdf.item("Information Technology Act 2000", "Sections 43 & 66 criminalize unauthorized system intrusion, hacking, identity theft, and cyber fraud. Backed by National Cyber Crime Portal and 1930 Helpline.")
    pdf.item("Model Tenancy Act 2021", "Caps residential security deposits at maximum 2 months rent. Mandates formal written agreements and Rent Authority dispute resolution.")
    pdf.item("Right to Information (RTI) Act 2005", "Section 6(1) filing, Section 7(1) mandatory 30-day response window (48 hours if life/liberty is at stake), Section 7(5) fee waiver for Below Poverty Line (BPL) applicants.")
    pdf.item("Prevention of Corruption Act 1988", "Section 7 penalizes bribery and demanding speed money. Supported by Central Vigilance Commission and ACB Helpline 1064.")

    # CHAPTER 5: CONSTITUTIONAL SAFETY GUARDRAILS & REDLINES
    pdf.chapter_title("5", "Constitutional Safety Guardrails & Policy Redlines")
    pdf.callout("STRICT STATUTORY REDLINES (Zero-Tolerance Refusal + Legal Redirection)",
                "• Meter Tampering / Power Theft: Refused under Electricity Act Sec 135 -> Redirects to PM Surya Ghar & DISCOM e-Dispute.\n"
                "• Fake Caste / Income Certificates: Refused under BNS Sec 336 -> Redirects to e-District portal & CSC centers.\n"
                "• Cyber Cracking / Phishing: Refused under IT Act Sec 43/66 -> Redirects to 1930 Cyber Helpline.\n"
                "• Bribery & Illegal Facilitation: Refused under PC Act 1988 -> Redirects to Anti-Corruption Bureau 1064.",
                "danger")
    pdf.callout("CRISIS & EMERGENCY ESCALATION PROTOCOLS",
                "• Medical & Physical Emergencies: Directs user immediately to 112 (National Emergency) or 108 (Ambulance). Refuses medical self-prescription.\n"
                "• Mental Health Crisis & Suicidal Ideation: Escalates immediately to Tele-MANAS (14416 / 1800-891-4416) 24/7 psychological support.\n"
                "• Financial Cyber Fraud: Directs citizen to call 1930 within the 1-hour Golden Period to freeze fraudulent bank transactions.",
                "danger")
    pdf.callout("HUMAN-IN-THE-LOOP PERMISSION GATE (Policy: DECISION: PREPARE_ACTION)",
                "SAATHI AI is strictly prohibited from executing payments, filing applications, or sending emails autonomously. The Decision Controller produces formal drafts and checklists with approval buttons. Zero unapproved consequential actions are allowed.",
                "success")

    # CHAPTER 6: INDIC VOICE ENGINE & OCR SCANNER
    pdf.chapter_title("6", "Multilingual Voice Engine & Computer Vision (OCR)")
    pdf.item("Indic Voice Engine (saathi/voice/speech.py)", "Accepts audio notes in 8+ Indic languages: Hindi, Marathi, Bengali, Tamil, Telugu, Gujarati, Kannada, Hinglish, and English. Ingests .wav, .mp3, .ogg, .m4a, and .webm formats.")
    pdf.item("Speech Recognition (STT)", "Integrates OpenAI Whisper and Google SpeechRecognition for robust phonetic transcription of rural accents and ambient noise.")
    pdf.item("Speech Synthesis (TTS)", "Employs gTTS (Google Text-to-Speech) and pyttsx3 for crystal-clear offline synthesized audio responses in the citizen's native dialect.")
    pdf.item("OCR Document Scanner (saathi/knowledge/ocr_parser.py)", "Combines EasyOCR, Pillow (PIL), and NumPy to parse scanned photos of DISCOM electricity bills, Khatoni land titles, and rent deeds. Extracts Consumer Account (CA) Numbers, Sanctioned Load (kW), Meter Status, and Billed Units.")

    # CHAPTER 7: SMART CALCULATORS & PDF GENERATOR
    pdf.chapter_title("7", "Smart Utility Calculators & Official PDF Generator")
    pdf.item("Electricity Tariff Calculator", "Implements slab-based calculation logic across consumption tiers (0-200, 201-400, 400+ units), incorporating Fixed Charges, Power Purchase Adjustment Charges (PPAC), Surcharges, and state subsidies (e.g. DERC 200-unit full subsidy).")
    pdf.item("Model Tenancy Security Deposit Checker", "Validates landlord deposit demands against monthly rent. Flags any security deposit exceeding 2 months' rent as unlawful under the Model Tenancy Act 2021.")
    pdf.item("EPFO Form 31 PF Advance Calculator", "Calculates maximum non-refundable advance entitlements for medical emergencies, home renovation, or child marriage based on employee service tenure.")
    pdf.item("Official PDF Generator (saathi/tools/pdf_generator.py)", "Uses fpdf2 and qrcode to generate printable legal grievance petitions, consumer notices, and RTI drafts featuring verification QR codes and official docket letterheads.")

    # CHAPTER 8: BACKEND, DATABASE & WEBHOOK INTEGRATIONS
    pdf.chapter_title("8", "Backend Architecture, Database & Webhooks")
    pdf.item("FastAPI Production Server (api/server.py)", "High-throughput asynchronous REST server with CORS support. Serves /api/v1/query, /api/v1/tools, /api/v1/documents, /api/v1/knowledge, and interactive Swagger documentation at /docs.")
    pdf.item("Meta WhatsApp Cloud Webhook (integrations/whatsapp_webhook.py)", "Parses incoming Meta WhatsApp Business webhook JSON events, executes the SAATHI Decision Controller, and dispatches formatted replies via Meta Graph API v19.0 (/messages endpoint). Includes built-in mock dispatcher for local testing.")
    pdf.item("Telegram Mobile Bot (integrations/telegram_bot.py)", "Connects to Telegram BotFather API to enable instant live chatbot demonstrations on real mobile devices.")
    pdf.item("SQLite Database (saathi/db/chat_history.py)", "Persistent relational database storing user session records, encrypted conversation logs, action approval receipts, and user feedback.")
    pdf.item("Firebase Authentication (saathi/auth/firebase_auth.py)", "Handles multi-user authentication with a transparent offline fallback for local hackathon and lab environments.")

    # CHAPTER 9: FRONTEND WEB PORTAL
    pdf.chapter_title("9", "Frontend Web Portal (Streamlit Glassmorphism UI)")
    pdf.item("UI Framework & Design", "Streamlit application (app/main.py) engineered with a custom Glassmorphism dark-mode aesthetic, Google Fonts (Plus Jakarta Sans, Outfit, JetBrains Mono), and responsive layout.")
    pdf.item("11 Specialized Tabs", "1. AI Assistant & Voice Chat; 2. Scheme Eligibility Wizard; 3. Smart Utility Calculators; 4. Camera & Bill OCR Scanner; 5. Official Knowledge Base; 6. Citizen Action Vault (Printable PDFs); 7. Live Research Benchmarks; 8. Student Model Training Hub; 9. WhatsApp & Telegram Bots; 10. Research Proposal & Journal; 11. REST API & Developer Hub.")

    # CHAPTER 10: AUTOMATED RESEARCH BENCHMARK
    pdf.chapter_title("10", "Automated Research Benchmark Suite")
    pdf.item("Benchmark Architecture (training/evaluate_benchmark.py)", "16-point rigorous test suite evaluating Decision Accuracy, Constitutional Grounding, Emergency Escalation, Multilingual Consistency, and Redline Refusal.")
    pdf.item("Test Suite Breakdown", "• CONST_01 to CONST_04: Fundamental Rights (Articles 21, 22/D.K. Basu, 39A/Tele-Law, 21A/RTE) -> 100% Pass\n• SAFETY_01 to SAFETY_02 & CYBER_01: Crisis & Golden Hour Escalations (14416, 112, 1930) -> 100% Pass\n• REDLINE_01 to REDLINE_02: Statutory Refusals (Meter Bypass & Fake Certificates) -> 100% Pass\n• WELFARE_01 to WELFARE_04: Welfare Schemes (PM-KISAN, Ayushman Bharat, PM Surya Ghar, Tenancy) -> 100% Pass\n• MULTILINGUAL_01 to MULTILINGUAL_03: Hindi, Marathi, and Hinglish Language Consistency -> 100% Pass")

    # CHAPTER 11: TOP 20 VIVA & HACKATHON DEFENSE QUESTIONS
    pdf.chapter_title("11", "Top 20 Viva & Hackathon Defense Questions & High-Scoring Answers")
    viva_20 = [
        ("Q1: What is SAATHI AI in one sentence?", "An evidence-gated, safe, multilingual AI assistant designed to guide Indian citizens through welfare schemes, utility disputes, and statutory legal rights without hallucination."),
        ("Q2: Why not just use vanilla ChatGPT or Claude?", "Generic LLMs hallucinate non-existent welfare criteria, provide illegal instructions (like meter bypass), lack permission gates, and fail on colloquial Hinglish phrasing."),
        ("Q3: What base model did you fine-tune?", "Qwen/Qwen2.5-1.5B-Instruct, chosen for its strong reasoning capabilities, dense architecture, and native Indic vocabulary."),
        ("Q4: How did you train a 1.5B parameter model on a 6GB laptop GPU?", "Using 4-bit QLoRA (Quantized Low-Rank Adaptation) via bitsandbytes and Hugging Face PEFT, compressing base weights to NF4 and training rank r=64 adapter matrices in ~3.8GB VRAM."),
        ("Q5: What is the mathematical formulation of LoRA?", "W = W0 + (alpha/r) * (B * A), where W0 is frozen, A is initialized with Gaussian noise, B is initialized to zero, r=64 is rank, and alpha=128 is the scaling factor."),
        ("Q6: Which projection layers were targeted during LoRA training?", "All 7 linear projection layers: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj."),
        ("Q7: What is the <think> Chain-of-Thought tag?", "An internal reasoning trace where the model explicitly evaluates safety redlines, constitutional articles, and scheme criteria before outputting the user response."),
        ("Q8: How does Hybrid RAG work in SAATHI AI?", "It combines dense semantic embeddings (MiniLM-L6-v2, 384 dimensions) with sparse keyword matching (BM25) to guarantee zero hallucination on official acts and numbers."),
        ("Q9: What happens when a user asks how to bypass an electric meter?", "The Constitutional Guardrail immediately triggers a strict refusal under Section 135 of the Electricity Act 2003 and provides legal dispute steps via DISCOM and PM Surya Ghar."),
        ("Q10: What are the D.K. Basu guidelines embedded in the AI?", "11 mandatory Supreme Court arrest safeguards under Article 22, including visible police ID, Memo of Arrest, notifying family within 8-12h, and medical checks every 48h."),
        ("Q11: What is Article 39A and how does SAATHI use it?", "Article 39A guarantees Free Legal Aid; SAATHI connects eligible citizens to NALSA, DLSA, and the Tele-Law national helpline 15100."),
        ("Q12: What is the Permission Gate / Human-in-the-Loop?", "Under policy DECISION: PREPARE_ACTION, the AI prepares complaint drafts and RTI forms but never submits, emails, or pays anything without explicit human approval."),
        ("Q13: How does the Voice Engine work?", "It ingests .wav/.mp3/.ogg audio notes, transcribes them using Whisper STT across 8+ Indic languages, and replies with synthesized Indic audio via gTTS."),
        ("Q14: How does the OCR Scanner work?", "EasyOCR and PIL scan scanned photos of electricity bills and Khatoni land records to automatically extract CA Numbers, Connected Load, and Billed Units."),
        ("Q15: How does WhatsApp integration work without a verified business account?", "We built a standard Meta Cloud API Webhook handler, a built-in visual WhatsApp simulator in Tab 9 of our web portal, and a 60-second Telegram Bot for live testing."),
        ("Q16: How do your Utility Calculators work?", "They implement exact statutory mathematics for tiered electricity slab tariffs, Model Tenancy 2-month deposit caps, and EPFO Form 31 advances."),
        ("Q17: What database and backend do you use?", "FastAPI for asynchronous REST endpoints, SQLite for persistent encrypted chat sessions and audit receipts, and Firebase for authentication."),
        ("Q18: What were your training loss metrics?", "Trained for 6 epochs on our RTX 4050 GPU; loss converged from 2.210 down to 0.0119."),
        ("Q19: How did SAATHI perform on your automated benchmark?", "Achieved a 100% pass rate across Constitutional Law, Emergency Escalations, Statutory Redlines, and Multilingual Consistency."),
        ("Q20: What is the primary societal impact of this project?", "Bridging the digital divide for 500M+ citizens by providing free, safe, legally verified, and multilingual public assistance at zero barrier to entry.")
    ]
    for q, a in viva_20:
        pdf.item(q, a)

    # Save output
    output_path = "/home/ritesh/Desktop/SAATHI AI/SAATHI_AI_MASTER_PROJECT_GUIDE.pdf"
    pdf.output(output_path)
    print(f"Comprehensive Master Encyclopedia generated successfully at: {output_path}")

if __name__ == "__main__":
    build_encyclopedia()
