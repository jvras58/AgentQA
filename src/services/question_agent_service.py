"""Módulo de serviço para construir o agente gerador de questões."""
from agno.agent import Agent
from agno.models.ollama import Ollama

from src.core.config import settings


class QuestionAgentService:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def build(self) -> Agent:
        """Constrói um agente especializado em criar questões com base nos documentos."""
        return Agent(
            model=Ollama(id=settings.llm_model, host=settings.ollama_host),
            knowledge=self.kb,
            search_knowledge=True,
            description="Você é um professor e avaliador especialista em criar questões baseadas em documentos de referência.",
            instructions=[
                "Use as informações da base de conhecimento para gerar as questões.",
                "Sempre forneça a resposta correta e uma breve explicação no final de cada questão.",
                "Se não encontrar informações suficientes na base sobre o tema solicitado, avise o usuário.",
                "Formate a saída em Markdown usando títulos, listas e negrito para facilitar a leitura."
            ],
            markdown=settings.markdown,
            debug_mode=settings.debug_mode,
        )
