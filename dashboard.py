#!/usr/bin/env python3
"""
Omri Association Dashboard - MAIN ENTRY POINT
Uses the modular structure we built together
"""

import logging

import streamlit as st

from ui.design_tokens import get_global_css

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


# Apply global design system
st.markdown(get_global_css(), unsafe_allow_html=True)

def main():
    """Main entry point for the dashboard"""
    try:
        # Import and run the working dashboard with all tabs
        from ui.dashboard_core import run_dashboard
        run_dashboard()
    except ImportError as e:
        st.error(f"❌ שגיאה בטעינת מודולים: {str(e)}")
        st.info("אנא ודא שכל הקבצים הנדרשים קיימים")
        logger.error(f"Import error: {e}")
    except Exception as e:
        st.error(f"❌ שגיאה כללית: {str(e)}")
        logger.error(f"General error: {e}")

if __name__ == "__main__":
    main()
