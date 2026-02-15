"""Schemas de request/response para o endpoint /ask."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pergunta a ser respondida pelo agente.")


class AskResponse(BaseModel):
    answer: str
