#!/usr/bin/env python3
"""
Omri Association Dashboard - MAIN ENTRY POINT
Uses the modular structure we built together
Updated: 2025-01-17
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
    initial_sidebar_state="expanded",
)


# Apply global design system
st.markdown(get_global_css(), unsafe_allow_html=True)

# Version indicator for deployment verification
st.markdown("<!-- Dashboard Version: 2025-01-17-v3 - FORCE DEPLOY -->", unsafe_allow_html=True)

# Force deployment refresh - this should trigger the modern UI
if st.session_state.get("force_refresh", False):
    st.rerun()


def main():
    """Main entry point for the dashboard - Updated 2025-01-17"""
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
