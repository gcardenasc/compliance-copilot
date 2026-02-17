from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retrieval import retrieve_context, build_rag_prompt
from app.services.llm import generate_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/qa")
async def ask_question(request: QuestionRequest):
    context = retrieve_context(request.question)
    prompt = build_rag_prompt(request.question, context)
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "context_used": context[:500]
    }