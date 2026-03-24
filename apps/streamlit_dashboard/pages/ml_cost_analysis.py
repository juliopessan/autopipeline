"""ML + Cost Integration Analytics"""
import streamlit as st
import pandas as pd
import plotly.express as px
from lib.api_client import get_api_client
import numpy as np

def show():
    st.subheader("🧠 ML + Cost Intelligence")
    st.write("Combine ML predictions with cost analysis for smarter optimization")
    
    api = get_api_client()
    
    tab1, tab2, tab3 = st.tabs([
        "💰 Cost-Adjusted Predictions",
        "🎯 Cost-Efficiency Clustering", 
        "📊 ROI vs Performance"
    ])
    
    # ==================== TAB 1: COST-ADJUSTED PREDICTIONS ====================
    with tab1:
        st.write("### Cost-Adjusted Performance Predictions")
        st.write("Predict performance while accounting for cost factors")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            param1 = st.slider("Parameter 1", 0.0, 1.0, 0.5, key="p1_ca")
        with col2:
            param2 = st.slider("Parameter 2", 0.0, 1.0, 0.5, key="p2_ca")
        with col3:
            param3 = st.slider("Parameter 3", 0.0, 1.0, 0.5, key="p3_ca")
        
        if st.button("🔮 Predict with Cost Analysis"):
            # Simulate prediction
            base_prediction = 0.75 + (param1 + param2 + param3) / 3 * 0.5
            estimated_cost = 50 + (param1 + param2 + param3) / 3 * 150
            cost_per_unit_performance = estimated_cost / base_prediction if base_prediction > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Predicted Performance", f"{base_prediction:.2f}")
            col2.metric("Estimated Cost", f"${estimated_cost:.2f}")
            col3.metric("Cost/Unit", f"${cost_per_unit_performance:.2f}")
            
            # Recommendation
            st.divider()
            
            if cost_per_unit_performance < 50:
                st.success("✅ Excellent cost-efficiency!")
            elif cost_per_unit_performance < 100:
                st.info("ℹ️ Good cost-efficiency")
            else:
                st.warning("⚠️ High cost per unit - consider optimization")
    
    # ==================== TAB 2: COST-EFFICIENCY CLUSTERING ====================
    with tab2:
        st.write("### Cost-Efficiency Clusters")
        st.write("Group experiments by cost-to-performance ratio")
        
        # Generate sample data
        np.random.seed(42)
        n_experiments = 50
        
        costs = np.random.normal(75, 30, n_experiments)
        costs = np.clip(costs, 20, 300)
        
        performance = np.random.normal(0.75, 0.2, n_experiments)
        performance = np.clip(performance, 0.1, 1.0)
        
        efficiency = performance / (costs / 100)
        
        df = pd.DataFrame({
            'Experiment': range(1, n_experiments + 1),
            'Cost': costs,
            'Performance': performance,
            'Efficiency': efficiency
        })
        
        # Categorize clusters
        df['Cluster'] = pd.cut(df['Efficiency'], bins=3, labels=['Low Efficiency', 'Medium Efficiency', 'High Efficiency'])
        
        # Scatter plot
        fig = px.scatter(
            df,
            x='Cost',
            y='Performance',
            color='Cluster',
            size='Efficiency',
            hover_data=['Experiment', 'Efficiency'],
            title="Cost vs Performance Clustering",
            color_discrete_map={
                'Low Efficiency': '#ff7f0e',
                'Medium Efficiency': '#ffdd57',
                'High Efficiency': '#2ecc71'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cluster summary
        st.write("### Cluster Summary")
        summary = df.groupby('Cluster').agg({
            'Cost': ['mean', 'min', 'max'],
            'Performance': ['mean', 'min', 'max'],
            'Efficiency': 'mean',
            'Experiment': 'count'
        }).round(2)
        
        st.dataframe(summary, use_container_width=True)
    
    # ==================== TAB 3: ROI VS PERFORMANCE ====================
    with tab3:
        st.write("### ROI vs Performance Analysis")
        
        # Generate sample data
        np.random.seed(42)
        n_experiments = 30
        
        baseline_cost = 100
        experiment_costs = np.random.normal(75, 25, n_experiments)
        experiment_costs = np.clip(experiment_costs, 30, 200)
        
        performance_gain = np.random.normal(15, 8, n_experiments)
        performance_gain = np.clip(performance_gain, -10, 40)
        
        roi_values = (performance_gain * 100 / baseline_cost)
        
        df = pd.DataFrame({
            'Experiment': range(1, n_experiments + 1),
            'Cost': experiment_costs,
            'Performance Gain %': performance_gain,
            'ROI %': roi_values
        })
        
        # Categorize ROI
        df['ROI Level'] = pd.cut(df['ROI %'], bins=3, labels=['Negative ROI', 'Moderate ROI', 'Strong ROI'])
        
        # Bubble chart
        fig = px.scatter(
            df,
            x='Cost',
            y='Performance Gain %',
            color='ROI %',
            size='ROI %',
            hover_data=['Experiment', 'ROI %'],
            title="ROI Analysis: Cost vs Performance Gain",
            color_continuous_scale='RdYlGn'
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.add_vline(x=baseline_cost, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Cost", f"${df['Cost'].mean():.2f}")
        col2.metric("Avg Performance Gain", f"{df['Performance Gain %'].mean():.1f}%")
        col3.metric("Avg ROI", f"{df['ROI %'].mean():.1f}%")
        
        # Recommendations
        st.divider()
        st.write("### Recommendations")
        
        positive_roi = len(df[df['ROI %'] > 0])
        total = len(df)
        roi_rate = (positive_roi / total) * 100
        
        if roi_rate > 70:
            st.success(f"✅ {roi_rate:.0f}% of experiments show positive ROI - continue current approach")
        elif roi_rate > 40:
            st.info(f"ℹ️ {roi_rate:.0f}% of experiments show positive ROI - optimization needed")
        else:
            st.warning(f"⚠️ Only {roi_rate:.0f}% of experiments show positive ROI - major optimization needed")

