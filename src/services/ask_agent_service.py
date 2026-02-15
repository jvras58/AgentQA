"""Módulo de serviço para construir
e configurar o agente com base na base de conhecimento e nas configurações definidas.
"""
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools

from src.core.config import settings


class AskAgentService:
    def __init__(self, knowledge_base):
        """Inicializa o serviço do agente com a base de conhecimento fornecida."""
        self.kb = knowledge_base

    def build(self) -> Agent:
        """Constrói e retorna uma instância do agente configurada."""
        tools = [DuckDuckGoTools()] if settings.enable_web_search else []

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
