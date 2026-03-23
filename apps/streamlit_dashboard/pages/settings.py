"""Settings page"""
import streamlit as st
from lib.auth import get_auth_manager

def show():
    st.subheader("⚙️ Settings")
    
    auth = get_auth_manager()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Account", "Application", "About"])
    
    with tab1:
        st.write("### Account Settings")
        
        st.write(f"**Username:** {st.session_state.get('username')}")
        st.write(f"**Name:** {st.session_state.get('name')}")
        
        st.divider()
        
        st.write("#### Change Password")
        
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Update Password"):
            if new_password != confirm_password:
                st.error("Passwords don't match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, message = auth.change_password(
                    st.session_state.get("username"),
                    new_password
                )
                if success:
                    st.success("✅ " + message)
                else:
                    st.error("❌ " + message)
    
    with tab2:
        st.write("### Application Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            backend_url = st.text_input("Backend URL", "http://localhost:8000")
            refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 30)
        
        with col2:
            theme = st.selectbox("Theme", ["Light", "Dark"])
            debug_mode = st.checkbox("Debug Mode")
    
    with tab3:
        st.write("### About")
        st.info("""
        **Azure Autonomous Data Platform v1.1**
        
        Features:
        - 🔐 User Authentication
        - 📊 Real-time Dashboard
        - 📈 Experiment Tracking
        - 🧠 ML Analytics (coming soon)
        - 🔔 Webhooks (coming soon)
        
        Stack:
        - Framework: Streamlit
        - Backend: FastAPI
        - Language: Python
        - License: MIT
        """)
        
        st.write("### Resources")
        st.markdown("""
        - [GitHub Repository](https://github.com/juliopessan/autopipeline)
        - [Streamlit Docs](https://docs.streamlit.io/)
        - [FastAPI Docs](https://fastapi.tiangolo.com/)
        """)
