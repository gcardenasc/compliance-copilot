from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


def parse_document(file_path: Path) -> str:
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".pdf":
        return parse_pdf(file_path)
    elif file_path.suffix.lower() in [".docx", ".doc"]:
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file type")


def parse_pdf(file_path: Path) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"

    return text


def parse_docx(file_path: Path) -> str:
    doc = Document(str(file_path))
    return "\n".join([p.text for p in doc.paragraphs])
