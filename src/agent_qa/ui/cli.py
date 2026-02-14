"""CLI interativa do AgentQA.

Permite ao usuário:
  - Fazer perguntas ao agente (modo padrão)
  - Adicionar documentos à base de conhecimento via texto
  - Sair do loop interativo
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge


from agent_qa.infra.seed_knowledge import add_document

# ── Constantes de UI ─────────────────────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════╗
║              🤖  AgentQA – CLI                   ║
╠══════════════════════════════════════════════════╣
║  Comandos:                                       ║
║    /add   → Adicionar documento à base           ║
║    /docs  → Listar comandos de documentos        ║
║    /help  → Mostrar esta ajuda                   ║
║    /quit  → Sair                                 ║
║                                                  ║
║  Ou simplesmente digite sua pergunta!            ║
╚══════════════════════════════════════════════════╝
"""

HELP_TEXT = """
Comandos disponíveis:
  /add <texto>  — Insere um documento de texto na base de conhecimento.
                   Ex: /add O Brasil foi descoberto em 1500 por Pedro Álvares Cabral.
  /add          — Sem texto: abre modo de inserção multilinha (termine com linha vazia).
  /docs         — Mostra ajuda sobre inserção de documentos.
  /help         — Mostra esta ajuda.
  /quit         — Encerra o programa.

Qualquer outra entrada é tratada como pergunta para o agente.
"""

DOCS_HELP = """
📄 Inserção de documentos:

  • Inline:    /add O PIB do Brasil em 2024 foi de 2.2 trilhões USD.
  • Multilinha: digite /add (sem texto) e cole várias linhas.
                Finalize com uma linha em branco.

Os documentos são vetorizados e ficam disponíveis imediatamente para o agente.
"""


def _read_multiline() -> str:
    """Lê múltiplas linhas até o usuário enviar uma linha vazia."""
    print("  (cole o texto; finalize com uma linha vazia)")
    lines: list[str] = []
    while True:
        line = input("  ... ")
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def _handle_add(args: str, kb: Knowledge) -> None:
    """Processa o comando /add."""
    text = args.strip()
    if not text:
        text = _read_multiline()
    if not text.strip():
        print("  ⚠ Nenhum texto fornecido. Documento não adicionado.")
        return
    add_document(kb, text)
    print(f"  ✅ Documento adicionado ({len(text)} caracteres).")


def run_interactive(agent: Agent, kb: Knowledge) -> None:
    """Loop principal da CLI interativa."""
    print(BANNER)

    while True:
        try:
            user_input = input("\n🟢 Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Até mais!")
            break

        if not user_input:
            continue

        # ── Comandos especiais ────────────────────────────────
        lower = user_input.lower()

        if lower in ("/quit", "/exit", "/sair"):
            print("👋 Até mais!")
            break

        if lower == "/help":
            print(HELP_TEXT)
            continue

        if lower == "/docs":
            print(DOCS_HELP)
            continue

        if lower.startswith("/add"):
            _handle_add(user_input[4:], kb)
            continue

        # ── Pergunta ao agente ────────────────────────────────
        print()
        agent.print_response(user_input)
