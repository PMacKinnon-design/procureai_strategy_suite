import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

from strategy_report import generate_strategy_narrative

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Procurement Metrics CSV", type="csv")
if uploaded_file:
    metrics_df = pd.read_csv(uploaded_file)
    st.subheader("📋 Uploaded Metrics")
    st.dataframe(metrics_df)

    if st.button("📄 Generate AI Strategy Summary Report"):
        st.info("Generating report using GPT-4. This may take up to 30 seconds...")
        strategy_text = generate_strategy_narrative(metrics_df)
        st.download_button("📥 Download Strategy Report (Text)", strategy_text, file_name="procureai_strategy_report.txt")
