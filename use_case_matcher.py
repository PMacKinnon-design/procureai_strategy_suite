def match_use_cases(metric_df):
    use_cases = []
    for _, row in metric_df.iterrows():
        metric = row["Metric"]
        value = row["Value"]
        if metric == "Maverick Spend %":
            use_cases.append("Guided Buying AI")
        elif metric == "PO Cycle Time":
            use_cases.append("Process Automation AI")
        elif metric == "Contract Coverage":
            use_cases.append("Contract Opportunity Analyzer")
        else:
            use_cases.append("Generic AI Opportunity")
    metric_df["Suggested Use Case"] = use_cases
    return metric_df
