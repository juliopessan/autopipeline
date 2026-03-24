"""Resource Optimization Dashboard"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    st.subheader("⚙️ Resource Optimization")
    
    tab1, tab2, tab3 = st.tabs(["🖥️ Resources", "📊 Quotas", "🔄 Auto-Scaling"])
    
    # ==================== TAB 1: RESOURCES ====================
    with tab1:
        st.write("### Azure Resources in Use")
        
        resources_data = {
            "Compute": {
                "type": "Virtual Machines",
                "count": 2,
                "sku": "Standard_B2s",
                "cost": "$450/month"
            },
            "Storage": {
                "type": "Azure Storage",
                "count": 1,
                "gb_used": 500,
                "cost": "$120/month"
            },
            "Database": {
                "type": "PostgreSQL",
                "count": 1,
                "sku": "General Purpose",
                "cost": "$80/month"
            },
            "API": {
                "type": "API Management",
                "count": 1,
                "calls_per_day": 10000,
                "cost": "$50/month"
            }
        }
        
        total_cost = 0
        for resource_type, details in resources_data.items():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**{resource_type}**")
                    st.caption(details["type"])
                
                with col2:
                    for k, v in details.items():
                        if k not in ["type", "cost"]:
                            st.caption(f"• {k.replace('_', ' ').title()}: {v}")
                
                with col3:
                    cost_str = details.get("cost", "TBD")
                    st.metric("Cost", cost_str)
                    
                    # Extract monthly cost
                    if "/month" in str(cost_str):
                        try:
                            cost_val = float(cost_str.replace("$", "").replace("/month", ""))
                            total_cost += cost_val
                        except:
                            pass
        
        st.divider()
        st.metric("💰 Total Monthly Cost", f"${total_cost:.0f}/month")
    
    # ==================== TAB 2: QUOTAS ====================
    with tab2:
        st.write("### Azure Service Quotas")
        
        quotas = [
            {"name": "CPU Cores", "used": 8, "limit": 20, "unit": "cores"},
            {"name": "RAM (GB)", "used": 32, "limit": 64, "unit": "GB"},
            {"name": "Storage (GB)", "used": 500, "limit": 1000, "unit": "GB"},
            {"name": "API Calls/min", "used": 800, "limit": 10000, "unit": "calls/min"},
            {"name": "Database Connections", "used": 15, "limit": 100, "unit": "connections"},
        ]
        
        for quota in quotas:
            percent = (quota['used'] / quota['limit']) * 100
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.write(f"**{quota['name']}**")
                
                with col2:
                    st.progress(min(percent / 100, 1.0))
                    st.caption(f"{quota['used']} / {quota['limit']} {quota['unit']}")
                
                with col3:
                    if percent > 85:
                        st.write("🚨 Critical")
                    elif percent > 70:
                        st.write("⚠️ Warning")
                    else:
                        st.write("✅ OK")
    
    # ==================== TAB 3: AUTO-SCALING ====================
    with tab3:
        st.write("### Auto-Scaling Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Compute Auto-Scaling**")
            min_instances = st.number_input("Min Instances", value=1, min_value=1, max_value=10)
            max_instances = st.number_input("Max Instances", value=5, min_value=1, max_value=20)
            
        with col2:
            st.write("**Scaling Thresholds**")
            cpu_threshold = st.slider("Scale-up CPU %", 0, 100, 75)
            memory_threshold = st.slider("Scale-up Memory %", 0, 100, 80)
        
        st.divider()
        
        # Current scaling metrics
        st.write("**Current Metrics**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Instances", "2")
        col2.metric("CPU Usage", "45%")
        col3.metric("Memory Usage", "62%")
        
        st.info("✅ System is within normal parameters. No scaling needed.")
        
        if st.button("💾 Save Auto-Scaling Config"):
            st.success("✅ Configuration saved!")
            st.balloons()

