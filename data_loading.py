import pandas as pd
import streamlit as st
import os
from google_sheets_io import read_sheet

def load_data():
    """Load data from Google Sheets"""
    try:
        # Load expenses data
        exp = read_sheet("Expenses")
        # הנתונים מגיעים עם עמודות: ['NaT', 'שם לקוח', 'סכום', ...]
        # צריך למפות אותם לעמודות הנכונות
        if 'NaT' in exp.columns and 'שם לקוח' in exp.columns and 'סכום' in exp.columns:
            exp = exp.rename(columns={
                'NaT': 'תאריך',
                'שם לקוח': 'שם', 
                'סכום': 'שקלים'
            })
        exp = clean_dataframe(exp)
        
        # Load donations data
        don = read_sheet("Donations")
        # הנתונים מגיעים עם עמודות: ['NaT', 'שם התורם', 'סכום', ...]
        if 'NaT' in don.columns and 'שם התורם' in don.columns and 'סכום' in don.columns:
            don = don.rename(columns={
                'NaT': 'תאריך',
                'שם התורם': 'שם',
                'סכום': 'שקלים'
            })
        don = clean_dataframe(don)
        
        # Load investors data
        inv = read_sheet("Investors")
        # הנתונים מגיעים עם עמודות: ['NaT', 'שם התורם', 'סכום', ...]
        if 'NaT' in inv.columns and 'שם התורם' in inv.columns and 'סכום' in inv.columns:
            inv = inv.rename(columns={
                'NaT': 'תאריך',
                'שם התורם': 'שם',
                'סכום': 'שקלים'
            })
        inv = clean_dataframe(inv)
        
        # Combine donations and investors
        donations_df = pd.concat([don, inv], ignore_index=True)
        
        # Load widows data
        alman = read_sheet("Widows")
        # הנתונים מגיעים עם עמודות: ['שם', 'מייל', 'טלפון', ...]
        # וודא שיש עמודת 'סכום חודשי'
        if 'סכום חודשי' not in alman.columns:
            st.warning("לא נמצאה עמודת 'סכום חודשי' בקובץ האלמנות. נוצרת עמודה עם ערך ברירת מחדל 0.")
            alman["סכום חודשי"] = 0
        alman = clean_widows_data(alman)
        
        return exp, donations_df, alman, inv
        
    except Exception as e:
        st.error(f"שגיאה בטעינת הנתונים: {str(e)}")
        return None, None, None, None

def clean_dataframe(df):
    """Clean dataframe data"""
    # Convert date format
    if 'תאריך' in df.columns:
        df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')
    
    # Remove currency symbols and convert to float
    if 'שקלים' in df.columns:
        df['שקלים'] = df['שקלים'].astype(str).str.replace('₪', '').str.replace(',', '').replace('', '0').astype(float)
    if 'סכום חודשי' in df.columns:
        df['סכום חודשי'] = df['סכום חודשי'].astype(str).str.replace('₪', '').str.replace(',', '').replace('', '0').astype(float)
    
    return df

def clean_widows_data(alman):
    """Clean widows data"""
    # Remove currency symbols and convert to float
    if 'סכום חודשי' in alman.columns:
        alman['סכום חודשי'] = alman['סכום חודשי'].astype(str).str.replace('₪', '').str.replace(',', '').replace('', '0').astype(float)
    
    return alman 