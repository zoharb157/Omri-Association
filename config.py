#!/usr/bin/env python3
"""
Configuration management for Omri Association Dashboard
Handles environment variables and configuration settings
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for the dashboard"""
    
    # Authentication settings
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    USER_PASSWORD = os.getenv('USER_PASSWORD', 'user123')
    VIEWER_PASSWORD = os.getenv('VIEWER_PASSWORD', 'view123')
    
    # Session settings
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
    ENABLE_AUTHENTICATION = os.getenv('ENABLE_AUTHENTICATION', 'false').lower() == 'true'
    
    # Cache settings
    DATA_CACHE_TTL = int(os.getenv('DATA_CACHE_TTL', '300'))  # 5 minutes
    STATS_CACHE_TTL = int(os.getenv('STATS_CACHE_TTL', '600'))  # 10 minutes
    
    # Google Sheets settings
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo')
    WIDOW_SPREADSHEET_ID = os.getenv('WIDOW_SPREADSHEET_ID', '1FQRFhChBVUI8G7GrJW8BZInxJ2F25UhMT-fj-O6odv8')
    
    # UI settings
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB
    SUPPORTED_FORMATS = ['.xlsx', '.csv', '.json']
    
    # Performance settings
    MAX_ROWS_DISPLAY = int(os.getenv('MAX_ROWS_DISPLAY', '1000'))
    CHART_UPDATE_INTERVAL = int(os.getenv('CHART_UPDATE_INTERVAL', '30'))  # seconds
    
    # Error codes
    class ErrorCodes:
        GOOGLE_SHEETS_ERROR = "GS001"
        AUTHENTICATION_ERROR = "AUTH001"
        DATA_VALIDATION_ERROR = "DATA001"
        FILE_UPLOAD_ERROR = "FILE001"
        PERMISSION_ERROR = "PERM001"
    
    # UI Constants
    class UI:
        # Text area height for service account upload
        SERVICE_ACCOUNT_TEXTAREA_HEIGHT = 300
        
        # Chart update intervals
        CHART_UPDATE_INTERVAL = int(os.getenv('CHART_UPDATE_INTERVAL', '30'))  # seconds
        
        # Default values for network filters
        DEFAULT_SHOW_CONNECTED = True
        DEFAULT_SHOW_UNCONNECTED_DONORS = True
        DEFAULT_SHOW_UNCONNECTED_WIDOWS = True
        DEFAULT_MIN_SUPPORT_AMOUNT = 0
        DEFAULT_SHOW_LABELS = True
        
        # Hebrew text constants
        CURRENCY_SYMBOL = "₪"
        NO_DATA_MESSAGE = "אין נתונים זמינים"
        LOADING_MESSAGE = "טוען נתונים..."
        
        # Alert messages
        ALERT_SUCCESS = "✅"
        ALERT_ERROR = "❌"
        ALERT_WARNING = "⚠️"
        ALERT_INFO = "ℹ️"
    
    @classmethod
    def get_auth_users(cls) -> Dict[str, Dict[str, Any]]:
        """Get authentication users configuration"""
        return {
            "admin": {
                "password": cls.ADMIN_PASSWORD,
                "role": "admin",
                "name": "מנהל מערכת",
                "permissions": ["read", "write", "admin", "export", "settings"],
            },
            "user": {
                "password": cls.USER_PASSWORD,
                "role": "user",
                "name": "משתמש רגיל",
                "permissions": ["read", "export"],
            },
            "viewer": {
                "password": cls.VIEWER_PASSWORD,
                "role": "viewer",
                "name": "צופה בלבד",
                "permissions": ["read"],
            },
        }
    
    @classmethod
    def get_google_sheets_config(cls) -> Dict[str, str]:
        """Get Google Sheets configuration"""
        return {
            "service_account_file": cls.SERVICE_ACCOUNT_FILE,
            "spreadsheet_id": cls.SPREADSHEET_ID,
            "widow_spreadsheet_id": cls.WIDOW_SPREADSHEET_ID,
        }
    
    @classmethod
    def get_cache_config(cls) -> Dict[str, int]:
        """Get cache configuration"""
        return {
            "data_cache_ttl": cls.DATA_CACHE_TTL,
            "stats_cache_ttl": cls.STATS_CACHE_TTL,
        }
