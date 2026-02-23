from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.ingestion.pipeline import ingest_document

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    save_path = Path("data/raw") / file.filename

    with open(save_path, "wb") as f:
        f.write(await file.read())

    doc_id = ingest_document(save_path)

    return {"doc_id": doc_id}