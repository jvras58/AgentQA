"""Testes para o endpoint POST /ask."""

from unittest.mock import AsyncMock, MagicMock

import pytest


class TestAskEndpoint:
    """Testes de integração para /ask."""

    def test_ask_returns_answer(self, client, mock_ask_agent):
        """Deve retornar uma resposta do agente."""
        response = client.post("/ask", json={"question": "Qual a capital da França?"})

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "A capital da França é Paris."
        mock_ask_agent.arun.assert_awaited_once_with("Qual a capital da França?")

    def test_ask_empty_question_returns_400(self, client):
        """Deve retornar 400 para pergunta vazia."""
        response = client.post("/ask", json={"question": "   "})

        assert response.status_code == 400

    def test_ask_missing_question_returns_422(self, client):
        """Deve retornar 422 para body sem o campo question."""
        response = client.post("/ask", json={})

        assert response.status_code == 422


class TestAskController:
    """Testes unitários do controller handle_ask."""

    @pytest.mark.asyncio
    async def test_handle_ask_calls_agent(self):
        from src.api.ask.controller import handle_ask

        agent = MagicMock()
        response_mock = MagicMock()
        response_mock.content = "Resposta mockada"
        agent.arun = AsyncMock(return_value=response_mock)

        result = await handle_ask(agent, "Pergunta teste")

        assert result == "Resposta mockada"
        agent.arun.assert_awaited_once_with("Pergunta teste")

    @pytest.mark.asyncio
    async def test_handle_ask_empty_raises_http_exception(self):
        from fastapi import HTTPException

        from src.api.ask.controller import handle_ask

        agent = MagicMock()
        with pytest.raises(HTTPException) as exc_info:
            await handle_ask(agent, "  ")

        assert exc_info.value.status_code == 400
