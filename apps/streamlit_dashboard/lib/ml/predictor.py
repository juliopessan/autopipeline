"""Predictive Analytics - Predict experiment outcomes"""
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')

class ExperimentPredictor:
    """Predict experiment outcomes using Random Forest"""
    
    def __init__(self, n_estimators: int = 100, model_type: str = "rf"):
        """
        Args:
            n_estimators: Number of trees
            model_type: "rf" for RandomForest, "gb" for GradientBoosting
        """
        self.scaler = StandardScaler()
        self.model = None
        self.model_type = model_type
        self.n_estimators = n_estimators
        self.is_trained = False
        self.feature_importance = None
    
    def train(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Train predictor on historical data
        
        Returns:
            R² score (0-1, higher is better)
        """
        if len(X) < 5:
            raise ValueError("Need at least 5 samples to train")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Choose model
        if self.model_type == "rf":
            self.model = RandomForestRegressor(
                n_estimators=self.n_estimators,
                random_state=42,
                n_jobs=-1
            )
        else:  # gradient boosting
            self.model = GradientBoostingRegressor(
                n_estimators=self.n_estimators,
                random_state=42
            )
        
        # Train
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Store feature importance
        self.feature_importance = self.model.feature_importances_
        
        # Return score
        score = self.model.score(X_scaled, y)
        return score
    
    def predict(self, params: List[float]) -> float:
        """Predict single outcome"""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        params_scaled = self.scaler.transform([params])
        return self.model.predict(params_scaled)[0]
    
    def predict_with_confidence(self, params: List[float]) -> Dict:
        """
        Predict with confidence interval using ensemble
        """
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        params_scaled = self.scaler.transform([params])
        
        # Get predictions from all trees
        predictions = []
        for estimator in self.model.estimators_:
            if hasattr(estimator, 'predict'):  # RF case
                pred = estimator.predict(params_scaled)[0]
            else:  # GB case
                pred = estimator[0].predict(params_scaled)[0]
            predictions.append(pred)
        
        predictions = np.array(predictions)
        
        return {
            "predicted_value": float(np.mean(predictions)),
            "confidence_interval_lower": float(np.percentile(predictions, 5)),
            "confidence_interval_upper": float(np.percentile(predictions, 95)),
            "std_dev": float(np.std(predictions)),
            "min": float(np.min(predictions)),
            "max": float(np.max(predictions))
        }
    
    def predict_batch(self, params_list: List[List[float]]) -> np.ndarray:
        """Predict multiple outcomes"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        params_scaled = self.scaler.transform(params_list)
        return self.model.predict(params_scaled)
    
    def get_feature_importance(self, feature_names: List[str] = None) -> Dict:
        """Get feature importance scores"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(len(self.feature_importance))]
        
        importance_dict = {}
        for name, importance in zip(feature_names, self.feature_importance):
            importance_dict[name] = float(importance)
        
        # Sort by importance
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_importance)
