import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from questionnaire import run_questionnaire, analyze_responses

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("🛠 App loaded: Safe fallback mode.")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

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

    st.subheader("✅ Processed Metrics vs Benchmarks")
    st.dataframe(benchmark_df)
