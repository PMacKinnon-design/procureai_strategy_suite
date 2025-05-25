
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

        with open("KPI_Calculation_Guide.pdf", "rb") as f:
            st.download_button("📘 Download KPI Calculation Guide (PDF)", f, file_name="KPI_Calculation_Guide.pdf")

    st.subheader("📤 Step 2: Upload completed files")
    kpi_file = st.file_uploader("Upload completed KPI Template (.csv)", type=["csv"])
    hc_file = st.file_uploader("Upload completed Health Check Questionnaire (.xlsx)", type=["xlsx"])

elif mode == "🤖 AI Strategy & Pilot Development":
    st.subheader("📥 Step 1: Download and complete the AI Readiness Assessment")
    with open("AI_Readiness_Questionnaire_Template.xlsx", "rb") as f:
        st.download_button("⬇️ Download AI Readiness Questionnaire", f, file_name="AI_Readiness_Questionnaire.xlsx")
    ar_file = st.file_uploader("📤 Upload completed AI Readiness Questionnaire (.xlsx)", type=["xlsx"])
    st.warning("⚠️ GPT Strategy Report temporarily disabled while KPI & Health integration is finalized.")

# ---- LOAD BENCHMARK DATA ----
@st.cache_data
def load_benchmark_data():
    return pd.read_csv("benchmark_data.csv")

benchmark_df = load_benchmark_data()

# ---- KPI ANALYSIS ----
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

# ---- HEALTH CHECK QUESTIONNAIRE ANALYSIS ----
if hc_file:
    try:
        hc_xls = pd.ExcelFile(hc_file)
        categories = hc_xls.sheet_names
        scores = []

        st.subheader("📋 Health Check: Scores by Category")
        for sheet in categories:
            df = hc_xls.parse(sheet)
            avg = df["Score (1–5)"].mean()
            comment = "; ".join(df["Comment"].dropna().astype(str).tolist())
            scores.append({"Category": sheet, "Avg Score": round(avg, 2), "Comments": comment})
            st.markdown(f"#### {sheet}")
            st.dataframe(df)

        hc_results = pd.DataFrame(scores)
        hc_results.loc[len(hc_results.index)] = {
            "Category": "Overall Average",
            "Avg Score": round(hc_results["Avg Score"].mean(), 2),
            "Comments": "—"
        }

        st.subheader("📊 Health Check Scores Summary")
        st.dataframe(hc_results)

        st.markdown("### 📊 Health Check Scores Chart")
        fig, ax = plt.subplots(figsize=(12, 4))
        chart_data = hc_results[hc_results["Category"] != "Overall Average"]
        ax.bar(chart_data["Category"], chart_data["Avg Score"], color="#1f77b4")
        ax.axhline(3, color="gray", linestyle="--", linewidth=1)
        ax.set_ylim(0, 5)
        ax.set_ylabel("Score (1–5)")
        ax.set_title("Health Check Questionnaire Results")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Could not parse Health Check data: {e}")
