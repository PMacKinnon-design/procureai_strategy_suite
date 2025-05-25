
import streamlit as st
import pandas as pd
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
from ai_readiness_parser import parse_ai_readiness
import os
from openai import OpenAI

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

st.sidebar.title("📂 Upload Input Files")
hc_file = st.sidebar.file_uploader("Upload completed Health Check Template (.xlsx)", type="xlsx")
ai_file = st.sidebar.file_uploader("Upload completed AI Readiness Template (.xlsx)", type="xlsx")

# Load internal benchmark data
benchmark_df = pd.read_csv("benchmark_data_with_sources.csv") if os.path.exists("benchmark_data_with_sources.csv") else None

# Load and parse Health Check
if hc_file:
    kpi_df, questionnaire_df = parse_health_check(hc_file)
    st.subheader("📊 KPI Performance Summary by Category")
    st.dataframe(kpi_df)

    st.subheader("🧠 Health Check Questionnaire Scores")
    st.dataframe(questionnaire_df)

# Load and parse AI Readiness
ai_results_df = pd.DataFrame()
if ai_file:
    ai_results_df = parse_ai_readiness(ai_file)
    st.subheader("🤖 AI Readiness Score by Category")
    st.dataframe(ai_results_df)

# Generate Strategy Report
if st.button("📝 Generate Strategy Report"):
    if hc_file and ai_file:
        report_text = generate_strategy_narrative(kpi_df, benchmark_df, questionnaire_df, ai_results_df, client)
        st.subheader("📄 AI Strategy Report")
        st.text_area("Preview", value=report_text, height=500)

        pdf_bytes = generate_pdf_from_text(report_text)
        st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="ProcureAI_Strategy_Report.pdf", mime="application/pdf")
    else:
        st.warning("Please upload both the Health Check and AI Readiness files.")
