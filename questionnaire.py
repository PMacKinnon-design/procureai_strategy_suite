import streamlit as st
def run_questionnaire():
    st.sidebar.title("📋 AI Readiness Questionnaire")
    q1 = st.sidebar.slider("How automated are your procurement workflows?", 0, 5, 2)
    q2 = st.sidebar.slider("How would you rate your procurement data quality?", 0, 5, 3)
    q3 = st.sidebar.slider("How familiar is your team with AI tools?", 0, 5, 1)
    q4 = st.sidebar.slider("How integrated are your systems (ERP, contract mgmt, etc.)?", 0, 5, 2)
    return {"automation": q1, "data_quality": q2, "ai_familiarity": q3, "integration": q4}
def analyze_responses(answers):
    readiness_score = sum(answers.values()) / len(answers)
    return {"ai_readiness_score": readiness_score}
