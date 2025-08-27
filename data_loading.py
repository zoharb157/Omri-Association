import pandas as pd
import streamlit as st
import os
import gspread
from google.oauth2.service_account import Credentials

# Define the scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Path to your service account file
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Spreadsheet ID
SPREADSHEET_ID = '1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo'

def load_data():
    """Load data directly from Google Sheets"""
    try:
        # Authenticate
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        gc = gspread.authorize(creds)
        
        # Open spreadsheet
        sh = gc.open_by_key(SPREADSHEET_ID)
        
        # Load expenses data
        exp_worksheet = sh.worksheet("Expenses")
        exp_values = exp_worksheet.get_all_values()
        if len(exp_values) >= 3:
            exp = pd.DataFrame(exp_values[2:], columns=exp_values[1])  # Skip title row, use row 1 as headers
            exp = exp.rename(columns={
                'NaT': 'תאריך',
                'שם לקוח': 'שם', 
                'סכום': 'שקלים'
            })
            exp = clean_dataframe(exp)
        else:
            exp = pd.DataFrame(columns=['תאריך', 'שם', 'שקלים'])
        
        # Load donations data
        don_worksheet = sh.worksheet("Donations")
        don_values = don_worksheet.get_all_values()
        if len(don_values) >= 3:
            don = pd.DataFrame(don_values[2:], columns=don_values[1])
            don = don.rename(columns={
                'NaT': 'תאריך',
                'שם התורם': 'שם',
                'סכום': 'שקלים'
            })
            don = clean_dataframe(don)
        else:
            don = pd.DataFrame(columns=['תאריך', 'שם', 'שקלים'])
        
        # Load investors data
        inv_worksheet = sh.worksheet("Investors")
        inv_values = inv_worksheet.get_all_values()
        if len(inv_values) >= 3:
            inv = pd.DataFrame(inv_values[2:], columns=inv_values[1])
            inv = inv.rename(columns={
                'NaT': 'תאריך',
                'שם התורם': 'שם',
                'סכום': 'שקלים'
            })
            inv = clean_dataframe(inv)
        else:
            inv = pd.DataFrame(columns=['תאריך', 'שם', 'שקלים'])
        
        # Combine donations and investors
        donations_df = pd.concat([don, inv], ignore_index=True)
        
        # Load widows data
        alman_worksheet = sh.worksheet("Almanot")  # Use Almanot instead of Widows
        alman_values = alman_worksheet.get_all_values()
        if len(alman_values) >= 2:
            alman = pd.DataFrame(alman_values[1:], columns=alman_values[0])  # Use first row as headers
            alman = clean_widows_data(alman)
        else:
            alman = pd.DataFrame(columns=['שם ', 'סכום חודשי', 'חודש התחלה', 'מייל', 'טלפון', 'תעודת זהות', 'מספר ילדים', 'חללים', 'הערות', 'תורם', 'איש קשר לתרומה'])
        
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
        df['שקלים'] = df['שקלים'].fillna('')
        df['שקלים'] = df['שקלים'].astype(str).str.replace('₪', '').str.replace(',', '')
        df['שקלים'] = df['שקלים'].replace('', pd.NA)
        df['שקלים'] = pd.to_numeric(df['שקלים'], errors='coerce')
    
    if 'סכום חודשי' in df.columns:
        df['סכום חודשי'] = df['סכום חודשי'].fillna('')
        df['סכום חודשי'] = df['סכום חודשי'].astype(str).str.replace('₪', '').str.replace(',', '')
        df['סכום חודשי'] = df['סכום חודשי'].replace('', pd.NA)
        df['סכום חודשי'] = pd.to_numeric(df['סכום חודשי'], errors='coerce')
    
    return df

def clean_widows_data(alman):
    """Clean widows data"""
    # Remove currency symbols and convert to float
    if 'סכום חודשי' in alman.columns:
        # First, handle empty strings and NaN values properly
        alman['סכום חודשי'] = alman['סכום חודשי'].fillna('')
        alman['סכום חודשי'] = alman['סכום חודשי'].astype(str)
        
        # Remove currency symbols and commas
        alman['סכום חודשי'] = alman['סכום חודשי'].str.replace('₪', '').str.replace(',', '')
        
        # Convert empty strings to NaN, then to numeric (this preserves actual 0 values but converts empty to NaN)
        alman['סכום חודשי'] = alman['סכום חודשי'].replace('', pd.NA)
        alman['סכום חודשי'] = pd.to_numeric(alman['סכום חודשי'], errors='coerce')
        
        # Fill NaN with 0 only if that's the intended behavior
        # alman['סכום חודשי'] = alman['סכום חודשי'].fillna(0)
    
    return alman 