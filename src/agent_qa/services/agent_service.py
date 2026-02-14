from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
from agent_qa.core.config import settings


class AgentService:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def build(self) -> Agent:
        tools = [DuckDuckGoTools()] if settings.enable_web_search else []

        return Agent(
            model=Ollama(id=settings.llm_model),
            tools=tools,
            knowledge=self.kb,
            db=SqliteDb(db_file=settings.memory_db_path),
            add_history_to_context=True,
            num_history_runs=settings.history_runs,
            markdown=True,
        )
