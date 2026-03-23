"""User management utilities"""
from lib.auth import get_auth_manager
import streamlit as st

def show_user_management():
    """Admin page for user management"""
    st.subheader("👥 User Management")
    
    auth = get_auth_manager()
    
    # Check if user is admin
    if st.session_state.get("username") != "admin":
        st.error("❌ Only admins can access user management")
        st.stop()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Users", "Register User", "Settings"])
    
    with tab1:
        st.write("### Registered Users")
        credentials = auth.load_credentials()
        
        users_data = []
        for username, info in credentials.get("usernames", {}).items():
            users_data.append({
                "Username": username,
                "Name": info.get("name", "N/A"),
                "Email": info.get("email", "N/A")
            })
        
        if users_data:
            st.dataframe(users_data, use_container_width=True)
        else:
            st.info("No users registered")
    
    with tab2:
        st.write("### Register New User")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
        
        with col2:
            new_name = st.text_input("Full Name")
            new_password = st.text_input("Password", type="password")
        
        if st.button("Register", type="primary"):
            if not all([new_username, new_email, new_name, new_password]):
                st.error("All fields are required")
            else:
                success, message = auth.register_user(
                    new_username, new_email, new_name, new_password
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab3:
        st.write("### Change Your Password")
        
        current_password = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Change Password"):
            if new_pass != confirm_pass:
                st.error("Passwords don't match")
            else:
                success, message = auth.change_password(
                    st.session_state.get("username"),
                    new_pass
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
