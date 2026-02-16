"""Testes para o script de seed."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.scripts.seed_knowledge import seed_knowledge


class TestSeedKnowledge:
    @pytest.mark.asyncio
    async def test_seed_inserts_documents(self):
        """Deve inserir 3 documentos na base."""
        kb = MagicMock()
        kb.ainsert = AsyncMock(return_value=None)

        await seed_knowledge(kb)

        assert kb.ainsert.await_count == 3
        kb.ainsert.assert_any_await(
            text_content="A capital da França é Paris.",
            name="doc_1",
            skip_if_exists=True,
        )
