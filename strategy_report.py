
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    metric_summary = metrics_df.to_string(index=False)
    benchmark_summary = benchmark_df.to_string(index=False)
    questionnaire_summary = questionnaire_df.to_string(index=False)
    use_case_summary = use_case_df.to_string(index=False)

    base_context = f"""
Procurement Metrics:
{metric_summary}

Benchmark Comparisons:
{benchmark_summary}

AI Readiness Results:
{questionnaire_summary}

Suggested AI Use Cases:
{use_case_summary}
"""

    def get_section(title, instructions, context):
        prompt = f"""
You are a senior consultant at MacKinnon Consulting creating a strategy report for a Fortune 500 Procurement Executive.

Write the following section of a 4-6 page AI Strategy Report using formal third-person tone, with:
- Rationale for each recommendation
- Real-world examples from procurement or supply chain
- Citations from sources (Gartner, Deloitte, BCG) if possible
- Estimated implementation cost
- ROI forecast and explanation

Section: {title}
{instructions}

Use this input context:
{context}

Do not repeat content from other sections. Write fully and clearly.
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    sections = []
    context_memory = base_context

    def add_section(title, instructions):
        section = get_section(title, instructions, context_memory)
        sections.append(f"{title}\n\n{section}")
        return "\n\n".join(sections)

    add_section("1. Executive Summary", "Summarize findings and recommendations (200-300 words).")
    add_section("2. Procurement Metrics vs Industry Benchmarks", "Analyze gaps vs. benchmarks and what they mean (400-500 words).")
    add_section("3. AI Readiness & Maturity Assessment", "Evaluate the org’s readiness to adopt AI (400-500 words).")
    add_section("4. Strategic AI Opportunity Areas", "Identify key use cases, rationale, and impact (400-500 words).")
    add_section("5. Procurement AI Roadmap", "Lay out a roadmap for adoption (400-500 words).")
    add_section("6. Pilot Project Recommendations & ROI Rationale", "Propose 1-2 pilots with cost and ROI (400-500 words).")
    add_section("7. Conclusion and Next Steps", "Summarize key actions and reinforce MacKinnon Consulting’s role (100-200 words).")

    final_report = "\n\n".join(sections)
    return final_report
