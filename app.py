import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

from strategy_report import generate_strategy_narrative
from benchmark_engine import compare_with_benchmarks
from scoring import score_metrics
from roi_estimator import estimate_roi
from use_case_matcher import match_use_cases
from questionnaire import run_questionnaire, analyze_responses

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite (Overlay Chart Fix)</h1>", unsafe_allow_html=True)
st.markdown("### ℹ️ You are running the **chart overlay-fixed version**.")

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
    table_df["Unit"] = table_df["Metric"].map(unit_map)

    st.subheader("📊 Metrics vs Benchmark Analysis Table (Full)")
    display_cols = ["Metric", "Value", "Benchmark", "Difference", "Unit"]
    st.dataframe(table_df[display_cols])

    st.download_button(
        "📥 Download Full Table as CSV",
        table_df.to_csv(index=False),
        file_name="metrics_vs_benchmark_table.csv",
        mime="text/csv"
    )

    for unit in table_df["Unit"].dropna().unique():
        unit_df = table_df[table_df["Unit"] == unit].dropna(subset=["Value", "Benchmark"])
        if not unit_df.empty:
            st.markdown(f"### 📐 Metrics Measured in {unit}")
            st.dataframe(unit_df[display_cols])
            fig, ax = plt.subplots(figsize=(8, max(3, len(unit_df) * 0.5)))

            # Order bars to ensure the taller one is plotted first (background)
            for idx, row in unit_df.iterrows():
                benchmark = row["Benchmark"]
                value = row["Value"]
                metric = row["Metric"]
                if benchmark >= value:
                    ax.barh(metric, benchmark, label="Benchmark" if idx == unit_df.index[0] else "", color="#ff7f0e", alpha=0.6)
                    ax.barh(metric, value, label="Your Value" if idx == unit_df.index[0] else "", color="#1f77b4")
                else:
                    ax.barh(metric, value, label="Your Value" if idx == unit_df.index[0] else "", color="#1f77b4")
                    ax.barh(metric, benchmark, label="Benchmark" if idx == unit_df.index[0] else "", color="#ff7f0e", alpha=0.6)

            ax.set_xlabel(f"Value ({unit})")
            ax.set_title(f"Your Values vs Benchmarks ({unit})")
            ax.legend()
            st.pyplot(fig)

    st.markdown("### 📘 Column Definitions")
    st.markdown("""
- **Metric**: The procurement KPI being evaluated  
- **Value**: Your organization’s current value for this metric  
- **Benchmark**: Industry or peer standard for this metric  
- **Difference**: The variance between your value and the benchmark  
- **Unit**: Clarifies if the metric is measured in %, days, counts, or dollars
""")
