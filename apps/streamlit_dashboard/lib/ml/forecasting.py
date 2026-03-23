"""Time Series Forecasting - Predict future metrics"""
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesForecaster:
    """Forecast time series metrics"""
    
    def __init__(self):
        self.decomposition = None
        self.arima_model = None
        self.is_trained = False
    
    def decompose(self, series: List[float], period: int = 12) -> Dict:
        """
        Decompose time series into components
        
        Returns:
            trend, seasonal, residual components
        """
        if len(series) < period * 2:
            return {
                "error": f"Need at least {period * 2} data points for decomposition"
            }
        
        try:
            series_pd = pd.Series(series)
            decomposition = seasonal_decompose(
                series_pd,
                model='additive',
                period=period
            )
            
            return {
                "trend": decomposition.trend.tolist(),
                "seasonal": decomposition.seasonal.tolist(),
                "residual": decomposition.resid.tolist(),
                "original": decomposition.observed.tolist()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def forecast_arima(self, series: List[float], steps: int = 10, 
                      order: Tuple = (1, 1, 1)) -> Dict:
        """
        ARIMA forecast for time series
        
        Args:
            series: Historical data
            steps: Number of steps to forecast
            order: (p, d, q) for ARIMA
        """
        if len(series) < 10:
            return {"error": "Need at least 10 data points"}
        
        try:
            model = ARIMA(series, order=order)
            results = model.fit()
            
            # Forecast
            forecast = results.get_forecast(steps=steps)
            forecast_values = forecast.predicted_mean.tolist()
            
            # Confidence intervals
            conf_int = forecast.conf_int()
            ci_lower = conf_int.iloc[:, 0].tolist()
            ci_upper = conf_int.iloc[:, 1].tolist()
            
            return {
                "forecast": forecast_values,
                "confidence_interval_lower": ci_lower,
                "confidence_interval_upper": ci_upper,
                "aic": float(results.aic),
                "bic": float(results.bic)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def forecast_linear(self, series: List[float], steps: int = 10) -> Dict:
        """Simple linear regression forecast"""
        if len(series) < 3:
            return {"error": "Need at least 3 data points"}
        
        X = np.arange(len(series)).reshape(-1, 1)
        y = np.array(series)
        
        # Fit linear model
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast
        X_future = np.arange(len(series), len(series) + steps).reshape(-1, 1)
        forecast = model.predict(X_future).tolist()
        
        return {
            "forecast": forecast,
            "slope": float(model.coef_[0]),
            "intercept": float(model.intercept_),
            "r_squared": float(model.score(X, y))
        }
    
    def detect_trend(self, series: List[float]) -> Dict:
        """Detect uptrend, downtrend, or stable"""
        if len(series) < 2:
            return {"trend": "insufficient_data"}
        
        series = np.array(series)
        
        # Compare first half vs second half
        mid = len(series) // 2
        first_half_mean = np.mean(series[:mid])
        second_half_mean = np.mean(series[mid:])
        
        change_percent = 100 * (second_half_mean - first_half_mean) / (first_half_mean + 1e-8)
        
        if change_percent > 5:
            trend = "uptrend"
        elif change_percent < -5:
            trend = "downtrend"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "first_half_mean": float(first_half_mean),
            "second_half_mean": float(second_half_mean),
            "change_percent": float(change_percent)
        }
