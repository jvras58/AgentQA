"""Dependências compartilhadas para injeção via FastAPI Depends."""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge


class AppState:
    """Armazena estado global inicializado no lifespan."""

    kb: Knowledge | None = None
    agent: Agent | None = None


app_state = AppState()


def get_knowledge_base() -> Knowledge:
    """Retorna a instância da base de conhecimento."""
    assert app_state.kb is not None, "Knowledge base não inicializada."
    return app_state.kb


def get_agent() -> Agent:
    """Retorna a instância do agente."""
    assert app_state.agent is not None, "Agent não inicializado."
    return app_state.agent
