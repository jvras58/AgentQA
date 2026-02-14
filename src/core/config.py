from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # LLM & Embeddings (Ollama)
    llm_model: str = "llama3.1"
    embedder_model: str = "nomic-embed-text"
    embedder_dims: int = 768

    # Vector DB (LanceDB)
    vector_db_uri: str = str(BASE_DIR / "tmp" / "lancedb")
    vector_db_table: str = "docs"

    # Memory (SQLite)
    memory_db_path: str = str(BASE_DIR / "tmp" / "agent.db")
    history_runs: int = 3

    # Features
    enable_web_search: bool = True
    debug_mode: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
