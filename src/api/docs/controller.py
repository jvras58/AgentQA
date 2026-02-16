"""Controller para o endpoint /docs – lógica de negócio da base de conhecimento."""

from agno.knowledge.knowledge import Knowledge
from fastapi import HTTPException


async def handle_add_document(kb: Knowledge, text: str) -> str:
    if not text.strip():
        raise HTTPException(
            status_code=400, detail="O texto do documento não pode estar vazio."
        )

    await kb.ainsert(text_content=text, skip_if_exists=True)
    return f"Documento adicionado ({len(text)} caracteres)."
