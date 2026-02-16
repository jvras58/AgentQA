"""Controller para o endpoint de questões."""

from agno.agent import Agent
from fastapi import HTTPException

from src.api.questions.schemas import GenerateQuestionsResponse


def handle_generate_questions(
    agent: Agent, topic: str, num_questions: int, difficulty: str
) -> GenerateQuestionsResponse:
    """Monta o prompt e executa a geração de questões no agente."""
    if not topic.strip():
        raise HTTPException(status_code=400, detail="O tema não pode estar vazio.")

    prompt = (
        f"Crie exatamente {num_questions} questões de múltipla escolha com nível de "
        f"dificuldade '{difficulty}' sobre o seguinte tema: {topic}."
    )

    response = agent.run(prompt)
    return response.content
