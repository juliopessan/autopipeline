# Azure Autonomous Data Platform — Architecture Diagrams

## 1. System Context (High Level)

```mermaid
graph TB
    subgraph "🤖 Autonomous Research Loop"
        Agent["Claude Agent<br/>(Continuous)"]
        Program["program.md<br/>(Boundaries)"]
        Results["results.tsv<br/>(History)"]
        Code["analysis.py<br/>(Modifications)"]
    end
    
    Agent -->|reads| Program
    Agent -->|reads| Results
    Agent -->|modifies| Code
    
    subgraph "⚙️ Execution Layer"
        Engine["executor.py<br/>(Time/Cost Budget)"]
        Adapters["azure_adapters.py<br/>(Azure Abstraction)"]
    end
    
    Code -->|executes in| Engine
    Engine -->|uses| Adapters
    
    subgraph "☁️ Azure Services"
        ADLS["ADLS Gen2<br/>(Data Lake)"]
        Synapse["Synapse SQL<br/>(Query Engine)"]
        ML["Azure ML<br/>(Inference)"]
        Insights["App Insights<br/>(Monitoring)"]
        CostAPI["Cost Mgmt API<br/>(Tracking)"]
    end
    
    Adapters -->|stores| ADLS
    Adapters -->|queries| Synapse
    Adapters -->|runs| ML
    Engine -->|logs to| Insights
    Engine -->|checks| CostAPI
    
    subgraph "📊 Visibility & Control"
        TSV["results.tsv<br/>(git-tracked)"]
        Dashboard["Web Dashboard<br/>(Trends)"]
        Slack["Slack<br/>(Alerts)"]
    end
    
    Engine -->|logs results to| TSV
    TSV -->|powers| Dashboard
    Engine -->|notifies| Slack
    
    subgraph "🔄 Feedback Loop"
        Git["Git Repo<br/>(Audit Trail)"]
    end
    
    Code -->|committed| Git
    Code -.->|pulled from| Git
    
    style Agent fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style Engine fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style ADLS fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Dashboard fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 2. Agent Loop (Detailed Sequence)

```mermaid
sequenceDiagram
    participant Human
    participant Agent as Claude Agent
    participant Git as Git Repo
    participant Engine as Executor
    participant Azure as Azure Services
    participant Monitor as Monitoring
    
    Human->>Agent: "Start autonomous loop"
    loop Every 5-10 minutes
        Agent->>Git: Read program.md
        Agent->>Git: Read results.tsv
        Agent->>Git: Read analysis.py
        Agent->>Agent: Propose improvement
        Agent->>Git: Modify analysis.py
        Agent->>Git: git commit
        
        Agent->>Engine: Run experiment
        activate Engine
        Engine->>Azure: Load checkpoint data
        Engine->>Azure: Execute pipeline
        Engine->>Azure: Run inference
        Engine->>Monitor: Log metrics
        Monitor->>Monitor: Calculate cost
        Engine-->>Agent: Return metric + cost + status
        deactivate Engine
        
        Agent->>Agent: Compare to best
        
        alt Metric Improved
            Agent->>Monitor: Log "keep"
            Note over Agent: Commit stays
        else Metric Same/Worse
            Agent->>Git: git reset --hard HEAD~1
            Agent->>Monitor: Log "discard"
            Note over Agent: Commit reverted
        end
    end
    
    Human->>Agent: SIGTERM (interrupt)
    Agent->>Human: "Stopped. 50 experiments completed."
```

---

## 3. File Structure & Ownership

```mermaid
graph LR
    subgraph Modifiable["🔴 Agent Modifies"]
        A["analysis.py"]
    end
    
    subgraph ReadOnly["🟢 Read-Only (Human Review)"]
        B["engine.py"]
        C["azure_adapters.py"]
        D["config.yaml"]
        E["requirements.txt"]
    end
    
    subgraph Human["👤 Human Edits"]
        F["program.md"]
        G["README.md"]
    end
    
    subgraph Generated["📊 Generated"]
        H["results.tsv"]
        I["run.log"]
    end
    
    subgraph VCS["🔒 Git-Tracked"]
        J[".git/"]
    end
    
    A -->|commit| J
    B -->|commit| J
    F -->|commit| J
    H -.->|can commit or .gitignore| J
    
    style A fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style B fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style F fill:#fff9c4,stroke:#f57f17,stroke-width:2px
