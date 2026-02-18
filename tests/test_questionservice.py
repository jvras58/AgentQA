"""Testes para o QuestionAgentService."""

from unittest.mock import MagicMock, patch

from src.services.question_agent_service import QuestionAgentService


class TestQuestionAgentService:
    @patch("src.services.question_agent_service.Agent")
    @patch("src.services.question_agent_service.Ollama")
    @patch("src.services.question_agent_service.KnowledgeTools")
    @patch("src.services.question_agent_service.load_prompts_from_yaml")
    def test_build_creates_agent_with_prompts(
        self, mock_load_yaml, mock_kt, mock_ollama, mock_agent
    ):
        """Deve construir agente carregando prompts do YAML."""
        mock_load_yaml.return_value = {
            "description": "Descrição teste",
            "instructions": ["Instrução 1"]
        }
        kb = MagicMock()
        service = QuestionAgentService(kb)

        with patch("src.services.question_agent_service.settings") as mock_settings:
            mock_settings.llm_model = "llama3.1"
            mock_settings.ollama_host = "localhost"
            mock_settings.debug_mode = False

            agent = service.build()
            assert agent is not None

        mock_load_yaml.assert_called_once_with("question_agent.yaml")
        mock_agent.assert_called_once()

    def test_init_uses_table_name_when_no_kb_provided(self):
        """Ao inicializar sem `knowledge_base`, deve chamar `get_knowledge_base(table_name=...)`."""

        with patch(
            "src.services.question_agent_service.get_knowledge_base"
        ) as mock_get_kb:
            mock_kb = MagicMock()
            mock_get_kb.return_value = mock_kb

            service = QuestionAgentService(None, table_name="faqs")

            mock_get_kb.assert_called_once_with(table_name="faqs")
            assert service.kb is mock_kb

    def test_init_keeps_provided_kb(self):
        kb = MagicMock()
        service = QuestionAgentService(kb)
        assert service.kb is kb
