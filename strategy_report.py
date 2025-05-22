import openai
import os

def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    # Convert DataFrames to usable summaries
    metric_summary = metrics_df.to_dict(orient="records")
    benchmark_summary = benchmark_df.to_dict(orient="records")
    readiness_summary = questionnaire_df.groupby("Question")["Score"].mean().reset_index().to_dict(orient="records")
    use_case_summary = use_case_df.to_dict(orient="records") if use_case_df is not None else []

    prompt = f"""
You are an expert procurement strategist at a top consulting firm like McKinsey or Bain.

Create a 3–5 page AI Strategy Report for the Procurement Department of a mid-to-large enterprise, using the provided organizational health data, benchmarking, and AI readiness assessment.

Please structure the report using the following sections and write in a polished executive tone:

---

**AI Strategy for Procurement – Powered by MacKinnon Consulting**

**1. Organizational Health & Benchmark Analysis**
Use the uploaded procurement metrics vs. benchmarks to describe:
- Areas of strong performance
- Metrics lagging behind competitors
- Observed patterns and concerns

Data:
{metric_summary}

Benchmarks:
{benchmark_summary}

---

**2. AI Readiness Assessment**
Use the questionnaire results to identify:
- Maturity in AI strategy, data, tools, people, and governance
- Organizational gaps
- Readiness strengths to build upon

Questionnaire Summary:
{readiness_summary}

---

**3. Strategic AI Roadmap for Procurement**
Recommend a phased AI strategy tailored to the organization’s capabilities:
- Short-term and long-term focus areas
- Where AI will deliver the most strategic value
- Alignment to what leading procurement departments are doing

---

**4. Pilot AI Projects**
Recommend 1–2 impactful AI pilots, describing:
- What the project will do
- Why it’s relevant based on the health and readiness profile
- Time to build
- Estimated cost
- Projected ROI and how to calculate it

Use Case Ideas:
{use_case_summary}

---

Include MacKinnon Consulting branding in the footer.
Write clearly and professionally, suitable for C-level readers.
Avoid bullet points except where useful. Write in paragraphs, like a real strategy deliverable.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
