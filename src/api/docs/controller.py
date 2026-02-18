"""Controller para o endpoint /docs – lógica de negócio da base de conhecimento."""

from pathlib import Path
from typing import List

from agno.knowledge.knowledge import Knowledge
from fastapi import HTTPException

from src.core.config import settings


async def handle_add_document(kb: Knowledge, text: str) -> str:
    if not text.strip():
        raise HTTPException(
            status_code=400, detail="O texto do documento não pode estar vazio."
        )

    await kb.ainsert(text_content=text, skip_if_exists=True)
    return f"Documento adicionado ({len(text)} caracteres)."


def list_tables() -> List[str]:
    """Retorna lista ordenada de tabelas (sem sufixo '.lance') existentes no LanceDB.

    - Mantém a lógica de filesystem aqui (controller), pois a listagem é
      uma concernência da API/controle — não da construção da KB.
    - Retorna lista vazia se o diretório não existir.
    """
    db_path = Path(settings.vector_db_uri)
    if not db_path.exists() or not db_path.is_dir():
        return []

    tables: List[str] = []
    for child in db_path.iterdir():
        if child.is_dir() and child.name.endswith(".lance"):
            tables.append(child.name[: -len(".lance")])

    return sorted(tables)
