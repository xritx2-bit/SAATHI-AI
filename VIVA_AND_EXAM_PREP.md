# 🎓 SAATHI AI — College Viva & Project Exhibition Guide
> **Top 20 Questions & High-Scoring Answers for 1st-Year Engineering Students**

---

### Q1: What is SAATHI AI in simple terms?
**Answer:**
> *"SAATHI AI is an evidence-gated, safe, multilingual AI assistant designed for Indian citizens. It helps people understand everyday documents—like high electricity bills, PM-KISAN subsidy delays, rental disputes, and cyber fraud—and drafts safe next steps only after explicit user approval."*

---

### Q2: Why build this when ChatGPT already exists?
**Answer:**
> *"Generic chatbots like ChatGPT have three critical flaws for public services in India:*
> 1. *They hallucinate plausible-sounding but legally inaccurate scheme procedures.*
> 2. *They lack a permission gate and can take unauthorized actions.*
> 3. *They lack dialect routing for Hinglish (colloquial Hindi written in English letters).*
> *SAATHI AI solves this by using an Evidence-Gated Decision Controller that verifies every fact against official government documents before answering."*

---

### Q3: What is the core research hypothesis of your project?
**Answer:**
> *"Hypothesis H1 states that an agent with an adaptive decision controller—which dynamically chooses whether to answer, retrieve knowledge, ask for clarification, draft an action, or escalate—will be more reliable, safe, and cost-effective than a standard fixed RAG pipeline. In our benchmark, our controller achieved 90.0% accuracy vs 45.0% for naive RAG."*

---

### Q4: What is the difference between RAG and Model Training/Fine-Tuning?
**Answer:**
> *"Think of it like an exam:*
> - **RAG (Retrieval-Augmented Generation):** An *open-book exam*. When a user asks a question, the system searches the latest vetted documents in real-time and grounds the answer with citations.
> - **Fine-Tuning (LoRA / QLoRA):** *Studying beforehand*. We adjust the neural network's weights so it deeply understands Indian phrasing, Hinglish dialects, and decision policies without forgetting its base knowledge."*

---

### Q5: How can you train an LLM on a laptop with only 6 GB VRAM (RTX 4050)?
**Answer:**
> *"Full parameter training of an 8B model requires 32+ GB VRAM. However, we use **QLoRA (4-bit Quantized Low-Rank Adaptation)**:*
> 1. *We compress the base model weights from 16-bit floats to 4-bit integers (saving 75% memory).*
> 2. *We freeze 99% of base model weights and attach small low-rank adapter matrices ($r=16$).*
> 3. *This allows us to train 1B–3B parameter models (like Qwen 2.5 1.5B or Llama 3.2 1B) locally on our RTX 4050 GPU using less than 4.5 GB of VRAM!"*

---

### Q6: What is the "Permission Gate" / "Human-in-the-Loop" in SAATHI?
**Answer:**
> *"Under our safety policy, the AI can prepare drafts (such as consumer complaints or scheme checklists) automatically, but it is strictly prohibited from submitting, emailing, or paying anything autonomously. The user must review, optionally edit, and click 'Approve Action' before any output is finalized. Our benchmark recorded 0 unapproved consequential actions."*

---

### Q7: How does SAATHI handle high-stakes medical or legal emergencies?
**Answer:**
> *"If a user mentions severe medical symptoms (e.g. chest pain) or emergency distress, the controller triggers `ESCALATE`. It immediately refuses medical diagnosis and provides verified national emergency helplines: 112 (National Emergency), 108 (Ambulance), and 1930 (Cyber Fraud Helpline)."*

---

### Q8: What technologies did you use to build this?
**Answer:**
> *"The backend is built in Python 3.12 with Pydantic for structured validation, a custom BM25/hybrid semantic retriever, PyTorch and Hugging Face PEFT for QLoRA training, and a Streamlit web interface with real-time policy visualization."*
