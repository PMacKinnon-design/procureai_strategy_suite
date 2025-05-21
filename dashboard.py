import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_dashboard(scored_df, benchmark_df):
    st.subheader("📊 Metric Health Check (Normalized)")

    # Drop missing
    scored_df = scored_df.dropna(subset=["Metric", "Value"])
    benchmark_df = benchmark_df.dropna(subset=["Metric", "Benchmark"])

    # Merge and normalize
    merged_df = pd.merge(scored_df, benchmark_df, on="Metric", how="inner")

    max_val = max(merged_df["Value"].max(), merged_df["Benchmark"].max())
    merged_df["Normalized Value"] = merged_df["Value"] / max_val
    merged_df["Normalized Benchmark"] = merged_df["Benchmark"] / max_val

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(merged_df["Metric"], merged_df["Normalized Benchmark"], color="#ff7f0e", label="Benchmark", alpha=0.6)
    ax.barh(merged_df["Metric"], merged_df["Normalized Value"], color="#1f77b4", label="Your Value")
    ax.set_xlabel("Normalized Value (0 to 1)")
    ax.set_title("Normalized Procurement Metrics vs. Benchmark")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📈 Use Case & ROI Summary")
    st.dataframe(scored_df)
