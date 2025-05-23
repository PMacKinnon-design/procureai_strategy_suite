
from fpdf import FPDF
import io

class MacKinnonPDF(FPDF):
    def header(self):
        self.image("assets/mackinnon_logo.png", x=10, y=8, w=30)

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(31, 78, 121)
        title = "AI Strategy for Procurement"
        self.set_xy((210 - self.get_string_width(title)) / 2, 15)
        self.cell(self.get_string_width(title) + 2, 10, title, ln=True)

        self.set_font("Helvetica", "", 11)
        subtitle = "Powered by MacKinnon Consulting"
        self.set_xy((210 - self.get_string_width(subtitle)) / 2, 25)
        self.cell(self.get_string_width(subtitle) + 2, 10, subtitle, ln=True)

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150)
        footer_text = "MacKinnon Consulting | Setting the Standard in Procurement Strategy"
        self.cell(0, 10, footer_text, 0, 0, "C")

    def add_formatted_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)
        for paragraph in text.split("\n\n"):
            clean_paragraph = (
                paragraph.replace("#", "")
                         .replace("**", "")
                         .replace("*", "")
                         .replace("?", "|")
                         .replace("We ", "MacKinnon Consulting ")
                         .replace("we ", "MacKinnon Consulting ")
                         .replace("Our ", "MacKinnon Consulting's ")
                         .replace("our ", "MacKinnon Consulting's ")
                         .replace("us ", "the consulting team ")
            )
            clean_paragraph = clean_paragraph.encode("latin-1", "replace").decode("latin-1")
            self.multi_cell(0, 6, clean_paragraph.strip())
            self.ln(4)

def generate_pdf_from_text(report_text: str) -> io.BytesIO:
    pdf = MacKinnonPDF()
    pdf.add_page()
    pdf.add_formatted_text(report_text)
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_bytes)
