#!/usr/bin/env python3
"""
Dashboard Core Module
Handles core dashboard logic, data loading, and processing
"""

import logging
from typing import Dict, Tuple

import pandas as pd
import streamlit as st

from alerts import (
    check_budget_alerts,
    check_data_quality_alerts,
    check_donations_alerts,
    check_widows_alerts,
)
from data_processing import (
    calculate_donor_statistics,
    calculate_monthly_budget,
    calculate_widow_statistics,
)
from google_sheets_io import check_service_account_validity
from services.sheets import fetch_dashboard_frames
from ui.dashboard_layout import (
    create_dashboard_header,
    create_main_tabs,
    create_recent_activity_section,
    create_reports_section,
)
from ui.dashboard_sections import (
    create_budget_section,
    create_donors_section,
    create_network_section,
    create_overview_section,
    create_residential_breakdown_section,
    create_widows_section,
)


def load_dashboard_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all dashboard data from Google Sheets with enhanced loading states and error handling"""
    try:
        # Check if data is already in session state
        if ('expenses_df' in st.session_state and 'donations_df' in st.session_state and
            'almanot_df' in st.session_state and 'investors_df' in st.session_state):

            # Use cached data
            expenses_df = st.session_state.expenses_df
            donations_df = st.session_state.donations_df
            almanot_df = st.session_state.almanot_df
            investors_df = st.session_state.investors_df

            # Validate cached data
            if (expenses_df is not None and donations_df is not None and
                almanot_df is not None and investors_df is not None):
                return expenses_df, donations_df, almanot_df, investors_df

        frames = fetch_dashboard_frames()
        expenses_df = frames.get('Expenses', pd.DataFrame())
        donations_df = frames.get('Donations', pd.DataFrame())
        investors_df = frames.get('Investors', pd.DataFrame())
        almanot_df = frames.get('Widows', pd.DataFrame())

        # Store in session state
        st.session_state.expenses_df = expenses_df
        st.session_state.donations_df = donations_df
        st.session_state.almanot_df = almanot_df
        st.session_state.investors_df = investors_df

        # Validate data integrity
        if expenses_df.empty and donations_df.empty and almanot_df.empty:
            st.error("❌ לא ניתן לטעון נתונים. אנא בדוק את חיבור Google Sheets")
            return None, None, None, None

        return expenses_df, donations_df, almanot_df, investors_df

    except Exception as e:
        error_msg = f"שגיאה בטעינת נתונים: {str(e)}"
        st.error(f"❌ {error_msg}")
        logging.error(f"Data loading error: {e}")

        # Show helpful troubleshooting tips
        st.info("💡 טיפים לפתרון בעיות:")
        st.info("• בדוק חיבור לאינטרנט")
        st.info("• ודא שקובץ service_account.json קיים ותקין")
        st.info("• בדוק הרשאות Google Sheets")

        return None, None, None, None

def process_dashboard_data(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame) -> Tuple[Dict, Dict, Dict]:
    """Process dashboard data and calculate statistics with enhanced error handling"""
    try:
        # Fix data types with validation (silent processing)
        for _df_name, df in [('expenses_df', expenses_df), ('donations_df', donations_df)]:
            if df is not None and not df.empty:
                if 'שקלים' in df.columns:
                    df['שקלים'] = pd.to_numeric(df['שקלים'], errors='coerce').fillna(0)
                if 'תאריך' in df.columns:
                    df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')

        if almanot_df is not None and not almanot_df.empty:
            if 'מספר ילדים' in almanot_df.columns:
                almanot_df['מספר ילדים'] = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce').fillna(0)
            if 'סכום חודשי' in almanot_df.columns:
                # Clean the data first - remove any non-numeric characters
                almanot_df['סכום חודשי'] = almanot_df['סכום חודשי'].astype(str).str.replace('₪', '').str.replace(',', '').str.replace(' ', '')
                almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce')
                # Only fill NaN with 0, not all values
                almanot_df['סכום חודשי'] = almanot_df['סכום חודשי'].fillna(0)

        # Calculate statistics (silent processing)
        budget_status = calculate_monthly_budget(expenses_df, donations_df)
        donor_stats = calculate_donor_statistics(donations_df)
        
        
        widow_stats = calculate_widow_statistics(almanot_df)

        return budget_status, donor_stats, widow_stats

    except Exception as e:
        error_msg = f"שגיאה בעיבוד נתונים: {str(e)}"
        st.error(f"❌ {error_msg}")
        logging.error(f"Data processing error: {e}")

        # Show helpful troubleshooting tips
        st.info("💡 טיפים לפתרון בעיות:")
        st.info("• בדוק שהנתונים לא ריקים")
        st.info("• ודא שעמודות הנתונים קיימות")
        st.info("• בדוק פורמט התאריכים")

        # Return default values to prevent crashes
        return {
            'monthly_donations': {},
            'monthly_expenses': {},
            'total_budget': 0,
            'total_expenses': 0
        }, {
            'total_donors': 0,
            'total_donations': 0,
            'avg_donation': 0,
            'max_donation': 0
        }, {
            'total_widows': 0,
            'total_support': 0
        }

def create_alerts_section(budget_status: Dict, expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame, donor_stats: Dict, widow_stats: Dict):
    """Create the alerts section"""
    try:
        all_alerts = []

        if budget_status and isinstance(budget_status, dict) and len(budget_status) > 0:
            budget_alerts = check_budget_alerts(budget_status, donations_df)
            if budget_alerts:
                all_alerts.extend(budget_alerts)

        data_alerts = check_data_quality_alerts(expenses_df, donations_df, almanot_df)
        if data_alerts:
            all_alerts.extend(data_alerts)

        widows_alerts = check_widows_alerts(widow_stats)
        if widows_alerts:
            all_alerts.extend(widows_alerts)

        donations_alerts = check_donations_alerts(donor_stats)
        if donations_alerts:
            all_alerts.extend(donations_alerts)

    except Exception as e:
        logging.error(f"Error checking alerts: {e}")
        st.warning("⚠️ לא ניתן לבדוק התראות")
        all_alerts = []

    if all_alerts:
        for alert in all_alerts:
            # Categorize alerts based on content
            if "✅" in alert or "מצוין" in alert or "טובה" in alert or "גבוהה" in alert:
                st.success(alert)
            elif "שגיאה" in alert or "קריטי" in alert or "שלילית" in alert:
                st.error(alert)
            elif "נמוך" in alert or "חסר" in alert or "אין" in alert:
                st.warning(alert)
            else:
                st.info(alert)
    else:
        st.success("✅ אין התראות פעילות")

def render_home_tab(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame,
                   budget_status: Dict, donor_stats: Dict, widow_stats: Dict):
    """Render the home tab content - clean and focused"""

    # 1. OVERVIEW & KEY METRICS (Executive summary - most important numbers)
    create_overview_section(expenses_df, donations_df, donor_stats, widow_stats)

    # 2. RECENT ACTIVITY (Operational insights - what's happening now)
    create_recent_activity_section(expenses_df, donations_df)

    # 3. BUDGET CHARTS (Visual financial overview)
    create_budget_section(expenses_df, donations_df, budget_status, "home")

    # 4. WIDOWS TABLE (Complete list of all widows)
    create_widows_table_section(almanot_df)

    # 5. REPORTS & EXPORTS (Data access - for analysis and record keeping)
    create_reports_section(expenses_df, donations_df, almanot_df)

def render_network_tab(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Render the network tab content"""
    create_network_section(expenses_df, donations_df, almanot_df, investors_df)

