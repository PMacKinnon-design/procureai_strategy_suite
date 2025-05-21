from fpdf import FPDF
import os

class StrategyPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ProcureAI Strategy Suite Report', ln=True, align='C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, content)
        self.ln(5)

def generate_pdf(metrics_df, benchmark_df, questionnaire_data):
    pdf = StrategyPDF()
    pdf.add_page()

    pdf.add_section("Executive Summary", "This report outlines key metrics, benchmark comparisons, AI readiness, and strategy recommendations for procurement transformation.")

    metric_analysis = ""
    for _, row in metrics_df.iterrows():
        metric_analysis += f"Metric: {row['Metric']}, Value: {row['Value']}, Benchmark: {row.get('Benchmark', 'N/A')}, ROI: ${row.get('Estimated ROI ($)', 0):,.2f}, Suggested AI Use: {row.get('Suggested Use Case', 'N/A')}\n"

    pdf.add_section("Procurement Metrics & Benchmark Comparison", metric_analysis)
    questionnaire_summary = f"Automation: {questionnaire_data['automation']}, Data Quality: {questionnaire_data['data_quality']}, AI Familiarity: {questionnaire_data['ai_familiarity']}, Integration: {questionnaire_data['integration']}"
    pdf.add_section("AI Readiness Questionnaire Results", questionnaire_summary)

    pdf.add_section("AI Strategy Recommendation", 
    "Based on the above diagnostics, the organization should prioritize AI initiatives in areas where benchmarks are underperformed and readiness allows. Pilot projects should focus on quick ROI, like Guided Buying or Workflow Automation.")

    output_path = os.path.join("downloads", "ai_strategy_summary.pdf")
    os.makedirs("downloads", exist_ok=True)
    pdf.output(output_path)
    return output_path
