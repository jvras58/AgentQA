# 🤖 AgentQA

Sistema de Perguntas e Respostas (QA) com IA utilizando **RAG (Retrieval-Augmented Generation)** local.

## 📂 Estrutura de Pastas

- `src/core/`: Configurações globais e validação de ambiente com **Pydantic Settings**.
- `src/infra/`: Gerenciamento de persistência (LanceDB) e conhecimento.
- `src/services/`: Lógica de construção e orquestração do Agente.
- `src/ui/`: Interface de usuário (CLI interativa).

## 🛠️ Instalação e Configuração

### Pré-requisitos
- [uv](https://github.com/astral-sh/uv) para gerenciamento de pacotes.
- [Ollama](https://ollama.ai/) rodando com os modelos:
  - `llama3.1` (LLM)
  - `nomic-embed-text` (Embeddings)

Verifique se o Ollama está rodando e tem os modelos:
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
ENABLE_WEB_SEARCH=true
```

## 🚀 Como Executar

Para iniciar a CLI interativa:
```bash
uv run python -m src.main
```

Para carregar os dados de exemplo (seed) e iniciar:
```bash
uv run python -m src.main --seed
```

Para uma pergunta direta via terminal:
```bash
uv run python -m src.main --ask "Qual a capital da França?"
```

## 📝 Comandos na CLI

- `/add`: Adiciona novos textos à base de conhecimento em tempo real.
- `/help`: Mostra a lista de comandos.
- `/quit`: Encerra o programa.

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

Algums modelos como o `phi3` não suporta o uso de ferramentas (tools) no Agno, conforme a documentação. Para usar modelos menores localmente, considere alternativas como:

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

Essas dependências são instaladas automaticamente ao executar `uv sync`. Se preferir instalar manualmente:

```bash
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

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
