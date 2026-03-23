"""Dashboard page"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from streamlit_dashboard.lib.api_client import get_api_client
from streamlit_dashboard.lib.utils import generate_mock_metrics, get_status_color
from streamlit_dashboard.lib.charts import success_rate_chart, experiments_chart

def show():
    st.subheader("📊 Dashboard")
    
    api_client = get_api_client()
    data = api_client.get_dashboard()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Experiments",
            value=data.get('total_experiments', 0),
            delta=10
        )
    
    with col2:
        success = data.get('success_rate', 0)
        st.metric(
            label="Success Rate",
            value=f"{success*100:.1f}%",
            delta="↑5%"
        )
    
    with col3:
        st.metric(
            label="Total Cost",
            value=f"${data.get('total_cost', 0):.2f}",
            delta="$50"
        )
    
    with col4:
        st.metric(
            label="Budget Remaining",
            value=f"${data.get('budget_remaining', 0):.2f}",
            delta="$100"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        metrics = generate_mock_metrics()
        fig = success_rate_chart(metrics)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = experiments_chart(
            data.get('successful_experiments', 0),
            data.get('failed_experiments', 0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Programs Table
    st.subheader("Active Programs")
    programs = data.get('programs', [])
    
    if programs:
        programs_df = pd.DataFrame(programs)
        st.dataframe(programs_df, use_container_width=True)
    else:
        st.info("No active programs yet. Create one to get started!")
    
    # Auto-refresh info
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    with col2:
        st.caption(f"⏱️ Last updated: {datetime.now().strftime('%H:%M:%S')}")
