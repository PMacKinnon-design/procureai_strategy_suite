
import streamlit as st
import pandas as pd
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
import os
from openai import OpenAI

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

st.sidebar.title("📂 Upload Input Files")
kpi_file = st.sidebar.file_uploader("Upload KPI Template (.xlsx)", type="xlsx")
hc_file = st.sidebar.file_uploader("Upload Health Check Questionnaire (.xlsx)", type="xlsx")
ai_file = st.sidebar.file_uploader("Upload AI Readiness Questionnaire (.xlsx)", type="xlsx")

# Load benchmark data
benchmark_df = pd.read_csv("benchmark_data_with_sources.csv") if os.path.exists("benchmark_data_with_sources.csv") else pd.DataFrame()

# Initialize containers
kpi_df = pd.DataFrame()
questionnaire_df = pd.DataFrame()
ai_results_df = pd.DataFrame()

# Parse KPI data
if kpi_file:
    kpi_df = pd.read_excel(kpi_file)
    st.subheader("📊 KPI Performance Summary by Category")
    st.dataframe(kpi_df)

# Parse Health Check
if hc_file:
    _, questionnaire_df = parse_health_check(hc_file)
    st.subheader("🧠 Health Check Questionnaire Scores")
    st.dataframe(questionnaire_df)

# Parse AI Readiness file and display summary
if ai_file:
    sheet_data = pd.read_excel(ai_file, sheet_name=None)
    parsed_data = []

    for category, df in sheet_data.items():
        df.columns = df.columns.str.strip()
        if "Score (1–5)" in df.columns:
            df = df.dropna(subset=["Score (1–5)"])
            df["Score (1–5)"] = pd.to_numeric(df["Score (1–5)"], errors="coerce")
            avg_score = df["Score (1–5)"].mean()
            comment_summary = df["Comment"].dropna().iloc[0] if "Comment" in df.columns and not df["Comment"].dropna().empty else ""
            parsed_data.append({
                "Category": category,
                "Avg Score": round(avg_score, 2),
                "Comments Summary": comment_summary
            })

    if parsed_data:
        overall_avg = round(pd.DataFrame(parsed_data)["Avg Score"].mean(), 2)
        parsed_data.append({
            "Category": "Overall Average",
            "Avg Score": overall_avg,
            "Comments Summary": "—"
        })
        ai_results_df = pd.DataFrame(parsed_data)
        st.subheader("🤖 AI Readiness Score by Category")
        st.dataframe(ai_results_df)

# Generate Strategy Report
if st.button("📝 Generate Strategy Report"):
    if not kpi_df.empty and not questionnaire_df.empty and not ai_results_df.empty:
        report_text = generate_strategy_narrative(kpi_df, benchmark_df, questionnaire_df, ai_results_df, client)
        st.subheader("📄 AI Strategy Report")
        st.text_area("Preview", value=report_text, height=500)

        pdf_bytes = generate_pdf_from_text(report_text)
        st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="ProcureAI_Strategy_Report.pdf", mime="application/pdf")
    else:
        st.warning("Please upload all required files: KPI, Health Check, and AI Readiness.")
