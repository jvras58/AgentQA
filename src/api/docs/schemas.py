"""Schemas de request/response para o endpoint /docs (base de conhecimento)."""

from pydantic import BaseModel, Field


class AddDocumentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto do documento a ser adicionado à base de conhecimento.")


class AddDocumentResponse(BaseModel):
    status: str
    message: str
