from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)   

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "uploaded"}