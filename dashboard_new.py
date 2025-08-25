#!/usr/bin/env python3
"""
Omri Association Management Dashboard
A modular dashboard for managing the association's finances, donors, and widows.
"""

import streamlit as st
import logging
from ui.dashboard_core import run_dashboard

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="מערכת ניהול עמותת עמרי",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light mode and disable dark mode
st.markdown("""
    <script>
        // Force light mode
        document.documentElement.setAttribute('data-theme', 'light');
        // Remove any dark mode classes
        document.body.classList.remove('dark');
        document.documentElement.classList.remove('dark');
    </script>
""", unsafe_allow_html=True)

# Add custom CSS for RTL support and styling
st.markdown("""
    <style>
    /* RTL Support */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* Force light mode and ensure text visibility */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Ensure all text is visible */
    * {
        color: #000000 !important;
    }
    
    /* Typography improvements with guaranteed visibility */
    h1 {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #000000 !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: #000000 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #000000 !important;
        margin-bottom: 0.75rem !important;
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
        color: #000000 !important;
        font-weight: 500;
        font-size: 14px;
        padding: 0 24px;
        margin: 0;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f3f4;
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-bottom: 2px solid #1a73e8 !important;
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
    
    /* Tables */
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Charts */
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 10px;
        margin: 10px 0;
        font-size: 1rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 1rem !important;
    }
    
    .stButton button:hover {
        background-color: #1668a1;
    }
    
    /* Ensure all Streamlit text is visible */
    .stText, .stMarkdown, .stMetric, .stDataFrame, .stPlotlyChart {
        color: #000000 !important;
    }
    
    /* Force light background for all components */
    .stMetric, .stDataFrame, .stPlotlyChart {
        background-color: #ffffff !important;
    }
    
    /* Ensure sidebar text is visible */
    .css-1d391kg {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Override any dark mode styles */
    [data-theme="dark"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-theme="dark"] * {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    run_dashboard()

if __name__ == "__main__":
    main()
