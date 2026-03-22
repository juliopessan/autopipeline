---
name: autonomous-data-research
description: >
  Executa e gerencia uma plataforma de pesquisa autônoma para otimização de pipelines de dados no Azure.
  Use esta skill sempre que: (1) for iniciar uma nova plataforma de análise autônoma;
  (2) for otimizar um pipeline existente delegando a um agente; (3) for revisar resultados de experimentos;
  (4) for diagnosticar falhas ou comportamentos inesperados do agente.
  Acionadores: "setup de plataforma autônoma", "monta autopipeline", "otimiza esse pipeline com agente",
  "revisa experimentos", "diagnostica por que o agente tá travado", ou qualquer tarefa de operação
  de plataforma de pesquisa de dados autônoma.
---

# Autonomous Data Research Skill

Skill de execução para **plataformas de pesquisa autônoma de pipelines de dados** (inspiradas no projeto autoresearch de Karpathy, mas adaptadas para Azure + análise empresarial).

> "A pesquisa de dados não é feita por engenheiros ajustando knobs manualmente — é feita por agentes autônomos testando ideias, mantendo resultados, e descartando fracassos."

---

## 1. Visão Geral

Uma **plataforma de pesquisa autônoma** deixa um agente AI experimentation com diferentes abordagens de pipeline **enquanto você dorme**:

- Agent propõe uma melhoria (otimizar SQL, ajustar parâmetros, cache)
- Modifica **ONLY** `analysis.py`
- Executa com budget fixo (tempo + custo Azure)
- Mede métrica (latência, qualidade, custo)
- Se melhorou → keep commit; se piorou → reset
- Repete ~12 vezes/hora, ~100+ vezes/noite
- Você acorda com log de experimentos + pipeline otimizado

---

## 2. Diagnóstico Inicial (Setup)

Ao receber solicitação de setup, determine:

| Dimensão | Pergunta-chave |
|---|---|
| **Pipeline Target** | Qual pipeline específico será otimizado? (Sales Analytics, Customer 360, etc.) |
| **Current State** | Qual é a métrica atual? (latência 120s, cost $5/run, cache hit 30%) |
| **Optimization Goal** | O que queremos minimizar/maximizar? (latência, custo, freshness, quality) |
| **Constraints** | Budget Azure? SLA? Restrições de complexidade? |
| **Autonomy Level** | Quanto a agent pode mudar? (SQL only? También params? También architecture?) |
| **Data** | Qual é o escopo de dados? (1 TB? 100 GB? Tempo de query atual?) |

Faça **no máximo 3 perguntas diretas** e assuma razoável para o resto.

---

## 3. Os 4 Modos de Operação

### Modo A — Setup & Launch de Nova Plataforma

**Quando usar:** Iniciar plataforma autônoma para um novo pipeline.

**Checklist de Execução:**

```
□ Step 1: Identificar pipeline target e métricas baseline
  - Qual é a métrica principal? (latência / custo / qualidade)
  - Qual o valor atual?
  - Qual o target?
  
□ Step 2: Provisionar infraestrutura Azure
  - ADLS Gen2 (data lake)
  - Synapse SQL Pool (query engine)
  - Application Insights (monitoring)
  - Key Vault (secrets)
  - Cost Management API access
  
□ Step 3: Criar estrutura de repositório
  - Estrutura básica: program.md, analysis.py, engine.py, azure_adapters.py
  - Templates preenchidos
  - resultados.tsv com header
  
□ Step 4: Escrever program.md
  - O que agent pode modificar (be SPECIFIC)
  - O que agent NÃO pode fazer (be SPECIFIC)
  - Métricas de sucesso
  - Ideias para testar (opcional)
  
□ Step 5: Draft analysis.py
  - Implementar `run_analysis()` que retorna métrica
  - Usar abstrações do `azure_adapters` (não hardcode Azure)
  - Teste manual 1-2x antes de dar ao agent
  
□ Step 6: Testar engine + adapters
  - Run 1 experimento manualmente
  - Verifique: métrica reportada, custo trackado, tempo respeitado
  
□ Step 7: Configurar agent
  - Sistema prompt personalizado com constraints
  - Testar 1-2 proposals antes de liberar loop autônomo
  
□ Step 8: Launch
  - Clone repo
  - Run: python agent_loop.py (background process / container)
  - Monitor: check results.tsv a cada hora
  - Alerts: Slack/email quando improvement encontrado
```

