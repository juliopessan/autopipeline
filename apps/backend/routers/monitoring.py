"""Monitoring & Alerts API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from models import Experiment
from integrations.app_insights_client import AppInsightsClient
from integrations.alert_rules import AlertRulesEngine

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])

# Initialize services
app_insights = AppInsightsClient()
alert_engine = AlertRulesEngine()

class AlertResponse(BaseModel):
    type: str
    severity: str
    message: str
    value: float
    timestamp: str

class MonitoringSummaryResponse(BaseModel):
    total_events: int
    experiments_started: int
    experiments_completed: int
    anomalies_detected: int
    alerts_triggered: int
    critical_alerts: int

# ==================== ENDPOINTS ====================

@router.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "app_insights": "connected",
            "alert_engine": "ready"
        }
    }

@router.get("/summary", response_model=MonitoringSummaryResponse)
async def get_monitoring_summary(db: Session = Depends(get_db)):
    """Get monitoring summary"""
    summary = app_insights.get_summary()
    
    return MonitoringSummaryResponse(
        total_events=summary['total_events'],
        experiments_started=summary['experiment_started'],
        experiments_completed=summary['experiment_completed'],
        anomalies_detected=summary['anomalies_detected'],
        alerts_triggered=len(alert_engine.get_all_alerts()),
        critical_alerts=len(alert_engine.get_critical_alerts())
    )

@router.post("/experiment-started")
async def log_experiment_started(
    experiment_id: int,
    program_id: int,
    db: Session = Depends(get_db)
):
    """Log experiment start"""
    app_insights.log_experiment_started(experiment_id, program_id)
    
    return {
        "status": "logged",
        "event": "experiment_started",
        "experiment_id": experiment_id
    }

@router.post("/experiment-completed")
async def log_experiment_completed(
    experiment_id: int,
    result: float,
    cost: float,
    duration: int,
    db: Session = Depends(get_db)
):
    """Log experiment completion with alerts"""
    # Log to App Insights
    app_insights.log_experiment_completed(experiment_id, result, cost, duration)
    
    # Evaluate rules and generate alerts
    avg_cost = 50.0  # Mock value
    alerts = alert_engine.evaluate_cost_rules(cost, avg_cost)
    perf_alerts = alert_engine.evaluate_performance_rules(duration)
    
    all_alerts = alerts + perf_alerts
    
    return {
        "status": "logged",
        "event": "experiment_completed",
        "experiment_id": experiment_id,
        "cost": cost,
        "duration": duration,
        "alerts_triggered": len(all_alerts),
        "alerts": all_alerts
    }

@router.post("/anomaly-detected")
async def log_anomaly(
    experiment_id: int,
    anomaly_score: float,
    db: Session = Depends(get_db)
):
    """Log detected anomaly"""
    app_insights.log_anomaly_detected(experiment_id, anomaly_score)
    
    return {
        "status": "logged",
        "event": "anomaly_detected",
        "experiment_id": experiment_id,
        "anomaly_score": anomaly_score
    }

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all alerts with optional filtering"""
    alerts = alert_engine.get_all_alerts(limit)
    
    if severity:
        alerts = [a for a in alerts if a["severity"] == severity]
    
    return [AlertResponse(**a) for a in alerts]

@router.get("/alerts/critical", response_model=List[AlertResponse])
async def get_critical_alerts(db: Session = Depends(get_db)):
    """Get critical alerts only"""
    alerts = alert_engine.get_critical_alerts()
    return [AlertResponse(**a) for a in alerts]

@router.post("/evaluate-budget")
async def evaluate_budget(
    spent: float,
    budget: float,
    db: Session = Depends(get_db)
):
    """Evaluate budget and generate alerts"""
    alerts = alert_engine.evaluate_budget_rules(spent, budget)
    
    return {
        "spent": spent,
        "budget": budget,
        "percent_used": (spent / budget * 100) if budget > 0 else 0,
        "alerts": alerts
    }

@router.get("/events")
async def get_events(limit: int = 100, db: Session = Depends(get_db)):
    """Get recent monitoring events"""
    events = app_insights.get_events(limit)
    
    return {
        "total_events": len(events),
        "events": events
    }

@router.get("/timeline")
async def get_timeline(days: int = 7, db: Session = Depends(get_db)):
    """Get timeline of events over period"""
    events = app_insights.get_events(1000)
    
    # Group by day
    timeline = {}
    for event in events:
        try:
            ts = datetime.fromisoformat(event['timestamp'])
            day = ts.strftime('%Y-%m-%d')
            
            if day not in timeline:
                timeline[day] = {'count': 0, 'events': []}
            
            timeline[day]['count'] += 1
            timeline[day]['events'].append(event['name'])
        except:
            pass
    
    return timeline

