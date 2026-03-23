"""Programs page"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from streamlit_dashboard.lib.api_client import get_api_client

def show():
    st.subheader("💼 Programs")
    
    api_client = get_api_client()
    
    # Tabs
    tab1, tab2 = st.tabs(["Active Programs", "Create New"])
    
    with tab1:
        programs = api_client.get_programs()
        
        if programs:
            df = pd.DataFrame(programs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No programs yet. Create one!")
    
    with tab2:
        st.write("Create a new optimization program")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Program Name")
            goal = st.selectbox("Optimization Goal", ["maximize", "minimize"])
            metric = st.text_input("Metric Name")
        
        with col2:
            baseline = st.number_input("Baseline Value", value=1.0)
            target = st.number_input("Target Value", value=1.5)
            max_it = st.number_input("Max Iterations", value=100, min_value=1)
        
        if st.button("Create Program"):
            if not name or not metric:
                st.error("Name and Metric are required!")
            else:
                result = api_client.create_program(name, goal, metric, baseline, target, max_it)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("Program created!")
                    st.rerun()
