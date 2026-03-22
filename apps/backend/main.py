#!/usr/bin/env python3
"""
Azure Autonomous Data Platform - FastAPI Backend
Main application with Azure integration
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks
from fastapi.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS
# ============================================================================

class ProgramUpdate(BaseModel):
    """Program.md configuration"""
    name: str
    constraints: str
    optimization_goal: str
    metric_name: str
    baseline_value: float
    target_value: float
    max_iterations: int

class ExperimentCreate(BaseModel):
    """Request to create experiment"""
    program_id: str
    analysis_code: str
    description: str

class ExperimentResult(BaseModel):
    """Experiment result"""
    id: str
    program_id: str
    metric: float
    cost_usd: float
    wall_time_sec: float
    status: str  # success, timeout, crash, budget_exceeded
    description: str
    created_at: datetime
    commit_hash: Optional[str] = None

class ProgramMetrics(BaseModel):
    """Program metrics summary"""
    total_experiments: int
    successful: int
    crashes: int
    best_metric: float
    baseline_metric: float
    improvement_pct: float
    success_rate: float
    avg_cost: float

class DashboardData(BaseModel):
    """Dashboard data"""
    programs: List[Dict[str, Any]]
    recent_experiments: List[ExperimentResult]
    system_health: Dict[str, Any]
    cost_summary: Dict[str, Any]

# ============================================================================
# AZURE SERVICES CLIENT
# ============================================================================

class AzureServicesClient:
    """Unified Azure services client"""
    
    def __init__(self):
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "")
        self.resource_group = os.getenv("AZURE_RESOURCE_GROUP", "rg-autopipeline")
        self.synapse_server = os.getenv("SYNAPSE_SERVER", "")
        self.synapse_db = os.getenv("SYNAPSE_DATABASE", "analytics")
        self.storage_account = os.getenv("STORAGE_ACCOUNT", "")
        self.insights_key = os.getenv("APPINSIGHTS_KEY", "")
        
        # Mock mode for demo
        self.mock_mode = not all([
            self.subscription_id,
            self.synapse_server,
            self.storage_account
        ])
        
        if self.mock_mode:
            logger.warning("Running in MOCK mode (Azure credentials not fully configured)")
        
    async def execute_query(self, query: str) -> List[Dict]:
        """Execute query on Synapse SQL Pool"""
        if self.mock_mode:
            return self._mock_query_result(query)
        
        try:
            # Real: Use pyodbc to connect to Synapse
            # import pyodbc
            # connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};" \
            #     f"Server={self.synapse_server};Database={self.synapse_db};" \
            #     f"Authentication=ActiveDirectoryMsi;Encrypt=yes;TrustServerCertificate=no;"
            # with pyodbc.connect(connection_string) as conn:
            #     cursor = conn.cursor()
            #     cursor.execute(query)
            #     return cursor.fetchall()
            
            logger.info(f"Executing query on Synapse: {query[:100]}...")
            return []
        except Exception as e:
            logger.error(f"Synapse query error: {e}")
            raise
    
    async def load_data(self, path: str) -> Dict[str, Any]:
        """Load data from ADLS Gen2"""
        if self.mock_mode:
            return {"rows": 1000, "size_mb": 150, "path": path}
        
        try:
            # Real: Use Azure SDK
            # from azure.storage.filedatalake import DataLakeServiceClient
            # service_client = DataLakeServiceClient.from_connection_string(...)
            
            logger.info(f"Loading data from ADLS: {path}")
            return {}
        except Exception as e:
            logger.error(f"ADLS load error: {e}")
            raise
    
    async def log_metric(self, metric_name: str, value: float, 
                        dimensions: Optional[Dict] = None) -> bool:
        """Log metric to Application Insights"""
        if self.mock_mode:
            logger.info(f"[MOCK] Logging metric: {metric_name}={value}")
            return True
        
        try:
            # Real: Use Azure Monitor SDK
            # from azure.monitor.opentelemetry import configure_azure_monitor
            
            logger.info(f"Logging metric to AppInsights: {metric_name}={value}")
            return True
        except Exception as e:
            logger.error(f"AppInsights error: {e}")
            raise
    
    async def get_cost(self, start_time: datetime, end_time: datetime) -> float:
        """Get Azure cost for time period"""
        if self.mock_mode:
            import random
            return round(random.uniform(1.5, 3.5), 2)
        
        try:
            # Real: Use Cost Management API
            # from azure.mgmt.costmanagement import CostManagementClient
            
            logger.info(f"Fetching costs from {start_time} to {end_time}")
            return 2.50
        except Exception as e:
            logger.error(f"Cost API error: {e}")
            raise
    
    async def get_storage_snapshot(self) -> str:
        """Create checkpoint/snapshot for reproducibility"""
        if self.mock_mode:
            timestamp = datetime.utcnow().isoformat()
            return f"checkpoint-{timestamp}"
        
        try:
            # Real: Create snapshot in ADLS
            logger.info("Creating storage snapshot")
            return "snapshot-id"
        except Exception as e:
            logger.error(f"Snapshot error: {e}")
            raise
    
    def _mock_query_result(self, query: str) -> List[Dict]:
        """Generate mock query results"""
        return [
            {"id": 1, "value": 100, "timestamp": "2025-03-22T10:00:00"},
            {"id": 2, "value": 102, "timestamp": "2025-03-22T10:05:00"},
            {"id": 3, "value": 101, "timestamp": "2025-03-22T10:10:00"},
        ]

# ============================================================================
# EXPERIMENT ENGINE
# ============================================================================

class ExperimentEngine:
    """Executes experiments with budget enforcement"""
    
    def __init__(self, azure_client: AzureServicesClient):
        self.azure = azure_client
        self.time_budget_sec = 600  # 10 minutes
        self.cost_limit_usd = 5.0
    
    async def run_experiment(self, analysis_code: str, program_id: str) -> ExperimentResult:
        """Execute experiment and return results"""
        import time
        import hashlib
        
        start_time = datetime.utcnow()
        start_wall = time.time()
        commit_hash = hashlib.sha1(analysis_code.encode()).hexdigest()[:7]
        
        try:
            # Create checkpoint
            checkpoint = await self.azure.get_storage_snapshot()
            
            # Execute analysis code (in real: subprocess with timeout)
            result = await self._execute_code(analysis_code, checkpoint)
            
            # Get cost
            cost = await self.azure.get_cost(start_time, datetime.utcnow())
            wall_time = time.time() - start_wall
            
            # Validate budgets
            if wall_time > self.time_budget_sec:
                return ExperimentResult(
                    id=f"exp_{commit_hash}",
                    program_id=program_id,
                    metric=0.0,
                    cost_usd=0.0,
                    wall_time_sec=wall_time,
                    status="timeout",
                    description="Exceeded time budget",
                    created_at=start_time,
                    commit_hash=commit_hash
                )
            
            if cost > self.cost_limit_usd:
                return ExperimentResult(
                    id=f"exp_{commit_hash}",
                    program_id=program_id,
                    metric=0.0,
                    cost_usd=cost,
                    wall_time_sec=wall_time,
                    status="budget_exceeded",
                    description="Exceeded cost budget",
                    created_at=start_time,
                    commit_hash=commit_hash
                )
            
            # Success
            return ExperimentResult(
                id=f"exp_{commit_hash}",
                program_id=program_id,
                metric=result.get("metric", 0.0),
                cost_usd=cost,
                wall_time_sec=wall_time,
                status="success",
                description=result.get("description", ""),
                created_at=start_time,
                commit_hash=commit_hash
            )
            
        except Exception as e:
            logger.error(f"Experiment error: {e}")
            wall_time = time.time() - start_wall
            return ExperimentResult(
                id=f"exp_{commit_hash}",
                program_id=program_id,
                metric=0.0,
                cost_usd=0.0,
                wall_time_sec=wall_time,
                status="crash",
                description=str(e),
                created_at=start_time,
                commit_hash=commit_hash
            )
    
    async def _execute_code(self, code: str, checkpoint: str) -> Dict[str, Any]:
        """Execute user's analysis code"""
        import random
        import time
        
        # Simulate execution
        time.sleep(0.5)
        
        # Mock result: simulate improvement over time
        improvement = random.uniform(0.98, 1.02)
        metric = 120.0 * improvement
        
        return {
            "metric": metric,
            "description": "Executed successfully",
            "checkpoint": checkpoint
        }

