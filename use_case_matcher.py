def match_use_cases(df, answers):
    use_cases = []
    for _, row in df.iterrows():
        metric = row["Metric"]
        if metric == "Maverick Spend %":
            use_cases.append("Guided Buying AI Tool")
        elif metric == "Contract Coverage":
            use_cases.append("Contract Lifecycle Intelligence")
        elif metric == "Supplier Risk Incidents":
            use_cases.append("AI-Powered Risk Detection")
        elif metric == "PO Cycle Time":
            use_cases.append("Procurement Workflow BOT")
        else:
            use_cases.append("Spend & Trend AI Analyzer")
    df["Suggested Use Case"] = use_cases
    return df
