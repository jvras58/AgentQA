"""Testes para o endpoint POST /questions/generate."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.questions.controller import handle_generate_questions


class TestQuestionsEndpoint:
    """Testes de integração para /questions/generate."""

    def test_generate_questions_success(self, client, mock_question_agent):
        """Deve gerar questões com sucesso."""
        response = client.post("/questions/generate", json={
            "topic": "Geografia",
            "num_questions": 1,
            "difficulty": "fácil"
        })

        assert response.status_code == 200
        data = response.json()
        assert "questoes" in data
        assert len(data["questoes"]) >= 1
        mock_question_agent.arun.assert_awaited_once()

    def test_generate_questions_empty_topic_returns_400(self, client):
        """Deve retornar 400 para tópico vazio."""
        response = client.post("/questions/generate", json={
            "topic": "   ",
            "num_questions": 1,
            "difficulty": "fácil"
        })

        assert response.status_code == 400

    def test_generate_questions_invalid_num(self, client):
        """Deve retornar 422 para num_questions fora do range."""
        response = client.post("/questions/generate", json={
            "topic": "Ciência",
            "num_questions": 50,
            "difficulty": "fácil"
        })

        assert response.status_code == 422


class TestQuestionsController:
    """Testes unitários do controller handle_generate_questions."""

    @pytest.mark.asyncio
    async def test_handle_generate_questions(self):

        agent = MagicMock()
        response_mock = MagicMock()
        response_mock.content = {
            "questoes": [{
                "enunciado": "Pergunta?",
                "opcoes": ["A", "B", "C", "D"],
                "resposta_correta": "A",
                "explicacao": "Porque sim."
            }]
        }
        agent.arun = AsyncMock(return_value=response_mock)

        result = await handle_generate_questions(agent, "Tema", 1, "fácil")
        assert "questoes" in result
        assert len(result["questoes"]) == 1
        agent.arun.assert_awaited_once()
