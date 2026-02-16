from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(title="Compliance Copilot")

app.include_router(upload_router)
