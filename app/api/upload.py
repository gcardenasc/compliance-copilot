from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from app.ingestion.parser import parse_document

router = APIRouter()

UPLOAD_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)   
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Guardar archivo original
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Parsear documento
    text = parse_document(file_path)

    # 3. Guardar texto procesado
    processed_path = PROCESSED_DIR / f"{file.filename}.txt"
    processed_path.write_text(text, encoding="utf-8")

    return {
        "filename": file.filename,
        "status": "uploaded and parsed"
    }