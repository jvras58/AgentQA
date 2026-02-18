"""Módulo para popular a base de conhecimento com dados iniciais de exemplo.

Adições:
- Mantém a função `seed_knowledge(kb)` (compatibilidade com testes).
- Adiciona seed específico para duas tabelas (definidas por variáveis abaixo):
  * `QUESTIONS_TABLE` — exemplos/few-shot úteis para gerar questões.
  * `RAG_TABLE` — documentos factuais para RAG (responder perguntas).

Uso simples: editar as variáveis no topo se quiser mudar os nomes das tabelas.
"""

import asyncio
from typing import List

from agno.knowledge.knowledge import Knowledge

from src.infra.knowledge import get_knowledge_base
from src.infra.logging import get_logger

logger = get_logger("seed_knowledge")

# Nomes das tabelas que queremos popular
QUESTIONS_TABLE = "questions"
RAG_TABLE = "ask"

# --- Conteúdo de exemplo ---
# Seed focado em fornecer bons exemplos para o gerador de questões
QUESTIONS_DOCS: List[str] = [
    # Multiple-choice example
    (
        "Enunciado: O que é LanceDB?\n"
        "Tipo: multiple_choice\n"
        "Opções: (A) Banco relacional, (B) Banco vetorial, (C) Linguagem de programação, (D) Framework web\n"
        "Resposta: (B) Banco vetorial\n"
        "Explicação: LanceDB armazena e recupera embeddings para aplicações de IA."
    ),
    # Short-answer example
    (
        "Enunciado: Qual é a capital da França?\n"
        "Tipo: short_answer\n"
        "Resposta: Paris\n"
        "Explicação: Paris é a capital e maior cidade da França."
    ),
    # True/False example
    (
        "Enunciado: O framework Agno já foi conhecido como Phidata.\n"
        "Tipo: true_false\n"
        "Resposta: True\n"
        "Explicação: Histórico do projeto mencionado nos documentos do repositório."
    ),
    # Complexity / multi-step example
    (
        "Enunciado: Explique por que embeddings são úteis em sistemas de recuperação de informação.\n"
        "Tipo: explanatory\n"
        "Resposta: Embeddings transformam texto em vetores numéricos, permitindo buscas semânticas por similaridade.\n"
        "Explicação: Uso em RAG para encontrar trechos relevantes que respondam uma pergunta."
    ),
]

# Seed focado em fornecer conhecimento factual para RAG (respostas)
RAG_DOCS: List[str] = [
    (
        "A capital da França é Paris. Paris é uma cidade histórica conhecida por monumentos como a Torre Eiffel e o Louvre."
    ),
    (
        "LanceDB é um banco de dados vetorial que armazena embeddings e suporta consultas de similaridade, útil em pipelines RAG e sistemas de busca semântica."
    ),
    (
        "Agno é um framework fictício usado nos exemplos do projeto; ele demonstra como integrar modelos, ferramentas e uma knowledge base para construir agentes de QA."
    ),
    (
        "Boas práticas para RAG: 1) indexar documentos curtos e informativos; 2) adicionar metadados (quando possível); 3) atualizar a base regularmente para evitar informações obsoletas."
    ),
]


async def seed_knowledge(kb: Knowledge) -> None:
    """Mantém o comportamento original — insere 3 documentos na KB fornecida.

    (Preservado para compatibilidade com os testes existentes.)
    """
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


async def _seed_documents_in_kb(
    kb: Knowledge, documents: List[str], prefix: str = "doc"
) -> None:
    logger.info("Inserindo %d documentos (prefix=%s)...", len(documents), prefix)
    for i, doc in enumerate(documents, start=1):
        name = f"{prefix}_{i}"
        await kb.ainsert(text_content=doc, name=name, skip_if_exists=True)
    logger.info("Inserção concluída (prefix=%s).", prefix)


async def seed_tables(
    questions_table: str = QUESTIONS_TABLE, rag_table: str = RAG_TABLE
) -> None:
    """Popula explicitamente as duas tabelas definidas nas variáveis do topo.

    - `questions_table`: documentos/few-shot para gerar questões.
    - `rag_table`: documentos factuais para consulta RAG.
    """
    logger.info(
        "Iniciando seed para tabelas: questions=%s, rag=%s", questions_table, rag_table
    )

    q_kb = get_knowledge_base(table_name=questions_table)
    r_kb = get_knowledge_base(table_name=rag_table)

    await _seed_documents_in_kb(q_kb, QUESTIONS_DOCS, prefix="qdoc")
    await _seed_documents_in_kb(r_kb, RAG_DOCS, prefix="rdoc")

    logger.info("Seed para todas as tabelas concluído.")


if __name__ == "__main__":
    default_kb = get_knowledge_base()

    async def _main():
        await seed_knowledge(default_kb)
        await seed_tables()

    asyncio.run(_main())
