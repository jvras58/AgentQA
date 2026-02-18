"""Testes para o AskAgentService."""

from unittest.mock import MagicMock, patch

from src.services.ask_agent_service import AskAgentService


class TestAskAgentService:
    @patch("src.services.ask_agent_service.Agent")
    @patch("src.services.ask_agent_service.Ollama")
    @patch("src.services.ask_agent_service.SqliteDb")
    @patch("src.services.ask_agent_service.KnowledgeTools")
    @patch("src.services.ask_agent_service.DuckDuckGoTools")
    def test_build_creates_agent_with_web_search(
        self, mock_ddg, mock_kt, mock_sqlite, mock_ollama, mock_agent
    ):
        """Deve construir agente com DuckDuckGo quando web search está habilitado."""
        kb = MagicMock()
        service = AskAgentService(kb)

        with patch("src.services.ask_agent_service.settings") as mock_settings:
            mock_settings.enable_web_search = True
            mock_settings.llm_model = "llama3.1"
            mock_settings.ollama_host = "localhost"
            mock_settings.memory_db_file = "tmp/agent.db"
            mock_settings.memory_history_runs = 3
            mock_settings.markdown = True
            mock_settings.debug_mode = False

            agent = service.build()
            assert agent is not None

        mock_agent.assert_called_once()
        mock_ddg.assert_called_once()

    @patch("src.services.ask_agent_service.Agent")
    @patch("src.services.ask_agent_service.Ollama")
    @patch("src.services.ask_agent_service.SqliteDb")
    @patch("src.services.ask_agent_service.KnowledgeTools")
    def test_build_creates_agent_without_web_search(
        self, mock_kt, mock_sqlite, mock_ollama, mock_agent
    ):
        """Deve construir agente sem DuckDuckGo quando web search está desabilitado."""
        kb = MagicMock()
        service = AskAgentService(kb)

        with patch("src.services.ask_agent_service.settings") as mock_settings:
            mock_settings.enable_web_search = False
            mock_settings.llm_model = "llama3.1"
            mock_settings.ollama_host = "localhost"
            mock_settings.memory_db_file = "tmp/agent.db"
            mock_settings.memory_history_runs = 3
            mock_settings.markdown = True
            mock_settings.debug_mode = False

            agent = service.build()
            assert agent is not None

        mock_agent.assert_called_once()

    def test_init_uses_table_name_when_no_kb_provided(self):
        """Ao inicializar sem `knowledge_base`, deve chamar `get_knowledge_base(table_name=...)`."""

        with patch("src.services.ask_agent_service.get_knowledge_base") as mock_get_kb:
            mock_kb = MagicMock()
            mock_get_kb.return_value = mock_kb
            service = AskAgentService(None, table_name="recipes")

            mock_get_kb.assert_called_once_with(table_name="recipes")
            assert service.kb is mock_kb

    def test_init_keeps_provided_kb(self):
        kb = MagicMock()
        service = AskAgentService(kb)
        assert service.kb is kb