```

---

## 4. Experiment Execution Pipeline

```mermaid
graph TD
    A["START: New experiment"] -->|Agent proposes| B["Modify analysis.py"]
    B --> C["git commit"]
    C -->|Engine starts| D["Load user code"]
    D --> E["Create checkpoint"]
    E --> F["Execute analysis.run_analysis"]
    
    F --> G{Timeout?}
    G -->|YES| H["TIMEOUT<br/>status=timeout"]
    G -->|NO| I{Budget Exceeded?}
    
    I -->|YES| J["BUDGET EXCEEDED<br/>status=budget_exceeded"]
    I -->|NO| K{Crash?}
    
    K -->|YES| L["CRASH<br/>status=crash"]
    K -->|NO| M["SUCCESS<br/>Extract metric"]
    
    M --> N["Log to results.tsv"]
    N --> O{Metric improved?}
    
    O -->|YES| P["KEEP<br/>Commit stays"]
    O -->|NO| Q["DISCARD<br/>git reset"]
    
    H --> R["Log result"]
    J --> R
    L --> R
    P --> S["END: Ready for next experiment"]
    Q --> S
    
    style A fill:#bbdefb,stroke:#1565c0
    style P fill:#c8e6c9,stroke:#2e7d32
    style Q fill:#ffcdd2,stroke:#c62828
    style H fill:#ffe0b2,stroke:#e65100
    style L fill:#f8bbd0,stroke:#ad1457
```

---

## 5. Azure Integration Layer

```mermaid
graph TB
    subgraph UserCode["analysis.py (Agent-Written)"]
        A["adapters.load_data<br/>adapters.run_sql<br/>adapters.run_inference<br/>adapters.log_metric"]
    end
    
    subgraph AdapterLayer["azure_adapters.py (Abstraction)"]
        B["DataLakeAdapter"]
        C["SynapseAdapter"]
        D["MLAdapter"]
        E["MetricsAdapter"]
        F["CostAdapter"]
        G["KeyVaultAdapter"]
    end
    
    subgraph Azure["Azure Services"]
        H["ADLS Gen2<br/>(read_parquet)"]
        I["Synapse SQL<br/>(execute_query)"]
        J["Azure ML<br/>(batch_predict)"]
        K["App Insights<br/>(track_metric)"]
        L["Cost Mgmt<br/>(get_cost)"]
        M["Key Vault<br/>(get_secret)"]
    end
    
    A -->|calls| B
    A -->|calls| C
    A -->|calls| D
    A -->|calls| E
    A -->|calls| F
    A -->|calls| G
    
    B -->|REST API| H
    C -->|ODBC/SQL| I
    D -->|REST API| J
    E -->|OpenTelemetry| K
    F -->|REST API| L
    G -->|REST API| M
    
    style A fill:#e0e0e0,stroke:#212121,stroke-width:2px
    style AdapterLayer fill:#f5f5f5,stroke:#424242,stroke-width:2px
    style Azure fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

---

## 6. Results Tracking (TSV Format)

```mermaid
graph LR
    A["Experiment 1<br/>Baseline"] -->|commit| B["a1b2c3d"]
    A -->|metric| C["1.5230"]
    A -->|cost| D["$2.10"]
    A -->|status| E["keep"]
    A -->|description| F["baseline"]
    
    B --> G["results.tsv<br/>─────<br/>a1b2c3d | 1.5230 | 2.10 | keep | baseline<br/>a2c3d4e | 1.4890 | 2.15 | keep | opt join<br/>b3d4e5f | 1.5010 | 2.05 | discard | tried batch<br/>c4e5f6g | 1.4850 | 2.20 | keep | parallel<br/>..."]
    
    G -->|git-tracked| H["Audit Trail<br/>● Full history<br/>● Diffs reviewable<br/>● Revertible"]
    
    H -->|analyze| I["Dashboard<br/>● Trend chart<br/>● Top experiments<br/>● Improvement %"]
    
    style G fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style I fill:#e0f2f1,stroke:#00695c,stroke-width:2px
```

---

## 7. Deployment Architecture

