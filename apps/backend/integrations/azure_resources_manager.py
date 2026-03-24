"""Azure Resources Manager Integration"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AzureResource:
    """Represents an Azure resource"""
    id: str
    name: str
    type: str
    sku: str
    cost_per_month: float
    status: str
    region: str = "East US"

class AzureResourcesManager:
    """Manage Azure resources and quotas"""
    
    def __init__(self, subscription_id: str = "default"):
        self.subscription_id = subscription_id
        self.resources = []
        self.quotas = {}
        self._initialize_resources()
    
    def _initialize_resources(self):
        """Initialize default resources"""
        self.resources = [
            AzureResource(
                id="vm-001",
                name="Standard_B2s VM 1",
                type="Virtual Machine",
                sku="Standard_B2s",
                cost_per_month=40.0,
                status="Running"
            ),
            AzureResource(
                id="vm-002",
                name="Standard_B2s VM 2",
                type="Virtual Machine",
                sku="Standard_B2s",
                cost_per_month=40.0,
                status="Running"
            ),
            AzureResource(
                id="storage-001",
                name="Storage Account",
                type="Storage",
                sku="Standard LRS",
                cost_per_month=20.0,
                status="Active"
            ),
            AzureResource(
                id="postgres-001",
                name="PostgreSQL Database",
                type="Database",
                sku="General Purpose",
                cost_per_month=80.0,
                status="Available"
            )
        ]
        
        self.quotas = {
            "cpu_cores": {"used": 8, "limit": 20},
            "memory_gb": {"used": 32, "limit": 64},
            "storage_gb": {"used": 500, "limit": 1000},
            "api_calls_per_min": {"used": 800, "limit": 10000}
        }
    
    def list_resources(self) -> List[Dict]:
        """List all resources"""
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "sku": r.sku,
                "cost_per_month": r.cost_per_month,
                "status": r.status,
                "region": r.region
            }
            for r in self.resources
        ]
    
    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """Get a specific resource"""
        for r in self.resources:
            if r.id == resource_id:
                return {
                    "id": r.id,
                    "name": r.name,
                    "type": r.type,
                    "sku": r.sku,
                    "cost_per_month": r.cost_per_month,
                    "status": r.status,
                    "region": r.region
                }
        return None
    
    def get_total_cost(self) -> float:
        """Get total monthly cost"""
        return sum(r.cost_per_month for r in self.resources)
    
    def get_quota_status(self, quota_name: str) -> Dict:
        """Get quota status"""
        if quota_name not in self.quotas:
            return None
        
        quota = self.quotas[quota_name]
        percent = (quota["used"] / quota["limit"]) * 100 if quota["limit"] > 0 else 0
        
        return {
            "name": quota_name,
            "used": quota["used"],
            "limit": quota["limit"],
            "percent_used": percent,
            "status": "critical" if percent > 85 else "warning" if percent > 70 else "healthy"
        }
    
    def get_all_quotas(self) -> List[Dict]:
        """Get all quotas"""
        quotas = []
        for quota_name in self.quotas.keys():
            quotas.append(self.get_quota_status(quota_name))
        return quotas
    
    def recommend_rightsizing(self) -> List[Dict]:
        """Get rightsizing recommendations"""
        recommendations = []
        
        for resource in self.resources:
            # Mock recommendations based on cost
            if resource.cost_per_month > 50:
                recommendations.append({
                    "resource_id": resource.id,
                    "resource_name": resource.name,
                    "type": "rightsizing",
                    "title": f"Downsize {resource.name}",
                    "description": f"Consider downsizing to save costs",
                    "potential_savings": "30-50%",
                    "estimated_monthly_savings": resource.cost_per_month * 0.4
                })
        
        return recommendations
    
    def get_autoscaling_config(self, resource_id: str) -> Dict:
        """Get auto-scaling config"""
        return {
            "resource_id": resource_id,
            "min_instances": 1,
            "max_instances": 5,
            "cpu_threshold": 75,
            "memory_threshold": 80,
            "enabled": True
        }
    
    def update_autoscaling_config(self, resource_id: str,
                                 min_instances: int,
                                 max_instances: int,
                                 cpu_threshold: int,
                                 memory_threshold: int) -> Dict:
        """Update auto-scaling config"""
        return {
            "resource_id": resource_id,
            "min_instances": min_instances,
            "max_instances": max_instances,
            "cpu_threshold": cpu_threshold,
            "memory_threshold": memory_threshold,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def get_cost_by_type(self) -> Dict:
        """Get cost breakdown by resource type"""
        cost_by_type = {}
        
        for resource in self.resources:
            if resource.type not in cost_by_type:
                cost_by_type[resource.type] = {
                    "count": 0,
                    "cost": 0.0
                }
            
            cost_by_type[resource.type]["count"] += 1
            cost_by_type[resource.type]["cost"] += resource.cost_per_month
        
        # Calculate percentages
        total_cost = self.get_total_cost()
        for res_type in cost_by_type:
            percent = (cost_by_type[res_type]["cost"] / total_cost * 100) if total_cost > 0 else 0
            cost_by_type[res_type]["percent"] = percent
        
        return {
            "by_type": cost_by_type,
            "total": total_cost,
            "monthly_trend": "stable"
        }

