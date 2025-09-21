import logging
import os

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

# Define the scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Get configuration from environment variables and Streamlit secrets
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo")
WIDOW_SPREADSHEET_ID = os.getenv(
    "WIDOW_SPREADSHEET_ID", "1FQRFhChBVUI8G7GrJW8BZInxJ2F25UhMT-fj-O6odv8"
)

# Global Google Sheets client - will be initialized when needed
gc = None


def get_google_sheets_client():
    """Get Google Sheets client, initializing it if needed"""
    global gc
    if gc is not None:
        return gc

    try:
        # Debug: Check what's available in Streamlit secrets
        logging.info(f"Streamlit secrets available: {hasattr(st, 'secrets')}")
        if hasattr(st, "secrets"):
            logging.info(
                f"Secrets keys: {list(st.secrets.keys()) if hasattr(st.secrets, 'keys') else 'No keys method'}"
            )
            logging.info(f"Service account in secrets: {'service_account' in st.secrets}")
            logging.info(f"'secrets' key in secrets: {'secrets' in st.secrets}")
            if "secrets" in st.secrets:
                logging.info(f"'secrets' key type: {type(st.secrets['secrets'])}")
                logging.info(
                    f"'secrets' key content preview: {str(st.secrets['secrets'])[:100]}..."
                )

        # Try to get service account from Streamlit secrets first
        if hasattr(st, "secrets") and (
            "service_account" in st.secrets
            or ("secrets" in st.secrets and "service_account" in st.secrets["secrets"])
        ):
            import json

            # Try service_account first, then fallback to secrets
            if "service_account" in st.secrets:
                secret_value = st.secrets["service_account"]
            else:
                # Check if secrets contains a service_account key
                if hasattr(st.secrets["secrets"], "service_account"):
                    secret_value = st.secrets["secrets"]["service_account"]
                else:
                    secret_value = st.secrets["secrets"]

            # Handle different secret structures
            if isinstance(secret_value, str):
                # If it's a string, try to parse as JSON
                try:
                    # Clean the JSON string to handle common issues
                    cleaned_json = secret_value.strip()
                    # Remove any control characters that might cause issues
                    import re

                    cleaned_json = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned_json)
                    service_account_info = json.loads(cleaned_json)
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse secret as JSON: {e}")
                    logging.error(f"JSON content preview: {secret_value[:200]}...")
                    return None
            elif isinstance(secret_value, (dict, type(st.secrets))):
                # If it's already a dict or AttrDict, use it directly
                service_account_info = secret_value
            else:
                logging.error(f"Unexpected secret type: {type(secret_value)}")
                return None

            creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
            gc = gspread.authorize(creds)
            logging.info(
                "Google Sheets connection established successfully using Streamlit secrets!"
            )
            return gc
        elif os.path.exists(SERVICE_ACCOUNT_FILE):
            # Fallback to file-based authentication
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            gc = gspread.authorize(creds)
            logging.info("Google Sheets connection established successfully using file!")
            return gc
        else:
            logging.warning(
                "No service account found in secrets or file. Falling back to Excel files."
            )
            return None
    except Exception as e:
        logging.warning(f"Could not connect to Google Sheets: {e}. Falling back to Excel files.")
        return None


