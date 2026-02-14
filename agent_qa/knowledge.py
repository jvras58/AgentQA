"""Gerenciamento da base de conhecimento (Knowledge Base).

Responsável por criar, popular e expor a instância de Knowledge
usada pelo agente para RAG.
"""

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.vectordb.lancedb import LanceDb

from agent_qa.config import AgentConfig


def create_knowledge(config: AgentConfig) -> Knowledge:
    """Cria e retorna uma instância de Knowledge configurada."""
    vector_db = LanceDb(
        table_name=config.vector_db.table_name,
        uri=config.vector_db.uri,
        embedder=OllamaEmbedder(
            id=config.embedder.model_id,
            dimensions=config.embedder.dimensions,
        ),
    )
    return Knowledge(vector_db=vector_db)


def seed_knowledge(kb: Knowledge, documents: list[str] | None = None) -> None:
    """Insere documentos iniciais (seed) na base de conhecimento.

    Args:
        kb: Instância de Knowledge já configurada.
        documents: Lista de textos para inserir. Se None, usa o dataset padrão.
    """
    if documents is None:
        documents = [
            "capital França: Paris. Easy.",
            "Média 10+20+30=20. Medium.",
            "João 1990→2010 RJ: 20 anos. Hard.",
        ]

    for doc in documents:
        kb.insert(text_content=doc)


def add_document(kb: Knowledge, text: str) -> None:
    """Adiciona um único documento à base de conhecimento.

    Args:
        kb: Instância de Knowledge já configurada.
        text: Conteúdo textual a ser inserido.
    """
    kb.insert(text_content=text)
