
from fpdf import FPDF
import io

class MacKinnonPDF(FPDF):
    def header(self):
        self.image("assets/mackinnon_logo.png", x=10, y=8, w=30)
        self.set_xy(0, 15)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(31, 78, 121)
        self.cell(0, 10, "AI Strategy for Procurement", ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, "Prepared by MacKinnon Consulting", ln=True, align="C")
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, "MacKinnon Consulting | Setting the Standard in Procurement Strategy", 0, 0, "C")

    def add_formatted_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)
        for paragraph in text.split("\n\n"):
            # Clean formatting artifacts
            paragraph = paragraph.replace("**", "").replace("*", "").replace("?", "|")
            paragraph = paragraph.encode("latin-1", "replace").decode("latin-1")
            self.multi_cell(0, 6, paragraph.strip())
            self.ln(4)

def generate_pdf_from_text(report_text: str) -> io.BytesIO:
    pdf = MacKinnonPDF()
    pdf.add_page()
    pdf.add_formatted_text(report_text)
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_bytes)
