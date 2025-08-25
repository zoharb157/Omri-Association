import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
import math
import logging
import traceback
from data_visualization import (
    create_monthly_trends,
    create_budget_distribution_chart,
    create_widows_support_chart,
    create_donor_contribution_chart,
    create_comparison_chart,
    create_monthly_budget_chart,
    create_forecast_chart
)
from data_processing import (
    calculate_monthly_averages,
    calculate_total_support,
    calculate_monthly_budget,
    calculate_donor_statistics,
    calculate_expense_statistics,
    calculate_widow_statistics,
    calculate_monthly_trends,
    calculate_budget_forecast,
    calculate_36_month_budget
)
from reports import (
    generate_monthly_report,
    generate_widows_report,
    generate_donor_report,
    generate_budget_report
)
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import tempfile
import json
import re
from google_sheets_io import read_sheet, write_sheet, check_service_account_validity
from alerts import check_budget_alerts, check_data_quality_alerts, check_widows_alerts, check_donations_alerts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log', mode='w', encoding='utf-8')
    ]
)

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

def show_success_message(message):
    """Show a success message that auto-dismisses after 3 seconds"""
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
            del st.session_state.success_message

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

def save_widows_data(almanot_df):
    """Save widows data to Google Sheets"""
    try:
        write_sheet("Widows", almanot_df)
        st.success("נתוני אלמנות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני אלמנות: {str(e)}")

