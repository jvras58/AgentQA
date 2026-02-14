import argparse

from src.infra.knowledge import get_knowledge_base
from src.infra.seed_knowledge import seed_knowledge
from src.services.agent_service import AgentService
from src.ui.cli import run_interactive


def main():
    parser = argparse.ArgumentParser(description="AgentQA CLI")
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--ask", type=str)
    args = parser.parse_args()

    kb = get_knowledge_base()
    if args.seed:
        seed_knowledge(kb)

    agent = AgentService(kb).build()

    if args.ask:
        agent.print_response(args.ask)
    else:
        run_interactive(agent, kb)


if __name__ == "__main__":
    main()