**Output Mínimo Garantido:**
- Repositório setup e versionado
- program.md completo (constraints + goals)
- analysis.py funcionando manualmente
- engine.py + adapters testados
- Agent rodando (verificado com 3-5 experimentos iniciais)
- Documentação: "como reproduzir, como interromper, como ler resultados"

---

### Modo B — Operação & Monitoramento Contínuo

**Quando usar:** Platform está rodando; você monitora + intervém ocasionalmente.

**Daily Routine:**

```
09:00 — Revisar results.tsv
  • Quantos experimentos rodaram?
  • Qual é o best metric agora vs. baseline?
  • Houve crashes? (se sim, qual foi o motivo?)
  
10:00 — Check Application Insights
  • Custo total gasto? (expected vs. actual)
  • Latency distribution (está piorando?)
  • Errors/exceptions?
  
11:00 — Slack review
  • Alerts (new best found? cost spike?)
  
2-3× semana — Deep dive
  • Leia os últimos 5 commits (git log)
  • Cada um faz sense? Agente tá aprendendo?
  • Se vendo padrão de failure (crash recorrente), interrompa + debug
```

**Intervention Points:**

| Situação | Ação |
|---|---|
| Agent preso (10+ crashes seguidos) | Interrompa, revise program.md, reinicie |
| Métrica plateauing (100+ keeps, 0 improvement) | Revise program.md: talvez agent precise de novo scope |
| Custo crescendo (avg cost per run está subindo) | Revise analysis.py: pode ter memory leak |
| Novo requirement (SLA changed) | Edite program.md, reinicie, agent adapta |

**KPIs to Track:**

| KPI | Healthy | Unhealthy |
|---|---|---|
| **Improvement %** | +3% per 8h | Flat for 24h+ |
| **Keep Ratio** | 40-60% | <20% or >80% |
| **Crash Rate** | <5% | >20% |
| **Cost Trend** | Stable or ↓ | ↑ month-over-month |
| **Simplicity Delta** | ≤ 10 lines added/week | >50 lines = complexity risk |

---

### Modo C — Diagnóstico de Falhas

**Quando usar:** Algo está errado (agent travado, crashes, costs spiking).

**Troubleshooting Framework:**

```
SYMPTOM: Agent não progrediu em 4 horas (10+ experiments, 0 keeps)

1. READ results.tsv
   → Last 10 rows: qual o padrão de status?
   → Tudo "discard"? = agent tá explorando mas não achando improvement
   → Tudo "crash"? = bug no code ou program.md muito restritivo

2. READ git log --oneline (last 20 commits)
   → Commits estão coerentes?
   → Cada mudança é uma ideia distinta?
   → Ou estão repetindo mesma ideia?

3. READ run.log (último arquivo de log)
   → Qual foi a última métrica?
   → Error messages? Stack traces?
   → Timeout? OOM?

4. INSPECT latest analysis.py
   → Compare com baseline (git show HEAD~10:analysis.py)
   → Mudanças fazem sentido?
   → Há syntax errors (Python compilaria?)

5. DIAGNOSE
   a) If all experiments crash:
      → Likely: syntax error, missing import, OOM
      → Fix: git reset, review program.md constraints, restart
      
   b) If metric not improving but no crashes:
      → Likely: optimization space exhausted or agent exploring dead ends
      → Fix: modify program.md (expand scope), provide hints, restart
      
   c) If cost per run increasing:
      → Likely: query is more complex, scanning more data
      → Fix: check for N+1 queries, memory leaks, missing WHERE clauses
      
   d) If crashes + increasing cost:
      → Likely: agent trying wild experiments that blow up
      → Fix: tighten program.md constraints (max complexity), restart
```

