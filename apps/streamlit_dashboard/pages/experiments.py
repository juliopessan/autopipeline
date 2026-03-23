"""Experiments page"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from streamlit_dashboard.lib.api_client import get_api_client

def show():
    st.subheader("📈 Experiments")
    
    api_client = get_api_client()
    
    # Tabs
    tab1, tab2 = st.tabs(["Recent Experiments", "Create New"])
    
    with tab1:
        experiments = api_client.get_experiments()
        
        if experiments:
            df = pd.DataFrame(experiments)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No experiments yet")
    
    with tab2:
        st.write("Create a new experiment")
        
        col1, col2 = st.columns(2)
        with col1:
            program_id = st.text_input("Program ID")
            param1 = st.number_input("Parameter 1", value=0.5)
        
        with col2:
            param2 = st.number_input("Parameter 2", value=0.8)
            param3 = st.number_input("Parameter 3", value=1.0)
        
        if st.button("Create Experiment"):
            params = {"p1": param1, "p2": param2, "p3": param3}
            result = api_client.create_experiment(program_id, params)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success("Experiment created!")
                st.rerun()
