# Azure Autonomous Data Platform — Technical Architecture

## System Context Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS RESEARCH LOOP                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Agent Controller (Claude + system prompt)               │  │
│  │  • Reads program.md (experiment boundaries)              │  │
│  │  • Reads results.tsv (latest metrics)                    │  │
│  │  • Proposes improvement                                  │  │
│  │  • Edits analysis.py                                     │  │
│  │  • Git commit + push                                     │  │
│  │  • Triggers experiment engine                            │  │
│  │  • Never asks for human approval                         │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                              │
│                   ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Experiment Engine (executor.py)                         │  │
│  │  • Load analysis.py code                                 │  │
│  │  • Set time budget (e.g., 10 min wall clock)             │  │
│  │  • Initialize Azure adapters                             │  │
│  │  • Run data pipeline                                     │  │
│  │  • Collect metrics in real-time                          │  │
│  │  • Return results JSON                                   │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                              │
│                   ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure Adapters Layer                                    │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  • Data Factory (trigger_pipeline)                       │  │
│  │  • Synapse SQL (execute_query)                           │  │
│  │  • Azure ML (run_inference)                              │  │
│  │  • Application Insights (log_metrics)                    │  │
│  │  • Cost Management API (get_run_cost)                    │  │
│  │  • ADLS Gen2 (read_checkpoint)                           │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                              │
│  ┌────────────────┴──────────────────────────────────────────┐  │
│  │                  AZURE SERVICES                           │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  Data Lake (ADLS Gen2)  │  Query (Synapse)  │  Compute   │  │
│  │  Monitoring (AppInsights)  │  Costs (CMgmt)  │  Security  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    RESULTS & VISIBILITY                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  results.tsv ◄──── Log Experiment       UI Dashboard ◄────      │
│  (git tracked)     (metric, status)     (React, trends)          │
│                                                                  │
│  Slack Alert  ◄──── When best improves                           │
│  Email Report ◄──── Daily summary                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dive

### 1. Agent Controller

**Responsibility:** Autonomous research loop — never requires human input once started.

**Implementation:** Claude API with structured system prompt.

```python
# Pseudocode

class AgentController:
    def __init__(self, program_md_path: str, repo_path: str, config: dict):
        self.program = self.read_program_md(program_md_path)
        self.repo = GitRepo(repo_path)
        self.engine = ExperimentEngine(config)
        
    def run_experiment_loop(self):
        """Run forever until interrupted (SIGTERM/SIGKILL)."""
        iteration = 0
        while True:
            iteration += 1
            
            # State assessment
            current_commit = self.repo.head()
            latest_results = self.read_results_tsv()
            baseline = latest_results[0]  # First row = baseline
            best = latest_results.best()
            
            # Prompt Claude with context
            context = {
                "program": self.program,
                "current_analysis_py": self.repo.read("analysis.py"),
                "baseline_metric": baseline.metric,
                "best_metric": best.metric,
                "recent_results": latest_results.tail(10),  # Last 10 experiments
                "iteration": iteration
            }
            
            # Get proposal from Claude
            proposal = self.claude_propose_experiment(context)
            
            # Apply changes
            self.repo.write("analysis.py", proposal["modified_code"])
            self.repo.commit(proposal["message"])
            
            # Execute experiment
            result = self.engine.run(self.repo.read("analysis.py"), 
                                     time_budget_sec=600,
                                     cost_limit_usd=5.0)
            
            # Evaluate: keep or discard?
            if result.metric < best.metric:
                # Improvement! Keep the commit.
                self.log_result(self.repo.head(), result, status="keep")
            else:
                # No improvement. Reset.
                self.repo.reset_hard(current_commit)
                self.log_result(current_commit, result, status="discard")
            
            # Alerts
            if result.metric < best.metric:
                self.send_slack_alert(f"New best: {result.metric}")
```

**System Prompt Template:**

