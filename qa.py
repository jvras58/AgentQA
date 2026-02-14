from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.vectordb.lancedb import LanceDb

# Poderiamos usar o PgVector(PostgreSQL) ou ChromaDB, mas o LanceDB é super leve e fácil de usar localmente, sem precisar de um servidor. e conseguimos usar o OllamaEmbedder pra criar os vetores de embedding usando um modelo local da Ollama, como o nomic-embed-text, que é gratuito e open-source. O LanceDB é ótimo pra prototipagem rápida e pequenos projetos, e tem uma API bem simples pra inserir e buscar dados. Ele armazena os vetores de embedding junto com o conteúdo original, o que facilita a recuperação de informações relevantes durante as conversas do agente. Além disso, o LanceDB é super rápido e eficiente, mesmo com um grande número de documentos, graças à sua estrutura otimizada para buscas vetoriais.
knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="docs",
        uri="tmp/lancedb",
        embedder=OllamaEmbedder(
            id="nomic-embed-text",
            dimensions=768,  # Dimensão do embedding: O nomic-embed-text gera embeddings de 768 dimensões, mas o LanceDb está esperando 4096. Você precisa definir dimensions=768 no OllamaEmbedder
        ),  # ollama pull nomic-embed-text
    ),
)

# Seu dataset variado como knowledge (JSON/CSV/txt)
knowledge.insert(text_content="capital França: Paris. Easy.")
knowledge.insert(text_content="Média 10+20+30=20. Medium.")
knowledge.insert(text_content="João 1990→2010 RJ: 20 anos. Hard.")

# Agente QA com memória + RAG
agent = Agent(
    model=Ollama(
        id="llama3.1"
    ),  # Local LLM (ollama pull llama3.1) não conseguimos usar tools com sml como o phi3, por isso usamos o llama3.1 que é ótimo pra RAG e tem um custo super baixo rodando localmente
    tools=[DuckDuckGoTools()],  # Opcional pra web
    knowledge=knowledge,
    db=SqliteDb(db_file="agent.db"),  # Memória persistente de conversas
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# Rode!
response = agent.print_response(
    "Pergunta hard: João mudou pra onde e com quantos anos?"
)
print(response)
