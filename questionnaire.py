import streamlit as st
import pandas as pd

def run_questionnaire():
    st.header("🧠 AI Readiness Questionnaire")
    st.markdown("**Please complete the following AI Readiness Questionnaire.**")
    st.markdown("> **Important**: Responses should reflect the **average input from Executives, Managers, and Procurement Professionals** in your organization to ensure a balanced view of AI readiness.")

    questions = {
        "Strategic Alignment": [
            "Our organization has a clearly defined AI strategy.",
            "Procurement leadership understands the potential impact of AI on performance.",
            "AI initiatives are prioritized based on business value and organizational goals."
        ],
        "Data Infrastructure & Accessibility": [
            "Our procurement data is clean, structured, and readily accessible for analysis.",
            "We have established pipelines, APIs, or data lakes that support AI initiatives.",
            "Historical procurement data is digitized and maintained for trend analysis."
        ],
        "AI Tool Familiarity": [
            "Our teams are familiar with AI technologies such as machine learning, natural language processing, or large language models.",
            "AI-enabled features in existing procurement tools (e.g., ERPs, sourcing platforms) are actively used.",
            "We are experimenting with or implementing GenAI tools (e.g., ChatGPT, Claude, or Copilot) in our procurement processes."
        ],
        "Talent, Training & Organizational Capability": [
            "Procurement staff have received training in AI fundamentals or data literacy.",
            "We have internal experts, data scientists, or AI-savvy procurement professionals.",
            "Cross-functional teams (e.g., IT, data, procurement) collaborate on AI initiatives."
        ],
        "Execution, Pilots & Scaling": [
            "We have executed at least one AI pilot within procurement.",
            "Lessons from AI pilots are integrated into broader sourcing or contract management practices.",
            "Our organization is actively scaling AI applications beyond the pilot phase."
        ],
        "Governance, Ethics & Risk Management": [
            "We have established ethical guidelines or policies for AI use in procurement.",
            "Risks related to AI (bias, compliance, IP security) are formally assessed.",
            "There is C-level oversight or a governance structure for enterprise-wide AI use."
        ]
    }

    results = {}
    for section, qs in questions.items():
        st.subheader(section)
        for q in qs:
            score = st.slider(q, 1, 5, 3, key=q)
            results[q] = score

    return results

def analyze_responses(results):
    df = pd.DataFrame(list(results.items()), columns=["Question", "Score"])
    return df
