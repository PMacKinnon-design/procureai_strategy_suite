
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config and logo
st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

# KPI Upload and Benchmark Merge
st.markdown("## 📊 KPI Comparison: Your Data vs Industry Benchmark")
kpi_file = st.file_uploader("📤 Upload your KPI performance data (.csv)", type=["csv"])

if kpi_file:
    try:
        your_df = pd.read_csv(kpi_file)
        benchmark_df = pd.read_csv("benchmark_data.csv")

        merged = pd.merge(your_df, benchmark_df, on="Metric", how="left")
        merged["Difference"] = merged["Your Value"] - merged["Benchmark"]

        st.markdown("### 📋 KPI Comparison Table")
        st.dataframe(merged)

        st.markdown("### 📊 KPI Comparison Chart")
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35
        index = range(len(merged))

        ax.barh(index, merged["Benchmark"], bar_width, label="Benchmark", color="gray")
        ax.barh([i + bar_width for i in index], merged["Your Value"], bar_width, label="Your Value", color="#1f77b4")
        ax.set_yticks([i + bar_width / 2 for i in index])
        ax.set_yticklabels(merged["Metric"])
        ax.invert_yaxis()
        ax.set_xlabel("Value")
        ax.set_title("Your KPI vs Industry Benchmark")
        ax.legend()

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing KPI data: {e}")
