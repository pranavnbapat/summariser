# extractor.py

import docx
import os
import pytesseract

from pdf2image import convert_from_path
from pdfplumber import open as pdf_open


def extract_text_from_pdf(filepath):
    all_text = []
    fallback_ocr_pages = []

    with pdf_open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                all_text.append(text)
            else:
                fallback_ocr_pages.append(i)

    # OCR fallback for scanned pages
    if fallback_ocr_pages:
        images = convert_from_path(filepath)
        for i in fallback_ocr_pages:
            image = images[i]
            ocr_text = pytesseract.image_to_string(image)
            all_text.append(ocr_text)

    return "\n".join(all_text)


def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
