import streamlit as st
import pandas as pd
from openai import OpenAI

from strategy_report import generate_strategy_narrative
from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from questionnaire import run_questionnaire, analyze_responses

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite (Final Table View)</h1>", unsafe_allow_html=True)
st.markdown("### ℹ️ You are running the **final table-only version** with column definitions.")

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

questionnaire_results = run_questionnaire()
user_inputs = analyze_responses(questionnaire_results)

uploaded_file = st.file_uploader("📤 Upload Procurement Metrics CSV", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)

    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df, user_inputs)

    unit_map = {
        "Cost Savings %": "%",
        "Contract Coverage": "%",
        "PO Cycle Time": "days",
        "Supplier Onboarding Time": "days",
        "Supplier Risk Incidents": "count",
        "Maverick Spend %": "%",
        "Procurement ROI": "%",
        "Spend Under Management": "%",
        "Supplier Diversity %": "%",
        "Procurement FTE Productivity": "$/FTE"
    }

    table_df = pd.merge(
        scored_df[["Metric", "Value"]],
        benchmark_df[["Metric", "Benchmark"]],
        on="Metric",
        how="outer"
    )
    table_df["Difference"] = table_df["Value"] - table_df["Benchmark"]
    table_df["Normalized Value"] = table_df["Value"] / table_df["Benchmark"]
    table_df["Normalized Benchmark"] = 1.0
    table_df["Unit"] = table_df["Metric"].map(unit_map)

    st.subheader("📊 Metrics vs Benchmark Analysis Table")
    display_cols = ["Metric", "Value", "Benchmark", "Difference", "Unit"]
    st.dataframe(table_df[display_cols])

    st.download_button(
        "📥 Download Full Table as CSV",
        table_df.to_csv(index=False),
        file_name="metrics_vs_benchmark_table.csv",
        mime="text/csv"
    )

    st.markdown("### 📘 Column Definitions")
    st.markdown("""
- **Metric**: The procurement KPI being evaluated  
- **Value**: Your organization’s current value for this metric  
- **Benchmark**: Industry or peer standard for this metric  
- **Difference**: The variance between your value and the benchmark  
- **Unit**: Clarifies if the metric is measured in %, days, counts, or dollars
""")
