"""Rotas do módulo /questions."""

from agno.agent import Agent
from fastapi import APIRouter, Depends

from src.api.deps import get_question_agent
from src.api.questions.controller import handle_generate_questions
from src.api.questions.schemas import (
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
)

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/generate", response_model=GenerateQuestionsResponse)
def generate_questions(
    req: GenerateQuestionsRequest,
    agent: Agent = Depends(get_question_agent),
):
    """Gera questões com base no tema, quantidade e dificuldade fornecidos."""
    content = handle_generate_questions(
        agent, req.topic, req.num_questions, req.difficulty
    )
    return GenerateQuestionsResponse(content=content)
