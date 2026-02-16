# 🤖 AgentQA

Sistema de Perguntas e Respostas (QA) com IA utilizando **RAG (Retrieval-Augmented Generation)** local, implementado como uma API FastAPI.

## 📂 Estrutura de Pastas

- `src/core/`: Configurações globais e validação de ambiente com **Pydantic Settings**.
- `src/infra/`: Gerenciamento de persistência (LanceDB) e conhecimento.
- `src/services/`: Lógica de construção e orquestração dos Agentes.
- `src/api/`: Endpoints da API FastAPI.

## 🛠️ Instalação e Configuração

### Pré-requisitos
- [uv](https://github.com/astral-sh/uv) para gerenciamento de pacotes.
- **Para execução local**: [Ollama](https://ollama.ai/) rodando com os modelos:
  - `llama3.1` (LLM)
  - `nomic-embed-text` (Embeddings)
- **Para execução com Docker** (opcional): [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/).

Verifique se o Ollama está rodando e tem os modelos (para execução local):
```bash
ollama list
```
Se não tiver os modelos, baixe-os:
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### Dependências
Instale as dependências do projeto:
```bash
uv sync
```

### Configuração (.env)
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
LLM_MODEL=llama3.1
EMBEDDER_MODEL=nomic-embed-text
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
EMBEDDER_HOST=localhost
EMBEDDER_PORT=11434  # Mesmo host/porta para ambos, pois Ollama local serve múltiplos modelos
ENABLE_WEB_SEARCH=true
```

## 🚀 Como Executar

### Opção 1: Execução Local (Recomendado para Desenvolvimento)
Para iniciar o servidor FastAPI:
```bash
make run
```
Ou diretamente:
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Para carregar os dados de exemplo (seed) antes de iniciar:
```bash
make seed
```

### Opção 2: Execução Local com Ollama em Docker (Para quem não tem Ollama instalado)
Use os contêineres Docker para os modelos Ollama, mas execute a aplicação localmente.

1. **Inicie os serviços Ollama em background**:
   ```bash
   docker compose up -d llama-service embed-service
   ```
   Isso expõe o LLM na porta 11434 e o embedder na porta 11435.

2. **Configure o .env para Docker**:
   ```env
   OLLAMA_HOST=localhost
   OLLAMA_PORT=11434
   EMBEDDER_HOST=localhost
   EMBEDDER_PORT=11435
   ```

3. **Execute a aplicação**:
   ```bash
   make seed && make run
   ```

**Para parar os contêineres**: `docker compose down`.

### Opção 3: Execução com Docker (Para Produção ou Isolamento)
O projeto inclui configurações Docker para rodar os modelos Ollama em contêineres isolados.

#### Pré-requisitos para Docker
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.

#### Passos para Executar com Docker
1. **Construa e inicie os serviços Ollama**:
   ```bash
   docker compose up --build
   ```
   Isso criará dois contêineres:
   - `llama-service`: Modelo LLM (`llama3.1`) na porta 11434.
   - `embed-service`: Modelo de embeddings (`nomic-embed-text`) na porta 11435.

2. **Configure o .env para Docker**:
   Edite o .env para apontar para os nomes dos serviços na rede Docker:
   ```env
   OLLAMA_HOST=llama-service
   OLLAMA_PORT=11434
   EMBEDDER_HOST=embed-service
   EMBEDDER_PORT=11434  # Porta interna dos contêineres
   ```

3. **Execute a aplicação**:
   Com os contêineres rodando em background, execute a aplicação localmente:
   ```bash
   make seed && make run
   ```

**Nota**: Os modelos são baixados durante a construção das imagens, o que pode levar tempo na primeira execução. Para parar os contêineres: `docker compose down`.

### Sessão de Testes
Use os comandos abaixo para executar os testes do projeto:

```bash
# Rodar todos os testes
uv run pytest -v

# Rodar com cobertura
uv run pytest --cov=src --cov-report=term-missing

# Rodar só um módulo
uv run pytest tests/api/test_ask.py -v
```

## 📡 API Endpoints

A API está disponível em `http://localhost:8000` (ou conforme configurado).

- **GET /**: Health check da API.
- **POST /ask**: Faz uma pergunta ao agente. Corpo: `{"question": "Sua pergunta aqui"}`.
- **POST /questions/generate**: Cria questões baseado na base de conhecimento fornecida. Corpo: `{"topic": "Topico da Pergunta", "num_questions": 5, "difficulty": "Nivel de dificuldade"}`
- **POST /docs/add**: Adiciona um documento à base de conhecimento. Corpo: `{"text": "Conteúdo do documento"}`.

Use ferramentas como Postman, curl ou a documentação automática do FastAPI em docs para testar.

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

Alguns modelos como o `phi3` não suportam o uso de ferramentas (tools) no Agno, conforme a documentação. Para usar modelos menores localmente, considere alternativas como:

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
- [KnowledgeTools](https://docs.agno.com/tools/toolkits/others/knowledge)
- [Reasoning](https://docs.agno.com/reasoning/reasoning-tools)
- [Engenharia de Contexto](https://docs.agno.com/context/agent/overview)
- [Traga seu próprio aplicativo FastAPI](https://docs.agno.com/agent-os/custom-fastapi/overview)
- [O que é o AgentOS](https://docs.agno.com/agent-os/introduction)
- [Execute seu AgentOS](https://docs.agno.com/agent-os/run-your-os)


Para mais informações, visite a [documentação oficial do Agno](https://docs.agno.com/).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
