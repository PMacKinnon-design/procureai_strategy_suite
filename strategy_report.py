
def generate_strategy_narrative(metrics_df, benchmark_df, questionnaire_df, use_case_df, client):
    summaries = {
        "metrics": "The company’s procurement metrics were benchmarked against industry standards and reveal performance gaps in cost savings, PO cycle time, supplier risk, and contract coverage.",
        "benchmarks": "Industry benchmarks reflect best-in-class performance across procurement efficiency, contract utilization, and strategic sourcing outcomes.",
        "questionnaire": "An AI readiness questionnaire completed by executives and procurement staff shows moderate digital maturity but reveals gaps in AI governance, training, and cross-functional alignment.",
        "use_cases": "Proposed use cases include contract review automation, spend analytics dashboards, risk scoring engines, and AI-enabled compliance monitoring."
    }

    def ask_gpt(section_number, title, instructions):
        prompt = f"""
You are a senior consultant at MacKinnon Consulting delivering an AI Strategy Report to a client’s procurement executive team.

Write the following section of the report using professional third-person language. Do not use 'we', 'our', or 'us'. Use a formal tone, executive-level vocabulary, and structured transitions. Do not use markdown, asterisks, hashtags, or formatting symbols.

This is Section {section_number}: {title}

Use the following input context:
- Procurement Metrics Summary: {summaries["metrics"]}
- Benchmark Insights: {summaries["benchmarks"]}
- AI Readiness Assessment: {summaries["questionnaire"]}
- AI Use Case Suggestions: {summaries["use_cases"]}

Your instructions for this section:
{instructions}

Write this section as part of a continuous strategy report.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    # Build each section
    sections = []
    sections.append(ask_gpt("1", "Executive Summary", "Summarize the overall findings and recommendations. 200–300 words."))
    sections.append(ask_gpt("2", "Procurement Metrics vs Industry Benchmarks", "Analyze key gaps and advantages found in the client’s metrics compared to peers. 400–500 words."))
    sections.append(ask_gpt("3", "AI Readiness & Maturity Assessment", "Assess the organization’s AI preparedness based on the questionnaire and context. 400–500 words."))
    sections.append(ask_gpt("4", "Strategic AI Opportunity Areas", "Highlight the most valuable AI opportunities for this procurement organization. 400–500 words."))
    sections.append(ask_gpt("5", "Procurement AI Roadmap", "Provide a phased roadmap for implementing AI in procurement over 12–24 months. 400–500 words."))
    sections.append(ask_gpt("6", "Pilot Project Recommendations & ROI Rationale", "Propose 1–2 pilot AI initiatives and explain implementation, costs, and ROI rationale. 400–500 words."))
    sections.append(ask_gpt("7", "Conclusion and Next Steps", "Summarize the overall recommendation and reinforce MacKinnon Consulting’s role. 100–200 words."))

    # Combine all into one report
    full_report = "\n\n".join(sections)
    return full_report
