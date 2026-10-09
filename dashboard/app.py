"""
Edge AI UPI Behaviour Risk Intelligence Dashboard
Clean, Human-Centric Fintech Interface (No Emojis)
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import uuid
import joblib
import textwrap
from datetime import datetime

def html_block(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# PAGE CONFIG
st.set_page_config(
    page_title="UPI Risk Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# REFINED HUMAN-CENTRIC DESIGN & TYPOGRAPHY
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    letter-spacing: -0.01em;
}

/* Hide Streamlit Deploy Button, Header Chrome, Footer, Contributors */
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stHeaderActionElements"],
[data-testid="stToolbar"],
div[data-testid="stToolbar"],
button[kind="header"],
#MainMenu,
footer,
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
[data-testid="stStatusWidget"],
span.css-fblp2m,
.css-fblp2m,
.css-1dp5vir,
div[class*="reportview"] footer,
.streamlit-footer,
[data-testid="stFooter"],
footer[data-testid="stFooter"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
    pointer-events: none !important;
}

/* Keep sidebar toggle visible */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Background & Main Canvas */
.stApp {
    background-color: #0d0f12;
    color: #e4e7eb;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #13161d;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}
section[data-testid="stSidebar"] * {
    color: #9aa2b1 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-weight: 500;
    font-size: 0.9rem;
    padding: 6px 10px;
    border-radius: 8px;
    transition: all 0.15s ease;
}

/* Human-made KPI Cards */
.kpi-card {
    background: #171a22;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.kpi-title {
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b94a5;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2.1rem;
    font-weight: 700;
    color: #f1f3f7;
    line-height: 1.1;
    font-feature-settings: "tnum";
}
.kpi-sub {
    font-size: 0.78rem;
    color: #636b7b;
    margin-top: 6px;
}

/* Clean Badges (Strictly Typographic, No Emojis) */
.badge-high {
    background: rgba(239, 68, 68, 0.12);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-low {
    background: rgba(16, 185, 129, 0.12);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-med {
    background: rgba(245, 158, 11, 0.12);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Section Header */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f3f5f8;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 10px;
    margin-bottom: 22px;
    letter-spacing: -0.01em;
}

/* Inputs & Form Elements */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: #171a22 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    color: #f1f3f7 !important;
    font-size: 0.92rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #4361ee !important;
}

/* Primary Buttons */
.stButton > button {
    background: #3b5bdb;
    color: #ffffff !important;
    border: 1px solid #4263eb;
    border-radius: 8px;
    padding: 8px 22px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: background 0.15s ease;
}
.stButton > button:hover {
    background: #4263eb;
    border-color: #4c6ef5;
}

/* Alerts */
.alert-high {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #fca5a5;
}
.alert-info {
    background: rgba(67, 97, 238, 0.08);
    border: 1px solid rgba(67, 97, 238, 0.25);
    border-left: 3px solid #4361ee;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #bac8ff;
}
.alert-ok {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-left: 3px solid #10b981;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #a7f3d0;
}

/* Result box */
.result-box {
    background: #171a22;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px;
    margin-top: 18px;
}
.risk-bar-outer {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    height: 10px;
    margin-top: 6px;
}
.risk-bar-inner {
    height: 10px;
    border-radius: 6px;
}

/* UPI Payment Device Canvas */
.upi-phone {
    max-width: 440px;
    margin: 0 auto;
    background: #141720;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 32px 28px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}
.upi-avatar {
    width: 52px;
    height: 52px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 auto 12px;
    letter-spacing: 0.05em;
}
.upi-label {
    font-size: 0.72rem;
    color: #7b8494;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 4px;
    font-weight: 600;
}
.upi-id {
    font-size: 0.88rem;
    color: #adb5bd;
    text-align: center;
    font-family: inherit;
    margin-bottom: 20px;
}
.upi-amount-display {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    letter-spacing: -0.02em;
    line-height: 1.1;
    font-feature-settings: "tnum";
}
.upi-rupee {
    font-size: 1.8rem;
    color: #8b94a5;
    font-weight: 400;
    margin-right: 2px;
}
.upi-divider {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    margin: 18px 0;
}

/* Status Cards in UPI */
.payment-success {
    background: #16221d;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 26px 20px;
    text-align: center;
}
.payment-failed {
    background: #271719;
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 16px;
    padding: 26px 20px;
    text-align: center;
}
.payment-warning {
    background: #251d13;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 16px;
    padding: 26px 20px;
    text-align: center;
}
.status-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.status-pill.success {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.status-pill.danger {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}
.status-pill.warning {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "transactions" not in st.session_state:
    csv_path = os.path.join(ROOT, "transactions.csv")
    if os.path.exists(csv_path):
        try:
            st.session_state.transactions = pd.read_csv(csv_path).to_dict("records")
        except Exception:
            st.session_state.transactions = []
    else:
        st.session_state.transactions = []

if "graph_edges" not in st.session_state:
    st.session_state.graph_edges = []

# ML MODELS
@st.cache_resource
def load_models():
    iso_path = os.path.join(ROOT, "models", "isolation_forest.pkl")
    log_path = os.path.join(ROOT, "models", "logistic_model.pkl")
    try:
        iso = joblib.load(iso_path)
        log = joblib.load(log_path)
        return iso, log, True
    except Exception:
        return None, None, False

iso_model, log_model, models_loaded = load_models()

def predict_risk(amount, is_night, rolling_avg, rolling_txn, time_gap, velocity_score):
    features_5 = np.array([[amount, is_night, rolling_avg, rolling_txn, time_gap]])
    features_3 = np.array([[amount, is_night, rolling_avg]])
    if models_loaded:
        try:
            log_prob = float(log_model.predict_proba(features_5)[0][1])
            iso_pred = iso_model.predict(features_3)[0]
            iso_score = 0.8 if iso_pred == -1 else 0.2
            prob = (0.7 * log_prob) + (0.3 * iso_score)
        except Exception:
            prob = min(amount / 200000, 0.95)
    else:
        prob = 0.1
        if amount > 50000: prob += 0.35
        elif amount > 20000: prob += 0.2
        if is_night: prob += 0.15
        if velocity_score > 5: prob += 0.2

    # ── Real-world amount-based overrides ──────────────────────────────
    # Small everyday payments should never be high risk
    if amount <= 2000 and not is_night:
        prob = min(prob, 0.30)          # cap at 30 → score max 30, always safe
    elif amount <= 2000 and is_night:
        prob = min(prob, 0.45)          # small night payment → max medium
    elif amount <= 10000:
        prob = min(prob, 0.60)          # medium payment → cap below high-risk threshold
    # Large transfers (>1 lakh) should always be elevated
    if amount > 100000:
        prob = max(prob, 0.72)
    prob = max(0.03, min(prob, 0.97))
    risk_score = int(prob * 100)
    if amount > 70000 or velocity_score > 7:
        risk = 1
    else:
        risk = 1 if risk_score >= 70 else 0
    return risk, risk_score, prob

def save_transaction(tx_dict):
    st.session_state.transactions.append(tx_dict)
    csv_path = os.path.join(ROOT, "transactions.csv")
    try:
        pd.DataFrame(st.session_state.transactions).to_csv(csv_path, index=False)
    except Exception:
        pass

def get_transactions_df():
    if not st.session_state.transactions:
        return pd.DataFrame()
    return pd.DataFrame(st.session_state.transactions)

# SIDEBAR (NO EMOJIS, CLEAN HUMAN DESIGN)
with st.sidebar:
    st.markdown("""
    <div style='padding: 6px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px;'>
        <div style='font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: #6c757d; font-weight: 700;'>Fintech Risk Engine</div>
        <div style='font-size: 1.15rem; font-weight: 700; color: #f8f9fa; margin-top: 2px;'>UPI Risk Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("Navigation", [
        "Overview",
        "UPI Payment",
        "Analyze Transaction",
        "Transaction History",
        "Fraud Network",
        "Fraud Rings",
        "Risk Heatmap",
        "Live Alerts",
    ], label_visibility="collapsed")
    
    st.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.06); margin: 16px 0;'>", unsafe_allow_html=True)
    
    df_all = get_transactions_df()
    total = len(df_all)
    high_risk = int(df_all["risk"].sum()) if total > 0 else 0
    low_risk = total - high_risk
    fraud_rate = round((high_risk / total * 100), 1) if total > 0 else 0
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 14px 12px;'>
        <div style='font-size: 0.68rem; color: #6c757d; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600;'>Session Overview</div>
        <div style='font-size: 1.6rem; font-weight: 700; color: #f1f3f5; margin-top: 4px;'>{total}</div>
        <div style='font-size: 0.72rem; color: #868e96;'>Transactions Processed</div>
        <div style='display:flex; justify-content:space-between; margin-top: 12px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.05);'>
            <div><span style='font-size:0.95rem; font-weight:700; color:#f87171;'>{high_risk}</span> <span style='font-size:0.7rem; color:#6c757d;'>Flagged</span></div>
            <div><span style='font-size:0.95rem; font-weight:700; color:#34d399;'>{low_risk}</span> <span style='font-size:0.7rem; color:#6c757d;'>Cleared</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
    if not models_loaded:
        st.caption("Engine: Rule-based mode")
    else:
        st.caption("Engine: ML Inference Active")

