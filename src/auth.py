#!/usr/bin/env python3
"""
Simple Authentication System for Omri Association Dashboard
Provides basic login/logout functionality
"""

import hashlib
import time
from typing import Any, Dict, Optional

import streamlit as st

from config.config import Config


class AuthManager:
    """Authentication manager for the dashboard"""

    def __init__(self) -> None:
        # Load users from configuration
        users_config = Config.get_auth_users()
        self.users = {}

        for username, user_config in users_config.items():
            self.users[username] = {
                "password_hash": self._hash_password(user_config["password"]),
                "role": user_config["role"],
                "name": user_config["name"],
                "permissions": user_config["permissions"],
            }

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user with username and password"""
        if username in self.users:
            user = self.users[username]
            if user["password_hash"] == self._hash_password(password):
                return True
        return False

    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        if username in self.users:
            user = self.users[username].copy()
            user.pop("password_hash", None)  # Don't expose password hash
            return user
        return None

    def has_permission(self, username: str, permission: str) -> bool:
        """Check if user has specific permission"""
        if username in self.users:
            return permission in self.users[username]["permissions"]
        return False


# Global auth manager instance
auth_manager = AuthManager()


def login_user(username: str, password: str) -> bool:
    """Login user and set session state"""
    if auth_manager.authenticate(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_info = auth_manager.get_user_info(username)
        st.session_state.login_time = time.time()
        return True
    return False


def logout_user() -> None:
    """Logout user and clear session state"""
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    if "username" in st.session_state:
        del st.session_state.username
    if "user_info" in st.session_state:
        del st.session_state.user_info
    if "login_time" in st.session_state:
        del st.session_state.login_time


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    if not st.session_state.get("ENABLE_AUTHENTICATION", Config.ENABLE_AUTHENTICATION):
        return True  # Authentication disabled

    if "authenticated" not in st.session_state:
        return False

    # Check session timeout
    if "login_time" in st.session_state:
        timeout = st.session_state.get("SESSION_TIMEOUT", Config.SESSION_TIMEOUT)
        if time.time() - st.session_state.login_time > timeout:
            logout_user()
            return False

    return st.session_state.authenticated


def get_current_user() -> Optional[str]:
    """Get current authenticated username"""
    if is_authenticated():
        return st.session_state.get("username")
    return None


def get_current_user_info() -> Optional[Dict[str, Any]]:
    """Get current user information"""
    if is_authenticated():
        return st.session_state.get("user_info")
    return None


def has_permission(permission: str) -> bool:
    """Check if current user has specific permission"""
    if not st.session_state.get("ENABLE_AUTHENTICATION", Config.ENABLE_AUTHENTICATION):
        return True  # All permissions when auth disabled

    username = get_current_user()
    if username:
        return auth_manager.has_permission(username, permission)
    return False


def require_auth():
    """Decorator to require authentication for functions"""
    if not is_authenticated():
        st.error("❌ נדרש להתחבר למערכת")
        st.stop()


def show_login_form() -> None:
    """Show login form in Streamlit"""
    st.markdown("### 🔐 התחברות למערכת")

    with st.form("login_form"):
        username = st.text_input("שם משתמש")
        password = st.text_input("סיסמה", type="password")

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🚪 התחבר", use_container_width=True)
        with col2:
            if st.form_submit_button("❌ ביטול", use_container_width=True):
                st.rerun()

        if submit:
            if login_user(username, password):
                st.success("✅ התחברת בהצלחה!")
                st.rerun()
            else:
                st.error("❌ שם משתמש או סיסמה שגויים")

    # Show demo credentials
    with st.expander("💡 פרטי התחברות לדוגמה"):
        st.markdown(
            """
        **מנהל מערכת:**
        - שם משתמש: `admin`
        - סיסמה: `admin123`

        **משתמש רגיל:**
        - שם משתמש: `user`
        - סיסמה: `user123`

        **צופה בלבד:**
        - שם משתמש: `viewer`
        - סיסמה: `view123`
        """
        )


def show_user_info() -> None:
    """Show current user information"""
    if is_authenticated():
        user_info = get_current_user_info()
        if user_info:
            st.sidebar.markdown("### 👤 משתמש נוכחי")
            st.sidebar.markdown(f"**שם:** {user_info['name']}")
            st.sidebar.markdown(f"**תפקיד:** {user_info['role']}")
            st.sidebar.markdown(f"**הרשאות:** {', '.join(user_info['permissions'])}")

            if st.sidebar.button("🚪 התנתק"):
                logout_user()
                st.rerun()
    else:
        st.sidebar.markdown("### 🔐 לא מחובר")
        if st.sidebar.button("🚪 התחבר"):
            st.session_state.show_login = True


def check_auth_and_redirect() -> bool:
    """Check authentication and redirect to login if needed"""
    if not is_authenticated():
        show_login_form()
        return False
    return True
