import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_dashboard(scored_df, benchmark_df):
    st.subheader("📊 Metric Health Check (Normalized)")

    if "Metric" not in scored_df or "Value" not in scored_df:
        st.error("The uploaded data is missing required columns: 'Metric' and 'Value'")
        return

    if "Metric" not in benchmark_df or "Benchmark" not in benchmark_df:
        st.error("The benchmark data is missing required columns: 'Metric' and 'Benchmark'")
        return

    # Merge for normalization
    merged_df = pd.merge(scored_df[["Metric", "Value"]], benchmark_df[["Metric", "Benchmark"]], on="Metric", how="inner")

    if merged_df.empty:
        st.warning("No matching metrics found between your data and benchmark.")
        return

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
