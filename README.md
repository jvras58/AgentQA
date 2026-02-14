# AgentQA - POC de Sistema de Perguntas e Respostas com IA

Este é um projeto de prova de conceito (POC) para um sistema de perguntas e respostas baseado em documentos enviados para uma IA. Utiliza o framework [Agno](https://docs.agno.com/) para criar um agente inteligente com Retrieval-Augmented Generation (RAG), permitindo consultas sobre documentos armazenados em uma base de dados vetorial.

## Funcionalidades

- **Agente QA com RAG**: O agente responde perguntas baseadas em documentos inseridos na base de conhecimento.
- **Base Vetorial Local**: Usa LanceDB para armazenar embeddings de documentos, permitindo buscas eficientes.
- **Embeddings Locais**: Utiliza Ollama com o modelo `nomic-embed-text` para gerar embeddings sem depender de APIs externas.
- **Memória Persistente**: Histórico de conversas armazenado em SQLite.
- **Ferramentas Opcionais**: Integração com DuckDuckGo para buscas na web (pode ser substituído por Brave Search).

## Pré-requisitos

1. **Python**: Versão 3.8 ou superior.
2. **Ollama**: Instale o [Ollama](https://ollama.com/) e baixe os modelos necessários:
   - `ollama pull llama3.1` (para o modelo principal)
   - `ollama pull nomic-embed-text` (para embeddings)
3. **Dependências**: Instale as bibliotecas via `pip` ou `uv`:
   ```
   pip install agno
   ```
   Ou usando `uv` se preferir:
   ```
   uv add agno
   ```

## Como Usar

1. Clone ou baixe o projeto.
2. Ative o ambiente virtual (se usar venv):
   ```
   .venv\Scripts\activate  # Windows
   ```
3. Execute o script principal:
   ```
   python qa.py
   ```
   Ou com `uv`:
   ```
   uv run qa.py
   ```

O agente irá responder à pergunta de exemplo: "Pergunta hard: João mudou pra onde e com quantos anos?"

## Estrutura do Projeto

- `qa.py`: Script principal com a configuração do agente.
- `tmp/lancedb/`: Diretório onde o LanceDB armazena os dados vetoriais.
- `agent.db`: Banco de dados SQLite para histórico de conversas.

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

