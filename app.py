
import streamlit as st
import pandas as pd
from health_check_parser import parse_health_check
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.title("ProcureAI Strategy Suite")

st.markdown("### 📥 Step 1: Download Questionnaire Templates")
with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
    st.download_button("Download Health Check Questionnaire", f, file_name="Health_Check_Questionnaire_Template.xlsx")
with open("AI_Readiness_Questionnaire_Template_v2.xlsx", "rb") as f:
    st.download_button("Download AI Readiness Questionnaire", f, file_name="AI_Readiness_Questionnaire_Template.xlsx")
with open("KPI_Performance_Template.xlsx", "rb") as f:
    st.download_button("Download KPI Performance Template", f, file_name="KPI_Performance_Template.xlsx")

st.markdown("### 📤 Step 2: Upload Completed Templates")

hc_file = st.file_uploader("Upload completed Procurement Health Check Template (.xlsx)", type=["xlsx"], key="hc")
kpi_file = st.file_uploader("Step 2A: Upload completed KPI Performance Template (.xlsx)", type=["xlsx"], key="kpi")
ai_file = st.file_uploader("Upload completed AI Readiness Template (.xlsx)", type=["xlsx"], key="ai")

if hc_file and kpi_file and ai_file:
    with st.spinner("Analyzing uploaded files..."):
        kpi_df = pd.read_excel(kpi_file, sheet_name=0)
        kpi_df = kpi_df[["KPI Name", "Your Value"]].rename(columns={"KPI Name": "Metric", "Your Value": "Value"})

        kpi_df["Value"] = pd.to_numeric(kpi_df["Value"], errors="coerce")
        benchmark_df = pd.read_csv("benchmark_data_with_sources.csv")
        merged_df = pd.merge(kpi_df, benchmark_df, on="Metric", how="left")

        kpi_display = merged_df[["Metric", "Value", "Benchmark", "Source"]].copy()
        kpi_display["Difference"] = kpi_display["Value"] - kpi_display["Benchmark"]

        health_df, questionnaire_df = parse_health_check(hc_file)
        ai_readiness_df = pd.read_excel(ai_file, sheet_name=None)
        ai_scores = {k: df["Score (1–5)"].mean() for k, df in ai_readiness_df.items()}

    st.subheader("📊 KPI Performance Summary (vs. Benchmark)")
    st.dataframe(kpi_display)

    st.subheader("📝 Health Check Questionnaire Scores")
    st.dataframe(questionnaire_df)

    st.subheader("🤖 AI Readiness Scores")
    st.dataframe(pd.DataFrame(list(ai_scores.items()), columns=["Category", "Avg Score"]))

    if st.button("Generate AI Strategy Report"):
        with st.spinner("Generating strategy report..."):
            report_text = generate_strategy_narrative(kpi_df, questionnaire_df, client, ai_scores)
            st.subheader("📄 AI Strategy Report")
            st.text_area("Full Report", report_text, height=600)

            pdf_bytes = generate_pdf_from_text(report_text)
            st.download_button(
                label="Download Branded PDF Report",
                data=pdf_bytes,
                file_name="ProcureAI_Strategy_Report.pdf",
                mime="application/pdf"
            )
