#!/usr/bin/env python3
"""
Network Editor Module
Allows users to edit network connections and automatically sync changes to Google Sheets
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple
from google_sheets_io import read_sheet, write_sheet
import logging

def create_network_editor(almanot_df: pd.DataFrame, donations_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Create an interactive network editor"""
    
    st.markdown("### 🔧 עורך רשת קשרים")
    st.markdown("ערוך את הקשרים בין תורמים לאלמנות ישירות מהדשבורד")
    
    # Create tabs for different editing functions
    tab1, tab2, tab3 = st.tabs(["➕ הוסף קשר", "✏️ ערוך קשר", "🗑️ מחק קשר"])
    
    with tab1:
        create_add_connection_tab(almanot_df, donations_df, investors_df)
    
    with tab2:
        create_edit_connection_tab(almanot_df, donations_df, investors_df)
    
    with tab3:
        create_delete_connection_tab(almanot_df, donations_df, investors_df)

def create_add_connection_tab(almanot_df: pd.DataFrame, donations_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Tab for adding new connections"""
    
    st.markdown("#### הוסף קשר חדש")
    
    # Get all available donors
    all_donors = set()
    if 'שם' in donations_df.columns:
        donors_from_donations = donations_df['שם'].dropna().unique()
        all_donors.update(donors_from_donations)
    
    if 'שם' in investors_df.columns:
        investors_names = investors_df['שם'].dropna().unique()
        all_donors.update(investors_names)
    
    # Get all widows without donors
    widows_without_donors = almanot_df[almanot_df['תורם'].isna() | (almanot_df['תורם'] == '')]
    
    if len(widows_without_donors) == 0:
        st.success("🎉 כל האלמנות כבר מחוברות לתורמים!")
        return
    
    # Create form for adding connection
    with st.form("add_connection_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Select widow
            widow_options = widows_without_donors['שם '].dropna().tolist()
            selected_widow = st.selectbox("בחר אלמנה", widow_options, key="add_widow")
            
            # Show widow details
            if selected_widow:
                widow_data = widows_without_donors[widows_without_donors['שם '] == selected_widow].iloc[0]
                st.info(f"**פרטי אלמנה:**\n- מספר ילדים: {widow_data.get('מספר ילדים', 'N/A')}\n- סכום חודשי נוכחי: ₪{widow_data.get('סכום חודשי', 0):,.0f}")
        
        with col2:
            # Select donor
            donor_options = sorted(list(all_donors))
            selected_donor = st.selectbox("בחר תורם", donor_options, key="add_donor")
            
            # Monthly support amount
            monthly_amount = st.number_input("סכום תמיכה חודשי (₪)", min_value=0, value=1000, step=100, key="add_amount")
        
        # Submit button
        if st.form_submit_button("➕ הוסף קשר", use_container_width=True):
            if add_connection_to_sheets(selected_widow, selected_donor, monthly_amount, almanot_df):
                st.success(f"✅ קשר נוסף בהצלחה: {selected_donor} → {selected_widow} (₪{monthly_amount:,.0f})")
                st.rerun()
            else:
                st.error("❌ שגיאה בהוספת הקשר")

def create_edit_connection_tab(almanot_df: pd.DataFrame, donations_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Tab for editing existing connections"""
    
    st.markdown("#### ערוך קשר קיים")
    
    # Get widows with donors
    widows_with_donors = almanot_df[almanot_df['תורם'].notna() & (almanot_df['תורם'] != '')]
    
    if len(widows_with_donors) == 0:
        st.info("אין קשרים קיימים לעריכה")
        return
    
    # Create form for editing connection
    with st.form("edit_connection_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Select widow to edit
            widow_options = widows_with_donors['שם '].dropna().tolist()
            selected_widow = st.selectbox("בחר אלמנה", widow_options, key="edit_widow")
            
            if selected_widow:
                widow_data = widows_with_donors[widows_with_donors['שם '] == selected_widow].iloc[0]
                current_donor = widow_data.get('תורם', '')
                current_amount = widow_data.get('סכום חודשי', 0)
                
                st.info(f"**קשר נוכחי:**\n- תורם: {current_donor}\n- סכום: ₪{current_amount:,.0f}")
        
        with col2:
            # Get all available donors
            all_donors = set()
            if 'שם' in donations_df.columns:
                donors_from_donations = donations_df['שם'].dropna().unique()
                all_donors.update(donors_from_donations)
            
            if 'שם' in investors_df.columns:
                investors_names = investors_df['שם'].dropna().unique()
                all_donors.update(investors_names)
            
            # Select new donor
            donor_options = sorted(list(all_donors))
            new_donor = st.selectbox("תורם חדש", donor_options, key="edit_donor", index=donor_options.index(current_donor) if current_donor in donor_options else 0)
            
            # New monthly support amount
            new_amount = st.number_input("סכום חדש (₪)", min_value=0, value=int(current_amount), step=100, key="edit_amount")
        
        # Submit button
        if st.form_submit_button("✏️ עדכן קשר", use_container_width=True):
            if update_connection_in_sheets(selected_widow, new_donor, new_amount, almanot_df):
                st.success(f"✅ קשר עודכן בהצלחה: {new_donor} → {selected_widow} (₪{new_amount:,.0f})")
                st.rerun()
            else:
                st.error("❌ שגיאה בעדכון הקשר")

def create_delete_connection_tab(almanot_df: pd.DataFrame, donations_df: pd.DataFrame, investors_df: pd.DataFrame):
    """Tab for deleting connections"""
    
    st.markdown("#### מחק קשר קיים")
    
    # Get widows with donors
    widows_with_donors = almanot_df[almanot_df['תורם'].notna() & (almanot_df['תורם'] != '')]
    
    if len(widows_with_donors) == 0:
        st.info("אין קשרים קיימים למחיקה")
        return
    
    # Create form for deleting connection
    with st.form("delete_connection_form"):
        # Select widow to disconnect
        widow_options = widows_with_donors['שם '].dropna().tolist()
        selected_widow = st.selectbox("בחר אלמנה", widow_options, key="delete_widow")
        
        if selected_widow:
            widow_data = widows_with_donors[widows_with_donors['שם '] == selected_widow].iloc[0]
            current_donor = widow_data.get('תורם', '')
            current_amount = widow_data.get('סכום חודשי', 0)
            
            st.warning(f"**קשר שיימחק:**\n- אלמנה: {selected_widow}\n- תורם: {current_donor}\n- סכום: ₪{current_amount:,.0f}")
            
            # Confirmation checkbox
            confirm_delete = st.checkbox("אני מאשר את מחיקת הקשר", key="confirm_delete")
        
        # Submit button
        if st.form_submit_button("🗑️ מחק קשר", use_container_width=True, disabled=not confirm_delete):
            if delete_connection_from_sheets(selected_widow, almanot_df):
                st.success(f"✅ קשר נמחק בהצלחה: {current_donor} → {selected_widow}")
                st.rerun()
            else:
                st.error("❌ שגיאה במחיקת הקשר")

def add_connection_to_sheets(widow_name: str, donor_name: str, monthly_amount: float, almanot_df: pd.DataFrame) -> bool:
    """Add a new connection to Google Sheets"""
    try:
        # Find the widow in the dataframe
        widow_mask = almanot_df['שם '] == widow_name
        if not widow_mask.any():
            st.error(f"לא נמצאה אלמנה בשם: {widow_name}")
            return False
        
        # Update the widow's donor and monthly amount
        almanot_df.loc[widow_mask, 'תורם'] = donor_name
        almanot_df.loc[widow_mask, 'סכום חודשי'] = monthly_amount
        
        # Write back to Google Sheets
        write_sheet("Widows", almanot_df)
        
        # Update session state
        if 'almanot_df' in st.session_state:
            st.session_state.almanot_df = almanot_df
        
        return True
        
    except Exception as e:
        logging.error(f"Error adding connection: {e}")
        st.error(f"שגיאה בהוספת קשר: {e}")
        return False

def update_connection_in_sheets(widow_name: str, new_donor: str, new_amount: float, almanot_df: pd.DataFrame) -> bool:
    """Update an existing connection in Google Sheets"""
    try:
        # Find the widow in the dataframe
        widow_mask = almanot_df['שם '] == widow_name
        if not widow_mask.any():
            st.error(f"לא נמצאה אלמנה בשם: {widow_name}")
            return False
        
        # Update the widow's donor and monthly amount
        almanot_df.loc[widow_mask, 'תורם'] = new_donor
        almanot_df.loc[widow_mask, 'סכום חודשי'] = new_amount
        
        # Write back to Google Sheets
        write_sheet("Widows", almanot_df)
        
        # Update session state
        if 'almanot_df' in st.session_state:
            st.session_state.almanot_df = almanot_df
        
        return True
        
    except Exception as e:
        logging.error(f"Error updating connection: {e}")
        st.error(f"שגיאה בעדכון קשר: {e}")
        return False

def delete_connection_from_sheets(widow_name: str, almanot_df: pd.DataFrame) -> bool:
    """Delete a connection from Google Sheets"""
    try:
        # Find the widow in the dataframe
        widow_mask = almanot_df['שם '] == widow_name
        if not widow_mask.any():
            st.error(f"לא נמצאה אלמנה בשם: {widow_name}")
            return False
        
        # Remove the donor connection
        almanot_df.loc[widow_mask, 'תורם'] = None
        almanot_df.loc[widow_mask, 'סכום חודשי'] = 0
        
        # Write back to Google Sheets
        write_sheet("Widows", almanot_df)
        
        # Update session state
        if 'almanot_df' in st.session_state:
            st.session_state.almanot_df = almanot_df
        
        return True
        
    except Exception as e:
        logging.error(f"Error deleting connection: {e}")
        st.error(f"שגיאה במחיקת קשר: {e}")
        return False
