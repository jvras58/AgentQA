### Resumo do Projeto AgentQA e Evolução das Abordagens

#### 1. **Visão Geral do Projeto**
O **AgentQA** é um sistema de Perguntas e Respostas (QA) com Inteligência Artificial, implementado como uma API usando **FastAPI**. Ele utiliza **RAG (Retrieval-Augmented Generation)** local para responder perguntas de forma inteligente, combinando recuperação de dados armazenados com geração de respostas via modelos de linguagem grandes (LLMs). O foco é em um sistema leve, executável localmente ou via Docker, sem depender de serviços externos caros (exceto opcionalmente para pesquisa na web).

- **Tecnologias Principais**:
  - **LLM e Embeddings**: Ollama com modelos `llama3.1` (para geração de texto) e `nomic-embed-text` (para embeddings vetoriais).
  - **Armazenamento**: LanceDB (banco de dados vetorial leve para RAG).
  - **Agentes**: Framework Agno para orquestração de agentes inteligentes.
  - **Pesquisa Web**: DuckDuckGo Tools (ddgs) para consultas externas quando necessário.
  - **Infraestrutura**: FastAPI para API, SQLAlchemy para histórico de conversas (SQLite), Pydantic para configurações.
  - **Gerenciamento**: uv para dependências, Docker para containerização.

O projeto está estruturado em módulos claros: `core` (configurações), `infra` (persistência e conhecimento), `services` (lógica dos agentes), `api` (endpoints), e scripts para seeding de dados.

#### 2. **Abordagem Atual Implementada**
A abordagem atual gira em torno de **dois agentes inteligentes especializados**, orquestrados para maximizar eficiência e inteligência:

- **Agente de Resposta a Perguntas**:
  - **Função**: Responde perguntas com base em dados locais (docs armazenados no LanceDB). Se não houver dados relevantes, pesquisa na internet usando **DuckDuckGo Tools** para enriquecer a resposta.
  - **Inteligência**: Usa **knowledgeTools** para uma busca mais "pensante" no RAG, em vez de uma recuperação simples. Isso permite contextualizar e raciocinar sobre os dados, evitando respostas superficiais.
  - **Limitações Controladas**: Acesso à internet apenas quando necessário, mantendo privacidade e controle local.

- **Agente de Geração de Questões**:
  - **Função**: Gera questões automaticamente com base nos documentos armazenados (docs no LanceDB). Não tem acesso à internet (não usa DuckDuckGo), mas conta com o poder do modelo treinado (3B de parâmetros no `llama3.1`) para criar questões criativas e relevantes por conta própria.
  - **Ajustes Potenciais**: Como é um modelo pré-treinado, pode demandar fine-tuning ou prompts ajustados para otimizar a geração, mas funciona bem para casos gerais.

- **Infraestrutura de Suporte**:
  - **RAG Inteligente**: Combina LanceDB (leve e rápido) com tools de conhecimento para "pensar" melhor, em vez de só recuperar vetores brutos.
  - **Persistência**: Histórico de conversas em SQLite (até 3 execuções anteriores no contexto para memória).
  - **Execução**: Local via Ollama ou containerizada com Docker (usando compose.yml e Dockerfiles específicos para embeddings e LLM).
  - **Seeds e Scripts**: Script `seed_knowledge.py` para popular o banco com docs iniciais.

Essa abordagem prioriza **leveza, inteligência local e modularidade**, permitindo execução offline na maioria dos casos, com fallback para web apenas quando essencial.

#### 3. **Por Que Fizemos Essa Abordagem? (Decisões e Motivações)**
- **Foco em RAG Local**: Evita dependências de APIs externas (como OpenAI) para reduzir custos e latência. Ollama permite execução local, mantendo privacidade.
- **Dois Agentes Especializados**: Separa responsabilidades para eficiência – um foca em respostas precisas (com pesquisa opcional), outro em geração criativa (offline). Isso evita sobrecarga em um único agente e permite escalabilidade.
- **Uso de knowledgeTools**: Adiciona "inteligência de pensar" ao RAG, superando limitações de buscas vetoriais simples (que só recuperam similaridade, sem raciocínio). Isso resulta em respostas mais contextuais e relevantes.
- **LanceDB por Leveza**: Escolhido por ser mais rápido e menos resource-intensive que alternativas como Pinecone ou Weaviate. A "troca não é difícil" se precisar migrar, mas mantém o sistema ágil.
- **Pesquisa Web Controlada**: DuckDuckGo para o agente de perguntas, mas só quando local falha – equilibra completude com eficiência e evita overuse.
- **Modularidade e Escalabilidade**: Estrutura em FastAPI permite APIs REST fáceis de integrar. Scripts e seeds facilitam manutenção e expansão.