def show_service_account_upload():
    """Show UI for uploading/pasting a new Google service account key, validate, and save if valid."""
    st.markdown(
        """
### לא נמצא מפתח Google Sheets תקין

1. לחץ על הכפתור כדי לפתוח את עמוד יצירת המפתח ב-Google Cloud:
"""
    )
    st.link_button(
        "פתח עמוד יצירת מפתח ב-Google Cloud",
        "https://console.cloud.google.com/iam-admin/serviceaccounts",
    )
    st.markdown(
        """
2. צור מפתח חדש (JSON) והעתק את כל התוכן.
3. הדבק את תוכן המפתח כאן:
"""
    )
    key_input = st.text_area("הדבק כאן את תוכן קובץ המפתח (JSON)", height=300)
    if st.button("בדוק ושמור מפתח חדש"):
        import json

        try:
            key_data = json.loads(key_input)
            # בדיקה בסיסית
            required_fields = ["type", "private_key", "client_email", "token_uri"]
            for field in required_fields:
                if field not in key_data or not key_data[field]:
                    st.error(f"המפתח חסר שדה חובה: {field}")
                    return False
            # בדוק את המפתח מול Google
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials

            creds = Credentials.from_service_account_info(key_data, scopes=SCOPES)
            creds.refresh(Request())
            # אם הגענו לכאן – המפתח תקין
            with open(SERVICE_ACCOUNT_FILE, "w", encoding="utf-8") as f:
                json.dump(key_data, f, ensure_ascii=False, indent=2)
            st.success("✅ המפתח נשמר בהצלחה! המערכת תיטען מחדש.")
            st.rerun()
        except Exception as e:
            st.error(f"המפתח לא תקין או לא ניתן לאימות מול Google.\n\nשגיאה: {e}")
        return False


