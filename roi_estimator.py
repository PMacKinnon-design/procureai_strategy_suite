def estimate_roi(metric_df):
    # Example logic for ROI estimation
    roi_estimates = []
    for _, row in metric_df.iterrows():
        metric = row["Metric"]
        value = row["Value"]
        if metric == "Maverick Spend %":
            estimated_savings = (value - 0.10) * 1000000  # Assume $1M base
        elif metric == "PO Cycle Time":
            estimated_savings = (value - 5) * 2000  # Time savings factor
        else:
            estimated_savings = 50000  # Default value
        roi_estimates.append(estimated_savings)
    metric_df["Estimated ROI ($)"] = roi_estimates
    return metric_df
