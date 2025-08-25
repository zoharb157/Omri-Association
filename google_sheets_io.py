import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from typing import Optional
import os
import streamlit as st

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


def show_service_account_upload():
    """Show UI for uploading/pasting a new Google service account key, validate, and save if valid."""
    st.markdown("""
### לא נמצא מפתח Google Sheets תקין

1. לחץ על הכפתור כדי לפתוח את עמוד יצירת המפתח ב-Google Cloud:
""")
    st.link_button("פתח עמוד יצירת מפתח ב-Google Cloud", "https://console.cloud.google.com/iam-admin/serviceaccounts")
    st.markdown("""
2. צור מפתח חדש (JSON) והעתק את כל התוכן.
3. הדבק את תוכן המפתח כאן:
""")
    key_input = st.text_area("הדבק כאן את תוכן קובץ המפתח (JSON)", height=300)
    if st.button("בדוק ושמור מפתח חדש"):
        import json
        from google.auth.exceptions import DefaultCredentialsError
        import io
        try:
            key_data = json.loads(key_input)
            # בדיקה בסיסית
            required_fields = ["type", "private_key", "client_email", "token_uri"]
            for field in required_fields:
                if field not in key_data or not key_data[field]:
                    st.error(f"המפתח חסר שדה חובה: {field}")
                    return False
            # בדוק את המפתח מול Google
            from google.oauth2.service_account import Credentials
            from google.auth.transport.requests import Request
            creds = Credentials.from_service_account_info(key_data, scopes=SCOPES)
            creds.refresh(Request())
            # אם הגענו לכאן – המפתח תקין
            with open(SERVICE_ACCOUNT_FILE, 'w', encoding='utf-8') as f:
                json.dump(key_data, f, ensure_ascii=False, indent=2)
            st.success("✅ המפתח נשמר בהצלחה! המערכת תיטען מחדש.")
            st.rerun()
        except Exception as e:
            st.error(f"המפתח לא תקין או לא ניתן לאימות מול Google.\n\nשגיאה: {e}")
        return False


def check_service_account_validity():
    """Check if the service account key is valid and display a user-friendly error if not, including setup instructions."""
    import json
    from google.auth.exceptions import DefaultCredentialsError
    from google.auth.transport.requests import Request
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            show_service_account_upload()
            return False
        with open(SERVICE_ACCOUNT_FILE, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
        # Basic checks
        required_fields = ["type", "private_key", "client_email", "token_uri"]
        for field in required_fields:
            if field not in key_data or not key_data[field]:
                show_service_account_upload()
                return False
        # Try to create credentials and get a token
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        # Try to get a token (will fail if key is invalid/expired)
        creds.refresh(Request())
        return True
    except Exception as e:
        show_service_account_upload()
        return False


def show_google_sheets_setup_instructions():
    """Display the most important Google Sheets setup instructions for non-technical users."""
    st.markdown("""
### איך להפעיל את המערכת עם Google Sheets?

1. **הורד מפתח חדש:**
   - היכנס ל-Google Cloud Console > IAM & Admin > Service Accounts
   - בחר את החשבון (או צור חדש)
   - עבור ל-Keys > Add Key > Create new key > JSON
   - הורד את הקובץ ושמור אותו בשם `service_account.json` בתיקיית המערכת

2. **שתף את הגיליון עם המייל של הסרוויס:**
   - פתח את Google Sheets
   - לחץ על 'שתף' והוסף את כתובת המייל של הסרוויס (מופיעה למטה)
   - תן הרשאת עריכה

3. **הרץ שוב את המערכת**

---
    """)
    # Try to show the service account email if possible
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            import json
            with open(SERVICE_ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                key_data = json.load(f)
            email = key_data.get("client_email", None)
            if email:
                st.info(f"""**כתובת המייל של הסרוויס:**
```
{email}
```
[העתק/י את הכתובת והוסף/י אותה לשיתוף הגיליון]""")
    except Exception:
        pass


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
            # Map the actual columns to expected columns - simplified
            column_mapping = {}
            
            # Map based on actual column names from the test
            for col in df.columns:
                col_str = str(col).strip()
                if col_str == 'NaT':
                    column_mapping[col] = 'תאריך'
                elif col_str == 'שם לקוח':
                    column_mapping[col] = 'שם'
                elif col_str == 'סכום':
                    column_mapping[col] = 'שקלים'
            
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
            # Similar mapping for donations - simplified
            column_mapping = {}
            
            # Map based on actual column names from the test
            for col in df.columns:
                col_str = str(col).strip()
                if col_str == 'NaT':
                    column_mapping[col] = 'תאריך'
                elif col_str == 'שם התורם':
                    column_mapping[col] = 'שם'
                elif col_str == 'סכום':
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
            # Similar mapping for investors - simplified
            column_mapping = {}
            
            # Map based on actual column names from the test
            for col in df.columns:
                col_str = str(col).strip()
                if col_str == 'NaT':
                    column_mapping[col] = 'תאריך'
                elif col_str == 'שם התורם':
                    column_mapping[col] = 'שם'
                elif col_str == 'סכום':
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
            # Mapping for widows sheet - simplified mapping based on actual data
            column_mapping = {}
            
            # Map based on actual column names from the test
            for col in df.columns:
                col_str = str(col).strip()
                if col_str == 'שם':
                    column_mapping[col] = 'שם '
                elif col_str == 'סכום חודשי':
                    column_mapping[col] = 'סכום חודשי'
                elif col_str == 'חודש התחלה':
                    column_mapping[col] = 'חודש התחלה'
                elif col_str == 'מייל':
                    column_mapping[col] = 'מייל'
                elif col_str == 'טלפון':
                    column_mapping[col] = 'טלפון'
                elif col_str == 'תעודת זהות':
                    column_mapping[col] = 'תעודת זהות'
                elif col_str == 'מספר ילדים':
                    column_mapping[col] = 'מספר ילדים'
                elif col_str == 'חללים':
                    column_mapping[col] = 'חללים'
                elif col_str == 'הערות':
                    column_mapping[col] = 'הערות'
                elif col_str == 'תורם':
                    column_mapping[col] = 'תורם'
                elif col_str == 'איש קשר לתרומה':
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
            "Widows": "Almanot",  # Map Widows to Almanot
            "Widows": "Almanot"   # Ensure both names map to Almanot
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
        
        # Map columns to expected names
        df = _map_columns_to_expected(df, sheet_name)
        
        # Convert date columns to datetime
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            if 'תאריך' in df.columns:
                df['תאריך'] = pd.to_datetime(df['תאריך'], errors='coerce')
        elif sheet_name == "Widows":
            if 'חודש התחלה' in df.columns:
                df['חודש התחלה'] = pd.to_datetime(df['חודש התחלה'], errors='coerce')
        
        # Convert amount columns to numeric - handle string amounts
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            if 'שקלים' in df.columns:
                # First clean the data - remove any non-numeric characters except decimal points
                df['שקלים'] = df['שקלים'].astype(str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to numeric, handling empty strings and invalid values
                df['שקלים'] = pd.to_numeric(df['שקלים'], errors='coerce')
                # Fill NaN values with 0
                df['שקלים'] = df['שקלים'].fillna(0)
        
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