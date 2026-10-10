# SAATHI AI 🤝
> **Evidence-Gated, Safe, Multilingual AI Assistant for Daily Life Tasks**  
> *Research Prototype & Blueprint Implementation*

---

## 🌟 Overview
**SAATHI AI** is an AI assistant designed to help people (especially across Indian communities in English, Hindi, and Hinglish) understand everyday problems—such as **electricity bills, tenant rights, consumer grievances, and government schemes (PM-KISAN, LPG Subsidies)**—find verified solutions, and draft safe next actions with **strict human approval**.

---

## 🏗️ Architecture & Core Components

```mermaid
flowchart LR
    User([User Query]) --> Safety[Safety & Guardrail Gate]
    Safety --> Lang[Language Router<br>Hindi / Hinglish / English]
    Lang --> Controller{Evidence-Gated<br>Decision Controller}
    
    Controller -->|Direct| DirectAns[Direct Response]
    Controller -->|Needs Proof| RAG[Hybrid Knowledge Store]
    Controller -->|Ambiguous| Clarify[Ask Clarification]
    Controller -->|Action Needed| DraftAction[Draft Letter/Checklist]
    Controller -->|Emergency/Risk| Escalate[Helpline Escalation]
    
    DraftAction --> HumanGate{Human Approval Gate}
    HumanGate -->|Approved| CopyAction[Final Output]
```

### Key Modules:
- **`saathi/controller/`**: Implements the Decision Policy (Direct Answer, Retrieve, Clarify, Prepare Action, Escalate).
- **`saathi/knowledge/`**: Hybrid RAG store with verified Indian utility, scheme, and legal guidelines.
- **`saathi/language/`**: Automatic detection for Hindi (Devanagari), Hinglish (Roman script Hindi), and English.
- **`saathi/safety/`**: Guardrails against prompt injection, sensitive credential leakage, and medical/legal emergencies.
- **`saathi/tools/`**: Generates formal consumer complaints, scheme checklists, and dispute letters.
- **`evaluation/`**: Repeatable automated benchmark suite comparing SAATHI against naive baselines.
- **`training/`**: QLoRA / LoRA fine-tuning pipeline for training your own model locally on GPU (RTX 4050 6GB) or Google Colab.

---

## 🚀 Quick Start (Running SAATHI)

### 1. Launch the Interactive Web App
```bash
./venv/bin/streamlit run app/main.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 2. Run the Automated Evaluation Benchmark
```bash
./venv/bin/python3 evaluation/run_benchmark.py
```

---

## 🎓 Student Model Training Guide (LoRA / QLoRA)

As a college student, you can train and fine-tune your own AI model easily without paying thousands of dollars!

1. **Read the Theory & Viva Notes:**
   Check out [`training/STUDENT_GUIDE_HOW_TO_TRAIN_YOUR_MODEL.md`](training/STUDENT_GUIDE_HOW_TO_TRAIN_YOUR_MODEL.md).

2. **Generate the Training Dataset:**
   ```bash
   ./venv/bin/python3 training/prepare_training_data.py
   ```

3. **Verify with Dry Run:**
   ```bash
   ./venv/bin/python3 training/train_qlora_local.py --dry-run
   ```

4. **Fine-Tune the Model on RTX 4050:**
   ```bash
   ./venv/bin/python3 training/train_qlora_local.py --epochs 3
   ```

5. **Test Your Trained Model:**
   ```bash
   ./venv/bin/python3 training/test_fine_tuned_model.py
   ```
