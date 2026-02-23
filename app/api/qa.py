from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import run_agent

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    doc_id: str | None = None

@router.post("/qa")
async def ask_question(request: QuestionRequest):
    result = run_agent(request.question, request.doc_id)
    return result