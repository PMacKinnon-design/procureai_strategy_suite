
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
from dotenv import load_dotenv
import os

from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from questionnaire import run_questionnaire, analyze_responses
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>AI Strategy for Procurement | Powered by MacKinnon Consulting</h1>", unsafe_allow_html=True)

st.subheader("📥 Download the Metrics Upload Template")
with open("macKinnon_procurement_metrics_template.csv", "rb") as f:
    st.download_button("Download Template", f, file_name="macKinnon_procurement_metrics_template.csv", mime="text/csv")

questionnaire_results = run_questionnaire()
questionnaire_df = analyze_responses(questionnaire_results)

uploaded_file = st.file_uploader("📤 Upload Your Completed Metrics Template", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)
    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df, questionnaire_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        with st.spinner("Generating report with GPT-4..."):
            client = openai.OpenAI(api_key=openai.api_key)
            report_text = generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client)

            formatted_text = report_text.replace("\n\n", "<br><br>").replace("\n", " ")
            st.markdown(f"<div style='font-family: Helvetica; font-size: 15px; line-height: 1.5;'>{formatted_text}</div>", unsafe_allow_html=True)

            pdf_bytes = generate_pdf_from_text(report_text)
            st.download_button("📥 Download Strategy Report (PDF)", data=pdf_bytes, file_name="MacKinnon_AI_Strategy_Report.pdf", mime="application/pdf")
