"""Configurações centralizadas do AgentQA.

Todas as constantes e parâmetros configuráveis ficam aqui.
Valores podem ser sobrescritos via variáveis de ambiente (.env).
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class EmbedderConfig:
    """Configurações do modelo de embeddings (Ollama)."""

    model_id: str = "nomic-embed-text"
    dimensions: int = 768  # nomic-embed-text gera 768 dimensões


@dataclass(frozen=True)
class VectorDbConfig:
    """Configurações do banco de dados vetorial (LanceDB)."""

    table_name: str = "docs"
    uri: str = str(BASE_DIR / "tmp" / "lancedb")


@dataclass(frozen=True)
class LlmConfig:
    """Configurações do modelo de linguagem (Ollama)."""

    model_id: str = "llama3.1"


@dataclass(frozen=True)
class MemoryConfig:
    """Configurações de memória / histórico de conversas."""

    db_file: str = str(BASE_DIR / "tmp" / "agent.db")
    num_history_runs: int = 3


@dataclass(frozen=True)
class AgentConfig:
    """Configuração agregada do agente — fonte única da verdade."""

    embedder: EmbedderConfig = field(default_factory=EmbedderConfig)
    vector_db: VectorDbConfig = field(default_factory=VectorDbConfig)
    llm: LlmConfig = field(default_factory=LlmConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    enable_web_search: bool = True
    markdown: bool = True


def load_config() -> AgentConfig:
    """Carrega a configuração, aplicando overrides de variáveis de ambiente."""
    return AgentConfig(
        embedder=EmbedderConfig(
            model_id=os.getenv("EMBEDDER_MODEL", EmbedderConfig.model_id),
            dimensions=int(
                os.getenv("EMBEDDER_DIMENSIONS", str(EmbedderConfig.dimensions))
            ),
        ),
        vector_db=VectorDbConfig(
            table_name=os.getenv("VECTOR_DB_TABLE", VectorDbConfig.table_name),
            uri=os.getenv("VECTOR_DB_URI", VectorDbConfig().uri),
        ),
        llm=LlmConfig(
            model_id=os.getenv("LLM_MODEL", LlmConfig.model_id),
        ),
        memory=MemoryConfig(
            db_file=os.getenv("MEMORY_DB_FILE", MemoryConfig().db_file),
            num_history_runs=int(
                os.getenv("MEMORY_HISTORY_RUNS", str(MemoryConfig.num_history_runs))
            ),
        ),
        enable_web_search=os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true",
        markdown=os.getenv("MARKDOWN", "true").lower() == "true",
    )
