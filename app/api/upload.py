from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.ingestion.pipeline import ingest_document

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Asegurar que el directorio existe
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        save_path = raw_dir / file.filename

        with open(save_path, "wb") as f:
            f.write(await file.read())

        doc_id = ingest_document(save_path)

        return {"doc_id": doc_id}
    except Exception as e:
        print(f">>> Error en upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))