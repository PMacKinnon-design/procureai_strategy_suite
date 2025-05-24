
def generate_strategy_narrative(kpi_df, questionnaire_df, client):
    from openai.types.chat import ChatCompletionMessage
    import textwrap

    # Create prompt summary from input data
    def summarize_kpi_insights(kpi_df):
        summary = []
        for category in kpi_df["Category"].unique():
            subset = kpi_df[kpi_df["Category"] == category]
            red_count = (subset["Performance"] == "Red").sum()
            yellow_count = (subset["Performance"] == "Yellow").sum()
            green_count = (subset["Performance"] == "Green").sum()
            summary.append(f"{category}: {green_count} Green, {yellow_count} Yellow, {red_count} Red KPIs")
        return "\n".join(summary)

    def summarize_questionnaire_insights(questionnaire_df):
        return "\n".join(
            f"{row['Category']}: Avg Score = {row['Avg Questionnaire Score']:.2f}"
            for _, row in questionnaire_df.iterrows()
        )

    kpi_summary = summarize_kpi_insights(kpi_df)
    questionnaire_summary = summarize_questionnaire_insights(questionnaire_df)

    prompt = f"""
You are a strategy consultant writing a 4–6 page strategic assessment for a Procurement Department.

The organization has just completed a full Procurement Health Check, which includes:

1. KPI analysis benchmarked against industry standards.
2. A qualitative questionnaire assessing maturity by category.
3. An AI readiness assessment.

Write a full report with 6 narrative sections:

1. Executive Summary – summarize the key findings and performance themes (300+ words).
2. Procurement Performance Analysis – describe strengths/weaknesses from KPI results:
{kpi_summary}

3. Organizational Sentiment & Maturity – summarize the questionnaire results and gaps:
{questionnaire_summary}

4. Recommended AI Use Cases – match specific AI tools to problem areas identified in 2 & 3.
5. Proposed AI Strategy – roadmap of initiatives, maturity improvement plan, sequencing.
6. Pilot Program Recommendations – 1–2 AI pilots, why they were chosen, costs, ROI projections.

The tone should be formal and objective, as if written by Bain, McKinsey, or BCG.
Do not repeat recommendations. Ensure the report is written entirely in third person.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
