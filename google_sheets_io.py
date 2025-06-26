import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from typing import Optional
import os

# Define the scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Path to your service account file
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Spreadsheet ID (replace with your actual spreadsheet ID)
SPREADSHEET_ID = '1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo'

# Initialize Google Sheets client
gc = None
try:
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        # Authenticate and create a client
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        gc = gspread.authorize(creds)
        print("Google Sheets connection established successfully!")
    else:
        print("Warning: service_account.json not found. Falling back to Excel files.")
except Exception as e:
    print(f"Warning: Could not connect to Google Sheets: {e}. Falling back to Excel files.")


def _fix_headers(headers):
    """Return a list of unique, non-empty headers. Empty headers get a default name. Duplicates get a suffix."""
    seen = {}
    fixed = []
    for i, h in enumerate(headers):
        name = h.strip() if isinstance(h, str) else ''
        if not name:
            name = f'עמודה_{i+1}'
        orig_name = name
        count = seen.get(name, 0)
        if count:
            name = f'{orig_name}_{count+1}'
        seen[orig_name] = count + 1
        fixed.append(name)
    return fixed


def _map_columns_to_expected(df, sheet_name):
    """Map actual columns from Google Sheets to expected column names"""
    try:
        if sheet_name == "Expenses":
            # Map the actual columns to expected columns
            column_mapping = {}
            
            # Find date column (look for any column with date-like content)
            for col in df.columns:
                if 'תאריך' in str(col):
                    column_mapping[col] = 'תאריך'
                    break
            
            # Find name column (look for any column with name-like content, but not the title)
            for col in df.columns:
                if 'שם' in str(col) and 'הוצאות' not in str(col) and 'עמרי' not in str(col):
                    column_mapping[col] = 'שם'
                    break
            
            # Find amount column (look for any column with amount-like content)
            for col in df.columns:
                if 'שקלים' in str(col) or 'סכום' in str(col):
                    column_mapping[col] = 'שקלים'
                    break
            
            # If we didn't find the expected columns, try to map by position
            if len(column_mapping) < 3:
                # Try to map by looking at the actual data
                for i, col in enumerate(df.columns):
                    if i == 0 and 'תאריך' not in column_mapping.values():
                        column_mapping[col] = 'תאריך'
                    elif i == 1 and 'שם' not in column_mapping.values():
                        column_mapping[col] = 'שם'
                    elif i == 2 and 'שקלים' not in column_mapping.values():
                        column_mapping[col] = 'שקלים'
            
            # Rename columns
            df = df.rename(columns=column_mapping)
            
            # Add missing columns with empty values
            expected_columns = ['תאריך', 'שם', 'שקלים']
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Keep only the expected columns
            df = df[expected_columns]
            
            return df
        
        elif sheet_name == "Donations":
            # Similar mapping for donations
            column_mapping = {}
            
            # Find date column
            for col in df.columns:
                if 'תאריך' in str(col):
                    column_mapping[col] = 'תאריך'
                    break
            
            # Find name column
            for col in df.columns:
                if 'שם' in str(col) and 'תורם' in str(col):
                    column_mapping[col] = 'שם'
                    break
            
            # Find amount column
            for col in df.columns:
                if 'שקלים' in str(col) or 'סכום' in str(col):
                    column_mapping[col] = 'שקלים'
                    break
            
            # If we didn't find the expected columns, try to map by position
            if len(column_mapping) < 3:
                for i, col in enumerate(df.columns):
                    if i == 0 and 'תאריך' not in column_mapping.values():
                        column_mapping[col] = 'תאריך'
                    elif i == 1 and 'שם' not in column_mapping.values():
                        column_mapping[col] = 'שם'
                    elif i == 2 and 'שקלים' not in column_mapping.values():
                        column_mapping[col] = 'שקלים'
            
            df = df.rename(columns=column_mapping)
            
            expected_columns = ['תאריך', 'שם', 'שקלים']
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Keep only the expected columns
            df = df[expected_columns]
            
            return df
        
        elif sheet_name == "Investors":
            # Similar mapping for investors
            column_mapping = {}
            
            # Find date column
            for col in df.columns:
                if 'תאריך' in str(col):
                    column_mapping[col] = 'תאריך'
                    break
            
            # Find name column
            for col in df.columns:
                if 'שם' in str(col) and 'משקיע' in str(col):
                    column_mapping[col] = 'שם'
                    break
            
            # Find amount column
            for col in df.columns:
                if 'שקלים' in str(col) or 'סכום' in str(col):
                    column_mapping[col] = 'שקלים'
                    break
            
            # If we didn't find the expected columns, try to map by position
            if len(column_mapping) < 3:
                for i, col in enumerate(df.columns):
                    if i == 0 and 'תאריך' not in column_mapping.values():
                        column_mapping[col] = 'תאריך'
                    elif i == 1 and 'שם' not in column_mapping.values():
                        column_mapping[col] = 'שם'
                    elif i == 2 and 'שקלים' not in column_mapping.values():
                        column_mapping[col] = 'שקלים'
            
            df = df.rename(columns=column_mapping)
            
            expected_columns = ['תאריך', 'שם', 'שקלים']
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Keep only the expected columns
            df = df[expected_columns]
            
            return df
        
        elif sheet_name == "Widows":
            # Mapping for widows sheet
            column_mapping = {}
            for col in df.columns:
                if 'שם' in str(col) and ' ' not in str(col):
                    column_mapping[col] = 'שם '
                elif 'סכום' in str(col) and 'חודשי' in str(col):
                    column_mapping[col] = 'סכום חודשי'
                elif 'חודש' in str(col) and 'התחלה' in str(col):
                    column_mapping[col] = 'חודש התחלה'
                elif 'מייל' in str(col) or 'email' in str(col).lower():
                    column_mapping[col] = 'מייל'
                elif 'טלפון' in str(col) or 'phone' in str(col).lower():
                    column_mapping[col] = 'טלפון'
                elif 'תעודת' in str(col) and 'זהות' in str(col):
                    column_mapping[col] = 'תעודת זהות'
                elif 'מספר' in str(col) and 'ילדים' in str(col):
                    column_mapping[col] = 'מספר ילדים'
                elif 'חללים' in str(col):
                    column_mapping[col] = 'חללים'
                elif 'הערות' in str(col):
                    column_mapping[col] = 'הערות'
                elif 'תורם' in str(col):
                    column_mapping[col] = 'תורם'
                elif 'איש' in str(col) and 'קשר' in str(col):
                    column_mapping[col] = 'איש קשר לתרומה'
            
            df = df.rename(columns=column_mapping)
            
            expected_columns = ['שם ', 'סכום חודשי', 'חודש התחלה', 'מייל', 'טלפון', 'תעודת זהות', 'מספר ילדים', 'חללים', 'הערות', 'תורם', 'איש קשר לתרומה']
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ''
            
            return df
        
        return df
    except Exception as e:
        print(f"Error in column mapping for {sheet_name}: {e}")
        # Return the original DataFrame if mapping fails
        return df


