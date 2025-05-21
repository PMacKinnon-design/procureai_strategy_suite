from fpdf import FPDF
import os

class StrategyPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'AI Strategy Summary Report', ln=True, align='C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, content)
        self.ln(5)

def generate_pdf(data, filename='ai_strategy_summary.pdf'):
    pdf = StrategyPDF()
    pdf.add_page()

    pdf.add_section("Executive Summary", 
        "This report provides a strategic overview of AI opportunities in Procurement based on key performance indicators, ROI estimations, and benchmark comparisons.")

    for index, row in data.iterrows():
        content = f"Metric: {row['Metric']}\n"                   f"Current Value: {row['Value']}\n"                   f"Health Score: {row['Score']}\n"                   f"Benchmark: {row.get('Benchmark', 'N/A')}\n"                   f"Estimated ROI: ${row.get('Estimated ROI ($)', 'N/A'):,}\n"                   f"Suggested AI Use Case: {row.get('Suggested Use Case', 'N/A')}\n"
        pdf.add_section(f"Analysis for: {row['Metric']}", content)

    output_path = os.path.join("downloads", filename)
    os.makedirs("downloads", exist_ok=True)
    pdf.output(output_path)
    return output_path
