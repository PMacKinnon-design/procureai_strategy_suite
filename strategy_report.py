def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire, use_cases_df, client):
    prompt = f"""
You are a senior procurement strategist. Based on the following metrics, benchmark data, AI readiness questionnaire results, and use case suggestions, write a 3–5 page professional strategy report.

Use formal tone, executive-level formatting, and complete paragraphs. Organize the report with clear sections, numbered headers, and bullet points as needed. Include:
1. Executive Summary
2. Performance Analysis vs Benchmarks
3. AI Readiness Insights
4. Recommended AI Strategy for Procurement
5. Pilot Use Cases with Cost and ROI Explanation
6. Next Steps and Governance

Metrics and Benchmarks:
{metrics_df.to_string(index=False)}

Benchmarks:
{benchmark_df.to_string(index=False)}

Questionnaire:
{questionnaire}

Use Case Recommendations:
{use_cases_df.to_string(index=False)}
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
