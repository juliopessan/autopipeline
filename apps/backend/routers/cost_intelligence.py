"""Cost Intelligence API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
import sys
from pathlib import Path

# Import database utilities
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from models import Experiment

# Import cost advisor
from integrations.azure_cost_optimizer import CostAdvisor

router = APIRouter(prefix="/api/cost", tags=["cost-intelligence"])

# Initialize cost advisor
cost_advisor = CostAdvisor(azure_subscription_id="default")

class CostTrendsResponse(BaseModel):
    period_days: int
    total_cost: float
    average_cost: float
    experiments_count: int
    cost_per_experiment: float
    trending: str

class RecommendationResponse(BaseModel):
    priority: str
    type: str
    title: str
    description: str
    potential_savings: str

class ROIResponse(BaseModel):
    baseline_cost: float
    experiment_cost: float
    savings: float
    roi_percentage: float
    breakeven_days: int = None

# ==================== ENDPOINTS ====================

@router.get("/trends", response_model=CostTrendsResponse)
async def get_cost_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get cost trends over period"""
    trends = cost_advisor.get_cost_trends(days)
    return CostTrendsResponse(**trends)

@router.get("/recommendations/{experiment_id}")
async def get_recommendations(experiment_id: int, db: Session = Depends(get_db)):
    """Get cost optimization recommendations for an experiment"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    # Simulate cost data from experiment
    experiment_data = {
        "cost_per_minute": 0.15,
        "duration": 3600
    }
    
    recommendations = cost_advisor.get_recommendations(experiment_data)
    return {
        "experiment_id": experiment_id,
        "recommendations": recommendations
    }

@router.post("/roi")
async def calculate_roi(experiment_id: int, baseline_cost: float, 
                       db: Session = Depends(get_db)):
    """Calculate ROI for an experiment"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    # Get experiment cost (mock for now)
    experiment_cost = 75.0
    
    roi = cost_advisor.calculate_roi(
        experiment_result=1.0,
        experiment_cost=experiment_cost,
        baseline_cost=baseline_cost
    )
    return roi

@router.get("/summary")
async def get_cost_summary(days: int = 30, db: Session = Depends(get_db)):
    """Get complete cost summary"""
    trends = cost_advisor.get_cost_trends(days)
    
    return {
        "period": f"Last {days} days",
        "total_cost": trends["total_cost"],
        "average_cost": trends["average_cost"],
        "experiments": trends["experiments_count"],
        "trend": trends["trending"],
        "estimated_monthly": trends["total_cost"] * (30 / days)
    }

@router.post("/log-cost")
async def log_experiment_cost(
    experiment_id: int,
    cost: float,
    duration: int,
    resources: Dict = None,
    db: Session = Depends(get_db)
):
    """Log cost for an experiment"""
    cost_advisor.log_experiment_cost(experiment_id, cost, duration, resources or {})
    
    return {
        "status": "logged",
        "experiment_id": experiment_id,
        "cost": cost,
        "duration": duration
    }

@router.get("/top-expensive")
async def get_top_expensive_experiments(limit: int = 10, db: Session = Depends(get_db)):
    """Get top most expensive experiments"""
    sorted_costs = sorted(
        cost_advisor.cost_history.items(),
        key=lambda x: x[1]["cost"],
        reverse=True
    )[:limit]
    
    return {
        "experiments": [
            {
                "experiment_id": exp_id,
                "cost": data["cost"],
                "duration": data["duration"],
                "cost_per_minute": data["cost_per_minute"]
            }
            for exp_id, data in sorted_costs
        ]
    }
