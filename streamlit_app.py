#!/usr/bin/env python3
"""
Streamlit App Entry Point for Omri Association Dashboard
This is the main entry point for Streamlit Cloud deployment
"""

import logging

import streamlit as st

# Import the main dashboard function
from ui.dashboard_core import run_dashboard

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config for Streamlit Cloud
st.set_page_config(
    page_title="מערכת ניהול עמותת עמרי",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/shalevatias/Omri-Association',
        'Report a bug': 'https://github.com/shalevatias/Omri-Association/issues',
        'About': "מערכת ניהול עמותת עמרי - דשבורד ניהול תורמים ואלמנות"
    }
)

# Apply global CSS
try:
    from ui.design_tokens import get_global_css
    st.markdown(get_global_css(), unsafe_allow_html=True)
except ImportError:
    # Fallback CSS if design_tokens is not available
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main function to run the dashboard"""
    try:
        logger.info("Starting Omri Association Dashboard on Streamlit Cloud")
        run_dashboard()
    except Exception as e:
        logger.error(f"Error running dashboard: {e}")
        st.error(f"שגיאה בהפעלת הדשבורד: {str(e)}")
        st.info("אנא רענן את הדף או פנה לתמיכה")

if __name__ == "__main__":
    main()
