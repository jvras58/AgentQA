"""Fábrica do agente QA.

Monta o Agent do Agno com todas as dependências injetadas
a partir da configuração centralizada.
"""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.db.sqlite import SqliteDb

from agent_qa.config import AgentConfig


def create_agent(config: AgentConfig, knowledge: Knowledge) -> Agent:
    """Cria e retorna o agente QA configurado.

    Args:
        config: Configuração centralizada do projeto.
        knowledge: Base de conhecimento já populada.

    Returns:
        Instância de Agent pronta para uso.
    """
    tools = []
    if config.enable_web_search:
        tools.append(DuckDuckGoTools())

    return Agent(
        model=Ollama(id=config.llm.model_id),
        tools=tools,
        knowledge=knowledge,
        db=SqliteDb(db_file=config.memory.db_file),
        add_history_to_context=True,
        num_history_runs=config.memory.num_history_runs,
        markdown=config.markdown,
    )