def check_service_account_validity():
    """Check if the service account key is valid and display a user-friendly error if not, including setup instructions."""
    import json

    from google.auth.transport.requests import Request

    try:
        # Debug: Check what's available in Streamlit secrets
        logging.info(f"Validation - Streamlit secrets available: {hasattr(st, 'secrets')}")
        if hasattr(st, "secrets"):
            logging.info(
                f"Validation - Secrets keys: {list(st.secrets.keys()) if hasattr(st.secrets, 'keys') else 'No keys method'}"
            )
            logging.info(
                f"Validation - Service account in secrets: {'service_account' in st.secrets}"
            )
            logging.info(f"Validation - 'secrets' key in secrets: {'secrets' in st.secrets}")
            if "secrets" in st.secrets:
                logging.info(f"Validation - 'secrets' key type: {type(st.secrets['secrets'])}")
                logging.info(
                    f"Validation - 'secrets' key content preview: {str(st.secrets['secrets'])[:100]}..."
                )
                logging.info(
                    f"Validation - 'service_account' in st.secrets['secrets']: {'service_account' in st.secrets['secrets']}"
                )
                logging.info(
                    f"Validation - hasattr(st.secrets['secrets'], 'service_account'): {hasattr(st.secrets['secrets'], 'service_account')}"
                )

        # Check Streamlit secrets first
        condition1 = "service_account" in st.secrets
        condition2 = "secrets" in st.secrets and "service_account" in st.secrets["secrets"]
        logging.info(f"Validation - condition1 (service_account in st.secrets): {condition1}")
        logging.info(
            f"Validation - condition2 (secrets in st.secrets and service_account in st.secrets['secrets']): {condition2}"
        )
        logging.info(
            f"Validation - overall condition: {hasattr(st, 'secrets') and (condition1 or condition2)}"
        )

        if hasattr(st, "secrets") and (condition1 or condition2):
            logging.info("Validation - ENTERING validation block - secrets found!")
            # Try service_account first, then fallback to secrets
            if "service_account" in st.secrets:
                secret_value = st.secrets["service_account"]
                logging.info("Validation - Using direct service_account from st.secrets")
            else:
                # Check if secrets contains a service_account key
                if hasattr(st.secrets["secrets"], "service_account"):
                    secret_value = st.secrets["secrets"]["service_account"]
                    logging.info("Validation - Using service_account from st.secrets['secrets']")
                else:
                    secret_value = st.secrets["secrets"]
                    logging.info("Validation - Using entire st.secrets['secrets']")

            logging.info(f"Validation - secret_value type: {type(secret_value)}")
            logging.info(f"Validation - secret_value preview: {str(secret_value)[:100]}...")

            # Handle different secret structures
            if isinstance(secret_value, str):
                logging.info("Validation - Processing secret as string (JSON)")
                # If it's a string, try to parse as JSON
                try:
                    # Clean the JSON string to handle common issues
                    cleaned_json = secret_value.strip()
                    # Remove any control characters that might cause issues
                    import re

                    cleaned_json = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned_json)
                    key_data = json.loads(cleaned_json)
                    logging.info("Validation - Successfully parsed JSON secret")
                except json.JSONDecodeError as e:
                    logging.error(f"Validation - Failed to parse secret as JSON: {e}")
                    logging.error(f"Validation - JSON content preview: {secret_value[:200]}...")
                    show_service_account_upload()
                    return False
            elif isinstance(secret_value, (dict, type(st.secrets))):
                # If it's already a dict or AttrDict, use it directly
                key_data = secret_value
            else:
                logging.error(f"Validation - Unexpected secret type: {type(secret_value)}")
                show_service_account_upload()
                return False

            # Basic checks
            required_fields = ["type", "private_key", "client_email", "token_uri"]
            for field in required_fields:
                if field not in key_data or not key_data[field]:
                    logging.warning(f"Validation - Missing field in secrets: {field}")
                    show_service_account_upload()
                    return False

            # Debug the private key format
            private_key = key_data.get("private_key", "")
            logging.info(f"Validation - Private key length: {len(private_key)}")
            logging.info(f"Validation - Private key starts with: {private_key[:50]}...")
            logging.info(f"Validation - Private key ends with: ...{private_key[-50:]}")
            newline_check = "\n" in private_key
            escaped_newline_check = "\\n" in private_key
            logging.info(f"Validation - Private key contains newlines: {newline_check}")
            logging.info(
                f"Validation - Private key contains escaped newlines: {escaped_newline_check}"
            )

            # Fix private key formatting if needed
            if "\\\\n" in private_key:
                logging.info("Validation - Fixing escaped newlines in private key")
                key_data["private_key"] = private_key.replace("\\\\n", "\\n")
            elif "\\n" in private_key and "\n" not in private_key:
                logging.info(
                    "Validation - Converting escaped newlines to actual newlines in private key"
                )
                key_data["private_key"] = private_key.replace("\\n", "\n")

            # Try to create credentials and get a token
            logging.info("Validation - Creating credentials from service account info")
            try:
                creds = Credentials.from_service_account_info(key_data, scopes=SCOPES)
                logging.info("Validation - Credentials created successfully")
                # Try to get a token (will fail if key is invalid/expired)
                logging.info("Validation - Refreshing credentials token")
                creds.refresh(Request())
                logging.info("Validation - Service account from secrets is valid!")
                return True
            except Exception as e:
                logging.error(f"Validation - Error creating credentials or refreshing token: {e}")
                logging.error(f"Validation - Error type: {type(e)}")
            show_service_account_upload()
            return False
        elif os.path.exists(SERVICE_ACCOUNT_FILE):
            with open(SERVICE_ACCOUNT_FILE, encoding="utf-8") as f:
                key_data = json.load(f)
            # Basic checks
            required_fields = ["type", "private_key", "client_email", "token_uri"]
            for field in required_fields:
                if field not in key_data or not key_data[field]:
                    show_service_account_upload()
                    return False
            # Try to create credentials and get a token
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            # Try to get a token (will fail if key is invalid/expired)
            creds.refresh(Request())
            return True
        else:
            show_service_account_upload()
            return False
    except Exception:
        show_service_account_upload()
        return False


def show_google_sheets_setup_instructions():
    """Display the most important Google Sheets setup instructions for non-technical users."""
    st.markdown(
        """
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
    """
    )
    # Try to show the service account email if possible
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            import json

            with open(SERVICE_ACCOUNT_FILE, encoding="utf-8") as f:
                key_data = json.load(f)
            email = key_data.get("client_email", None)
            if email:
                st.info(
                    f"""**כתובת המייל של הסרוויס:**
```
{email}
```
[העתק/י את הכתובת והוסף/י אותה לשיתוף הגיליון]"""
                )
    except Exception:
        pass


