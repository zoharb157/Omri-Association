#!/usr/bin/env python3
"""
Configuration Management for Omri Association Dashboard
Handles environment variables, settings, and configuration
"""

import logging
import os
from typing import Any, Dict

import streamlit as st


class DashboardConfig:
    """Dashboard configuration management class"""

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and defaults"""
        config = {
            # Dashboard Settings
            "DASHBOARD_PORT": int(os.getenv("DASHBOARD_PORT", 8501)),
            "DASHBOARD_HOST": os.getenv("DASHBOARD_HOST", "0.0.0.0"),
            "DASHBOARD_TITLE": os.getenv("DASHBOARD_TITLE", "מערכת ניהול עמותת עמרי"),
            # Google Sheets Settings
            "GOOGLE_SHEETS_SPREADSHEET_ID": os.getenv(
                "GOOGLE_SHEETS_SPREADSHEET_ID", "1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo"
            ),
            "GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE": os.getenv(
                "GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE", "service_account.json"
            ),
            # Data Settings
            "DATA_REFRESH_INTERVAL": int(os.getenv("DATA_REFRESH_INTERVAL", 300)),  # seconds
            "DATA_CACHE_ENABLED": os.getenv("DATA_CACHE_ENABLED", "true").lower() == "true",
            "MAX_ROWS_DISPLAY": int(os.getenv("MAX_ROWS_DISPLAY", 1000)),
            # Logging Settings
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "LOG_FILE": os.getenv("LOG_FILE", "dashboard.log"),
            # Security Settings
            "ENABLE_PUBLIC_ACCESS": os.getenv("ENABLE_PUBLIC_ACCESS", "false").lower() == "true",
            "ENABLE_AUTHENTICATION": os.getenv("ENABLE_AUTHENTICATION", "false").lower() == "true",
            "SESSION_TIMEOUT": int(os.getenv("SESSION_TIMEOUT", 3600)),  # seconds
            # UI Settings
            "ENABLE_DARK_MODE": os.getenv("ENABLE_DARK_MODE", "false").lower() == "true",
            "ENABLE_ANIMATIONS": os.getenv("ENABLE_ANIMATIONS", "true").lower() == "true",
            "ENABLE_EXPORT": os.getenv("ENABLE_EXPORT", "true").lower() == "true",
            # Performance Settings
            "ENABLE_CACHING": os.getenv("ENABLE_CACHING", "true").lower() == "true",
            "CACHE_TTL": int(os.getenv("CACHE_TTL", 300)),  # seconds
            "MAX_CONCURRENT_REQUESTS": int(os.getenv("MAX_CONCURRENT_REQUESTS", 10)),
        }

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()

    def validate(self) -> bool:
        """Validate configuration values"""
        try:
            # Check required files
            if not os.path.exists(self.get("GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE")):
                logging.warning(
                    f"Service account file not found: {self.get('GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE')}"
                )

            # Validate numeric values
            if self.get("DASHBOARD_PORT") <= 0:
                logging.error("Invalid dashboard port")
                return False

            if self.get("DATA_REFRESH_INTERVAL") <= 0:
                logging.error("Invalid data refresh interval")
                return False

            return True

        except Exception as e:
            logging.error(f"Configuration validation error: {e}")
            return False

    def to_streamlit_config(self) -> Dict[str, Any]:
        """Convert to Streamlit configuration format"""
        return {
            "server.port": self.get("DASHBOARD_PORT"),
            "server.address": self.get("DASHBOARD_HOST"),
            "server.headless": True,
            "server.enableCORS": False,
            "server.enableXsrfProtection": True,
            "browser.gatherUsageStats": False,
            "theme.base": "light" if not self.get("ENABLE_DARK_MODE") else "dark",
            "theme.primaryColor": "#1f77b4",
            "theme.backgroundColor": "#ffffff",
            "theme.secondaryBackgroundColor": "#f0f2f6",
            "theme.textColor": "#000000",
        }


# Global configuration instance
config = DashboardConfig()


def get_config() -> DashboardConfig:
    """Get global configuration instance"""
    return config


def get_setting(key: str, default: Any = None) -> Any:
    """Get configuration setting"""
    return config.get(key, default)


def set_setting(key: str, value: Any) -> None:
    """Set configuration setting"""
    config.set(key, value)


def validate_config() -> bool:
    """Validate configuration"""
    return config.validate()


def get_streamlit_config() -> Dict[str, Any]:
    """Get Streamlit configuration"""
    return config.to_streamlit_config()


# Configuration UI for Streamlit
def show_config_ui():
    """Show configuration UI in Streamlit"""
    st.markdown("### ⚙️ הגדרות מערכת")

    # Dashboard Settings
    st.markdown("#### 🎛️ הגדרות דשבורד")
    col1, col2 = st.columns(2)

    with col1:
        port = st.number_input(
            "פורט", value=get_setting("DASHBOARD_PORT"), min_value=1, max_value=65535
        )
        host = st.text_input("כתובת", value=get_setting("DASHBOARD_HOST"))
        refresh_interval = st.number_input(
            "מרווח רענון נתונים (שניות)",
            value=get_setting("DATA_REFRESH_INTERVAL"),
            min_value=30,
            max_value=3600,
        )

    with col2:
        enable_cache = st.checkbox("אפשר מטמון", value=get_setting("ENABLE_CACHING"))
        enable_export = st.checkbox("אפשר ייצוא", value=get_setting("ENABLE_EXPORT"))
        enable_animations = st.checkbox("אפשר אנימציות", value=get_setting("ENABLE_ANIMATIONS"))

    # Security Settings
    st.markdown("#### 🔒 הגדרות אבטחה")
    col1, col2 = st.columns(2)

    with col1:
        enable_auth = st.checkbox("אפשר אימות", value=get_setting("ENABLE_AUTHENTICATION"))
        session_timeout = st.number_input(
            "פסק זמן סשן (שניות)",
            value=get_setting("SESSION_TIMEOUT"),
            min_value=300,
            max_value=86400,
        )

    with col2:
        enable_public = st.checkbox("אפשר גישה ציבורית", value=get_setting("ENABLE_PUBLIC_ACCESS"))
        max_requests = st.number_input(
            "מקסימום בקשות במקביל",
            value=get_setting("MAX_CONCURRENT_REQUESTS"),
            min_value=1,
            max_value=100,
        )

    # Save Configuration
    if st.button("💾 שמור הגדרות", use_container_width=True):
        try:
            # Update configuration
            set_setting("DASHBOARD_PORT", port)
            set_setting("DASHBOARD_HOST", host)
            set_setting("DATA_REFRESH_INTERVAL", refresh_interval)
            set_setting("ENABLE_CACHING", enable_cache)
            set_setting("ENABLE_EXPORT", enable_export)
            set_setting("ENABLE_ANIMATIONS", enable_animations)
            set_setting("ENABLE_AUTHENTICATION", enable_auth)
            set_setting("SESSION_TIMEOUT", session_timeout)
            set_setting("ENABLE_PUBLIC_ACCESS", enable_public)
            set_setting("MAX_CONCURRENT_REQUESTS", max_requests)

            st.success("✅ ההגדרות נשמרו בהצלחה!")

            # Validate configuration
            if validate_config():
                st.info("✅ הגדרות תקינות")
            else:
                st.warning("⚠️ חלק מההגדרות אינן תקינות")

        except Exception as e:
            st.error(f"❌ שגיאה בשמירת הגדרות: {e}")

    # Configuration Status
    st.markdown("#### 📊 סטטוס הגדרות")
    if validate_config():
        st.success("✅ כל ההגדרות תקינות")
    else:
        st.error("❌ יש בעיות בהגדרות")

    # Show current configuration
    if st.expander("👁️ הצג הגדרות נוכחיות"):
        st.json(config.get_all())
