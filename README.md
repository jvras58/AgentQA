# AgentQA - Sistema de Perguntas e Respostas com IA

Sistema de perguntas e respostas baseado em documentos com Retrieval-Augmented Generation (RAG), usando o framework [Agno](https://docs.agno.com/), modelos locais via Ollama e base vetorial LanceDB.

## Funcionalidades

- **Agente QA com RAG**: Responde perguntas baseadas em documentos da base de conhecimento.
- **CLI Interativa**: Faça perguntas e adicione documentos via texto diretamente no terminal.
- **Base Vetorial Local**: LanceDB para armazenar embeddings sem precisar de servidor externo.
- **Embeddings Locais**: Ollama + `nomic-embed-text` — sem dependência de APIs pagas.
- **Memória Persistente**: Histórico de conversas em SQLite.
- **Busca Web** (opcional): DuckDuckGo integrado.
- **Configuração via Env Vars**: Todas as configs podem ser sobrescritas por variáveis de ambiente.

## Pré-requisitos

1. **Python** ≥ 3.12
2. **Ollama** instalado ([ollama.com](https://ollama.com/)):
   ```bash
   ollama pull llama3.1          # LLM principal
   ollama pull nomic-embed-text  # Embeddings
   ```
3. **uv** (recomendado) ou pip.

## Instalação

```bash
# Clone o repositório
git clone <repo-url> && cd AgentQA

# Instale as dependências
uv sync

# (Opcional) Copie e edite as variáveis de ambiente
cp .env.example .env
```

## Como Usar

### CLI Interativa (modo padrão)

```bash
uv run main.py
```

### Populando a base com dados de exemplo

```bash
uv run main.py --seed
```

### Pergunta única (modo não-interativo)

```bash
uv run main.py --ask "Qual é a capital da França?"
```

### Comandos dentro da CLI

| Comando        | Descrição                                      |
|----------------|-------------------------------------------------|
| `/add <texto>` | Adiciona documento inline à base de conhecimento |
| `/add`         | Modo multilinha — cole texto e finalize com linha vazia |
| `/docs`        | Ajuda sobre inserção de documentos              |
| `/help`        | Mostra ajuda geral                              |
| `/quit`        | Sair                                            |

## Estrutura do Projeto

```
AgentQA/
├── main.py                  # Entrypoint — CLI args e orquestração
├── agent_qa/
│   ├── __init__.py
│   ├── config.py            # Configurações centralizadas (env vars)
│   ├── agent.py             # Fábrica do agente (Agent + tools)
│   ├── knowledge.py         # Gerenciamento da base RAG
│   └── cli.py               # Loop interativo (perguntas + /add docs)
├── .env.example             # Variáveis de ambiente de exemplo
├── pyproject.toml
├── tmp/                     # Dados de runtime (LanceDB, SQLite)
└── README.md
```

## Detalhes da Implementação

### Escolha da Base Vetorial
Poderíamos usar o PgVector (PostgreSQL) ou ChromaDB, mas o LanceDB é super leve e fácil de usar localmente, sem precisar de um servidor. Conseguimos usar o OllamaEmbedder para criar os vetores de embedding usando um modelo local da Ollama, como o `nomic-embed-text`, que é gratuito e open-source. O LanceDB é ótimo para prototipagem rápida e pequenos projetos, e tem uma API bem simples para inserir e buscar dados. Ele armazena os vetores de embedding junto com o conteúdo original, o que facilita a recuperação de informações relevantes durante as conversas do agente. Além disso, o LanceDB é super rápido e eficiente, mesmo com um grande número de documentos, graças à sua estrutura otimizada para buscas vetoriais.

### Configuração dos Embeddings
O modelo `nomic-embed-text` gera embeddings de 768 dimensões, mas o LanceDB pode esperar 4096 por padrão. Por isso, definimos explicitamente `dimensions=768` no `OllamaEmbedder` para garantir compatibilidade.

### Modelo de Linguagem
Usamos o `llama3.1` como LLM local via Ollama, pois não conseguimos usar ferramentas (tools) com modelos pequenos (SMLs) como o `phi3`. O `llama3.1` é ótimo para RAG e tem um custo super baixo rodando localmente.

### Ferramentas e Memória
- As ferramentas como DuckDuckGo são opcionais para buscas na web.
- O histórico de conversas é armazenado em SQLite para memória persistente, com até 3 execuções anteriores incluídas no contexto.

### Dados de Exemplo
Os dados inseridos na base de conhecimento são exemplos variados (fáceis, médios e difíceis) para testar o RAG.

## Problemas Conhecidos

### Uso de Modelos Pequenos (SMLs) com Tools

O modelo `phi3` não suporta o uso de ferramentas (tools) no Agno, conforme a documentação. Para usar modelos menores localmente, considere alternativas como:

- **phi4** ou **qwen2.5-7b**: Modelos pequenos mas poderosos.
- **Provedores Locais**: Ollama, LM Studio, LlamaCpp ou VLLM.

Exemplo de uso com LM Studio:

```python
from agno.agent import Agent
from agno.models.lmstudio import LMStudio

agent = Agent(
    model=LMStudio(id="qwen2.5-7b-instruct-1m"),
    markdown=True,
)
agent.print_response("Olá!")
```

Certifique-se de que o modelo suporte tools se precisar dessa funcionalidade.

### Instalação obrigatória de pacotes/libs

Embora o projeto utilize modelos locais via Ollama (evitando dependências de APIs externas como OpenAI), o Agno requer algumas bibliotecas como dependências obrigatórias. Mesmo que não sejam usadas diretamente no código, elas são necessárias para o funcionamento do framework:

- `"openai"`: Biblioteca para integração com OpenAI, mas não utilizada aqui, pois optamos por modelos locais.
- `"sqlalchemy"`: ORM para bancos de dados, usado internamente pelo Agno para gerenciar o histórico e outras funcionalidades.

Essas dependências são instaladas automaticamente ao executar `pip install agno` ou `uv add agno`. Se preferir instalar manualmente:

```
pip install openai sqlalchemy
```

Ou com `uv`:

```
uv add openai sqlalchemy
```

## Referências da Documentação do Agno

- [Ferramentas de Busca - DuckDuckGo](https://docs.agno.com/tools/toolkits/search/duckduckgo)
- [Ferramentas de Busca - Brave Search](https://docs.agno.com/tools/toolkits/search/bravesearch)
- [LanceDB - Vector Databases](https://docs.agno.com/cookbook/knowledge/vector-databases)
- [LanceDB Overview](https://docs.agno.com/knowledge/vector-stores/lancedb/overview)
- [Histórico de Chat](https://docs.agno.com/database/chat-history)
- [Gerenciamento de Sessões](https://docs.agno.com/sessions/history-management)
- [Histórico do Agente](https://docs.agno.com/history/agent/overview)
- [Modelos Locais com Ollama](https://docs.agno.com/models/ollama)
- [Modelos com LM Studio](https://docs.agno.com/models/lmstudio)

Para mais informações, visite a [documentação oficial do Agno](https://docs.agno.com/).

