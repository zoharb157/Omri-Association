"""
Data Loader Module for Omri Association Dashboard
Handles Google Sheets connection and data loading
"""

import pandas as pd
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Google Sheets dependencies
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False

def create_google_sheets_connection():
    """יצירת חיבור ל-Google Sheets"""
    if not GOOGLE_SHEETS_AVAILABLE:
        return None
        
    try:
        # הגדרת הרשאות
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # טעינת פרטי החשבון
        creds = Credentials.from_service_account_file(
            'service_account.json',
            scopes=SCOPES
        )
        
        # יצירת שירות
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        return None

def load_sheet_data(service, spreadsheet_id, sheet_name):
    """טעינת נתונים מגיליון ספציפי"""
    if not service:
        return pd.DataFrame()
        
    try:
        # קריאת הנתונים
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=sheet_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            return pd.DataFrame()
        
        # המרה ל-DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        
        # ניקוי נתונים
        df = clean_dataframe(df, sheet_name)
        
        return df
        
    except Exception as e:
        return pd.DataFrame()

def clean_dataframe(df, sheet_name):
    """ניקוי DataFrame לפי סוג הגיליון"""
    if sheet_name == 'Expenses':
        return clean_expenses_data(df)
    elif sheet_name == 'Donations':
        return clean_donations_data(df)
    elif sheet_name == 'Widows':
        return clean_widows_data(df)
    elif sheet_name == 'Investors':
        return clean_investors_data(df)
    else:
        return df

def clean_expenses_data(df):
    """ניקוי נתוני הוצאות"""
    if df.empty:
        return df
    
    # הסרת עמודות ריקות
    df = df.dropna(how='all')
    
    # המרת עמודת תאריך
    if 'NaT' in df.columns:
        df['תאריך'] = pd.to_datetime(df['NaT'], errors='coerce')
        df = df.drop('NaT', axis=1)
    
    # המרת עמודת סכום וניקוי ערכים לא תקינים
    if 'סכום' in df.columns:
        df['סכום'] = pd.to_numeric(df['סכום'], errors='coerce')
        # הסרת שורות עם ערכים אפס, שליליים או NaN
        df = df[(df['סכום'] > 0) & (df['סכום'].notna())]
    
    # בחירת עמודות רלוונטיות
    relevant_columns = ['תאריך', 'שם לקוח', 'סכום']
    df = df[relevant_columns].copy()
    
    return df

def clean_donations_data(df):
    """ניקוי נתוני תרומות"""
    if df.empty:
        return df
    
    # הסרת עמודות ריקות
    df = df.dropna(how='all')
    
    # המרת עמודת תאריך
    if 'NaT' in df.columns:
        df['תאריך'] = pd.to_datetime(df['NaT'], errors='coerce')
        df = df.drop('NaT', axis=1)
    
    # המרת עמודת סכום וניקוי ערכים לא תקינים
    if 'סכום' in df.columns:
        df['סכום'] = pd.to_numeric(df['סכום'], errors='coerce')
        # הסרת שורות עם ערכים אפס, שליליים או NaN
        df = df[(df['סכום'] > 0) & (df['סכום'].notna())]
    
    # בחירת עמודות רלוונטיות
    relevant_columns = ['תאריך', 'שם התורם', 'סכום']
    df = df[relevant_columns].copy()
    
    return df

def clean_widows_data(df):
    """ניקוי נתוני אלמנות"""
    if df.empty:
        return df
    
    # הסרת עמודות ריקות
    df = df.dropna(how='all')
    
    # המרת עמודת סכום חודשי וניקוי ערכים לא תקינים
    if 'סכום חודשי' in df.columns:
        df['סכום חודשי'] = pd.to_numeric(df['סכום חודשי'], errors='coerce')
        # הסרת שורות עם ערכים אפס, שליליים או NaN
        df = df[(df['סכום חודשי'] > 0) & (df['סכום חודשי'].notna())]
    
    return df

def clean_investors_data(df):
    """ניקוי נתוני משקיעים"""
    if df.empty:
        return df
    
    # הסרת עמודות ריקות
    df = df.dropna(how='all')
    
    return df

def load_all_data():
    """טעינת כל הנתונים מ-Google Sheets"""
    if not GOOGLE_SHEETS_AVAILABLE:
        # יצירת נתונים ריקים אם Google Sheets לא זמין
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # ID של ה-Spreadsheet
    SPREADSHEET_ID = '1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo'
    
    # יצירת חיבור
    service = create_google_sheets_connection()
    if not service:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # טעינת נתונים
    expenses_df = load_sheet_data(service, SPREADSHEET_ID, 'Expenses')
    donations_df = load_sheet_data(service, SPREADSHEET_ID, 'Donations')
    widows_df = load_sheet_data(service, SPREADSHEET_ID, 'Widows')
    investors_df = load_sheet_data(service, SPREADSHEET_ID, 'Investors')
    
    return expenses_df, donations_df, widows_df, investors_df 