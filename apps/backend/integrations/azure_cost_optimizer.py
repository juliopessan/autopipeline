"""Azure Cost Optimization Integration"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class CostAdvisor:
    """Analyze experiment costs and provide recommendations"""
    
    def __init__(self, azure_subscription_id: str = "default"):
        self.subscription_id = azure_subscription_id
        self.cost_history = {}
    
    def log_experiment_cost(self, experiment_id: int, 
                           cost: float, duration: int, 
                           resources_used: Dict = None):
        """Log experiment cost"""
        if resources_used is None:
            resources_used = {}
            
        self.cost_history[experiment_id] = {
            "timestamp": datetime.utcnow().isoformat(),
            "cost": cost,
            "duration": duration,
            "cost_per_minute": cost / (duration / 60) if duration > 0 else 0,
            "resources": resources_used
        }
    
    def get_cost_trends(self, days: int = 30) -> Dict:
        """Get cost trending over time"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_costs = {}
        
        for k, v in self.cost_history.items():
            try:
                ts = datetime.fromisoformat(v["timestamp"])
                if ts > cutoff:
                    recent_costs[k] = v
            except:
                pass
        
        total_cost = sum(c["cost"] for c in recent_costs.values())
        avg_cost = total_cost / len(recent_costs) if recent_costs else 0
        
        return {
            "period_days": days,
            "total_cost": total_cost,
            "average_cost": avg_cost,
            "experiments_count": len(recent_costs),
            "cost_per_experiment": avg_cost,
            "trending": "up" if avg_cost > 0.5 else "stable"
        }
    
    def get_recommendations(self, experiment_data: Dict) -> List[Dict]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        cost_per_min = experiment_data.get("cost_per_minute", 0)
        duration = experiment_data.get("duration", 0)
        
        # Recommendation 1: Long-running experiments
        if duration > 3600:  # > 1 hour
            recommendations.append({
                "priority": "high",
                "type": "duration",
                "title": "Optimize Experiment Duration",
                "description": "This experiment ran for over 1 hour. Consider breaking it into smaller sub-experiments.",
                "potential_savings": "30-50%"
            })
        
        # Recommendation 2: Resource optimization
        if cost_per_min > 0.1:
            recommendations.append({
                "priority": "high",
                "type": "resources",
                "title": "Use Smaller Instance Size",
                "description": "Consider using smaller compute instances for this workload.",
                "potential_savings": "20-40%"
            })
        
        # Recommendation 3: Batch processing
        recommendations.append({
            "priority": "medium",
            "type": "batching",
            "title": "Batch Similar Experiments",
            "description": "Grouping similar experiments can reduce setup overhead.",
            "potential_savings": "15-25%"
        })
        
        return recommendations
    
    def calculate_roi(self, experiment_result: float, 
                     experiment_cost: float, 
                     baseline_cost: float) -> Dict:
        """Calculate ROI of experiment vs baseline"""
        cost_difference = baseline_cost - experiment_cost
        roi_percentage = (cost_difference / baseline_cost) * 100 if baseline_cost else 0
        
        return {
            "baseline_cost": baseline_cost,
            "experiment_cost": experiment_cost,
            "savings": cost_difference,
            "roi_percentage": roi_percentage,
            "breakeven_days": 1 if roi_percentage > 0 else None
        }
