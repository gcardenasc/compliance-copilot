from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno al inicio
load_dotenv()

# Asegurar que los directorios de datos existen
for path in ["data/raw", "data/chroma"]:
    Path(path).mkdir(parents=True, exist_ok=True)

from app.api.upload import router as upload_router
from app.api.qa import router as qa_router


app = FastAPI(
    title="Compliance Copilot API",
    description="RAG-based compliance assistant running locally with open-source LLMs",
    version="0.1.0"
)


app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(qa_router, prefix="/api", tags=["Q&A"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
