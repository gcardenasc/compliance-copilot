from pathlib import Path
from pypdf import PdfReader
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
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_docx(file_path: Path) -> str:
    doc = Document(str(file_path))
    return "\n".join([p.text for p in doc.paragraphs])