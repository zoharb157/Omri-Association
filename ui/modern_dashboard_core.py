#!/usr/bin/env python3
"""
Modern Dashboard Core Module
Handles core dashboard logic with modern UI components
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any, Tuple
from google_sheets_io import load_all_data, check_service_account_validity
from data_processing import calculate_monthly_budget, calculate_donor_statistics, calculate_widow_statistics
from alerts import check_budget_alerts, check_data_quality_alerts, check_widows_alerts, check_donations_alerts
from ui.dashboard_sections import create_budget_section, create_donors_section, create_widows_section, create_widows_table_section, create_network_section, create_residential_breakdown_section
from ui.components.headers import create_page_title
from ui.components.modern_dashboard import create_modern_overview_section, create_modern_charts_section, create_modern_recent_activity_section, create_modern_alerts_section
from ui.components.responsive_design import create_responsive_container, create_mobile_navigation, create_touch_friendly_buttons, create_responsive_typography, create_responsive_spacing
from ui.components.micro_interactions import create_loading_animations, create_hover_effects, create_focus_states, create_transition_animations, create_interactive_feedback

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
        
        # Load fresh data using our improved load_all_data function
        all_data = load_all_data()
        
        if all_data and len(all_data) > 0:
            expenses_df = all_data.get('Expenses', pd.DataFrame())
            donations_df = all_data.get('Donations', pd.DataFrame())
            investors_df = all_data.get('Investors', pd.DataFrame())
            almanot_df = all_data.get('Widows', all_data.get('Almanot', pd.DataFrame()))
        else:
            # Fallback to empty DataFrames
            expenses_df = pd.DataFrame()
            donations_df = pd.DataFrame()
            investors_df = pd.DataFrame()
            almanot_df = pd.DataFrame()
        
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
        for df_name, df in [('expenses_df', expenses_df), ('donations_df', donations_df)]:
            if df is not None and not df.empty:
                amount_col = 'שקלים' if 'שקלים' in df.columns else 'סכום' if 'סכום' in df.columns else None
                if amount_col:
                    df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
                if len(df.columns) > 0:
                    date_col = df.columns[0]
                    df['תאריך'] = pd.to_datetime(df[date_col], errors='coerce')
        
        if almanot_df is not None and not almanot_df.empty:
            if 'מספר ילדים' in almanot_df.columns:
                almanot_df['מספר ילדים'] = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce').fillna(0)
            if 'סכום חודשי' in almanot_df.columns:
                almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
                # Fill missing values with 0 (intended behavior)
        
        # Calculate statistics (silent processing) - only if DataFrames have data
        if expenses_df is not None and donations_df is not None and not expenses_df.empty and not donations_df.empty:
            budget_status = calculate_monthly_budget(expenses_df, donations_df)
        else:
            budget_status = {
                'total_donations': 0,
                'total_expenses': 0,
                'balance': 0,
                'utilization_percentage': 0,
                'monthly_donations': {},
                'monthly_expenses': {},
                'donation_trend': 'stable',
                'expense_trend': 'stable'
            }
        
        if donations_df is not None and not donations_df.empty:
            donor_stats = calculate_donor_statistics(donations_df)
        else:
            donor_stats = {
                'total_donors': 0,
                'total_donations': 0,
                'avg_donation': 0,
                'min_donation': 0,
                'max_donation': 0,
                'top_donors': []
            }
        
        if almanot_df is not None and not almanot_df.empty:
            widow_stats = calculate_widow_statistics(almanot_df)
        else:
            widow_stats = {
                'total_widows': 0,
                'total_support': 0,
                'support_1000_count': 0,
                'support_2000_count': 0,
                'support_distribution': {},
                'monthly_support': []
            }
        
        return budget_status, donor_stats, widow_stats
        
    except Exception as e:
        logging.error(f"Error processing dashboard data: {e}")
        st.warning("⚠️ שגיאה בעיבוד נתונים")
        
        # Return empty stats
        return {
            'total_donations': 0,
            'total_expenses': 0,
            'balance': 0,
            'utilization_percentage': 0,
            'monthly_donations': {},
            'monthly_expenses': {},
            'donation_trend': 'stable',
            'expense_trend': 'stable'
        }, {
            'total_donors': 0,
            'total_donations': 0,
            'avg_donation': 0,
            'min_donation': 0,
            'max_donation': 0,
            'top_donors': []
        }, {
            'total_widows': 0,
            'total_support': 0,
            'support_1000_count': 0,
            'support_2000_count': 0,
            'support_distribution': {},
            'monthly_support': []
        }

def run_modern_dashboard():
    """Main modern dashboard function that orchestrates all modern components"""
    try:
        logging.info("=== STARTING MODERN DASHBOARD ===")
        
        # Initialize modern components
        create_responsive_container()
        create_mobile_navigation()
        create_touch_friendly_buttons()
        create_responsive_typography()
        create_responsive_spacing()
        create_loading_animations()
        create_hover_effects()
        create_focus_states()
        create_transition_animations()
        create_interactive_feedback()
        
        # Create page title
        create_page_title("מערכת ניהול עמותת עמרי", "סקירה מקיפה של מצב העמותה")
        
        # Check service account validity
        if not check_service_account_validity():
            st.error("Service account validation failed")
            st.stop()
        
        # Load data
        expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()
        
        if expenses_df is None or donations_df is None or almanot_df is None:
            st.error("❌ לא ניתן לטעון נתונים. אנא נסה שוב מאוחר יותר.")
            return
        
        # Check for empty dataframes
        empty_dataframes = []
        if expenses_df is not None and expenses_df.empty:
            empty_dataframes.append("הוצאות")
        if donations_df is not None and donations_df.empty:
            empty_dataframes.append("תרומות")
        if almanot_df is not None and almanot_df.empty:
            empty_dataframes.append("אלמנות")
        
        if empty_dataframes:
            st.warning(f"⚠️ הנתונים הבאים ריקים: {', '.join(empty_dataframes)}. יוצגו רק הנתונים הזמינים.")
        
        # Process data - only if we have non-empty DataFrames
        if expenses_df is not None and donations_df is not None and not expenses_df.empty and not donations_df.empty:
            try:
                budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, almanot_df)
            except Exception as e:
                logging.error(f"Error in process_dashboard_data: {e}")
                st.error(f"❌ שגיאה בעיבוד נתונים: {str(e)}")
                # Create empty stats as fallback
                budget_status = {
                    'total_donations': 0,
                    'total_expenses': 0,
                    'balance': 0,
                    'utilization_percentage': 0,
                    'monthly_donations': {},
                    'monthly_expenses': {},
                    'donation_trend': 'stable',
                    'expense_trend': 'stable'
                }
                donor_stats = {
                    'total_donors': 0,
                    'total_donations': 0,
                    'avg_donation': 0,
                    'min_donation': 0,
                    'max_donation': 0,
                    'top_donors': []
                }
                widow_stats = {
                    'total_widows': 0,
                    'total_support': 0,
                    'support_1000_count': 0,
                    'support_2000_count': 0,
                    'support_distribution': {},
                    'monthly_support': []
                }
        else:
            # Create empty stats for empty DataFrames
            budget_status = {
                'total_donations': 0,
                'total_expenses': 0,
                'balance': 0,
                'utilization_percentage': 0,
                'monthly_donations': {},
                'monthly_expenses': {},
                'donation_trend': 'stable',
                'expense_trend': 'stable'
            }
            donor_stats = {
                'total_donors': 0,
                'total_donations': 0,
                'avg_donation': 0,
                'min_donation': 0,
                'max_donation': 0,
                'top_donors': []
            }
            widow_stats = {
                'total_widows': 0,
                'total_support': 0,
                'support_1000_count': 0,
                'support_2000_count': 0,
                'support_distribution': {},
                'monthly_support': []
            }
        
        # Create main tabs using Streamlit's native tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 דף הבית", 
            "💰 תקציב", 
            "👥 תורמים", 
            "👩 אלמנות", 
            "🕸️ מפת קשרים", 
            "🏘️ אזורי מגורים"
        ])
        
        with tab1:
            # Modern overview section
            create_modern_overview_section(budget_status, donor_stats, widow_stats)
            
            # Modern charts section - only if we have data
            if (expenses_df is not None and not expenses_df.empty) or (donations_df is not None and not donations_df.empty):
                create_modern_charts_section(expenses_df, donations_df, donations_df, almanot_df)
            else:
                st.info("ℹ️ אין נתונים להצגת תרשימים")
            
            # Modern recent activity section - only if we have data
            if (expenses_df is not None and not expenses_df.empty) or (donations_df is not None and not donations_df.empty):
                create_modern_recent_activity_section(expenses_df, donations_df)
            else:
                st.info("ℹ️ אין נתונים להצגת פעילות אחרונה")
            
            # Modern alerts section
            create_modern_alerts_section(budget_status, donor_stats, widow_stats)
        
        with tab2:
            create_budget_section(expenses_df, donations_df, budget_status)

        with tab3:
            create_donors_section(donations_df, donor_stats)

        with tab4:
            create_widows_section(almanot_df, widow_stats)
            create_widows_table_section(almanot_df)

        with tab5:
            create_network_section(expenses_df, donations_df, almanot_df, investors_df)

        with tab6:
            create_residential_breakdown_section(almanot_df, donations_df)
        
        
    except Exception as e:
        import traceback
        st.error(f"❌ שגיאה כללית: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        logging.error(f"Modern dashboard error: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
