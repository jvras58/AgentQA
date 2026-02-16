# Métricas de Avaliação para Agentes RAG no AgentQA

## Como Avaliar se o Agente Usou o Plano/RAG Definido?

Métricas como **RAGAS** (ex.: Faithfulness, Answer Relevance, Context Precision) são essenciais para medir a qualidade de sistemas RAG, especialmente se o agente realmente utilizou o contexto recuperado do knowledge base. No entanto, o framework **Agno** não oferece suporte nativo direto para RAGAS. Em vez disso, ele fornece um sistema de avaliação próprio, que pode ser adaptado para simular essas métricas. Abaixo, explicamos as opções e como implementá-las no **AgentQA**.

### 1. Sistema de Avaliação Nativo do Agno
O Agno inclui quatro tipos principais de avaliações (Evals), que podem ser executadas após uma run do agente. Elas ajudam a verificar se o agente seguiu o plano esperado (ex.: buscar no knowledge base) e se a resposta é fiel ao contexto.

- **Accuracy Eval**: Verifica se a resposta final está correta, comparando com um `expected_output` usando um LLM como juiz (LLM-as-a-Judge). Útil para validar a precisão geral.
- **Agent as Judge Eval**: Permite critérios customizados (ex.: "A resposta usou o contexto do knowledge base?") com pontuação de 1-10. Isso simula métricas como **Faithfulness** (fidelidade ao contexto).
- **Reliability Eval**: Valida se as tool calls esperadas foram executadas (ex.: `search_knowledge_base`). Ideal para confirmar que o agente acessou o RAG.
- **Performance Eval**: Mede latência, uso de memória e tokens. Não avalia qualidade, mas eficiência.

#### Como Usar no AgentQA
Para implementar, importe as evals no seu serviço de agentes (ex.: `src/services/ask_agent_service.py` ou `question_agent_service.py`) e execute após uma run.

Exemplo de código para avaliar o agente de perguntas:

```python
from agno.eval import AccuracyEval, AgentAsJudgeEval, ReliabilityEval

# Após executar o agente
run_output = agent.run("Pergunta de teste")

# Avaliações
accuracy_eval = AccuracyEval(expected_output="Resposta esperada")
accuracy_result = accuracy_eval.run(run_output)

judge_eval = AgentAsJudgeEval(
    criteria="A resposta é fiel ao contexto recuperado do knowledge base?",
    scale=10
)
judge_result = judge_eval.run(run_output)

reliability_eval = ReliabilityEval(expected_tool_calls=["search_knowledge_base"])
reliability_result = reliability_eval.run(run_output)

# Resultados
print(f"Accuracy: {accuracy_result.score}")
print(f"Faithfulness (Judge): {judge_result.score}")
print(f"Reliability: {reliability_result.score}")
```

- **Para simular RAGAS**:
  - Use **AgentAsJudgeEval** com critérios como "A resposta é relevante para a pergunta?" (Answer Relevance) ou "O contexto foi usado adequadamente?" (Faithfulness).
  - Combine com **ReliabilityEval** para garantir que tools como `search_knowledge_base` foram chamadas.

### 2. Integração Externa com RAGAS
Se precisar de métricas RAGAS específicas (Faithfulness, Answer Relevance, Context Relevancy), integre a biblioteca `ragas` externamente. Ela usa dados como resposta, contexto recuperado e input para calcular scores.

#### Passos para Implementar
1. **Adicione a dependência**:
   ```bash
   uv add ragas
   ```
   Atualize o `pyproject.toml` com `ragas>=0.1.0` (ou versão compatível).

2. **Extraia dados do Agno**:
   O `RunOutput` do Agno contém `response`, `messages` e `tools_used`. Extraia o contexto (ex.: do knowledge base) e a resposta.

3. **Calcule métricas com RAGAS**:
   ```python
   from ragas import evaluate
   from ragas.metrics import faithfulness, answer_relevancy, context_relevancy
   from datasets import Dataset

   # Dados extraídos do RunOutput
   data = {
       "question": ["Pergunta de teste"],
       "answer": ["Resposta do agente"],
       "contexts": [["Contexto recuperado do knowledge base"]],
       "ground_truth": ["Resposta esperada (opcional)"]
   }
   dataset = Dataset.from_dict(data)

   # Avaliação
   result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_relevancy])
   print(result)
   ```

   - **Faithfulness**: Mede se a resposta é fiel ao contexto (sem alucinações).
   - **Answer Relevancy**: Verifica se a resposta é relevante para a pergunta.
   - **Context Relevancy**: Avalia se o contexto recuperado é útil.

#### Integração Completa no AgentQA
Adicione uma função de avaliação em `src/services/` ou crie um script separado (ex.: `scripts/evaluate_agent.py`).

Exemplo em `evaluate_agent.py`:
```python
import asyncio
from src.services.ask_agent_service import ask_agent
from agno.eval import AgentAsJudgeEval
from ragas import evaluate
from ragas.metrics import faithfulness

async def evaluate_agent():
    # Run do agente
    response = await ask_agent.arun("Como funciona o RAG?")

    # Eval Agno
    judge_eval = AgentAsJudgeEval(criteria="Usou o knowledge base?", scale=10)
    agno_score = judge_eval.run(response).score

    # Eval RAGAS (se contexto disponível)
    if response.contexts:  # Supondo que RunOutput tenha contexts
        dataset = Dataset.from_dict({
            "question": ["Como funciona o RAG?"],
            "answer": [response.content],
            "contexts": [response.contexts]
        })
        ragas_result = evaluate(dataset, [faithfulness])
        print(f"Agno Judge: {agno_score}, RAGAS Faithfulness: {ragas_result['faithfulness']}")

asyncio.run(evaluate_agent())
```

### 3. Recomendações e Limitações
- **Quando usar Agno vs. RAGAS**: Agno é mais simples e integrado; use RAGAS para métricas padronizadas em pesquisa.
- **Limitações**: RAGAS requer dados estruturados; Agno é mais flexível para customização.
- **Próximos Passos**: Teste com dados reais do AgentQA. Monitore performance para evitar overhead em produção.

Para mais detalhes:
- [Documentação Agno Evals](https://docs.agno.com/evals/overview)
- [RAGAS Docs](https://docs.ragas.io/)
- [Agent as Judge no Agno](https://docs.agno.com/evals/agent-as-judge/overview)
