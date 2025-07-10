"""
Data Management Functions for the Omri Association Dashboard
"""

import streamlit as st
import pandas as pd
from google_sheets_io import write_sheet
import logging

def save_expenses_data(expenses_df):
    """Save expenses data to Google Sheets"""
    try:
        write_sheet('Expenses', expenses_df)
        st.success("נתוני הוצאות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני הוצאות: {str(e)}")
        logging.error(f"Error saving expenses data: {str(e)}")

def save_donations_data(donations_df):
    """Save donations data to Google Sheets"""
    try:
        write_sheet('Donations', donations_df)
        st.success("נתוני תרומות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני תרומות: {str(e)}")
        logging.error(f"Error saving donations data: {str(e)}")

def save_widows_data(almanot_df):
    """Save widows data to Google Sheets"""
    try:
        write_sheet('Almanot', almanot_df)
        st.success("נתוני אלמנות נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני אלמנות: {str(e)}")
        logging.error(f"Error saving widows data: {str(e)}")

def save_investors_data(investors_df):
    """Save investors data to Google Sheets"""
    try:
        write_sheet('Investors', investors_df)
        st.success("נתוני משקיעים נשמרו בהצלחה!")
    except Exception as e:
        st.error(f"שגיאה בשמירת נתוני משקיעים: {str(e)}")
        logging.error(f"Error saving investors data: {str(e)}")

def get_edge_color(amount):
    """Get color for network graph edges based on amount"""
    if amount >= 10000:
        return "#dc2626"  # Red for high amounts
    elif amount >= 5000:
        return "#ea580c"  # Orange for medium-high amounts
    elif amount >= 2000:
        return "#d97706"  # Yellow for medium amounts
    else:
        return "#059669"  # Green for low amounts

def extract_amount_from_title(title):
    """Extract amount from title string"""
    try:
        # Look for numbers in the title
        import re
        numbers = re.findall(r'\d+', str(title))
        if numbers:
            return int(numbers[0])
        return 0
    except:
        return 0

def update_connection_in_data(donor_name, widow_name, amount):
    """Update connection data in the widows DataFrame"""
    try:
        # Get current data
        if 'almanot_df' in st.session_state:
            almanot_df = st.session_state.almanot_df.copy()
            
            # Find the widow and update the donor and amount
            mask = almanot_df['שם'] == widow_name
            if mask.any():
                almanot_df.loc[mask, 'תורם'] = donor_name
                almanot_df.loc[mask, 'סכום חודשי'] = amount
                
                # Update session state
                st.session_state.almanot_df = almanot_df
                
                # Save to Google Sheets
                save_widows_data(almanot_df)
                
                return True
        return False
    except Exception as e:
        st.error(f"שגיאה בעדכון הקשר: {str(e)}")
        logging.error(f"Error updating connection: {str(e)}")
        return False

def remove_connection_from_data(donor_name, widow_name):
    """Remove connection data from the widows DataFrame"""
    try:
        # Get current data
        if 'almanot_df' in st.session_state:
            almanot_df = st.session_state.almanot_df.copy()
            
            # Find the widow and remove the donor
            mask = almanot_df['שם'] == widow_name
            if mask.any():
                almanot_df.loc[mask, 'תורם'] = ''
                almanot_df.loc[mask, 'סכום חודשי'] = 0
                
                # Update session state
                st.session_state.almanot_df = almanot_df
                
                # Save to Google Sheets
                save_widows_data(almanot_df)
                
                return True
        return False
    except Exception as e:
        st.error(f"שגיאה בהסרת הקשר: {str(e)}")
        logging.error(f"Error removing connection: {str(e)}")
        return False 