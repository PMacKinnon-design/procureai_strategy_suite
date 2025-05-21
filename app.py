import streamlit as st
import pandas as pd
from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from dashboard import display_dashboard
from pdf_generator import generate_pdf

st.set_page_config(layout="wide", page_title="AI Opportunity Builder")
st.markdown("<h1 style='color: #1F4E79;'>AI Opportunity & Use Case Builder</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Procurement Metrics CSV", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)
    st.subheader("📋 Uploaded Metrics")
    st.dataframe(metrics_df)

    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df)

    display_dashboard(use_case_df, benchmark_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        pdf_path = generate_pdf(use_case_df)
        with open(pdf_path, "rb") as f:
            st.download_button(label="📥 Download Strategy Report PDF", data=f, file_name="ai_strategy_summary.pdf")
