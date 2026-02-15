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
                id=settings.embedder_model,
                dimensions=settings.embedder_dimensions,
                host=f"{settings.embedder_host}:{settings.embedder_port}",
            ),
        )
    )
