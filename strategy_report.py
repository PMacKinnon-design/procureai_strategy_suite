
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are a senior consultant at MacKinnon Consulting preparing a 4–5 page AI Strategy Report for a client's Procurement department. 
This report must be written in the third person voice — not "we" or "our". 
It is from MacKinnon Consulting to a client executive. Avoid markdown, asterisks, hashtags, or bullet symbols.

Your goal is to deliver a formal strategy report like one prepared by McKinsey, Bain, or BCG. The language should be polished, executive-level, and clear.

=== STRUCTURE ===

The report must be divided into the following numbered sections:

1. Executive Summary (200–300 words)
2. Procurement Metrics vs Industry Benchmarks (400–500 words)
3. AI Readiness & Maturity Assessment (400–500 words)
4. Strategic AI Opportunity Areas (400–500 words)
5. Procurement AI Roadmap (400–500 words)
6. Pilot Project Recommendations & ROI Rationale (400–500 words)
7. Conclusion and Next Steps (100–200 words)

Each section should reference insights from the uploaded metrics, benchmarks, questionnaire, and use case alignment.

Do not list raw tables. Extract insights and describe findings in prose with examples, implications, and transitions.
Use clear section labels as in: "1. Executive Summary"

MacKinnon Consulting must be referred to by name where appropriate.

=== METRICS DATA ===
{metric_summary}

=== BENCHMARK DATA ===
{benchmark_summary}

=== QUESTIONNAIRE RESULTS ===
{questionnaire_summary}

=== USE CASE SUGGESTIONS ===
{use_case_summary}

Please now write the full strategy report.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
