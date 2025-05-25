
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Page configuration
st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)
st.markdown("### Choose the tool mode to proceed:")

mode = st.radio("Select mode:", ["🔍 Procurement Health Check", "🤖 AI Strategy & Pilot Development"])

# Load benchmark file
@st.cache_data
def load_benchmark_data():
    return pd.read_csv("benchmark_data_full.csv")

benchmark_df = load_benchmark_data()

# Tool mode: Procurement Health Check
if mode == "🔍 Procurement Health Check":
    st.subheader("📥 Upload Your KPI Performance Data")
    kpi_file = st.file_uploader("Upload a completed KPI Performance Template (.csv)", type=["csv"])

    if kpi_file:
        try:
            your_df = pd.read_csv(kpi_file)
            merged = pd.merge(your_df, benchmark_df, on="Metric", how="left")
            merged["Difference"] = merged["Your Value"] - merged["Benchmark"]

            st.markdown("### 📊 KPI Comparison Table")
            st.dataframe(merged)

            st.markdown("### 📊 Bar Charts by Category")
            for category in benchmark_df["Category"].unique():
                cat_df = merged[merged["Category"] == category]
                if not cat_df.empty:
                    st.markdown(f"#### 📌 {category}")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    bar_width = 0.35
                    index = range(len(cat_df))

                    ax.barh(index, cat_df["Benchmark"], bar_width, label="Benchmark", color="gray")
                    ax.barh([i + bar_width for i in index], cat_df["Your Value"], bar_width, label="Your Value", color="#1f77b4")
                    ax.set_yticks([i + bar_width / 2 for i in index])
                    ax.set_yticklabels(cat_df["Metric"])
                    ax.invert_yaxis()
                    ax.set_xlabel("Value")
                    ax.set_title(f"{category}: Your Value vs Benchmark")
                    ax.legend()
                    st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error processing KPI data: {e}")

else:
    st.info("🧠 The AI Strategy & Pilot Development Tool is under reconstruction and will be reinstated shortly.")
