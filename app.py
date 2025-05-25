
import streamlit as st
import pandas as pd
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
from ai_readiness_parser import parse_ai_readiness

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")

# Logo and header
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

# Introductory text
st.markdown("""
### 🧠 About This Tool

The **ProcureAI Strategy Suite** is a dual-purpose solution designed for Procurement Leaders and Teams to:

1. 🔍 **Assess Procurement Health** — Evaluate organizational performance across 8 functional areas using KPIs and team input to identify operational gaps and improvement priorities.  
2. 🤖 **Develop a Procurement AI Strategy** — Assess AI readiness, compare current performance to benchmarks, and generate a tailored AI roadmap including pilot projects with ROI analysis.

Select your objective below to begin.
""")

# Tool selector toggle
tool_choice = st.radio(
    "Select your objective:",
    ["🩺 Procurement Health Check", "🤖 AI Strategy & Pilot Development"]
)

# Download buttons
st.markdown("## 📥 Download Templates")

col1, col2, col3 = st.columns(3)

with col1:
    with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
        st.download_button(
            label="📄 Health Check Template",
            data=f,
            file_name="Health_Check_Questionnaire_Template_v2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col2:
    with open("AI_Readiness_Questionnaire_Template_v2.xlsx", "rb") as f:
        st.download_button(
            label="🤖 AI Readiness Template",
            data=f,
            file_name="AI_Readiness_Questionnaire_Template_v2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col3:
    with open("KPI_Performance_Template_v2.xlsx", "rb") as f:
        st.download_button(
            label="📊 KPI Performance Template",
            data=f,
            file_name="KPI_Performance_Template_v2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("---")
st.markdown("### 📘 Supporting Document")

with open("KPI_Calculation_Guide.pdf", "rb") as f:
    st.download_button(
        label="📘 Download KPI Calculation Guide (PDF)",
        data=f,
        file_name="KPI_Calculation_Guide.pdf",
        mime="application/pdf"
    )

st.markdown("---")

# Tool-specific placeholders
if tool_choice == "🩺 Procurement Health Check":
    st.markdown("### 🩺 You selected: Procurement Health Check")
    st.info("📂 Upload KPI and Health Check Questionnaire data here...")
    st.markdown("_[Placeholder for charts, scoring, and health report generation]_")

elif tool_choice == "🤖 AI Strategy & Pilot Development":
    st.markdown("### 🤖 You selected: AI Strategy & Pilot Development")
    st.info("📂 Upload KPI and AI Readiness Questionnaire data here...")
    st.markdown("_[Placeholder for benchmark comparison, use cases, and AI strategy report]_")
