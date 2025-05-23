
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    prompt = """
You are a senior consultant at MacKinnon Consulting. Your task is to deliver a formal, 4–5 page AI Strategy Report (minimum 2000 words) to a client’s Procurement Executive.

### Requirements:
- Write in third-person (e.g., "MacKinnon Consulting recommends..."). Never use "we," "our," or "us."
- Use clear, structured business language suitable for C-suite review (McKinsey/Bain style).
- Do not use markdown formatting, hashtags, or asterisks.
- Write each section completely before moving on.
- Do not stop early or summarize prematurely.
- Minimum length: 2000 words (target 2200–2500 words).

### Report Structure (use numbered sections):

1. Executive Summary (200–300 words)
2. Procurement Metrics vs Industry Benchmarks (400–500 words)
3. AI Readiness & Maturity Assessment (400–500 words)
4. Strategic AI Opportunity Areas (400–500 words)
5. Procurement AI Roadmap (400–500 words)
6. Pilot Project Recommendations & ROI Rationale (400–500 words)
7. Conclusion and Next Steps (100–200 words)

Use examples, transitions, and strategic tone. Reinforce MacKinnon Consulting’s value as the ideal implementation partner.

The data provided is summarized as follows:

- The company’s procurement metrics were benchmarked against industry standards and reveal gaps in cost savings, PO cycle time, supplier risk, and contract coverage.
- An AI readiness questionnaire was completed by executives and staff, showing moderate digital maturity but gaps in AI training, governance, and use-case prioritization.
- Suggested AI use cases include contract analysis automation, spend intelligence dashboards, supplier risk scoring, and process compliance bots.

Please now write the full report using this guidance.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
