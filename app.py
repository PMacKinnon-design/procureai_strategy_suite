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

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite (Debug Export)")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite (Debug Export)</h1>", unsafe_allow_html=True)

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

    # Create merged debug DataFrame
    merged_df = pd.merge(
        scored_df[["Metric", "Value"]],
        benchmark_df[["Metric", "Benchmark"]],
        on="Metric",
        how="outer"
    )
    merged_df["Normalized Value"] = merged_df["Value"] / merged_df["Benchmark"]
    merged_df["Normalized Benchmark"] = 1.0
    merged_df["Difference"] = merged_df["Value"] - merged_df["Benchmark"]

    st.subheader("🛠 DEBUG: Export Full Metric Analysis")
    st.dataframe(merged_df)
    st.download_button(
        "📥 Download Full Debug Dataset as CSV",
        merged_df.to_csv(index=False),
        file_name="debug_metrics_analysis.csv",
        mime="text/csv"
    )

    display_dashboard(scored_df, benchmark_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        strategy_text = generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_results, use_case_df, client)
        st.markdown(strategy_text)
        st.download_button("📥 Download Strategy Report (Text)", strategy_text, file_name="procureai_strategy_report.txt")
