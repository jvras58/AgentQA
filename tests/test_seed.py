"""Testes para o script de seed."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.scripts.seed_knowledge import (
    QUESTIONS_DOCS,
    RAG_DOCS,
    seed_knowledge,
    seed_tables,
)


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

    @pytest.mark.asyncio
    async def test_seed_tables_populates_both(self, monkeypatch):
        """seed_tables deve popular as duas tabelas (questions e RAG)."""
        kb_q = MagicMock()
        kb_q.ainsert = AsyncMock(return_value=None)
        kb_r = MagicMock()
        kb_r.ainsert = AsyncMock(return_value=None)

        def fake_get_kb(table_name=None):
            return kb_q if table_name == "questions" else kb_r

        monkeypatch.setattr(
            "src.scripts.seed_knowledge.get_knowledge_base", fake_get_kb
        )

        await seed_tables(questions_table="questions", rag_table="ask")

        assert kb_q.ainsert.await_count == len(QUESTIONS_DOCS)
        assert kb_r.ainsert.await_count == len(RAG_DOCS)
