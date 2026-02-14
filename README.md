# 🤖 AgentQA

Sistema de Perguntas e Respostas (QA) com IA utilizando **RAG (Retrieval-Augmented Generation)** local.

## 📂 Estrutura de Pastas

- `src/agent_qa/core/`: Configurações globais e validação de ambiente com **Pydantic Settings**.
- `src/agent_qa/infra/`: Gerenciamento de persistência (LanceDB) e conhecimento.
- `src/agent_qa/services/`: Lógica de construção e orquestração do Agente.
- `src/agent_qa/ui/`: Interface de usuário (CLI interativa).

## 🛠️ Instalação e Configuração

### Pré-requisitos
- [uv](https://github.com/astral-sh/uv) para gerenciamento de pacotes.
- [Ollama](https://ollama.ai/) rodando com os modelos:
  - `llama3.1` (LLM)
  - `nomic-embed-text` (Embeddings)

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
uv run agentqa
```

Para carregar os dados de exemplo (seed) e iniciar:
```bash
uv run agentqa --seed
```

Para uma pergunta direta via terminal:
```bash
uv run agentqa --ask "Qual a capital da França?"
```

## 📝 Comandos na CLI

- `/add`: Adiciona novos textos à base de conhecimento em tempo real.
- `/help`: Mostra a lista de comandos.
- `/quit`: Encerra o programa.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.