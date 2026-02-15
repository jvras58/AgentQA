"""Controller para o endpoint de questões."""

from agno.agent import Agent
from fastapi import HTTPException


def handle_generate_questions(
    agent: Agent, topic: str, num_questions: int, difficulty: str
) -> str:
    """Monta o prompt e executa a geração de questões no agente."""
    if not topic.strip():
        raise HTTPException(status_code=400, detail="O tema não pode estar vazio.")

    prompt = (
        f"Crie exatamente {num_questions} questões de múltipla escolha com nível de "
        f"dificuldade '{difficulty}' sobre o seguinte tema: {topic}."
    )

    response = agent.run(prompt)
    return response.content