```
You are an autonomous data pipeline researcher. Your job:

1. READ the program.md file for your experiment boundaries
2. UNDERSTAND the current analysis.py code and recent results
3. PROPOSE a concrete improvement (rewrite SQL, change params, etc.)
4. MODIFY ONLY analysis.py — nothing else
5. GIT COMMIT with clear message
6. The execution engine will run your code

CONSTRAINTS:
- You modify ONLY analysis.py
- Every change must be a concrete improvement idea
- Think incrementally; don't rewrite everything at once
- Simplicity is valued — prefer small, understandable changes

GOALS:
- Minimize: [metric from program.md]
- Respect: budget constraints, performance SLAs
- Document: why you're trying this change

LOOP FOREVER:
- Propose → Modify → Commit
- Engine runs and reports metric
- If better → keep exploring similar ideas
- If worse → try something different
- Never ask "should I continue?" — you run until interrupted

STATUS: Always assume you have full context. Never ask for clarification.
```

**Key Behaviors:**
- Never requests approval
- Reads results.tsv to understand what's working
- Proposes one experiment per iteration (not 10 at once)
- Commits before running (so diffs are clear)
- Handles crashes gracefully (log as "crash", reset, move on)

---

### 2. Experiment Engine (executor.py)

**Responsibility:** Isolated, reproducible execution of a single experiment with fixed time/cost budget.

```python
class ExperimentEngine:
    def __init__(self, config: dict):
        self.config = config
        self.azure = AzureAdapters(config)
        self.metrics = MetricsCollector()
        
    def run(self, analysis_code: str, time_budget_sec: int, cost_limit_usd: float):
        """
        Execute one experiment.
        
        Returns:
            {
                "metric": 1.234,  # Primary metric value
                "latency_sec": 45.2,
                "cost_usd": 2.30,
                "status": "success" | "timeout" | "oom" | "error",
                "error_msg": "...",
                "logs": "..."
            }
        """
        start = time.time()
        cost_tracker = CostTracker(self.azure.cost_api)
        
        try:
            # Load user's analysis code
            analysis_module = self._load_code(analysis_code)
            
            # Set up isolated environment
            with self.azure.create_checkpoint() as checkpoint:
                # Run their pipeline
                result = analysis_module.run_analysis(
                    data_source=checkpoint.data_path,
                    adapters=self.azure
                )
                
                # Measure metrics
                elapsed = time.time() - start
                cost = cost_tracker.get_cost()
                
                # Validate
                if elapsed > time_budget_sec:
                    return self._timeout_result()
                if cost > cost_limit_usd:
                    return self._budget_exceeded_result()
                    
                return {
                    "metric": result["primary_metric"],
                    "latency_sec": elapsed,
                    "cost_usd": cost,
                    "status": "success",
                    "result": result
                }
                
        except MemoryError as e:
            return {"metric": 0.0, "status": "oom", "error_msg": str(e)}
        except TimeoutError as e:
            return {"metric": 0.0, "status": "timeout", "error_msg": str(e)}
        except Exception as e:
            return {"metric": 0.0, "status": "error", "error_msg": str(e)}
        finally:
            self.metrics.flush()  # Write to Application Insights

    def _load_code(self, code_str: str):
        """Safely load user's Python code."""
        # Compile + execute in restricted namespace
        compiled = compile(code_str, "<analysis>", "exec")
        namespace = {
            "pandas": pd,
            "numpy": np,
            # ... whitelisted imports only
        }
        exec(compiled, namespace)
        return namespace
```

**Time Budget Enforcement:**

```python
class TimeoutManager:
    def __init__(self, budget_sec: int):
        self.budget = budget_sec
        self.start = time.time()
        
    def check(self):
        elapsed = time.time() - self.start
        if elapsed > self.budget:
            raise TimeoutError(f"Exceeded {self.budget}s budget")
            
    def remaining(self) -> float:
        return self.budget - (time.time() - self.start)
```

**Cost Tracking:**

