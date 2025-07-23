import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging
import traceback
import sys
import os
import math
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
from data_loading import load_data
from google_sheets_io import write_sheet, check_service_account_validity
from alerts import check_budget_alerts, check_data_quality_alerts, check_widows_alerts, check_donations_alerts

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
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

# Add success message function
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

# Add custom CSS for RTL support and styling
st.markdown("""
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
        margin: 0;
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Data editor */
    .stDataEditor {
        font-size: 0.9rem !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Metric styling */
    .css-1wivap2 {
        font-size: 1.2rem !important;
    }
    
    .css-1wivap2 > div > div > div {
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }
    
    /* General text */
    p, div, span {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Strong text */
    strong {
        font-weight: 600 !important;
        color: #374151 !important;
    }
    
    /* Tables */
    .stDataFrame {
        margin: 1rem 0;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
        border: 1px solid #e1e5ea !important;
    }
    
    .streamlit-expanderContent {
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #e1e5ea !important;
    }
    
    /* Sections */
    .section-header {
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e5e7eb !important;
    }
    
    /* Columns spacing */
    .row-widget.stHorizontal {
        gap: 1rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        margin: 0.5rem 0 !important;
        padding: 0.75rem 1.5rem !important;
    }
    
    /* Metrics */
    .metric-container {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
        border: 1px solid #e1e5ea !important;
    }
    
    /* Alerts */
    .stAlert {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Data editor */
    .stDataEditor {
        margin: 1rem 0 !important;
        border-radius: 8px !important;
        border: 1px solid #e1e5ea !important;
    }
    
    /* Charts */
    .stPlotlyChart {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #e1e5ea !important;
    }
    
    /* Tabs content */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 1.5rem 0 !important;
    }
    
    /* Success messages */
    .stSuccess {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Info boxes */
    .stInfo {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Warning boxes */
    .stWarning {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Error boxes */
    .stError {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

def save_expenses_data(expenses_df):
    """Save expenses data to Excel file"""
    try:
        write_sheet("Expenses", expenses_df)
        st.session_state.changes_made['expenses'] = False
        st.success("הוצאות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת הוצאות: {str(e)}")

def save_donations_data(donations_df):
    """Save donations data to Excel file"""
    try:
        write_sheet("Donations", donations_df)
        st.session_state.changes_made['donations'] = False
        st.success("תרומות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת תרומות: {str(e)}")

def save_widows_data(almanot_df):
    """Save widows data to Excel file"""
    try:
        write_sheet("Widows", almanot_df)
        st.session_state.changes_made['widows'] = False
        st.success("נתוני אלמנות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני אלמנות: {str(e)}")

def save_investors_data(investors_df):
    """Save investors data to Excel file"""
    try:
        write_sheet("Investors", investors_df)
        st.session_state.changes_made['investors'] = False
        st.success("נתוני משקיעים נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני משקיעים: {str(e)}")

def get_edge_color(amount):
    """מחזיר צבע קשר לפי סכום התרומה"""
    if amount == 1000:
        return "#fbbf24"  # צהוב
    elif amount == 2000:
        return "#3b82f6"  # כחול
    else:
        return "#9ca3af"  # אפור

def extract_amount_from_title(title):
    """מחלץ סכום מתיאור הקשר"""
    try:
        # מחפש תבנית כמו "1.0k ₪" או "2.0k ₪"
        import re
        match = re.search(r'(\d+\.?\d*)k', title)
        if match:
            return int(float(match.group(1)) * 1000)
        return 1000  # ברירת מחדל
    except:
        return 1000

def update_connection_in_data(donor_name, widow_name, amount):
    """מעדכן קשר בקבצי הנתונים"""
    try:
        # טעינת הנתונים הנוכחיים
        almanot_df = pd.read_excel('almanot.xlsx')
        
        # עדכון התורם והסכום באלמנה
        almanot_df.loc[almanot_df['שם '] == widow_name, 'תורם'] = donor_name
        almanot_df.loc[almanot_df['שם '] == widow_name, 'סכום חודשי'] = amount
        
        # שמירת הנתונים
        almanot_df.to_excel('almanot.xlsx', index=False)
        
        # הוספת תרומה חדשה לקובץ התרומות
        donations_df = pd.read_excel('omri.xlsx')
        new_donation = {
            'תאריך': pd.Timestamp.now(),
            'שם': donor_name,
            'שקלים': amount,
            'הערות': f'תרומה חודשית ל{widow_name}'
        }
        donations_df = pd.concat([donations_df, pd.DataFrame([new_donation])], ignore_index=True)
        donations_df.to_excel('omri.xlsx', index=False)
        
        return True
    except Exception as e:
        st.error(f"שגיאה בעדכון הנתונים: {str(e)}")
        return False

def remove_connection_from_data(donor_name, widow_name):
    """מסיר קשר מקבצי הנתונים"""
    try:
        # טעינת הנתונים הנוכחיים
        almanot_df = pd.read_excel('almanot.xlsx')
        
        # הסרת התורם מהאלמנה
        almanot_df.loc[almanot_df['שם '] == widow_name, 'תורם'] = None
        almanot_df.loc[almanot_df['שם '] == widow_name, 'סכום חודשי'] = 0
        
        # שמירת הנתונים
        almanot_df.to_excel('almanot.xlsx', index=False)
        
        return True
    except Exception as e:
        st.error(f"שגיאה בהסרת הקשר: {str(e)}")
        return False

def main():
    try:
        logging.info("=== DASHBOARD STARTED ===")
        logging.info("Main function called successfully")
        
        st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>מערכת ניהול עמותת עמרי</h1>", unsafe_allow_html=True)
        
        # Check service account validity before loading data
        if not check_service_account_validity():
            st.stop()
        
        # Display success messages
        display_success_messages()
        
        # Initialize session state for tracking changes
        if 'changes_made' not in st.session_state:
            st.session_state.changes_made = {
                'expenses': False,
                'donations': False,
                'investors': False,
                'widows': False
            }
        
        # Load data ONCE per session and keep in session_state
        if 'expenses_df' not in st.session_state or 'donations_df' not in st.session_state or 'almanot_df' not in st.session_state or 'investors_df' not in st.session_state:
        expenses_df, donations_df, almanot_df, investors_df = load_data()
            st.session_state.expenses_df = expenses_df
            st.session_state.donations_df = donations_df
            st.session_state.almanot_df = almanot_df
            st.session_state.investors_df = investors_df
        else:
            expenses_df = st.session_state.expenses_df
            donations_df = st.session_state.donations_df
            almanot_df = st.session_state.almanot_df
            investors_df = st.session_state.investors_df
        
        # Log data loading results
        logging.info("=== DATA LOADING DEBUG INFO ===")
        logging.info(f"Expenses DataFrame: {'Loaded' if expenses_df is not None else 'Failed to load'}")
        logging.info(f"Donations DataFrame: {'Loaded' if donations_df is not None else 'Failed to load'}")
        logging.info(f"Almanot DataFrame: {'Loaded' if almanot_df is not None else 'Failed to load'}")
        logging.info(f"Investors DataFrame: {'Loaded' if investors_df is not None else 'Failed to load'}")
        if expenses_df is not None:
            logging.info(f"Expenses shape: {expenses_df.shape}, columns: {list(expenses_df.columns)}")
        if donations_df is not None:
            logging.info(f"Donations shape: {donations_df.shape}, columns: {list(donations_df.columns)}")
        if almanot_df is not None:
            logging.info(f"Almanot shape: {almanot_df.shape}, columns: {list(almanot_df.columns)}")
        if investors_df is not None:
            logging.info(f"Investors shape: {investors_df.shape}, columns: {list(investors_df.columns)}")
        logging.info("=== END DATA LOADING DEBUG INFO ===")
        
        # Check if data was loaded successfully
        if expenses_df is None or donations_df is None or almanot_df is None or investors_df is None:
            st.error("לא ניתן להמשיך ללא נתונים תקינים")
            return
        
        # Show success message for data loading
        show_success_message("הנתונים נטענו בהצלחה!")
        
        # Calculate statistics for alerts
        budget_status = calculate_monthly_budget(expenses_df, donations_df)
        donor_stats = calculate_donor_statistics(donations_df)
        widow_stats = calculate_widow_statistics(almanot_df)
        
        # Calculate missing variables for budget summary
        total_don = donations_df['שקלים'].sum() if 'שקלים' in donations_df.columns else 0
        sum_exp = expenses_df['שקלים'].sum() if 'שקלים' in expenses_df.columns else 0
        available = total_don - sum_exp
        
        # Add monthly_budget to budget_status if it doesn't exist
        if 'monthly_budget' not in budget_status:
            try:
                monthly_expenses = expenses_df.groupby(expenses_df['תאריך'].dt.strftime('%Y-%m') if pd.notna(expenses_df['תאריך']).any() else 'Unknown')['שקלים'].sum()
                monthly_donations = donations_df.groupby(donations_df['תאריך'].dt.strftime('%Y-%m') if pd.notna(donations_df['תאריך']).any() else 'Unknown')['שקלים'].sum()
                
                monthly_budget_data = []
                all_months = sorted(set(monthly_expenses.index) | set(monthly_donations.index))
                
                for month in all_months:
                    expenses = monthly_expenses.get(month, 0)
                    donations = monthly_donations.get(month, 0)
                    balance = donations - expenses
                    coverage_ratio = (donations / expenses * 100) if expenses > 0 else 0
                    
                    monthly_budget_data.append({
                        'חודש': month,
                        'הוצאות': expenses,
                        'תרומות': donations,
                        'יתרה': balance,
                        'יחס כיסוי': coverage_ratio / 100
                    })
                
                budget_status['monthly_budget'] = monthly_budget_data
            except Exception as e:
                logging.error(f"Error creating monthly budget: {str(e)}")
                budget_status['monthly_budget'] = []
        
        # Create tabs - Homepage and Network
        tab1, tab2 = st.tabs(["🏠 דף הבית", "🕸️ מפת קשרים"])
        
        with tab1:
            # Internal Navigation Menu
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
                <h3 style='margin: 0 0 1rem 0; color: #374151;'>ניווט מהיר:</h3>
                <div style='display: flex; gap: 1rem; flex-wrap: wrap;'>
                    <a href='#dashboard' style='text-decoration: none; color: #1a73e8; padding: 0.5rem 1rem; background: white; border-radius: 5px; border: 1px solid #e1e5ea;'>📊 סקירה כללית</a>
                    <a href='#budget' style='text-decoration: none; color: #1a73e8; padding: 0.5rem 1rem; background: white; border-radius: 5px; border: 1px solid #e1e5ea;'>💰 ניהול תקציב</a>
                    <a href='#donors' style='text-decoration: none; color: #1a73e8; padding: 0.5rem 1rem; background: white; border-radius: 5px; border: 1px solid #e1e5ea;'>👥 ניהול תורמים</a>
                    <a href='#widows' style='text-decoration: none; color: #1a73e8; padding: 0.5rem 1rem; background: white; border-radius: 5px; border: 1px solid #e1e5ea;'>👩 ניהול אלמנות</a>
                    <a href='#reports' style='text-decoration: none; color: #1a73e8; padding: 0.5rem 1rem; background: white; border-radius: 5px; border: 1px solid #e1e5ea;'>📋 דוחות</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ===== DASHBOARD SECTION =====
            st.markdown("<div id='dashboard'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>📊 סקירה כללית</h2>", unsafe_allow_html=True)
            
            # General Statistics
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטיסטיקות כלליות</h3>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("סך תרומות", f"₪{total_don:,.0f}")
            with col2:
                st.metric("סך הוצאות", f"₪{sum_exp:,.0f}")
            with col3:
                st.metric("יתרה", f"₪{available:,.0f}")
            with col4:
                coverage = (total_don / sum_exp * 100) if sum_exp > 0 else 0
                st.metric("יחס כיסוי", f"{coverage:.1f}%")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Key Metrics Row
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>מדדים מרכזיים</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}")
            with col2:
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Recent Activity
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>פעילות אחרונה</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 style='color: #6b7280; margin-bottom: 0.5rem;'>תרומות אחרונות</h4>", unsafe_allow_html=True)
                recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                for _, donation in recent_donations.iterrows():
                    donation_date = donation['תאריך']
                    if pd.notna(donation_date):
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} ({donation_date.strftime('%d/%m/%Y')})")
                    else:
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} (תאריך לא מוגדר)")
            
            with col2:
                st.markdown("<h4 style='color: #6b7280; margin-bottom: 0.5rem;'>הוצאות אחרונות</h4>", unsafe_allow_html=True)
                recent_expenses = expenses_df.sort_values('תאריך', ascending=False).head(5)
                for _, expense in recent_expenses.iterrows():
                    expense_date = expense['תאריך']
                    if pd.notna(expense_date):
                        st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} ({expense_date.strftime('%d/%m/%Y')})")
                    else:
                        st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} (תאריך לא מוגדר)")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Alerts
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>התראות</h3>", unsafe_allow_html=True)
            
            # Check for various alerts
            all_alerts = []
            
            # Budget alerts
            budget_alerts = check_budget_alerts(budget_status, donations_df)
            if budget_alerts:
                all_alerts.extend(budget_alerts)
            
            # Data quality alerts
            data_alerts = check_data_quality_alerts(expenses_df, donations_df, almanot_df)
            if data_alerts:
                all_alerts.extend(data_alerts)
            
            # Widows alerts
            widows_alerts = check_widows_alerts(widow_stats)
            if widows_alerts:
                all_alerts.extend(widows_alerts)
            
            # Donations alerts
            donations_alerts = check_donations_alerts(donor_stats)
            if donations_alerts:
                all_alerts.extend(donations_alerts)
            
            if all_alerts:
                for alert in all_alerts:
                    st.warning(f"⚠️ {alert}")
            else:
                st.success("✅ אין התראות פעילות")
            
            # Add spacing
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # ===== BUDGET MANAGEMENT SECTION =====
            st.markdown("<div id='budget'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>💰 ניהול תקציב</h2>", unsafe_allow_html=True)
            
            # Budget Status
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטוס תקציב</h3>", unsafe_allow_html=True)
            
            # Calculate budget status
            total_donations = donations_df['שקלים'].sum() if 'שקלים' in donations_df.columns else 0
            total_expenses = expenses_df['שקלים'].sum() if 'שקלים' in expenses_df.columns else 0
            available_budget = total_donations - total_expenses
            
            # Determine budget status color
            if available_budget > 0:
                status_color = "green"
                status_text = "מצוין"
            elif available_budget == 0:
                status_color = "orange"
                status_text = "מאוזן"
            else:
                status_color = "red"
                status_text = "גירעון"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("סך תרומות", f"₪{total_donations:,.0f}")
            with col2:
                st.metric("סך הוצאות", f"₪{total_expenses:,.0f}")
            with col3:
                st.metric("יתרה זמינה", f"₪{available_budget:,.0f}")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Budget Charts
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>גרפים תקציביים</h3>", unsafe_allow_html=True)
            
            # Add CSS for centering charts
            st.markdown("""
            <style>
            .stPlotlyChart {
                display: flex;
                justify-content: center;
                margin: 0 auto;
            }
            .stPlotlyChart > div {
                width: 100% !important;
                max-width: 800px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Monthly trends chart
            monthly_trends_fig = create_monthly_trends(expenses_df, donations_df)
            if monthly_trends_fig:
                st.plotly_chart(monthly_trends_fig, use_container_width=True)
            
            # Budget distribution chart - fixed function call
            create_budget_distribution_chart(expenses_df)
            
            # Add spacing
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # ===== DONORS MANAGEMENT SECTION =====
            st.markdown("<div id='donors'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>👥 ניהול תורמים</h2>", unsafe_allow_html=True)
            
            # Donor Statistics
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטיסטיקות תורמים</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}")
            with col2:
                st.metric("סך תרומות", f"₪{donor_stats['total_donations']:,.0f}")
            with col3:
                st.metric("תרומה ממוצעת", f"₪{donor_stats['avg_donation']:,.0f}")
            with col4:
                st.metric("תורם הגדול ביותר", f"₪{donor_stats['max_donation']:,.0f}")
            
            # Donor Charts
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>גרפי תורמים</h3>", unsafe_allow_html=True)
            
            # Donor contribution chart
            create_donor_contribution_chart(donations_df)
            
            # Add spacing
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # ===== WIDOWS MANAGEMENT SECTION =====
            st.markdown("<div id='widows'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>👩 ניהול אלמנות</h2>", unsafe_allow_html=True)
            
            # Widow Statistics
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטיסטיקות אלמנות</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}")
            with col2:
                st.metric("סך תמיכה חודשית", f"₪{widow_stats['total_support']:,.0f}")
            with col3:
                try:
                    if 'מספר ילדים' in almanot_df.columns:
                        # Convert to numeric, handling non-numeric values
                        children_col = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce')
                        avg_children = children_col.mean()
                        if pd.notna(avg_children):
                            st.metric("מספר ילדים ממוצע", f"{avg_children:.1f}")
                        else:
                            st.metric("מספר ילדים ממוצע", "N/A")
                    else:
                        st.metric("מספר ילדים ממוצע", "N/A")
                except Exception as e:
                    logging.error(f"Error calculating average children: {str(e)}")
                    st.metric("מספר ילדים ממוצע", "N/A")
            
            # Widow Charts
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>גרפי אלמנות</h3>", unsafe_allow_html=True)
            
            # Widows support chart
            create_widows_support_chart(almanot_df)
            
            # Add information about widows without donors
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>אלמנות ללא תורם מוגדר</h3>", unsafe_allow_html=True)
            
            # Get widows without donors
            widows_without_donors_df = almanot_df[
                (almanot_df['תורם'].isna()) | 
                (almanot_df['תורם'].str.strip() == '') |
                (almanot_df['תורם'].str.contains('DONOR_', case=False, na=False))
            ]
            
            if len(widows_without_donors_df) > 0:
                st.info(f"יש {len(widows_without_donors_df)} אלמנות ללא תורם מוגדר")
                st.dataframe(
                    widows_without_donors_df[['שם ', 'מייל', 'טלפון', 'סכום חודשי']].rename(columns={
                        'שם ': 'שם',
                        'סכום חודשי': 'סכום חודשי (₪)'
                    }),
                    use_container_width=True
                )
            else:
                st.success("כל האלמנות מחוברות לתורמים!")
            
            # Add spacing
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
            
            # ===== REPORTS SECTION =====
            st.markdown("<div id='reports'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>📋 דוחות</h2>", unsafe_allow_html=True)
            
            # Report Generation
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>יצירת דוחות</h3>", unsafe_allow_html=True)
            
                    col1, col2 = st.columns(2)
                    with col1:
                if st.button("📊 דוח חודשי מפורט", use_container_width=True):
                    filename = generate_monthly_report(expenses_df, donations_df, almanot_df)
                    if filename:
                        show_success_message("דוח חודשי נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח חודשי",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
                
                if st.button("👥 דוח תורמים מפורט", use_container_width=True):
                    filename = generate_donor_report(donations_df)
                    if filename:
                        show_success_message("דוח תורמים נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח תורמים",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
                
            with col2:
                if st.button("👩 דוח אלמנות מפורט", use_container_width=True):
                    filename = generate_widows_report(almanot_df)
                    if filename:
                        show_success_message("דוח אלמנות נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח אלמנות",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
                
                if st.button("💰 דוח תקציב מפורט", use_container_width=True):
                    filename = generate_budget_report(expenses_df, donations_df)
                    if filename:
                        show_success_message("דוח תקציב נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח תקציב",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
            
            # Add spacing at the end
            st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
        
        with tab2:
            # ===== NETWORK SECTION =====
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>🕸️ מפת קשרים</h2>", unsafe_allow_html=True)
            
            # Network Visualization
            st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>מפת קשרים בין תורמים לאלמנות</h3>", unsafe_allow_html=True)
            
            # Create network visualization
            try:
                # Log detailed information about the data
                logging.info("=== NETWORK MAP DEBUG INFO ===")
                logging.info(f"Almanot DataFrame shape: {almanot_df.shape}")
                logging.info(f"Almanot DataFrame columns: {list(almanot_df.columns)}")
                logging.info(f"Sample almanot data (first 3 rows):")
                for i, row in almanot_df.head(3).iterrows():
                    logging.info(f"  Row {i}: {dict(row)}")
                
                logging.info(f"Donations DataFrame shape: {donations_df.shape}")
                logging.info(f"Donations DataFrame columns: {list(donations_df.columns)}")
                logging.info(f"Sample donations data (first 3 rows):")
                for i, row in donations_df.head(3).iterrows():
                    logging.info(f"  Row {i}: {dict(row)}")
                
                logging.info(f"Investors DataFrame shape: {investors_df.shape}")
                logging.info(f"Investors DataFrame columns: {list(investors_df.columns)}")
                logging.info(f"Sample investors data (first 3 rows):")
                for i, row in investors_df.head(3).iterrows():
                    logging.info(f"  Row {i}: {dict(row)}")
                
                # Create nodes and edges for the network
                nodes = []
                edges = []
                
                # Get all valid donors from donations data
                all_donors = set()
                
                # Debug donations data
                logging.info(f"Debug: Donations columns: {list(donations_df.columns)}")
                logging.info(f"Debug: Donations shape: {donations_df.shape}")
                if 'שם' in donations_df.columns:
                    donors_from_donations = donations_df['שם'].dropna().unique()
                    logging.info(f"Debug: Found {len(donors_from_donations)} donors from donations")
                    logging.info(f"Debug: Sample donors from donations: {list(donors_from_donations[:5])}")
                    all_donors.update(donors_from_donations)
                else:
                    logging.info("Debug: 'שם' column not found in donations_df")
                
                # Debug investors data
                logging.info(f"Debug: Investors columns: {list(investors_df.columns)}")
                logging.info(f"Debug: Investors shape: {investors_df.shape}")
                if 'שם' in investors_df.columns:
                    donors_from_investors = investors_df['שם'].dropna().unique()
                    logging.info(f"Debug: Found {len(donors_from_investors)} donors from investors")
                    logging.info(f"Debug: Sample donors from investors: {list(donors_from_investors[:5])}")
                    all_donors.update(donors_from_investors)
                else:
                    logging.info("Debug: 'שם' column not found in investors_df")
                
                # Debug info
                logging.info(f"Debug: Found {len(all_donors)} total donors")
                logging.info(f"Debug: Found {len(almanot_df)} total widows")
                
                # Get valid donor-widow pairs where both donor and widow names exist
                valid_donor_widow_pairs = almanot_df[['שם ', 'תורם']].dropna()
                logging.info(f"Debug: Initial donor-widow pairs: {len(valid_donor_widow_pairs)}")
                
                # Log sample donor-widow pairs before filtering
                logging.info("Sample donor-widow pairs before filtering:")
                for i, row in valid_donor_widow_pairs.head(5).iterrows():
                    logging.info(f"  Row {i}: Donor='{row['תורם']}', Widow='{row['שם ']}'")
                
                # Filter out invalid donor names (like 'DONOR_', empty strings, etc.)
                valid_donor_widow_pairs = valid_donor_widow_pairs[
                    (valid_donor_widow_pairs['תורם'].str.strip() != '') & 
                    (~valid_donor_widow_pairs['תורם'].str.contains('DONOR_', case=False, na=False)) &
                    (valid_donor_widow_pairs['תורם'].str.len() > 1) &
                    (valid_donor_widow_pairs['שם '].str.strip() != '') &
                    (valid_donor_widow_pairs['שם '].str.len() > 1)
                ]
                logging.info(f"Debug: After filtering: {len(valid_donor_widow_pairs)} pairs")
                
                # Log sample donor-widow pairs after filtering
                logging.info("Sample donor-widow pairs after filtering:")
                for i, row in valid_donor_widow_pairs.head(5).iterrows():
                    logging.info(f"  Row {i}: Donor='{row['תורם']}', Widow='{row['שם ']}'")
                
                # Add all donors as nodes (including those without widows)
                for donor in all_donors:
                    if pd.notna(donor) and str(donor).strip() != '' and len(str(donor).strip()) > 1:
                        nodes.append(Node(id=f"donor_{donor}", label=donor, size=25, color="#2563eb", shape="circle"))
                
                # Add all widows as nodes (including those without donors)
                for _, widow in almanot_df.iterrows():
                    if pd.notna(widow['שם ']) and str(widow['שם ']).strip() != '' and len(str(widow['שם ']).strip()) > 1:
                        nodes.append(Node(id=f"widow_{widow['שם ']}", label=widow['שם '], size=20, color="#f43f5e", shape="square"))
                
                # Add edges only for valid donor-widow relationships
                for _, widow in valid_donor_widow_pairs.iterrows():
                    if pd.notna(widow['תורם']) and pd.notna(widow['שם ']):
                        edges.append(Edge(source=f"donor_{widow['תורם']}", target=f"widow_{widow['שם ']}", color="#9ca3af"))
                
                logging.info(f"Debug: Created {len(nodes)} nodes and {len(edges)} edges")
                logging.info("=== END NETWORK MAP DEBUG INFO ===")
                
                # Configure the network to use full screen space
                config = Config(
                    height=1200,  # Reduced height for better fit
                    width="100%",  # Use full width
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    # Add responsive settings
                    responsive=True,
                    # Improve visualization
                    nodeSpacing=50,
                    linkDistance=100,
                    # Add zoom and pan controls
                    zoom=True,
                    pan=True
                )
                
                # Add CSS to ensure the container is large enough and properly positioned
                st.markdown("""
                <style>
                .stApp {
                    min-height: 100vh;
                }
                .main .block-container {
                    padding-bottom: 2rem;
                }
                /* Ensure the network graph container is large enough */
                .stAgraph {
                    min-height: 2500px !important;
                    height: 2500px !important;
                }
                /* Position the network graph properly */
                div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stAgraph"]) {
                    min-height: 2500px !important;
                    height: 2500px !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Display the network directly
                if nodes:
                    # Show statistics above the map
                    connected_donors = len(valid_donor_widow_pairs['תורם'].unique()) if len(valid_donor_widow_pairs) > 0 else 0
                    connected_widows = len(valid_donor_widow_pairs)
                    st.info(f"מציג {len(all_donors)} תורמים ו-{len(almanot_df)} אלמנות. {connected_donors} תורמים מחוברים ל-{connected_widows} אלמנות.")
                    
                    # Add connection management section BEFORE the graph
                    st.markdown("<h3 style='color: #4b5563; margin-top: 2rem; margin-bottom: 1rem;'>ניהול קשרים</h3>", unsafe_allow_html=True)
                    
                    # Initialize session state for showing sections
                    if 'show_create_connection' not in st.session_state:
                        st.session_state.show_create_connection = False
                    if 'show_remove_connection' not in st.session_state:
                        st.session_state.show_remove_connection = False
                    
                    # Main buttons row
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
            with col1:
                        if st.button("➕ צור קשר חדש", key="show_create_btn", use_container_width=True):
                            st.session_state.show_create_connection = not st.session_state.show_create_connection
                            st.session_state.show_remove_connection = False
                            # No rerun here
                    
            with col2:
                        if st.button("➖ הסר קשר קיים", key="show_remove_btn", use_container_width=True):
                            st.session_state.show_remove_connection = not st.session_state.show_remove_connection
                            st.session_state.show_create_connection = False
                            # No rerun here
                    
                    # Show create connection section
                    if st.session_state.show_create_connection:
                        st.markdown("---")
                        st.markdown("**יצירת קשר חדש**")
                        
                        # Get available donors and widows
                        available_donors = list(all_donors)
                        available_widows = almanot_df['שם '].dropna().unique().tolist()
                        
                        # Filter out widows that already have donors
                        widows_with_donors = valid_donor_widow_pairs['שם '].unique()
                        available_widows = [w for w in available_widows if w not in widows_with_donors]
                        
                        if available_donors and available_widows:
                            selected_donor = st.selectbox("בחר תורם:", available_donors, key="new_connection_donor")
                            selected_widow = st.selectbox("בחר אלמנה:", available_widows, key="new_connection_widow")
                            connection_amount = st.number_input("סכום חודשי (₪):", min_value=0, value=1000, step=100, key="new_connection_amount")
                            
                            if st.button("יצור קשר", key="create_connection"):
                                try:
                                    # Update the widow's donor information in session_state only
                                    st.session_state.almanot_df.loc[st.session_state.almanot_df['שם '] == selected_widow, 'תורם'] = selected_donor
                                    st.session_state.almanot_df.loc[st.session_state.almanot_df['שם '] == selected_widow, 'סכום חודשי'] = connection_amount
                                    st.session_state.unsaved_changes = True
                                    show_success_message(f"קשר נוצר בהצלחה בין {selected_donor} ל-{selected_widow}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"שגיאה ביצירת הקשר: {str(e)}")
                        else:
                            if not available_donors:
                                st.warning("אין תורמים זמינים")
                            if not available_widows:
                                st.warning("אין אלמנות זמינות ליצירת קשר")
                    
                    # Show remove connection section
                    if st.session_state.show_remove_connection:
                        st.markdown("---")
                        st.markdown("**הסרת קשר קיים**")
                        
                        if len(valid_donor_widow_pairs) > 0:
                            # Create a list of existing connections
                            existing_connections = []
                            for _, row in valid_donor_widow_pairs.iterrows():
                                existing_connections.append(f"{row['תורם']} → {row['שם ']}" )
                            
                            selected_connection = st.selectbox("בחר קשר להסרה:", existing_connections, key="remove_connection")
                            
                            if st.button("הסר קשר", key="remove_connection_btn"):
                                try:
                                    donor_name, widow_name = selected_connection.split(" → ")
                                    st.session_state.almanot_df.loc[st.session_state.almanot_df['שם '] == widow_name, 'תורם'] = ''
                                    st.session_state.almanot_df.loc[st.session_state.almanot_df['שם '] == widow_name, 'סכום חודשי'] = 0
                                    st.session_state.unsaved_changes = True
                                    show_success_message(f"קשר הוסר בהצלחה בין {donor_name} ל-{widow_name}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"שגיאה בהסרת הקשר: {str(e)}")
                        else:
                            st.info("אין קשרים קיימים להסרה")
                    
                    # Add save button only if there are unsaved changes
                    if 'unsaved_changes' not in st.session_state:
                        st.session_state.unsaved_changes = False
                    
                    if st.session_state.unsaved_changes:
                        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
                        st.warning("⚠️ יש שינויים שלא נשמרו!")
                        if st.button("💾 שמור שינויים ל-Google Sheets", key="save_changes", type="primary", use_container_width=True):
                            try:
                                # Save the updated data to Google Sheets
                                save_widows_data(st.session_state.almanot_df)
                                st.session_state.unsaved_changes = False
                                show_success_message("✅ כל השינויים נשמרו בהצלחה ל-Google Sheets!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ שגיאה בשמירת השינויים: {str(e)}")
                    
                    # Display the network graph AFTER the connection management
                    st.markdown("<h3 style='color: #4b5563; margin-top: 2rem; margin-bottom: 1rem;'>מפת הקשרים</h3>", unsafe_allow_html=True)
                    agraph(nodes=nodes, edges=edges, config=config)
                else:
                    st.info("אין נתונים להצגה במפת הקשרים")
                
            except Exception as e:
                logging.error(f"שגיאה ביצירת מפת הקשרים: {str(e)}")
                st.write(f"Debug error details: {e}")
        
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        st.error(f"שגיאה: {str(e)}")

if __name__ == "__main__":
    main()
