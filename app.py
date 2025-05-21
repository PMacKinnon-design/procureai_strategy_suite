import streamlit as st
import pandas as pd
from openai import OpenAI

from strategy_report import generate_strategy_narrative
from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from dashboard import display_dashboard
from questionnaire import run_questionnaire, analyze_responses

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

questionnaire_results = run_questionnaire()
user_inputs = analyze_responses(questionnaire_results)

uploaded_file = st.file_uploader("📤 Upload Procurement Metrics CSV", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)
    st.subheader("📋 Uploaded Metrics")
    st.dataframe(metrics_df)

    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df, user_inputs)

    display_dashboard(scored_df, benchmark_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        strategy_text = generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_results, use_case_df, client)
        st.markdown(strategy_text)
        st.download_button("📥 Download Strategy Report (Text)", strategy_text, file_name="procureai_strategy_report.txt")