def _fix_headers(headers):
    """Return a list of unique, non-empty headers. Empty headers get a default name. Duplicates get a suffix."""
    seen = {}
    fixed = []
    for i, h in enumerate(headers):
        name = h.strip() if isinstance(h, str) else ""
        if not name:
            name = f"עמודה_{i+1}"
        orig_name = name
        count = seen.get(name, 0)
        if count:
            name = f"{orig_name}_{count+1}"
        seen[orig_name] = count + 1
        fixed.append(name)
    return fixed


def _map_columns_to_expected(df, sheet_name):
    """Map actual columns from Google Sheets to expected column names"""
    try:
        if sheet_name == "Expenses":
            column_mapping = {}

            for col in df.columns:
                col_str = str(col).strip()
                if col_str == "NaT":
                    column_mapping[col] = "תאריך"
                elif col_str in ("שם לקוח", "שם ספק"):
                    column_mapping[col] = "שם"
                elif col_str == "סכום":
                    column_mapping[col] = "שקלים"

            df = df.rename(columns=column_mapping)

            expected_columns = ["תאריך", "שם", "שקלים"]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            return df[expected_columns]

        elif sheet_name == "Donations":
            column_mapping = {}

            for col in df.columns:
                col_str = str(col).strip()
                if col_str == "NaT":
                    column_mapping[col] = "תאריך"
                elif col_str in ("שם התורם", "שם", "שם לקוח"):
                    column_mapping[col] = "שם"
                elif col_str == "סכום":
                    column_mapping[col] = "שקלים"

            df = df.rename(columns=column_mapping)

            expected_columns = ["תאריך", "שם", "שקלים"]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            return df[expected_columns]

        elif sheet_name == "Investors":
            column_mapping = {}

            for col in df.columns:
                col_str = str(col).strip()
                if col_str == "NaT":
                    column_mapping[col] = "תאריך"
                elif col_str in ("שם התורם", "שם לקוח", "שם"):
                    column_mapping[col] = "שם"
                elif col_str == "סכום":
                    column_mapping[col] = "שקלים"

            df = df.rename(columns=column_mapping)

            expected_columns = ["תאריך", "שם", "שקלים"]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            return df[expected_columns]

        elif sheet_name == "Widows":
            # Mapping for widows sheet - simplified mapping based on actual data
            column_mapping = {}

            # Map based on actual column names from the test
            for col in df.columns:
                col_str = str(col).strip()
                if col_str == "שם":
                    column_mapping[col] = "שם "
                elif col_str == "סכום חודשי":
                    column_mapping[col] = "סכום חודשי"
                elif col_str == "חודש התחלה":
                    column_mapping[col] = "חודש התחלה"
                elif col_str == "מייל":
                    column_mapping[col] = "מייל"
                elif col_str == "טלפון":
                    column_mapping[col] = "טלפון"
                elif col_str == "תעודת זהות":
                    column_mapping[col] = "תעודת זהות"
                elif col_str == "מספר ילדים":
                    column_mapping[col] = "מספר ילדים"
                elif col_str == "חללים":
                    column_mapping[col] = "חללים"
                elif col_str == "הערות":
                    column_mapping[col] = "הערות"
                elif col_str == "תורם":
                    column_mapping[col] = "תורם"
                elif col_str == "איש קשר לתרומה":
                    column_mapping[col] = "איש קשר לתרומה"

            df = df.rename(columns=column_mapping)

            expected_columns = [
                "שם ",
                "סכום חודשי",
                "חודש התחלה",
                "מייל",
                "טלפון",
                "תעודת זהות",
                "מספר ילדים",
                "חללים",
                "הערות",
                "תורם",
                "איש קשר לתרומה",
            ]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            return df

        return df
    except Exception as e:
        logging.error(f"Error in column mapping for {sheet_name}: {e}")
        # Return the original DataFrame if mapping fails
        return df


