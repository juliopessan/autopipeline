"""Executive Dashboard - Complete Overview"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from lib.api_client import get_api_client
import numpy as np

def show():
    st.subheader("👔 Executive Dashboard")
    st.write("Complete platform overview for decision makers")
    
    api = get_api_client()
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Monthly Cost", "$700", "-15%", delta_color="inverse")
    col2.metric("Utilization", "62%", "+5%")
    col3.metric("Alerts", "3", "↓ 40%", delta_color="inverse")
    col4.metric("Optimizations", "12", "↑ 8")
    col5.metric("ROI", "175%", "+25%")
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs([
        "📊 Financial Overview",
        "🎯 Performance Metrics",
        "💡 Key Insights"
    ])
    
    # ==================== TAB 1: FINANCIAL ====================
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Cost Trend (30 Days)")
            
            days = list(range(1, 31))
            costs = [680 + (i % 15) for i in range(30)]
            
            fig = px.line(
                x=days,
                y=costs,
                title="Daily Cost",
                labels={"x": "Day", "y": "Cost ($)"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### Budget Status")
            
            spent = 700
            budget = 1000
            percent = (spent / budget) * 100
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=percent,
                title={'text': "Budget Used %"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [0, 150]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgreen"},
                        {'range': [50, 80], 'color': "lightyellow"},
                        {'range': [80, 100], 'color': "lightcoral"},
                        {'range': [100, 150], 'color': "darkred"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Cost Breakdown")
            categories = ['VM', 'Database', 'Storage', 'API', 'Other']
            costs_breakdown = [280, 280, 80, 50, 10]
            
            fig = px.pie(
                values=costs_breakdown,
                names=categories,
                title="Monthly Cost by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### Savings Potential")
            
            recommendations = [
                {"type": "Rightsizing", "savings": 120},
                {"type": "Auto-Scaling", "savings": 80},
                {"type": "Cleanup", "savings": 45},
                {"type": "Reserved Instances", "savings": 200}
            ]
            
            df = pd.DataFrame(recommendations)
            
            fig = px.bar(
                df,
                x='type',
                y='savings',
                title="Potential Monthly Savings",
                labels={"savings": "Savings ($)", "type": "Optimization Type"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: PERFORMANCE ====================
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Experiment Performance")
            
            df = pd.DataFrame({
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'Success Rate': [0.78, 0.82, 0.85, 0.88],
                'Avg ROI': [145, 152, 165, 175]
            })
            
            fig = px.line(
                df,
                x='Week',
                y='Success Rate',
                title="Experiment Success Rate Trend",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### Resource Utilization")
            
            resources = ['CPU', 'Memory', 'Storage', 'Network', 'DB']
            utilization = [45, 62, 50, 38, 15]
            
            fig = px.bar(
                x=resources,
                y=utilization,
                title="Resource Utilization %",
                labels={"y": "Utilization (%)"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.write("### System Health")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Uptime", "99.97%")
        col2.metric("Response Time", "245ms", "-12%")
        col3.metric("Error Rate", "0.03%", "↓")
        col4.metric("SLA Status", "✅ Green")
    
    # ==================== TAB 3: INSIGHTS ====================
    with tab3:
        st.write("### Key Insights & Recommendations")
        
        insights = [
            {
                "icon": "💰",
                "title": "30% Cost Reduction Possible",
                "desc": "Implementing all recommendations could save $280/month",
                "action": "Review recommendations in Resource Optimization"
            },
            {
                "icon": "📈",
                "title": "Positive ROI Trend",
                "desc": "ROI increased from 145% to 175% over 4 weeks",
                "action": "Continue current optimization strategy"
            },
            {
                "icon": "🎯",
                "title": "High Utilization Peaks",
                "desc": "CPU peaks at 85% during business hours",
                "action": "Enable auto-scaling to handle spikes"
            },
            {
                "icon": "🚨",
                "title": "Critical Alert Reduced",
                "desc": "Critical alerts down 40% due to monitoring improvements",
                "action": "Maintain alert rules configuration"
            }
        ]
        
        for insight in insights:
            with st.container(border=True):
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.write(insight['icon'])
                
                with col2:
                    st.write(f"**{insight['title']}**")
                    st.caption(insight['desc'])
                    st.write(f"→ {insight['action']}")
        
        st.divider()
        
        st.write("### Action Items")
        
        actions = [
            {"priority": "🔴 High", "task": "Implement VM rightsizing", "owner": "Cloud Ops", "deadline": "This week"},
            {"priority": "🟡 Medium", "task": "Enable auto-scaling", "owner": "DevOps", "deadline": "Next week"},
            {"priority": "🟡 Medium", "task": "Cleanup unused storage", "owner": "Storage Team", "deadline": "Next 2 weeks"},
            {"priority": "🟢 Low", "task": "Review monitoring rules", "owner": "SRE", "deadline": "Next month"}
        ]
        
        df_actions = pd.DataFrame(actions)
        st.dataframe(df_actions, use_container_width=True)

