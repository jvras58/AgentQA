"""Rotas do módulo /ask."""

from agno.agent import Agent
from fastapi import APIRouter, Depends

from src.api.ask.controller import handle_ask
from src.api.ask.schemas import AskRequest, AskResponse
from src.api.deps import get_ask_agent

router = APIRouter(prefix="/ask", tags=["Ask"])


@router.post("", response_model=AskResponse)
def ask_question(
    req: AskRequest,
    agent: Agent = Depends(get_ask_agent),
):
    """Recebe uma pergunta e retorna a resposta do agente."""
    answer = handle_ask(agent, req.question)
    return AskResponse(answer=answer)
