"""Fixtures globais para os testes do AgentQA."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.deps import app_state
from src.main import app


@pytest.fixture()
def mock_knowledge_base():
    """Mock da base de conhecimento (Knowledge)."""
    kb = MagicMock()
    kb.ainsert = AsyncMock(return_value=None)
    kb.search = AsyncMock(return_value=[
        {"content": "A capital da França é Paris.", "score": 0.95}
    ])
    return kb


@pytest.fixture()
def mock_ask_agent():
    """Mock do agente de perguntas."""
    agent = MagicMock()
    response = MagicMock()
    response.content = "A capital da França é Paris."
    agent.arun = AsyncMock(return_value=response)
    return agent


@pytest.fixture()
def mock_question_agent():
    """Mock do agente gerador de questões."""
    agent = MagicMock()
    response = MagicMock()
    response.content = {
        "questoes": [
            {
                "enunciado": "Qual é a capital da França?",
                "opcoes": ["Paris", "Londres", "Berlim", "Madrid"],
                "resposta_correta": "Paris",
                "explicacao": "Paris é a capital da França."
            }
        ]
    }
    agent.arun = AsyncMock(return_value=response)
    return agent


@pytest.fixture()
def configured_app_state(mock_knowledge_base, mock_ask_agent, mock_question_agent):
    """Injeta os mocks no app_state global."""
    original_kb = app_state.kb
    original_ask = app_state.ask_agent
    original_question = app_state.question_agent

    app_state.kb = mock_knowledge_base
    app_state.ask_agent = mock_ask_agent
    app_state.question_agent = mock_question_agent

    yield app_state

    # Restaura estado original
    app_state.kb = original_kb
    app_state.ask_agent = original_ask
    app_state.question_agent = original_question


@pytest.fixture()
def client(configured_app_state):
    """TestClient síncrono com o lifespan desligado (mocks já injetados)."""
    # Desativa o lifespan para não tentar conectar ao Ollama
    app.router.lifespan_context = _noop_lifespan
    return TestClient(app)


@pytest.fixture()
async def async_client(configured_app_state):
    """AsyncClient para testes assíncronos."""
    app.router.lifespan_context = _noop_lifespan
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@asynccontextmanager
async def _noop_lifespan(app):
    """Lifespan vazio — não inicializa Ollama nem knowledge base."""
    yield