Essas escolhas foram guiadas por necessidades de **performance local, custo zero (exceto hardware)** e **inteligência adaptável**, adequadas para protótipos ou sistemas pequenos/médios.

#### 4. **Comparação com Abordagens Anteriores**
Com base no checkpoint.md e na estrutura do projeto, inferimos que abordagens anteriores eram mais básicas e limitadas, evoluindo para a atual por meio de iterações. Aqui uma comparação:

- **Abordagem Anterior 1: RAG Simples com LanceDB Básico**:
  - **O Que Era**: Só usava LanceDB para armazenar e recuperar vetores de embeddings, sem tools inteligentes. Buscas eram puramente por similaridade vetorial (sem "pensar" ou contextualizar).
  - **Problemas**: "Pecava na questão de inteligência de pensar" – respostas superficiais, sem raciocínio sobre relevância ou contexto. Dependia totalmente de dados locais, sem fallback para web.
  - **Por Que Mudamos**: Adicionamos knowledgeTools para enriquecer o RAG, tornando-o mais "inteligente" e capaz de inferir conexões entre dados.

- **Abordagem Anterior 2: Uso de Bancos Vetoriais Mais Pesados**:
  - **O Que Era**: Usar alternativas como ChromaDB, FAISS ou até bancos relacionais, que são mais robustos mas pesados em recursos (CPU/memória).
  - **Problemas**: Lentidão em setups locais, dificuldade de execução em máquinas modestas, maior complexidade de setup.
  - **Por Que Mudamos**: Optamos por LanceDB por ser "mais leve em comparação com os outros". A troca é fácil se precisar, mas mantém foco em eficiência local.


#### 5. **Atualizações e Detalhes Adicionais na Evolução**
Durante o desenvolvimento, fizemos otimizações adicionais para eficiência e performance:

- **Rotas FastAPI Assíncronas**: As rotas da API foram tornadas assíncronas (`async def`), e a chamada no agente mudou de `run` para `arun` no método `handle_generate_questions`. Isso permite execução não-bloqueante, melhorando a responsividade em cenários de alta carga.

- **LanceDB Assíncrono**: O LanceDB suporta operações assíncronas, permitindo trocar `insert` por `ainsert` no objeto `knowledge`. Isso otimiza inserções em lote ou operações pesadas, reduzindo latência.

- **Ingestão de Prompts via YAML**: Substituímos prompts diretos no código do agente pelo uso de arquivos YAML (ex.: `question_agent.yaml`), já que o framework Agno suporta essa configuração externa. Isso facilita manutenção, versionamento e ajustes sem alterar o código.

- **Modelos Menores (SML) Recomendados**: Para casos como este (QA local e geração de questões), modelos menores como o Phi4 podem se sair ligeiramente melhores em termos de velocidade e eficiência de recursos, sem comprometer muito a qualidade, comparado a modelos maiores como Llama3.1.

- **Sobre Fine-Tuning**: É possível fazer fine-tuning em modelos que já passaram por treinamento prévio, desde que sejam open-source e acessíveis (como o Llama3.1 usado aqui via Ollama). Isso envolve treinar o modelo em um dataset específico (ex.: pares de perguntas/respostas do seu domínio) usando ferramentas como Hugging Face Transformers ou Axolotl. No entanto, requer hardware potente (GPU), dados de qualidade e tempo. Para protótipos, ajustes de prompts ou few-shot learning podem ser suficientes antes de investir em fine-tuning.



#### 6. **Próximos Passos ou Ajustes**
- **Ajustes no Agente de Geração**: Como mencionado, o modelo treinado pode precisar de fine-tuning (ou algo do tipo) para questões mais precisas.
- **Expansão**: Adicionar mais docs via `seed_knowledge.py` ou integrar com outras fontes.
