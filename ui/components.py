"""
UI Components for the Omri Association Dashboard
"""

from datetime import datetime

import streamlit as st


def show_success_message(message):
    """Show a success message that auto-dismisses after 3 seconds"""
    # Store message in session state with timestamp
    st.session_state.success_message = {
        'text': message,
        'timestamp': datetime.now()
    }

def display_success_messages():
    """Display and auto-dismiss success messages"""
    if 'success_message' in st.session_state:
        message_data = st.session_state.success_message
        elapsed = (datetime.now() - message_data['timestamp']).total_seconds()

        if elapsed < 3:
            st.success(f"✅ {message_data['text']}")
        else:
            # Remove message after 3 seconds
            del st.session_state.success_message

def get_custom_css():
    """Return custom CSS for the dashboard"""
    return """
    <style>
    /* RTL Support */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* Typography improvements */
    h1 {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #1f2937 !important;
        margin-bottom: 1.5rem !important;
    }

    h2 {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: #374151 !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
        margin-bottom: 0.75rem !important;
    }

    .stSubheader {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #6b7280 !important;
        margin-bottom: 0.5rem !important;
    }

    /* Sidebar typography */
    .css-1d391kg {
        font-size: 1.1rem !important;
    }

    .css-1d391kg h1 {
        font-size: 1.8rem !important;
    }

    .css-1d391kg h2 {
        font-size: 1.4rem !important;
    }

    .css-1d391kg h3 {
        font-size: 1.2rem !important;
    }

    /* Google Docs style tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f8f9fa;
        border-bottom: 1px solid #e1e5ea;
        padding: 0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: nowrap;
        background-color: transparent;
        border-radius: 0;
        border: none;
        border-bottom: 2px solid transparent;
        color: #5f6368;
        font-weight: 500;
        font-size: 14px;
        padding: 0 24px;
        margin: 0;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f3f4;
        color: #202124;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: white;
        color: #1a73e8;
        border-bottom: 2px solid #1a73e8;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding: 24px 0;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .metric-card h2 {
        color: #1f77b4;
        font-size: 1.8em;
        font-weight: bold;
        margin: 0;
    }

    /* Status indicators */
    .status-excellent {
        color: #059669;
        font-weight: bold;
    }
    .status-good {
        color: #0d9488;
        font-weight: bold;
    }
    .status-adequate {
        color: #d97706;
        font-weight: bold;
    }
    .status-attention {
        color: #dc2626;
        font-weight: bold;
    }
    .status-critical {
        color: #991b1b;
        font-weight: bold;
    }
    .status-emergency {
        color: #7f1d1d;
        font-weight: bold;
    }

    /* Network graph styling */
    .network-container {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        background-color: #f9fafb;
    }

    /* Data table styling */
    .data-table {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 6px;
    }

    .stSelectbox > div > div > div {
        border-radius: 6px;
    }

    /* Alert styling */
    .alert-info {
        background-color: #dbeafe;
        border: 1px solid #93c5fd;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0;
    }

    .alert-warning {
        background-color: #fef3c7;
        border: 1px solid #fbbf24;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0;
    }

    .alert-error {
        background-color: #fee2e2;
        border: 1px solid #f87171;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.25rem !important;
        }
    }
    </style>
    """

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="מערכת ניהול עמותת עמרי",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
