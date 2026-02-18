"""Testes para as dependências de injeção."""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.api.deps import (
    app_state,
    get_ask_agent,
    get_knowledge_base,
    get_question_agent,
)


class TestDeps:
    def test_get_knowledge_base_raises_when_none(self):
        original_kb = app_state.kb
        original_kbs = dict(app_state.kbs)
        app_state.kb = None
        app_state.kbs.clear()

        with pytest.raises(HTTPException) as exc_info:
            get_knowledge_base()

        assert exc_info.value.status_code == 503

        app_state.kb = original_kb
        app_state.kbs.update(original_kbs)

    def test_get_knowledge_base_returns_named_kb(self):

        original_kb = app_state.kb
        original_kbs = dict(app_state.kbs)

        mock_kb = MagicMock()
        app_state.kbs["recipes"] = mock_kb
        app_state.kb = None

        try:
            kb = get_knowledge_base(kb_name="recipes")
            assert kb is mock_kb
        finally:
            app_state.kb = original_kb
            app_state.kbs.clear()
            app_state.kbs.update(original_kbs)

    def test_get_knowledge_base_raises_when_unknown_name(self):
        original_kb = app_state.kb
        original_kbs = dict(app_state.kbs)

        app_state.kb = None
        app_state.kbs.clear()
        app_state.kbs["only"] = object()

        with pytest.raises(HTTPException) as exc_info:
            get_knowledge_base(kb_name="does_not_exist")

        assert exc_info.value.status_code == 503

        app_state.kb = original_kb
        app_state.kbs.clear()
        app_state.kbs.update(original_kbs)

    def test_get_ask_agent_raises_when_none(self):
        original = app_state.ask_agent
        app_state.ask_agent = None

        with pytest.raises(HTTPException) as exc_info:
            get_ask_agent()

        assert exc_info.value.status_code == 503
        app_state.ask_agent = original

    @pytest.mark.asyncio
    async def test_get_question_agent_raises_when_none(self):
        original = app_state.question_agent
        app_state.question_agent = None

        with pytest.raises(HTTPException) as exc_info:
            await get_question_agent()

        assert exc_info.value.status_code == 503
        app_state.question_agent = original
