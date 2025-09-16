#!/usr/bin/env python3
"""
Omri Association Dashboard - COMPLETE VERSION
All sections and improvements we built together
"""

import streamlit as st
import pandas as pd
import logging
import plotly.express as px
import plotly.graph_objects as go
from google_sheets_io import load_all_data, check_service_account_validity
from data_processing import calculate_monthly_budget, calculate_donor_statistics, calculate_widow_statistics
from data_visualization import create_monthly_trends, create_budget_distribution_chart, create_donor_contribution_chart, create_widows_support_chart
from ui.dashboard_sections import (
    create_overview_section, create_budget_section, create_donors_section, 
    create_widows_section, create_widows_table_section, create_network_section, 
    create_residential_breakdown_section
)

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

# Custom CSS for better styling
st.markdown("""
<style>
/* RTL Support */
[data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
}

/* Hebrew font support */
* {
    font-family: "Segoe UI", "Noto Sans Hebrew", "Arial Hebrew", sans-serif;
}

/* Network graph styling */
.network-graph-wrapper {
    width: 100% !important;
    height: 1000px !important;
}

.stAgraph {
    width: 100% !important;
    height: 1000px !important;
}

/* Force all text in network view to be black */
.stPlotlyChart, .stPlotlyChart * {
    color: #000000 !important;
}

/* Network specific text colors */
.vis-network, .vis-network * {
    color: #000000 !important;
}

/* Edge labels */
.vis-edge-label {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* Make network use full available width */
.stPlotlyChart {
    width: 100% !important;
    max-width: none !important;
}

/* Ensure the agraph container uses full width */
.stPlotlyChart > div {
    width: 100% !important;
    max-width: none !important;
}
</style>
""", unsafe_allow_html=True)

def create_section_header(title: str, icon: str = ""):
    """Create a consistent section header"""
    icon_text = f"{icon} " if icon else ""
    st.markdown(f"### {icon_text}{title}")

def create_metric_row(metrics: list, columns: int = 4):
    """Create a row of metrics"""
    cols = st.columns(len(metrics))
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=metric.get('label', ''),
                value=metric.get('value', ''),
                help=metric.get('help', '')
            )

def get_sample_data():
    """Generate sample data for testing when Google Sheets is not available"""
    # Sample expenses data
    expenses_data = {
        'תאריך': pd.date_range('2024-01-01', periods=20, freq='D'),
        'שם': ['רוני קדמי', 'הראל פנסיה', 'דוד כהן', 'שרה לוי', 'משה ישראלי'] * 4,
        'שקלים': [18916, 6249, 15000, 8500, 12000] * 4
    }
    expenses_df = pd.DataFrame(expenses_data)
    
    # Sample donations data
    donations_data = {
        'תאריך': pd.date_range('2024-01-01', periods=15, freq='D'),
        'שם': ['אלבין שמואל', 'וולקס מיכאל וניל', 'דורון נאור', 'אמ רייסל ייעוץ', 'ישי מור'] * 3,
        'שקלים': [72000, 3600, 15000, 25000, 18000] * 3
    }
    donations_df = pd.DataFrame(donations_data)
    
    # Sample investors data
    investors_data = {
        'תאריך': pd.date_range('2024-01-01', periods=10, freq='D'),
        'שם': ['איליון דינמיקס', 'ישי מור', 'דורון נאור', 'אמ רייסל ייעוץ', 'וולקס מיכאל'] * 2,
        'שקלים': [2000, 18000, 12000, 15000, 8000] * 2
    }
    investors_df = pd.DataFrame(investors_data)
    
    # Sample widows data
    widows_data = {
        'שם ': ['זהר הופמן', 'אביה סלוטקי', 'רחל כהן', 'מירי לוי', 'שרה ישראלי'] * 18,
        'מייל': ['zohary3@gmail.com', 'avia911@gmail.com', 'rachel@email.com', 'miri@email.com', 'sarah@email.com'] * 18,
        'טלפון': ['542476617', '587654911', '0501234567', '0529876543', '0541111111'] * 18,
        'תעודת זהות': [''] * 90,
        'מספר ילדים': ['2', '1', '3', '2', '4'] * 18,
        'חודש התחלה': pd.date_range('2024-01-01', periods=90, freq='D'),
        'סכום חודשי': ['1000', '1500', '2000', '1200', '1800'] * 18,
        'חללים': ['יצהר הופמן', 'ישי סלוטקי', 'דוד כהן', 'אברהם לוי', 'משה ישראלי'] * 18,
        'הערות': [''] * 90,
        'תורם': ['אמ רייסל ייעוץ', 'דורון נאור', 'אלבין שמואל', 'וולקס מיכאל', 'ישי מור'] * 18,
        'איש קשר לתרומה': ['איתן 0547308070', 'דורון 0544989989', 'רחל 0501234567', 'מירי 0529876543', 'שרה 0541111111'] * 18,
        'עיר': ['תל אביב', 'ירושלים', 'חיפה', 'באר שבע', 'נתניה'] * 18
    }
    almanot_df = pd.DataFrame(widows_data)
    
    return expenses_df, donations_df, investors_df, almanot_df

