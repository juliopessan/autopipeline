"""Smart Alert Rules Engine"""
from enum import Enum
from typing import Dict, List
from datetime import datetime

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertRulesEngine:
    """Generate alerts based on rules"""
    
    def __init__(self):
        self.rules = {
            "cost_spike": {"threshold": 1.5, "severity": AlertSeverity.HIGH},
            "long_duration": {"threshold": 7200, "severity": AlertSeverity.MEDIUM},
            "high_error_rate": {"threshold": 0.1, "severity": AlertSeverity.CRITICAL},
            "budget_exceeded": {"threshold": 1.0, "severity": AlertSeverity.CRITICAL},
        }
        self.alerts = []
    
    def evaluate_cost_rules(self, experiment_cost: float, 
                           avg_cost: float) -> List[Dict]:
        """Evaluate cost-related rules"""
        alerts = []
        
        # Rule 1: Cost spike (cost is 1.5x average)
        if avg_cost > 0 and experiment_cost > avg_cost * self.rules["cost_spike"]["threshold"]:
            alert = {
                "type": "cost_spike",
                "severity": "high",
                "message": f"Cost spike detected: ${experiment_cost:.2f} (avg: ${avg_cost:.2f})",
                "value": experiment_cost,
                "timestamp": datetime.utcnow().isoformat()
            }
            alerts.append(alert)
            self.alerts.append(alert)
        
        return alerts
    
    def evaluate_performance_rules(self, duration: int, 
                                   error_rate: float = 0.0) -> List[Dict]:
        """Evaluate performance rules"""
        alerts = []
        
        # Rule 1: Long duration (> 2 hours)
        if duration > self.rules["long_duration"]["threshold"]:
            alert = {
                "type": "long_duration",
                "severity": "medium",
                "message": f"Experiment took {duration}s ({duration/3600:.1f} hours)",
                "value": duration,
                "timestamp": datetime.utcnow().isoformat()
            }
            alerts.append(alert)
            self.alerts.append(alert)
        
        # Rule 2: High error rate (> 10%)
        if error_rate > self.rules["high_error_rate"]["threshold"]:
            alert = {
                "type": "high_error_rate",
                "severity": "critical",
                "message": f"Error rate: {error_rate*100:.1f}%",
                "value": error_rate,
                "timestamp": datetime.utcnow().isoformat()
            }
            alerts.append(alert)
            self.alerts.append(alert)
        
        return alerts
    
    def evaluate_budget_rules(self, spent: float, budget: float) -> List[Dict]:
        """Evaluate budget rules"""
        alerts = []
        
        if budget > 0:
            spent_percent = spent / budget
            
            # Alert at 80%
            if spent_percent > 0.8 and spent_percent < 1.0:
                alert = {
                    "type": "budget_warning",
                    "severity": "high",
                    "message": f"Budget usage: {spent_percent*100:.0f}% (${spent:.2f}/${budget:.2f})",
                    "value": spent_percent,
                    "timestamp": datetime.utcnow().isoformat()
                }
                alerts.append(alert)
                self.alerts.append(alert)
            
            # Alert at 100%+
            elif spent_percent >= 1.0:
                alert = {
                    "type": "budget_exceeded",
                    "severity": "critical",
                    "message": f"Budget exceeded: {spent_percent*100:.0f}% (${spent:.2f}/${budget:.2f})",
                    "value": spent_percent,
                    "timestamp": datetime.utcnow().isoformat()
                }
                alerts.append(alert)
                self.alerts.append(alert)
        
        return alerts
    
    def get_all_alerts(self, limit: int = 100) -> List[Dict]:
        """Get all logged alerts"""
        return self.alerts[-limit:]
    
    def get_critical_alerts(self) -> List[Dict]:
        """Get only critical alerts"""
        return [a for a in self.alerts if a["severity"] == "critical"]