def read_sheet(sheet_name: str) -> pd.DataFrame:
    """Read a worksheet from Google Sheets and return as a DataFrame."""
    gc = get_google_sheets_client()
    if gc is None:
        # No Excel fallback - return empty DataFrame with expected columns
        logging.warning("Google Sheets not available - returning empty DataFrame")
        if sheet_name == "Widows":
            return pd.DataFrame(
                columns=[
                    "שם ",
                    "סכום חודשי",
                    "חודש התחלה",
                    "מייל",
                    "טלפון",
                    "תעודת זהות",
                    "מספר ילדים",
                    "חללים",
                    "הערות",
                    "תורם",
                    "איש קשר לתרומה",
                ]
            )
        else:
            return pd.DataFrame(columns=["תאריך", "שם", "שקלים"])

    try:
        sh = gc.open_by_key(SPREADSHEET_ID)

        # Map sheet names to actual Google Sheets names
        sheet_mapping = {"Widows": "Almanot"}  # Ensure both names map to Almanot

        actual_sheet_name = sheet_mapping.get(sheet_name, sheet_name)
        worksheet = sh.worksheet(actual_sheet_name)

        # Get all values (including header row)
        values = worksheet.get_all_values()
        if not values:
            logging.warning(f"Sheet '{actual_sheet_name}' is empty")
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
                logging.warning(f"Sheet '{actual_sheet_name}' has insufficient data")
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
            if "תאריך" in df.columns:
                df["תאריך"] = pd.to_datetime(df["תאריך"], errors="coerce")
        elif sheet_name == "Widows":
            if "חודש התחלה" in df.columns:
                df["חודש התחלה"] = pd.to_datetime(df["חודש התחלה"], errors="coerce")

        # Convert amount columns to numeric - handle string amounts
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            if "שקלים" in df.columns:
                # First clean the data - remove any non-numeric characters except decimal points
                df["שקלים"] = df["שקלים"].astype(str).str.replace(r"[^\d.-]", "", regex=True)
                # Convert to numeric, handling empty strings and invalid values
                df["שקלים"] = pd.to_numeric(df["שקלים"], errors="coerce")
                # Fill NaN values with 0
                df["שקלים"] = df["שקלים"].fillna(0)

        # Remove rows that contain headers instead of data
        if sheet_name in ["Expenses", "Donations", "Investors"]:
            # Remove rows where the first column contains header-like text
            df = df[
                ~df["תאריך"].astype(str).str.contains("עמרי|הוצאות|תאריך|שם|לקוח|סכום", na=False)
            ]
            # Remove rows where all columns are empty or contain header-like text
            df = df[~(df["תאריך"].isna() & df["שם"].isna() & df["שקלים"].isna())]
            # Remove rows where name column contains header text
            df = df[~df["שם"].str.contains("שם לקוח|שם תורם|שם משקיע", na=False)]
            # Remove rows where amount column contains header text
            df = df[~df["שקלים"].astype(str).str.contains("סכום", na=False)]

        return df
    except Exception as e:
        logging.error(f"שגיאה בטעינת נתונים מ-Google Sheets: {e}")
        logging.error(f"Sheet name: {sheet_name}")
        logging.error(f"Spreadsheet ID: {SPREADSHEET_ID}")

        # Create empty DataFrame with expected columns instead of falling back to Excel
        if sheet_name == "Widows":
            return pd.DataFrame(
                columns=[
                    "שם ",
                    "סכום חודשי",
                    "חודש התחלה",
                    "מייל",
                    "טלפון",
                    "תעודת זהות",
                    "מספר ילדים",
                    "חללים",
                    "הערות",
                    "תורם",
                    "איש קשר לתרומה",
                ]
            )
        else:
            return pd.DataFrame(columns=["תאריך", "שם", "שקלים"])


def write_sheet(sheet_name: str, df: pd.DataFrame) -> None:
    """Write a DataFrame to a worksheet in Google Sheets (overwrites existing data)."""
    gc = get_google_sheets_client()
    if gc is None:
        # No Excel fallback - just print error
        logging.warning("Google Sheets not available - cannot save data")
        return

    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        logging.info(f"Data saved successfully to Google Sheets: {sheet_name}")
    except Exception as e:
        logging.error(f"Error writing to Google Sheets: {e}")
        logging.error("Data could not be saved")


