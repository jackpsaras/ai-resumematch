# backend/app/utils/pdf_parser.py
import pdfplumber
# I use pdfplumber because it's the most reliable for resume text extraction in 2026

# function to extract text from PDF bytes
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(layout=True)  # layout=True preserves structure
            if page_text:
                text += page_text + "\n"
    return text.strip()