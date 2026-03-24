"""Cost Intelligence Dashboard"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from lib.api_client import get_api_client
from datetime import datetime, timedelta

def show():
    st.subheader("💰 Cost Intelligence Dashboard")
    
    api = get_api_client()
    
    # Get cost summary
    try:
        summary = api.get("/api/cost/summary?days=30").json()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Cost (30d)", f"${summary['total_cost']:.2f}")
        col2.metric("Avg Cost/Exp", f"${summary['average_cost']:.2f}")
        col3.metric("Experiments", f"{summary['experiments']}")
        col4.metric("Trend", summary['trend'].upper())
        
    except Exception as e:
        st.error(f"Error loading summary: {e}")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Trends", 
        "💡 Recommendations", 
        "📈 ROI Analysis",
        "🚨 Top Expensive"
    ])
    
    # ==================== TAB 1: TRENDS ====================
    with tab1:
        st.write("### Cost Trends Over Time")
        
        # Generate sample data
        days = pd.date_range(start='2025-02-23', end='2025-03-23', freq='D')
        costs = [10 + (i % 20) for i in range(len(days))]
        
        fig = px.line(
            x=days, y=costs,
            title="Daily Experiment Costs",
            labels={"x": "Date", "y": "Cost ($)"},
            markers=True
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost breakdown pie chart
        st.write("### Cost Breakdown by Resource Type")
        
        breakdown = {
            "Compute": 450,
            "Storage": 120,
            "API Calls": 80,
            "Network": 50
        }
        
        fig = px.pie(
            values=list(breakdown.values()),
            names=list(breakdown.keys()),
            title="Monthly Cost Breakdown"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: RECOMMENDATIONS ====================
    with tab2:
        st.write("### Cost Optimization Recommendations")
        
        try:
            experiments = api.get("/api/experiments").json()
            
            if experiments and len(experiments) > 0:
                selected_exp = st.selectbox(
                    "Select Experiment",
                    [e['id'] for e in experiments]
                )
                
                if st.button("Get Recommendations", key="get_recs"):
                    try:
                        rec_response = api.get(f"/api/cost/recommendations/{selected_exp}").json()
                        
                        for rec in rec_response.get("recommendations", []):
                            severity_colors = {
                                "high": "🔴",
                                "medium": "🟡",
                                "low": "🟢"
                            }
                            
                            with st.container(border=True):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"{severity_colors.get(rec['priority'], '🔵')} **{rec['title']}**")
                                    st.caption(rec['description'])
                                
                                with col2:
                                    st.write(f"**{rec['potential_savings']}**")
                                    st.caption("potential savings")
                    except Exception as e:
                        st.error(f"Error getting recommendations: {e}")
            else:
                st.info("No experiments yet. Create some experiments to get recommendations!")
        
        except Exception as e:
            st.error(f"Error: {e}")
    
    # ==================== TAB 3: ROI ANALYSIS ====================
    with tab3:
        st.write("### ROI Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            baseline = st.number_input("Baseline Cost ($)", value=100.0, min_value=0.0)
        
        with col2:
            experiment_cost = st.number_input("Experiment Cost ($)", value=75.0, min_value=0.0)
        
        with col3:
            if st.button("Calculate ROI", key="calc_roi"):
                if baseline > 0:
                    roi_percentage = ((baseline - experiment_cost) / baseline) * 100
                    savings = baseline - experiment_cost
                    
                    # Display ROI gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=roi_percentage,
                        title={'text': "ROI %"},
                        delta={'reference': 0},
                        gauge={
                            'axis': {'range': [-50, 150]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [-50, 0], 'color': "lightcoral"},
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "lightyellow"},
                                {'range': [50, 75], 'color': "lightgreen"},
                                {'range': [75, 150], 'color': "darkgreen"}
                            ]
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("ROI %", f"{roi_percentage:.1f}%")
                    col2.metric("Savings", f"${savings:.2f}")
                    col3.metric("Result", "✅ Positive" if roi_percentage > 0 else "❌ Negative")
                else:
                    st.error("Baseline cost must be greater than 0")
    
    # ==================== TAB 4: TOP EXPENSIVE ====================
    with tab4:
        st.write("### Top 10 Most Expensive Experiments")
        
        try:
            expensive = api.get("/api/cost/top-expensive?limit=10").json()
            
            if expensive.get("experiments"):
                df = pd.DataFrame(expensive["experiments"])
                
                # Format columns
                df['cost'] = df['cost'].apply(lambda x: f"${x:.2f}")
                df['cost_per_minute'] = df['cost_per_minute'].apply(lambda x: f"${x:.3f}")
                df['duration'] = df['duration'].apply(lambda x: f"{x}s ({x/60:.0f}m)")
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No experiments logged yet")
        except Exception as e:
            st.error(f"Error: {e}")