---

### Modo D — Escalação para Multi-Pipeline

**Quando usar:** Primeiro pipeline está estável; pronto para rodar 5-10 pipelines em paralelo.

**Escalação Pattern:**

1. **Organize pipelines by domain**
   - Domain 1: Sales Analytics (4 pipelines)
   - Domain 2: Customer 360 (3 pipelines)
   - etc.

2. **Shared agent vs. per-pipeline agents**
   - Shared: 1 agent manages all, must queue experiments (simpler)
   - Per-pipeline: 1 agent per pipeline (parallelism, but more compute)
   - Recommendation: start with shared, move to per-pipeline if bottleneck

3. **Cross-pipeline learning**
   - Agent in Domain 1 finds technique X (index optimization)
   - Can this apply to Domain 2 pipelines?
   - Add `cross_domain_hints` to program.md

4. **Resource allocation**
   - Each pipeline has own Azure resources OR shared pool?
   - If shared pool: monitor contention (via Application Insights)
   - If separate: monitor total spend (sum of all pools)

---

## 4. Verificação Antes de Entregar (Modo A — Launch)

**CHECKLIST — Launch Safety:**

```
□ program.md
  • Constraints são SPECIFIC? (não "optimize everything", mas "otimizar SQL joins")
  • Stopping criteria definido? (não aberto-ended)
  • Métrica de sucesso é measurable?

□ analysis.py
  • Roda sem erro quando executado manualmente?
  • `run_analysis()` retorna dict com "primary_metric"?
  • Não hardcodeia Azure credentials?

□ engine.py
  • Time budget enforcement funciona?
  • Cost limit enforcement funciona?
  • Timeout detection funciona?

□ azure_adapters.py
  • Todas APIs necessárias implementadas?
  • Erro handling para transient failures?
  • Cost tracking API integrado?

□ Infrastructure
  • Todos os Azure resources provisionados?
  • Agent managed identity tem as permissões certas?
  • Key Vault secrets estão em place?

□ Agent
  • 3-5 experimentos rodaram manualmente (não em loop)?
  • Commits fazem sense?
  • Não há infinite loops (ideias repetidas)?

□ Monitoring
  • Application Insights collecting metrics?
  • Alertas configurados (cost, crashes)?
  • Slack/Email integrado?

□ Documentation
  • README com "como rodar", "como parar", "como ler resultados"?
  • program.md comentado?
  • Assumptions/risks documentados?

Se QUALQUER item falhar → NÃO libere autonomously.
Fixa primeiro, testa manualmente, depois libera.
```

---

## 5. Self-Improvement Loop da Skill

Após cada execução (setup, operação, diagnóstico):

1. **Registre a lição em `lessons.md`**
   ```
   ## Lesson [NNN] [DATA]: [Título]
   **Cenário:** O que aconteceu
   **Inesperado:** O que foi surpreendente
   **Raiz:** Por que aconteceu
   **Fix:** O que fez funcionar
   **Padrão:** Quando repetir esta solução
   ```

2. **Atualize templates se necessário**
   - program.md template ficou desatualizado?
   - analysis.py skeleton precisa de melhorias?
   - Documentação ficou confusa?

3. **Rastreie padrões**
   - Qual constraint de program.md mais causa crash?
   - Qual metrica é mais fácil de otimizar?
   - Quanto tempo leva tipicamente para 10% improvement?

---

## 6. Seleção de Formato de Output

| Modo | Receptor | Formato | Conteúdo |
|---|---|---|---|
| Setup | Tech Lead / Engenharia | Repositório Git + README | Estrutura + template preenchido |
| Operação | Data Engineer | Relatório diário (Slack/email) | Top experiments, KPIs, recomendações |
| Diagnóstico | DevOps / On-call | Troubleshooting doc + git diffs | Análise raiz + próximos steps |
| Escalação | Arquiteto | Proposta técnica (§2 ai-solutions-architect) | Multi-pipeline design, resource plan |

---

## 7. Referências Internas

Quando precisar de detalhes:

