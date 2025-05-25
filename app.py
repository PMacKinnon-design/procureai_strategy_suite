
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

# --- Download Section ---
st.sidebar.header("📥 Download Templates")
with st.sidebar:
    if os.path.exists("KPI_Performance_Template_FULL.xlsx"):
        with open("KPI_Performance_Template_FULL.xlsx", "rb") as f:
            st.download_button("📊 Download KPI Performance Template", f, file_name="KPI_Performance_Template_FULL.xlsx")

    if os.path.exists("Health_Check_Questionnaire_Template_v2.xlsx"):
        with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
            st.download_button("🩺 Download Health Check Questionnaire", f, file_name="Health_Check_Questionnaire_Template_v2.xlsx")

    if os.path.exists("AI_Readiness_Questionnaire_Template.xlsx"):
        with open("AI_Readiness_Questionnaire_Template.xlsx", "rb") as f:
            st.download_button("🤖 Download AI Readiness Questionnaire", f, file_name="AI_Readiness_Questionnaire_Template.xlsx")

# --- KPI Comparison Upload & Chart ---
st.header("📊 KPI Performance Comparison")
kpi_file = st.file_uploader("Upload Completed KPI Performance Template", type=["csv", "xlsx"])
if kpi_file:
    try:
        if kpi_file.name.endswith(".csv"):
            kpi_df = pd.read_csv(kpi_file)
        else:
            kpi_df = pd.read_excel(kpi_file)

        if "Metric" in kpi_df.columns and "Your Value" in kpi_df.columns and "Category" in kpi_df.columns:
            st.dataframe(kpi_df[["Category", "Metric", "Your Value"]])
            kpi_grouped = kpi_df.groupby("Category")["Your Value"].mean().reset_index()

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(kpi_grouped["Category"], kpi_grouped["Your Value"], color="#1f77b4")
            ax.set_xlabel("Average Your Value")
            ax.set_title("KPI Comparison by Category")
            st.pyplot(fig)
        else:
            st.error("KPI file must include 'Metric', 'Your Value', and 'Category' columns.")
    except Exception as e:
        st.error(f"❌ Error processing KPI file: {e}")

# --- Health Check Questionnaire Upload ---
st.header("🩺 Health Check Questionnaire Scores")
hc_file = st.file_uploader("Upload Completed Health Check Questionnaire", type=["xlsx"], key="health_check")
if hc_file:
    try:
        xls = pd.ExcelFile(hc_file)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet)
            if {"Question", "Score (1–5)", "Comment"}.issubset(df.columns):
                st.subheader(f"📄 {sheet}")
                st.dataframe(df[["Question", "Score (1–5)", "Comment"]])
                fig, ax = plt.subplots()
                ax.bar(df["Question"], df["Score (1–5)"], color="#1f77b4")
                ax.set_title(f"Scores: {sheet}")
                ax.set_xticklabels(df["Question"], rotation=90)
                st.pyplot(fig)
            else:
                st.warning(f"Sheet '{sheet}' does not have expected columns.")
    except Exception as e:
        st.error(f"⚠️ Could not parse Health Check data: {e}")
