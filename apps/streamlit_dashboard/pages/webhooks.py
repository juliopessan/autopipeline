"""Webhook Management Dashboard"""
import streamlit as st
import pandas as pd
from lib.api_client import get_api_client

def show():
    st.subheader("🔔 Webhook Management")
    st.write("Configure webhooks for real-time event notifications (Slack, Teams, etc.)")
    
    api = get_api_client()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Active Webhooks", "Create Webhook", "Documentation"])
    
    # ==================== TAB 1: ACTIVE WEBHOOKS ====================
    with tab1:
        st.write("### Active Webhooks")
        
        try:
            webhooks = api.get("/api/webhooks").json()
            
            if not webhooks:
                st.info("No webhooks configured yet. Create one in the 'Create Webhook' tab!")
            else:
                # Display webhooks
                for webhook in webhooks:
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{webhook['name']}**")
                        st.caption(f"Event: {webhook['event_type']}")
                        st.caption(f"URL: {webhook['url'][:50]}...")
                    
                    with col2:
                        status = "🟢 Active" if webhook['is_active'] else "🔴 Inactive"
                        st.write(status)
                    
                    with col3:
                        if st.button("Test", key=f"test_{webhook['id']}"):
                            result = api.post(f"/api/webhooks/{webhook['id']}/test").json()
                            st.success("✅ Test sent!")
                    
                    with col4:
                        if st.button("Delete", key=f"del_{webhook['id']}"):
                            api.delete(f"/api/webhooks/{webhook['id']}")
                            st.success("Deleted!")
                            st.rerun()
                    
                    st.divider()
        
        except Exception as e:
            st.error(f"Error loading webhooks: {e}")
    
    # ==================== TAB 2: CREATE WEBHOOK ====================
    with tab2:
        st.write("### Create New Webhook")
        
        name = st.text_input("Webhook Name", placeholder="e.g., Slack Notifications")
        
        url = st.text_input(
            "Webhook URL",
            placeholder="e.g., https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
        )
        
        event_type = st.selectbox("Event Type", [
            "experiment_created",
            "experiment_completed",
            "experiment_failed",
            "anomaly_detected",
            "program_completed",
            "all"
        ])
        
        st.info("""
        **Event Types:**
        - `experiment_created` - When a new experiment is created
        - `experiment_completed` - When an experiment finishes
        - `experiment_failed` - When an experiment fails
        - `anomaly_detected` - When an anomaly is detected
        - `program_completed` - When a program finishes
        - `all` - All events
        """)
        
        if st.button("Create Webhook", type="primary"):
            if not all([name, url, event_type]):
                st.error("Please fill in all fields")
            else:
                try:
                    payload = {
                        "name": name,
                        "url": url,
                        "event_type": event_type
                    }
                    
                    result = api.post("/api/webhooks", json=payload)
                    
                    if result.status_code == 200:
                        st.success("✅ Webhook created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"Error creating webhook: {e}")
    
    # ==================== TAB 3: DOCUMENTATION ====================
    with tab3:
        st.write("### Webhook Documentation")
        
        st.write("#### What are Webhooks?")
        st.write("""
        Webhooks allow you to receive real-time notifications when events occur in your optimization programs.
        When an event is triggered, we send a JSON POST request to your configured webhook URL.
        """)
        
        st.write("#### Webhook Payload Example")
        st.code("""{
  "event": "experiment_completed",
  "timestamp": "2025-03-23T12:00:00Z",
  "data": {
    "experiment_id": 42,
    "program_id": 5,
    "result": 1.25,
    "cost": 0.50,
    "duration_seconds": 120,
    "parameters": {"param1": 0.5, "param2": 0.8, "param3": 0.3}
  }
}""", language="json")
        
        st.write("#### Slack Integration Example")
        st.write("""
        To integrate with Slack:
        1. Go to your Slack workspace's Apps → Create New App
        2. Enable Incoming Webhooks
        3. Create a webhook for the channel
        4. Copy the webhook URL here
        5. Create webhook with event type `all`
        
        We'll send JSON to Slack's webhook endpoint, which it will post to your channel!
        """)
        
        st.write("#### Microsoft Teams Integration Example")
        st.write("""
        To integrate with Teams:
        1. Go to your Teams channel
        2. Click the three dots menu
        3. Select "Connectors"
        4. Search for "Incoming Webhook"
        5. Configure and copy the webhook URL
        6. Create webhook with event type `all`
        """)
        
        st.write("#### Custom Integration")
        st.write("""
        You can create custom integrations by:
        1. Setting up an endpoint on your server
        2. Pointing the webhook URL to your endpoint
        3. Processing the JSON payload
        4. Returning HTTP 200 for success
        """)

