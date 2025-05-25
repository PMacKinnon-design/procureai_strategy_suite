
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")

st.title("ProcureAI Strategy Suite")

st.header("📊 KPI Comparison by Category")

try:
    kpi_file = st.file_uploader("Upload KPI Performance Test File", type=["csv"])
    if kpi_file:
        kpi_df = pd.read_csv(kpi_file)
        if "Category" not in kpi_df.columns:
            st.error("❌ 'Category' column is missing from the uploaded KPI file.")
        else:
            st.dataframe(kpi_df)

            grouped = kpi_df.groupby("Category")["Your Value"].mean().reset_index()
            st.bar_chart(grouped.set_index("Category"))

except Exception as e:
    st.error(f"❌ Error processing KPI file: {e}")

st.header("📝 Health Check: Scores by Category")

try:
    hc_file = st.file_uploader("Upload Health Check Questionnaire", type=["xlsx"])
    if hc_file:
        xls = pd.ExcelFile(hc_file)
        for sheet_name in xls.sheet_names:
            st.subheader(f"📄 {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if "Question" in df.columns and "Score (1–5)" in df.columns:
                st.dataframe(df[["Question", "Score (1–5)", "Comment"]])
            else:
                st.warning(f"Sheet '{sheet_name}' is missing expected columns.")
except Exception as e:
    st.error(f"⚠️ Could not parse Health Check data: {e}")
