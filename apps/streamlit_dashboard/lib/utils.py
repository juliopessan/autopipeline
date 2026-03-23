"""Utility functions"""
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_mock_metrics(days: int = 7) -> pd.DataFrame:
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    data = {
        'date': sorted(dates),
        'success_rate': [random.uniform(0.7, 0.95) for _ in range(days)],
        'cost': [random.uniform(0.1, 1.5) for _ in range(days)],
        'experiments': [random.randint(5, 20) for _ in range(days)]
    }
    return pd.DataFrame(data)

def get_status_color(success_rate: float) -> str:
    if success_rate > 0.9:
        return "🟢"
    elif success_rate > 0.7:
        return "🟡"
    else:
        return "🔴"
