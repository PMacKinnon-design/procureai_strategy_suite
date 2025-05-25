
import streamlit as st
import pandas as pd
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
from ai_readiness_parser import parse_ai_readiness

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")

# Display branding
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

# Download buttons section
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

# Placeholder for future: tool selector, form inputs, report generation
st.markdown("---")
st.markdown("🚧 *Next steps: Add tool selection logic and full functionality below...*")
