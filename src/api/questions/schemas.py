"""Schemas para o módulo de geração de questões."""

from pydantic import BaseModel, Field


class GenerateQuestionsRequest(BaseModel):
    topic: str = Field(..., description="O tema ou assunto das questões")
    num_questions: int = Field(
        default=3, ge=1, le=10, description="Quantidade de questões a serem geradas"
    )
    difficulty: str = Field(
        default="média", description="Nível de dificuldade (ex: fácil, média, difícil)"
    )


class GenerateQuestionsResponse(BaseModel):
    content: str
