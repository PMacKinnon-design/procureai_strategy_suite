import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_dashboard(scored_df, benchmark_df):
    st.subheader("📊 Metric Health Check")

    # Drop rows with missing data
    scored_df = scored_df.dropna(subset=["Metric", "Value"])
    benchmark_df = benchmark_df.dropna(subset=["Metric", "Benchmark"])

    # Merge for consistent ordering and matching
    merged_df = pd.merge(scored_df, benchmark_df, on="Metric", how="inner")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Use aligned values
    ax.barh(merged_df["Metric"], merged_df["Benchmark"], color="#ff7f0e", label="Benchmark", alpha=0.6)
    ax.barh(merged_df["Metric"], merged_df["Value"], color="#1f77b4", label="Your Value")

    ax.set_xlabel("Value")
    ax.set_xlim([0, max(merged_df["Value"].max(), merged_df["Benchmark"].max()) * 1.1])
    ax.set_title("Procurement Metrics vs. Benchmark")
    ax.legend()

    st.pyplot(fig)

    st.subheader("📈 Use Case & ROI Summary")
    st.dataframe(scored_df)