def load_all_data():
    """Load ALL data from ALL sheets in the Google Spreadsheet."""
    gc = get_google_sheets_client()
    if gc is None:
        logging.warning("Google Sheets not available")
        return {}

    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        all_data = {}

        for ws in sh.worksheets():
            try:
                values = ws.get_all_values()

                if not values:
                    all_data[ws.title] = pd.DataFrame()
                    continue

                # For financial sheets (Expenses, Donations, Investors), skip the first 2 rows
                # Row 0: Title (e.g., "עמרי למען משפחות השכול- הוצאות")
                # Row 1: Headers (e.g., "תאריך", "שם לקוח", "סכום")
                # Row 2+: Data
                if ws.title in ["Expenses", "Donations", "Investors"]:
                    if len(values) >= 3:
                        headers = _fix_headers(values[1])  # Use row 1 as headers
                        data = values[2:]  # Start from row 2
                    else:
                        all_data[ws.title] = pd.DataFrame()
                        continue
                else:
                    # For other sheets, use first row as headers
                    headers = _fix_headers(values[0])
                    data = values[1:]

                # Create DataFrame
                df = pd.DataFrame(data, columns=headers)

                # Clean the data
                df = df.replace("", pd.NA)

                # Apply the same column mapping logic as read_sheet()
                df = _map_columns_to_expected(df, ws.title)

                # Convert date columns first (before numeric conversion)
                for col in df.columns:
                    col_lower = str(col).lower()
                    # Exclude 'סכום חודשי' from date processing - it's a monetary column, not a date
                    if (
                        any(keyword in col_lower for keyword in ["תאריך", "date", "חודש", "month"])
                        and "סכום" not in col_lower
                    ):
                        df[col] = pd.to_datetime(df[col], errors="coerce")

                # Convert numeric columns (only for amount columns, not date columns)
                for col in df.columns:
                    col_lower = str(col).lower()
                    if any(
                        keyword in col_lower
                        for keyword in ["סכום", "amount", "שקלים", "מחיר", "price", "חודשי"]
                    ):
                        # Clean and convert numeric columns
                        df[col] = df[col].astype(str).str.replace(r"[^\d.,-]", "", regex=True)
                        df[col] = df[col].str.replace(",", ".")
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                        df[col] = df[col].fillna(0)

                all_data[ws.title] = df
            except Exception as e:
                logging.error(f"Error loading sheet '{ws.title}': {e}")
                all_data[ws.title] = pd.DataFrame()
        return all_data

    except Exception as e:
        logging.error(f"Error loading all data: {e}")
        return {}


def read_widow_support_data() -> pd.DataFrame:
    """Read widow support data from the new widow support spreadsheet."""
    gc = get_google_sheets_client()
    if gc is None:
        logging.warning("Google Sheets not available - returning empty DataFrame")
        return pd.DataFrame(
            columns=[
                "שם הבחורה",
                "כמה ילדים",
                "סכום חודשי",
                "מתי התחילה לקבל",
                "עד מתי תחת תורם",
                "כמה מקבלת בכל חודש",
                "תורם",
            ]
        )

    try:
        # Open the widow support spreadsheet
        sh = gc.open_by_key(WIDOW_SPREADSHEET_ID)

        # Try to find the correct worksheet
        # The gid parameter suggests it might be a specific worksheet
        try:
            # Try "Widows Support" first
            worksheet = sh.worksheet("Widows Support")
        except Exception:
            try:
                # Try other possible names
                worksheet = sh.worksheet("Widows")
            except Exception:
                try:
                    worksheet = sh.worksheet("Almanot")
                except Exception:
                    # Get the first worksheet if none of the above work
                    worksheet = sh.sheet1

        # Get all values
        values = worksheet.get_all_values()
        if not values:
            logging.warning("Widow support sheet is empty")
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])  # First row as headers

        # Clean the data
        df = df.replace("", pd.NA)

        logging.info(f"Widow support data loaded: {len(df)} rows")
        return df

    except Exception as e:
        logging.error(f"Error reading widow support data: {e}")
        return pd.DataFrame()
