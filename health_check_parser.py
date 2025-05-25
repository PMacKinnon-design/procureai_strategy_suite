
import pandas as pd

def parse_health_check(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        category_scores = []
        category_comments = []

        for sheet in xls.sheet_names:
            df = xls.parse(sheet)

            if "Score (1–5)" in df.columns and "Comment" in df.columns:
                avg_score = df["Score (1–5)"].mean()
                comments = df["Comment"].dropna().unique().tolist()
                summary_comment = "; ".join(comments[:3]) if comments else "No comments"

                category_scores.append({"Category": sheet, "Average Score": round(avg_score, 2)})
                category_comments.append({"Category": sheet, "Top Comments": summary_comment})
            else:
                return None, None  # Missing columns

        return pd.DataFrame(category_scores), pd.DataFrame(category_comments)

    except Exception as e:
        return None, None
