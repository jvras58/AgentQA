"""AgentQA — Entrypoint principal.

Uso:
    uv run main.py              → Inicia a CLI interativa
    uv run main.py --seed       → Popula a base com dados de exemplo e inicia
    uv run main.py --ask "..."  → Faz uma pergunta única e sai
"""

import argparse
import sys

from agent_qa.config import load_config
from agent_qa.knowledge import create_knowledge, seed_knowledge
from agent_qa.agent import create_agent
from agent_qa.cli import run_interactive


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AgentQA — Sistema de Perguntas e Respostas com IA"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Insere documentos de exemplo na base de conhecimento antes de iniciar.",
    )
    parser.add_argument(
        "--ask",
        type=str,
        default=None,
        help="Faz uma pergunta única ao agente e sai (modo não-interativo).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()

    # ── Knowledge base ────────────────────────────────────
    kb = create_knowledge(config)

    if args.seed:
        print("📚 Inserindo documentos de exemplo na base de conhecimento...")
        seed_knowledge(kb)
        print("✅ Base populada com sucesso.\n")

    # ── Agent ─────────────────────────────────────────────
    agent = create_agent(config, kb)

    # ── Modo de execução ──────────────────────────────────
    if args.ask:
        agent.print_response(args.ask)
        sys.exit(0)

    run_interactive(agent, kb)


if __name__ == "__main__":
    main()