```mermaid
graph TB
    subgraph Development["👨‍💻 Development"]
        A["Local repo<br/>Clone + test"]
    end
    
    subgraph CI["🔄 CI/CD (Azure DevOps)"]
        B["Test agent loop<br/>Validate Python<br/>Build Docker"]
    end
    
    subgraph Container["📦 Container"]
        C["Docker image<br/>python:3.10<br/>+ requirements<br/>+ code"]
    end
    
    subgraph Registry["📝 Registry"]
        D["Azure Container Registry<br/>autpipeline:latest"]
    end
    
    subgraph Cloud["☁️ Azure"]
        E["Container Instance<br/>or VM"]
        F["ADLS Gen2"]
        G["Synapse"]
        H["Key Vault"]
        I["App Insights"]
    end
    
    subgraph Monitoring["📊 Monitoring"]
        J["results.tsv"]
        K["Slack alerts"]
        L["Dashboard"]
    end
    
    A -->|git push| CI
    CI -->|builds| C
    C -->|pushed| D
    D -->|deployed| E
    E -->|runs agent| E
    E -->|uses| F
    E -->|uses| G
    E -->|uses| H
    E -->|logs to| I
    E -->|writes| J
    E -->|notifies| K
    J -->|updates| L
    
    style A fill:#bbdefb
    style E fill:#fff3e0
    style L fill:#c8e6c9
```

---

## 8. KPI & Health Dashboard

```mermaid
graph TB
    subgraph Metrics["📊 Real-Time Metrics"]
        A["Total Experiments"] --> B["120 today"]
        C["Success Rate"] --> D["85%"]
        E["Improvement %"] --> F["+7.3% vs baseline"]
        G["Cost Trend"] --> H["Stable ($2.15/run)"]
    end
    
    subgraph Trends["📈 Trends"]
        I["Last 24h"] --> J["45 experiments<br/>12 improvements<br/>3 crashes"]
        K["Last 7d"] --> L["350 experiments<br/>47 improvements<br/>+4.8% metric"]
        M["Last 30d"] --> N["1500 experiments<br/>180 improvements<br/>+8.2% metric"]
    end
    
    subgraph Health["🟢 System Health"]
        O["Agent Status"] --> P["Running"]
        Q["Cost Status"] --> R["Within budget"]
        S["Crash Rate"] --> T["2% (healthy)"]
        U["Last Improvement"] --> V["45 min ago"]
    end
    
    subgraph Alerts["🔔 Active Alerts"]
        W["New Best Found"] -.->|Slack| X["📢 Metric: 1.428"]
        Y["Crashes Spiked"] -.->|Email| Z["⚠️ 5 in last hour"]
    end
    
    style B fill:#c8e6c9
    style D fill:#c8e6c9
    style F fill:#c8e6c9
    style H fill:#c8e6c9
    style P fill:#c8e6c9
    style R fill:#c8e6c9
    style Z fill:#ffcdd2
```

---

## 9. Multi-Pipeline Orchestration (Future)

```mermaid
graph TB
    subgraph Pipeline1["Pipeline 1: Sales"]
        A["Agent 1"]
        B["program.md (sales)"]
        C["analysis.py (sales)"]
    end
    
    subgraph Pipeline2["Pipeline 2: Customer360"]
        D["Agent 2"]
        E["program.md (cust)"]
        F["analysis.py (cust)"]
    end
    
    subgraph Pipeline3["Pipeline 3: Inventory"]
        G["Agent 3"]
        H["program.md (inv)"]
        I["analysis.py (inv)"]
    end
    
    subgraph Orchestrator["🎼 Central Orchestrator"]
        J["Resource Manager<br/>Queue experiments<br/>Allocate compute"]
        K["Cross-Learning<br/>Share techniques<br/>Recommend ideas"]
    end
    
    subgraph Shared["Shared Layer"]
        L["ADLS Gen2<br/>(all data)"]
        M["Synapse<br/>(shared pool)"]
        N["Central Metrics<br/>(all results)"]
    end
    
    A -->|controlled by| J
    D -->|controlled by| J
    G -->|controlled by| J
    J -->|learns from| K
    K -->|suggests improvements| A
    K -->|suggests improvements| D
    K -->|suggests improvements| G
    C -->|uses| L
    F -->|uses| L
    I -->|uses| L
    C -->|queries| M
    F -->|queries| M
    I -->|queries| M
    C -->|logs| N
    F -->|logs| N
    I -->|logs| N
    
    style J fill:#b3e5fc,stroke:#0277bd,stroke-width:2px
    style K fill:#f0f4c3,stroke:#9e9d24,stroke-width:2px
    style L fill:#ffe0b2,stroke:#e65100,stroke-width:2px
```

