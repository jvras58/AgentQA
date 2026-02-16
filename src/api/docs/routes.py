"""Rotas do módulo /docs (gerenciamento da base de conhecimento)."""

from agno.knowledge.knowledge import Knowledge
from fastapi import APIRouter, Depends

from src.api.deps import get_knowledge_base
from src.api.docs.controller import handle_add_document
from src.api.docs.schemas import AddDocumentRequest, AddDocumentResponse

router = APIRouter(prefix="/docs", tags=["Knowledge Base"])


@router.post("/add", response_model=AddDocumentResponse)
async def add_knowledge(
    req: AddDocumentRequest,
    kb: Knowledge = Depends(get_knowledge_base),
):
    """Adiciona um novo documento à base de conhecimento."""
    message = await handle_add_document(kb, req.text)
    return AddDocumentResponse(status="success", message=message)
