
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

# Load and summarize AI Readiness
if ai_file:
    ai_readiness_df = pd.read_excel(ai_file, sheet_name=None)
    ai_data = []

    for sheet, df in ai_readiness_df.items():
        if "Score (1–5)" in df.columns:
            avg_score = df["Score (1–5)"].mean()
            comment_summary = df["Comment"].dropna().iloc[0] if "Comment" in df.columns and not df["Comment"].dropna().empty else ""
            ai_data.append({"Category": sheet, "Avg Score": round(avg_score, 2), "Comments Summary": comment_summary})

    if ai_data:
        overall_avg = round(pd.DataFrame(ai_data)["Avg Score"].mean(), 2)
        ai_data.append({"Category": "Overall Average", "Avg Score": overall_avg, "Comments Summary": "—"})
        ai_results_df = pd.DataFrame(ai_data, columns=["Category", "Avg Score", "Comments Summary"])
        st.subheader("🤖 AI Readiness Score by Category")
        st.dataframe(ai_results_df)
    else:
        ai_results_df = pd.DataFrame(columns=["Category", "Avg Score", "Comments Summary"])

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
