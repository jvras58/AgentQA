"""Dependências compartilhadas para injeção via FastAPI Depends."""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from fastapi import HTTPException


class AppState:
    """Armazena estado global inicializado no lifespan."""

    kb: Knowledge | None = None
    agent: Agent | None = None


app_state = AppState()


def get_knowledge_base() -> Knowledge:
    """Retorna a instância da base de conhecimento."""
    if app_state.kb is None:
        raise HTTPException(status_code=503, detail="Knowledge base não inicializada.")
    return app_state.kb


def get_agent() -> Agent:
    """Retorna a instância do agente."""
    if app_state.agent is None:
        raise HTTPException(status_code=503, detail="Agent não inicializado.")
    return app_state.agent
