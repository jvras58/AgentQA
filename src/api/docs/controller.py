"""Controller para o endpoint /query – lógica de negócio da base de conhecimento."""

from agno.knowledge.knowledge import Knowledge
from fastapi import HTTPException


def handle_add_document(kb: Knowledge, text: str) -> str:
    """Adiciona um documento à base de conhecimento e retorna mensagem de sucesso."""
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="O texto do documento não pode estar vazio.",
        )

    kb.insert(text_content=text, skip_if_exists=True)
    return f"Documento adicionado ({len(text)} caracteres)."
