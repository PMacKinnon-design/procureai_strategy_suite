
from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_text_color(31, 78, 121)
        self.cell(0, 10, "AI Strategy for Procurement | Powered by MacKinnon Consulting", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, "MacKinnon Consulting – Setting the Standard in Procurement Strategy", 0, 0, "C")

def generate_pdf_from_text(report_text):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for paragraph in report_text.split("\n\n"):
        pdf.multi_cell(0, 10, paragraph.strip())
        pdf.ln(2)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
