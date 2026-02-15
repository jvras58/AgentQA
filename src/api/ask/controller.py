"""Controller para o endpoint /ask – lógica de negócio isolada da rota."""

from agno.agent import Agent
from fastapi import HTTPException


def handle_ask(agent: Agent, question: str) -> str:
    """Executa a pergunta no agente e retorna o conteúdo da resposta."""
    if not question.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

    response = agent.run(question)
    return response.content
