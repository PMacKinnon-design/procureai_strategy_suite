
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    prompt = f"""
You are a senior AI consultant at a top-tier firm like McKinsey, Bain, or BCG. A procurement executive at a Fortune 500 company has submitted internal performance metrics, peer benchmarks, and an AI readiness questionnaire. Your task is to write a high-quality, 4–5 page strategy report that:

1. Summarizes key findings from procurement metrics and how they compare to industry benchmarks
2. Analyzes the company's AI maturity using their questionnaire results
3. Identifies procurement process areas where AI can deliver the greatest impact
4. Develops a clear AI Strategy for Procurement tailored to this organization's strengths and gaps
5. Recommends 1–2 pilot AI projects including high-level implementation timeframes and ROI rationale

Format the response as a structured report with section headings. Write in clear, executive-level prose. Do not use markdown or formatting characters like asterisks. Make sure paragraphs are concise and transitions are logical. Include a brief closing statement that positions MacKinnon Consulting as the ideal implementation partner.

## METRICS (company values)
{metric_summary}

## BENCHMARKS (industry values)
{benchmark_summary}

## QUESTIONNAIRE RESULTS (AI readiness self-assessment)
{questionnaire_summary}

## AI USE CASE RECOMMENDATIONS
{use_case_summary}

Respond with the full narrative below:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
