from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from app.ingestion.parser import parse_document
from app.ingestion.pipeline import ingest_document

router = APIRouter()

UPLOAD_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)   
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_document(file_path)

    processed_path = PROCESSED_DIR / f"{file.filename}.txt"
    processed_path.write_text(text, encoding="utf-8")

    metadata = {"source": file.filename}
    chunks = ingest_document(text, metadata)

    return {
        "status": "ok",
        "chunks_indexed": chunks,
        "filename": file.filename
    }