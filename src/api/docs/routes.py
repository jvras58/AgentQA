"""Rotas do módulo /docs (gerenciamento da base de conhecimento)."""

from agno.knowledge.knowledge import Knowledge
from fastapi import APIRouter, Depends

from src.api.deps import get_knowledge_base as get_default_kb
from src.api.docs.controller import handle_add_document, list_tables
from src.api.docs.schemas import (
    AddDocumentRequest,
    AddDocumentResponse,
    TablesListResponse,
)
from src.infra.knowledge import get_knowledge_base as infra_get_knowledge_base

router = APIRouter(prefix="/docs", tags=["Knowledge Base"])


@router.post("/add", response_model=AddDocumentResponse)
async def add_knowledge(
    req: AddDocumentRequest,
    default_kb: Knowledge = Depends(get_default_kb),
):
    """Adiciona um novo documento à base de conhecimento.

    - Se `table` estiver presente no body, será usada/criada uma KB para
      essa tabela (ex.: 'ask', 'questions', etc).
    - Caso contrário, usa a KB padrão injetada por dependência.
    """
    kb = infra_get_knowledge_base(table_name=req.table) if req.table else default_kb
    message = await handle_add_document(kb, req.text)
    return AddDocumentResponse(status="success", message=message)


@router.get("/tables", response_model=TablesListResponse)
def get_tables():
    """Retorna a lista de tabelas existentes no diretório do LanceDB."""
    tables = list_tables()
    return TablesListResponse(tables=tables)
