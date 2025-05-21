def estimate_roi(df):
    roi_values = []
    for _, row in df.iterrows():
        metric = row["Metric"]
        value = row["Value"]
        if metric == "Maverick Spend %":
            roi = round((value - 0.1) * 1000000 * 0.2, 2)
        elif metric == "PO Cycle Time":
            roi = round((value - 5) * 2000, 2)
        else:
            roi = 50000
        roi_values.append(roi)
    df["Estimated ROI ($)"] = roi_values
    return df
