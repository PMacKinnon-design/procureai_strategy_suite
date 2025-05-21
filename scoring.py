def score_metrics(df):
    def score(value):
        if isinstance(value, (int, float)):
            if value < 0.5:
                return "Red"
            elif value < 0.8:
                return "Yellow"
        return "Green"
    df["Score"] = df["Value"].apply(score)
    return df
