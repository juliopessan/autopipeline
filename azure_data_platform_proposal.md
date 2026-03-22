# Azure Autonomous Data Analysis Platform

## Executive Summary

A **self-improving autonomous research platform** for data analysis that lets AI agents experiment with different analytical approaches, optimize pipelines, and iterate on models — all running against Azure services. Similar to autoresearch's paradigm for ML training, but adapted for enterprise data workflows: agents autonomously modify analysis code, test it against real data, track metrics, and keep improvements. Teams wake up to optimized pipelines and documented experiment trails.

**Key insight:** Most data teams spend 70% of time hand-tuning pipelines. This platform delegates that tuning to autonomous agents while humans define the "research org code" (program.md equivalent) that governs exploration boundaries.

---

## Problem Statement

**Current state:**
- Data engineers manually optimize pipelines (ETL, aggregations, model inference)
- Changes are ad-hoc, undocumented, and hard to compare
- No systematic way to track which optimization works and why
- Team context is lost when approaches fail
- Scaling from 1 pipeline to 100+ becomes chaotic

**Desired state:**
- Agents autonomously test pipeline improvements overnight
- Every experiment is tracked with metrics, commit hash, and rationale
- Bad ideas are discarded; good ideas compound
- Human engineers remain in control (they write the experiment boundaries)
- Runs are repeatable, comparable, and auditable

---

## Solution Overview

### Core Components

| Component | Purpose |
|---|---|
| **Experiment Engine** | Runs data pipelines with fixed time/cost budget, measures quality metrics (latency, accuracy, cost) |
| **Agent Controller** | Autonomous agent that reads program.md, modifies analysis code, commits, runs, tracks results |
| **Results Tracker** | TSV-based experiment log (like autoresearch) with metrics, status, commit hash |
| **Azure Integration Layer** | Abstracts Data Factory, Synapse, Cosmos DB, Application Insights, Azure AI services |
| **Program Manifest** | YAML/JSON that defines: scope, constraints, optimization goals, out-of-bounds rules |
| **UI Dashboard** | Real-time experiment results, metric trends, recommended actions |

### Execution Model

```
LOOP (run autonomously until interrupted):

1. Read program.md (experiment boundaries)
2. Review latest results.tsv (what's working)
3. Propose an improvement (architecture, queries, parameters)
4. Modify analysis.py (agent edits ONLY this file)
5. git commit with descriptive message
6. Run pipeline with fixed time budget (e.g., 10 min)
7. Measure metrics (latency, data quality score, cost)
8. Compare to baseline → keep or discard
9. Log to results.tsv
10. Repeat (never stop)
```

---

## Technical Architecture

### Layers

```
┌─────────────────────────────────────────────────────────┐
│  UI Dashboard (Metric trends, recommendations, logs)    │
├─────────────────────────────────────────────────────────┤
│  Agent Controller (Claude + system prompt → loop)       │
├─────────────────────────────────────────────────────────┤
│  Experiment Engine (Execute, measure, track)            │
├─────────────────────────────────────────────────────────┤
│  Analysis Code Layer (analysis.py — agent modifies)     │
├─────────────────────────────────────────────────────────┤
│  Azure Service Adapters (Data Factory, Synapse, Cosmos) │
├─────────────────────────────────────────────────────────┤
│  Data Layer (ADLS Gen2, SQL, Cosmos DB)                 │
└─────────────────────────────────────────────────────────┘
```

### File Structure (inspired by autoresearch)

```
project/
├── program.md              # Human-written: experiment boundaries
├── analysis.py             # Agent modifies this (pipelines, queries, models)
├── engine.py               # Fixed: experiment executor, metrics collector
├── azure_adapters.py       # Fixed: Data Factory, Synapse, Cosmos abstractions
├── results.tsv             # Experiment log (commit, metric, status, notes)
├── .git/                   # Every change is committed for audit trail
├── config.yaml             # Azure credentials, pipeline definitions
└── requirements.txt        # Python dependencies (locked)
```

