"""Schemas para o módulo de geração de questões."""

from typing import List

from pydantic import BaseModel, Field


class Questao(BaseModel):
    enunciado: str = Field(..., description="O texto da pergunta")
    opcoes: List[str] = Field(
        ..., min_length=4, max_length=4, description="Lista com 4 opções"
    )
    resposta_correta: str = Field(..., description="A alternativa correta")
    explicacao: str = Field(..., description="Explicação do porquê da resposta")


class GenerateQuestionsRequest(BaseModel):
    topic: str = Field(..., description="O tema ou assunto das questões")
    num_questions: int = Field(default=3, ge=1, le=10)
    difficulty: str = Field(default="média")

class GenerateQuestionsResponse(BaseModel):
    questoes: List[Questao] = Field(..., description="Lista de questões geradas")
