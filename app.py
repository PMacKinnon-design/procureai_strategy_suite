
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- PAGE CONFIG ----
st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)
st.markdown("### Select your objective:")

mode = st.radio("Use this tool to perform:", ["🔍 Procurement Health Check", "🤖 AI Strategy & Pilot Development"])

# ---- DOWNLOAD TEMPLATE BUTTONS ----
if mode == "🔍 Procurement Health Check":
    st.subheader("📥 Step 1: Download and complete the templates")

    col1, col2 = st.columns(2)
    with col1:
        with open("KPI_Performance_Template_FULL.xlsx", "rb") as f:
            st.download_button("⬇️ Download KPI Performance Template", f, file_name="KPI_Performance_Template.xlsx")

        with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
            st.download_button("⬇️ Download Health Check Questionnaire", f, file_name="Health_Check_Questionnaire.xlsx")

    st.subheader("📤 Step 2: Upload completed files")
    kpi_file = st.file_uploader("Upload completed KPI Template (.csv)", type=["csv"])
    hc_file = st.file_uploader("Upload completed Health Check Questionnaire (.xlsx)", type=["xlsx"])

elif mode == "🤖 AI Strategy & Pilot Development":
    st.subheader("📥 Step 1: Download and complete the AI Readiness Assessment")
    with open("AI_Readiness_Questionnaire_Template.xlsx", "rb") as f:
        st.download_button("⬇️ Download AI Readiness Questionnaire", f, file_name="AI_Readiness_Questionnaire.xlsx")
    ar_file = st.file_uploader("📤 Upload completed AI Readiness Questionnaire (.xlsx)", type=["xlsx"])
    st.info("📄 Strategy report generation and pilot recommendation engine will be re-enabled shortly.")

# ---- LOAD BENCHMARK DATA ----
@st.cache_data
def load_benchmark_data():
    return pd.read_csv("benchmark_data.csv")

benchmark_df = load_benchmark_data()

# ---- HEALTH CHECK MODE DISPLAY ----
if mode == "🔍 Procurement Health Check" and kpi_file:
    st.subheader("📊 KPI Comparison Table")
    try:
        user_df = pd.read_csv(kpi_file)
        merged = pd.merge(user_df, benchmark_df, on="Metric", how="left")
        merged["Difference"] = merged["Your Value"] - merged["Benchmark"]
        st.dataframe(merged)

        st.markdown("### 📊 KPI Comparison by Category")
        for category in merged["Category"].unique():
            cat_df = merged[merged["Category"] == category]
            if not cat_df.empty:
                st.markdown(f"#### 📌 {category}")
                fig, ax = plt.subplots(figsize=(10, 5))
                idx = range(len(cat_df))
                bar_width = 0.35
                ax.barh(idx, cat_df["Benchmark"], bar_width, label="Benchmark", color="gray")
                ax.barh([i + bar_width for i in idx], cat_df["Your Value"], bar_width, label="Your Value", color="#1f77b4")
                ax.set_yticks([i + bar_width / 2 for i in idx])
                ax.set_yticklabels(cat_df["Metric"])
                ax.invert_yaxis()
                ax.set_title(f"{category}: Your Value vs Benchmark")
                ax.legend()
                st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing KPI file: {e}")

# Placeholder AI Readiness + Health Check visuals will be reconnected next