- **Azure Services:** Consulte documentação oficial (Synapse, ADLS, Insights)
- **Padrões de Arquitetura:** Use skill `ai-solutions-architect` para trade-offs cloud
- **Código + Templates:** Ver seção "§3 File Structure" em `azure_platform_architecture.md`
- **Segurança/Compliance:** Consulte skill `ai-solutions-architect` + Azure Well-Architected Review

---

## 8. Quick Reference Card

```
AO RECEBER SOLICITAÇÃO:
  → Diagnóstico: Qual modo? (setup / operação / diagnóstico / escalação)
  → Máximo 3 perguntas se faltar contexto crítico
  → Assuma razoável e declare premissas

SE MODO = SETUP:
  → Siga Modo A checklist (8 steps)
  → Teste manualmente antes de liberar autonomous
  → Entregue repositório + documentação

SE MODO = OPERAÇÃO:
  → Revise results.tsv, Application Insights, Slack alerts
  → Calcule KPIs (improvement %, keep ratio, cost trend)
  → Recomende ações (continuar / intervir / escalar)

SE MODO = DIAGNÓSTICO:
  → Siga troubleshooting framework (5 steps)
  → Leia results.tsv + git log + run.log
  → Identifique raiz (syntax error? budget? optimization ceiling?)
  → Prescreva fix (reset git, edit program.md, restart)

AO ENTREGAR:
  → Rode Launch Safety Checklist (se setup)
  → Formato certo para receptor
  → Próximos passos explícitos

QUANDO CORRIGIDO:
  → Escreva lição em lessons.md imediatamente
  → Nunca repita o mesmo erro
```

---

## 9. Common Pitfalls & How to Avoid

| Pitfall | Causa | Prevenção |
|---|---|---|
| **Agent otimiza métrica errada** | program.md ambíguo | Defina primary_metric NUMERICAMENTE (não "better performance") |
| **Crashes infinitos** | program.md scope demais aberto | Listar explicitamente o que agent CAN'T fazer |
| **Custo cresce** | Sem enforcement de cost budget | Use Cost API polling; set hard limit in engine.py |
| **Agent trava** | Optimization space exhausted | Monitorar "discard" ratio; se >80%, reset + new ideas |
| **Audit trail perdido** | Commits reescrito (git rebase) | Rodar em branch separada (não main); never force-push |
| **Desenvolvimento bloqueado** | Agent mudando código que humans precisam editar | Separar responsabilidades: agent só toca analysis.py |
| **Setup demorando semanas** | Over-engineering infrastructure | Start minimal (ADLS + Synapse + AppInsights only), scale depois |

---

## 10. Success Metrics & Graduation Criteria

### Fase 1 (Setup) — Success Metrics

| Métrica | Target | Medida |
|---|---|---|
| **Setup Time** | < 1 week | Dias até primeiro autonomous run |
| **Initial Stability** | 0 crashes em 50 runs | % de runs que completam sem erro |
| **Baseline Understood** | Yes | Team entende métrica atual + target |

### Fase 2 (Operação) — Success Metrics

| Métrica | Target | Medida |
|---|---|---|
| **Improvement** | +3% per week | (best_metric - baseline) / baseline |
| **Velocity** | 50+ experiments/week | Experiments completados / semana |
| **False Positives** | < 10% | Experiments que "keep" mas falham em produção |
| **Cost Stability** | Flat or ↓ | $ per run trend |

### Graduation to Production

Quando mover de "experimental" para "production pipeline":

```
✓ 200+ experiments rodados sem manual intervention
✓ Improvement > 5% sustentável
✓ Zero crashes por 48h+ contínuo
✓ Custo por run < budget por 30 dias
✓ Audit trail completo (100% git commits)
✓ Team confortável operando independently
✓ SLA documentado + monitorado
```

---

**Visão Final:** Um plataforma de pesquisa autônoma não é "deixar agente fazer o que quiser". É criar **structure for the agent's autonomy**: boundaries (program.md), tools (adapters), observation (results.tsv), e intervención points (monitoring). Isso permite escala sem caos.

