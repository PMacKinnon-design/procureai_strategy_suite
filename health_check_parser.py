
import pandas as pd

def parse_health_check(file_path):
    xls = pd.ExcelFile(file_path)
    kpi_results = []
    questionnaire_results = []

    for sheet_name in xls.sheet_names:
        if sheet_name == "Questionnaire":
            continue

        df = pd.read_excel(xls, sheet_name=sheet_name)
        for _, row in df.iterrows():
            try:
                your_value = float(row["Your Value"])
                benchmark = float(row["Benchmark Value"])
            except:
                your_value, benchmark = None, None

            if your_value is not None and benchmark is not None:
                ratio = your_value / benchmark if benchmark != 0 else 0
                if ratio >= 1:
                    status = "Green"
                elif 0.8 <= ratio < 1:
                    status = "Yellow"
                else:
                    status = "Red"
            else:
                status = "N/A"

            kpi_results.append({
                "Category": sheet_name,
                "KPI Name": row["KPI Name"],
                "Your Value": your_value,
                "Benchmark Value": benchmark,
                "Performance": status
            })

    # Questionnaire scoring
    questionnaire_df = pd.read_excel(xls, sheet_name="Questionnaire")
    grouped = questionnaire_df.groupby("Category")["Score (1–5)"]
    avg_scores = grouped.mean().reset_index()
    avg_scores.columns = ["Category", "Avg Questionnaire Score"]

    return pd.DataFrame(kpi_results), avg_scores