def read_sheet(sheet_name: str) -> pd.DataFrame:
    """Read a worksheet from Google Sheets and return as a DataFrame."""
    if gc is None:
        # No Excel fallback - return empty DataFrame with expected columns
        print("Google Sheets not available - returning empty DataFrame")
        if sheet_name == "Widows":
            return pd.DataFrame(columns=['שם ', 'סכום חודשי', 'חודש התחלה', 'מייל', 'טלפון', 'תעודת זהות', 'מספר ילדים', 'חללים', 'הערות', 'תורם', 'איש קשר לתרומה'])
        else:
            return pd.DataFrame(columns=['תאריך', 'שם', 'שקלים'])
    
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        
        # Map sheet names to actual Google Sheets names
        sheet_mapping = {
            "Widows": "Almanot"  # Map Widows to Almanot
        }
        
        actual_sheet_name = sheet_mapping.get(sheet_name, sheet_name)
        worksheet = sh.worksheet(actual_sheet_name)
        
        # Get all values (including header row)
        values = worksheet.get_all_values()
        if not values:
            print(f"Sheet '{actual_sheet_name}' is empty")
            return pd.DataFrame()
        
        # For financial sheets (Expenses, Donations, Investors), skip the first 2 rows
        # Row 0: Title (e.g., "עמרי למען משפחות השכול- הוצאות")
        # Row 1: Headers (e.g., "תאריך", "שם לקוח", "סכום")
        # Row 2+: Data
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            if len(values) >= 3:
                headers = _fix_headers(values[1])  # Use row 1 as headers
                data = values[2:]  # Start from row 2
            else:
                print(f"Sheet '{actual_sheet_name}' has insufficient data")
                return pd.DataFrame()
        else:
            # For other sheets, use first row as headers
            headers = _fix_headers(values[0])
            data = values[1:]
        
        df = pd.DataFrame(data, columns=headers)
        
        # Debug: Print the DataFrame info
        print(f"Loaded DataFrame for {sheet_name}:")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape}")
        print(f"First few rows:")
        print(df.head())
        
        # Map columns to expected names
        df = _map_columns_to_expected(df, sheet_name)
        
        # Convert date columns to datetime
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            if 'תאריך' in df.columns:
                df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')
        elif sheet_name == "Widows":
            if 'חודש התחלה' in df.columns:
                df['חודש התחלה'] = pd.to_datetime(df['חודש התחלה'], errors='coerce')
        
        # Remove rows that contain headers instead of data
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            # Remove rows where the first column contains header-like text
            df = df[~df['תאריך'].astype(str).str.contains('עמרי|הוצאות|תאריך|שם|לקוח|סכום', na=False)]
            # Remove rows where all columns are empty or contain header-like text
            df = df[~(df['תאריך'].isna() & df['שם'].isna() & df['שקלים'].isna())]
            # Remove rows where name column contains header text
            df = df[~df['שם'].str.contains('שם לקוח|שם תורם|שם משקיע', na=False)]
            # Remove rows where amount column contains header text
            df = df[~df['שקלים'].astype(str).str.contains('סכום', na=False)]
        
        print(f"Final DataFrame shape: {df.shape}")
        return df
    except Exception as e:
        print(f"שגיאה בטעינת נתונים מ-Google Sheets: {e}")
        print(f"Sheet name: {sheet_name}")
        print(f"Spreadsheet ID: {SPREADSHEET_ID}")
        
        # Create empty DataFrame with expected columns instead of falling back to Excel
        if sheet_name == "Widows":
            return pd.DataFrame(columns=['שם ', 'סכום חודשי', 'חודש התחלה', 'מייל', 'טלפון', 'תעודת זהות', 'מספר ילדים', 'חללים', 'הערות', 'תורם', 'איש קשר לתרומה'])
        else:
            return pd.DataFrame(columns=['תאריך', 'שם', 'שקלים'])


def write_sheet(sheet_name: str, df: pd.DataFrame) -> None:
    """Write a DataFrame to a worksheet in Google Sheets (overwrites existing data)."""
    if gc is None:
        # No Excel fallback - just print error
        print("Google Sheets not available - cannot save data")
        return
    
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"Data saved successfully to Google Sheets: {sheet_name}")
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")
        print("Data could not be saved") 