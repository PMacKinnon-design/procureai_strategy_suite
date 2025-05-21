import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_dashboard(scored_df, benchmark_df):
    st.subheader("📊 Metric Health Check (Per-Metric Normalization)")

    if "Metric" not in scored_df or "Value" not in scored_df:
        st.error("Missing 'Metric' or 'Value' in scored_df.")
        return
    if "Metric" not in benchmark_df or "Benchmark" not in benchmark_df:
        st.error("Missing 'Metric' or 'Benchmark' in benchmark_df.")
        return

    # Merge only necessary columns
    merged_df = pd.merge(
        scored_df[["Metric", "Value"]],
        benchmark_df[["Metric", "Benchmark"]],
        on="Metric",
        how="inner"
    )

    if merged_df.empty:
        st.warning("No matching metrics found.")
        return

    # Normalize by each metric's own benchmark
    merged_df["Normalized Value"] = merged_df["Value"] / merged_df["Benchmark"]
    merged_df["Normalized Benchmark"] = 1.0  # Benchmark becomes 1.0 baseline

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(merged_df["Metric"], merged_df["Normalized Benchmark"], color="#ff7f0e", label="Benchmark", alpha=0.6)
    ax.barh(merged_df["Metric"], merged_df["Normalized Value"], color="#1f77b4", label="Your Value")
    ax.set_xlabel("Normalized Ratio to Benchmark")
    ax.set_title("Procurement Metrics (Relative to Benchmark = 1.0)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📈 Use Case & ROI Summary")
    st.dataframe(scored_df)
