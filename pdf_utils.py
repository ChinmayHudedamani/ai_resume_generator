from fpdf import FPDF
from docx import Document


def save_resume_as_pdf(resume_text, filename="generated_resume.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    lines = resume_text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename


def save_resume_as_docx(resume_text, filename="generated_resume.docx"):
    doc = Document()

    for line in resume_text.split("\n"):
        cleaned_line = line.strip()
        if cleaned_line:
            doc.add_paragraph(cleaned_line)

    doc.save(filename)
    return filename