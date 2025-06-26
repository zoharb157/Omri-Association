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
from alerts import (
    check_budget_alerts,
    check_data_quality_alerts,
    check_widows_alerts,
    check_donations_alerts,
    display_alerts
)
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import tempfile
import json
import re
from data_loading import load_data
from google_sheets_io import write_sheet

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
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
        st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>מערכת ניהול עמותת עמרי</h1>", unsafe_allow_html=True)
        
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
        
        # Load data
        expenses_df, donations_df, almanot_df, investors_df = load_data()
        
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
        
        # Navigation with tabs like Google Docs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["דף הבית", "ניהול תקציב", "ניהול תורמים", "ניהול אלמנות", "דוחות", "מפת קשרים"])
        
        # Display page content based on tab selection
        with tab1:
            st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>דף הבית - עמותת עמרי</h1>", unsafe_allow_html=True)
            
            # Quick Actions Row
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>פעולות מהירות</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📊 דוח חודשי", use_container_width=True):
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
            with col2:
                if st.button("👥 דוח תורמים", use_container_width=True):
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
            with col3:
                if st.button("👩 דוח אלמנות", use_container_width=True):
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
            with col4:
                if st.button("💰 דוח תקציב", use_container_width=True):
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
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # General Statistics
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>סטטיסטיקות כלליות</h2>", unsafe_allow_html=True)
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
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>מדדים מרכזיים</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}")
            with col2:
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}")
            with col3:
                st.metric("תמיכה חודשית", f"₪{widow_stats['total_support']:,.0f}")
            with col4:
                st.metric("תרומה ממוצעת", f"₪{donor_stats['avg_donation']:,.0f}")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Charts
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>גרפים</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                create_monthly_trends(expenses_df, donations_df)
            with col2:
                create_comparison_chart(expenses_df, donations_df)
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Recent Activity
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>פעילות אחרונה</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>תרומות אחרונות</h3>", unsafe_allow_html=True)
                recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                for _, donation in recent_donations.iterrows():
                    donation_date = donation['תאריך']
                    if pd.notna(donation_date):
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} ({donation_date.strftime('%d/%m/%Y')})")
                    else:
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} (תאריך לא מוגדר)")
            
            with col2:
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>הוצאות אחרונות</h3>", unsafe_allow_html=True)
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
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>התראות</h2>", unsafe_allow_html=True)
            
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
                    st.warning(alert)
            else:
                st.success("אין התראות פעילות")
        
        with tab2:
            st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>ניהול תקציב</h1>", unsafe_allow_html=True)
            
            # Budget Status
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;'>סטטוס תקציב</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("סך הוצאות", f"₪{budget_status['total_expenses']:,.2f}")
            with col2:
                st.metric("סך תרומות", f"₪{budget_status['total_donations']:,.2f}")
            with col3:
                st.metric("יתרה", f"₪{budget_status['balance']:,.2f}")
            with col4:
                st.metric("יחס כיסוי", f"{budget_status['coverage_ratio']:.1f}%")
            # Remove colored status box
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Budget Charts
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>גרפי תקציב</h2>", unsafe_allow_html=True)
            trends = calculate_monthly_trends(expenses_df, donations_df)
            
            col1, col2 = st.columns(2)
            with col1:
                # Custom metric for expenses with correct icon and color
                expenses_change = trends['expenses_change']
                expenses_trend = trends['expenses_trend']
                
                if expenses_trend == "עולה":
                    icon = "📈"
                    color = "#ef4444"  # Red for increasing expenses
                else:
                    icon = "📉"
                    color = "#10b981"  # Green for decreasing expenses
                
                st.markdown(f"""
                <div style="padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; background-color: white;">
                    <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">שינוי בהוצאות</div>
                    <div style="font-size: 2rem; font-weight: bold; color: {color}; margin-bottom: 0.5rem;">
                        {icon} {expenses_change:.1f}%
                    </div>
                    <div style="font-size: 0.875rem; color: #6b7280;">מגמה: {expenses_trend}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Custom metric for donations with correct icon and color
                donations_change = trends['donations_change']
                donations_trend = trends['donations_trend']
                
                if donations_trend == "עולה":
                    icon = "📈"
                    color = "#10b981"  # Green for increasing donations
                else:
                    icon = "📉"
                    color = "#ef4444"  # Red for decreasing donations
                
                st.markdown(f"""
                <div style="padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; background-color: white;">
                    <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">שינוי בתרומות</div>
                    <div style="font-size: 2rem; font-weight: bold; color: {color}; margin-bottom: 0.5rem;">
                        {icon} {donations_change:.1f}%
                    </div>
                    <div style="font-size: 0.875rem; color: #6b7280;">מגמה: {donations_trend}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Monthly Comparison
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;'>השוואה חודשית</h2>", unsafe_allow_html=True)
            if trends['monthly_comparison']:
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>השוואה חודשית</h3>", unsafe_allow_html=True)
                monthly_data = []
                for month, data in trends['monthly_comparison'].items():
                    monthly_data.append({
                        'חודש': month,
                        'הוצאות': data['expenses'],
                        'תרומות': data['donations'],
                        'יתרה': data['balance']
                    })
                
                monthly_df = pd.DataFrame(monthly_data)
                st.dataframe(
                    monthly_df.style.format({
                        'הוצאות': '₪{:,.0f}',
                        'תרומות': '₪{:,.0f}',
                        'יתרה': '₪{:,.0f}'
                    }),
                    use_container_width=True
                )
            
            # Donations Distribution
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;'>התפלגות תרומות</h2>", unsafe_allow_html=True)
            donation_counts = donations_df['שקלים'].value_counts().sort_index()
            
            col1, col2 = st.columns(2)
            with col1:
                # Show top donation amounts
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>🏆 סכומי תרומה נפוצים</h3>", unsafe_allow_html=True)
                for amount, count in donation_counts.head(10).items():
                    st.write(f"**₪{amount:,.0f}:** {count} תרומות")
            
            with col2:
                # Show donation statistics
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטיסטיקות תרומות</h3>", unsafe_allow_html=True)
                st.write(f"**תרומה מקסימלית:** ₪{donations_df['שקלים'].max():,.0f}")
                st.write(f"**תרומה מינימלית:** ₪{donations_df['שקלים'].min():,.0f}")
                st.write(f"**חציון:** ₪{donations_df['שקלים'].median():,.0f}")
            
            # Charts
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;'>גרפים</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                create_monthly_trends(expenses_df, donations_df)
            with col2:
                create_comparison_chart(expenses_df, donations_df)
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Data Editing Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>עריכת נתונים</h2>", unsafe_allow_html=True)
            
            with st.expander("עריכת הוצאות"):
                edited_expenses = st.data_editor(
                    expenses_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config={
                        "תאריך": st.column_config.DateColumn("תאריך", format="DD/MM/YYYY"),
                        "שקלים": st.column_config.NumberColumn("שקלים", format="₪%d")
                    },
                    key="expenses_editor"
                )
                # Check if expenses were changed
                if not edited_expenses.equals(expenses_df):
                    st.session_state.changes_made['expenses'] = True
            
            with st.expander("עריכת תרומות"):
                column_config = {}
                if "שם" in donations_df.columns:
                    column_config["שם"] = st.column_config.TextColumn("שם", required=True)
                if "שקלים" in donations_df.columns:
                    column_config["שקלים"] = st.column_config.NumberColumn("שקלים", format="₪%d")
                if "תאריך" in donations_df.columns:
                    column_config["תאריך"] = st.column_config.DateColumn("תאריך", format="DD/MM/YYYY")
                if "הערות" in donations_df.columns:
                    column_config["הערות"] = st.column_config.TextColumn("הערות")
                
                edited_donations = st.data_editor(
                    donations_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config=column_config,
                    key="donations_budget_editor"
                )
                # Check if donations were changed
                if not edited_donations.equals(donations_df):
                    st.session_state.changes_made['donations'] = True
            
            with st.expander("עריכת משקיעים"):
                column_config = {}
                if "תאריך" in investors_df.columns:
                    column_config["תאריך"] = st.column_config.DateColumn("תאריך", format="DD/MM/YYYY")
                if "שקלים" in investors_df.columns:
                    column_config["שקלים"] = st.column_config.NumberColumn("שקלים", format="₪%d")
                
                edited_investors = st.data_editor(
                    investors_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config=column_config,
                    key="investors_budget_editor"
                )
                # Check if investors were changed
                if not edited_investors.equals(investors_df):
                    st.session_state.changes_made['investors'] = True
            
            with st.expander("עריכת אלמנות"):
                column_config = {}
                if "חודש התחלה" in almanot_df.columns:
                    column_config["חודש התחלה"] = st.column_config.DateColumn("חודש התחלה", format="DD/MM/YYYY")
                if "סכום חודשי" in almanot_df.columns:
                    column_config["סכום חודשי"] = st.column_config.NumberColumn("סכום חודשי", format="₪%d")
                if "שם " in almanot_df.columns:
                    column_config["שם "] = st.column_config.TextColumn("שם", required=True)
                if "מייל" in almanot_df.columns:
                    column_config["מייל"] = st.column_config.TextColumn("מייל")
                if "טלפון" in almanot_df.columns:
                    column_config["טלפון"] = st.column_config.TextColumn("טלפון")
                if "תעודת זהות" in almanot_df.columns:
                    column_config["תעודת זהות"] = st.column_config.TextColumn("תעודת זהות")
                if "מספר ילדים" in almanot_df.columns:
                    column_config["מספר ילדים"] = st.column_config.NumberColumn("מספר ילדים", min_value=0)
                if "חללים" in almanot_df.columns:
                    column_config["חללים"] = st.column_config.CheckboxColumn("חללים")
                if "הערות" in almanot_df.columns:
                    column_config["הערות"] = st.column_config.TextColumn("הערות")
                if "תורם" in almanot_df.columns:
                    column_config["תורם"] = st.column_config.TextColumn("תורם")
                if "איש קשר לתרומה" in almanot_df.columns:
                    column_config["איש קשר לתרומה"] = st.column_config.TextColumn("איש קשר לתרומה")
                
                edited_almanot = st.data_editor(
                    almanot_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config=column_config,
                    key="widows_budget_editor"
                )
                # Check if widows were changed
                if not edited_almanot.equals(almanot_df):
                    st.session_state.changes_made['widows'] = True
            
            # Save edited data - only show if there are changes
            if any(st.session_state.changes_made.values()):
                if st.button("שמור שינויים", type="primary"):
                    try:
                        with pd.ExcelWriter("omri.xlsx", engine="openpyxl") as writer:
                            write_sheet('Expenses', expenses_df)
                            write_sheet('Donations', edited_donations)
                            write_sheet('Investors', edited_investors)
                        
                        # Reset all change flags
                        for key in st.session_state.changes_made:
                            st.session_state.changes_made[key] = False
                        
                        st.success("השינויים נשמרו בהצלחה!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"שגיאה בשמירת השינויים: {str(e)}")
            else:
                st.info("אין שינויים לשמירה")
            
            # Display budget alerts
            st.subheader("התראות תקציב")
            budget_alerts = check_budget_alerts(budget_status, donations_df)
            if budget_alerts:
                for alert in budget_alerts:
                    st.warning(alert)
            else:
                st.success("אין התראות תקציב")
            
            # Calculate current monthly support for 36-month forecast
            if "סכום חודשי" in almanot_df.columns:
                count_1000 = int((almanot_df["סכום חודשי"] == 1000).sum())
                count_2000 = int((almanot_df["סכום חודשי"] == 2000).sum())
                current_monthly_support = (count_1000 * 1000) + (count_2000 * 2000)
                support_36_months = current_monthly_support * 36
            else:
                count_1000 = 0
                count_2000 = 0
                current_monthly_support = 0
                support_36_months = 0
            
            # Display 36-Month Budget Forecast
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;'>תחזית תקציב (36 חודשים)</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                n1 = st.slider(
                    "כמות אלמנות ₪1,000/קרן",
                    min_value=0,
                    max_value=int((available / (1000 * 36)) + 10),
                    value=0,
                    step=1
                )
                req1 = n1 * 1000 * 12 * 3
            
            with col2:
                n2 = st.slider(
                    "כמות אלמנות ₪2,000/קרן",
                    min_value=0,
                    max_value=int((available / (2000 * 36)) + 10),
                    value=0,
                    step=1
                )
                req2 = n2 * 2000 * 12 * 3
            
            # Calculate required budget
            total_required = req1 + req2
            diff = available - support_36_months
            
            st.write(f"**סכום נדרש לתמיכה:** ₪{total_required:,.0f}")
            st.write(f"**סכום זמין לתמיכה:** ₪{support_36_months:,.0f}")
            
            if diff >= 0:
                st.success(f"**יתרה חיובית:** ₪{diff:,.0f}")
            else:
                st.error(f"**גירעון:** ₪{abs(diff):,.0f}")
            
        with tab3:
            st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>ניהול תורמים</h1>", unsafe_allow_html=True)
            
            # Display donor statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}")
            with col2:
                st.metric("סך תרומות", f"₪{donor_stats['total_donations']:,.2f}")
            with col3:
                st.metric("תרומה ממוצעת", f"₪{donor_stats['avg_donation']:,.2f}")
            with col4:
                st.metric("תרומה מקסימלית", f"₪{donor_stats['max_donation']:,.2f}")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Display top donors
            if donor_stats['top_donors']:
                st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>תורמים מובילים</h2>", unsafe_allow_html=True)
                top_donors_df = pd.DataFrame(donor_stats['top_donors'])
                st.dataframe(
                    top_donors_df.style.format({
                        'sum': '₪{:,.0f}',
                        'count': '{:,.0f}'
                    }),
                    use_container_width=True
                )
            
            # Display donor contribution chart
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>תרומות לפי תורם</h2>", unsafe_allow_html=True)
            create_donor_contribution_chart(donations_df)
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Display monthly donations
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>תרומות חודשיות</h2>", unsafe_allow_html=True)
            monthly_donations = donations_df.groupby(donations_df['תאריך'].dt.strftime('%Y-%m') if pd.notna(donations_df['תאריך']).any() else 'Unknown')['שקלים'].sum().reset_index()
            monthly_donations.columns = ['חודש', 'סכום']
            monthly_donations = monthly_donations.sort_values('חודש', ascending=False)
            st.dataframe(
                monthly_donations.style.format({'סכום': '₪{:,.0f}'}),
                use_container_width=True
            )
            
            # Display editable donations table
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>עריכת נתוני תרומות</h2>", unsafe_allow_html=True)
            edited_donations = st.data_editor(
                donations_df,
                num_rows="dynamic",
                use_container_width=True,
                column_config=column_config,
                key="donations_donors_editor"
            )
            
            # Check if donations were changed
            if not edited_donations.equals(donations_df):
                st.session_state.changes_made['donations'] = True
            
            # Save edited donations data - only show if there are changes
            if st.session_state.changes_made['donations']:
                if st.button("שמור שינויים", type="primary"):
                    try:
                        with pd.ExcelWriter("omri.xlsx", engine="openpyxl", mode="a") as writer:
                            write_sheet('Donations', edited_donations)
                        
                        # Reset changes flag
                        st.session_state.changes_made['donations'] = False
                        st.success("השינויים נשמרו בהצלחה!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"שגיאה בשמירת השינויים: {str(e)}")
            else:
                st.info("אין שינויים לשמירה")
            
            # Display donations alerts
            st.subheader("התראות תרומות")
            donations_alerts = check_donations_alerts(donor_stats)
            if donations_alerts:
                for alert in donations_alerts:
                    st.warning(alert)
            else:
                st.success("אין התראות תרומות")
            
            # Display detailed donor information
            st.subheader("פרטי תורמים")
            donor_summary = donations_df.groupby("שם").agg({
                "שקלים": ["sum", "count", "mean"],
                "תאריך": ["min", "max"]
            }).reset_index()
            donor_summary.columns = ["שם", "סך תרומות", "מספר תרומות", "תרומה ממוצעת", "תרומה ראשונה", "תרומה אחרונה"]
            
            for _, donor in donor_summary.iterrows():
                with st.expander(f"{donor['שם']} - ₪{donor['סך תרומות']:,.0f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**סך תרומות:** ₪{donor['סך תרומות']:,.0f}")
                        st.write(f"**מספר תרומות:** {donor['מספר תרומות']}")
                        st.write(f"**תרומה ממוצעת:** ₪{donor['תרומה ממוצעת']:,.0f}")
                    with col2:
                        # Handle NaT values in date fields
                        first_donation = donor['תרומה ראשונה']
                        if pd.notna(first_donation):
                            st.write(f"**תרומה ראשונה:** {first_donation.strftime('%d/%m/%Y')}")
                        else:
                            st.write(f"**תרומה ראשונה:** לא מוגדר")
                        
                        last_donation = donor['תרומה אחרונה']
                        if pd.notna(last_donation):
                            st.write(f"**תרומה אחרונה:** {last_donation.strftime('%d/%m/%Y')}")
                        else:
                            st.write(f"**תרומה אחרונה:** לא מוגדר")
                    
                    # Display donor's donations history
                    st.subheader("היסטוריית תרומות")
                    donor_history = donations_df[donations_df["שם"] == donor["שם"]].sort_values("תאריך", ascending=False)
                    st.dataframe(
                        donor_history.style.format({
                            "שקלים": "₪{:,.0f}",
                            "תאריך": lambda x: x.strftime("%d/%m/%Y") if pd.notna(x) else "לא מוגדר"
                        }),
                        use_container_width=True
                    )
            
        with tab4:
            st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>ניהול אלמנות</h1>", unsafe_allow_html=True)
            
            # Display widow statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}")
            with col2:
                st.metric("סך תמיכה", f"₪{widow_stats['total_support']:,.2f}")
            with col3:
                st.metric("אלמנות ₪1,000", f"{widow_stats['support_1000_count']}")
            with col4:
                st.metric("אלמנות ₪2,000", f"{widow_stats['support_2000_count']}")
            
            # Display support distribution
            if widow_stats['support_distribution']:
                st.subheader("התפלגות תמיכה")
                support_df = pd.DataFrame([
                    {'שם': k, 'סכום': v}
                    for k, v in widow_stats['support_distribution'].items()
                ])
                st.dataframe(
                    support_df.style.format({'סכום': '₪{:,.0f}'}),
                    use_container_width=True
                )
            
            # Display widows support chart
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>תמיכה באלמנות</h2>", unsafe_allow_html=True)
            create_widows_support_chart(almanot_df)
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Display editable widows table
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>עריכת נתוני אלמנות</h2>", unsafe_allow_html=True)
            
            # Convert phone column to string to avoid type conflicts
            almanot_df_for_edit = almanot_df.copy()
            if 'טלפון' in almanot_df_for_edit.columns:
                almanot_df_for_edit['טלפון'] = almanot_df_for_edit['טלפון'].astype(str)
            
            # Create column config only for existing columns
            column_config = {}
            if "שם " in almanot_df_for_edit.columns:
                column_config["שם "] = st.column_config.TextColumn("שם", required=True)
            if "מייל" in almanot_df_for_edit.columns:
                column_config["מייל"] = st.column_config.TextColumn("מייל")
            if "טלפון" in almanot_df_for_edit.columns:
                column_config["טלפון"] = st.column_config.TextColumn("טלפון")
            if "תעודת זהות" in almanot_df_for_edit.columns:
                column_config["תעודת זהות"] = st.column_config.TextColumn("תעודת זהות")
            if "מספר ילדים" in almanot_df_for_edit.columns:
                column_config["מספר ילדים"] = st.column_config.NumberColumn("מספר ילדים", min_value=0)
            if "חללים" in almanot_df_for_edit.columns:
                column_config["חללים"] = st.column_config.CheckboxColumn("חללים")
            if "הערות" in almanot_df_for_edit.columns:
                column_config["הערות"] = st.column_config.TextColumn("הערות")
            if "תורם" in almanot_df_for_edit.columns:
                column_config["תורם"] = st.column_config.TextColumn("תורם")
            if "איש קשר לתרומה" in almanot_df_for_edit.columns:
                column_config["איש קשר לתרומה"] = st.column_config.TextColumn("איש קשר לתרומה")
            
            edited_almanot = st.data_editor(
                almanot_df_for_edit,
                num_rows="dynamic",
                use_container_width=True,
                column_config=column_config,
                key="widows_widows_editor"
            )
            
            # Check if widows were changed
            if not edited_almanot.equals(almanot_df_for_edit):
                st.session_state.changes_made['widows'] = True
            
            # Save edited widows data - only show if there are changes
            if st.session_state.changes_made['widows']:
                if st.button("שמור שינויים", type="primary"):
                    try:
                        write_sheet('Widows', edited_almanot)
                        
                        # Reset changes flag
                        st.session_state.changes_made['widows'] = False
                        st.success("השינויים נשמרו בהצלחה!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"שגיאה בשמירת השינויים: {str(e)}")
            else:
                st.info("אין שינויים לשמירה")
            
            # Display widows alerts
            st.subheader("התראות אלמנות")
            widows_alerts = check_widows_alerts(widow_stats)
            if widows_alerts:
                for alert in widows_alerts:
                    st.warning(alert)
            else:
                st.success("אין התראות אלמנות")
            
            # Display detailed widow information
            st.subheader("פרטי אלמנות")
            for _, widow in almanot_df.iterrows():
                with st.expander(f"{widow['שם ']} - ₪{widow['סכום חודשי']:,.0f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**מייל:** {widow['מייל']}")
                        st.write(f"**טלפון:** {widow['טלפון']}")
                        st.write(f"**תעודת זהות:** {widow['תעודת זהות']}")
                        st.write(f"**מספר ילדים:** {widow['מספר ילדים']}")
                    with col2:
                        # Handle NaT values in date fields
                        start_date = widow['חודש התחלה']
                        if pd.notna(start_date):
                            st.write(f"**חודש התחלה:** {start_date.strftime('%d/%m/%Y')}")
                        else:
                            st.write(f"**חודש התחלה:** לא מוגדר")
                        
                        st.write(f"**סכום חודשי:** ₪{widow['סכום חודשי']:,.0f}")
                        
                        # Handle checkbox values
                        if 'חללים' in widow and pd.notna(widow['חללים']):
                            st.write(f"**חללים:** {'כן' if widow['חללים'] else 'לא'}")
                        else:
                            st.write(f"**חללים:** לא מוגדר")
                        
                        st.write(f"**תורם:** {widow['תורם']}")
                        st.write(f"**איש קשר לתרומה:** {widow['איש קשר לתרומה']}")
                    
                    if pd.notna(widow['הערות']):
                        st.write(f"**הערות:** {widow['הערות']}")
        
        with tab5:
            st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>דוחות</h1>", unsafe_allow_html=True)
            
            # Report Generation Section
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>יצירת דוחות</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>דוחות מהירים</h3>", unsafe_allow_html=True)
                
                if st.button("📊 דוח חודשי מלא", use_container_width=True):
                    filename = generate_monthly_report(expenses_df, donations_df, almanot_df)
                    if filename:
                        show_success_message("דוח חודשי מלא נוצר בהצלחה!")
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
                        show_success_message("דוח תורמים מפורט נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח תורמים",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
                
                if st.button("👩 דוח אלמנות מפורט", use_container_width=True):
                    filename = generate_widows_report(almanot_df)
                    if filename:
                        show_success_message("דוח אלמנות מפורט נוצר בהצלחה!")
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
                        show_success_message("דוח תקציב מפורט נוצר בהצלחה!")
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="הורד דוח תקציב",
                                data=file.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )
            
            with col2:
                st.markdown("<h3 style='color: #4b5563; margin-bottom: 1rem;'>סטטיסטיקות מהירות</h3>", unsafe_allow_html=True)
                
                # Quick stats
                st.metric("סך תרומות", f"₪{total_don:,.0f}")
                st.metric("סך הוצאות", f"₪{sum_exp:,.0f}")
                st.metric("יתרה", f"₪{available:,.0f}")
                st.metric("מספר תורמים", f"{donor_stats['total_donors']:,}")
                st.metric("מספר אלמנות", f"{widow_stats['total_widows']:,}")
                st.metric("תמיכה חודשית", f"₪{widow_stats['total_support']:,.0f}")
            
            # Add spacing
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Custom Report Builder
            st.markdown("<h2 style='color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-bottom: 2rem;'>בניית דוח מותאם</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                report_type = st.selectbox(
                    "סוג דוח",
                    ["דוח חודשי", "דוח תורמים", "דוח אלמנות", "דוח תקציב"]
                )
            
            with col2:
                date_from = st.date_input("מתאריך", value=donations_df['תאריך'].min())
            
            with col3:
                date_to = st.date_input("עד תאריך", value=donations_df['תאריך'].max())
            
            if st.button("יצור דוח מותאם", type="primary"):
                # Filter data by date range
                filtered_donations = donations_df[
                    (donations_df['תאריך'] >= pd.Timestamp(date_from)) & 
                    (donations_df['תאריך'] <= pd.Timestamp(date_to))
                ]
                filtered_expenses = expenses_df[
                    (expenses_df['תאריך'] >= pd.Timestamp(date_from)) & 
                    (expenses_df['תאריך'] <= pd.Timestamp(date_to))
                ]
                
                if report_type == "דוח חודשי":
                    filename = generate_monthly_report(filtered_expenses, filtered_donations, almanot_df)
                elif report_type == "דוח תורמים":
                    filename = generate_donor_report(filtered_donations)
                elif report_type == "דוח אלמנות":
                    filename = generate_widows_report(almanot_df)
                elif report_type == "דוח תקציב":
                    filename = generate_budget_report(filtered_expenses, filtered_donations)
                
                if filename:
                    show_success_message(f"{report_type} נוצר בהצלחה!")
                    with open(filename, "rb") as file:
                        st.download_button(
                            label=f"הורד {report_type}",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf"
                        )

        with tab6:
            st.markdown("<h1 style='text-align: center; color: #2563eb; margin-bottom: 1rem;'>מפת קשרים - תרומות ואלמנות</h1>", unsafe_allow_html=True)
            
            try:
                # יצירת רשימת צמתים וקשתות עבור streamlit-agraph
                nodes = []
                edges = []
                
                # צבעים תואמים לעיצוב
                donor_color = "#2563eb"  # כחול עיקרי
                widow_color = "#f43f5e"  # ורוד-אדום
                highlight_color = "#a21caf"  # סגול כהה להדגשה
                edge_color_1000 = "#fbbf24"  # צהוב רך
                edge_color_2000 = "#2563eb"  # כחול
                edge_color_other = "#a3a3a3"  # אפור
                
                # הוספת תורמים כ-nodes
                # ניקוי נתונים - הסרת שורות עם שמות תורמים ריקים
                donations_df_clean = donations_df.dropna(subset=['שם'])
                donations_df_clean = donations_df_clean[donations_df_clean['שם'] != '']
                donations_df_clean = donations_df_clean[donations_df_clean['שם'].str.strip() != '']
                
                # הדפסת מידע על ניקוי הנתונים
                print(f"DEBUG: Original donations count: {len(donations_df)}")
                print(f"DEBUG: Cleaned donations count: {len(donations_df_clean)}")
                print(f"DEBUG: Removed {len(donations_df) - len(donations_df_clean)} rows with empty donor names")
                
                donors = donations_df_clean['שם'].unique()
                print(f"DEBUG: Unique donors after cleaning: {len(donors)}")
                print(f"DEBUG: Donors: {list(donors)}")
                
                # מיפוי אוטומטי של שמות תורמים
                def create_donor_mapping():
                    """יצירת מיפוי אוטומטי בין שמות תורמים"""
                    mapping = {}
                    
                    # רשימת מיפויים ידניים ידועים
                    manual_mappings = {
                        'פלייטיקה': 'פלייטק',
                        'שפע זיכיונות ': 'שפע זיכיונות',
                        'סופר פליי ': 'סופר פליי',
                        'מייקרוסופט ': 'מייקרוסופט',
                        'ווקמי בעמ\xa0': 'ווקמי בעמ',
                        'א.ל. סקיישילד': 'סקיישילד',
                        'ישי מור': 'ישי מר',
                        'פרידלנד מאיר': 'מאיר פרידלנד',
                        'מולודצקי איליה': 'אליה מולודצקי',
                        'יהלומי יורם דבש': 'יורם דבש',
                        'הלפרין קובי': 'קובי הלפרין',
                        'איליון דינמיקס': 'איליון',
                        'פאראגון פתרונות': 'פאראגון',
                        'שפע זיכיונות ': 'שפע זיכיונות',
                        'פלייטק+גלים': 'גלים',
                        'יתרת זכות': 'יתרת זכות',
                        'יונתן ארז': 'יונתן ארז',
                        'דורון נאור': 'דורון נאור'
                    }
                    
                    # הוספת מיפויים ידניים
                    for old_name, new_name in manual_mappings.items():
                        mapping[old_name] = new_name
                    
                    return mapping
                
                # יצירת המיפוי
                donor_mapping = create_donor_mapping()
                print(f"DEBUG: Donor mapping created: {donor_mapping}")
                
                # עדכון שמות תורמים בקובץ האלמנות
                almanot_df_clean = almanot_df.copy()
                almanot_df_clean['תורם'] = almanot_df_clean['תורם'].replace(donor_mapping)
                
                # עדכון שמות תורמים בקובץ התרומות
                donations_df_clean['שם'] = donations_df_clean['שם'].replace(donor_mapping)
                
                # עדכון רשימת התורמים
                donors = donations_df_clean['שם'].unique()
                print(f"DEBUG: Unique donors after mapping: {len(donors)}")
                
                # --- יצירת קשרים אמיתיים: רק אלמנות (סכום חודשי 1000 או 2000) עם תורם ---
                connections_count = 0
                widow_to_donor_mapping = {}
                donor_connections = {}
                
                # סינון אלמנות אמיתיות
                real_widows_df = almanot_df_clean[(almanot_df_clean['סכום חודשי'].isin([1000, 2000])) & (almanot_df_clean['תורם'].notna()) & (almanot_df_clean['תורם'] != '')]
                
                # הדפסת מידע על האלמנות
                print(f"DEBUG: Total widows in almanot_df: {len(almanot_df)}")
                print(f"DEBUG: Widows with monthly amount 1000 or 2000: {len(almanot_df[almanot_df['סכום חודשי'].isin([1000, 2000])])}")
                print(f"DEBUG: Widows with donor: {len(almanot_df[almanot_df['תורם'].notna()])}")
                print(f"DEBUG: Real widows (with amount and donor): {len(real_widows_df)}")
                
                # הדפסת דוגמאות של אלמנות עם תורמים
                print("DEBUG: Sample widows with donors:")
                for i, (_, row) in enumerate(real_widows_df.head(10).iterrows()):
                    print(f"  {i+1}. {row['שם ']} -> {row['תורם']} (₪{row['סכום חודשי']})")
                
                # הדפסת אלמנות ללא תורם
                widows_without_donor = almanot_df_clean[(almanot_df_clean['סכום חודשי'].isin([1000, 2000])) & (almanot_df_clean['תורם'].isna())]
                print(f"DEBUG: Widows without donor: {len(widows_without_donor)}")
                for i, (_, row) in enumerate(widows_without_donor.head(5).iterrows()):
                    print(f"  {i+1}. {row['שם ']} (₪{row['סכום חודשי']}) - NO DONOR")
                
                # יצירת מיפוי חיבורים
                for i, widow_row in real_widows_df.iterrows():
                    widow_name = widow_row['שם ']
                    donor_name = widow_row['תורם']
                    
                    widow_to_donor_mapping[widow_name] = donor_name
                    if donor_name not in donor_connections:
                        donor_connections[donor_name] = 0
                    donor_connections[donor_name] += 1
                
                # בדיקה אילו תורמים יש להם תרומות בפועל
                donors_with_actual_donations = set(donations_df_clean['שם'].unique())
                
                # זיהוי תורמים עם קשרים (רק כאלה שיש להם תרומות בפועל)
                donors_with_connections = set(donor_connections.keys()) - {'nan'}
                donors_with_connections = donors_with_connections.intersection(donors_with_actual_donations)
                donors_without_connections = set(donors) - donors_with_connections
                
                print(f"DEBUG: Donors with actual donations: {len(donors_with_actual_donations)}")
                print(f"DEBUG: Donors with connections: {len(donors_with_connections)}")
                print(f"DEBUG: Donors without connections: {len(donors_without_connections)}")
                print(f"DEBUG: Donors in mapping but no actual donations: {set(donor_connections.keys()) - {'nan'} - donors_with_actual_donations}")
                
                # יצירת מיפוי של מספר חיבורים לגודל צומת
                connection_size_mapping = {}
                max_connections = max(donor_connections.values()) if donor_connections else 0
                
                # יצירת מיפוי אחיד של גודל לפי מספר חיבורים
                for connection_count in range(1, max_connections + 1):
                    base_size = 20  # גודל בסיסי קטן יותר
                    connection_bonus = connection_count * 4  # תוספת אחידה לכל חיבור
                    connection_size_mapping[connection_count] = base_size + connection_bonus
                
                print(f"DEBUG: Connection size mapping: {connection_size_mapping}")
                print(f"DEBUG: Donor connections: {donor_connections}")
                
                donor_nodes = {}
                
                # הוספת תורמים עם קשרים במרכז במעגל
                center_x = 0
                center_y = 0
                donors_with_connections_list = list(donors_with_connections)
                for i, donor in enumerate(donors_with_connections_list):
                    node_id = f"donor_{donor}"
                    donor_nodes[donor] = node_id
                    
                    # חישוב גודל הצומת לפי מספר החיבורים
                    connection_count = donor_connections.get(donor, 1)
                    node_size = connection_size_mapping.get(connection_count, 20)
                    
                    # חישוב מיקום במעגל
                    angle = (i / len(donors_with_connections_list)) * 2 * 3.14159
                    radius = 200
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                    nodes.append(
                        Node(
                            id=node_id,
                            label=donor,
                            size=node_size,
                            color=donor_color,
                            shape="circle",
                            x=x,
                            y=y
                        )
                    )
                
                # הוספת תורמים ללא קשרים משמאל
                left_x = -600
                left_y = 0
                donors_without_connections_list = list(donors_without_connections)
                for i, donor in enumerate(donors_without_connections_list):
                    node_id = f"donor_{donor}"
                    donor_nodes[donor] = node_id
                    nodes.append(
                        Node(
                            id=node_id,
                            label=donor,
                            size=20,
                            color="#9ca3af",  # אפור לתורמים ללא קשרים
                            shape="circle",
                            x=left_x,
                            y=left_y + (i * 40) - (len(donors_without_connections_list) * 20)
                        )
                    )
                
                # הוספת אלמנות כ-nodes
                widows = almanot_df_clean['שם '].unique()
                widow_nodes = {}
                
                # זיהוי אלמנות עם קשרים
                widows_with_connections = set(widow_to_donor_mapping.keys())
                widows_without_connections = set(widows) - widows_with_connections
                
                # בדיקה אילו אלמנות יש להן קשרים בפועל (רק אם התורם קיים בפועל)
                actual_widows_with_connections = set()
                for widow_name, donor_name in widow_to_donor_mapping.items():
                    if donor_name in donors_with_actual_donations:
                        actual_widows_with_connections.add(widow_name)
                
                widows_with_connections = actual_widows_with_connections
                widows_without_connections = set(widows) - widows_with_connections
                
                print(f"DEBUG: Widows with connections: {len(widows_with_connections)}")
                print(f"DEBUG: Widows without connections: {len(widows_without_connections)}")
                print(f"DEBUG: Widows with actual connections: {len(widows_with_connections)}")
                print(f"DEBUG: Widows without actual connections: {len(widows_without_connections)}")
                print(f"DEBUG: Widows in mapping but no actual connections: {set(widow_to_donor_mapping.keys()) - actual_widows_with_connections}")
                
                # הוספת אלמנות עם קשרים מימין
                right_x = 600
                right_y = 0
                widows_with_connections_list = list(widows_with_connections)
                for i, widow in enumerate(widows_with_connections_list):
                    node_id = f"widow_{widow}"
                    widow_nodes[widow] = node_id
                    nodes.append(
                        Node(
                            id=node_id,
                            label=widow,
                            size=25,
                            color=widow_color,
                            shape="square",
                            x=right_x,
                            y=right_y + (i * 40) - (len(widows_with_connections_list) * 20)
                        )
                    )
                
                # הוספת אלמנות ללא קשרים מימין יותר
                far_right_x = 800
                far_right_y = 0
                widows_without_connections_list = list(widows_without_connections)
                for i, widow in enumerate(widows_without_connections_list):
                    node_id = f"widow_{widow}"
                    widow_nodes[widow] = node_id
                    nodes.append(
                        Node(
                            id=node_id,
                            label=widow,
                            size=20,
                            color="#9ca3af",  # אפור לאלמנות ללא קשרים
                            shape="square",
                            x=far_right_x,
                            y=far_right_y + (i * 40) - (len(widows_without_connections_list) * 20)
                        )
                    )
                
                # הדפסת כל הצמתים שנוצרים
                print("DEBUG: Nodes created:")
                for node in nodes:
                    warn = ""
                    if not node.label or str(node.label).strip() == "" or str(node.label).lower() == "nan" or str(node.label).startswith("קשר"):
                        warn = " <== WARNING: suspicious label!"
                    print(f"  id={node.id}, label={node.label!r}, shape={node.shape}, color={node.color}{warn}")
                
                # יצירת הקשרים
                for i, widow_row in real_widows_df.iterrows():
                    widow_name = widow_row['שם ']
                    donor_name = widow_row['תורם']
                    
                    # בדיקה אם התורם קיים ברשימת התורמים
                    if donor_name in donor_nodes and widow_name in widow_nodes:
                        # חפש את התרומה האחרונה של התורם הזה
                        donor_donations = donations_df_clean[donations_df_clean['שם'] == donor_name]
                        if not donor_donations.empty:
                            last_row = donor_donations.sort_values('תאריך', ascending=False).iloc[0]
                            last_amount = last_row['שקלים']
                            last_date = last_row['תאריך']
                            donation_k = last_amount / 1000
                            edge_width = max(1, min(8, donation_k / 10))
                            if last_amount == 1000:
                                edge_color = edge_color_1000
                            elif last_amount == 2000:
                                edge_color = edge_color_2000
                            else:
                                edge_color = edge_color_other
                            edges.append(
                                Edge(
                                    source=donor_nodes[donor_name],
                                    target=widow_nodes[widow_name],
                                    color=edge_color,
                                    width=edge_width,
                                    title=f"{donor_name} → {widow_name}: {donation_k:.1f}k ₪ ({last_date.strftime('%d/%m/%Y') if pd.notna(last_date) else 'תאריך לא מוגדר'})"
                                )
                            )
                            connections_count += 1
                        else:
                            print(f"DEBUG: No donations found for donor '{donor_name}'")
                    else:
                        if donor_name not in donor_nodes:
                            print(f"DEBUG: Donor '{donor_name}' not found in donations data")
                        if widow_name not in widow_nodes:
                            print(f"DEBUG: Widow '{widow_name}' not found in widows data")
                
                # הדפסת מידע על חיבורים וגודל צמתים (לבדיקה)
                print(f"DEBUG: Connection size mapping: {connection_size_mapping}")
                print(f"DEBUG: Donor connections: {donor_connections}")
                
                # --- חיפוש ידני מעל הגרף ---
                all_names = list(donors) + list(widows)
                selected_name = st.selectbox("חפש תורם/אלמנה להדגשה בגרף", options=["בחר שם להדגשה..."] + sorted(all_names), index=0)
                
                # הדגשת הצומת שנבחרה
                if selected_name != "בחר שם להדגשה...":
                    for node in nodes:
                        if node.label == selected_name:
                            node.color = highlight_color
                            node.size = node.size + 5
                            break
                    st.info(f"🔎 בחרת להדגיש את: {selected_name}. הצומת מודגשת בצבע סגול.")
                
                # הגדרת תצורת הגרף
                config = Config(
                    height=800,
                    width=1200,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightNearest=True,
                    collapsible=False,
                    node={'labelProperty': 'label'},
                    link={'labelProperty': 'label', 'renderLabel': True},
                    d3={'gravity': -100, 'linkLength': 100},
                    stabilization=True,
                    fit=True,
                    # הוספת פונקציונליות עריכה
                    manipulation={
                        'enabled': True,
                        'initiallyActive': False,
                        'addNode': False,  # לא מאפשר יצירת צמתים חדשים
                        'addEdge': True,
                        'editNode': False,  # לא מאפשר עריכת צמתים
                        'editEdge': True,
                        'deleteNode': False,  # לא מאפשר מחיקת צמתים
                        'deleteEdge': True,
                        'controlNodeStyle': {
                            'shape': 'circle',
                            'size': 20,
                            'color': {'background': '#4ade80', 'border': '#22c55e'},
                            'font': {'color': '#ffffff', 'size': 12}
                        }
                    }
                )
                
                # הצגת הגרף
                agraph(nodes=nodes, edges=edges, config=config)
                
                # כפתור להפעלת/כיבוי מצב עריכה
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    edit_mode = st.toggle("✏️ מצב עריכה", key="edit_mode_toggle")
                    if edit_mode:
                        st.info("🔧 **מצב עריכה פעיל**: גרור צמתים ליצירת קשרים חדשים, לחץ על קשרים לעריכה, או לחץ על צמתים למחיקה.")
                    else:
                        st.info("👆 **מצב צפייה**: לחץ על צמתים וקשרים לפרטים נוספים.")
                
                # כפתורי פעולה מהירה במצב עריכה
                if edit_mode:
                    st.markdown("### ⚡ פעולות מהירות")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("🔄 רענן גרף", key="refresh_graph"):
                            st.rerun()
                    
                    with col2:
                        if st.button("💾 שמור שינויים", key="save_changes"):
                            # שמירת כל השינויים הזמניים
                            if 'temp_changes' in st.session_state and st.session_state.temp_changes:
                                for change in st.session_state.temp_changes:
                                    if change['action'] == 'add':
                                        update_connection_in_data(change['donor'], change['widow'], change['amount'])
                                    elif change['action'] == 'edit':
                                        update_connection_in_data(change['donor'], change['widow'], change['amount'])
                                    elif change['action'] == 'delete':
                                        remove_connection_from_data(change['donor'], change['widow'])
                                
                                # ניקוי השינויים הזמניים
                                st.session_state.temp_changes = []
                                st.success("✅ כל השינויים נשמרו בהצלחה!")
                                st.rerun()
                            else:
                                st.info("ℹ️ אין שינויים לשמירה")
                    
                    with col3:
                        if st.button("📊 סטטיסטיקות", key="show_stats"):
                            pending_changes = len(st.session_state.get('temp_changes', []))
                            st.info(f"📈 **סטטיסטיקות נוכחיות**: {len(donors)} תורמים, {len(widows)} אלמנות, {len(edges)} קשרים פעילים, {pending_changes} שינויים ממתינים")
                    
                    with col4:
                        if st.button("❌ ביטול עריכה", key="cancel_edit"):
                            # ביטול כל השינויים הזמניים
                            if 'temp_changes' in st.session_state:
                                del st.session_state.temp_changes
                            st.session_state.edit_mode_toggle = False
                            st.rerun()
                
                # הוראות שימוש
                with st.expander("📖 הוראות שימוש במערכת העריכה"):
                    st.markdown("""
                    ### איך לערוך קשרים ישירות על הגרף:
                    
                    **🔧 מצב עריכה:**
                    1. **הפעל את כפתור "מצב עריכה"** למעלה
                    2. **גרור צמתים** - גרור תורם לאלמנה ליצירת קשר חדש
                    3. **לחץ על קשרים** - לעריכת סכום התרומה
                    4. **הדגשת אלמנות זמינות** - אלמנות ללא תורם יודגשו בצבע שונה
                    
                    **👆 מצב צפייה:**
                    - לחץ על צמתים וקשרים לפרטים נוספים
                    - השתמש בחיפוש למעלה להדגשת צמתים
                    
                    **💾 שמירה ידנית:**
                    - השינויים נשמרים רק בלחיצה על "שמור שינויים"
                    - השתמש ב"ביטול עריכה" לביטול כל השינויים
                    - התרומות מתעדכנות ב-`omri.xlsx`
                    - הקשרים מתעדכנים ב-`almanot.xlsx`
                    
                    **⚠️ הגבלות:**
                    - לא ניתן ליצור צמתים חדשים
                    - לא ניתן לחבר לאלמנה שכבר יש לה תורם
                    - לא ניתן למחוק צמתים קיימים
                    """)
                
                # JavaScript לטיפול באירועי עריכה
                if edit_mode:
                    st.markdown("""
                    <script>
                    // פונקציה לטיפול באירועי עריכה
                    function setupGraphEditing() {
                        // רשימת אלמנות עם תורמים (למניעת חיבורים כפולים)
                        const widowsWithDonors = new Set();
                        network.body.data.edges.forEach(edge => {
                            if (edge.to.startsWith('widow_')) {
                                widowsWithDonors.add(edge.to);
                            }
                        });
                        
                        // הדגשת אלמנות זמינות (ללא תורם)
                        network.body.data.nodes.forEach(node => {
                            if (node.id.startsWith('widow_') && !widowsWithDonors.has(node.id)) {
                                // הדגשת אלמנות זמינות בצבע שונה
                                node.color = '#10b981'; // צבע ירוק לאלמנות זמינות
                                node.size = node.size + 5;
                                network.body.data.nodes.update(node);
                            }
                        });
                        
                        // אירוע יצירת קשר חדש
                        network.on('addEdge', function(data) {
                            const fromNode = data.from;
                            const toNode = data.to;
                            
                            // בדיקה שהקשר הוא בין תורם לאלמנה
                            if (fromNode.startsWith('donor_') && toNode.startsWith('widow_')) {
                                const donorName = fromNode.replace('donor_', '');
                                const widowName = toNode.replace('widow_', '');
                                
                                // בדיקה שהאלמנה לא מחוברת כבר
                                if (widowsWithDonors.has(toNode)) {
                                    alert('אלמנה זו כבר מחוברת לתורם אחר!');
                                    network.body.data.edges.remove(data.id);
                                    return;
                                }
                                
                                // הצגת דיאלוג לבחירת סכום
                                const amount = prompt('בחר סכום התרומה (בשקלים):', '1000');
                                if (amount && !isNaN(amount)) {
                                    // עדכון הקשר עם הסכום החדש
                                    const edge = network.body.data.edges.get(data.id);
                                    if (edge) {
                                        edge.title = donorName + ' → ' + widowName + ': ' + (amount/1000) + 'k ₪';
                                        edge.color = amount >= 2000 ? '#3b82f6' : '#fbbf24';
                                        edge.width = Math.max(1, Math.min(8, amount / 1000 / 10));
                                        network.body.data.edges.update(edge);
                                        
                                        // עדכון צבע התורם לכחול (עם קשרים)
                                        const donorNode = network.body.data.nodes.get(fromNode);
                                        if (donorNode) {
                                            donorNode.color = '#2563eb';
                                            network.body.data.nodes.update(donorNode);
                                        }
                                        
                                        // עדכון צבע האלמנה לאדום (עם קשרים)
                                        const widowNode = network.body.data.nodes.get(toNode);
                                        if (widowNode) {
                                            widowNode.color = '#f43f5e';
                                            widowNode.size = Math.max(20, widowNode.size - 5);
                                            network.body.data.nodes.update(widowNode);
                                        }
                                        
                                        // הוספה לרשימת אלמנות עם תורמים
                                        widowsWithDonors.add(toNode);
                                    }
                                    
                                    // שליחת הנתונים לשרת
                                    fetch('/update_connection', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({
                                            donor: donorName,
                                            widow: widowName,
                                            amount: parseInt(amount),
                                            action: 'add'
                                        })
                                    }).then(() => {
                                        console.log('Connection updated successfully');
                                    });
                                } else {
                                    // ביטול הקשר אם לא נבחר סכום
                                    network.body.data.edges.remove(data.id);
                                }
                            }
                        });
                        
                        // אירוע מחיקת קשר
                        network.on('deleteEdge', function(data) {
                            const edgeId = data.edges[0];
                            const edge = network.body.data.edges.get(edgeId);
                            
                            if (edge) {
                                const fromNode = edge.from;
                                const toNode = edge.to;
                                
                                if (fromNode.startsWith('donor_') && toNode.startsWith('widow_')) {
                                    const donorName = fromNode.replace('donor_', '');
                                    const widowName = toNode.replace('widow_', '');
                                    
                                    if (confirm('האם אתה בטוח שברצונך למחוק את הקשר הזה?')) {
                                        // הסרה מרשימת אלמנות עם תורמים
                                        widowsWithDonors.delete(toNode);
                                        
                                        // עדכון צבע האלמנה לירוק (זמינה)
                                        const widowNode = network.body.data.nodes.get(toNode);
                                        if (widowNode) {
                                            widowNode.color = '#10b981';
                                            widowNode.size = widowNode.size + 5;
                                            network.body.data.nodes.update(widowNode);
                                        }
                                        
                                        fetch('/update_connection', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json',
                                            },
                                            body: JSON.stringify({
                                                donor: donorName,
                                                widow: widowName,
                                                action: 'delete'
                                            })
                                        }).then(() => {
                                            console.log('Connection deleted successfully');
                                        });
                                    }
                                }
                            }
                        });
                        
                        // אירוע עריכת קשר
                        network.on('editEdge', function(data) {
                            const edge = data.edge;
                            const fromNode = edge.from;
                            const toNode = edge.to;
                            
                            if (fromNode.startsWith('donor_') && toNode.startsWith('widow_')) {
                                const donorName = fromNode.replace('donor_', '');
                                const widowName = toNode.replace('widow_', '');
                                
                                const newAmount = prompt('ערוך סכום התרומה (בשקלים):', '1000');
                                if (newAmount && !isNaN(newAmount)) {
                                    edge.title = donorName + ' → ' + widowName + ': ' + (newAmount/1000) + 'k ₪';
                                    edge.color = newAmount >= 2000 ? '#3b82f6' : '#fbbf24';
                                    edge.width = Math.max(1, Math.min(8, newAmount / 1000 / 10));
                                    network.body.data.edges.update(edge);
                                    
                                    fetch('/update_connection', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({
                                            donor: donorName,
                                            widow: widowName,
                                            amount: parseInt(newAmount),
                                            action: 'edit'
                                        })
                                    }).then(() => {
                                        console.log('Connection edited successfully');
                                    });
                                }
                            }
                        });
                    }
                    
                    // הפעלת הפונקציה כשהדף נטען
                    document.addEventListener('DOMContentLoaded', setupGraphEditing);
                    </script>
                    """, unsafe_allow_html=True)
                
                # טיפול בעדכוני קשרים
                if 'pending_connection_update' in st.session_state:
                    update_data = st.session_state.pending_connection_update
                    donor_name = update_data.get('donor')
                    widow_name = update_data.get('widow')
                    action = update_data.get('action')
                    amount = update_data.get('amount', 1000)
                    
                    if action == 'add':
                        # הוספה לרשימת השינויים הזמניים
                        if 'temp_changes' not in st.session_state:
                            st.session_state.temp_changes = []
                        st.session_state.temp_changes.append({
                            'action': 'add',
                            'donor': donor_name,
                            'widow': widow_name,
                            'amount': amount
                        })
                        st.success(f"✅ קשר חדש נוסף: {donor_name} → {widow_name} ({amount:,} ₪)")
                    elif action == 'edit':
                        # עדכון ברשימת השינויים הזמניים
                        if 'temp_changes' not in st.session_state:
                            st.session_state.temp_changes = []
                        st.session_state.temp_changes.append({
                            'action': 'edit',
                            'donor': donor_name,
                            'widow': widow_name,
                            'amount': amount
                        })
                        st.success(f"✅ קשר עודכן: {donor_name} → {widow_name} ({amount:,} ₪)")
                    elif action == 'delete':
                        # הוספת מחיקה לרשימת השינויים הזמניים
                        if 'temp_changes' not in st.session_state:
                            st.session_state.temp_changes = []
                        st.session_state.temp_changes.append({
                            'action': 'delete',
                            'donor': donor_name,
                            'widow': widow_name
                        })
                        st.success(f"✅ קשר נמחק: {donor_name} → {widow_name}")
                    
                    # ניקוי הנתונים הזמניים
                    del st.session_state.pending_connection_update
                    st.rerun()
            except Exception as e:
                logging.error(f"Error creating network graph: {str(e)}")
                logging.error(traceback.format_exc())
                st.error("שגיאה ביצירת מפת הקשרים. אנא נסה שוב.")
        
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        logging.error(traceback.format_exc())
        st.error("שגיאה בהצגת הדשבורד. אנא נסה לרענן את הדף.")

if __name__ == "__main__":
    main()