---

## 10. Decision Framework (When to Use)

```mermaid
graph TD
    A["New data optimization<br/>challenge?"] -->|YES| B["Good fit for<br/>autonomous platform"]
    A -->|NO| C["Traditional approach"]
    
    B --> D["Is optimization<br/>space large?"]
    D -->|YES| E["Will benefit<br/>from agent exploration"]
    D -->|NO| F["May be too simple<br/>for agent"]
    
    E --> G["Can you define<br/>clear boundaries?"]
    G -->|YES| H["✅ LAUNCH<br/>Build platform"]
    G -->|NO| I["❌ WAIT<br/>Clarify scope first"]
    
    H --> J["Start small<br/>1 pipeline"]
    J --> K["Run 100+ experiments"]
    K --> L["Validate improvements<br/>in production"]
    L --> M["Scale to 5-10 pipelines"]
    
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style B fill:#bbdefb,stroke:#1565c0,stroke-width:2px
```

---

## 11. Risk Mitigation Posture

```mermaid
graph LR
    subgraph Risks["🔴 Potential Risks"]
        A["Agent produces<br/>bad code"]
        B["Azure costs<br/>spiral"]
        C["Audit trail<br/>lost"]
        D["Agent gets<br/>stuck"]
    end
    
    subgraph Controls["🟢 Controls"]
        A -->|Mitigation| A1["Code isolation<br/>Diff review<br/>Time budget"]
        B -->|Mitigation| B1["Cost API limit<br/>Budget enforcement<br/>Alerts"]
        C -->|Mitigation| C1["Git history<br/>App Insights logs<br/>Immutable TSV"]
        D -->|Mitigation| D1["Monitoring<br/>Auto-restart<br/>Manual intervention"]
    end
    
    subgraph Residual["🟡 Residual Risk"]
        A1 -.->|Low| E["Unlikely to cause<br/>production outage"]
        B1 -.->|Low| F["Cost overrun<br/>< 2% probability"]
        C1 -.->|Very Low| G["Lost audit trail<br/>< 0.1% probability"]
        D1 -.->|Medium| H["Agent plateaus<br/>Requires intervention"]
    end
    
    style A1 fill:#fff9c4
    style E fill:#c8e6c9
    style H fill:#ffe0b2
```

---

## 12. Success Metrics Over Time

```mermaid
graph TD
    subgraph Day1["📅 Day 1-3"]
        A["✅ Setup complete"]
        B["✅ First 5 experiments run"]
        C["✅ Baseline established"]
    end
    
    subgraph Week1["📅 Week 1"]
        D["✅ 50+ experiments"]
        E["✅ 0 manual intervention"]
        F["✅ No crashes (or tolerable)"]
    end
    
    subgraph Week2["📅 Week 2"]
        G["✅ +2% improvement"]
        H["✅ 100+ experiments"]
        I["✅ Pattern recognition<br/>Agent learning"]
    end
    
    subgraph Week3["📅 Week 3"]
        J["✅ +5% improvement<br/>sustained"]
        K["✅ Team confident<br/>operating it"]
        L["✅ Ready to scale"]
    end
    
    subgraph Month2["📅 Month 2"]
        M["✅ 5+ pipelines running"]
        N["✅ +8% aggregate improvement"]
        O["✅ ROI positive"]
    end
    
    A --> D
    B --> D
    C --> D
    D --> G
    E --> G
    F --> G
    G --> J
    H --> J
    I --> J
    J --> M
    K --> M
    L --> M
    
    style A fill:#c8e6c9,stroke:#2e7d32
    style J fill:#c8e6c9,stroke:#2e7d32
    style M fill:#c8e6c9,stroke:#2e7d32
```

---

## Document Summary

These diagrams illustrate:
1. **System Context** — The big picture
2. **Agent Loop** — How it actually works
3. **File Ownership** — What agent can/cannot change
4. **Execution Pipeline** — Every experiment
5. **Azure Integration** — Service abstractions
6. **Results Tracking** — Audit trail
7. **Deployment** — Getting to production
8. **KPI Dashboard** — Observability
9. **Multi-Pipeline** — Future scaling
10. **Decision Framework** — When to use
11. **Risk Mitigation** — Safety guardrails
12. **Success Timeline** — What "done" looks like

**Use these as references when** designing architecture, explaining to stakeholders, or debugging issues.
