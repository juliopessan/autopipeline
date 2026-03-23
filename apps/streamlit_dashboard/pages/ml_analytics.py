"""Advanced ML Analytics Dashboard"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from lib.ml.predictor import ExperimentPredictor
from lib.ml.anomaly import AnomalyDetector
from lib.ml.forecasting import TimeSeriesForecaster
from lib.ml.clustering import ExperimentClustering
from lib.api_client import get_api_client

def show():
    st.subheader("🧠 Advanced ML Analytics")
    
    api = get_api_client()
    experiments = api.get_experiments()
    
    if not experiments:
        st.warning("No experiments yet. Create experiments to enable ML analytics.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(experiments)
    
    # Ensure numeric columns
    for col in ['param1', 'param2', 'param3', 'result', 'cost']:
        if col not in df.columns:
            df[col] = np.random.rand(len(df))
    
    # Tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Predictions",
        "🚨 Anomalies",
        "📈 Forecasting",
        "🎯 Clustering"
    ])
    
    # ==================== TAB 1: PREDICTIONS ====================
    with tab1:
        st.write("### 🔮 Experiment Outcome Predictions")
        st.write("Predict the outcome of experiments based on historical data")
        
        # Train predictor
        try:
            X = df[['param1', 'param2', 'param3']].values
            y = df['result'].values
            
            predictor = ExperimentPredictor(n_estimators=50, model_type="rf")
            score = predictor.train(X, y)
            
            st.success(f"✅ Model trained with R² = {score:.3f}")
            
            # Predict new experiment
            st.write("#### Predict New Experiment")
            
            col1, col2, col3 = st.columns(3)
            p1 = col1.number_input("Parameter 1", value=0.5, min_value=0.0, max_value=1.0)
            p2 = col2.number_input("Parameter 2", value=0.5, min_value=0.0, max_value=1.0)
            p3 = col3.number_input("Parameter 3", value=0.5, min_value=0.0, max_value=1.0)
            
            if st.button("🔮 Predict", key="predict_btn"):
                prediction = predictor.predict_with_confidence([p1, p2, p3])
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Predicted Value", f"{prediction['predicted_value']:.4f}")
                col2.metric("Std Dev", f"{prediction['std_dev']:.4f}")
                col3.metric("Confidence", f"{prediction['confidence_interval_upper'] - prediction['confidence_interval_lower']:.4f}")
                
                # Confidence interval visualization
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=prediction['predicted_value'],
                    title={'text': "Predicted Outcome"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [prediction['min'], prediction['max']]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [prediction['min'], prediction['confidence_interval_lower']], 'color': "lightgray"},
                            {'range': [prediction['confidence_interval_lower'], prediction['confidence_interval_upper']], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': prediction['max']
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance
            st.write("#### Feature Importance")
            importance = predictor.get_feature_importance(['Param 1', 'Param 2', 'Param 3'])
            
            fig = px.bar(
                x=list(importance.values()),
                y=list(importance.keys()),
                orientation='h',
                title="Feature Importance for Predictions",
                labels={'x': 'Importance Score', 'y': 'Feature'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error in predictions: {e}")
    
    # ==================== TAB 2: ANOMALIES ====================
    with tab2:
        st.write("### 🚨 Anomaly Detection")
        st.write("Identify unusual or anomalous experiments")
        
        try:
            X = df[['param1', 'param2', 'param3']].values
            
            detector = AnomalyDetector(contamination=0.15)
            detector.fit(X)
            
            results = detector.predict(X)
            
            # Stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Experiments", len(X))
            col2.metric("Anomalies Detected", results['n_anomalies'])
            col3.metric("Anomaly %", f"{results['anomaly_percentage']:.1f}%")
            
            # Scatter plot with anomalies highlighted
            df_plot = df.copy()
            df_plot['anomaly'] = results['is_anomaly']
            
            fig = px.scatter_3d(
                df_plot,
                x='param1',
                y='param2',
                z='param3',
                color='anomaly',
                size='result',
                title="Experiments in 3D Space (Red = Anomalies)",
                color_discrete_map={True: 'red', False: 'blue'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Anomaly scores distribution
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=results['anomaly_score'],
                nbinsx=30,
                name='Anomaly Score',
                marker_color='rgba(100, 100, 255, 0.7)'
            ))
            fig.add_vline(
                x=results['threshold'],
                line_dash="dash",
                line_color="red",
                annotation_text="Threshold",
                annotation_position="top right"
            )
            fig.update_layout(
                title="Distribution of Anomaly Scores",
                xaxis_title="Anomaly Score",
                yaxis_title="Count",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error in anomaly detection: {e}")
    
    # ==================== TAB 3: FORECASTING ====================
    with tab3:
        st.write("### 📈 Time Series Forecasting")
        st.write("Forecast future metric values")
        
        try:
            # Create time series from results
            time_series = df.sort_index()['result'].values.tolist()
            
            if len(time_series) >= 10:
                forecaster = TimeSeriesForecasting()
                
                # Trend detection
                trend_info = forecaster.detect_trend(time_series)
                st.info(f"🔍 Trend: **{trend_info['trend'].upper()}** (Change: {trend_info['change_percent']:.1f}%)")
                
                # ARIMA Forecast
                st.write("#### ARIMA Forecast")
                forecast_steps = st.slider("Forecast Steps", 5, 20, 10)
                
                forecast_results = forecaster.forecast_arima(time_series, steps=forecast_steps)
                
                if 'error' not in forecast_results:
                    # Plot
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(go.Scatter(
                        x=list(range(len(time_series))),
                        y=time_series,
                        name='Historical',
                        mode='lines+markers'
                    ))
                    
                    # Forecast
                    forecast_x = list(range(len(time_series), len(time_series) + forecast_steps))
                    fig.add_trace(go.Scatter(
                        x=forecast_x,
                        y=forecast_results['forecast'],
                        name='Forecast',
                        mode='lines+markers',
                        line=dict(dash='dash')
                    ))
                    
                    # Confidence interval
                    fig.add_trace(go.Scatter(
                        x=forecast_x + forecast_x[::-1],
                        y=forecast_results['confidence_interval_upper'] + forecast_results['confidence_interval_lower'][::-1],
                        fill='toself',
                        fillcolor='rgba(0,100,200,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='95% CI'
                    ))
                    
                    fig.update_layout(
                        title="ARIMA Forecast",
                        xaxis_title="Time",
                        yaxis_title="Metric Value",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Decomposition
                st.write("#### Time Series Decomposition")
                decomp = forecaster.decompose(time_series, period=4)
                
                if 'error' not in decomp:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(y=decomp['original'], name='Original', mode='lines'))
                    fig.add_trace(go.Scatter(y=decomp['trend'], name='Trend', mode='lines'))
                    fig.add_trace(go.Scatter(y=decomp['seasonal'], name='Seasonal', mode='lines'))
                    fig.add_trace(go.Scatter(y=decomp['residual'], name='Residual', mode='lines'))
                    
                    fig.update_layout(
                        title="Time Series Decomposition",
                        xaxis_title="Time",
                        yaxis_title="Value",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need at least 10 experiments for time series analysis")
        
        except Exception as e:
            st.error(f"Error in forecasting: {e}")
    
    # ==================== TAB 4: CLUSTERING ====================
    with tab4:
        st.write("### 🎯 Experiment Clustering")
        st.write("Group similar experiments together")
        
        try:
            X = df[['param1', 'param2', 'param3']].values
            
            # Find optimal clusters
            st.write("#### Finding Optimal Number of Clusters...")
            clustering = ExperimentClustering(n_clusters=3)
            
            optimal = clustering.find_optimal_clusters(X, max_clusters=6)
            
            n_clusters = st.slider(
                "Number of Clusters",
                2,
                6,
                value=optimal['suggested_clusters']
            )
            
            # Re-fit with selected clusters
            clustering = ExperimentClustering(n_clusters=n_clusters)
            cluster_results = clustering.fit_predict(X)
            
            # Stats
            st.write("#### Cluster Statistics")
            cluster_cols = st.columns(n_clusters)
            for i in range(n_clusters):
                with cluster_cols[i]:
                    stats = cluster_results['cluster_stats'][f'cluster_{i}']
                    st.metric(
                        f"Cluster {i}",
                        f"{stats['size']} experiments",
                        f"{stats['percentage']:.1f}%"
                    )
            
            # 3D visualization
            df_cluster = df.copy()
            df_cluster['cluster'] = cluster_results['cluster_assignments']
            
            fig = px.scatter_3d(
                df_cluster,
                x='param1',
                y='param2',
                z='param3',
                color='cluster',
                size='result',
                title="Experiments Clustered",
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Silhouette scores
            fig = px.line(
                x=optimal['k_values'],
                y=optimal['silhouette_scores'],
                title="Silhouette Score by Number of Clusters",
                labels={'x': 'Number of Clusters', 'y': 'Silhouette Score'},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error in clustering: {e}")

