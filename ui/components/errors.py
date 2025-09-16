#!/usr/bin/env python3
"""
Error Handling Components for Dashboard
Consistent error messages and user feedback
"""

import streamlit as st
from ui.design_tokens import DesignSystem

class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

class NetworkError(Exception):
    """Custom exception for network-related errors"""
    pass

class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

def create_error_message(error: Exception, context: str = "", show_details: bool = False):
    """Create user-friendly error messages with consistent styling"""
    
    # Determine error type and styling
    if isinstance(error, DataValidationError):
        error_type = "שגיאת נתונים"
        error_color = DesignSystem.COLORS['error']
        error_icon = "📊"
        suggestions = [
            "בדוק שהנתונים מכילים את העמודות הנדרשות",
            "ודא שהפורמט של הנתונים תקין",
            "נסה לרענן את הדף"
        ]
    elif isinstance(error, NetworkError):
        error_type = "שגיאת רשת"
        error_color = DesignSystem.COLORS['warning']
        error_icon = "🌐"
        suggestions = [
            "בדוק את החיבור לאינטרנט",
            "ודא שהשרת זמין",
            "נסה שוב בעוד כמה דקות"
        ]
    elif isinstance(error, AuthenticationError):
        error_type = "שגיאת אימות"
        error_color = DesignSystem.COLORS['error']
        error_icon = "🔐"
        suggestions = [
            "בדוק את פרטי ההתחברות",
            "ודא שיש לך הרשאות מתאימות",
            "פנה למנהל המערכת"
        ]
    else:
        error_type = "שגיאה כללית"
        error_color = DesignSystem.COLORS['error']
        error_icon = "❌"
        suggestions = [
            "נסה לרענן את הדף",
            "פנה לתמיכה טכנית",
            "בדוק את הלוגים לפרטים נוספים"
        ]
    
    # Create error message HTML
    error_html = f"""
    <div style="
        background: {DesignSystem.COLORS['background']};
        border: 2px solid {error_color};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin: {DesignSystem.SPACING['md']} 0;
        box-shadow: {DesignSystem.SHADOWS['md']};
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: {DesignSystem.SPACING['md']};
        ">
            <span style="
                font-size: 24px;
                margin-left: {DesignSystem.SPACING['sm']};
            ">
                {error_icon}
            </span>
            <h4 style="
                color: {error_color};
                margin: 0;
                font-size: {DesignSystem.TYPOGRAPHY['h4']['size']};
                font-weight: {DesignSystem.TYPOGRAPHY['h4']['weight']};
            ">
                {error_type}
            </h4>
        </div>
        
        <p style="
            color: {DesignSystem.COLORS['text']};
            font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
            margin: 0 0 {DesignSystem.SPACING['md']} 0;
            line-height: {DesignSystem.TYPOGRAPHY['body']['line_height']};
        ">
            {str(error)}
        </p>
        
        {f'''
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            margin: 0 0 {DesignSystem.SPACING['md']} 0;
            font-style: italic;
        ">
            הקשר: {context}
        </p>
        ''' if context else ''}
        
        <div style="
            background: {DesignSystem.COLORS['surface']};
            border-radius: {DesignSystem.BORDER_RADIUS['sm']};
            padding: {DesignSystem.SPACING['md']};
            margin-top: {DesignSystem.SPACING['md']};
        ">
            <h5 style="
                color: {DesignSystem.COLORS['text']};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                font-weight: 600;
                margin: 0 0 {DesignSystem.SPACING['sm']} 0;
            ">
                💡 הצעות לפתרון:
            </h5>
            <ul style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                margin: 0;
                padding-right: {DesignSystem.SPACING['md']};
            ">
                {''.join([f'<li>{suggestion}</li>' for suggestion in suggestions])}
            </ul>
        </div>
        
        {f'''
        <details style="
            margin-top: {DesignSystem.SPACING['md']};
        ">
            <summary style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['caption']['size']};
                cursor: pointer;
            ">
                פרטים טכניים
            </summary>
            <pre style="
                background: {DesignSystem.COLORS['surface_dark']};
                padding: {DesignSystem.SPACING['sm']};
                border-radius: {DesignSystem.BORDER_RADIUS['sm']};
                font-size: {DesignSystem.TYPOGRAPHY['caption']['size']};
                overflow-x: auto;
                margin: {DesignSystem.SPACING['sm']} 0 0 0;
            ">
{type(error).__name__}: {str(error)}
            </pre>
        </details>
        ''' if show_details else ''}
    </div>
    """
    
    st.markdown(error_html, unsafe_allow_html=True)

