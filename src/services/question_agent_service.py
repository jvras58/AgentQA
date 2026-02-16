from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.knowledge import KnowledgeTools

from src.core.config import settings
from utils.load_yaml import load_question_agent_prompts


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

        prompts = load_question_agent_prompts()

        return Agent(
            model=Ollama(id=settings.llm_model, host=settings.ollama_host),
            tools=[knowledge_tools],
            description=prompts["description"],
            instructions=prompts["instructions"],
            markdown=settings.markdown,
            debug_mode=settings.debug_mode,
        )
