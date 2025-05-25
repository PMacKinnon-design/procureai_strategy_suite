
import pandas as pd

def parse_ai_readiness(uploaded_file):
    sheet_data = pd.read_excel(uploaded_file, sheet_name=None)
    ai_data = []

    for category, df in sheet_data.items():
        df.columns = df.columns.str.strip()
        if "Score (1–5)" in df.columns:
            df = df.dropna(subset=["Score (1–5)"])
            df["Score (1–5)"] = pd.to_numeric(df["Score (1–5)"], errors="coerce")
            avg_score = df["Score (1–5)"].mean()
            comment_summary = df["Comment"].dropna().iloc[0] if "Comment" in df.columns and not df["Comment"].dropna().empty else ""
            ai_data.append({
                "Category": category,
                "Avg Score": round(avg_score, 2),
                "Comments Summary": comment_summary
            })

    result_df = pd.DataFrame(ai_data)
    if not result_df.empty:
        overall_avg = round(result_df["Avg Score"].mean(), 2)
        result_df = pd.concat([
            result_df,
            pd.DataFrame([{
                "Category": "Overall Average",
                "Avg Score": overall_avg,
                "Comments Summary": "—"
            }])
        ], ignore_index=True)

    return result_df