# Removed unused tab render functions for cleaner code

def run_dashboard():
    """Main dashboard execution function with authentication"""
    try:
        logging.info("=== STARTING DASHBOARD ===")

        # Check authentication if enabled
        try:
            from auth import check_auth_and_redirect, is_authenticated, show_user_info
            if not check_auth_and_redirect():
                return  # User not authenticated, login form shown
        except ImportError:
            # Authentication module not available, continue without auth
            pass

        # Apply current theme
        try:
            from theme_manager import apply_current_theme
            apply_current_theme()
        except ImportError:
            pass  # Theme manager not available

        # Create dashboard header
        create_dashboard_header()

        # Show user info in sidebar if authentication is enabled
        try:
            if is_authenticated():
                show_user_info()
        except Exception:
            pass

        # Check service account validity
        if not check_service_account_validity():
            st.error("Service account validation failed")
            st.stop()

        # Load data
        expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()
        if expenses_df is None or donations_df is None or almanot_df is None or investors_df is None:
            st.error("לא ניתן לטעון נתונים. אנא בדוק את חיבור Google Sheets")
            return

        # Process data
        budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, almanot_df)

        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = create_main_tabs()

        # Render Home Tab
        with tab1:
            render_home_tab(expenses_df, donations_df, almanot_df, budget_status, donor_stats, widow_stats)

        # Render Budget Tab
        with tab2:
            create_budget_section(expenses_df, donations_df, budget_status, "budget")

        # Render Donors Tab
        with tab3:
            create_donors_section(donations_df, donor_stats)

        # Render Widows Tab
        with tab4:
            create_widows_section(almanot_df, widow_stats)

        # Render Network Tab
        with tab5:
            create_network_section(expenses_df, donations_df, almanot_df, investors_df)

        # Render Residential Breakdown Tab
        with tab6:
            create_residential_breakdown_section(almanot_df, donations_df)

        logging.info("=== DASHBOARD RENDERING COMPLETED ===")

    except Exception as e:
        error_msg = f"שגיאה כללית בדשבורד: {str(e)}"
        st.error(error_msg)
        logging.error(f"General dashboard error: {e}")
        logging.error(f"Error type: {type(e).__name__}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        st.info("אנא רענן את הדף או פנה לתמיכה")