# ============================================================================
# CLAUDE AGENT
# ============================================================================

class AutonomousAgent:
    """Claude-powered autonomous agent"""
    
    def __init__(self, engine: ExperimentEngine):
        self.engine = engine
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.is_running = False
    
    async def get_proposal(self, program: Dict[str, Any], 
                          recent_results: List[ExperimentResult]) -> Optional[Dict]:
        """Ask Claude for experiment proposal"""
        
        try:
            context = self._build_context(program, recent_results)
            
            response = self.client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": context
                }]
            )
            
            response_text = response.content[0].text
            
            # Parse JSON from response
            import json
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                proposal = json.loads(json_str)
                return proposal
            
            return None
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return None
    
    def _build_context(self, program: Dict, results: List) -> str:
        """Build context for Claude"""
        recent = results[-5:] if results else []
        best = min([r.metric for r in recent], default=float("inf"))
        
        return f"""
You are an autonomous data pipeline researcher.

PROGRAM:
{program.get('constraints', '')}

GOAL: {program.get('optimization_goal', '')}

RECENT RESULTS:
{json.dumps([{"metric": r.metric, "status": r.status} for r in recent], indent=2)}

BEST METRIC: {best:.4f}

Propose ONE improvement to optimize the pipeline.

RESPONSE FORMAT (JSON):
{{
    "idea": "Brief description",
    "code": "Python code for get_metric() function",
    "rationale": "Why this should help"
}}
"""

