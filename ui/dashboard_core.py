#!/usr/bin/env python3
"""
Dashboard Core Module
Handles core dashboard logic, data loading, and processing
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any, Tuple
from google_sheets_io import read_sheet, check_service_account_validity
from data_processing import calculate_monthly_budget, calculate_donor_statistics, calculate_widow_statistics
from alerts import check_budget_alerts, check_data_quality_alerts, check_widows_alerts, check_donations_alerts
from ui.dashboard_layout import create_dashboard_header, create_main_tabs, create_recent_activity_section, create_reports_section, add_spacing
from ui.dashboard_sections import create_overview_section, create_budget_section, create_donors_section, create_widows_section, create_network_section

def load_dashboard_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all dashboard data from Google Sheets"""
    try:
        # Load data from Google Sheets
        if 'expenses_df' not in st.session_state or 'donations_df' not in st.session_state or 'almanot_df' not in st.session_state or 'investors_df' not in st.session_state:
            expenses_df = read_sheet("Expenses")
            donations_df = read_sheet("Donations")
            investors_df = read_sheet("Investors")
            almanot_df = read_sheet("Widows")
            
            st.session_state.expenses_df = expenses_df
            st.session_state.donations_df = donations_df
            st.session_state.almanot_df = almanot_df
            st.session_state.investors_df = investors_df
        else:
            expenses_df = st.session_state.expenses_df
            donations_df = st.session_state.donations_df
            almanot_df = st.session_state.almanot_df
            investors_df = st.session_state.investors_df
        
        # Check if data was loaded successfully
        if expenses_df is None or donations_df is None or almanot_df is None or investors_df is None:
            st.error("לא ניתן להמשיך ללא נתונים תקינים")
            return None, None, None, None
            
        return expenses_df, donations_df, almanot_df, investors_df
        
    except Exception as e:
        st.error(f"שגיאה בטעינת נתונים: {e}")
        logging.error(f"Data loading error: {e}")
        return None, None, None, None

def process_dashboard_data(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame) -> Tuple[Dict, Dict, Dict]:
    """Process dashboard data and calculate statistics"""
    try:
        # Fix data types
        for df_name, df in [('expenses_df', expenses_df), ('donations_df', donations_df)]:
            if 'שקלים' in df.columns:
                df['שקלים'] = pd.to_numeric(df['שקלים'], errors='coerce').fillna(0)
            if 'תאריך' in df.columns:
                df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')
        
        if 'מספר ילדים' in almanot_df.columns:
            almanot_df['מספר ילדים'] = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce').fillna(0)
        if 'סכום חודשי' in almanot_df.columns:
            almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
        
        # Calculate statistics
        budget_status = calculate_monthly_budget(expenses_df, donations_df)
        donor_stats = calculate_donor_statistics(donations_df)
        widow_stats = calculate_widow_statistics(almanot_df)
        
        return budget_status, donor_stats, widow_stats
        
    except Exception as e:
        logging.error(f"Data processing error: {e}")
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
    """Render the home tab content"""
    # Overview Section
    create_overview_section(expenses_df, donations_df, donor_stats, widow_stats)
    
    # Recent Activity Section
    create_recent_activity_section(expenses_df, donations_df)
    
    # Alerts Section
    create_alerts_section(budget_status, expenses_df, donations_df, almanot_df, donor_stats, widow_stats)
    
    # Budget Section
    create_budget_section(expenses_df, donations_df, budget_status)
    
    # Donors Section
    create_donors_section(donations_df, donor_stats)
    
    # Widows Section
    create_widows_section(almanot_df, widow_stats)
    
    # Reports Section
    create_reports_section(expenses_df, donations_df, almanot_df)

def render_network_tab(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Render the network tab content"""
    create_network_section(expenses_df, donations_df, almanot_df, investors_df)

def run_dashboard():
    """Main dashboard execution function"""
    try:
        logging.info("=== STARTING DASHBOARD ===")
        
        # Create dashboard header
        create_dashboard_header()
        
        # Check service account validity
        if not check_service_account_validity():
            st.error("Service account validation failed")
            st.stop()
        
        # Load data
        expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()
        if expenses_df is None:
            return
        
        # Process data
        budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, almanot_df)
        
        # Create tabs
        tab1, tab2 = create_main_tabs()
        
        # Render Home Tab
        with tab1:
            render_home_tab(expenses_df, donations_df, almanot_df, budget_status, donor_stats, widow_stats)
        
        # Render Network Tab
        with tab2:
            render_network_tab(expenses_df, donations_df, almanot_df, investors_df)
        
        logging.info("=== DASHBOARD RENDERING COMPLETED ===")
        
    except Exception as e:
        st.error(f"שגיאה כללית בדשבורד: {e}")
        logging.error(f"General dashboard error: {e}")
        st.stop()
