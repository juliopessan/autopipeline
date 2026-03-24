"""Monitoring & Alerts Dashboard"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from lib.api_client import get_api_client
from datetime import datetime, timedelta

def show():
    st.subheader("📊 Monitoring & Alerts")
    
    api = get_api_client()
    
    # Get monitoring summary
    try:
        summary = api.get("/api/monitoring/summary").json()
        
        # Display KPI metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Events", f"{summary['total_events']}")
        col2.metric("Experiments", f"{summary['experiments_completed']}")
        col3.metric("Anomalies", f"{summary['anomalies_detected']}")
        col4.metric("Alerts", f"{summary['alerts_triggered']}")
        col5.metric("🚨 Critical", f"{summary['critical_alerts']}")
        
    except Exception as e:
        st.error(f"Error loading summary: {e}")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚨 Active Alerts",
        "📈 Events Timeline",
        "💰 Budget Monitor",
        "📋 Event Logs"
    ])
    
    # ==================== TAB 1: ACTIVE ALERTS ====================
    with tab1:
        st.write("### Active Alerts")
        
        try:
            alerts = api.get("/api/monitoring/alerts").json()
            
            if alerts:
                # Filter by severity
                severity_filter = st.selectbox(
                    "Filter by Severity",
                    ["All", "Critical", "High", "Medium", "Low"]
                )
                
                if severity_filter != "All":
                    alerts = [a for a in alerts if a.get('severity') == severity_filter.lower()]
                
                # Display alerts
                for alert in alerts:
                    severity_color = {
                        "critical": "🔴",
                        "high": "🟠",
                        "medium": "🟡",
                        "low": "🟢"
                    }
                    
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            icon = severity_color.get(alert.get('severity'), '⚪')
                            st.write(f"{icon} **{alert.get('type', 'Unknown').upper()}**")
                            st.caption(alert.get('message', ''))
                        
                        with col2:
                            st.write(f"**{alert.get('value', 0):.2f}**")
                        
                        with col3:
                            ts = alert.get('timestamp', '')
                            if ts:
                                try:
                                    dt = datetime.fromisoformat(ts)
                                    st.caption(dt.strftime("%H:%M:%S"))
                                except:
                                    st.caption(ts[-8:])
            else:
                st.info("✅ No active alerts - system is healthy!")
        
        except Exception as e:
            st.error(f"Error loading alerts: {e}")
    
    # ==================== TAB 2: EVENTS TIMELINE ====================
    with tab2:
        st.write("### Events Timeline (Last 7 Days)")
        
        try:
            timeline = api.get("/api/monitoring/timeline?days=7").json()
            
            if timeline:
                # Prepare data for chart
                dates = sorted(timeline.keys())
                counts = [timeline[d]['count'] for d in dates]
                
                # Line chart
                fig = px.line(
                    x=dates,
                    y=counts,
                    title="Events per Day",
                    labels={"x": "Date", "y": "Event Count"},
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary table
                st.write("### Event Summary")
                data = []
                for date in dates:
                    event_counts = {}
                    for event in timeline[date]['events']:
                        event_counts[event] = event_counts.get(event, 0) + 1
                    
                    data.append({
                        "Date": date,
                        "Total": timeline[date]['count'],
                        "Events": ", ".join(f"{k}:{v}" for k, v in event_counts.items())
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No events in timeline")
        
        except Exception as e:
            st.error(f"Error loading timeline: {e}")
    
    # ==================== TAB 3: BUDGET MONITOR ====================
    with tab3:
        st.write("### Budget Monitoring")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            spent = st.number_input("Amount Spent ($)", value=700.0, min_value=0.0)
        
        with col2:
            budget = st.number_input("Monthly Budget ($)", value=1000.0, min_value=0.0)
        
        with col3:
            if st.button("📊 Evaluate Budget", key="eval_budget"):
                try:
                    result = api.post(
                        "/api/monitoring/evaluate-budget",
                        json={"spent": spent, "budget": budget}
                    ).json()
                    
                    percent = result['percent_used']
                    
                    # Gauge chart
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
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 100
                            }
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Alerts
                    if result.get('alerts'):
                        st.write("### Budget Alerts")
                        for alert in result['alerts']:
                            severity = alert.get('severity', 'info')
                            icon = '🔴' if severity == 'critical' else '🟡'
                            st.warning(f"{icon} {alert.get('message', '')}")
                    else:
                        st.success("✅ Budget is within limits")
                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # ==================== TAB 4: EVENT LOGS ====================
    with tab4:
        st.write("### Recent Events")
        
        try:
            limit = st.slider("Show last N events", 10, 500, 100)
            events = api.get(f"/api/monitoring/events?limit={limit}").json()
            
            if events.get('events'):
                # Convert to DataFrame
                df_events = []
                for event in events['events']:
                    props = event.get('properties', {})
                    df_events.append({
                        'Time': event.get('timestamp', '')[-8:],
                        'Event': event.get('name', ''),
                        'Experiment ID': props.get('experiment_id', '-'),
                        'Status': props.get('status', '-'),
                        'Result': props.get('result', '-')
                    })
                
                df = pd.DataFrame(df_events)
                st.dataframe(df, use_container_width=True)
                
                st.caption(f"Showing {len(df_events)} events")
            else:
                st.info("No events yet")
        
        except Exception as e:
            st.error(f"Error: {e}")

