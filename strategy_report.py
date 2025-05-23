
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are a senior consultant at MacKinnon Consulting delivering a strategic AI report to a Fortune 500 Procurement Executive. 
Write a formal, executive-level strategy report using a third-person voice (no "we", "our", or "us").

This report must be 4–6 pages (minimum 2000 words) and meet the following content criteria:

### For Every Key Recommendation:
- Explain the **rationale** behind the recommendation (why it matters)
- Provide **examples** of similar implementations in other procurement or supply chain organizations (real or representative)
- **Cite reputable sources** such as Gartner, Deloitte, McKinsey, etc. (if no direct source, use phrasing like "According to industry analysts...")
- Include **cost estimates** for implementation (high-level: tool licensing, integration, training, etc.)
- Forecast a reasonable **ROI** with explanation (e.g., time savings, cost reduction, risk mitigation)

### Structure:
Use the following numbered sections. Do not include markdown formatting or asterisks. Write in one continuous narrative.

1. Executive Summary (200–300 words)
2. Procurement Metrics vs Industry Benchmarks (400–500 words)
3. AI Readiness & Maturity Assessment (400–500 words)
4. Strategic AI Opportunity Areas (400–500 words)
5. Procurement AI Roadmap (400–500 words)
6. Pilot Project Recommendations & ROI Rationale (400–500 words)
7. Conclusion and Next Steps (100–200 words)

Be specific, include transitions, and avoid generalities or unsupported claims.

Use the following data to support your narrative:

-- METRICS DATA --
{metric_summary}

-- BENCHMARKS --
{benchmark_summary}

-- AI READINESS RESPONSES --
{questionnaire_summary}

-- SUGGESTED AI USE CASES --
{use_case_summary}

Now write the full report, incorporating the above expectations into every recommendation and section.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
