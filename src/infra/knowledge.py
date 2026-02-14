"""Módulo de conhecimento para a aplicação AgentQA."""

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from src.core.config import settings


def get_knowledge_base() -> Knowledge:
    """Inicializa a base de conhecimento usando LanceDB e OllamaEmbedder."""
    return Knowledge(
        vector_db=LanceDb(
            table_name=settings.vector_db_table,
            uri=settings.vector_db_uri,
            embedder=OllamaEmbedder(
                id=settings.embedder_model, dimensions=settings.embedder_dims, host=settings.embedder_host, port=settings.embedder_port
            ),
        )
    )

def add_document(kb: Knowledge, text: str) -> None:
    """Adiciona um único documento txt à base."""
    kb.insert(text_content=text)
