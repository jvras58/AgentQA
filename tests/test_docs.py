"""Testes para o endpoint POST /docs/add."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.api.docs.controller import handle_add_document


class TestDocsEndpoint:
    """Testes de integração para /docs/add."""

    def test_add_document_success(self, client, mock_knowledge_base):
        """Deve adicionar documento com sucesso."""
        response = client.post("/docs/add", json={"text": "Novo documento de teste."})

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "caracteres" in data["message"]
        mock_knowledge_base.ainsert.assert_awaited_once()

    def test_add_empty_document_returns_400(self, client):
        """Deve retornar 400 para documento vazio."""
        response = client.post("/docs/add", json={"text": "   "})

        assert response.status_code == 400


class TestDocsController:
    """Testes unitários do controller handle_add_document."""

    @pytest.mark.asyncio
    async def test_handle_add_document_inserts(self):

        kb = MagicMock()
        kb.ainsert = AsyncMock(return_value=None)

        result = await handle_add_document(kb, "Texto de teste")

        assert "14 caracteres" in result
        kb.ainsert.assert_awaited_once_with(
            text_content="Texto de teste", skip_if_exists=True
        )

    @pytest.mark.asyncio
    async def test_handle_add_document_empty_raises(self):

        kb = MagicMock()
        with pytest.raises(HTTPException) as exc_info:
            await handle_add_document(kb, "  ")

        assert exc_info.value.status_code == 400
