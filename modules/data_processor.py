"""
Data Processor Module for Omri Association Dashboard
Handles data analysis, calculations, and processing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def calculate_monthly_stats(expenses_df, donations_df):
    """חישוב סטטיסטיקות חודשיות"""
    if expenses_df.empty and donations_df.empty:
        return {}
    
    # חישוב הוצאות חודשיות
    monthly_expenses = {}
    if not expenses_df.empty and 'תאריך' in expenses_df.columns:
        expenses_df['חודש'] = expenses_df['תאריך'].dt.to_period('M')
        monthly_expenses = expenses_df.groupby('חודש')['סכום'].sum().to_dict()
    
    # חישוב תרומות חודשיות
    monthly_donations = {}
    if not donations_df.empty and 'תאריך' in donations_df.columns:
        donations_df['חודש'] = donations_df['תאריך'].dt.to_period('M')
        monthly_donations = donations_df.groupby('חודש')['סכום'].sum().to_dict()
    
    return {
        'monthly_expenses': monthly_expenses,
        'monthly_donations': monthly_donations
    }

def calculate_donor_statistics(donations_df):
    """חישוב סטטיסטיקות תורמים"""
    if donations_df.empty:
        return {}
    
    # סך תרומות לפי תורם
    donor_totals = donations_df.groupby('שם התורם')['סכום'].sum().sort_values(ascending=False)
    
    # מספר תרומות לפי תורם
    donor_counts = donations_df.groupby('שם התורם').size().sort_values(ascending=False)
    
    # תרומה ממוצעת לפי תורם
    donor_averages = donations_df.groupby('שם התורם')['סכום'].mean().sort_values(ascending=False)
    
    return {
        'donor_totals': donor_totals,
        'donor_counts': donor_counts,
        'donor_averages': donor_averages,
        'total_donations': donations_df['סכום'].sum(),
        'total_donors': len(donor_totals)
    }

def calculate_widow_statistics(widows_df):
    """חישוב סטטיסטיקות אלמנות"""
    if widows_df.empty:
        return {}
    
    # אלמנות עם תורם
    widows_with_donor = widows_df[widows_df['תורם'].notna() & (widows_df['תורם'] != '')]
    
    # אלמנות ללא תורם
    widows_without_donor = widows_df[widows_df['תורם'].isna() | (widows_df['תורם'] == '')]
    
    # סך סכומים חודשיים
    total_monthly_amount = widows_df['סכום חודשי'].sum() if 'סכום חודשי' in widows_df.columns else 0
    
    return {
        'total_widows': len(widows_df),
        'widows_with_donor': len(widows_with_donor),
        'widows_without_donor': len(widows_without_donor),
        'total_monthly_amount': total_monthly_amount,
        'average_monthly_amount': widows_df['סכום חודשי'].mean() if 'סכום חודשי' in widows_df.columns else 0
    }

def process_graph_data(donations_df, widows_df):
    """עיבוד נתונים לגרף הקשרים"""
    if donations_df.empty or widows_df.empty:
        return {}, {}, pd.DataFrame()
    
    # ניקוי נתונים
    donations_clean = donations_df.dropna(subset=['שם התורם'])
    donations_clean = donations_clean[donations_clean['שם התורם'] != '']
    
    # יצירת מיפוי תורמים-אלמנות
    widow_to_donor_mapping = {}
    donor_connections = {}
    
    # סינון אלמנות אמיתיות (עם סכום חודשי 1000 או 2000)
    real_widows_df = widows_df[
        (widows_df['סכום חודשי'].isin([1000, 2000])) & 
        (widows_df['תורם'].notna()) & 
        (widows_df['תורם'] != '')
    ] if 'סכום חודשי' in widows_df.columns else pd.DataFrame()
    
    # יצירת מיפוי חיבורים
    for _, widow_row in real_widows_df.iterrows():
        widow_name = widow_row['שם ']
        donor_name = widow_row['תורם']
        
        # וודא שהתורם קיים בקובץ התרומות
        if donor_name in donations_clean['שם התורם'].values:
            widow_to_donor_mapping[widow_name] = donor_name
            if donor_name not in donor_connections:
                donor_connections[donor_name] = 0
            donor_connections[donor_name] += 1
    
    return widow_to_donor_mapping, donor_connections, real_widows_df

def get_recent_activity(expenses_df, donations_df, days=30):
    """קבלת פעילות אחרונה"""
    if expenses_df.empty and donations_df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # תאריך לפני X ימים
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # פעילות אחרונה בהוצאות
    recent_expenses = pd.DataFrame()
    if not expenses_df.empty and 'תאריך' in expenses_df.columns:
        recent_expenses = expenses_df[expenses_df['תאריך'] >= cutoff_date].copy()
    
    # פעילות אחרונה בתרומות
    recent_donations = pd.DataFrame()
    if not donations_df.empty and 'תאריך' in donations_df.columns:
        recent_donations = donations_df[donations_df['תאריך'] >= cutoff_date].copy()
    
    return recent_expenses, recent_donations

def calculate_budget_analysis(expenses_df, donations_df, widows_df):
    """ניתוח תקציבי"""
    if expenses_df.empty and donations_df.empty:
        return {}
    
    # הוצאות כוללות
    total_expenses = expenses_df['סכום'].sum() if not expenses_df.empty else 0
    
    # תרומות כוללות
    total_donations = donations_df['סכום'].sum() if not donations_df.empty else 0
    
    # הוצאות חודשיות לאלמנות
    monthly_widow_expenses = widows_df['סכום חודשי'].sum() if not widows_df.empty and 'סכום חודשי' in widows_df.columns else 0
    
    # יתרה
    balance = total_donations - total_expenses
    
    return {
        'total_expenses': total_expenses,
        'total_donations': total_donations,
        'monthly_widow_expenses': monthly_widow_expenses,
        'balance': balance,
        'donation_coverage_months': balance / monthly_widow_expenses if monthly_widow_expenses > 0 else 0
    } 