```python
class CostTracker:
    """Polls Azure Cost Management API to get real-time spend."""
    
    def __init__(self, cost_api_client):
        self.client = cost_api_client
        self.start_time = datetime.utcnow()
        
    def get_cost(self) -> float:
        """Query Azure for actual spend since start_time."""
        result = self.client.query_costs(
            time_period={"start": self.start_time, "end": datetime.utcnow()}
        )
        return sum(r.cost for r in result.rows)
```

---

### 3. Azure Adapters (azure_adapters.py)

**Responsibility:** Abstracts Azure services; agent code doesn't care about Azure details.

```python
class AzureAdapters:
    """Unified interface to Azure services."""
    
    def __init__(self, config: dict):
        self.config = config
        self.data_factory = DataFactoryAdapter(config)
        self.synapse = SynapseAdapter(config)
        self.storage = ADLSAdapter(config)
        self.insights = AppInsightsAdapter(config)
        self.cost_api = CostManagementAdapter(config)
        self.ml = AzureMLAdapter(config)
        
    # Abstractions that analysis.py uses:
    
    def load_data(self, path: str) -> pd.DataFrame:
        """Load from ADLS Gen2."""
        return self.storage.read_parquet(path)
        
    def run_sql(self, query: str) -> pd.DataFrame:
        """Execute on Synapse."""
        return self.synapse.execute_query(query)
        
    def trigger_pipeline(self, pipeline_name: str) -> str:
        """Trigger Data Factory pipeline, return run_id."""
        return self.data_factory.trigger(pipeline_name)
        
    def wait_pipeline(self, run_id: str, timeout_sec: int = 600):
        """Wait for pipeline to complete."""
        return self.data_factory.wait(run_id, timeout_sec)
        
    def run_inference(self, model_id: str, data: pd.DataFrame) -> np.ndarray:
        """Batch inference via Azure ML."""
        return self.ml.batch_predict(model_id, data)
        
    def log_metric(self, name: str, value: float, dimensions: dict = None):
        """Log custom metric to Application Insights."""
        self.insights.log_metric(name, value, dimensions)
        
    def create_checkpoint(self):
        """Create a snapshot of data for reproducibility."""
        timestamp = datetime.utcnow().isoformat()
        checkpoint_path = f"s3://checkpoints/{timestamp}"
        return Checkpoint(checkpoint_path, self.storage)
```

**Example: SynapseAdapter**

```python
class SynapseAdapter:
    def __init__(self, config: dict):
        self.conn_str = config["synapse_connection_string"]
        
    def execute_query(self, sql: str) -> pd.DataFrame:
        """Run SQL against Synapse, return DataFrame."""
        with pyodbc.connect(self.conn_str) as conn:
            return pd.read_sql(sql, conn)
            
    def execute_stored_proc(self, proc_name: str, params: dict):
        """Run stored procedure (if pre-built by humans)."""
        # ... implementation
```

---

### 4. Results Tracker (results.tsv)

