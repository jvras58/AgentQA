"""Ponto de entrada da aplicação FastAPI AgentQA."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.deps import app_state
from src.api.router import api_router
from src.core.config import settings
from src.infra.knowledge import get_knowledge_base
from src.infra.logging import get_logger
from src.services.agent_service import AgentService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa a base de conhecimento e o agente no startup."""
    logger = get_logger("lifespan")
    logger.info("Inicializando knowledge base...")
    app_state.kb = get_knowledge_base()
    logger.info("Construindo agente (debug_mode=%s)...", settings.debug_mode)
    app_state.agent = AgentService(app_state.kb).build()
    logger.info("AgentQA pronto!")
    yield


app = FastAPI(
    title="AgentQA API",
    description="API para o sistema de perguntas e respostas com IA",
    lifespan=lifespan,
)

# ----------------------------------
#  APP CORSMiddleware
# ----------------------------------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

# ----------------------------------
#  Root endpoint health check
# ----------------------------------

@app.get("/")
def read_root():
    """Root endpoint to verify that the API is running."""
    return {"message": "Welcome to API!"}
