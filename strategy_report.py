
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are a senior strategy consultant at MacKinnon Consulting. Write a 4–6 page AI Strategy Report for a client’s Procurement department. The report should be written in third person, with no use of "we", "our", or "us".

Use a clear, executive tone suitable for a Fortune 500 audience, like reports written by McKinsey, Bain, or BCG. Write in continuous narrative form with structured, numbered sections. Do not use markdown symbols, asterisks, or hashtags. Maintain strong transitions, avoid repetition, and ensure consistent style.

Your report should be at least 2000–2500 words, clearly separated into the following sections:

1. Executive Summary (200–300 words)
2. Procurement Metrics vs Industry Benchmarks (400–500 words)
3. AI Readiness & Maturity Assessment (400–500 words)
4. Strategic AI Opportunity Areas (400–500 words)
5. Procurement AI Roadmap (400–500 words)
6. Pilot Project Recommendations & ROI Rationale (400–500 words)
7. Conclusion and Next Steps (100–200 words)

Draw insights from the following input data:

-- Procurement Metrics --
{metric_summary}

-- Benchmark Comparisons --
{benchmark_summary}

-- AI Readiness Questionnaire Summary --
{questionnaire_summary}

-- Suggested AI Use Cases --
{use_case_summary}

Now write the full strategy report, preserving a formal voice, strategic clarity, and cohesion across all sections. Do not truncate early.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