# ─────────────────────────────────────────────────
# 1. OVERVIEW PAGE
# ─────────────────────────────────────────────────
if page == "Overview":
    st.markdown('<div class="section-header">Executive Risk Overview</div>', unsafe_allow_html=True)
    df_all = get_transactions_df()
    total = len(df_all)
    high_risk = int(df_all["risk"].sum()) if total > 0 else 0
    low_risk = total - high_risk
    avg_score = round(df_all["risk_score"].mean(), 1) if total > 0 else 0
    fraud_rate = round((high_risk / total * 100), 1) if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, title, val, sub in [
        (c1, "Total Volume", total, "All processed records"),
        (c2, "Flagged Suspicious", high_risk, f"{fraud_rate}% anomaly rate"),
        (c3, "Cleared Safe", low_risk, "Standard threshold"),
        (c4, "Average Risk Index", f"{avg_score}", "Scale of 0 to 100"),
    ]:
        col.markdown(f'<div class="kpi-card"><div class="kpi-title">{title}</div><div class="kpi-value">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if total > 0:
        col_l, col_r = st.columns([3, 2])
        with col_l:
            st.markdown('<div class="section-header">Temporal Risk Progression</div>', unsafe_allow_html=True)
            st.line_chart(df_all[["risk_score"]].reset_index(drop=True), color="#3b5bdb", height=230)
        with col_r:
            st.markdown('<div class="section-header">Classification Breakdown</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(4, 3.5))
            fig.patch.set_facecolor("#13161d")
            ax.set_facecolor("#13161d")
            sizes = [max(low_risk, 0.001), max(high_risk, 0.001)]
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=["Safe", "Flagged"],
                colors=["#10b981", "#ef4444"],
                autopct="%1.1f%%",
                explode=(0.03, 0.03),
                textprops={"color": "#9aa2b1", "fontsize": 9},
                wedgeprops={"linewidth": 1.5, "edgecolor": "#13161d"}
            )
            for at in autotexts:
                at.set_color("white")
                at.set_fontweight("bold")
            st.pyplot(fig)
            plt.close(fig)

        st.markdown('<div class="section-header">Recent Activity Log</div>', unsafe_allow_html=True)
        st.dataframe(
            df_all.tail(8).sort_index(ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "risk": st.column_config.CheckboxColumn("Flagged"),
                "risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%d"),
                "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
            }
        )
    else:
        st.markdown('<div class="alert-info">No activity recorded yet. Use <b>UPI Payment</b> or <b>Analyze Transaction</b> to evaluate transfers.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# 2. UPI PAYMENT SIMULATOR (HUMAN DESIGN, NO EMOJIS)
# ─────────────────────────────────────────────────
elif page == "UPI Payment":
    CONTACTS = [
        {"name": "Rahul Verma",  "upi": "rahul@okicici", "tag": "RV", "color": "#2b4c7e"},
        {"name": "Priya Sharma", "upi": "priya@okhdfc",  "tag": "PS", "color": "#5a3d7a"},
        {"name": "Kiran Patel",  "upi": "kiran@paytm",   "tag": "KP", "color": "#1e5c46"},
        {"name": "Retail Store", "upi": "myshop@upi",    "tag": "RS", "color": "#7a4e1e"},
        {"name": "Amazon India", "upi": "amazon@apl",    "tag": "AZ", "color": "#6e3b2e"},
        {"name": "Food Delivery","upi": "swiggy@icici",  "tag": "FD", "color": "#6e252a"},
    ]

    if "upi_receiver"      not in st.session_state: st.session_state.upi_receiver = ""
    if "upi_receiver_name" not in st.session_state: st.session_state.upi_receiver_name = ""
    if "upi_amount"        not in st.session_state: st.session_state.upi_amount = 0.0
    if "upi_note"          not in st.session_state: st.session_state.upi_note = ""
    if "upi_paid"          not in st.session_state: st.session_state.upi_paid = False
    if "upi_last_tx"       not in st.session_state: st.session_state.upi_last_tx = None
    if "upi_sender"        not in st.session_state: st.session_state.upi_sender = "user@bank"

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown('<div class="section-header">Direct UPI Transfer</div>', unsafe_allow_html=True)

        st.session_state.upi_sender = st.text_input(
            "Debiting Account (VPA)",
            value=st.session_state.upi_sender,
            placeholder="yourname@bank"
        )

        st.markdown("<div style='font-size:0.82rem; font-weight:600; color:#8b94a5; margin: 12px 0 6px 0;'>Select Beneficiary</div>", unsafe_allow_html=True)

        chip_cols = st.columns(3)
        for i, c in enumerate(CONTACTS):
            with chip_cols[i % 3]:
                if st.button(f"[{c['tag']}] {c['name'].split()[0]}", key=f"chip_{c['tag']}", use_container_width=True):
                    st.session_state.upi_receiver      = c["upi"]
                    st.session_state.upi_receiver_name = c["name"]
                    st.session_state.upi_paid          = False
                    st.session_state.upi_last_tx       = None
                    st.rerun()

        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        manual = st.text_input(
            "Or specify custom UPI ID",
            value=st.session_state.upi_receiver,
            placeholder="recipient@upi"
        )
        if manual != st.session_state.upi_receiver:
            st.session_state.upi_receiver      = manual
            st.session_state.upi_receiver_name = manual.split("@")[0].capitalize()
            st.session_state.upi_paid          = False

        amt_col, note_col = st.columns([1, 1])
        with amt_col:
            new_amt = st.number_input("Transfer Amount (INR)", min_value=0.0, step=100.0,
                                      value=float(st.session_state.upi_amount))
            if new_amt != st.session_state.upi_amount:
                st.session_state.upi_amount = new_amt
                st.session_state.upi_paid   = False
        with note_col:
            st.session_state.upi_note = st.text_input("Remarks",
                                                       value=st.session_state.upi_note,
                                                       placeholder="e.g. Invoice #2041")

        st.markdown("<div style='font-size:0.82rem; font-weight:600; color:#8b94a5; margin: 8px 0 4px 0;'>Quick Preset Amounts</div>", unsafe_allow_html=True)
        qa_cols = st.columns(5)
        for i, qa in enumerate([500, 2000, 5000, 15000, 50000]):
            with qa_cols[i]:
                if st.button(f"{qa:,}", key=f"qa_{qa}", use_container_width=True):
                    st.session_state.upi_amount = float(qa)
                    st.session_state.upi_paid   = False
                    st.rerun()

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        can_pay = bool(st.session_state.upi_receiver and st.session_state.upi_amount > 0)

        pay_btn = st.button("Authorize Transfer", use_container_width=True,
                            disabled=not can_pay,
                            type="primary")

        if pay_btn and can_pay:
            with st.spinner("Analyzing risk vector & executing payment..."):
                import time; time.sleep(0.5)

                df_all   = get_transactions_df()
                now      = datetime.now()
                is_night = 1 if now.hour < 6 or now.hour > 22 else 0
                amount   = st.session_state.upi_amount

                if not df_all.empty:
                    rolling_avg = float(df_all["amount"].tail(5).mean())
                    rolling_txn = len(df_all.tail(5))
                    try:
                        last_time = pd.to_datetime(df_all.iloc[-1]["timestamp"])
                        time_gap  = (now - last_time.replace(tzinfo=None)).total_seconds()
                    except Exception:
                        time_gap = 100.0
                else:
                    rolling_avg = amount; rolling_txn = 1; time_gap = 100.0

                risk, risk_score, prob = predict_risk(
                    amount, is_night, rolling_avg, rolling_txn, time_gap, 1.0
                )
                tx_id = f"tx_{uuid.uuid4().hex[:8]}"

                save_transaction({
                    "transaction_id": tx_id,
                    "sender":         st.session_state.upi_sender,
                    "receiver":       st.session_state.upi_receiver,
                    "amount":         amount,
                    "device_score":   0.85,
                    "location_score": 0.90,
                    "velocity_score": 1.0,
                    "note":           st.session_state.upi_note,
                    "timestamp":      str(now),
                    "risk":           risk,
                    "risk_score":     risk_score,
                })
                st.session_state.upi_last_tx = {
                    "tx_id": tx_id, "risk": risk, "risk_score": risk_score,
                    "amount": amount, "receiver": st.session_state.upi_receiver,
                    "receiver_name": st.session_state.upi_receiver_name,
                    "note": st.session_state.upi_note, "timestamp": str(now),
                }
                st.session_state.upi_paid = True
                st.rerun()

    with right_col:
        r = st.session_state.upi_receiver
        rname = st.session_state.upi_receiver_name or (r.split("@")[0].capitalize() if r else "")
        amt = st.session_state.upi_amount
        monogram = (rname[:2].upper()) if rname else "--"

        if not st.session_state.upi_paid:
            note_html = f"<div style='text-align:center; margin-top:8px; font-size:0.8rem; color:#6c757d;'>Note: {st.session_state.upi_note}</div>" if st.session_state.upi_note else ""
            hint_text = "Awaiting amount and recipient details" if not can_pay else "Ready for authorization"
            html_block(f"""<div class="upi-phone">
<div style="text-align:center;"><div style="font-size:0.7rem; color:#6c757d; letter-spacing:0.12em; text-transform:uppercase; font-weight:700;">Payment Mandate</div></div>
<hr class="upi-divider">
<div class="upi-avatar" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #adb5bd;">{monogram}</div>
<div class="upi-label">Beneficiary</div>
<div style="font-size:1.15rem; font-weight:700; color:#f8f9fa; text-align:center; margin-bottom:2px;">{rname if rname else "Select Recipient"}</div>
<div class="upi-id">{r if r else "Virtual Payment Address"}</div>
<hr class="upi-divider">
<div class="upi-label">Total Debit</div>
<div class="upi-amount-display"><span class="upi-rupee">₹</span>{amt:,.2f}</div>
{note_html}
<hr class="upi-divider">
<div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#6c757d; margin-bottom:6px;"><span>Debit Source</span><span style="color:#ced4da; font-weight:500;">{st.session_state.upi_sender}</span></div>
<div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#6c757d;"><span>AI Risk Verification</span><span style="color:#34d399; font-weight:600;">ACTIVE</span></div>
<div style="margin-top:28px; text-align:center; font-size:0.75rem; color:#6c757d;">{hint_text}</div>
</div>""")

        else:
            tx = st.session_state.upi_last_tx
            if tx is None:
                st.session_state.upi_paid = False
                st.rerun()
            rs = tx["risk_score"]
            risk = tx["risk"]

            if risk == 0:
                note_line = f"<div style='font-size:0.78rem; color:#6c757d; margin-top:6px;'>Remarks: {tx['note']}</div>" if tx['note'] else ""
                status_html = f"""<div class="payment-success">
<span class="status-pill success">Payment Cleared</span>
<div style="font-size:1.3rem; font-weight:700; color:#34d399; margin: 12px 0 4px 0;">Transfer Completed</div>
<div style="font-size:2.4rem; font-weight:700; color:#ffffff; margin: 8px 0;">₹{tx["amount"]:,.2f}</div>
<div style="font-size:0.85rem; color:#9aa2b1;">Transferred to <b>{tx["receiver_name"]}</b> ({tx["receiver"]})</div>
{note_line}
<div style="margin-top:18px; padding:12px; background:rgba(16,185,129,0.08); border-radius:10px; border:1px solid rgba(16,185,129,0.2);">
<div style="font-size:0.68rem; color:#868e96; letter-spacing:0.08em; text-transform:uppercase;">Evaluated Risk Score</div>
<div style="font-size:1.5rem; font-weight:700; color:#34d399;">{rs} <span style="font-size:0.8rem; font-weight:400; color:#6c757d;">/ 100</span></div>
<div style="font-size:0.72rem; color:#10b981; font-weight:600;">NORMAL RANGE - No suspicious patterns detected</div>
</div>
<div style="font-size:0.72rem; color:#495057; margin-top:14px; font-family:monospace;">ID: {tx["tx_id"]} | {tx["timestamp"][:19]}</div>
</div>"""
            elif risk == 1 or rs >= 70:
                status_html = f"""<div class="payment-failed">
<span class="status-pill danger">Critical Anomaly</span>
<div style="font-size:1.3rem; font-weight:700; color:#f87171; margin: 12px 0 4px 0;">High Risk Detected</div>
<div style="font-size:2.4rem; font-weight:700; color:#ffffff; margin: 8px 0;">₹{tx["amount"]:,.2f}</div>
<div style="font-size:0.85rem; color:#fca5a5;">Held for verification: <b>{tx["receiver_name"]}</b> ({tx["receiver"]})</div>
<div style="margin-top:18px; padding:12px; background:rgba(239,68,68,0.08); border-radius:10px; border:1px solid rgba(239,68,68,0.2);">
<div style="font-size:0.68rem; color:#868e96; letter-spacing:0.08em; text-transform:uppercase;">Evaluated Risk Score</div>
<div style="font-size:1.5rem; font-weight:700; color:#f87171;">{rs} <span style="font-size:0.8rem; font-weight:400; color:#6c757d;">/ 100</span></div>
<div style="font-size:0.72rem; color:#ef4444; font-weight:600;">ANOMALOUS - Flagged in live monitoring feed</div>
</div>
<div style="font-size:0.72rem; color:#495057; margin-top:14px; font-family:monospace;">ID: {tx["tx_id"]} | {tx["timestamp"][:19]}</div>
</div>"""
            else:
                status_html = f"""<div class="payment-warning">
<span class="status-pill warning">Elevated Risk</span>
<div style="font-size:1.3rem; font-weight:700; color:#fbbf24; margin: 12px 0 4px 0;">Processed with Caution</div>
<div style="font-size:2.4rem; font-weight:700; color:#ffffff; margin: 8px 0;">₹{tx["amount"]:,.2f}</div>
<div style="font-size:0.85rem; color:#fde68a;">Sent to <b>{tx["receiver_name"]}</b> ({tx["receiver"]})</div>
<div style="margin-top:18px; padding:12px; background:rgba(245,158,11,0.08); border-radius:10px; border:1px solid rgba(245,158,11,0.2);">
<div style="font-size:0.68rem; color:#868e96; letter-spacing:0.08em; text-transform:uppercase;">Evaluated Risk Score</div>
<div style="font-size:1.5rem; font-weight:700; color:#fbbf24;">{rs} <span style="font-size:0.8rem; font-weight:400; color:#6c757d;">/ 100</span></div>
<div style="font-size:0.72rem; color:#f59e0b; font-weight:600;">ELEVATED - Transaction marked for behavioral review</div>
</div>
<div style="font-size:0.72rem; color:#495057; margin-top:14px; font-family:monospace;">ID: {tx["tx_id"]} | {tx["timestamp"][:19]}</div>
</div>"""

            html_block(status_html)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("New Transfer", use_container_width=True):
                st.session_state.upi_paid    = False
                st.session_state.upi_last_tx = None
                st.session_state.upi_amount  = 0.0
                st.session_state.upi_note    = ""
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header" style="font-size:0.95rem;">Recent Beneficiary Transfers</div>', unsafe_allow_html=True)
        df_all = get_transactions_df()
        if df_all.empty:
            st.markdown('<div class="alert-info" style="font-size:0.8rem;">No transfers on record.</div>', unsafe_allow_html=True)
        else:
            recent = df_all.tail(5).sort_index(ascending=False)
            for _, row in recent.iterrows():
                is_high = row.get("risk", 0) == 1
                score = int(row.get("risk_score", 0))
                tag_col = "#f87171" if is_high else ("#fbbf24" if score >= 50 else "#34d399")
                st_label = "HIGH" if is_high else ("MED" if score >= 50 else "SAFE")
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px;
                    background:#141720; border:1px solid rgba(255,255,255,0.05);
                    border-radius:10px; margin-bottom:6px;">
                    <div>
                        <div style="font-size:0.82rem; font-weight:600; color:#e4e7eb;">{str(row.get("receiver","?"))}</div>
                        <div style="font-size:0.7rem; color:#6c757d;">{str(row.get("timestamp",""))[:16]}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.92rem; font-weight:700; color:#ffffff;">₹{float(row.get("amount",0)):,.2f}</div>
                        <div style="font-size:0.68rem; font-weight:700; color:{tag_col}; letter-spacing:0.04em;">{st_label} ({score})</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# 3. ANALYZE TRANSACTION
# ─────────────────────────────────────────────────
elif page == "Analyze Transaction":
    st.markdown('<div class="section-header">Simulated UPI Risk Evaluation</div>', unsafe_allow_html=True)
    with st.form("tx_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            user_id   = st.text_input("Sender VPA", placeholder="e.g. sender@axis")
            amount    = st.number_input("Amount (INR)", min_value=0.0, step=100.0)
        with col2:
            merchant  = st.text_input("Receiver VPA", placeholder="e.g. merchant@icici")
            device_sc = st.slider("Device Trust Index", 0.0, 1.0, 0.85, 0.01)
        with col3:
            location_sc = st.slider("Location Trust Index", 0.0, 1.0, 0.90, 0.01)
            velocity_sc = st.slider("Transaction Velocity (per hour)", 0.0, 10.0, 1.0, 0.5)
        submitted = st.form_submit_button("Run Risk Assessment", use_container_width=True)

    if submitted:
        if not user_id or not merchant:
            st.warning("Please provide valid Sender and Receiver VPAs.")
        else:
            df_all = get_transactions_df()
            now = datetime.now()
            is_night = 1 if now.hour < 6 or now.hour > 22 else 0
            if not df_all.empty:
                rolling_avg = float(df_all["amount"].tail(5).mean())
                rolling_txn = len(df_all.tail(5))
                try:
                    last_time = pd.to_datetime(df_all.iloc[-1]["timestamp"])
                    time_gap = (now - last_time.replace(tzinfo=None)).total_seconds()
                except Exception:
                    time_gap = 100.0
            else:
                rolling_avg = amount; rolling_txn = 1; time_gap = 100.0

            risk, risk_score, prob = predict_risk(amount, is_night, rolling_avg, rolling_txn, time_gap, velocity_sc)
            tx_id = f"tx_{uuid.uuid4().hex[:8]}"
            save_transaction({
                "transaction_id": tx_id, "sender": user_id, "receiver": merchant,
                "amount": amount, "device_score": device_sc, "location_score": location_sc,
                "velocity_score": velocity_sc, "timestamp": str(now), "risk": risk, "risk_score": risk_score
            })
            st.session_state.graph_edges.append({"user": user_id, "merchant": merchant})

            risk_color = "#f87171" if risk == 1 else ("#fbbf24" if risk_score >= 50 else "#34d399")
            badge_class = "badge-high" if risk == 1 else ("badge-med" if risk_score >= 50 else "badge-low")
            level_text  = "FLAGGED HIGH RISK" if risk == 1 else ("ELEVATED RISK" if risk_score >= 50 else "CLEARED SAFE")

            html_block(f"""
            <div class="result-box">
                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div style="font-size:0.72rem; color:#6c757d; text-transform:uppercase; font-weight:600;">Transaction Reference</div>
                        <div style="font-size:1rem; font-weight:600; color:#bac8ff; font-family:monospace;">{tx_id}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-size:0.72rem; color:#6c757d; text-transform:uppercase; font-weight:600;">Evaluated Score</div>
                        <div style="font-size:2.8rem; font-weight:700; color:{risk_color}; line-height:1;">{risk_score}</div>
                        <div style="font-size:0.7rem; color:#6c757d;">out of 100</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.72rem; color:#6c757d; text-transform:uppercase; font-weight:600; margin-bottom:6px;">Decision</div>
                        <span class="{badge_class}">{level_text}</span>
                    </div>
                </div>
                <div style="margin-top:20px;">
                    <div style="font-size:0.72rem; color:#6c757d; margin-bottom:6px; font-weight:600; text-transform:uppercase;">Probability Threshold</div>
                    <div class="risk-bar-outer">
                        <div class="risk-bar-inner" style="width:{risk_score}%; background:linear-gradient(90deg, #3b5bdb, {risk_color})"></div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:20px;">
                    <div style="background:#141720; border-radius:8px; padding:12px; text-align:center;">
                        <div style="font-size:0.7rem; color:#6c757d;">Amount</div>
                        <div style="font-weight:700; color:#f1f3f5;">₹{amount:,.2f}</div>
                    </div>
                    <div style="background:#141720; border-radius:8px; padding:12px; text-align:center;">
                        <div style="font-size:0.7rem; color:#6c757d;">Off-Hours Transfer</div>
                        <div style="font-weight:700; color:#{'f87171' if is_night else '34d399'}">{'Yes' if is_night else 'No'}</div>
                    </div>
                    <div style="background:#141720; border-radius:8px; padding:12px; text-align:center;">
                        <div style="font-size:0.7rem; color:#6c757d;">Velocity (txn/hr)</div>
                        <div style="font-weight:700; color:#{'f87171' if velocity_sc > 5 else '34d399'}">{velocity_sc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# 4. TRANSACTION HISTORY
# ─────────────────────────────────────────────────
elif page == "Transaction History":
    st.markdown('<div class="section-header">Historical Transaction Records</div>', unsafe_allow_html=True)
    df_all = get_transactions_df()
    if df_all.empty:
        st.markdown('<div class="alert-info">No transaction logs available.</div>', unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            risk_filter = st.selectbox("Filter by Category", ["All Records", "Flagged Anomaly Only", "Cleared Safe Only"])
        with col2:
            min_amt = st.number_input("Minimum Amount", value=0.0, step=100.0)
        with col3:
            max_amt = st.number_input("Maximum Amount", value=float(df_all["amount"].max()), step=100.0)

        filtered = df_all.copy()
        if risk_filter == "Flagged Anomaly Only":
            filtered = filtered[filtered["risk"] == 1]
        elif risk_filter == "Cleared Safe Only":
            filtered = filtered[filtered["risk"] == 0]

        filtered = filtered[(filtered["amount"] >= min_amt) & (filtered["amount"] <= max_amt)]
        st.markdown(f"**Showing {len(filtered)} of {len(df_all)} records**")
        st.dataframe(
            filtered.sort_index(ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "risk": st.column_config.CheckboxColumn("Flagged"),
                "risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%d"),
                "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
            }
        )
        st.download_button("Export Dataset (CSV)", filtered.to_csv(index=False).encode("utf-8"),
                           "upi_transactions.csv", "text/csv")

# ─────────────────────────────────────────────────
# 5. FRAUD NETWORK
# ─────────────────────────────────────────────────
elif page == "Fraud Network":
    st.markdown('<div class="section-header">Entity Relationship Topology</div>', unsafe_allow_html=True)
    df_all = get_transactions_df()
    edges = []
    if not df_all.empty and "sender" in df_all.columns:
        for _, row in df_all.iterrows():
            edges.append({"user": str(row.get("sender","")), "merchant": str(row.get("receiver","")), "risk": int(row.get("risk",0))})
    edges += [{"user": e["user"], "merchant": e["merchant"], "risk": 0} for e in st.session_state.graph_edges]

    if not edges:
        st.markdown('<div class="alert-info">No graph topology data. Execute transactions to build connection graph.</div>', unsafe_allow_html=True)
    else:
        G = nx.Graph()
        for e in edges:
            u, m = e["user"], e["merchant"]
            if u and m:
                if G.has_edge(u, m):
                    G[u][m]["weight"] = G[u][m].get("weight",1) + 1
                    G[u][m]["risk"]   = max(G[u][m].get("risk",0), e["risk"])
                else:
                    G.add_edge(u, m, weight=1, risk=e["risk"])

        fig, ax = plt.subplots(figsize=(11, 6))
        fig.patch.set_facecolor("#13161d")
        ax.set_facecolor("#13161d")
        pos = nx.spring_layout(G, seed=42, k=1.8)

        edge_colors = ["#ef4444" if G[u][v].get("risk",0)==1 else "#4263eb" for u,v in G.edges()]
        edge_widths = [G[u][v].get("weight",1)*1.4 for u,v in G.edges()]
        node_colors = ["#3b5bdb" if any(e["user"]==n for e in edges) else "#7950f2" for n in G.nodes()]

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=edge_widths, alpha=0.6)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=500, alpha=0.9)
        nx.draw_networkx_labels(G, pos, ax=ax, font_color="#f8f9fa", font_size=8, font_weight="bold")

        ax.set_title("Inter-Account Flow Network", color="#dee2e6", fontsize=13, fontweight="bold", pad=15)
        legend_elements = [
            mpatches.Patch(color="#3b5bdb", label="Payer Entity"),
            mpatches.Patch(color="#7950f2", label="Payee / Beneficiary"),
            mpatches.Patch(color="#4263eb", label="Standard Flow"),
            mpatches.Patch(color="#ef4444", label="Suspicious Route"),
        ]
        ax.legend(handles=legend_elements, loc="upper left", facecolor="#171a22", edgecolor="#2b3144", labelcolor="#ced4da", fontsize=8)
        ax.axis("off")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(f"""
        <div style="display:flex; gap:16px; margin-top:12px;">
            <div class="kpi-card" style="flex:1; padding:16px;"><div class="kpi-title">Entity Nodes</div><div class="kpi-value" style="font-size:1.6rem;">{G.number_of_nodes()}</div></div>
            <div class="kpi-card" style="flex:1; padding:16px;"><div class="kpi-title">Active Edges</div><div class="kpi-value" style="font-size:1.6rem;">{G.number_of_edges()}</div></div>
            <div class="kpi-card" style="flex:1; padding:16px;"><div class="kpi-title">High-Risk Edges</div><div class="kpi-value" style="font-size:1.6rem; color:#f87171;">{sum(1 for u,v in G.edges() if G[u][v].get("risk",0)==1)}</div></div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# 6. FRAUD RINGS
# ─────────────────────────────────────────────────
elif page == "Fraud Rings":
    st.markdown('<div class="section-header">Coordinated Ring Detection</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#8b94a5; font-size:0.88rem;'>Evaluates dense subgraph formations and hubs with 3+ unique inbound connections.</p>", unsafe_allow_html=True)
    df_all = get_transactions_df()
    rings = []
    if not df_all.empty and "sender" in df_all.columns:
        G = nx.Graph()
        for _, row in df_all.iterrows():
            s, r = str(row.get("sender","")), str(row.get("receiver",""))
            if s and r: G.add_edge(s, r)
        for node in G.nodes():
            neighbors = list(G.neighbors(node))
            if len(neighbors) >= 3:
                rings.append({"hub": node, "connected": neighbors})

    if not rings:
        st.markdown('<div class="alert-ok">No suspicious mule rings or aggregator hubs identified.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-high">Flagged {len(rings)} concentrated aggregator hub(s).</div>', unsafe_allow_html=True)
        for ring in rings:
            with st.expander(f"Hub Account: {ring['hub']} ({len(ring['connected'])} links)"):
                for i, user in enumerate(ring["connected"], 1):
                    st.markdown(f"**{i}.** `{user}` → `{ring['hub']}`")

# ─────────────────────────────────────────────────
# 7. RISK HEATMAP
# ─────────────────────────────────────────────────
elif page == "Risk Heatmap":
    st.markdown('<div class="section-header">Statistical Risk Heatmap</div>', unsafe_allow_html=True)
    df_all = get_transactions_df()
    if df_all.empty or len(df_all) < 2:
        st.markdown('<div class="alert-info">A minimum of 2 transactions is required to plot correlation charts.</div>', unsafe_allow_html=True)
    else:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("<div style='font-size:0.88rem; font-weight:600; color:#adb5bd; margin-bottom:8px;'>Amount vs. Risk Index Correlation</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6.5, 4))
            fig.patch.set_facecolor("#13161d")
            ax.set_facecolor("#13161d")
            scatter = ax.scatter(df_all["amount"], df_all["risk_score"],
                                 c=df_all["risk_score"], cmap="viridis", s=70, alpha=0.85, edgecolors="none")
            ax.set_xlabel("Amount (INR)", color="#868e96", fontsize=9)
            ax.set_ylabel("Risk Index", color="#868e96", fontsize=9)
            ax.tick_params(colors="#6c757d", labelsize=8)
            for spine in ax.spines.values(): spine.set_edgecolor("#2b3144")
            cbar = plt.colorbar(scatter, ax=ax)
            plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#868e96", fontsize=8)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with col_r:
            st.markdown("<div style='font-size:0.88rem; font-weight:600; color:#adb5bd; margin-bottom:8px;'>Risk Score Distribution Frequency</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6.5, 4))
            fig.patch.set_facecolor("#13161d")
            ax.set_facecolor("#13161d")
            ax.hist(df_all["risk_score"], bins=15, color="#3b5bdb", edgecolor="#13161d", alpha=0.85)
            ax.axvline(70, color="#ef4444", linestyle="--", linewidth=1.5, label="High-Risk Threshold (70)")
            ax.set_xlabel("Risk Score", color="#868e96", fontsize=9)
            ax.set_ylabel("Occurrences", color="#868e96", fontsize=9)
            ax.tick_params(colors="#6c757d", labelsize=8)
            for spine in ax.spines.values(): spine.set_edgecolor("#2b3144")
            ax.legend(facecolor="#171a22", edgecolor="#2b3144", labelcolor="#ced4da", fontsize=8)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

# ─────────────────────────────────────────────────
# 8. LIVE ALERTS
# ─────────────────────────────────────────────────
elif page == "Live Alerts":
    st.markdown('<div class="section-header">Live Security Alerts Monitor</div>', unsafe_allow_html=True)
    df_all = get_transactions_df()
    if df_all.empty:
        st.markdown('<div class="alert-info">No transactions logged in monitoring stream.</div>', unsafe_allow_html=True)
    else:
        alerts = df_all[df_all["risk"] == 1]
        medium = df_all[(df_all["risk"] == 0) & (df_all["risk_score"] >= 50)]
        safe   = df_all[df_all["risk_score"] < 50]

        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="kpi-card"><div class="kpi-title">Critical Alerts</div><div class="kpi-value" style="color:#f87171;">{len(alerts)}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><div class="kpi-title">Elevated Reviews</div><div class="kpi-value" style="color:#fbbf24;">{len(medium)}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><div class="kpi-title">Normal Status</div><div class="kpi-value" style="color:#34d399;">{len(safe)}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if len(alerts) == 0:
            st.markdown('<div class="alert-ok">Zero critical risk events detected.</div>', unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#f87171; margin-bottom:10px;'>Critical Risk Events</div>", unsafe_allow_html=True)
            for _, row in alerts.sort_values("risk_score", ascending=False).iterrows():
                html_block(f"""
                <div class="alert-high">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                        <div>
                            <span style="font-family:monospace; font-weight:700; color:#f87171;">{row.get("transaction_id","N/A")}</span>
                            &nbsp;|&nbsp; <b>₹{float(row.get("amount",0)):,.2f}</b>
                            &nbsp;|&nbsp; {str(row.get("sender","?"))} → {str(row.get("receiver","?"))}
                        </div>
                        <div><span class="badge-high">Risk: {int(row.get("risk_score",0))}</span></div>
                    </div>
                    <div style="font-size:0.75rem; color:#868e96; margin-top:6px;">Timestamp: {str(row.get("timestamp",""))[:19]}</div>
                </div>
                """)

        if len(medium) > 0:
            st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#fbbf24; margin: 16px 0 10px 0;'>Elevated Caution Queue</div>", unsafe_allow_html=True)
            for _, row in medium.sort_values("risk_score", ascending=False).iterrows():
                html_block(f"""
                <div style="background:#251d13; border:1px solid rgba(245,158,11,0.25); border-left:3px solid #f59e0b; border-radius:8px; padding:12px 16px; margin-bottom:8px; color:#fde68a;">
                    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
                        <div>
                            <span style="font-family:monospace; font-weight:700; color:#fbbf24;">{row.get("transaction_id","N/A")}</span>
                            &nbsp;|&nbsp; <b>₹{float(row.get("amount",0)):,.2f}</b>
                            &nbsp;|&nbsp; {str(row.get("sender","?"))} → {str(row.get("receiver","?"))}
                        </div>
                        <div><span class="badge-med">Risk: {int(row.get("risk_score",0))}</span></div>
                    </div>
                </div>
                """)
