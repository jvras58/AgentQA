"""Módulo para popular a base de conhecimento com dados iniciais de exemplo."""

import asyncio

from agno.knowledge.knowledge import Knowledge

from src.infra.knowledge import get_knowledge_base
from src.infra.logging import get_logger

logger = get_logger("seed_knowledge")

async def seed_knowledge(kb: Knowledge) -> None:
    """Popula a base com dados iniciais de exemplo."""
    documents = [
        "A capital da França é Paris.",
        "O framework Agno era anteriormente conhecido como Phidata.",
        "LanceDB é um banco de dados vetorial serverless para IA.",
    ]
    
    logger.info("Inserindo documentos na base de conhecimento...")
    for i, doc in enumerate(documents, start=1):
        logger.info(f"Inserindo: {doc}")
        await kb.ainsert(text_content=doc, name=f"doc_{i}", skip_if_exists=True)
    logger.info("Base de conhecimento populada com sucesso!")


if __name__ == "__main__":
    kb = get_knowledge_base()
    asyncio.run(seed_knowledge(kb))
