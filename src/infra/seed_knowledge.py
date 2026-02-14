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


def add_document(kb: Knowledge, text: str) -> None:
    """Adiciona um único documento txt à base."""
    kb.insert(text_content=text)
