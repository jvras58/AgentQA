from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.knowledge import KnowledgeTools

from src.core.config import settings


class QuestionAgentService:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def build(self) -> Agent:
        knowledge_tools = KnowledgeTools(
            knowledge=self.kb,
            enable_think=True,
            enable_search=True,
            enable_analyze=True,
            add_instructions=True,
            add_few_shot=True,
        )

        return Agent(
            model=Ollama(id=settings.llm_model, host=settings.ollama_host),
            tools=[knowledge_tools],
            description="Você é um professor especialista em criar questões baseadas em documentos.",
            instructions=[
                "Use as informações da base de conhecimento para gerar as questões.",
                "Sempre forneça a resposta correta e uma breve explicação.",
                "Se não encontrar informações suficientes, avise o usuário.",
                "Formate a saída em Markdown.",
            ],
            markdown=settings.markdown,
            debug_mode=settings.debug_mode,
        )
