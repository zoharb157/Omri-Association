#!/usr/bin/env python3
"""
Omri Association Dashboard - SIMPLE WORKING VERSION
Complete dashboard with all 6 tabs and features we built together
"""

import streamlit as st
import pandas as pd
import logging
import plotly.express as px
import plotly.graph_objects as go
from google_sheets_io import load_all_data, check_service_account_validity

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

def create_monthly_trends_chart(expenses_df, donations_df):
    """Create monthly trends chart"""
    try:
        if expenses_df.empty or donations_df.empty:
            return None
            
        # Ensure dates are properly converted
        expenses_df_copy = expenses_df.copy()
        expenses_df_copy['תאריך'] = pd.to_datetime(expenses_df_copy['תאריך'], errors='coerce')
        valid_expenses = expenses_df_copy.dropna(subset=['תאריך'])
        
        donations_df_copy = donations_df.copy()
        donations_df_copy['תאריך'] = pd.to_datetime(donations_df_copy['תאריך'], errors='coerce')
        valid_donations = donations_df_copy.dropna(subset=['תאריך'])
        
        if valid_expenses.empty or valid_donations.empty:
            return None
            
        # Calculate monthly totals
        monthly_expenses = valid_expenses.groupby(valid_expenses['תאריך'].dt.strftime('%Y-%m'))['שקלים'].sum().reset_index()
        monthly_donations = valid_donations.groupby(valid_donations['תאריך'].dt.strftime('%Y-%m'))['שקלים'].sum().reset_index()
        
        # Create the chart
        fig = go.Figure()
        
        # Add expenses line
        fig.add_trace(go.Scatter(
            x=monthly_expenses['תאריך'],
            y=monthly_expenses['שקלים'],
            name='הוצאות',
            line=dict(color='red', width=2),
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))
        
        # Add donations line
        fig.add_trace(go.Scatter(
            x=monthly_donations['תאריך'],
            y=monthly_donations['שקלים'],
            name='תרומות',
            line=dict(color='green', width=2),
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title='מגמות חודשיות בהוצאות ותרומות',
            xaxis_title='חודש',
            yaxis_title='סכום (₪)',
            hovermode='x unified',
            height=400
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating monthly trends chart: {e}")
        return None

def create_budget_distribution_chart(expenses_df):
    """Create budget distribution chart"""
    try:
        if expenses_df.empty:
            return None
            
        # Group by name and calculate totals
        budget_data = expenses_df.groupby('שם')['שקלים'].sum().reset_index()
        budget_data = budget_data.sort_values('שקלים', ascending=False)
        
        # Create figure
        fig = px.pie(
            budget_data,
            values='שקלים',
            names='שם',
            title='התפלגות תקציב',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            title_x=0.5,
            showlegend=True,
            height=400
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating budget distribution chart: {e}")
        return None

def create_donor_contribution_chart(donations_df):
    """Create donor contribution chart"""
    try:
        if donations_df.empty:
            return None
            
        # Calculate total donations by donor
        donor_totals = donations_df.groupby('שם')['שקלים'].sum().sort_values(ascending=False)
        
        # Create the chart
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=donor_totals.index,
            y=donor_totals.values,
            name='תרומות',
            marker_color='lightblue',
            hovertemplate='תורם: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))
        
        fig.update_layout(
            title='תרומות לפי תורם',
            xaxis_title='תורם',
            yaxis_title='סכום (₪)',
            height=400
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating donor contribution chart: {e}")
        return None

def create_widows_support_chart(almanot_df):
    """Create widows support chart"""
    try:
        if almanot_df.empty or 'סכום חודשי' not in almanot_df.columns:
            return None
            
        # Clean monthly support data
        almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
        
        # Group by name and calculate totals
        support_data = almanot_df.groupby('שם ')['סכום חודשי'].sum().reset_index()
        support_data = support_data.sort_values('סכום חודשי', ascending=False)
        
        # Create figure
        fig = px.bar(
            support_data,
            x='שם ',
            y='סכום חודשי',
            title='תמיכה באלמנות',
            color='סכום חודשי',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            title_x=0.5,
            height=400
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating widows support chart: {e}")
        return None

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
        
        # Fallback to sample data
        expenses_df, donations_df, investors_df, almanot_df = get_sample_data()
    
    # Create the 6 main tabs we had working
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
        
        # Financial metrics
        st.markdown("#### 💰 סקירה פיננסית")
        financial_metrics = [
            {
                'label': 'סך תרומות',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל התרומות שהתקבלו עד כה'
            },
            {
                'label': 'סך הוצאות',
                'value': f"₪{pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל ההוצאות שהוצאו עד כה'
            },
            {
                'label': 'יתרה זמינה',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() - pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'יתרה זמינה לפעילות עתידית'
            },
            {
                'label': 'אחוז ניצול',
                'value': f"{(pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum() / pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() * 100) if pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() > 0 else 0:.1f}%",
                'help': 'אחוז התרומות שהוצאו'
            }
        ]
        create_metric_row(financial_metrics, 4)
        
        # Organizational metrics
        st.markdown("#### 👥 מדדים ארגוניים")
        org_metrics = [
            {
                'label': 'מספר תורמים',
                'value': f"{len(donations_df['שם'].unique()) if 'שם' in donations_df.columns else 0:,}",
                'help': 'סך כל התורמים שתרמו לעמותה'
            },
            {
                'label': 'מספר אלמנות',
                'value': f"{len(almanot_df['שם '].unique()) if 'שם ' in almanot_df.columns else 0:,}",
                'help': 'סך כל האלמנות המטופלות על ידי העמותה'
            }
        ]
        create_metric_row(org_metrics, 2)
        
        # Charts
        st.markdown("#### 📈 גרפים")
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_trends_fig = create_monthly_trends_chart(expenses_df, donations_df)
            if monthly_trends_fig:
                st.plotly_chart(monthly_trends_fig, use_container_width=True, key="home_monthly_trends")
        
        with col2:
            budget_dist_fig = create_budget_distribution_chart(expenses_df)
            if budget_dist_fig:
                st.plotly_chart(budget_dist_fig, use_container_width=True, key="home_budget_dist")
        
        # Complete widows table
        st.markdown("#### 📋 טבלת כל האלמנות")
        if not almanot_df.empty:
            display_columns = ['שם ', 'מספר ילדים', 'סכום חודשי', 'תורם']
            available_columns = [col for col in display_columns if col in almanot_df.columns]
            
            if len(available_columns) > 0:
                sorted_widows = almanot_df.sort_values('סכום חודשי', ascending=False)
                st.dataframe(sorted_widows[available_columns], use_container_width=True)
            else:
                st.warning("⚠️ לא ניתן לטעון טבלת אלמנות")
        else:
            st.info("אין נתוני אלמנות להצגה")
    
    with tab2:
        create_section_header("💰 ניהול תקציב")
        
        # Budget metrics
        st.markdown("#### 💰 סקירה פיננסית")
        financial_metrics = [
            {
                'label': 'סך תרומות',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל התרומות שהתקבלו עד כה'
            },
            {
                'label': 'סך הוצאות',
                'value': f"₪{pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל ההוצאות שהוצאו עד כה'
            },
            {
                'label': 'יתרה זמינה',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() - pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'יתרה זמינה לפעילות עתידית'
            },
            {
                'label': 'אחוז ניצול',
                'value': f"{(pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum() / pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() * 100) if pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() > 0 else 0:.1f}%",
                'help': 'אחוז התרומות שהוצאו'
            }
        ]
        create_metric_row(financial_metrics, 4)
        
        # Budget Charts
        st.markdown("#### 📈 גרפי תקציב")
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_trends_fig = create_monthly_trends_chart(expenses_df, donations_df)
            if monthly_trends_fig:
                st.plotly_chart(monthly_trends_fig, use_container_width=True, key="budget_monthly_trends")
        
        with col2:
            budget_dist_fig = create_budget_distribution_chart(expenses_df)
            if budget_dist_fig:
                st.plotly_chart(budget_dist_fig, use_container_width=True, key="budget_distribution")
    
    with tab3:
        create_section_header("👥 ניהול תורמים")
        
        # Donor metrics
        st.markdown("#### 👥 סטטיסטיקות תורמים")
        donor_metrics = [
            {
                'label': 'מספר תורמים',
                'value': f"{len(donations_df['שם'].unique()) if 'שם' in donations_df.columns else 0:,}",
                'help': 'סך כל התורמים שתרמו לעמותה'
            },
            {
                'label': 'סך תרומות',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל התרומות שהתקבלו'
            },
            {
                'label': 'תרומה ממוצעת',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).mean():,.0f}",
                'help': 'תרומה ממוצעת לתורם'
            }
        ]
        create_metric_row(donor_metrics, 3)
        
        # Donor Charts
        st.markdown("#### 📈 גרפי תורמים")
        if not donations_df.empty:
            donor_fig = create_donor_contribution_chart(donations_df)
            if donor_fig:
                st.plotly_chart(donor_fig, use_container_width=True, key="donor_contributions")
    
    with tab4:
        create_section_header("👩 ניהול אלמנות")
        
        # Widow metrics
        st.markdown("#### 👩 סטטיסטיקות אלמנות")
        widow_metrics = [
            {
                'label': 'מספר אלמנות',
                'value': f"{len(almanot_df['שם '].unique()) if 'שם ' in almanot_df.columns else 0:,}",
                'help': 'סך כל האלמנות המטופלות'
            },
            {
                'label': 'סך תמיכה חודשית',
                'value': f"₪{pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך תמיכה חודשית באלמנות'
            },
            {
                'label': 'תמיכה ממוצעת',
                'value': f"₪{pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0).mean():,.0f}",
                'help': 'תמיכה ממוצעת לאלמנה'
            }
        ]
        create_metric_row(widow_metrics, 3)
        
        # Widow Charts
        st.markdown("#### 📈 גרפי אלמנות")
        if not almanot_df.empty:
            widows_fig = create_widows_support_chart(almanot_df)
            if widows_fig:
                st.plotly_chart(widows_fig, use_container_width=True, key="widows_support")
        
        # Complete Widows Table
        st.markdown("#### 📋 טבלת כל האלמנות")
        if not almanot_df.empty:
            display_columns = ['שם ', 'מספר ילדים', 'סכום חודשי', 'תורם']
            available_columns = [col for col in display_columns if col in almanot_df.columns]
            
            if len(available_columns) > 0:
                sorted_widows = almanot_df.sort_values('סכום חודשי', ascending=False)
                st.dataframe(sorted_widows[available_columns], use_container_width=True)
            else:
                st.warning("⚠️ לא ניתן לטעון טבלת אלמנות")
        else:
            st.info("אין נתוני אלמנות להצגה")
    
    with tab5:
        create_section_header("🕸️ מפת קשרים")
        
        # Filter controls - EXACT version we built together
        st.markdown("#### 🔍 מסננים")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_connected = st.checkbox("הצג מחוברים", value=True, help="הצג תורמים ואלמנות עם קשרים")
        
        with col2:
            show_unconnected_donors = st.checkbox("הצג תורמים ללא קשר", value=True, help="הצג תורמים ללא קשרים")
        
        with col3:
            show_unconnected_widows = st.checkbox("הצג אלמנות ללא קשר", value=True, help="הצג אלמנות ללא קשרים")
        
        st.markdown("---")
        
        # Network graph
        try:
            # Clean monthly support data
            if 'סכום חודשי' in almanot_df.columns:
                almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
            
            # Create nodes and edges
            nodes = []
            edges = []
            
            # Get all valid donors
            all_donors = set()
            if 'שם' in donations_df.columns:
                donors_from_donations = donations_df['שם'].dropna().unique()
                for donor in donors_from_donations:
                    all_donors.add(str(donor).strip())
            
            if 'שם' in investors_df.columns:
                investors_names = investors_df['שם'].dropna().unique()
                for investor in investors_names:
                    all_donors.add(str(investor).strip())
            
            # Categorize nodes
            connected_donors = set()
            connected_widows = set()
            unconnected_donors = set()
            unconnected_widows = set()
            
            # Find connections
            if 'שם ' in almanot_df.columns:
                for _, widow in almanot_df.iterrows():
                    widow_name = widow['שם ']
                    if pd.notna(widow_name):
                        donor = widow.get('תורם')
                        monthly_support = widow.get('סכום חודשי', 0)
                        
                        if pd.isna(monthly_support) or monthly_support == '' or monthly_support == 0:
                            monthly_support = 0
                        else:
                            try:
                                monthly_support = float(monthly_support)
                                if pd.isna(monthly_support):
                                    monthly_support = 0
                            except (ValueError, TypeError):
                                monthly_support = 0
                        
                        # Try to find matching donor
                        matched_donor = None
                        if pd.notna(donor):
                            donor_str = str(donor).strip()
                            if donor_str in all_donors:
                                matched_donor = donor_str
                            else:
                                # Try partial matching
                                for potential_donor in all_donors:
                                    if (donor_str in potential_donor or 
                                        potential_donor in donor_str or
                                        donor_str.lower() == potential_donor.lower()):
                                        matched_donor = potential_donor
                                        break
                        
                        if matched_donor and monthly_support > 0:
                            connected_donors.add(matched_donor)
                            connected_widows.add(widow_name)
                            
                            # Add edge only if showing connected
                            if show_connected:
                                edges.append({
                                    'from': matched_donor,
                                    'to': widow_name,
                                    'arrows': 'to',
                                    'label': f"₪{monthly_support:,.0f}"
                                })
                        else:
                            unconnected_widows.add(widow_name)
            
            # Identify unconnected donors
            unconnected_donors = all_donors - connected_donors
            
            # Add nodes with area constraints for natural floating - RESPECT FILTERS
            
            # Left area: Unconnected widows (will float naturally in left area)
            if show_unconnected_widows:
                for widow_name in sorted(unconnected_widows):
                    nodes.append({
                        'id': widow_name,
                        'label': widow_name,
                        'group': 'widow_unconnected',
                        'title': 'אלמנה ללא קשר',
                        'color': '#ffb347',  # Light orange for unconnected widows
                        'size': 18,
                        'font': {'size': 7, 'color': '#000000', 'face': 'Arial', 'bold': True}
                    })
            
            # Middle area: Connected pairs (will float naturally in middle area)
            if show_connected:
                for donor in sorted(connected_donors):
                    nodes.append({
                        'id': donor,
                        'label': donor,
                        'group': 'donor_connected',
                        'title': 'תורם מחובר',
                        'color': '#1f77b4',  # Blue for connected donors
                        'size': 25,
                        'font': {'size': 8, 'color': '#000000', 'face': 'Arial', 'bold': True}
                    })
                
                for widow in sorted(connected_widows):
                    nodes.append({
                        'id': widow,
                        'label': widow,
                        'group': 'widow_connected',
                        'title': 'אלמנה מחוברת',
                        'color': '#ff7f0e',  # Orange for connected widows
                        'size': 22,
                        'font': {'size': 7, 'color': '#000000', 'face': 'Arial', 'bold': True}
                    })
            
            # Right area: Unconnected donors (will float naturally in right area)
            if show_unconnected_donors:
                for donor_name in sorted(unconnected_donors):
                    nodes.append({
                        'id': donor_name,
                        'label': donor_name,
                        'group': 'donor_unconnected',
                        'title': 'תורם ללא קשר',
                        'color': '#87ceeb',  # Light blue for unconnected donors
                        'size': 20,
                        'font': {'size': 7, 'color': '#000000', 'face': 'Arial', 'bold': True}
                    })
            
            # Create network visualization
            if nodes and edges:
                try:
                    from streamlit_agraph import agraph, Node, Edge, Config
                    
                    # Convert to agraph format
                    agraph_nodes = []
                    for node in nodes:
                        if node['group'] == 'donor_connected':
                            agraph_nodes.append(Node(
                                id=node['id'], 
                                label=node['label'], 
                                size=25,
                                color="#1f77b4",
                                font={"size": 8, "color": "#000000", "face": "Arial", "bold": True},
                                title=node['title']
                            ))
                        elif node['group'] == 'widow_connected':
                            agraph_nodes.append(Node(
                                id=node['id'], 
                                label=node['label'], 
                                size=22,
                                color="#ff7f0e",
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node['title']
                            ))
                        elif node['group'] == 'donor_unconnected':
                            agraph_nodes.append(Node(
                                id=node['id'], 
                                label=node['label'], 
                                size=20,
                                color="#87ceeb",
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node['title']
                            ))
                        elif node['group'] == 'widow_unconnected':
                            agraph_nodes.append(Node(
                                id=node['id'], 
                                label=node['label'], 
                                size=18,
                                color="#ffb347",
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node['title']
                            ))
                    
                    agraph_edges = [Edge(
                        source=edge['from'], 
                        target=edge['to'], 
                        arrows="to",
                        label=edge['label'],
                        color="#333333",
                        width=1.5,
                        font={"size": 8, "color": "#000000"}
                    ) for edge in edges]
                    
                    config = Config(
                        height=800,
                        width="100%",
                        directed=True,
                        physics=True,
                        hierarchical=False,
                        nodeHighlightBehavior=True,
                        highlightColor="#F7A7A6",
                        collapsible=True,
                        nodeSpacing=20,
                        nodeSize=25,
                        fontSize=8,
                        fontColor="#000000",
                        backgroundColor="#ffffff",
                        linkHighlightBehavior=True,
                        linkHighlightColor="#F7A7A6",
                        labelHighlightBold=True,
                        showEdgeLabels=True
                    )
                    
                    agraph(nodes=agraph_nodes, edges=agraph_edges, config=config)
                    
                except ImportError:
                    st.warning("⚠️ streamlit-agraph לא מותקן. התקן עם: pip install streamlit-agraph")
            else:
                st.info("אין נתונים להצגת מפת קשרים")
                
        except Exception as e:
            st.error("שגיאה ביצירת מפת קשרים")
            logger.error(f"Network error: {e}")
    
    with tab6:
        create_section_header("🏘️ פילוח של אזורי מגורים")
        
        if not almanot_df.empty:
            # Check if city column exists and has valid data
            if 'עיר' in almanot_df.columns:
                city_data = almanot_df['עיר'].dropna()
                valid_cities = city_data[~city_data.astype(str).str.contains(r'\d{3,}', regex=True)]
                
                if len(valid_cities) > 0:
                    st.subheader("🏙️ פילוח לפי עיר")
                    if 'סכום חודשי' in almanot_df.columns:
                        city_breakdown = almanot_df.groupby('עיר').agg({
                            'סכום חודשי': ['sum', 'count', 'mean']
                        }).round(0)
                        city_breakdown.columns = ['סך תמיכה', 'מספר אלמנות', 'תמיכה ממוצעת']
                        city_breakdown = city_breakdown.sort_values('סך תמיכה', ascending=False)
                        st.dataframe(city_breakdown, use_container_width=True)
                    else:
                        city_breakdown = almanot_df.groupby('עיר').size().reset_index(name='מספר אלמנות')
                        city_breakdown = city_breakdown.sort_values('מספר אלמנות', ascending=False)
                        st.dataframe(city_breakdown, use_container_width=True)
                else:
                    st.info("אין נתוני עיר זמינים - מציג מידע כללי")
                    st.subheader("📊 סיכום כללי")
                    st.write(f"**סך אלמנות:** {len(almanot_df)}")
                    if 'סכום חודשי' in almanot_df.columns:
                        total_support = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').sum()
                        st.write(f"**סך תמיכה חודשית:** ₪{total_support:,.0f}")
            else:
                st.info("אין נתוני עיר זמינים - מציג מידע כללי")
                st.subheader("📊 סיכום כללי")
                st.write(f"**סך אלמנות:** {len(almanot_df)}")
                if 'סכום חודשי' in almanot_df.columns:
                    total_support = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').sum()
                    st.write(f"**סך תמיכה חודשית:** ₪{total_support:,.0f}")
            
            # Widows table
            st.subheader("📋 רשימת אלמנות")
            st.dataframe(almanot_df, use_container_width=True)
        else:
            st.warning("אין נתוני מגורים להצגה")

if __name__ == "__main__":
    main()



