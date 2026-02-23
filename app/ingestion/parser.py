from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


def parse_document(file_path: Path):
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".pdf":
        return parse_pdf(file_path)
    elif file_path.suffix.lower() in [".docx", ".doc"]:
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file type")


def parse_pdf(file_path: Path):
    doc = fitz.open(file_path)

    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "text": text,
            "page": i + 1
        })

    return pages


def parse_docx(file_path: Path):
    doc = Document(str(file_path))

    return [{
        "text": "\n".join(p.text for p in doc.paragraphs),
        "page": 1
    }]
