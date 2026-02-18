"""Módulo de serviço para construir
e configurar o agente com base na base de conhecimento e nas configurações definidas.
"""
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.knowledge import KnowledgeTools

from src.core.config import settings
from src.infra.knowledge import get_knowledge_base


class AskAgentService:
    def __init__(self, knowledge_base=None, table_name: str | None = "ask"):
        """Inicializa o serviço do agente.

        - Se `knowledge_base` for fornecida, será utilizada (compatibilidade).
        - Caso contrário, cria uma `Knowledge` específica para este agente
          usando `get_knowledge_base(table_name=...)`.
        """
        self.kb = knowledge_base or get_knowledge_base(table_name=table_name)

    def build(self) -> Agent:
        """Constrói e retorna uma instância do agente configurada."""
        knowledge_tools = KnowledgeTools(
            knowledge=self.kb,
            enable_think=True,
            enable_search=True,
            enable_analyze=True,
            add_instructions=True,
            add_few_shot=True,
        )

        tools = [knowledge_tools] + (
            [DuckDuckGoTools()] if settings.enable_web_search else []
        )

        return Agent(
            model=Ollama(id=settings.llm_model, host=settings.ollama_host),
            tools=tools,
            knowledge=self.kb,
            search_knowledge=True,
            db=SqliteDb(db_file=settings.memory_db_file),
            add_history_to_context=True,
            num_history_runs=settings.memory_history_runs,
            markdown=settings.markdown,
            debug_mode=settings.debug_mode,
        )
