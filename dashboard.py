import streamlit as st
import matplotlib.pyplot as plt

def display_dashboard(scored_df, benchmark_df):
    st.subheader("Health Scores")
    st.write(scored_df)

    st.subheader("Benchmark Comparison")
    st.write(benchmark_df)

    st.subheader("Metric Health Chart")
    fig, ax = plt.subplots()
    ax.bar(scored_df["Metric"], scored_df["Value"], color="blue", label="Your Value")
    ax.bar(scored_df["Metric"], benchmark_df["Benchmark"], color="orange", alpha=0.5, label="Benchmark")
    ax.set_ylabel("Value")
    ax.set_title("Your Metrics vs Industry Benchmarks")
    ax.legend()
    st.pyplot(fig)
