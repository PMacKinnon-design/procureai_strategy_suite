
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from strategy_report import generate_strategy_narrative
from generate_pdf import generate_pdf_from_text
from health_check_parser import parse_health_check
from ai_readiness_parser import parse_ai_readiness

st.set_page_config(layout="wide", page_title="ProcureAI Strategy Suite")

st.image("assets/mackinnon_logo.png", width=120)
st.markdown("<h1 style='color: #1F4E79;'>ProcureAI Strategy Suite</h1>", unsafe_allow_html=True)

st.markdown("""
### 🧠 About This Tool

The **ProcureAI Strategy Suite** is a dual-purpose solution designed for Procurement Leaders and Teams to:

1. 🔍 **Assess Procurement Health**
2. 🤖 **Develop a Procurement AI Strategy**
""")

tool_choice = st.radio(
    "Select your objective:",
    ["🩺 Procurement Health Check", "🤖 AI Strategy & Pilot Development"]
)

st.markdown("## 📥 Download Templates")
col1, col2, col3 = st.columns(3)

with col1:
    with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
        st.download_button("📄 Health Check Template", f, "Health_Check_Questionnaire_Template_v2.xlsx")

with col2:
    with open("AI_Readiness_Questionnaire_Template_v2.xlsx", "rb") as f:
        st.download_button("🤖 AI Readiness Template", f, "AI_Readiness_Questionnaire_Template_v2.xlsx")

with col3:
    with open("KPI_Performance_Template_v2.xlsx", "rb") as f:
        st.download_button("📊 KPI Performance Template", f, "KPI_Performance_Template_v2.xlsx")

st.markdown("### 📘 Supporting Document")
with open("KPI_Calculation_Guide.pdf", "rb") as f:
    st.download_button("📘 Download KPI Calculation Guide (PDF)", f, "KPI_Calculation_Guide.pdf")

st.markdown("---")

# =========================
# HEALTH CHECK PATH
# =========================
if tool_choice == "🩺 Procurement Health Check":
    st.markdown("## 🩺 Procurement Health Check")
    hc_file = st.file_uploader("📤 Upload Health Check Questionnaire (.xlsx)", type=["xlsx"], key="hc_upload")
    kpi_file = st.file_uploader("📤 Upload KPI Performance Template (.xlsx)", type=["xlsx"], key="kpi_upload")

    if hc_file and kpi_file:
        st.success("✅ Files uploaded successfully.")
        try:
            health_scores_df, comments_df = parse_health_check(hc_file)
            kpi_data = pd.read_excel(kpi_file)

            if health_scores_df is None or comments_df is None:
                st.error("⚠️ Could not parse Health Check data. Please check file formatting.")
            else:
                st.markdown("### 🧮 Health Check Scores by Category")
                st.dataframe(health_scores_df)

                st.markdown("### 🗒 Comments Summary")
                st.dataframe(comments_df)

                st.markdown("### 📊 KPI Performance Summary by Category")
                st.dataframe(kpi_data)

                st.markdown("### 📈 Health Check Bar Chart (1–5 Scale by Category)")
                try:
                    fig, ax = plt.subplots()
                    health_scores_df.set_index("Category")["Average Score"].plot(kind='bar', ax=ax, color="#1f77b4")
                    ax.set_ylabel("Average Score (1–5)")
                    ax.set_title("Procurement Health Check Results")
                    st.pyplot(fig)
                except Exception as chart_err:
                    st.error(f"📉 Chart error: {chart_err}")

                st.markdown("📄 [Placeholder] Generate Operational Health Report (AI-generated)")

        except Exception as e:
            st.error(f"❌ Error processing Health Check data: {e}")
