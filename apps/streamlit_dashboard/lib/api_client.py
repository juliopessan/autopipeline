"""API client para comunicação com FastAPI backend"""
import requests
import pandas as pd
from typing import Dict, List
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class APIClient:
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
    
    def get_dashboard(self) -> Dict:
        try:
            response = requests.get(f"{self.base_url}/api/dashboard", timeout=2)
            return response.json()
        except:
            return {"total_experiments": 0, "success_rate": 0, "total_cost": 0, "budget_remaining": 5000, "programs": []}
    
    def get_programs(self) -> List[Dict]:
        try:
            response = requests.get(f"{self.base_url}/api/programs", timeout=2)
            return response.json()
        except:
            return []
    
    def create_program(self, name: str, goal: str, metric: str, baseline: float, target: float, max_it: int) -> Dict:
        try:
            payload = {"name": name, "optimization_goal": goal, "metric_name": metric, 
                      "baseline_value": baseline, "target_value": target, "max_iterations": max_it}
            response = requests.post(f"{self.base_url}/api/programs", json=payload, timeout=2)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

def get_api_client() -> APIClient:
    return APIClient()
