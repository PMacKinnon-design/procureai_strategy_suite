
import streamlit as st
import pandas as pd
from health_check_parser import parse_health_check
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.image("assets/mackinnon_logo.png", width=120)
st.title("ProcureAI Strategy Suite")
st.markdown("### Upload your completed Procurement Health Check Template (.xlsx)")

uploaded_file = st.file_uploader("Upload Health Check Excel File", type=["xlsx"])

if uploaded_file:
    with st.spinner("Parsing Health Check data..."):
        kpi_df, questionnaire_df = parse_health_check(uploaded_file)

    st.subheader("📊 KPI Performance Summary")
    st.dataframe(kpi_df)

    st.subheader("📝 Average Questionnaire Scores")
    st.dataframe(questionnaire_df)

    if st.button("Generate Strategy Report"):
        with st.spinner("Generating strategy report..."):
            report_text = generate_strategy_narrative(kpi_df, questionnaire_df, client)
            st.subheader("📄 AI Strategy Report")
            st.text_area("Full Report", report_text, height=600)

            # PDF download button
            pdf_bytes = generate_pdf_from_text(report_text)
            st.download_button(
                label="Download Branded PDF Report",
                data=pdf_bytes,
                file_name="ProcureAI_Strategy_Report.pdf",
                mime="application/pdf"
            )