def create_success_message(message: str, icon: str = "✅", context: str = ""):
    """Create success messages with consistent styling"""
    
    success_html = f"""
    <div style="
        background: {DesignSystem.COLORS['background']};
        border: 2px solid {DesignSystem.COLORS['success']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin: {DesignSystem.SPACING['md']} 0;
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: {DesignSystem.SPACING['sm']};
        ">
            <span style="
                font-size: 20px;
                margin-left: {DesignSystem.SPACING['sm']};
            ">
                {icon}
            </span>
            <p style="
                color: {DesignSystem.COLORS['success']};
                font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
                font-weight: 600;
                margin: 0;
            ">
                {message}
            </p>
        </div>
        
        {f'''
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            margin: 0;
        ">
            {context}
        </p>
        ''' if context else ''}
    </div>
    """
    
    st.markdown(success_html, unsafe_allow_html=True)

def create_warning_message(message: str, icon: str = "⚠️", context: str = ""):
    """Create warning messages with consistent styling"""
    
    warning_html = f"""
    <div style="
        background: {DesignSystem.COLORS['background']};
        border: 2px solid {DesignSystem.COLORS['warning']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin: {DesignSystem.SPACING['md']} 0;
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: {DesignSystem.SPACING['sm']};
        ">
            <span style="
                font-size: 20px;
                margin-left: {DesignSystem.SPACING['sm']};
            ">
                {icon}
            </span>
            <p style="
                color: {DesignSystem.COLORS['warning']};
                font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
                font-weight: 600;
                margin: 0;
            ">
                {message}
            </p>
        </div>
        
        {f'''
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            margin: 0;
        ">
            {context}
        </p>
        ''' if context else ''}
    </div>
    """
    
    st.markdown(warning_html, unsafe_allow_html=True)

def create_info_message(message: str, icon: str = "ℹ️", context: str = ""):
    """Create info messages with consistent styling"""
    
    info_html = f"""
    <div style="
        background: {DesignSystem.COLORS['surface']};
        border: 1px solid {DesignSystem.COLORS['info']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin: {DesignSystem.SPACING['md']} 0;
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: {DesignSystem.SPACING['sm']};
        ">
            <span style="
                font-size: 18px;
                margin-left: {DesignSystem.SPACING['sm']};
            ">
                {icon}
            </span>
            <p style="
                color: {DesignSystem.COLORS['info']};
                font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
                font-weight: 500;
                margin: 0;
            ">
                {message}
            </p>
        </div>
        
        {f'''
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            margin: 0;
        ">
            {context}
        </p>
        ''' if context else ''}
    </div>
    """
    
    st.markdown(info_html, unsafe_allow_html=True)

def handle_error_with_retry(error: Exception, retry_function, max_retries: int = 3):
    """Handle errors with automatic retry functionality"""
    
    if max_retries > 0:
        create_warning_message(
            f"שגיאה זמנית. מנסה שוב... ({max_retries} ניסיונות נותרו)",
            "🔄"
        )
        
        try:
            return retry_function()
        except Exception as retry_error:
            return handle_error_with_retry(retry_error, retry_function, max_retries - 1)
    else:
        create_error_message(error, "כל הניסיונות נכשלו")
        return None
