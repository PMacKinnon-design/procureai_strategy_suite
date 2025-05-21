from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_strategy_narrative(metrics_df):
    prompt = f"""
You are a senior procurement strategist and AI advisor. Based on the following company data, write a 3–5 page professional strategy report:

Metrics and Benchmarks:
{metrics_df.to_string(index=False)}

Your report should include:
- Executive Summary
- Key Insights from Metrics
- Strategic Recommendations for AI in Procurement
- Suggested Pilot Projects with explanation of ROI and cost ranges
- Next Steps and Governance Considerations

Make the tone formal and tailored for a CPO.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior strategy consultant specializing in AI and procurement."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
