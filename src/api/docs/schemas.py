"""Schemas de request/response para o endpoint /docs (base de conhecimento)."""

from typing import List, Optional

from pydantic import BaseModel, Field


class AddDocumentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto do documento a ser adicionado à base de conhecimento.")
    table: Optional[str] = Field(
        None,
        description="Nome da tabela (opcional). Se informado, o documento será adicionado nessa tabela; caso contrário usa a KB padrão.",
    )


class AddDocumentResponse(BaseModel):
    status: str
    message: str


class TablesListResponse(BaseModel):
    tables: List[str] = Field(
        ...,
        description="Lista de tabelas vetoriais disponíveis no diretório do LanceDB.",
    )
