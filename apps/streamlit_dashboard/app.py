"""Azure Autonomous Data Platform - Streamlit Dashboard"""
import streamlit as st
import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from streamlit_dashboard.lib.api_client import get_api_client

# Configure page
st.set_page_config(
    page_title="Azure Autonomous Data Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #F04E37 0%, #d93d28 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #F04E37;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Azure Autonomous Data Platform</h1>
    <p>AI-powered pipeline optimization dashboard</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Select page:", [
        "📊 Dashboard",
        "📈 Experiments",
        "💼 Programs",
        "⚙️ Settings"
    ])
    
    st.divider()
    st.subheader("Backend Status")
    
    api_client = get_api_client()
    is_healthy = api_client.health_check()
    
    if is_healthy:
        st.success("✅ Backend Online")
    else:
        st.error("❌ Backend Offline")
        st.info("Make sure FastAPI is running on http://localhost:8000")

# Page routing
if page == "📊 Dashboard":
    from streamlit_dashboard.pages import dashboard
    dashboard.show()
elif page == "📈 Experiments":
    from streamlit_dashboard.pages import experiments
    experiments.show()
elif page == "💼 Programs":
    from streamlit_dashboard.pages import programs
    programs.show()
elif page == "⚙️ Settings":
    from streamlit_dashboard.pages import settings
    settings.show()

# Footer
st.divider()
st.caption("🚀 Azure Autonomous Data Platform v1.0 | Powered by Streamlit + FastAPI")
