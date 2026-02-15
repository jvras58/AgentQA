"""Controller para o endpoint /query – lógica de negócio da base de conhecimento."""

from agno.knowledge.knowledge import Knowledge
from fastapi import HTTPException

from src.infra.knowledge import add_document


def handle_add_document(kb: Knowledge, text: str) -> str:
    """Adiciona um documento à base de conhecimento e retorna mensagem de sucesso."""
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="O texto do documento não pode estar vazio.",
        )

    add_document(kb, text)
    return f"Documento adicionado ({len(text)} caracteres)."
