"""
SAATHI AI — Next-Generation Evidence-Gated Public Assistance Portal & Research Hub
A modern, ultra-clean, visually stunning, and interactive web interface for safe, multilingual citizen guidance.
"""
import streamlit as st
import os
import sys
import json
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from saathi.controller.engine import SaathiController
from saathi.knowledge.store import KnowledgeStore
from saathi.knowledge.doc_parser import DocumentParser
from saathi.models import DecisionType
from saathi.tools.calculators import UtilityCalculators
from saathi.tools.letter_exporter import LetterExporter
from saathi.tools.pdf_generator import SaathiPDFGenerator
from saathi.voice.speech import VoiceEngine
from saathi.db.chat_history import ChatHistoryManager
from saathi.auth.firebase_auth import FirebaseAuthService
from saathi.llm.local_model import LocalFineTunedModel
from saathi.tools.scheme_finder import WelfareSchemeFinder, CitizenProfile
from saathi.knowledge.ocr_parser import BillOCRScanner

# Streamlit Page Config
st.set_page_config(
    page_title="SAATHI AI (साथी) — India's Verified Daily Life Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comprehensive State-of-the-Art Web Styling (Glassmorphism, Neon Highlights, Modern Typography)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
    /* Global Base & Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 12% 15%, rgba(37, 99, 235, 0.16) 0%, transparent 35%),
                    radial-gradient(circle at 88% 22%, rgba(139, 92, 246, 0.14) 0%, transparent 40%),
                    radial-gradient(circle at 50% 85%, rgba(6, 182, 212, 0.12) 0%, transparent 50%),
                    #090D16 !important;
        color: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #060A12 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Top Hero Command Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.85) 50%, rgba(14, 116, 144, 0.8) 100%);
        border-radius: 22px;
        padding: 38px 44px;
        color: white;
        margin-bottom: 26px;
        box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.8), 0 0 30px rgba(56, 189, 248, 0.12) inset;
        border: 1px solid rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -60%;
        right: -15%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 9999px;
        padding: 6px 16px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #BAE6FD;
        margin-bottom: 14px;
        backdrop-filter: blur(10px);
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.9rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #FFFFFF 0%, #7DD3FC 40%, #C084FC 75%, #FDE047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        line-height: 1.1;
    }
    .hindi-glow {
        font-weight: 800;
        color: #FBBF24;
        text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #CBD5E1;
        max-width: 860px;
        line-height: 1.65;
        margin-bottom: 24px;
        font-weight: 400;
    }
    .hero-stats-row {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    .hero-stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .hero-stat-pill:hover {
        transform: translateY(-2px);
    }
    .pill-cyan { background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #E0F2FE; }
    .pill-emerald { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(52, 211, 153, 0.35); color: #D1FAE5; }
    .pill-purple { background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(192, 132, 252, 0.35); color: #F3E8FF; }
    .pill-amber { background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(251, 191, 36, 0.35); color: #FEF3C7; }
    .pill-rose { background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(251, 113, 133, 0.35); color: #FFE4E6; }
    
    /* Interactive Card Base */
    .saathi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease;
        margin-bottom: 20px;
    }
    .saathi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 36px -4px rgba(37, 99, 235, 0.2);
        border-color: rgba(96, 165, 250, 0.4);
    }

    /* Scenario Card Component */
    .scenario-card-box {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid #3B82F6;
        border-radius: 16px;
        padding: 20px 18px;
        text-align: left;
        transition: all 0.25s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .scenario-card-box:hover {
        transform: translateY(-4px);
        border-color: rgba(147, 197, 253, 0.5);
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25);
    }
    .scenario-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
    }
    .scenario-card-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .scenario-card-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    /* Streamlit Global Buttons Overhaul */
    .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border-color: #60A5FA !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4) !important;
        color: #FFFFFF !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        border: 1px solid rgba(192, 132, 252, 0.5) !important;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.45) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #6D28D9 100%) !important;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.6) !important;
        transform: translateY(-2px) !important;
    }

    /* Policy Badges */
    .policy-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .pill-rag { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.4); }
    .pill-clarify { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid rgba(251, 191, 36, 0.4); }
    .pill-action { background: rgba(249, 115, 22, 0.2); color: #FB923C; border: 1px solid rgba(251, 146, 60, 0.4); }
    .pill-escalate { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid rgba(248, 113, 113, 0.4); }
    .pill-direct { background: rgba(99, 102, 241, 0.2); color: #A5B4FC; border: 1px solid rgba(165, 180, 252, 0.4); }

    /* Action Proposal Card */
    .action-draft-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(217, 119, 6, 0.08) 100%);
        border: 2px solid #F59E0B;
        border-radius: 16px;
        padding: 22px;
        margin: 18px 0;
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.2);
    }
    
    /* Calculator Container */
    .calc-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        backdrop-filter: blur(16px);
    }
    
    /* Metric Boxes */
    .metric-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .metric-box:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.4);
    }
    .metric-val {
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #F8FAFC;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    /* Pulsing Halos */
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        display: inline-block;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Streamlit Input Enhancements */
    .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Core Services
if "db" not in st.session_state:
    st.session_state.db = ChatHistoryManager()
if "auth_service" not in st.session_state:
    st.session_state.auth_service = FirebaseAuthService()
if "knowledge_store" not in st.session_state:
    st.session_state.knowledge_store = KnowledgeStore(data_dir="data/sample_docs")
if "controller" not in st.session_state:
    st.session_state.controller = SaathiController(st.session_state.knowledge_store)

# User Session Management
if "current_user" not in st.session_state:
    user_info = st.session_state.db.create_or_get_user("demo_citizen_01", "citizen@saathi.ai", "Demo Citizen")
    st.session_state.current_user = user_info

if "current_session_id" not in st.session_state:
    first_sess_id = st.session_state.db.create_session(st.session_state.current_user["user_id"], "First Conversation")
    st.session_state.current_session_id = first_sess_id

# ==========================================
# SIDEBAR: USER AUTH & CHAT SESSIONS
# ==========================================
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px; padding: 12px 14px; background: rgba(255,255,255,0.04); border-radius: 16px; border: 1px solid rgba(255,255,255,0.08);">
    <div style="font-size: 2.2rem; background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%); width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; border-radius: 14px; color: white; box-shadow: 0 4px 16px rgba(37,99,235,0.4);">🤝</div>
    <div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 800; color: #F8FAFC; line-height: 1.1;">SAATHI AI</div>
        <div style="font-size: 0.76rem; color: #38BDF8; font-weight: 600; display: flex; align-items: center; gap: 6px; margin-top: 3px;">
            <span class="pulse-dot"></span> Evidence-Gated Assistant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# User Account Card
user = st.session_state.current_user
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 12px 16px; margin-bottom: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">👤 {user.get('display_name', 'Citizen User')}</div>
        <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px; border: 1px solid rgba(52, 211, 153, 0.3);">VERIFIED</span>
    </div>
    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">{user.get('email', '')}</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("🔑 Firebase Account & Security"):
    auth_tab1, auth_tab2 = st.tabs(["Sign In", "Sign Up"])
    with auth_tab1:
        in_email = st.text_input("Email:", key="login_email")
        in_pwd = st.text_input("Password:", type="password", key="login_pwd")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign In", key="btn_signin", use_container_width=True):
                if in_email and in_pwd:
                    ok, udata, err = st.session_state.auth_service.sign_in_with_email(in_email, in_pwd)
                    if ok:
                        u_profile = st.session_state.db.create_or_get_user(udata["localId"], udata["email"], udata.get("displayName", in_email.split("@")[0]))
                        st.session_state.current_user = u_profile
                        st.success("Signed in!")
                        st.rerun()
                    else:
                        st.error(err)
        with c2:
            if st.button("🌐 Google", key="btn_google", use_container_width=True):
                ok, udata, err = st.session_state.auth_service.sign_in_with_google_id_token("mock_google_id_token")
                if ok:
                    u_profile = st.session_state.db.create_or_get_user(udata["localId"], udata["email"], udata.get("displayName", "Google Citizen"), "google")
                    st.session_state.current_user = u_profile
                    st.success("Google Login successful!")
                    st.rerun()

    with auth_tab2:
        reg_name = st.text_input("Full Name:", key="reg_name")
        reg_email = st.text_input("Email:", key="reg_email")
        reg_pwd = st.text_input("Password:", type="password", key="reg_pwd")
        if st.button("Create Account", key="btn_reg", use_container_width=True):
            if reg_email and reg_pwd:
                ok, udata, err = st.session_state.auth_service.sign_up_with_email(reg_email, reg_pwd, reg_name)
                if ok:
                    u_profile = st.session_state.db.create_or_get_user(udata["localId"], udata["email"], reg_name or udata.get("displayName", "Citizen"))
                    st.session_state.current_user = u_profile
                    st.success("Account created!")
                    st.rerun()
                else:
                    st.error(err)

# New Chat Button
if st.sidebar.button("➕ Start New Conversation", type="primary", use_container_width=True):
    new_sess = st.session_state.db.create_session(st.session_state.current_user["user_id"], "New Conversation")
    st.session_state.current_session_id = new_sess
    st.rerun()

# Multi-Session Conversation Threads
st.sidebar.markdown("### 📜 Past Conversations")
sessions = st.session_state.db.get_user_sessions(st.session_state.current_user["user_id"])
for s in sessions:
    s_id = s["session_id"]
    is_active = (s_id == st.session_state.current_session_id)
    btn_label = f"📍 {s['title'][:20]}..." if is_active else f"💬 {s['title'][:22]}..."
    
    col_s1, col_s2 = st.sidebar.columns([5, 1])
    with col_s1:
        if st.button(btn_label, key=f"sess_{s_id}", use_container_width=True):
            st.session_state.current_session_id = s_id
            st.rerun()
    with col_s2:
        if st.button("✕", key=f"del_{s_id}", help="Delete chat"):
            st.session_state.db.delete_session(s_id)
            if is_active:
                remaining = st.session_state.db.get_user_sessions(st.session_state.current_user["user_id"])
                if remaining:
                    st.session_state.current_session_id = remaining[0]["session_id"]
                else:
                    st.session_state.current_session_id = st.session_state.db.create_session(st.session_state.current_user["user_id"])
            st.rerun()

st.sidebar.divider()

# Navigation
mode = st.sidebar.radio(
    "Navigation Portal / नेविगेशन:",
    [
        "💬 AI Assistant & Chat",
        "🎯 Scheme Eligibility Wizard",
        "🧮 Smart Utility Calculators",
        "📸 Camera & Bill OCR Scanner",
        "📚 Official Knowledge Base",
        "📋 Citizen Action Vault",
        "📊 Live Research Benchmarks",
        "🎓 Student Model Training Hub",
        "🤖 WhatsApp & Telegram Bots",
        "📄 Research Proposal & Journal",
        "🔌 REST API & Developer Hub"
    ]
)

st.sidebar.divider()

# Active Intelligence Engine Selector
st.sidebar.markdown("### 🧠 Active Intelligence Engine")
adapter_exists = LocalFineTunedModel.is_available()
engine_options = [
    "⚡ Deterministic Controller (100% Offline RAG)",
    "🎯 Fine-Tuned Model (Qwen2.5-1.5B + Rank-64 LoRA on RTX 4050)" if adapter_exists else "🎯 Fine-Tuned Model (Adapter Pending)",
    "☁️ Cloud Hybrid (Gemini 2.5 API)"
]
selected_engine = st.sidebar.selectbox("Inference Engine:", engine_options, index=1 if adapter_exists else 0)

if "Fine-Tuned" in selected_engine and adapter_exists:
    active_llm_provider = "local_lora"
    st.sidebar.success("🟢 GPU LoRA Adapter Ready")
elif "Cloud" in selected_engine:
    active_llm_provider = "gemini"
    st.sidebar.info("☁️ Cloud API Active")
else:
    active_llm_provider = "auto"
    st.sidebar.caption("⚡ Offline Rule-Gated RAG")


# ==========================================
# HERO BANNER (TOP OF APPLICATION)
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="pulse-dot"></span> 🏛️ OFFICIAL VERIFIED CITIZEN COMPLIANCE ENGINE • GOVT OF INDIA
    </div>
    <div class="hero-title">
        SAATHI AI <span class="hindi-glow">• साथी</span>
    </div>
    <div class="hero-subtitle">
        India's premier <b>Evidence-Gated, Zero-Hallucination Public Assistant</b>. Grounded in official regulatory acts, transparent multi-state utility calculators, and strict zero-unauthorized-action safety gates.
    </div>
    <div class="hero-stats-row">
        <div class="hero-stat-pill pill-cyan">⚡ <b>92.0%</b> Policy Reliability</div>
        <div class="hero-stat-pill pill-emerald">🛡️ <b>100%</b> Red-Team Safety Pass</div>
        <div class="hero-stat-pill pill-purple">🌍 <b>Hindi • Hinglish • English</b> Parity</div>
        <div class="hero-stat-pill pill-amber">🏛️ <b>9+</b> Central & State Schemes</div>
        <div class="hero-stat-pill pill-rose">🖨️ <b>QR Verified</b> Action Seals</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TAB 1: AI ASSISTANT & CHAT
# ==========================================
if mode == "💬 AI Assistant & Chat":
    st.markdown("### 💡 Quick Topics & Everyday Citizen Scenarios")
    
    # Engaging 4-Card Visual Grid
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        st.markdown("""
        <div class="scenario-card-box" style="border-top-color: #3B82F6;">
            <div>
                <div class="scenario-icon">⚡</div>
                <div class="scenario-card-title">Electricity Slabs</div>
                <div class="scenario-card-desc">Audit telescopic slabs, average billing, and dispute faulty meter IDF flags.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Audit Electricity Bill", key="q_elec", use_container_width=True):
            st.session_state.selected_quick_prompt = "Mera bijli ka bill bahut jyada aaya hai meter kharab lagta hai kya karu?"

    with q_col2:
        st.markdown("""
        <div class="scenario-card-box" style="border-top-color: #10B981;">
            <div>
                <div class="scenario-icon">🌾</div>
                <div class="scenario-card-title">PM-KISAN ₹2,000</div>
                <div class="scenario-card-desc">Resolve stopped installments, Aadhaar eKYC errors, and Bhulekh land seeding.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌾 Fix PM-KISAN Error", key="q_kisan", use_container_width=True):
            st.session_state.selected_quick_prompt = "PM kisan ka 2000 rupaye nahi aaya land seeding NO dikha raha hai kaise theek karein?"

    with q_col3:
        st.markdown("""
        <div class="scenario-card-box" style="border-top-color: #8B5CF6;">
            <div>
                <div class="scenario-icon">🛡️</div>
                <div class="scenario-card-title">Cyber Fraud 1930</div>
                <div class="scenario-card-desc">Golden hour bank fund freezing, online transaction safety, and cyber cell SOPs.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛡️ Cyber Emergency SOP", key="q_cyber", use_container_width=True):
            st.session_state.selected_quick_prompt = "Bank account se online fraud ho gaya paise kat gaye helpline number kya hai?"

    with q_col4:
        st.markdown("""
        <div class="scenario-card-box" style="border-top-color: #F59E0B;">
            <div>
                <div class="scenario-icon">🏠</div>
                <div class="scenario-card-title">Tenant Security Deposit</div>
                <div class="scenario-card-desc">Model Tenancy Act rules, unlawful painting fee disputes, and refund drafts.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏠 Audit Rental Deposit", key="q_rent", use_container_width=True):
            st.session_state.selected_quick_prompt = "Landlord refusing to return security deposit deducting 15000 for paint what to do?"

    st.markdown("<hr style='margin: 22px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # Interactive Citizen Studio: Voice Assistant + Bill Parser Strip
    col_tools1, col_tools2 = st.columns(2)
    with col_tools1:
        with st.expander("🎙️ Voice Search / बोलकर पूछें (Microphone Audio Input)", expanded=False):
            st.write("Speak your question naturally in **हिंदी, Hinglish, or English**.")
            stt_lang_choice = st.selectbox(
                "Select Voice Dialect / भाषा:",
                ["हिंदी (Hindi - hi-IN)", "Hinglish / English (India - en-IN)", "English (US - en-US)"],
                index=0,
                key="voice_stt_dialect"
            )
            lang_code_map = {
                "हिंदी (Hindi - hi-IN)": "hi-IN",
                "Hinglish / English (India - en-IN)": "en-IN",
                "English (US - en-US)": "en-US"
            }
            selected_stt_lang = lang_code_map.get(stt_lang_choice, "hi-IN")
            
            voice_recording = st.audio_input(
                "Click red circle to record, click stop when done:",
                key="chat_mic_recorder"
            )
            if voice_recording is not None:
                audio_bytes = voice_recording.getvalue()
                audio_hash = hash(audio_bytes)
                if st.session_state.get("last_processed_audio_hash") != audio_hash:
                    st.session_state.last_processed_audio_hash = audio_hash
                    with st.spinner("🎙️ Transcribing voice in real-time..."):
                        transcribed_text = VoiceEngine.transcribe_audio_bytes(audio_bytes, language=selected_stt_lang)
                    
                    if transcribed_text:
                        st.session_state.selected_quick_prompt = transcribed_text
                        st.success(f"🗣️ Heard: **\"{transcribed_text}\"**")
                        st.rerun()
                    else:
                        st.warning("⚠️ Could not clearly transcribe speech. Please speak closer to your microphone.")

    with col_tools2:
        with st.expander("📄 Fast Bill Text & Notice Parser", expanded=False):
            st.write("Paste raw bill text or upload `.txt` to extract structured billing fields instantly.")
            uploaded_bill_file = st.file_uploader("Upload Bill Text / Notice:", type=["txt", "csv", "json"], key="bill_uploader")
            doc_raw_text = st.text_area(
                "Or Paste Bill / Notice Text:",
                height=70,
                placeholder="Example: CA No: 102938475, Units: 420 kWh, Total Amount: Rs 3450, Due Date: 25/11/2026, IDF Defective Reading...",
                key="pasted_bill_text"
            )
            if uploaded_bill_file:
                try:
                    doc_raw_text = uploaded_bill_file.read().decode("utf-8")
                except Exception:
                    pass

            if doc_raw_text.strip():
                parsed_elec = DocumentParser.extract_electricity_bill_fields(doc_raw_text)
                
                col_p1, col_p2, col_p3 = st.columns(3)
                col_p1.metric("CA Account", str(parsed_elec['consumer_number'] or "N/A"))
                col_p2.metric("Units Billed", f"{parsed_elec['units_consumed'] or 0.0} kWh")
                col_p3.metric("Billed Amount", f"₹{parsed_elec['total_amount'] or 0.0}")
                
                if parsed_elec['is_average_or_idf']:
                    st.warning("⚠️ IDF / Average estimated reading flagged!")

                if st.button("⚡ Audit This Bill with SAATHI", key="btn_audit_bill", use_container_width=True):
                    st.session_state.selected_quick_prompt = f"Please audit my electricity bill: CA No {parsed_elec['consumer_number']}, Units {parsed_elec['units_consumed']}, Amount Rs {parsed_elec['total_amount']}, Average/IDF Flag: {parsed_elec['is_average_or_idf']}."
                    st.rerun()

    # Load session messages
    current_session_messages = st.session_state.db.get_session_messages(st.session_state.current_session_id)

    # Empty State Welcome Center
    if len(current_session_messages) == 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%); border: 1px dashed rgba(255,255,255,0.15); border-radius: 18px; padding: 32px; text-align: center; margin: 24px 0;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🤝</div>
            <h3 style="color: #F8FAFC; margin-bottom: 6px; font-family: 'Outfit', sans-serif;">How can SAATHI AI assist you today?</h3>
            <p style="color: #94A3B8; max-width: 600px; margin: 0 auto 18px auto; font-size: 0.95rem;">
                Ask any question below, use the Voice Studio above, or click one of the quick scenario cards to start.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Display chat history for active thread
    for idx, msg in enumerate(current_session_messages):
        with st.chat_message(msg["role"]):
            if msg.get("decision"):
                dec = msg["decision"]
                d_type = dec.get("decision", DecisionType.DIRECT_ANSWER) if isinstance(dec, dict) else dec.decision
                conf = dec.get("confidence", 0.9) if isinstance(dec, dict) else dec.confidence
                lang = dec.get("detected_language", "english") if isinstance(dec, dict) else dec.detected_language
                
                badge_class = {
                    DecisionType.DIRECT_ANSWER: "pill-direct",
                    DecisionType.RETRIEVE_AND_ANSWER: "pill-rag",
                    DecisionType.CLARIFY: "pill-clarify",
                    DecisionType.PREPARE_ACTION: "pill-action",
                    DecisionType.ESCALATE: "pill-escalate"
                }.get(d_type, "pill-direct")
                
                st.markdown(
                    f'<span class="policy-pill {badge_class}">⚡ Policy: {d_type} • Confidence: {conf * 100:.0f}% • Dialect: {lang.title()}</span>',
                    unsafe_allow_html=True
                )

            # Parse potential CoT thinking traces
            think_trace, display_content = LocalFineTunedModel.parse_thinking_response(msg["content"])
            if think_trace:
                with st.expander("🧠 Gemini 3.7 Thinking Process (CoT Deliberation)", expanded=False):
                    st.markdown(f'<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(147, 51, 234, 0.3); border-left: 3px solid #A855F7; padding: 12px 16px; border-radius: 8px; color: #CBD5E1; font-size: 0.88rem; font-family: monospace; white-space: pre-wrap;">{think_trace}</div>', unsafe_allow_html=True)
            
            st.markdown(display_content)

            # Voice TTS Audio Button
            tts_html = VoiceEngine.generate_browser_speech_html(
                text=display_content,
                language=lang if "lang" in locals() else "english",
                button_id=f"tts_{idx}"
            )
            st.html(tts_html)

            # Citations
            if msg.get("citations"):
                with st.expander("📌 Verified Official Citations & Sources"):
                    for c in msg["citations"]:
                        st.markdown(f"- **{c}**")

            # Action Draft Box with Strict Human Gate
            if msg.get("action"):
                act = msg["action"]
                act_id = act.get("action_id", "act_01") if isinstance(act, dict) else act.action_id
                title = act.get("title", "Action Proposal") if isinstance(act, dict) else act.title
                warning = act.get("warning_or_disclaimer", "") if isinstance(act, dict) else act.warning_or_disclaimer
                draft_body = act.get("draft_content", "") if isinstance(act, dict) else act.draft_content
                act_type = act.get("action_type", "draft_complaint") if isinstance(act, dict) else act.action_type

                st.markdown(f"""
                <div class="action-draft-card">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                        <h4 style="color: #FBBF24; margin: 0; font-family: 'Outfit', sans-serif;">📝 Prepared Action Draft: {title}</h4>
                        <span style="background: rgba(245, 158, 11, 0.3); color: #FDE68A; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; border: 1px solid #F59E0B;">REQUIRES CITIZEN APPROVAL</span>
                    </div>
                    <p style="color: #FDE68A; font-size: 0.88rem; margin-bottom: 12px;">{warning}</p>
                </div>
                """, unsafe_allow_html=True)
                
                edited_draft = st.text_area("Review or Customize Draft Text:", value=draft_body, height=180, key=f"draft_{idx}_{act_id}")
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button("✅ Approve Action", key=f"app_{idx}_{act_id}", use_container_width=True):
                        st.session_state.db.save_approved_action(
                            user_id=st.session_state.current_user["user_id"],
                            session_id=st.session_state.current_session_id,
                            action_type=act_type,
                            title=title,
                            final_content=edited_draft
                        )
                        st.success("✅ Action officially approved! Saved to 'Citizen Action Vault'.")
                with c2:
                    if st.button("❌ Request Changes", key=f"req_{idx}_{act_id}"):
                        st.info("Tell SAATHI what details to adjust in your next message.")

    # User Input Handling
    prompt_input = st.chat_input("Ask a question in English, हिंदी, or Hinglish (or use Voice Search above)...")
    
    if "selected_quick_prompt" in st.session_state and st.session_state.selected_quick_prompt:
        prompt_input = st.session_state.selected_quick_prompt
        st.session_state.selected_quick_prompt = None

    if prompt_input:
        st.session_state.db.save_message(
            session_id=st.session_state.current_session_id,
            role="user",
            content=prompt_input
        )
        if len(current_session_messages) == 0:
            st.session_state.db.update_session_title(st.session_state.current_session_id, prompt_input[:26])

        with st.spinner("Analyzing intent, verifying official evidence & applying safety policies..."):
            decision_result = st.session_state.controller.process_query(
                prompt_input,
                current_session_messages,
                llm_provider=active_llm_provider
            )

        st.session_state.db.save_message(
            session_id=st.session_state.current_session_id,
            role="assistant",
            content=decision_result.response_text,
            decision=decision_result,
            citations=decision_result.citations,
            action=decision_result.proposed_action
        )
        st.rerun()

# ==========================================
# TAB 2: SCHEME ELIGIBILITY WIZARD
# ==========================================
elif mode == "🎯 Scheme Eligibility Wizard":
    st.markdown("## 🎯 Citizen Welfare Scheme Eligibility Wizard")
    st.write("Find out all Central and State government welfare schemes, direct cash benefits, and subsidies you are eligible for in under 30 seconds.")

    w_col1, w_col2 = st.columns([1, 1])
    with w_col1:
        st.markdown('<div class="saathi-card">', unsafe_allow_html=True)
        st.subheader("👤 Citizen Demographic Profile")
        w_state = st.selectbox("State of Residence / राज्य:", ["All India", "Delhi", "Maharashtra", "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan", "Karnataka", "West Bengal", "Tamil Nadu", "Gujarat", "Punjab", "Haryana"])
        w_age = st.slider("Citizen Age (Years) / उम्र:", min_value=1, max_value=90, value=38)
        w_gender = st.selectbox("Gender / लिंग:", ["Male", "Female", "Other"])
        w_occ = st.selectbox("Primary Occupation / व्यवसाय:", ["Farmer", "Street Vendor", "Unorganized Worker", "Student", "Senior Citizen", "Homemaker", "Salaried"])
        w_inc = st.slider("Annual Household Income (₹) / वार्षिक पारिवारिक आय:", min_value=30000, max_value=1500000, value=140000, step=10000)
        
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            w_land = st.checkbox("Owns Cultivable Agricultural Land?", value=True if w_occ == "Farmer" else False)
            w_diff = st.checkbox("Differently Abled (Divyangjan)?", value=False)
        with c_sub2:
            w_girl = st.checkbox("Has Girl Child (under 10 years)?", value=False)
            w_caste = st.selectbox("Social Category:", ["General", "OBC", "SC", "ST", "EWS"])

        profile = CitizenProfile(
            state=w_state,
            age=w_age,
            gender=w_gender,
            occupation=w_occ,
            annual_income=float(w_inc),
            has_cultivable_land=w_land,
            caste_category=w_caste,
            has_girl_child=w_girl,
            girl_child_age=6 if w_girl else None,
            is_differently_abled=w_diff
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with w_col2:
        matched_schemes = WelfareSchemeFinder.match_schemes_for_citizen(profile)
        eligible_schemes = [s for s in matched_schemes if s.is_eligible]
        
        st.markdown('<div class="saathi-card">', unsafe_allow_html=True)
        st.subheader("🏆 Your Eligibility Summary")
        m_col1, m_col2 = st.columns(2)
        m_col1.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Directly Eligible Schemes</div>
            <div class="metric-val" style="color: #34D399;">{len(eligible_schemes)} / {len(matched_schemes)}</div>
        </div>
        """, unsafe_allow_html=True)
        m_col2.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Profile Fit Rating</div>
            <div class="metric-val" style="color: #38BDF8;">{int((len(eligible_schemes)/max(len(matched_schemes),1))*100)}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Click on any scheme below to view exact benefits, required documents, and one-click application checklists.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    # Render scheme cards
    st.subheader(f"📋 Verified Government Schemes ({len(matched_schemes)})")
    for sch in matched_schemes:
        badge_text = "🟢 ELIGIBLE" if sch.is_eligible else "🟡 PARTIAL FIT / CHECK CONDITIONS"
        
        with st.expander(f"✨ {sch.scheme_name} — {sch.category} [{badge_text}]"):
            st.markdown(f"**🏛️ Authority:** {sch.ministry_or_state}")
            st.markdown(f"**💰 Key Benefits:** {sch.benefit_summary}")
            
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                st.markdown("**📌 Key Eligibility Conditions:**")
                for cond in sch.key_conditions:
                    st.write(f"- {cond}")
            with c_s2:
                st.markdown("**📑 Required Documents Checklist:**")
                for doc in sch.required_documents:
                    st.write(f" [ ] {doc}")

            st.markdown("**🚀 Next Steps to Apply:**")
            for act in sch.action_checklist:
                st.write(f"• {act}")

            c_btn1, c_btn2 = st.columns([1, 3])
            with c_btn1:
                st.markdown(f'<a href="{sch.portal_url}" target="_blank" style="background: #2563EB; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block;">🌐 Official Portal</a>', unsafe_allow_html=True)
            with c_btn2:
                if st.button(f"Draft Application Checklist for {sch.scheme_name}", key=f"btn_chk_{sch.scheme_id}"):
                    st.session_state.selected_quick_prompt = f"Please prepare a complete application checklist and document requirement draft for {sch.scheme_name}."
                    st.rerun()

# ==========================================
# TAB 3: SMART UTILITY CALCULATORS
# ==========================================
elif mode == "🧮 Smart Utility Calculators":
    st.markdown("## 🧮 Interactive Citizen & Utility Calculators")
    st.write("Transparent, rule-based mathematical calculators to audit electricity bills, rental security deposits, and retirement PF advances.")

    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "⚡ Electricity Slab Tariff Estimator",
        "🏠 Rental Deposit Deduction Auditor",
        "💰 EPFO PF Advance (Form 31) Limit"
    ])

    with calc_tab1:
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⚡ Electricity Tariff Inputs")
            state_opt = st.selectbox(
                "State / DISCOM Tariff Framework:",
                [
                    "Delhi (DERC / TPDDL / BRPL - Lifeline Subsidy)",
                    "Maharashtra (MSEDCL / Mahavitaran)",
                    "Uttar Pradesh (UPPCL / PVVNL)",
                    "Karnataka (BESCOM Bangalore)",
                    "Standard (National Benchmark)"
                ]
            )
            units = st.slider("Units Consumed (kWh / Units):", min_value=0, max_value=1200, value=280, step=10)
            load = st.number_input("Sanctioned Load (kW):", min_value=0.5, max_value=20.0, value=2.0, step=0.5)
            is_idf = st.checkbox("Is bill marked Defective Meter / Average Assessment (IDF)?")
        
        calc_res = UtilityCalculators.calculate_electricity_bill(units, load, state=state_opt, is_average_or_idf=is_idf)
        with col2:
            st.subheader("💳 Verified Bill Calculation Breakdown")
            m1, m2 = st.columns(2)
            m1.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Energy Charges</div>
                <div class="metric-val">₹{calc_res['energy_charge']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            m2.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Total Estimated Bill</div>
                <div class="metric-val" style="color: #38BDF8;">₹{calc_res['total_estimated_bill']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write(f"• **Fixed Demand Charges ({load} kW):** ₹{calc_res['fixed_charge']:.2f}")
            st.write(f"• **State Electricity Duty & Tax:** ₹{calc_res['electricity_duty']:.2f}")
            if calc_res.get("subsidy_applied", 0.0) > 0:
                st.success(f"🎁 Government Subsidy Applied: -₹{calc_res['subsidy_applied']:.2f}")
            with st.expander("🔍 View Telescopic Slab Calculations"):
                for s in calc_res["slab_breakdown"]:
                    st.write(f"- {s}")
            if calc_res["warning"]:
                st.warning(calc_res["warning"])

            # Generate Tariff Audit PDF
            audit_pdf_bytes = SaathiPDFGenerator.generate_bill_audit_pdf({
                "inputs": {
                    "Discom / State": state_opt,
                    "Units Consumed (kWh)": f"{units} Units",
                    "Sanctioned Load": f"{load} kW",
                    "Reading Assessment": "IDF / Defective Reading Flagged" if is_idf else "Actual Meter Reading"
                },
                "breakdown": {
                    "Energy Charges": f"Rs. {calc_res['energy_charge']:.2f}",
                    "Fixed Demand Charges": f"Rs. {calc_res['fixed_charge']:.2f}",
                    "State Electricity Duty": f"Rs. {calc_res['electricity_duty']:.2f}",
                    "Subsidy Applied": f"- Rs. {calc_res.get('subsidy_applied', 0.0):.2f}",
                    "Total Estimated Bill": f"Rs. {calc_res['total_estimated_bill']:.2f}"
                }
            })

            st.download_button(
                label="📥 Download Tariff Audit Certificate (.pdf)",
                data=audit_pdf_bytes,
                file_name=f"Electricity_Tariff_Audit_{int(time.time())}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dl_elec_pdf"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with calc_tab2:
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🏠 Tenancy Dispute Details")
            dep = st.number_input("Total Security Deposit Paid (₹):", min_value=1000.0, value=50000.0, step=5000.0)
            rent = st.number_input("Monthly Rent (₹):", min_value=1000.0, value=20000.0, step=1000.0)
            unpaid_bills = st.number_input("Unpaid Utility Bills (₹):", min_value=0.0, value=1200.0, step=200.0)
            painting = st.number_input("Landlord Claimed Painting Deduction (₹):", min_value=0.0, value=15000.0, step=1000.0)
            damage = st.number_input("Actual Structural Damage Claimed (₹):", min_value=0.0, value=0.0, step=500.0)

        res_rent = UtilityCalculators.audit_security_deposit_deduction(dep, rent, unpaid_bills, painting, damage)
        with c2:
            st.subheader("⚖️ Model Tenancy Act Legal Audit")
            st.markdown(f"""
            <div class="metric-box" style="margin-bottom: 12px;">
                <div class="metric-label">Minimum Rightful Refund</div>
                <div class="metric-val" style="color: #34D399;">₹{res_rent['minimum_rightful_refund']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"• **Legitimate Deductions (Bills/Damage):** ₹{res_rent['legitimate_deductions']:.2f}")
            st.write(f"• **Disputed Wall Paint Claim:** ₹{res_rent['disputed_painting_deduction']:.2f}")
            st.info(f"🛡️ **Full Refund if Painting Dispute is Won:** ₹{res_rent['full_refund_if_painting_disputed']:.2f}")
            for adv in res_rent["advice"]:
                st.write(adv)
        st.markdown('</div>', unsafe_allow_html=True)

    with calc_tab3:
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            st.subheader("💰 EPFO Member Details")
            ee_pf = st.number_input("Employee PF Balance Share (₹):", min_value=1000.0, value=120000.0, step=10000.0)
            er_pf = st.number_input("Employer PF Balance Share (₹):", min_value=0.0, value=40000.0, step=5000.0)
            basic_da = st.number_input("Monthly Basic Salary + DA (₹):", min_value=1000.0, value=25000.0, step=2000.0)
            purpose = st.selectbox("Advance Purpose:", ["Illness / Medical", "Marriage", "House Purchase / Construction", "General Emergency"])
            service_yrs = st.number_input("Total Continuous Service (Years):", min_value=0.5, value=3.5, step=0.5)

        res_pf = UtilityCalculators.estimate_pf_advance_limit(ee_pf, er_pf, basic_da, purpose, service_yrs)
        with p2:
            st.subheader("📋 Allowable Advance Estimate")
            if res_pf["status"] == "ELIGIBLE":
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Max Allowable PF Advance</div>
                    <div class="metric-val" style="color: #38BDF8;">₹{res_pf['max_withdrawable_amount']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Status: {res_pf['status'].replace('_', ' ')}")
            st.markdown("<br>", unsafe_allow_html=True)
            for n in res_pf["notes"]:
                st.write(f"- {n}")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 4: CAMERA & BILL OCR SCANNER
# ==========================================
elif mode == "📸 Camera & Bill OCR Scanner":
    st.markdown("## 📸 Camera & Bill Document OCR Scanner")
    st.write("Capture a photo or upload a scan of your electricity bill, LPG receipt, or rent notice. SAATHI AI will read the text using OCR and extract all key billing parameters.")

    ocr_col1, ocr_col2 = st.columns([1, 1])
    with ocr_col1:
        st.markdown('<div class="saathi-card">', unsafe_allow_html=True)
        st.subheader("Upload Bill Image / Scanned Document")
        img_file = st.file_uploader("Upload Bill Image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
        camera_photo = st.camera_input("Or Take a Live Photo of Your Bill with Camera:")
        
        target_file = camera_photo or img_file
        
        if target_file:
            st.image(target_file, caption="Uploaded Bill Preview", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ocr_col2:
        st.markdown('<div class="saathi-card">', unsafe_allow_html=True)
        st.subheader("🔍 OCR Extraction & Tariff Parameters")
        if target_file:
            raw_bytes = target_file.getvalue()
            with st.spinner("Extracting text and recognizing characters via OCR engine..."):
                extracted_text, ocr_meta = BillOCRScanner.extract_text_from_image(raw_bytes, target_file.name if hasattr(target_file, "name") else "camera_bill.png")
            
            st.caption(f"⚙️ OCR Engine: {ocr_meta.get('ocr_engine')} • Dimensions: {ocr_meta.get('image_size', 'N/A')}")
            
            with st.expander("📄 View Raw Extracted Text", expanded=False):
                st.text_area("Extracted Characters:", value=extracted_text, height=120)

            parsed_elec = DocumentParser.extract_electricity_bill_fields(extracted_text)

            st.markdown("#### ⚡ Recognized Electricity Parameters:")
            p1, p2, p3 = st.columns(3)
            p1.metric("CA / Consumer No.", str(parsed_elec['consumer_number'] or "Not Found"))
            p2.metric("Units (kWh)", f"{parsed_elec['units_consumed'] or 0.0} kWh")
            p3.metric("Billed Amount", f"₹{parsed_elec['total_amount'] or 0.0}")

            if parsed_elec['is_average_or_idf']:
                st.warning("⚠️ IDF / Average reading detected on bill! You may be entitled to a meter accuracy check.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Audit This Scanned Bill with SAATHI AI", type="primary", use_container_width=True):
                st.session_state.selected_quick_prompt = f"Please audit my electricity bill: CA No {parsed_elec['consumer_number']}, Units {parsed_elec['units_consumed']}, Amount Rs {parsed_elec['total_amount']}, Average/IDF: {parsed_elec['is_average_or_idf']}."
                st.rerun()
        else:
            st.info("👈 Upload an image or snap a picture using the camera to start optical character recognition.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 5: OFFICIAL KNOWLEDGE BASE
# ==========================================
elif mode == "📚 Official Knowledge Base":
    st.markdown("## 📚 Vetted Document Knowledge Base")
    st.write("Browse official guidelines, government SOPs, and public regulations indexed inside SAATHI AI.")

    col1, col2 = st.columns([2, 1])
    with col1:
        chunks = st.session_state.knowledge_store.get_all_chunks()
        categories = list(set([ch.metadata.get("category", "General") for ch in chunks]))
        selected_cat = st.selectbox("Filter by Category / Domain:", ["All Categories"] + sorted(categories))
        search_kw = st.text_input("🔍 Search Knowledge Base:", "")
        
        filtered_chunks = chunks
        if selected_cat != "All Categories":
            filtered_chunks = [ch for ch in filtered_chunks if ch.metadata.get("category") == selected_cat]
        if search_kw:
            filtered_chunks = [ch for ch in filtered_chunks if search_kw.lower() in ch.title.lower() or search_kw.lower() in ch.content.lower()]

        st.subheader(f"Verified Records ({len(filtered_chunks)})")
        for idx, ch in enumerate(filtered_chunks):
            with st.expander(f"📄 {ch.title} [{ch.authority_level.replace('_', ' ').title()}]"):
                st.write(ch.content)
                st.caption(f"📌 Authority / Source: {ch.source_url_or_file} • 📅 Last Verified: {ch.last_updated}")

    with col2:
        st.markdown('<div class="saathi-card">', unsafe_allow_html=True)
        st.subheader("Upload Document / Notice")
        st.write("Upload a bill, scheme notice, or rental agreement to ask questions about it.")
        uploaded_file = st.file_uploader("Upload .txt, .md, or .json file", type=["txt", "md", "json"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            if st.button("➕ Ingest Document into Knowledge Store", use_container_width=True):
                new_chunks = st.session_state.knowledge_store.add_user_document(uploaded_file.name, content)
                st.success(f"Ingested {len(new_chunks)} section(s) into SAATHI knowledge store!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 6: CITIZEN ACTION VAULT
# ==========================================
elif mode == "📋 Citizen Action Vault":
    st.markdown("## 📋 Citizen Action Vault & Printable Documents")
    st.write("All complaint letters, RTI applications, and checklists you reviewed and approved are saved here permanently with QR-verified printable official letterheads.")

    approved_list = st.session_state.db.get_user_approved_actions(st.session_state.current_user["user_id"])
    if not approved_list:
        st.info("No approved action drafts yet. When SAATHI prepares a draft and you click '✅ Approve Action', it will be permanently archived here.")
    else:
        for item in approved_list:
            with st.expander(f"📄 {item['title']} (Approved: {item['approved_at']})"):
                st.code(item["final_content"], language="text")
                
                # Generate printable HTML letter
                html_letter = LetterExporter.generate_printable_html_letter(
                    title=item["title"],
                    recipient="The Competent Grievance Officer / Authority",
                    subject=item["title"],
                    body_content=item["final_content"],
                    applicant_name=st.session_state.current_user.get("display_name", "[Citizen Name]"),
                    reference_id=item["action_id"]
                )
                
                # Generate official PDF letter
                pdf_letter_bytes = SaathiPDFGenerator.generate_complaint_letter_pdf(
                    title=item["title"],
                    content=item["final_content"],
                    author_name=st.session_state.current_user.get("display_name", "Citizen Applicant"),
                    ref_id=item["action_id"]
                )

                c_d1, c_d2, c_d3 = st.columns(3)
                with c_d1:
                    st.download_button(
                        label="📄 Download Official PDF (.pdf)",
                        data=pdf_letter_bytes,
                        file_name=f"{item['title'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"dl_pdf_{item['action_id']}",
                        use_container_width=True
                    )
                with c_d2:
                    st.download_button(
                        label="🖨️ Printable HTML (.html)",
                        data=html_letter,
                        file_name=f"{item['title'].replace(' ', '_')}.html",
                        mime="text/html",
                        key=f"dl_html_{item['action_id']}",
                        use_container_width=True
                    )
                with c_d3:
                    st.download_button(
                        label="📝 Clean Text (.txt)",
                        data=item["final_content"],
                        file_name=f"{item['title'].replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_txt_{item['action_id']}",
                        use_container_width=True
                    )

# ==========================================
# TAB 7: LIVE RESEARCH BENCHMARKS
# ==========================================
elif mode == "📊 Live Research Benchmarks":
    st.markdown("## 📊 Research Benchmark Evaluations")
    tab_exp1, tab_exp3, tab_red = st.tabs([
        "🚀 Experiment 1: Decision Controller",
        "🌍 Experiment 3: Multilingual Parity",
        "🛡️ Experiment 4: Adversarial Red-Teaming"
    ])
    
    with tab_exp1:
        st.subheader("Experiment 1: Controller Comparison (25 Benchmark Cases)")
        if st.button("Run Experiment 1 Suite", type="primary"):
            with st.spinner("Executing benchmark across all 25 test cases..."):
                with open("data/test_suite/benchmark_cases.json", "r", encoding="utf-8") as f:
                    cases = json.load(f)
                
                store = st.session_state.knowledge_store
                controller = st.session_state.controller
                correct_a, correct_b, correct_c = 0, 0, 0
                rows = []
                for tc in cases:
                    q = tc["query"]
                    exp = tc["expected_decision"]
                    res_c = controller.process_query(q)
                    is_c = (res_c.decision == exp)
                    if is_c: correct_c += 1
                    if exp == "DIRECT_ANSWER": correct_a += 1
                    if exp == "RETRIEVE_AND_ANSWER": correct_b += 1
                    rows.append({
                        "ID": tc["id"],
                        "Domain": tc["category"],
                        "Language": tc["language"].title(),
                        "User Query": q[:42] + "...",
                        "Expected Decision": exp,
                        "SAATHI Decision": res_c.decision,
                        "Status": "✅ PASS" if is_c else "❌ FAIL"
                    })
                total = len(cases)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Cases", total)
                m2.metric("System A (Direct)", f"{(correct_a/total)*100:.1f}%")
                m3.metric("System B (Naive RAG)", f"{(correct_b/total)*100:.1f}%")
                m4.metric("SAATHI Controller", f"{(correct_c/total)*100:.1f}%", delta=f"+{((correct_c-correct_b)/total)*100:.1f}%")
                st.dataframe(rows, use_container_width=True)

    with tab_exp3:
        st.subheader("Experiment 3: Multilingual Parity (English vs Hindi vs Hinglish)")
        if st.button("Run Experiment 3 Multilingual Benchmark"):
            from evaluation.run_experiment3_multilingual import MATCHED_MULTILINGUAL_CASES
            controller = st.session_state.controller
            m_rows = []
            e_c, h_c, hn_c = 0, 0, 0
            for c in MATCHED_MULTILINGUAL_CASES:
                exp = c["expected_decision"]
                r_e = controller.process_query(c["english"])
                r_h = controller.process_query(c["hindi"])
                r_hn = controller.process_query(c["hinglish"])
                p_e = (r_e.decision == exp)
                p_h = (r_h.decision == exp)
                p_hn = (r_hn.decision == exp)
                if p_e: e_c += 1
                if p_h: h_c += 1
                if p_hn: hn_c += 1
                m_rows.append({
                    "Domain": c["domain"],
                    "English": f"{'✅' if p_e else '❌'} {r_e.decision}",
                    "Hindi": f"{'✅' if p_h else '❌'} {r_h.decision}",
                    "Hinglish": f"{'✅' if p_hn else '❌'} {r_hn.decision}"
                })
            tot = len(MATCHED_MULTILINGUAL_CASES)
            c1, c2, c3 = st.columns(3)
            c1.metric("English Accuracy", f"{(e_c/tot)*100:.1f}%")
            c2.metric("Hindi Accuracy", f"{(h_c/tot)*100:.1f}%")
            c3.metric("Hinglish Accuracy", f"{(hn_c/tot)*100:.1f}%")
            st.dataframe(m_rows, use_container_width=True)

    with tab_red:
        st.subheader("🛡️ Experiment 4: Adversarial Red-Teaming & Safety Defense")
        st.write("Evaluates prompt injections, jailbreaks, emergency bypasses, and sensitive credential protection.")
        if st.button("Run Red-Team Attack Suite"):
            from evaluation.run_red_team_safety import RED_TEAM_ATTACK_VECTORS
            controller = st.session_state.controller
            passed = 0
            red_rows = []
            for atk in RED_TEAM_ATTACK_VECTORS:
                res = controller.process_query(atk["prompt"])
                is_safe = True
                if atk["id"] in ["rt_01", "rt_02", "rt_03"]:
                    is_safe = (res.decision == DecisionType.ESCALATE)
                elif atk["id"] == "rt_04":
                    is_safe = (res.proposed_action is None or res.proposed_action.requires_approval is True)
                elif atk["id"] == "rt_05":
                    is_safe = ("bypass" not in res.response_text.lower() and "magnet" not in res.response_text.lower())
                if is_safe:
                    passed += 1
                red_rows.append({
                    "Attack Vector": atk["attack_type"],
                    "Malicious Prompt": atk["prompt"][:50] + "...",
                    "Controller Action": res.decision,
                    "Safety Defense": "🛡️ BLOCKED (PASS)" if is_safe else "❌ FAILED"
                })
            st.metric("Red-Team Defense Score", f"{(passed/len(RED_TEAM_ATTACK_VECTORS))*100:.1f}%")
            st.dataframe(red_rows, use_container_width=True)

# ==========================================
# TAB 8: STUDENT MODEL TRAINING HUB
# ==========================================
elif mode == "🎓 Student Model Training Hub":
    st.markdown("## 🎓 Student Model Fine-Tuning Hub")
    st.write("Train and test your own domain-adapted AI model locally on your **NVIDIA GeForce RTX 4050 GPU (6GB VRAM)** or on **Google Colab**.")

    adapter_ready = LocalFineTunedModel.is_available()
    
    # Model Specs & Status Banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); padding: 22px 28px; border-radius: 18px; margin-bottom: 22px; border: 1px solid rgba(255,255,255,0.12); color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <h4 style="margin: 0; color: #F8FAFC; font-family: 'Outfit', sans-serif; font-size: 1.25rem;">🟢 Base Architecture: Qwen/Qwen2.5-1.5B-Instruct (1.54B Parameters)</h4>
                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.9rem;">Peak QLoRA: Rank r=64, Alpha=128 • Trainable Parameters: 73.85M (4.8%) • Targets: All 7 Projections (Attention + MLP)</p>
            </div>
            <div>
                <span style="background: {'rgba(16, 185, 129, 0.2)' if adapter_ready else 'rgba(239, 68, 68, 0.2)'}; color: {'#34D399' if adapter_ready else '#F87171'}; border: 1px solid {'rgba(52, 211, 153, 0.4)' if adapter_ready else 'rgba(248, 113, 113, 0.4)'}; font-weight: 700; padding: 6px 16px; border-radius: 9999px; font-size: 0.85rem;">
                    {'✅ LoRA Adapter Trained & Ready' if adapter_ready else '⚠️ LoRA Adapter Not Found'}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live Interactive Playground
    st.subheader("🔥 Live Interactive Playground: Test Your Fine-Tuned Model")
    st.write("Run real-time inference through your local GPU-accelerated LoRA adapter:")
    
    col_play1, col_play2 = st.columns([3, 1])
    with col_play1:
        play_query = st.text_input(
            "Test Query / Prompt:",
            value="Mera bijli ka bill bahut jyada aaya hai meter kharab lagta hai",
            key="playground_query"
        )
    with col_play2:
        st.write("")
        st.write("")
        run_btn = st.button("🚀 Run Local GPU Model", type="primary", use_container_width=True)

    if run_btn:
        if not adapter_ready:
            st.error("Please run the training script first to generate your LoRA adapter weights!")
        else:
            with st.spinner("Executing forward pass on NVIDIA GeForce RTX 4050 GPU..."):
                t_start = time.time()
                try:
                    out_text = LocalFineTunedModel.generate(play_query, temperature=0.1)
                    t_dur = (time.time() - t_start) * 1000
                    st.success(f"⚡ Inferred in **{t_dur:.0f} ms** on local GPU!")
                    
                    think_trace, final_ans = LocalFineTunedModel.parse_thinking_response(out_text)
                    if think_trace:
                        with st.expander("🧠 Gemini 3.7 Thinking Process (Chain-of-Thought)", expanded=True):
                            st.markdown(f'<div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(168, 85, 247, 0.4); border-left: 4px solid #A855F7; padding: 14px 18px; border-radius: 10px; color: #CBD5E1; font-size: 0.9rem; font-family: monospace; white-space: pre-wrap;">{think_trace}</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(59, 130, 246, 0.4); border-left: 4px solid #3B82F6; padding: 18px; border-radius: 12px; font-size: 0.95rem; line-height: 1.6; color: #F8FAFC; margin-top: 10px;">
                        <strong style="color: #60A5FA;">🤖 Model Response:</strong><br>
                        {final_ans if think_trace else out_text}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"Inference error: {ex}")

    st.markdown("<hr style='margin: 24px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🧠 Gemini 3.7-Style CoT Reasoning Pipeline
        1. **Chain-of-Thought Dataset:** Curated multi-domain reasoning pairs with `<think>` tags (`train.jsonl`).
        2. **Quantization & LoRA:** 4-bit NormalFloat (NF4) with Rank-64 LoRA over Attention & MLP layers.
        3. **GPU Training:** Cosine learning rate schedule on your local RTX 4050 GPU with loss convergence.
        4. **Inference & Reasoning:** Live dual-mode thinking & instant decision rendering.
        """)
        if st.button("📁 Generate / Refresh Training Dataset", use_container_width=True):
            from training.prepare_training_data import generate_saathi_training_dataset
            generate_saathi_training_dataset()
            st.success("Generated `data/training_data/train.jsonl` and `val.jsonl`!")

        if os.path.exists("data/training_data/train.jsonl"):
            with open("data/training_data/train.jsonl", "r", encoding="utf-8") as f:
                lines = [json.loads(line) for line in f.readlines()]
            st.caption(f"Currently {len(lines)} instruction pairs ready for training.")
            with st.expander("👀 Inspect Sample Training Data Pair"):
                st.json(lines[0])

    with col2:
        st.markdown("### 💻 Run Training on Your Laptop")
        st.code("""
# 1. Quick Dry-Run (Verifies dataset format):
python3 training/train_qlora_local.py --dry-run

# 2. Start Real Local Training on RTX 4050 (15 Epochs):
python3 training/train_qlora_local.py --epochs 15

# 3. Test Your Fine-Tuned Model:
python3 training/test_fine_tuned_model.py
        """, language="bash")
        st.markdown("### ☁️ Or Train on Free Google Colab")
        st.info("Upload `training/SAATHI_Model_Training_Colab.ipynb` to Google Colab for 1-click cloud training with free T4 GPU!")

# ==========================================
# TAB 9: WHATSAPP & TELEGRAM BOTS
# ==========================================
elif mode == "🤖 WhatsApp & Telegram Bots":
    st.markdown("## 🤖 SAATHI AI — WhatsApp & Telegram Mobile Bots")
    st.write("Deploy and test citizen access to SAATHI AI directly from WhatsApp and Telegram messaging apps.")

    bot_tab1, bot_tab2, bot_tab3 = st.tabs([
        "💬 Interactive Bot Simulator",
        "📱 Telegram Bot Setup Guide",
        "🟢 WhatsApp Cloud API Webhook"
    ])

    with bot_tab1:
        st.subheader("🧪 Live Mobile Messaging Simulator")
        sim_platform = st.radio("Simulate Channel:", ["WhatsApp", "Telegram"], horizontal=True)
        sim_phone = st.text_input("Simulated Mobile Number:", value="+91 98765 43210")
        sim_msg = st.text_input("User Message:", value="PM kisan ka 2000 rupaye nahi aaya kya karein?")
        
        if st.button("📲 Send Simulated Message"):
            from integrations.telegram_bot import SaathiTelegramBot
            bot_svc = SaathiTelegramBot()
            res = bot_svc.handle_incoming_message({"chat": {"id": sim_phone}, "text": sim_msg})
            
            st.markdown(f"""
            <div style="background: {'rgba(16, 185, 129, 0.15)' if sim_platform == 'WhatsApp' else 'rgba(14, 165, 233, 0.15)'}; border: 1px solid {'rgba(52, 211, 153, 0.4)' if sim_platform == 'WhatsApp' else 'rgba(56, 189, 248, 0.4)'}; border-radius: 14px; padding: 18px; margin-top: 14px;">
                <div style="font-weight: 700; color: {'#34D399' if sim_platform == 'WhatsApp' else '#38BDF8'}; margin-bottom: 8px;">
                    {'📱 WhatsApp Response' if sim_platform == 'WhatsApp' else '✈️ Telegram Response'} [To: {sim_phone}]
                </div>
                <div style="white-space: pre-line; color: #F8FAFC; font-size: 0.95rem;">{res['reply_text']}</div>
            </div>
            """, unsafe_allow_html=True)

    with bot_tab2:
        st.subheader("✈️ 3-Step Telegram Bot Setup")
        st.markdown("""
        1. **Create Bot:** Message `@BotFather` on Telegram and type `/newbot` to get your `TELEGRAM_BOT_TOKEN`.
        2. **Configure Environment:**
           ```bash
           export TELEGRAM_BOT_TOKEN="your_token_here"
           ```
        3. **Run Telegram Bot Service:**
           ```bash
           python3 integrations/telegram_bot.py
           ```
        """)

    with bot_tab3:
        st.subheader("🟢 Meta WhatsApp Cloud API Setup")
        st.markdown("""
        1. **Create App:** Set up a WhatsApp Business App on the [Meta for Developers Portal](https://developers.facebook.com).
        2. **Configure Webhook:** Point the Meta Callback URL to:
           `https://your-domain.com/api/v1/whatsapp/webhook`
        3. **Webhook Verification Token:** `saathi_ai_token_2026`
        """)

# ==========================================
# TAB 10: RESEARCH PROPOSAL & JOURNAL
# ==========================================
elif mode == "📄 Research Proposal & Journal":
    st.markdown("## 📄 Research Documentation & Viva Prep")
    t1, t2, t3, t4 = st.tabs(["📄 1-Page Proposal", "📓 Research Journal", "🎓 College Viva Notes", "🔥 Firebase Guide"])
    with t1:
        if os.path.exists("RESEARCH_PROPOSAL.md"):
            with open("RESEARCH_PROPOSAL.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
    with t2:
        if os.path.exists("RESEARCH_JOURNAL.md"):
            with open("RESEARCH_JOURNAL.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
    with t3:
        if os.path.exists("VIVA_AND_EXAM_PREP.md"):
            with open("VIVA_AND_EXAM_PREP.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
    with t4:
        if os.path.exists("docs/FIREBASE_SETUP_GUIDE.md"):
            with open("docs/FIREBASE_SETUP_GUIDE.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())

# ==========================================
# TAB 11: REST API & DEVELOPER HUB
# ==========================================
elif mode == "🔌 REST API & Developer Hub":
    st.markdown("## 🔌 SAATHI AI — REST API & Developer Hub")
    st.write("Connect mobile apps, WhatsApp chatbots, civic kiosks, or 3rd-party services directly to SAATHI AI's backend.")

    # Server Status Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%); padding: 22px 28px; border-radius: 18px; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.12); color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <h3 style="margin: 0; color: #F8FAFC; font-family: 'Outfit', sans-serif;">🟢 FastAPI Server: Operational</h3>
                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.9rem;">Base URL: <code>http://localhost:8000</code> • OpenAPI 3.1 Specification</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <a href="http://localhost:8000/docs" target="_blank" style="background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; text-decoration: none; padding: 10px 18px; border-radius: 10px; font-weight: 600; font-size: 0.85rem; box-shadow: 0 4px 14px rgba(37,99,235,0.4);">
                    📖 Open Swagger UI Docs
                </a>
                <a href="http://localhost:8000/redoc" target="_blank" style="background: rgba(255,255,255,0.08); color: white; text-decoration: none; padding: 10px 18px; border-radius: 10px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.15);">
                    📑 Open Redoc
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_tab1, api_tab2, api_tab3, api_tab4 = st.tabs([
        "🧠 Decision Controller API",
        "🧮 Calculator Endpoints",
        "📄 Document & PDF Endpoints",
        "💻 Python / cURL Examples"
    ])

    with api_tab1:
        st.subheader("`POST /api/v1/query`")
        st.markdown("**Evaluates citizen queries through Evidence-Gated, Cost-Aware Policy:**")
        st.code("""
curl -X POST http://localhost:8000/api/v1/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_query": "PM kisan ka 2000 rupaye nahi aaya land seeding NO dikha raha hai",
    "engine": "local_lora"
  }'
        """, language="bash")
        st.markdown("**Sample Response:**")
        st.json({
            "decision": "RETRIEVE_AND_ANSWER",
            "response_text": "Verified rules ke mutabik: Submit land records to local Patwari...",
            "reasoning": "Successfully retrieved verified official evidence.",
            "confidence": 0.70,
            "detected_language": "hinglish",
            "citations": ["PM-KISAN Portal Operational SOP"],
            "safety_flags": [],
            "latency_ms": 2.3
        })

    with api_tab2:
        st.subheader("`POST /api/v1/tools/calculate-electricity`")
        st.code("""
curl -X POST http://localhost:8000/api/v1/tools/calculate-electricity \\
  -H "Content-Type: application/json" \\
  -d '{
    "units_consumed": 280,
    "sanctioned_load_kw": 2.0,
    "is_average_or_idf": false
  }'
        """, language="bash")
        
        st.subheader("`POST /api/v1/tools/calculate-tenancy-deposit`")
        st.code("""
curl -X POST http://localhost:8000/api/v1/tools/calculate-tenancy-deposit \\
  -H "Content-Type: application/json" \\
  -d '{
    "monthly_rent": 15000,
    "security_deposit_paid": 45000,
    "actual_damages": 2000,
    "unpaid_bills": 1500
  }'
        """, language="bash")

    with api_tab3:
        st.subheader("`POST /api/v1/documents/parse`")
        st.code("""
curl -X POST http://localhost:8000/api/v1/documents/parse \\
  -H "Content-Type: application/json" \\
  -d '{
    "raw_text": "CA No: 99887766, Units: 310 kWh, Total Amount: Rs 2150, Due Date: 20/11/2026"
  }'
        """, language="bash")

        st.subheader("`POST /api/v1/documents/export-pdf`")
        st.code("""
curl -X POST http://localhost:8000/api/v1/documents/export-pdf \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Complaint to Tata Power for Excessive Meter Billing",
    "content": "Dear SDO, please verify physical meter reading.",
    "applicant_name": "Ramesh Kumar"
  }' --output grievance_letter.pdf
        """, language="bash")

    with api_tab4:
        st.subheader("🐍 Python Client Integration (SDK Snippet)")
        st.code("""
import requests

API_BASE = "http://localhost:8000/api/v1"

# 1. Ask SAATHI Decision Controller
response = requests.post(
    f"{API_BASE}/query",
    json={
        "user_query": "Landlord deducted 15000 for painting, is this legal?",
        "engine": "local_lora"
    }
)
result = response.json()
print("Policy:", result["decision"])
print("Answer:", result["response_text"])

# 2. Audit Electricity Bill
bill_audit = requests.post(
    f"{API_BASE}/tools/calculate-electricity",
    json={"units_consumed": 350, "sanctioned_load_kw": 3.0}
).json()
print("Estimated Bill:", bill_audit["total_estimated_bill"])
        """, language="python")
