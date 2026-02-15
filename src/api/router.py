"""Router principal que agrega todas as sub-rotas da API."""

from fastapi import APIRouter

from src.api.ask.routes import router as ask_router
from src.api.docs.routes import router as docs_router
from src.api.questions.routes import router as questions_router

api_router = APIRouter()

api_router.include_router(ask_router)
api_router.include_router(docs_router)
api_router.include_router(questions_router)
