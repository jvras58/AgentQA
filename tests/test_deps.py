"""Testes para as dependências de injeção."""

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
        original = app_state.kb
        app_state.kb = None

        with pytest.raises(HTTPException) as exc_info:
            get_knowledge_base()

        assert exc_info.value.status_code == 503
        app_state.kb = original

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
