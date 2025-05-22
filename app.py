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

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite – GPT Strategy Enabled</h1>", unsafe_allow_html=True)

# Load questionnaire
questionnaire_results = run_questionnaire()
questionnaire_df = analyze_responses(questionnaire_results)

# Upload metrics
uploaded_file = st.file_uploader("📤 Upload Your Completed Metrics Template", type="csv")
if uploaded_file:
    st.markdown("🛠 Uploaded file detected.")
    metrics_df = pd.read_csv(uploaded_file)
    st.dataframe(metrics_df)

    st.markdown("🛠 Running scoring and benchmark comparison...")
    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df, questionnaire_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        with st.spinner("Generating report with GPT-4..."):
            client = openai.OpenAI(api_key=openai.api_key)
            report_text = generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client)
            html_text = f"<div style='font-family: Helvetica; font-size: 15px; line-height: 1.6;'>{report_text.replace(chr(10), '<br><br>')}</div>"
            st.markdown(html_text, unsafe_allow_html=True)