### Key Design Decisions

**1. Fixed Time/Cost Budget**
- Each experiment runs for exactly N minutes (e.g., 10 min wall clock)
- All metrics are normalized to this budget (like autoresearch's 5-minute runs)
- Enables fair comparison across different approaches
- Predictable cost: N experiments/day = known Azure spend

**2. Single Editable File (analysis.py)**
- Agent only modifies `analysis.py` (queries, aggregations, model params)
- `engine.py` and `azure_adapters.py` are read-only (human review required)
- Diffs are readable, mergeable, auditable
- Clear scope prevents chaos

**3. Results Tracking (TSV Format)**
- Lightweight: tab-separated values (not database)
- Human-readable: can be viewed in any text editor or Excel
- Git-friendly: diffs show exactly what changed
- Schema: `commit | metric | cost_usd | latency_sec | data_quality | status | description`

**4. Commit-per-Experiment**
- Every change is committed to git (with agent's rationale)
- If experiment fails → git reset to previous commit
- If experiment succeeds → keep the commit, advance branch
- Full audit trail: who changed what, when, and why

---

## Functional Specifications

### Phase 1: Core Platform (Wave 1)

**Goals:**
- Run autonomous experiments against a sample data pipeline
- Track results in TSV
- Implement agent loop (program.md → modify → run → evaluate)

**Deliverables:**
1. **Program.md Template**
   - Experiment boundaries (what agent can/cannot modify)
   - Optimization goals (metrics to minimize/maximize)
   - Constraints (budget, compute, SLA)
   - Example experiments to try

2. **Analysis.py Skeleton**
   - SQL queries for data aggregation
   - Model inference logic
   - Parameter hooks for agent tuning

3. **Engine.py**
   - Execute pipeline with timeout
   - Measure metrics (latency, cost from Azure logs, data quality)
   - Return results in JSON

4. **Azure Adapters**
   - Data Factory: trigger pipelines, poll status
   - Synapse: execute SQL against data lake
   - Application Insights: query execution times, errors
   - Cost Management API: estimate run cost

5. **Agent System Prompt**
   - Instructions: read program.md, propose ideas, execute loop
   - Constraints: what files to edit, what APIs available
   - Feedback: how to interpret results.tsv
   - Termination: when to stop (never, unless interrupted)

6. **Results Tracker**
   - CLI tool to log experiments
   - CSV export for dashboards
   - Comparison view (top N experiments)

### Phase 2: UI & Analytics (Wave 2)

**Goals:**
- Visualize experiment trends
- Recommend next experiments
- Human oversight dashboard

**Deliverables:**
1. **Web Dashboard** (React)
   - Real-time experiment log
   - Metric trend charts
   - Commit diff viewer
   - Recommended experiments (based on patterns)

2. **Alerts & Notifications**
   - Slack: new best result found
   - Email: experiment summary each morning
   - Cost warnings: if trend is increasing

3. **Collaboration Features**
   - Comments on experiments
   - Pause/resume agent
   - Manual experiment creation

### Phase 3: Multi-Pipeline (Wave 3)

**Goals:**
- Scale to 10+ concurrent pipelines
- Orchestrate agent swarms
- Cross-pipeline optimization

**Deliverables:**
1. **Pipeline Manager**
   - Deploy new pipeline templates
   - Queue experiments across pipelines
   - Resource allocation (which pipeline gets GPU time, etc.)

2. **Agent Swarm Orchestration**
   - Multiple agents, one per pipeline (or one shared)
   - Communicate findings across pipelines
   - Share learned hyperparameters

3. **Advanced Analytics**
   - Correlation: which changes break downstream pipelines?
   - Cost attribution: which pipeline optimization added cost?
   - Recommendations: "if you apply optimizer X from pipeline A to pipeline B, expect Y% improvement"

---

## Azure Service Mapping

| Need | Azure Service | Notes |
|---|---|---|
| Data Ingestion | Data Factory / Event Hubs | Trigger pipelines, ingest streaming data |
| Data Lake | ADLS Gen2 | Store raw + processed data |
| Query Engine | Synapse SQL Pool / Kusto | Execute user's analytical queries |
| Monitoring | Application Insights | Track execution time, cost, errors |
| ML Inference | Azure ML / Cognitive Services | Run models, extract features |
| Cost Tracking | Cost Management API | Get real-time run costs |
| Secrets | Key Vault | Store DB credentials, API keys |
| Storage | Blob Storage (or Cosmos DB) | Archive results, cache intermediate data |
| Compute | Container Instances / Functions | Stateless execution, scale to zero |

---

## Non-Functional Requirements

| Requirement | Metric | Rationale |
|---|---|---|
| **Experiment Isolation** | Every run uses fresh checkpoint | Prevent cross-contamination |
| **Reproducibility** | Same code + same data = same results | Auditable, debuggable |
| **Cost Predictability** | Budget per experiment (e.g., $10 max) | Prevent runaway Azure bills |
| **Visibility** | All decisions logged + committed | Audit trail for compliance |
| **Autonomy** | Agent never asks for human approval | Design for unattended overnight runs |
| **Resilience** | Tolerate transient Azure API failures | Retry logic, fallback metrics |
| **Simplicity** | No ML frameworks, no complex configs | Pure Python + SQL, easy to debug |

---

## Success Metrics

| Metric | Target | Measured How |
|---|---|---|
| **Improvement per 8 hours** | ≥ 3% metric gain | Compare best result to baseline |
| **Experiment Velocity** | 12 experiments/hour | Time per run × number of runs |
| **False Positive Rate** | < 10% | Experiments that improve metrics but hurt real-world performance |
| **Cost per Experiment** | < $5 USD | Azure consumption API |
| **Adoption Readiness** | Runnable in < 1 hour | Time from repo clone to first autonomous run |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| **Agent produces untrustworthy code** | Data corruption, queries that run 1000x slower | Code review before merge; safety constraints in program.md; time/cost budget enforcement |
| **Azure costs spiral** | Runaway bill | Hard budget cap per experiment; cost alerts; disable auto-run if budget exceeded |
| **Experiments hang or timeout** | Agent gets stuck, no progress | Timeout enforcement; detection of stuck processes; auto-retry with reset |
| **Agent creates infinite loop of marginal improvements** | No real progress | Require minimum improvement threshold (e.g., 0.5% or discard); periodic manual reset |
| **Compliance/audit trails lost** | Regulatory risk | Git commit per change; immutable results.tsv; audit logs in Application Insights |

---

## Deployment Strategy

### Prerequisites
- Azure subscription (Standard tier recommended for sustained workloads)
- Azure DevOps or GitHub repo for code storage
- Python 3.10+
- RBAC access to Data Factory, Synapse, Cost Management API

### Deployment Phases

**Week 1: Infrastructure**
1. Provision Azure resources (ADLS Gen2, Synapse, Key Vault, Application Insights)
2. Configure service principals (agent's identity)
3. Set up Azure DevOps pipeline for automated tests

**Week 2: Core Platform**
1. Implement `engine.py`, `azure_adapters.py`
2. Deploy agent system prompt + loop
3. Manual testing: run 10 experiments, verify results.tsv

**Week 3: Validation & Go-Live**
1. Run 100+ experiments overnight
2. Verify no Azure overspend
3. Train team on program.md editing
4. Open to first pipeline

---

## Team & Effort Estimate

| Role | Effort | Notes |
|---|---|---|
| **Cloud Architect** | 10 days | Design Azure integration, cost model, security |
| **Platform Engineer** | 20 days | Implement engine.py, adapters, agent loop, monitoring |
| **Data Engineer** | 10 days | Create sample pipelines, define metrics, optimize queries |
| **AI/Agent Specialist** | 15 days | System prompt, failure handling, learning loop |
| **QA/Test** | 10 days | Reliability testing, cost validation, compliance audit |
| **Total** | ~65 days (~3 person-months) | Assumes parallel work; 1-2 month calendar time |

---

## Next Steps

1. **Align on scope:** Which Azure services does your team already use? Any preferred regions?
2. **Define first pipeline:** What's the highest-impact data pipeline that could benefit from optimization?
3. **Draft program.md:** What experiments should agents try? What's off-limits?
4. **Prototype:** Build engine.py + basic agent for that one pipeline (1-2 weeks)
5. **Iterate:** Run first autonomous experiments, refine feedback loop

---

## Appendix: Sample program.md

```markdown
# Autonomous Data Pipeline Optimization

This is an experiment to let the AI agent optimize your data pipeline autonomously.

## Setup

To start:
1. Create a branch: `git checkout -b autopipeline/exp-001`
2. Read `analysis.py` — this is the only file the agent modifies
3. Verify Azure credentials are in `config.yaml`
4. Run once manually: `python engine.py --run-once` to establish baseline
5. Create `results.tsv` with header: `commit|metric|cost_usd|status|description`

## Optimization Goals

**Primary Metric:** Query latency (seconds) — minimize
**Secondary Metric:** Data freshness (minutes) — minimize
**Constraint:** Cost < $5 per experiment, memory < 50GB

## What You Can Do

- Rewrite SQL queries (add indexes, change join order)
- Tune aggregation window sizes
- Change model inference batch size
- Adjust caching strategy
- Parallelize operations

## What You Cannot Do

- Modify `engine.py`, `azure_adapters.py` (read-only)
- Add new Python packages (locked dependencies)
- Change Azure resource SKUs
- Modify `config.yaml` credentials

## The Loop

LOOP FOREVER:
1. Read latest results.tsv (see what's working)
2. Propose an experiment (10-20 words describing the idea)
3. Modify `analysis.py`
4. `git commit -m "experiment: [your idea]"`
5. `python engine.py` (runs for exactly 10 min)
6. `grep "^metric:" run.log` → extract result
7. Log to results.tsv
8. If metric improved → keep commit, continue loop
9. If metric worse/same → `git reset --hard HEAD~1`, continue loop

## Stopping Criteria

You run until manually interrupted. If stuck (20+ consecutive discards), review the logs and try different ideas.

## Success Criteria

If you can achieve:
- Latency < 2 seconds (currently 5 sec)
- Cost < $3 per run (currently $4)
- 95% cache hit rate (currently 60%)

…then stop and await human approval to merge.
```

---

## Appendix: Azure Cost Estimate (Wave 1)

Assumptions:
- 12 experiments/day × 10 minutes each = 2 hours Synapse compute/day
- Data: 100 GB in ADLS Gen2
- Results stored in Cosmos DB (lightweight)

| Service | SKU | Cost/Month | Notes |
|---|---|---|---|
| **Synapse (Dedicated SQL Pool)** | 100 DWU (on-demand) | $600–800 | Scale down 40%: ~$300–400 |
| **ADLS Gen2 Storage** | Standard | $50 | 100 GB; auto-tiering to cool |
| **Application Insights** | Standard (1 GB/day) | $50 | Logs, metrics, traces |
| **Key Vault** | Standard | $10 | Credential storage |
| **Data Factory** | Consumption | $100 | Pipelines, triggers, runs |
| **Cost Management API** | Included | $0 | Query Azure costs |
| **Total** | | ~$800–1050/mo | ~ $27/day, ~$2/hour |

**Per experiment:** 10 min × $27/day = **~$0.19 per run**

**Budget: Allow $5 per experiment = 26× headroom** ✓

---

## References

- Inspired by: [autoresearch](https://github.com/karpathy/autoresearch)
- Azure ML best practices: Azure ML Ops documentation
- Data pipeline patterns: [Medallion Architecture](https://databricks.com/discover/articles/medallion-architecture)
- Autonomous systems design: [Research on AI Agents](https://arxiv.org/abs/2308.16069)
