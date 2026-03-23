"""Authentication module for Streamlit Dashboard"""
import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
import json
from pathlib import Path
from typing import Dict, Tuple, Optional

class AuthManager:
    """Manage user authentication"""
    
    def __init__(self, credentials_path: str = "data/credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.credentials_path.parent.mkdir(exist_ok=True)
        self.authenticator = None
        self.setup_authenticator()
    
    def setup_authenticator(self):
        """Initialize Streamlit authenticator"""
        credentials = self.load_credentials()
        
        # Validate credentials structure
        if "usernames" not in credentials:
            credentials["usernames"] = {}
        
        self.authenticator = stauth.Authenticate(
            credentials=credentials,
            cookie_name="autopipeline_auth",
            key="autopipeline-secret-key-v1",
            cookie_expiry_days=30
        )
    
    def load_credentials(self) -> Dict:
        """Load credentials from file"""
        if self.credentials_path.exists():
            with open(self.credentials_path, 'r') as f:
                return json.load(f)
        
        # Default credentials
        return {
            "usernames": {
                "admin": {
                    "email": "admin@company.com",
                    "name": "Admin User",
                    "password": self.hash_password("admin123")
                },
                "user": {
                    "email": "user@company.com",
                    "name": "Test User",
                    "password": self.hash_password("user123")
                }
            }
        }
    
    def save_credentials(self, credentials: Dict) -> bool:
        """Save credentials to file"""
        try:
            with open(self.credentials_path, 'w') as f:
                json.dump(credentials, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving credentials: {e}")
            return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def login(self, location: str = "main") -> bool:
        """
        Render login form
        Returns True if login successful
        """
        name, authentication_status, username = self.authenticator.login(
            "Login",
            location
        )
        
        if authentication_status:
            st.session_state["username"] = username
            st.session_state["name"] = name
            st.session_state["authenticated"] = True
            return True
        
        return False
    
    def logout(self, button_name: str = "Logout", location: str = "sidebar") -> bool:
        """Render logout button"""
        self.authenticator.logout(button_name, location)
        if st.session_state.get("authentication_status") is False:
            st.session_state["authenticated"] = False
            return True
        return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get("authentication_status", False)
    
    def get_current_user(self) -> Optional[str]:
        """Get current authenticated user"""
        return st.session_state.get("username")
    
    def get_current_name(self) -> Optional[str]:
        """Get current user's display name"""
        return st.session_state.get("name")
    
    def register_user(self, username: str, email: str, name: str, password: str) -> Tuple[bool, str]:
        """Register new user"""
        credentials = self.load_credentials()
        
        # Validate
        if username in credentials.get("usernames", {}):
            return False, "Username already exists"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Add user
        credentials["usernames"][username] = {
            "email": email,
            "name": name,
            "password": self.hash_password(password)
        }
        
        if self.save_credentials(credentials):
            self.setup_authenticator()
            return True, "User registered successfully"
        
        return False, "Error registering user"
    
    def change_password(self, username: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        credentials = self.load_credentials()
        
        if username not in credentials.get("usernames", {}):
            return False, "User not found"
        
        if len(new_password) < 6:
            return False, "Password must be at least 6 characters"
        
        credentials["usernames"][username]["password"] = self.hash_password(new_password)
        
        if self.save_credentials(credentials):
            self.setup_authenticator()
            return True, "Password changed successfully"
        
        return False, "Error changing password"

def login_required(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authentication_status"):
            st.error("❌ Please login first")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

# Singleton instance
_auth_manager = None

def get_auth_manager() -> AuthManager:
    """Get singleton AuthManager instance"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
