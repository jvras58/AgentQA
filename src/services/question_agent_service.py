from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.knowledge import KnowledgeTools

from src.api.questions.schemas import GenerateQuestionsResponse
from src.core.config import settings
from utils.load_yaml import load_prompts_from_yaml
from src.infra.knowledge import get_knowledge_base


class QuestionAgentService:
    def __init__(self, knowledge_base=None, table_name: str | None = "questions"):
        """Inicializa o QuestionAgentService.

        - Usa `knowledge_base` quando fornecida (compatibilidade).
        - Caso contrário cria uma KB específica para o agente com `table_name`.
        """
        self.kb = knowledge_base or get_knowledge_base(table_name=table_name)

    def build(self) -> Agent:
        knowledge_tools = KnowledgeTools(
            knowledge=self.kb,
            enable_think=True,
            enable_search=True,
            enable_analyze=True,
            add_instructions=True,
            add_few_shot=True,
        )

        prompts = load_prompts_from_yaml("question_agent.yaml")

        return Agent(
            model=Ollama(id=settings.llm_model, host=settings.ollama_host),
            tools=[knowledge_tools],
            description=prompts["description"],
            instructions=prompts["instructions"],
            output_schema=GenerateQuestionsResponse,
            markdown=False,
            debug_mode=settings.debug_mode,
        )