# ============================================================================
# FASTAPI APP
# ============================================================================

# Global instances
azure_client: Optional[AzureServicesClient] = None
engine: Optional[ExperimentEngine] = None
agent: Optional[AutonomousAgent] = None

# In-memory storage (replace with database in production)
programs_db: Dict[str, Dict] = {}
experiments_db: Dict[str, ExperimentResult] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup and shutdown"""
    global azure_client, engine, agent
    
    # Startup
    azure_client = AzureServicesClient()
    engine = ExperimentEngine(azure_client)
    agent = AutonomousAgent(engine)
    logger.info("Application started")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")

app = FastAPI(
    title="Azure Autonomous Data Platform",
    description="Autonomous data pipeline optimization with Claude",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ROUTES: PROGRAMS
# ============================================================================

@app.get("/api/programs")
async def list_programs() -> List[Dict[str, Any]]:
    """List all programs"""
    return list(programs_db.values())

@app.post("/api/programs")
async def create_program(program: ProgramUpdate) -> Dict[str, Any]:
    """Create new program"""
    program_id = f"prog_{len(programs_db) + 1}"
    
    program_data = {
        "id": program_id,
        "name": program.name,
        "constraints": program.constraints,
        "optimization_goal": program.optimization_goal,
        "metric_name": program.metric_name,
        "baseline_value": program.baseline_value,
        "target_value": program.target_value,
        "max_iterations": program.max_iterations,
        "created_at": datetime.utcnow().isoformat(),
        "status": "active"
    }
    
    programs_db[program_id] = program_data
    logger.info(f"Created program: {program_id}")
    
    return program_data

@app.get("/api/programs/{program_id}")
async def get_program(program_id: str) -> Dict[str, Any]:
    """Get program details"""
    if program_id not in programs_db:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return programs_db[program_id]

@app.get("/api/programs/{program_id}/metrics")
async def get_program_metrics(program_id: str) -> ProgramMetrics:
    """Get program metrics"""
    program_exps = [
        e for e in experiments_db.values() 
        if e.program_id == program_id
    ]
    
    if not program_exps:
        return ProgramMetrics(
            total_experiments=0,
            successful=0,
            crashes=0,
            best_metric=0.0,
            baseline_metric=programs_db.get(program_id, {}).get("baseline_value", 0.0),
            improvement_pct=0.0,
            success_rate=0.0,
            avg_cost=0.0
        )
    
    successful = [e for e in program_exps if e.status == "success"]
    crashes = [e for e in program_exps if e.status == "crash"]
    best = min([e.metric for e in successful], default=0.0) if successful else 0.0
    baseline = programs_db.get(program_id, {}).get("baseline_value", 0.0)
    
    return ProgramMetrics(
        total_experiments=len(program_exps),
        successful=len(successful),
        crashes=len(crashes),
        best_metric=best,
        baseline_metric=baseline,
        improvement_pct=((baseline - best) / baseline * 100) if baseline > 0 else 0.0,
        success_rate=(len(successful) / len(program_exps) * 100) if program_exps else 0.0,
        avg_cost=sum(e.cost_usd for e in successful) / len(successful) if successful else 0.0
    )

# ============================================================================
# ROUTES: EXPERIMENTS
# ============================================================================

@app.post("/api/experiments")
async def create_experiment(
    experiment: ExperimentCreate,
    background_tasks: BackgroundTasks
) -> ExperimentResult:
    """Create and run experiment"""
    
    if experiment.program_id not in programs_db:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Run experiment asynchronously
    result = await engine.run_experiment(
        experiment.analysis_code,
        experiment.program_id
    )
    
    experiments_db[result.id] = result
    logger.info(f"Experiment completed: {result.id} - {result.status}")
    
    return result

@app.get("/api/experiments")
async def list_experiments(program_id: Optional[str] = None) -> List[ExperimentResult]:
    """List experiments"""
    exps = list(experiments_db.values())
    
    if program_id:
        exps = [e for e in exps if e.program_id == program_id]
    
    return sorted(exps, key=lambda x: x.created_at, reverse=True)

@app.get("/api/experiments/{experiment_id}")
async def get_experiment(experiment_id: str) -> ExperimentResult:
    """Get experiment details"""
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return experiments_db[experiment_id]

# ============================================================================
# ROUTES: AGENT
# ============================================================================

@app.post("/api/agent/propose")
async def propose_experiment(program_id: str) -> Optional[Dict]:
    """Get agent proposal for next experiment"""
    
    if program_id not in programs_db:
        raise HTTPException(status_code=404, detail="Program not found")
    
    program = programs_db[program_id]
    recent_results = [
        e for e in experiments_db.values()
        if e.program_id == program_id
    ][-10:]
    
    proposal = await agent.get_proposal(program, recent_results)
    
    if not proposal:
        raise HTTPException(status_code=500, detail="Failed to get proposal")
    
    return proposal

@app.post("/api/agent/start-loop")
async def start_agent_loop(program_id: str) -> Dict[str, str]:
    """Start autonomous agent loop"""
    
    if program_id not in programs_db:
        raise HTTPException(status_code=404, detail="Program not found")
    
    if agent.is_running:
        raise HTTPException(status_code=409, detail="Agent already running")
    
    agent.is_running = True
    logger.info(f"Started agent loop for {program_id}")
    
    return {"status": "started", "program_id": program_id}

@app.post("/api/agent/stop-loop")
async def stop_agent_loop() -> Dict[str, str]:
    """Stop autonomous agent loop"""
    agent.is_running = False
    logger.info("Stopped agent loop")
    
    return {"status": "stopped"}

# ============================================================================
# ROUTES: DASHBOARD
# ============================================================================

@app.get("/api/dashboard")
async def get_dashboard() -> DashboardData:
    """Get dashboard data"""
    
    all_programs = list(programs_db.values())
    recent_exps = sorted(
        list(experiments_db.values()),
        key=lambda x: x.created_at,
        reverse=True
    )[:10]
    
    total_cost = sum(e.cost_usd for e in experiments_db.values())
    total_exps = len(experiments_db)
    successful = len([e for e in experiments_db.values() if e.status == "success"])
    
    return DashboardData(
        programs=all_programs,
        recent_experiments=recent_exps,
        system_health={
            "agent_running": agent.is_running,
            "total_experiments": total_exps,
            "success_rate": (successful / total_exps * 100) if total_exps > 0 else 0.0,
            "status": "healthy"
        },
        cost_summary={
            "total_cost_usd": round(total_cost, 2),
            "avg_per_experiment": round(total_cost / total_exps, 2) if total_exps > 0 else 0.0,
            "budget_remaining": 1000.0  # Example
        }
    )

# ============================================================================
# ROUTES: HEALTH
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/azure-status")
async def azure_status() -> Dict[str, Any]:
    """Check Azure services status"""
    return {
        "synapse": "connected" if not azure_client.mock_mode else "mock",
        "adls": "connected" if not azure_client.mock_mode else "mock",
        "insights": "connected" if not azure_client.mock_mode else "mock",
        "mock_mode": azure_client.mock_mode
    }

# ============================================================================
# ROOT
# ============================================================================

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Azure Autonomous Data Platform API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
