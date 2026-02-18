"""Módulo de conhecimento para a aplicação AgentQA."""

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from src.core.config import settings


def get_knowledge_base(table_name: str | None = None) -> Knowledge:
    """Inicializa a base de conhecimento usando LanceDB e OllamaEmbedder.

    Permite criar/retornar uma Knowledge usando um `table_name` diferente
    (útil para ter múltiplas KBs isoladas dentro do mesmo LanceDB).
    Se `table_name` não for informado, usa o valor padrão em `settings`.
    """
    table = table_name or settings.vector_db_table
    return Knowledge(
        vector_db=LanceDb(
            table_name=table,
            uri=settings.vector_db_uri,
            embedder=OllamaEmbedder(
                id=settings.embedder_model,
                dimensions=settings.embedder_dimensions,
                host=f"{settings.embedder_host}:{settings.embedder_port}",
            ),
        )
    )
