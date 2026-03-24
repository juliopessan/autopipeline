"""Advanced Resource Optimization & Recommendations"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from lib.api_client import get_api_client

def show():
    st.subheader("🔧 Advanced Resource Management")
    
    api = get_api_client()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Resources",
        "💡 Recommendations",
        "🔄 Auto-Scaling",
        "📊 Cost Analysis"
    ])
    
    # ==================== TAB 1: RESOURCES ====================
    with tab1:
        st.write("### Azure Resources Inventory")
        
        try:
            summary = api.get("/api/resources/summary").json()
            
            # KPIs
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Resources", summary['total_resources'])
            col2.metric("Monthly Cost", f"${summary['total_monthly_cost']:.2f}")
            col3.metric("Annual Cost", f"${summary['estimated_annual_cost']:.2f}")
            
            st.divider()
            
            # Resources table
            resources = api.get("/api/resources/list").json()
            
            df = pd.DataFrame(resources)
            df['cost_per_month'] = df['cost_per_month'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")
    
    # ==================== TAB 2: RECOMMENDATIONS ====================
    with tab2:
        st.write("### Optimization Recommendations")
        
        try:
            recs = api.get("/api/resources/recommendations").json()
            
            # Summary
            col1, col2 = st.columns(2)
            col1.metric("Recommendations", recs['total_recommendations'])
            col2.metric("Potential Savings", f"${recs['total_potential_savings']:.2f}/month")
            
            st.divider()
            
            # Recommendations list
            for rec in recs.get('recommendations', []):
                priority_color = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢"
                }
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        icon = priority_color.get(rec['priority'], '⚪')
                        st.write(f"{icon} **{rec['title']}**")
                        st.caption(rec['description'])
                        st.write(f"Resource: `{rec['resource']}`")
                    
                    with col2:
                        st.write(f"**{rec['potential_savings']}**")
                        st.write(f"**${rec['estimated_monthly_savings']:.2f}**")
                        st.caption("monthly savings")
        
        except Exception as e:
            st.error(f"Error: {e}")
    
    # ==================== TAB 3: AUTO-SCALING ====================
    with tab3:
        st.write("### Auto-Scaling Configuration")
        
        try:
            resources = api.get("/api/resources/list").json()
            resource_names = [f"{r['name']} ({r['id']})" for r in resources]
            
            selected_resource = st.selectbox("Select Resource", resource_names)
            resource_id = selected_resource.split('(')[-1].replace(')', '')
            
            config = api.get(f"/api/resources/autoscaling/{resource_id}").json()
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Instance Configuration**")
                min_inst = st.number_input("Minimum Instances", 
                                          value=config['min_instances'],
                                          min_value=1, max_value=20)
                max_inst = st.number_input("Maximum Instances",
                                          value=config['max_instances'],
                                          min_value=1, max_value=50)
            
            with col2:
                st.write("**Scaling Thresholds**")
                cpu_thresh = st.slider("Scale-up CPU %",
                                      0, 100,
                                      config['cpu_threshold'])
                mem_thresh = st.slider("Scale-up Memory %",
                                      0, 100,
                                      config['memory_threshold'])
            
            st.divider()
            
            # Current metrics
            st.write("### Current Metrics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Instances", "2")
            col2.metric("CPU Usage", "45%")
            col3.metric("Memory Usage", "62%")
            col4.metric("Scaling Status", "Stable")
            
            st.divider()
            
            # Auto-scaling chart
            st.write("### 24h Scaling History")
            
            hours = list(range(24))
            instances = [2 + (i % 4) for i in range(24)]
            
            fig = px.line(
                x=hours,
                y=instances,
                title="Instances Over 24 Hours",
                labels={"x": "Hour of Day", "y": "Active Instances"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("💾 Save Auto-Scaling Config"):
                try:
                    api.post(
                        f"/api/resources/autoscaling/{resource_id}",
                        json={
                            "min_instances": min_inst,
                            "max_instances": max_inst,
                            "cpu_threshold": cpu_thresh,
                            "memory_threshold": mem_thresh,
                            "enabled": True
                        }
                    )
                    st.success("✅ Configuration saved!")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        except Exception as e:
            st.error(f"Error: {e}")
    
    # ==================== TAB 4: COST ANALYSIS ====================
    with tab4:
        st.write("### Resource Cost Analysis")
        
        try:
            cost_data = api.get("/api/resources/cost-by-type").json()
            
            # Pie chart
            labels = list(cost_data['by_type'].keys())
            values = [cost_data['by_type'][k]['cost'] for k in labels]
            
            fig = px.pie(
                values=values,
                names=labels,
                title="Cost Distribution by Resource Type"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed breakdown
            st.write("### Cost Breakdown")
            
            breakdown_data = []
            for resource_type, details in cost_data['by_type'].items():
                breakdown_data.append({
                    'Resource Type': resource_type,
                    'Count': details['count'],
                    'Monthly Cost': f"${details['cost']:.2f}",
                    'Percentage': f"{details['percent']:.1f}%"
                })
            
            df = pd.DataFrame(breakdown_data)
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            col1.metric("Total Monthly", f"${cost_data['total']:.2f}")
            col2.metric("Total Annual", f"${cost_data['total'] * 12:.2f}")
        
        except Exception as e:
            st.error(f"Error: {e}")