def main():
    try:
        logging.info("=== STARTING DASHBOARD ===")
        st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>מערכת ניהול עמותת עמרי</h1>", unsafe_allow_html=True)
        
        # Check service account validity
        if not check_service_account_validity():
            st.error("Service account validation failed")
            st.stop()
        
        # Display success messages
        display_success_messages()
        
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
            return
        
        # Fix data types
        try:
            for df_name, df in [('expenses_df', expenses_df), ('donations_df', donations_df), ('investors_df', investors_df)]:
                if 'שקלים' in df.columns:
                    df['שקלים'] = pd.to_numeric(df['שקלים'], errors='coerce').fillna(0)
                if 'תאריך' in df.columns:
                    df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')
            
            if 'מספר ילדים' in almanot_df.columns:
                almanot_df['מספר ילדים'] = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce').fillna(0)
            if 'סכום חודשי' in almanot_df.columns:
                almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
        except Exception as e:
            logging.error(f"Error fixing data types: {e}")
        
        # Show success message
        show_success_message("הנתונים נטענו בהצלחה!")
        
        # Calculate statistics
        try:
            budget_status = calculate_monthly_budget(expenses_df, donations_df)
        except Exception as e:
            logging.error(f"Error calculating budget status: {e}")
            budget_status = {}
        
        try:
            donor_stats = calculate_donor_statistics(donations_df)
        except Exception as e:
            logging.error(f"Error calculating donor stats: {e}")
            donor_stats = {'total_donors': 0, 'total_donations': 0, 'avg_donation': 0, 'max_donation': 0}
        
        try:
            widow_stats = calculate_widow_statistics(almanot_df)
        except Exception as e:
            logging.error(f"Error calculating widow stats: {e}")
            widow_stats = {'total_widows': 0, 'total_support': 0}
        
        # Calculate budget summary
        total_don = pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() if 'שקלים' in donations_df.columns else 0
        sum_exp = pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum() if 'שקלים' in expenses_df.columns else 0
        available = total_don - sum_exp
        
        # Create tabs
        tab1, tab2 = st.tabs(["🏠 דף הבית", "🕸️ מפת קשרים"])
        
        with tab1:
            # Dashboard Overview
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>📊 סקירה כללית</h2>", unsafe_allow_html=True)
            
            # General Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("סך תרומות", f"₪{total_don:,.0f}", help="סך כל התרומות שהתקבלו עד כה")
            with col2:
                st.metric("סך הוצאות", f"₪{sum_exp:,.0f}", help="סך כל ההוצאות שהוצאו עד כה")
            with col3:
                st.metric("יתרה זמינה", f"₪{available:,.0f}", help="יתרה זמינה לפעילות עתידית")
            with col4:
                coverage = (total_don / sum_exp * 100) if sum_exp > 0 else 0
                st.metric("יחס כיסוי", f"{coverage:.1f}%", help="אחוז הכיסוי של הוצאות על ידי תרומות")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Key Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}", help="סך כל התורמים שתרמו לעמותה")
            with col2:
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}", help="סך כל האלמנות המטופלות על ידי העמותה")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Recent Activity
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4>🎁 תרומות אחרונות</h4>", unsafe_allow_html=True)
                try:
                    recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                    if len(recent_donations) > 0:
                        for _, donation in recent_donations.iterrows():
                            donation_date = donation['תאריך']
                            if pd.notna(donation_date):
                                st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} ({donation_date.strftime('%d/%m/%Y')})")
                            else:
                                st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} (תאריך לא מוגדר)")
                    else:
                        st.info("אין תרומות להצגה")
                except Exception as e:
                    st.error("שגיאה בטעינת תרומות אחרונות")
            
            with col2:
                st.markdown("<h4>💸 הוצאות אחרונות</h4>", unsafe_allow_html=True)
                try:
                    recent_expenses = expenses_df.sort_values('תאריך', ascending=False).head(5)
                    if len(recent_expenses) > 0:
                        for _, expense in recent_expenses.iterrows():
                            expense_date = expense['תאריך']
                            if pd.notna(expense_date):
                                st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} ({expense_date.strftime('%d/%m/%Y')})")
                            else:
                                st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} (תאריך לא מוגדר)")
                    else:
                        st.info("אין הוצאות להצגה")
                except Exception as e:
                    st.error("שגיאה בטעינת הוצאות אחרונות")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Alerts
            all_alerts = []
            try:
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
            
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # Budget Management Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>💰 ניהול תקציב</h2>", unsafe_allow_html=True)
            
            # Check if budget_status is valid
            if budget_status and isinstance(budget_status, dict) and len(budget_status) > 0:
                try:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        # Calculate total monthly budget from donations
                        monthly_donations = budget_status.get('monthly_donations', {})
                        total_monthly_budget = sum(monthly_donations.values()) if monthly_donations else 0
                        st.metric("תקציב חודשי", f"₪{total_monthly_budget:,.0f}")
                    with col2:
                        # Calculate total monthly expenses
                        monthly_expenses = budget_status.get('monthly_expenses', {})
                        total_monthly_expenses = sum(monthly_expenses.values()) if monthly_expenses else 0
                        st.metric("הוצאות חודשיות", f"₪{total_monthly_expenses:,.0f}")
                    with col3:
                        available_budget = total_monthly_budget - total_monthly_expenses
                        st.metric("יתרה זמינה", f"₪{available_budget:,.0f}")
                except Exception as e:
                    st.error("שגיאה בטעינת סטטוס תקציב")
                    logging.error(f"Budget status error: {e}")
            else:
                # Fallback when budget_status is empty or invalid
                st.warning("⚠️ לא ניתן לטעון נתוני תקציב חודשי")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("תקציב חודשי", "₪0")
                with col2:
                    st.metric("הוצאות חודשיות", "₪0")
                with col3:
                    st.metric("יתרה זמינה", "₪0")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Budget Charts
            try:
                monthly_trends_fig = create_monthly_trends(expenses_df, donations_df)
                if monthly_trends_fig:
                    st.plotly_chart(monthly_trends_fig, use_container_width=True)
                else:
                    st.warning("⚠️ לא ניתן לטעון גרף מגמות חודשיות")
                
                budget_dist_fig = create_budget_distribution_chart(expenses_df)
                if budget_dist_fig:
                    st.plotly_chart(budget_dist_fig, use_container_width=True)
                else:
                    st.warning("⚠️ לא ניתן לטעון גרף התפלגות תקציב")
            except Exception as e:
                st.error("שגיאה בטעינת גרפים תקציביים")
                logging.error(f"Budget charts error: {e}")
            
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # Donors Management Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>👥 ניהול תורמים</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("סה״כ תורמים", f"{donor_stats['total_donors']:,}")
            with col2:
                st.metric("סה״כ תרומות", f"₪{donor_stats['total_donations']:,.0f}")
            with col3:
                st.metric("תרומה ממוצעת", f"₪{donor_stats['avg_donation']:,.0f}")
            with col4:
                st.metric("תרומה גבוהה ביותר", f"₪{donor_stats['max_donation']:,.0f}")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Donor Charts
            try:
                donor_fig = create_donor_contribution_chart(donations_df)
                if donor_fig:
                    st.plotly_chart(donor_fig, use_container_width=True)
                else:
                    st.warning("⚠️ לא ניתן לטעון גרף תרומות תורמים")
            except Exception as e:
                st.error("שגיאה בטעינת גרפי תורמים")
                logging.error(f"Donor charts error: {e}")
            
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # Widows Management Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>👩 ניהול אלמנות</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("סה״כ אלמנות", f"{widow_stats['total_widows']:,}")
            with col2:
                try:
                    total_support = float(widow_stats['total_support']) if widow_stats['total_support'] is not None else 0
                    st.metric("סך תמיכה חודשית", f"₪{total_support:,.0f}")
                except (ValueError, TypeError):
                    st.metric("סך תמיכה חודשית", "₪0")
            with col3:
                try:
                    avg_children = almanot_df['מספר ילדים'].mean() if 'מספר ילדים' in almanot_df.columns else 0
                    st.metric("מספר ילדים ממוצע", f"{avg_children:.1f}")
                except Exception as e:
                    st.metric("מספר ילדים ממוצע", "N/A")
            with col4:
                try:
                    avg_monthly_support = almanot_df['סכום חודשי'].mean() if 'סכום חודשי' in almanot_df.columns else 0
                    st.metric("תמיכה חודשית ממוצעת", f"₪{avg_monthly_support:,.0f}")
                except Exception as e:
                    st.metric("תמיכה חודשית ממוצעת", "N/A")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Widow Charts
            try:
                widows_fig = create_widows_support_chart(almanot_df)
                if widows_fig:
                    st.plotly_chart(widows_fig, use_container_width=True)
                else:
                    st.warning("⚠️ לא ניתן לטעון גרף תמיכה אלמנות")
            except Exception as e:
                st.error("שגיאה בטעינת גרפי אלמנות")
                logging.error(f"Widow charts error: {e}")
            
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Widows without donors
            try:
                widows_without_donors = almanot_df[almanot_df['תורם'].isna() | (almanot_df['תורם'] == '')]
                if len(widows_without_donors) > 0:
                    st.warning(f"⚠️ יש {len(widows_without_donors)} אלמנות ללא תורם")
                    st.dataframe(widows_without_donors[['שם ', 'מספר ילדים', 'סכום חודשי']], use_container_width=True)
                else:
                    st.success("כל האלמנות מחוברות לתורמים!")
            except Exception as e:
                st.error("שגיאה בטעינת אלמנות ללא תורם")
            
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # Reports Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>📋 דוחות</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 דוח חודשי מפורט", use_container_width=True):
                    try:
                        filename = generate_monthly_report(expenses_df, donations_df, almanot_df)
                        if filename:
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="הורד דוח חודשי",
                                    data=file.read(),
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error("שגיאה ביצירת דוח חודשי")
                
                if st.button("👥 דוח תורמים מפורט", use_container_width=True):
                    try:
                        filename = generate_donor_report(donations_df)
                        if filename:
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="הורד דוח תורמים",
                                    data=file.read(),
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error("שגיאה ביצירת דוח תורמים")
            
            with col2:
                if st.button("👩 דוח אלמנות מפורט", use_container_width=True):
                    try:
                        filename = generate_widows_report(almanot_df)
                        if filename:
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="הורד דוח אלמנות",
                                    data=file.read(),
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error("שגיאה ביצירת דוח אלמנות")
                
                if st.button("💰 דוח תקציב מפורט", use_container_width=True):
                    try:
                        filename = generate_budget_report(expenses_df, donations_df)
                        if filename:
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="הורד דוח תקציב",
                                    data=file.read(),
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error("שגיאה ביצירת דוח תקציב")
        
        with tab2:
            # Network Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>🕸️ מפת קשרים</h2>", unsafe_allow_html=True)
            
            try:
                # Create nodes and edges for the network
                nodes = []
                edges = []
                
                # Get all valid donors
                all_donors = set()
                if 'שם' in donations_df.columns:
                    donors_from_donations = donations_df['שם'].dropna().unique()
                    all_donors.update(donors_from_donations)
                
                if 'שם' in investors_df.columns:
                    donors_from_investors = investors_df['שם'].dropna().unique()
                    all_donors.update(donors_from_investors)
                
                # Get valid donor-widow pairs
                valid_donor_widow_pairs = almanot_df[['שם ', 'תורם']].dropna()
                valid_donor_widow_pairs = valid_donor_widow_pairs[
                    (valid_donor_widow_pairs['תורם'].str.strip() != '') & 
                    (~valid_donor_widow_pairs['תורם'].str.contains('DONOR_', case=False, na=False)) &
                    (valid_donor_widow_pairs['תורם'].str.len() > 1) &
                    (valid_donor_widow_pairs['שם '].str.strip() != '') &
                    (valid_donor_widow_pairs['שם '].str.len() > 1)
                ]
                
                # Add donors as nodes
                for donor in all_donors:
                    if pd.notna(donor) and str(donor).strip() != '' and len(str(donor).strip()) > 1:
                        nodes.append(Node(id=f"donor_{donor}", label=donor, size=25, color="#1f77b4"))
                
                # Add widows as nodes
                for _, widow in almanot_df.iterrows():
                    if pd.notna(widow['שם ']) and str(widow['שם ']).strip() != '' and len(str(widow['שם ']).strip()) > 1:
                        nodes.append(Node(id=f"widow_{widow['שם ']}", label=widow['שם '], size=20, color="#ff7f0e"))
                
                # Add edges for relationships
                for _, widow in valid_donor_widow_pairs.iterrows():
                    if pd.notna(widow['תורם']) and pd.notna(widow['שם ']):
                        edges.append(Edge(source=f"donor_{widow['תורם']}", target=f"widow_{widow['שם ']}", label="תמיכה"))
                
                # Configure network
                config = Config(
                    height=1200,
                    width="100%",
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    responsive=True,
                    nodeSpacing=50,
                    linkDistance=100,
                    zoom=True,
                    pan=True
                )
                
                # Display network
                if nodes:
                    connected_donors = len(valid_donor_widow_pairs['תורם'].unique()) if len(valid_donor_widow_pairs) > 0 else 0
                    connected_widows = len(valid_donor_widow_pairs)
                    st.info(f"מציג {len(all_donors)} תורמים ו-{len(almanot_df)} אלמנות. {connected_donors} תורמים מחוברים ל-{connected_widows} אלמנות.")
                    
                    agraph(nodes=nodes, edges=edges, config=config)
                else:
                    st.info("אין נתונים להצגה במפת הקשרים")
                
            except Exception as e:
                logging.error(f"שגיאה ביצירת מפת הקשרים: {str(e)}")
                st.error(f"שגיאה ביצירת מפת הקשרים: {str(e)}")
        
        logging.info("=== DASHBOARD RENDERING COMPLETED ===")
        
    except Exception as e:
        logging.error(f"General error in main function: {e}")
        st.error(f"שגיאה כללית: {str(e)}")

if __name__ == "__main__":
    main() 
