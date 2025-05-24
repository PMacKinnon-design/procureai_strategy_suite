
import pandas as pd

def parse_health_check(file_path):
    # Only read the "Health Check" sheet
    df = pd.read_excel(file_path, sheet_name="Health Check")

    # Normalize and clean
    df.columns = [col.strip() for col in df.columns]
    df = df[["Category", "Score (1–5)", "Comments"]]
    df = df.groupby("Category").agg({
        "Score (1–5)": "mean",
        "Comments": lambda x: " | ".join(str(c) for c in x if pd.notnull(c))
    }).reset_index()

    df.rename(columns={"Score (1–5)": "Average Score", "Comments": "Aggregated Comments"}, inplace=True)
    return None, df
