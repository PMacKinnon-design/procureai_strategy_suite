
import streamlit as st
import pandas as pd
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
from ai_readiness_parser import parse_ai_readiness

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")

# Logo and title
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

# Objective selector
tool_choice = st.radio(
    "Select your objective:",
    ["🩺 Procurement Health Check", "🤖 AI Strategy & Pilot Development"]
)

# Download templates
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

# =========================
# HEALTH CHECK PATH
# =========================
if tool_choice == "🩺 Procurement Health Check":

    if hc_file and kpi_file:
        st.success("✅ Files uploaded successfully.")

        # Parse Health Check questionnaire and KPI performance data
        try:
            health_scores_df, comments_df = parse_health_check(hc_file)
            st.markdown("### 🧮 Health Check Scores by Category")
            st.dataframe(health_scores_df)

            st.markdown("### 🗒 Summary Comments")
            st.dataframe(comments_df)

            st.markdown("### 📊 Health Check Bar Chart (1–5 Score per Category)")
            st.bar_chart(health_scores_df.set_index("Category")["Average Score"])

            st.markdown("📄 [Placeholder] Generate Operational Health Report (AI-generated)")
        except Exception as e:
            st.error(f"❌ Error processing Health Check data: {e}")

# =========================
# AI STRATEGY PATH
# =========================
elif tool_choice == "🤖 AI Strategy & Pilot Development":
    st.markdown("## 🤖 AI Strategy & Pilot Development")
    ai_file = st.file_uploader("📤 Upload AI Readiness Questionnaire (.xlsx)", type=["xlsx"], key="ai_upload")
    kpi_file = st.file_uploader("📤 Upload KPI Performance Template (.xlsx)", type=["xlsx"], key="kpi_upload_ai")

    if ai_file and kpi_file:
        st.success("✅ Files uploaded. [Placeholder] Process and display AI Readiness analysis...")
        st.markdown("📊 [Placeholder] Show Benchmark Comparisons, ROI Visuals, Use Case Matches")
        st.markdown("📄 [Placeholder] Generate Full Procurement AI Strategy Report")

