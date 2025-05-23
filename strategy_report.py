
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are an AI Strategy Consultant writing a 4–5 page (2000–2500 word) executive strategy report for a Procurement Executive.
Use clear, formal business language like McKinsey or Bain would use in board-facing deliverables.

### GOAL:
Provide a full AI in Procurement Strategy Report, including analysis, recommendations, and next steps.

### STRUCTURE:
Your report must contain the following clearly separated sections:

1. Executive Summary (200–300 words)
2. Procurement Metrics Performance vs Benchmarks (400–500 words)
3. AI Maturity & Organizational Readiness (400–500 words)
4. High-Impact AI Opportunities & Strategic Use Cases (400–500 words)
5. AI in Procurement Strategic Roadmap (400–500 words)
6. Pilot Projects with ROI Expectations & Implementation Path (400–500 words)
7. Conclusion (100–200 words) reinforcing MacKinnon Consulting’s value

Each section must include transitions and insights. Avoid repeating the tables. Summarize insights, not raw data.

### METRICS
{metric_summary}

### BENCHMARKS
{benchmark_summary}

### AI READINESS (QUESTIONNAIRE)
{questionnaire_summary}

### AI USE CASES
{use_case_summary}

Please now write the full report.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
