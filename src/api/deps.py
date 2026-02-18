"""Dependências compartilhadas para injeção via FastAPI Depends."""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from fastapi import Header, HTTPException, Query


class AppState:
    """Armazena estado global inicializado no lifespan.

    - `kb` mantém compatibilidade com o comportamento anterior (KB padrão).
    - `kbs` permite registrar múltiplas KBs nomeadas (por domínio).
    """

    kb: Knowledge | None = None
    kbs: dict[str, Knowledge] = {}
    ask_agent: Agent | None = None
    question_agent: Agent | None = None


app_state = AppState()


def get_knowledge_base(
    kb_name: str | None = Header(None, alias="X-KB"),
    kb_param: str | None = Query(None, alias="kb"),
) -> Knowledge:
    """Retorna a instância da base de conhecimento.

    Seleção por (ordem de prioridade): query param `?kb=NAME` -> header `X-KB: NAME` -> KB padrão.
    """

    def _to_str(v: object) -> str | None:
        return v if isinstance(v, str) else None

    name = _to_str(kb_param) or _to_str(kb_name)

    if name:
        kb = app_state.kbs.get(name)
        if kb is None and name == "default":
            kb = app_state.kb
        if kb is None:
            raise HTTPException(
                status_code=503, detail=f"Knowledge base '{name}' não encontrada."
            )
        return kb

    if app_state.kb is not None:
        return app_state.kb

    if len(app_state.kbs) == 1:
        return next(iter(app_state.kbs.values()))

    raise HTTPException(status_code=503, detail="Knowledge base não inicializada.")


def get_ask_agent() -> Agent:
    """Retorna a instância do agente de perguntas."""
    if app_state.ask_agent is None:
        raise HTTPException(status_code=503, detail="Ask Agent não inicializado.")
    return app_state.ask_agent


async def get_question_agent() -> Agent:
    """Retorna a instância do agente gerador de questões."""
    if app_state.question_agent is None:
        raise HTTPException(status_code=503, detail="Question Agent não inicializado.")
    return app_state.question_agent
