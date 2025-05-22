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
st.markdown(
    """
    <style>
        .main { background-color: #ffffff; }
        h1, h2, h3, h4 { color: #1F4E79; }
        .stButton>button { background-color: #1F4E79; color: white; }
        .css-1d391kg { background-color: #ffffff; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

# Branding Banner
st.image("MacKinnon Consulting Logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)
st.markdown("#### Consulting That Delivers – Powered by MacKinnon Consulting")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

questionnaire_results = run_questionnaire()
questionnaire_df = analyze_responses(questionnaire_results)

# Template download section
st.subheader("📥 Download the Metrics Upload Template")
st.markdown("Use this template to provide your organization's procurement metrics. Complete all rows, then upload below.")
with open("macKinnon_procurement_metrics_template.csv", "rb") as f:
    st.download_button("Download Metrics Template", f, file_name="macKinnon_procurement_metrics_template.csv", mime="text/csv")

uploaded_file = st.file_uploader("📤 Upload Your Completed Metrics Template", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)

    scored_df = score_metrics(metrics_df)
    benchmark_df = compare_with_benchmarks(scored_df)
    roi_df = estimate_roi(scored_df)
    use_case_df = match_use_cases(roi_df, questionnaire_df)

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

    if st.button("📄 Generate AI Strategy Summary Report"):
        with st.spinner("Generating report with GPT-4..."):
            report_text = generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client)
            st.subheader("📄 AI Strategy Summary Report")
            st.markdown(report_text)
            st.download_button("📥 Download Strategy Report (Text)", report_text, file_name="macKinnon_AI_Strategy_Report.txt")
