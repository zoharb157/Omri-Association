#!/usr/bin/env python3
"""
Streamlit App Entry Point for Omri Association Dashboard
This is the main entry point for Streamlit Cloud deployment
"""

import logging

import streamlit as st

# Import will be done inside main() function to avoid circular imports

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
        "Get Help": "https://github.com/shalevatias/Omri-Association",
        "Report a bug": "https://github.com/shalevatias/Omri-Association/issues",
        "About": "מערכת ניהול עמותת עמרי - דשבורד ניהול תורמים ואלמנות",
    },
)

# Apply global design system
try:
    from ui.design_tokens import get_global_css

    st.markdown(get_global_css(), unsafe_allow_html=True)
except ImportError:
    # Fallback CSS if design_tokens is not available
    st.markdown(
        """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

# Version indicator for deployment verification
st.markdown("<!-- Dashboard Version: 2025-01-17-v3 - FORCE DEPLOY -->", unsafe_allow_html=True)

# Force deployment refresh - this should trigger the modern UI
if st.session_state.get("force_refresh", False):
    st.rerun()


def main():
    """Main entry point for the dashboard - Updated 2025-01-17"""
    try:
        logger.info("Starting Omri Association Dashboard on Streamlit Cloud")
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
