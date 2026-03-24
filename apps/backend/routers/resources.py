"""Azure Resources Management API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db

router = APIRouter(prefix="/api/resources", tags=["resources"])

class ResourceResponse(BaseModel):
    id: str
    name: str
    type: str
    sku: str
    cost_per_month: float
    status: str

class QuotaResponse(BaseModel):
    name: str
    used: float
    limit: float
    unit: str
    percent_used: float
    status: str

class AutoScalingResponse(BaseModel):
    resource_id: str
    min_instances: int
    max_instances: int
    cpu_threshold: int
    memory_threshold: int
    enabled: bool

# ==================== ENDPOINTS ====================

@router.get("/list", response_model=List[ResourceResponse])
async def list_resources(db: Session = Depends(get_db)):
    """List all Azure resources"""
    resources = [
        {
            "id": "vm-001",
            "name": "Standard_B2s VM 1",
            "type": "Virtual Machine",
            "sku": "Standard_B2s",
            "cost_per_month": 40.0,
            "status": "Running"
        },
        {
            "id": "vm-002",
            "name": "Standard_B2s VM 2",
            "type": "Virtual Machine",
            "sku": "Standard_B2s",
            "cost_per_month": 40.0,
            "status": "Running"
        },
        {
            "id": "storage-001",
            "name": "Storage Account",
            "type": "Storage",
            "sku": "Standard LRS",
            "cost_per_month": 20.0,
            "status": "Active"
        },
        {
            "id": "postgres-001",
            "name": "PostgreSQL Database",
            "type": "Database",
            "sku": "General Purpose",
            "cost_per_month": 80.0,
            "status": "Available"
        },
        {
            "id": "api-001",
            "name": "API Management",
            "type": "API Service",
            "sku": "Standard",
            "cost_per_month": 50.0,
            "status": "Active"
        }
    ]
    return [ResourceResponse(**r) for r in resources]

@router.get("/summary")
async def get_resources_summary(db: Session = Depends(get_db)):
    """Get resources summary"""
    resources = [
        {"type": "Virtual Machine", "count": 2, "cost": 80.0},
        {"type": "Storage", "count": 1, "cost": 20.0},
        {"type": "Database", "count": 1, "cost": 80.0},
        {"type": "API Service", "count": 1, "cost": 50.0}
    ]
    
    total_cost = sum(r["cost"] for r in resources)
    total_resources = sum(r["count"] for r in resources)
    
    return {
        "total_resources": total_resources,
        "total_monthly_cost": total_cost,
        "by_type": resources,
        "estimated_annual_cost": total_cost * 12
    }

@router.get("/quotas", response_model=List[QuotaResponse])
async def get_quotas(db: Session = Depends(get_db)):
    """Get Azure service quotas"""
    quotas = [
        {
            "name": "CPU Cores",
            "used": 8,
            "limit": 20,
            "unit": "cores",
            "percent_used": 40.0
        },
        {
            "name": "RAM (GB)",
            "used": 32,
            "limit": 64,
            "unit": "GB",
            "percent_used": 50.0
        },
        {
            "name": "Storage (GB)",
            "used": 500,
            "limit": 1000,
            "unit": "GB",
            "percent_used": 50.0
        },
        {
            "name": "API Calls/min",
            "used": 800,
            "limit": 10000,
            "unit": "calls/min",
            "percent_used": 8.0
        },
        {
            "name": "Database Connections",
            "used": 15,
            "limit": 100,
            "unit": "connections",
            "percent_used": 15.0
        }
    ]
    
    # Set status based on usage
    for quota in quotas:
        if quota["percent_used"] > 85:
            quota["status"] = "critical"
        elif quota["percent_used"] > 70:
            quota["status"] = "warning"
        else:
            quota["status"] = "healthy"
    
    return [QuotaResponse(**q) for q in quotas]

@router.get("/recommendations")
async def get_resource_recommendations(db: Session = Depends(get_db)):
    """Get resource optimization recommendations"""
    recommendations = [
        {
            "priority": "high",
            "type": "rightsizing",
            "resource": "VM-001",
            "title": "Downsize VM-001",
            "description": "VM-001 is underutilized. Consider downsizing to Standard_B1s",
            "potential_savings": "50%",
            "estimated_monthly_savings": 20.0
        },
        {
            "priority": "medium",
            "type": "autoscaling",
            "resource": "API Service",
            "title": "Enable Auto-Scaling",
            "description": "Enable auto-scaling for API service to handle traffic spikes",
            "potential_savings": "20%",
            "estimated_monthly_savings": 10.0
        },
        {
            "priority": "medium",
            "type": "cleanup",
            "resource": "Storage",
            "title": "Clean Up Old Data",
            "description": "Delete unused backups and old log files from storage",
            "potential_savings": "30%",
            "estimated_monthly_savings": 6.0
        }
    ]
    
    return {
        "total_recommendations": len(recommendations),
        "total_potential_savings": sum(r["estimated_monthly_savings"] for r in recommendations),
        "recommendations": recommendations
    }

@router.get("/autoscaling/{resource_id}", response_model=AutoScalingResponse)
async def get_autoscaling_config(resource_id: str, db: Session = Depends(get_db)):
    """Get auto-scaling configuration for a resource"""
    return {
        "resource_id": resource_id,
        "min_instances": 1,
        "max_instances": 5,
        "cpu_threshold": 75,
        "memory_threshold": 80,
        "enabled": True
    }

@router.post("/autoscaling/{resource_id}")
async def update_autoscaling_config(
    resource_id: str,
    min_instances: int = 1,
    max_instances: int = 5,
    cpu_threshold: int = 75,
    memory_threshold: int = 80,
    enabled: bool = True,
    db: Session = Depends(get_db)
):
    """Update auto-scaling configuration"""
    return {
        "status": "updated",
        "resource_id": resource_id,
        "min_instances": min_instances,
        "max_instances": max_instances,
        "cpu_threshold": cpu_threshold,
        "memory_threshold": memory_threshold,
        "enabled": enabled
    }

@router.get("/cost-by-type")
async def get_cost_by_type(db: Session = Depends(get_db)):
    """Get cost breakdown by resource type"""
    return {
        "by_type": {
            "Virtual Machines": {"count": 2, "cost": 80.0, "percent": 34.2},
            "Database": {"count": 1, "cost": 80.0, "percent": 34.2},
            "API Service": {"count": 1, "cost": 50.0, "percent": 21.4},
            "Storage": {"count": 1, "cost": 20.0, "percent": 8.5}
        },
        "total": 230.0,
        "monthly_trend": "stable"
    }

@router.post("/request-quota-increase")
async def request_quota_increase(
    quota_name: str,
    requested_limit: float,
    db: Session = Depends(get_db)
):
    """Request a quota increase"""
    return {
        "status": "requested",
        "quota": quota_name,
        "requested_limit": requested_limit,
        "created_at": datetime.utcnow().isoformat()
    }

