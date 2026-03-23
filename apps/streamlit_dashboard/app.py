"""Azure Autonomous Data Platform - Streamlit Dashboard with Authentication"""
import streamlit as st
import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from streamlit_dashboard.lib.auth import get_auth_manager
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
    .login-container {
        max-width: 400px;
        margin: 50px auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication
auth = get_auth_manager()

# Login page
if not st.session_state.authenticated:
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Azure Autonomous Data Platform</h1>
        <p>Please login to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    if auth.login("main"):
        st.success(f"Welcome {st.session_state.get('name')}! 🎉")
        st.rerun()
    else:
        if st.session_state.get("authentication_status") is False:
            st.error("Username/password is incorrect")

else:
    # Main dashboard (authenticated)
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Azure Autonomous Data Platform</h1>
        <p>AI-powered pipeline optimization dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.write(f"👤 Logged in as: **{st.session_state.get('name')}**")
        
        page = st.radio("Select page:", [
            "📊 Dashboard",
            "📈 Experiments",
            "💼 Programs",
            "👥 Users" if st.session_state.get("username") == "admin" else None,
            "🧠 ML Analytics", "⚙️ Settings"
        ], options=[p for p in [
            "📊 Dashboard",
            "📈 Experiments",
            "💼 Programs",
            "👥 Users" if st.session_state.get("username") == "admin" else None,
            "🧠 ML Analytics", "⚙️ Settings"
        ] if p])
        
        st.divider()
        st.subheader("Backend Status")
        
        api_client = get_api_client()
        is_healthy = api_client.health_check()
        
        if is_healthy:
            st.success("✅ Backend Online")
        else:
            st.error("❌ Backend Offline")
            st.info("Make sure FastAPI is running on http://localhost:8000")
        
        st.divider()
        
        if st.button("🔒 Logout", use_container_width=True):
            auth.logout()
            st.session_state.authenticated = False
            st.rerun()
    
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
    elif page == "👥 Users" and st.session_state.get("username") == "admin":
        from streamlit_dashboard.lib.user_manager import show_user_management
        show_user_management()
    elif page == "🧠 ML Analytics", "⚙️ Settings":
        from streamlit_dashboard.pages import settings
        settings.show()
    
    # Footer
    st.divider()
    st.caption("🚀 Azure Autonomous Data Platform v1.1 | Powered by Streamlit + FastAPI")
