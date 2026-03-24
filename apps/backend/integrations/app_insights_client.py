"""Azure Application Insights Integration"""
from typing import Dict, Any
from datetime import datetime
import json

class AppInsightsClient:
    """Monitor experiments with Application Insights"""
    
    def __init__(self, instrumentation_key: str = "local-dev"):
        self.instrumentation_key = instrumentation_key
        self.events = []
    
    def log_experiment_started(self, experiment_id: int, program_id: int):
        """Log experiment start"""
        event = {
            "name": "experiment_started",
            "timestamp": datetime.utcnow().isoformat(),
            "properties": {
                "experiment_id": experiment_id,
                "program_id": program_id,
                "status": "started"
            }
        }
        self.events.append(event)
    
    def log_experiment_completed(self, experiment_id: int, 
                                result: float, cost: float, duration: int):
        """Log experiment completion"""
        event = {
            "name": "experiment_completed",
            "timestamp": datetime.utcnow().isoformat(),
            "properties": {
                "experiment_id": experiment_id,
                "status": "completed",
                "result": result,
                "cost": cost,
                "duration": duration
            }
        }
        self.events.append(event)
    
    def log_anomaly_detected(self, experiment_id: int, anomaly_score: float):
        """Log detected anomaly"""
        event = {
            "name": "anomaly_detected",
            "timestamp": datetime.utcnow().isoformat(),
            "properties": {
                "experiment_id": experiment_id,
                "anomaly_score": anomaly_score
            }
        }
        self.events.append(event)
    
    def log_custom_event(self, event_name: str, properties: Dict[str, Any]):
        """Log custom event"""
        event = {
            "name": event_name,
            "timestamp": datetime.utcnow().isoformat(),
            "properties": properties
        }
        self.events.append(event)
    
    def get_events(self, limit: int = 100) -> list:
        """Get logged events"""
        return self.events[-limit:]
    
    def get_summary(self) -> Dict:
        """Get events summary"""
        return {
            "total_events": len(self.events),
            "experiment_started": len([e for e in self.events if e['name'] == 'experiment_started']),
            "experiment_completed": len([e for e in self.events if e['name'] == 'experiment_completed']),
            "anomalies_detected": len([e for e in self.events if e['name'] == 'anomaly_detected'])
        }
