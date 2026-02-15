"""Módulo de configuração central para a aplicação AgentQA.
Define as configurações para LLM, embeddings, banco de dados vetorial,
memória e recursos adicionais. Utiliza Pydantic para gerenciamento de configurações"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # LLM & Embeddings (Ollama)
    llm_model: str = "llama3.1"
    embedder_model: str = "nomic-embed-text"
    embedder_dimensions: int = Field(default=768, alias="EMBEDDER_DIMENSIONS")

    # Ollama hosts/ports
    ollama_host: str = "localhost"
    ollama_port: int = 11434
    embedder_host: str = "localhost"
    embedder_port: int = (
        11435  # Porta diferente para o embedder se rodar em um container separado
    )

    # Vector DB (LanceDB)
    vector_db_uri: str = str(BASE_DIR / "tmp" / "lancedb")
    vector_db_table: str = "docs"

    # Memory (SQLite)
    memory_db_file: str = Field(
        default=str(BASE_DIR / "tmp" / "agent.db"), alias="MEMORY_DB_FILE"
    )
    memory_history_runs: int = Field(default=3, alias="MEMORY_HISTORY_RUNS")

    # Features
    enable_web_search: bool = True
    debug_mode: bool = False
    markdown: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