def main():
    """Main dashboard function"""
    # Header
    st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>מערכת ניהול עמותת עמרי</h1>", unsafe_allow_html=True)
    
    # Check Google Sheets connection
    if not check_service_account_validity():
        st.error("❌ לא ניתן להתחבר ל-Google Sheets. נא לבדוק את הגדרות החיבור.")
        return
    
    # Load data
    try:
        # Try to load real data from Google Sheets
        all_data = load_all_data()
        
        if all_data and len(all_data) > 0:
            expenses_df = all_data.get('Expenses', pd.DataFrame())
            donations_df = all_data.get('Donations', pd.DataFrame())
            investors_df = all_data.get('Investors', pd.DataFrame())
            almanot_df = all_data.get('Almanot', pd.DataFrame())
            
            # Show success message
            st.toast("✅ נתונים אמיתיים - נטענו בהצלחה מ-Google Sheets", icon="📊")
        else:
            # Fallback to sample data
            st.warning("⚠️ לא ניתן לטעון נתונים מ-Google Sheets. מציג נתונים לדוגמה.")
            expenses_df, donations_df, investors_df, almanot_df = get_sample_data()
    
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת הנתונים: {str(e)}")
        logger.error(f"Dashboard error: {e}")
        
        # Show debug information
        st.subheader("🔍 מידע דיבוג")
        st.write(f"Error details: {e}")
        
        # Fallback to sample data
        expenses_df, donations_df, investors_df, almanot_df = get_sample_data()
    
    # Process data for statistics
    try:
        budget_status = calculate_monthly_budget(expenses_df, donations_df)
        donor_stats = calculate_donor_statistics(donations_df)
        widow_stats = calculate_widow_statistics(almanot_df)
    except Exception as e:
        st.error(f"❌ שגיאה בעיבוד נתונים: {str(e)}")
        logger.error(f"Data processing error: {e}")
        # Create empty stats
        budget_status = {}
        donor_stats = {'total_donors': 0}
        widow_stats = {'total_widows': 0, 'total_support': 0}
    
    # Create ALL the tabs we built together
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 דף הבית", 
        "💰 תקציב", 
        "👥 תורמים", 
        "👩 אלמנות", 
        "🕸️ מפת קשרים", 
        "🏘️ אזורי מגורים"
    ])
    
    with tab1:
        create_section_header("🏠 דף הבית")
        
        # Overview section
        create_overview_section(expenses_df, donations_df, donor_stats, widow_stats)
        
        # Recent activity
        st.markdown("#### 📋 פעילות אחרונה")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎁 תרומות אחרונות**")
            if not donations_df.empty:
                recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                for _, donation in recent_donations.iterrows():
                    donation_date = donation['תאריך']
                    if pd.notna(donation_date):
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} ({donation_date.strftime('%d/%m/%Y')})")
                    else:
                        st.write(f"**{donation['שם']}** - ₪{donation['שקלים']:,.0f} (תאריך לא מוגדר)")
            else:
                st.info("אין תרומות להצגה")
        
        with col2:
            st.markdown("**💸 הוצאות אחרונות**")
            if not expenses_df.empty:
                recent_expenses = expenses_df.sort_values('תאריך', ascending=False).head(5)
                for _, expense in recent_expenses.iterrows():
                    expense_date = expense['תאריך']
                    if pd.notna(expense_date):
                        st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} ({expense_date.strftime('%d/%m/%Y')})")
                    else:
                        st.write(f"**{expense['שם']}** - ₪{expense['שקלים']:,.0f} (תאריך לא מוגדר)")
            else:
                st.info("אין הוצאות להצגה")
        
        # Charts
        st.markdown("#### 📈 גרפים")
        col1, col2 = st.columns(2)
        
        with col1:
            if not expenses_df.empty and not donations_df.empty:
                monthly_trends_fig = create_monthly_trends(expenses_df, donations_df)
                if monthly_trends_fig:
                    st.plotly_chart(monthly_trends_fig, use_container_width=True)
        
        with col2:
            if not expenses_df.empty:
                budget_dist_fig = create_budget_distribution_chart(expenses_df)
                if budget_dist_fig:
                    st.plotly_chart(budget_dist_fig, use_container_width=True)
    
    with tab2:
        create_section_header("💰 ניהול תקציב")
        create_budget_section(expenses_df, donations_df, budget_status)
    
    with tab3:
        create_section_header("👥 ניהול תורמים")
        create_donors_section(donations_df, donor_stats)
    
    with tab4:
        create_section_header("👩 ניהול אלמנות")
        create_widows_section(almanot_df, widow_stats)
        
        # Add the complete widows table
        create_widows_table_section(almanot_df)
    
    with tab5:
        create_section_header("🕸️ מפת קשרים")
        create_network_section(expenses_df, donations_df, almanot_df, investors_df)
    
    with tab6:
        create_section_header("🏘️ אזורי מגורים")
        create_residential_breakdown_section(almanot_df, donations_df)

if __name__ == "__main__":
    main()



