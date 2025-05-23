
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are a senior strategy consultant at MacKinnon Consulting. Write a 4–6 page AI Strategy Report for a Procurement Executive at a Fortune 500 company.

### STYLE & FORMAT:
- Third-person voice only (do not use "we", "our", or "us")
- Executive tone suitable for board-level review (McKinsey/Bain/BCG quality)
- Continuous professional narrative, no bullet points or markdown formatting
- Maintain flow, transitions, and readability across sections

### STRUCTURE:
Write a report with the following 7 clearly labeled sections. Each section should include:
- Rationale for each recommendation
- Specific examples or analogs from procurement or supply chain
- Citations from known sources (e.g., Gartner, Deloitte, BCG), or state "according to industry analysts"
- Estimated cost of implementation (high-level)
- ROI forecast with supporting explanation

Use the following structure:

1. Executive Summary (200–300 words)
2. Procurement Metrics vs Industry Benchmarks (400–500 words)
3. AI Readiness & Maturity Assessment (400–500 words)
4. Strategic AI Opportunity Areas (400–500 words)
5. Procurement AI Roadmap (400–500 words)
6. Pilot Project Recommendations & ROI Rationale (400–500 words)
7. Conclusion and Next Steps (100–200 words)

Each section must be complete and contribute to the overall continuity of the report. Do not repeat identical content across sections.

### INPUT DATA FOR CONTEXT:
-- Procurement Metrics --
{metric_summary}

-- Benchmark Comparisons --
{benchmark_summary}

-- AI Readiness Responses --
{questionnaire_summary}

-- Suggested AI Use Cases --
{use_case_summary}

Now generate the full strategy report according to the structure and expectations above. Do not truncate early.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
