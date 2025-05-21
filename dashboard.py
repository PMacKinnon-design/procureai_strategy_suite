import streamlit as st
import matplotlib.pyplot as plt

def display_dashboard(scored_df, benchmark_df):
    st.subheader("📊 Metric Health Check")

    # Filter valid rows
    scored_df = scored_df.dropna(subset=["Value"])
    benchmark_df = benchmark_df.dropna(subset=["Benchmark"])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(scored_df["Metric"], scored_df["Value"], color="#1f77b4", label="Your Value")
    ax.barh(benchmark_df["Metric"], benchmark_df["Benchmark"], color="#ff7f0e", alpha=0.6, label="Benchmark")
    ax.set_xlabel("Value")
    ax.set_title("Procurement Metrics vs. Benchmark")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📈 Use Case & ROI Summary")
    st.dataframe(scored_df)