**Format:** Tab-separated values, git-tracked (but can be .gitignore'd if preferred).

```
commit	metric	cost_usd	latency_sec	status	description
a1b2c3d	1.5230	2.10	45.2	keep	baseline
a2c3d4e	1.4890	2.15	44.8	keep	optimized aggregation window
b3d4e5f	1.5010	2.05	50.1	discard	tried batch inference (worse)
c4e5f6g	1.4850	2.20	42.1	keep	parallel query execution
d5f6g7h	0.0000	0.0	0.0	crash	syntax error in query
e6g7h8i	1.4810	2.18	41.5	keep	cache hit optimization
```

**Properties:**
- One row per experiment
- Git history shows progression
- Can be analyzed in Excel or Python
- TSV (not CSV) to avoid comma issues in descriptions
- Status: `keep`, `discard`, or `crash`
- Metric is the primary optimization target (lower = better in this example, but configurable)

**Python API:**

```python
class ResultsTracker:
    def __init__(self, tsv_path: str):
        self.path = tsv_path
        self.df = pd.read_csv(tsv_path, sep="\t") if Path(tsv_path).exists() else None
        
    def log(self, commit_hash: str, metric: float, cost_usd: float, 
            latency_sec: float, status: str, description: str):
        """Append a result."""
        row = {
            "commit": commit_hash[:7],
            "metric": f"{metric:.4f}",
            "cost_usd": f"{cost_usd:.2f}",
            "latency_sec": f"{latency_sec:.1f}",
            "status": status,
            "description": description
        }
        # Append to TSV
        with open(self.path, "a") as f:
            f.write("\t".join(row.values()) + "\n")
            
    def best(self) -> dict:
        """Get row with best (lowest) metric."""
        return self.df.loc[self.df["metric"].idxmin()]
        
    def summary(self) -> dict:
        """Stats: baseline, best, improvement %."""
        baseline = self.df.iloc[0]
        best = self.best()
        improvement_pct = ((baseline["metric"] - best["metric"]) / baseline["metric"]) * 100
        return {
            "baseline": baseline,
            "best": best,
            "improvement_pct": improvement_pct,
            "num_experiments": len(self.df),
            "num_keeps": (self.df["status"] == "keep").sum()
        }
```

---

### 5. Program.md (Human-Editable)

Template that humans write to define agent boundaries:

```markdown
# [Project Name] Autonomous Pipeline Optimization

## Experiment Boundaries

**What the agent CAN do:**
- Rewrite SQL queries (add WHERE clauses, change joins, add indexes)
- Adjust aggregation granularity (hourly → 5-minute windows)
- Tune batch size for inference (8 → 16 → 32)
- Enable/disable caching layers
- Change aggregation functions (SUM → AVG, etc.)

**What the agent CANNOT do:**
- Modify engine.py, azure_adapters.py
- Add new Python packages
- Change Azure resource SKUs
- Access other data than /curated/sales_data/*

## Optimization Goals

**Primary Metric:** Query latency (seconds) — MINIMIZE
**Secondary Metric:** Cache hit rate (%) — MAXIMIZE
**Soft Constraint:** Cost < $3 per run

## Baseline Metrics (from first run)

- Latency: 120 seconds
- Cost: $2.50
- Cache hit: 30%

## Stopping Criteria

If you can achieve ALL of:
- Latency < 20 seconds
- Cache hit > 80%
- Cost < $1.50

…then stop and await human review.

## Ideas to Try (Optional Hints)

1. Add predicate pushdown to SQL (filter in query, not in Python)
2. Materialize common subqueries
3. Increase cache TTL
4. Batch inference requests
```

---

### 6. Analysis.py (Agent-Editable)

Template that agent modifies to optimize pipeline:

```python
# analysis.py — the ONLY file the agent modifies

import pandas as pd
import numpy as np
from typing import Dict, Any

def run_analysis(data_source: str, adapters) -> Dict[str, Any]:
    """
    Main entry point. Agent modifies this function.
    
    Args:
        data_source: Path to checkpoint data (ADLS)
        adapters: AzureAdapters instance (Synapse, ML, etc.)
        
    Returns:
        {
            "primary_metric": float,  # e.g., latency_sec
            "secondary_metrics": {...},
            "artifacts": {...}
        }
    """
    import time
    start = time.time()
    
    # Load raw data from checkpoint
    raw_sales = adapters.load_data(f"{data_source}/raw_sales.parquet")
    
    # Agent might optimize this SQL:
    query = """
    SELECT 
        DATE_TRUNC('hour', event_time) as hour,
        product_category,
        COUNT(*) as transaction_count,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_transaction
    FROM sales_events
    WHERE event_time >= DATEADD(DAY, -7, GETDATE())
    GROUP BY DATE_TRUNC('hour', event_time), product_category
    """
    
    aggregated = adapters.run_sql(query)
    
    # Run inference (agent might tune batch_size)
    predictions = adapters.run_inference(
        model_id="demand-forecast-v2",
        data=aggregated,
        batch_size=32  # Agent might change this
    )
    
    # Calculate primary metric
    elapsed = time.time() - start
    
    # Log metrics to Application Insights
    adapters.log_metric("query_latency_sec", elapsed)
    adapters.log_metric("row_count", len(aggregated))
    
    return {
        "primary_metric": elapsed,  # Minimize this
        "secondary_metrics": {
            "rows_processed": len(aggregated),
            "inference_time_sec": time.time() - start
        },
        "artifacts": {
            "aggregated_data": aggregated,
            "predictions": predictions
        }
    }
```

---

## Architectural Decision Records (ADRs)

### ADR-001: Single Editable File Model

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Agent needs clear scope to avoid breaking things
- Diff reviewing should be easy (show what agent changed)
- Prevent accidental modifications to critical infrastructure code

**Decision:**
Agent modifies ONLY `analysis.py`. All other files (`engine.py`, `azure_adapters.py`, `program.md`, `config.yaml`) are read-only.

**Alternatives Considered:**
- Allow agent to modify config.yaml (rejected: too risky, complex validation)
- Allow agent to add new Python files (rejected: diffs become unreadable)
- Allow multiple files, but with strict patterns (rejected: complexity not worth it)

**Consequences:**
- ✓ Diffs are easy to review
- ✓ Clear scope prevents chaos
- ✓ Rollback is trivial (`git reset`)
- ✗ Some optimizations may require infrastructure changes (must be pre-built by humans)

**Review in:** Q2 2025 (or if agent hits scope limitations)

---

### ADR-002: Fixed Time/Cost Budget per Experiment

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Without boundaries, agents might run long-tail experiments (optimize for 1% of cases)
- Azure costs are unpredictable without constraints
- Need fair comparison across experiments

**Decision:**
Every experiment runs for exactly T minutes (e.g., 10 min wall clock) with cost limit L (e.g., $5). Experiments that exceed either limit are terminated and logged as timeout/budget-exceeded.

**Alternatives Considered:**
- No time limit, just track cost (rejected: unpredictable AWS bills)
- Adaptive budget based on platform (rejected: makes runs incomparable)
- Soft budget (warn but don't kill) (rejected: still unpredictable)

**Consequences:**
- ✓ Predictable costs
- ✓ Fair comparison (all experiments have same compute budget)
- ✓ Encourages efficient code
- ✗ Some good ideas might be killed due to timeout (acceptable tradeoff)
- ✗ Platform-specific: an H100 gets more done in 10 min than a V100

**Review in:** After 500+ experiments (Dec 2025)

---

### ADR-003: Git Commit per Experiment

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Need full audit trail (compliance, debugging)
- Need to compare experiments code-to-code
- Need rollback capability

**Decision:**
Agent commits every experiment before running it. If experiment fails, `git reset --hard HEAD~1` reverts. If succeeds, commit is kept.

**Alternatives Considered:**
- Commit only on success (rejected: can't see what failed)
- No git tracking (rejected: no audit trail)
- Commit after run (rejected: harder to rollback)

**Consequences:**
- ✓ Full audit trail
- ✓ Easy rollback
- ✓ Code diffs are clear
- ✗ Git history becomes long (1000+ commits/week possible)
- ✗ Requires branch strategy (run branch ≠ production branch)

**Review in:** Q2 2025 (git repo size concern)

---

### ADR-004: TSV Results Tracker (vs. Database)

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Need lightweight results tracking
- Need human readability (inspect in Excel)
- Need git-friendly format

**Decision:**
Results logged to `results.tsv` (tab-separated values). One row per experiment. Human-readable, git-friendly, no database required.

**Alternatives Considered:**
- Database (Cosmos DB) (rejected: overkill, adds infra dependency)
- JSON file (rejected: harder to query/sort)
- CloudWatch / Application Insights only (rejected: harder to compare locally)

**Consequences:**
- ✓ No database dependency
- ✓ Readable in any text editor
- ✓ Easy to version control
- ✗ Doesn't scale to 100k+ rows (but 100k rows = ~300 experiments/day for 1 year, acceptable)
- ✗ No real-time querying (acceptable: results are batch)

**Migrate to database if:** results.tsv exceeds 100k rows (late 2025 probably)

---

### ADR-005: Autonomous Agent (Never Pause)

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Humans expect to leave agent running overnight
- Asking "should I continue?" breaks the loop
- Autonomy is the whole point

**Decision:**
Agent runs continuously until manually interrupted (SIGTERM). It never asks for human approval or pauses.

**Alternatives Considered:**
- Pause between experiments for human review (rejected: defeats the purpose)
- Ask for feedback (rejected: humans might be asleep)
- Auto-stop when metric plateaus (rejected: hides variance)

**Consequences:**
- ✓ Unattended overnight runs work as designed
- ✓ No bottleneck on human feedback
- ✓ Agent can explore more ideas
- ✗ Risk: agent wastes time on dead ends (mitigated by results tracking, human can interrupt)
- ✗ Cost spiral if budget constraint fails (mitigated by cost limit enforcement)

**Safeguard:** Hard cost limit + timeout enforcement prevents runaway spend.

---

### ADR-006: Azure Services Stack

**Status:** Accepted  
**Date:** 2025-09-01

**Context:**
- Team already uses Azure
- Multi-region support required
- Cost-conscious (prefer managed services)

**Decision:**
Core stack: ADLS Gen2 (storage) + Synapse SQL (query) + Application Insights (observability) + Cost Management API (tracking). Secondary: Data Factory (orchestration), Azure ML (inference).

**Alternatives Considered:**
- AWS (rejected: team skill is Azure)
- Databricks (rejected: added cost, less control)
- BigQuery (rejected: team is Azure-first)

**Consequences:**
- ✓ Leverages existing Azure investment
- ✓ Managed services reduce ops burden
- ✓ Good audit/compliance features
- ✗ Potential vendor lock-in (acceptable for 2-3 year horizon)
- ✗ Some advanced features cost extra (Synapse Spark, etc.)

**Review in:** If multi-cloud becomes requirement.

---

## Deployment Architecture

### Infrastructure as Code (Terraform)

```hcl
# core.tf

resource "azurerm_resource_group" "autopipeline" {
  name     = "rg-autopipeline-${var.environment}"
  location = var.azure_region
}

resource "azurerm_storage_account" "datalake" {
  name                     = "st${var.project}datalake${var.environment}"
  resource_group_name      = azurerm_resource_group.autopipeline.name
  location                 = azurerm_resource_group.autopipeline.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true  # Enable Data Lake
}

resource "azurerm_sql_server" "synapse" {
  name                         = "syn-${var.project}-${var.environment}"
  resource_group_name          = azurerm_resource_group.autopipeline.name
  location                     = azurerm_resource_group.autopipeline.location
  version                      = "12.0"
  administrator_login          = var.synapse_admin_username
  administrator_login_password = var.synapse_admin_password
}

resource "azurerm_synapse_sql_pool" "analytics" {
  name                 = "analytics"
  synapse_workspace_id = azurerm_synapse_workspace.this.id
  sku_name             = "DW500c"  # Adjustable
  create_mode          = "Default"
}

resource "azurerm_key_vault" "secrets" {
  name                        = "kv-${var.project}-${var.environment}"
  location                    = azurerm_resource_group.autopipeline.location
  resource_group_name         = azurerm_resource_group.autopipeline.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true
}

resource "azurerm_application_insights" "monitoring" {
  name                = "ai-${var.project}-${var.environment}"
  location            = azurerm_resource_group.autopipeline.location
  resource_group_name = azurerm_resource_group.autopipeline.name
  application_type    = "general"
}
```

### Authentication & RBAC

Agent runs with managed identity:

```hcl
resource "azurerm_user_assigned_identity" "agent" {
  name                = "agent-${var.project}"
  resource_group_name = azurerm_resource_group.autopipeline.name
  location            = azurerm_resource_group.autopipeline.location
}

# Grant agent permissions to Synapse, Storage, Key Vault, etc.
resource "azurerm_role_assignment" "agent_synapse" {
  scope              = azurerm_synapse_workspace.this.id
  role_definition_name = "SQL Administrator"  # or more restricted role
  principal_id       = azurerm_user_assigned_identity.agent.principal_id
}
```

---

## Monitoring & Alerting

### Application Insights Integration

Agent logs all metrics:

```python
# In engine.py

class MetricsCollector:
    def __init__(self, insights_client):
        self.insights = insights_client
        self.metrics = {}
        
    def record(self, name: str, value: float, dimensions: dict = None):
        self.metrics[name] = (value, dimensions)
        
    def flush(self):
        for name, (value, dimensions) in self.metrics.items():
            self.insights.track_metric(name, value, properties=dimensions)

# Usage:
metrics.record("query_latency_sec", 45.2, {"query_type": "aggregation"})
metrics.record("cache_hit_ratio", 0.75)
metrics.record("cost_usd", 2.30)
metrics.flush()
```

### Alerts

```hcl
# alerts.tf

resource "azurerm_monitor_metric_alert" "cost_spike" {
  name                = "alert-cost-spike"
  resource_group_name = azurerm_resource_group.autopipeline.name
  scopes              = [azurerm_application_insights.monitoring.id]
  
  criteria {
    metric_name      = "cost_usd"
    operator         = "GreaterThan"
    threshold        = 10  # Alert if single experiment > $10
    aggregation      = "Maximum"
  }
  
  action {
    action_group_id = azurerm_monitor_action_group.oncall.id
  }
}

resource "azurerm_monitor_metric_alert" "experiment_failure_rate" {
  name                = "alert-high-crash-rate"
  resource_group_name = azurerm_resource_group.autopipeline.name
  scopes              = [azurerm_application_insights.monitoring.id]
  
  criteria {
    metric_name      = "experiments_crashed"
    operator         = "GreaterThan"
    threshold        = 5  # Alert if > 5 crashes in last hour
  }
  
  action {
    action_group_id = azurerm_monitor_action_group.oncall.id
  }
}
```

---

## Security Considerations

| Concern | Mitigation |
|---|---|
| **Rogue code execution** | Analyze `analysis.py` diffs before auto-merge; disable auto-merge if complexity metric too high |
| **Data exfiltration** | Agent runs with minimal IAM (read-only on sensitive tables); monitor all API calls |
| **Cost runaway** | Hard limit on cost per experiment; auto-shutdown if monthly spend exceeds threshold |
| **Audit trail** | Every change committed + logged to Application Insights; never delete git history |
| **Secret leakage** | Secrets in Key Vault, accessed via managed identity; never hardcoded in config.yaml |

---

## Performance Benchmarks (Target)

| Metric | Target | Rationale |
|---|---|---|
| **Startup overhead** | < 10 sec | Time to load, connect, init |
| **Query compilation** | < 5 sec | SQL parsing, plan optimization |
| **Actual work** | 590 sec (of 600) | Maximum useful work per 10-min budget |
| **Cooldown** | < 5 sec | Logging, cleanup, commit |
| **Cost per run** | < $2 | Actual: ~0.33/min × 10 = $3.30 (within $5 budget) |
| **Experiment throughput** | 12-15/day | 600 sec per run + 10% overhead = ~5 min per cycle |

---

## References

- **Autoresearch Paper:** https://github.com/karpathy/autoresearch
- **Azure Synapse Best Practices:** Microsoft Docs
- **Cost Optimization:** Azure Well-Architected Review
- **Python Code Safety:** [Securing Python Code Execution](https://docs.python.org/3/library/code.html)
