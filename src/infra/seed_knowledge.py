"""Módulo para popular a base de conhecimento com dados iniciais de exemplo."""

from agno.knowledge.knowledge import Knowledge


def seed_knowledge(kb: Knowledge) -> None:
    """Popula a base com dados iniciais de exemplo."""
    documents = [
        "A capital da França é Paris.",
        "O framework Agno era anteriormente conhecido como Phidata.",
        "LanceDB é um banco de dados vetorial serverless para IA.",
    ]
    for doc in documents:
        kb.insert(text_content=doc)
