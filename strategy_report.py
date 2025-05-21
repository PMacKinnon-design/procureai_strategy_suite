def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire, use_cases_df, client):
    prompt = f"""
You are a senior procurement strategist and AI advisor. Based on the following company data, write a 3–5 page professional strategy report:

1. Metrics and Benchmarks:
{metrics_df.to_string(index=False)}

2. Benchmark Comparisons:
{benchmark_df.to_string(index=False)}

3. Questionnaire Responses (AI Readiness):
{questionnaire}

4. Use Cases and Estimated ROI:
{use_cases_df.to_string(index=False)}

Your report should include:
- Executive Summary
- Key Insights from Metrics and Benchmarking
- AI Readiness Analysis
- Strategic Recommendations for AI in Procurement
- Suggested Pilot Projects with explanation of ROI and cost ranges
- Next Steps and Governance Considerations

Make the tone formal and tailored for a CPO.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior strategy consultant specializing in AI and procurement."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
