"""Anomaly Detection - Identify unusual experiments"""
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import Dict, List

class AnomalyDetector:
    """Detect anomalies in experiment metrics using Isolation Forest"""
    
    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Args:
            contamination: Expected proportion of anomalies (0-0.5)
            random_state: Random seed
        """
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_trained = False
        self.threshold = None
    
    def fit(self, X: np.ndarray):
        """Fit anomaly detector on normal data"""
        if len(X) < 5:
            raise ValueError("Need at least 5 samples")
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        
        # Calculate threshold as 10th percentile
        scores = self.model.score_samples(X_scaled)
        self.threshold = np.percentile(scores, 10)
        
        self.is_trained = True
    
    def predict(self, X: np.ndarray) -> Dict:
        """
        Detect anomalies in new data
        
        Returns:
            Dict with anomaly flags and scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call fit() first.")
        
        X_scaled = self.scaler.transform(X)
        
        # Get predictions (-1 = anomaly, 1 = normal)
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        is_anomaly = predictions == -1
        
        return {
            "is_anomaly": is_anomaly.tolist(),
            "anomaly_score": scores.tolist(),
            "threshold": float(self.threshold),
            "n_anomalies": int(np.sum(is_anomaly)),
            "anomaly_percentage": float(100 * np.sum(is_anomaly) / len(is_anomaly))
        }
    
    def predict_single(self, x: List[float]) -> Dict:
        """Detect anomaly in single sample"""
        result = self.predict(np.array([x]))
        return {
            "is_anomaly": result["is_anomaly"][0],
            "anomaly_score": result["anomaly_score"][0],
            "threshold": result["threshold"]
        }
    
    def explain_anomaly(self, x: List[float], feature_names: List[str] = None) -> Dict:
        """
        Explain why a sample is anomalous
        """
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(len(x))]
        
        result = self.predict_single(x)
        
        # Calculate feature contributions (simple approach)
        contributions = {}
        for i, (name, value) in enumerate(zip(feature_names, x)):
            # Normalize and check deviation from mean
            scaled_val = (value - self.scaler.mean_[i]) / (self.scaler.scale_[i] + 1e-8)
            contributions[name] = float(np.abs(scaled_val))
        
        # Sort by contribution
        sorted_contrib = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "is_anomaly": result["is_anomaly"],
            "anomaly_score": result["anomaly_score"],
            "contributing_features": dict(sorted_contrib)
        }
