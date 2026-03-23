"""Settings page"""
import streamlit as st

def show():
    st.subheader("⚙️ Settings")
    
    st.write("### Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        backend_url = st.text_input("Backend URL", "http://localhost:8000")
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 30)
    
    with col2:
        theme = st.selectbox("Theme", ["Light", "Dark"])
        debug_mode = st.checkbox("Debug Mode")
    
    st.divider()
    
    st.write("### About")
    st.info("""
    **Azure Autonomous Data Platform v1.0**
    
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
