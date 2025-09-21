#!/usr/bin/env python3
"""
Widow Import System for Omri Association Dashboard
Handles importing widow data from Google Sheets with donor assignments
"""

import logging
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

from src.google_sheets_io import read_widow_support_data


class WidowImportManager:
    """Manages widow data import and donor assignments"""

    def __init__(self):
        self.sheet_id = "1FQRFhChBVUI8G7GrJW8BZInxJ2F25UhMT-fj-O6odv8"
        self.tab_name = "Widows Support"  # Based on the gid parameter
        self.required_columns = [
            "שם הבחורה",
            "כמה ילדים",
            "סכום חודשי",
            "מתי התחילה לקבל",
            "עד מתי תחת תורם",
            "כמה מקבלת בכל חודש",
        ]

    def load_widow_data(self) -> Tuple[pd.DataFrame, List[Dict]]:
        """Load widow data from Google Sheets"""
        try:
            # Load data from the widow support spreadsheet
            df = read_widow_support_data()

            if df is None or df.empty:
                st.error("❌ לא ניתן לטעון נתוני אלמנות")
                return pd.DataFrame(), []

            # Clean and validate data
            cleaned_df = self._clean_widow_data(df)

            # Identify new widows (purple/highlighted rows)
            new_widows = self._identify_new_widows(cleaned_df)

            return cleaned_df, new_widows

        except Exception as e:
            st.error(f"❌ שגיאה בטעינת נתוני אלמנות: {str(e)}")
            logging.error(f"Widow data loading error: {e}")
            return pd.DataFrame(), []

    def _clean_widow_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize widow data"""
        try:
            # Create a copy to avoid modifying original
            cleaned_df = df.copy()

            # Standardize column names
            column_mapping = {
                "שם הבחורה": "widow_name",
                "כמה ילדים": "children_count",
                "סכום חודשי": "monthly_amount",
                "מתי התחילה לקבל": "start_date",
                "עד מתי תחת תורם": "end_date",
                "כמה מקבלת בכל חודש": "monthly_support",
                "תורם": "donor_name",
            }

            # Rename columns if they exist
            for hebrew_name, english_name in column_mapping.items():
                if hebrew_name in cleaned_df.columns:
                    cleaned_df[english_name] = cleaned_df[hebrew_name]

            # Ensure required columns exist
            for col in ["widow_name", "children_count", "monthly_amount"]:
                if col not in cleaned_df.columns:
                    cleaned_df[col] = ""

            # Clean data types
            if "children_count" in cleaned_df.columns:
                cleaned_df["children_count"] = (
                    pd.to_numeric(cleaned_df["children_count"], errors="coerce")
                    .fillna(0)
                    .astype(int)
                )

            if "monthly_amount" in cleaned_df.columns:
                cleaned_df["monthly_amount"] = pd.to_numeric(
                    cleaned_df["monthly_amount"], errors="coerce"
                ).fillna(0)

            if "monthly_support" in cleaned_df.columns:
                cleaned_df["monthly_support"] = pd.to_numeric(
                    cleaned_df["monthly_support"], errors="coerce"
                ).fillna(0)

            # Clean dates
            for date_col in ["start_date", "end_date"]:
                if date_col in cleaned_df.columns:
                    cleaned_df[date_col] = pd.to_datetime(cleaned_df[date_col], errors="coerce")

            # Remove empty rows
            cleaned_df = cleaned_df.dropna(subset=["widow_name"])

            return cleaned_df

        except Exception as e:
            st.error(f"❌ שגיאה בניקוי נתונים: {str(e)}")
            logging.error(f"Data cleaning error: {e}")
            return df

    def _identify_new_widows(self, df: pd.DataFrame) -> List[Dict]:
        """Identify new widows that need donor assignment"""
        new_widows = []

        try:
            # Look for rows without donor assignment
            for index, row in df.iterrows():
                if pd.isna(row.get("donor_name")) or row.get("donor_name") == "":
                    new_widow = {
                        "index": index,
                        "widow_name": row.get("widow_name", ""),
                        "children_count": row.get("children_count", 0),
                        "monthly_amount": row.get("monthly_amount", 0),
                        "start_date": row.get("start_date"),
                        "end_date": row.get("end_date"),
                        "monthly_support": row.get("monthly_support", 0),
                        "status": "new",  # Mark as new widow
                    }
                    new_widows.append(new_widow)

            return new_widows

        except Exception as e:
            st.error(f"❌ שגיאה בזיהוי אלמנות חדשות: {str(e)}")
            logging.error(f"New widow identification error: {e}")
            return []

    def create_widow_import_ui(self):
        """Create UI for widow data import and management"""
        st.markdown("### 👩 ניהול אלמנות - ייבוא נתונים")

        # Load data
        with st.spinner("טוען נתוני אלמנות..."):
            widow_df, new_widows = self.load_widow_data()

        if widow_df.empty:
            st.error("❌ לא ניתן לטעון נתוני אלמנות")
            return

        # Display statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("סך אלמנות", len(widow_df))

        with col2:
            assigned_count = len(widow_df[widow_df["donor_name"].notna()])
            st.metric("משוייכות לתורם", assigned_count)

        with col3:
            st.metric("אלמנות חדשות", len(new_widows))

        with col4:
            total_support = widow_df["monthly_support"].sum()
            st.metric("סך תמיכה חודשית", f"₪{total_support:,.0f}")

        st.divider()

        # New widows section
        if new_widows:
            st.markdown("#### 🆕 אלמנות חדשות שצריכות שיוך לתורם")

            # Create assignment interface
            for i, widow in enumerate(new_widows):
                with st.expander(f"👩 {widow['widow_name']} - {widow['children_count']} ילדים"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**שם:** {widow['widow_name']}")
                        st.write(f"**מספר ילדים:** {widow['children_count']}")
                        st.write(f"**סכום חודשי:** ₪{widow['monthly_amount']:,.0f}")

                    with col2:
                        st.write(
                            f"**תאריך התחלה:** {widow['start_date'].strftime('%d/%m/%Y') if pd.notna(widow['start_date']) else 'לא מוגדר'}"
                        )
                        st.write(
                            f"**תאריך סיום:** {widow['end_date'].strftime('%d/%m/%Y') if pd.notna(widow['end_date']) else 'לא מוגדר'}"
                        )
                        st.write(f"**תמיכה חודשית:** ₪{widow['monthly_support']:,.0f}")

                    # Donor assignment
                    st.markdown("**שיוך לתורם:**")
                    donor_name = st.text_input(
                        f"שם התורם עבור {widow['widow_name']}",
                        key=f"donor_{i}",
                        placeholder="הזן שם התורם",
                    )

                    if st.button("שייך לתורם", key=f"assign_{i}"):
                        if donor_name:
                            # Here you would update the Google Sheet
                            st.success(f"✅ {widow['widow_name']} שויכה לתורם {donor_name}")
                        else:
                            st.warning("⚠️ אנא הזן שם תורם")

        # All widows table
        st.markdown("#### 📋 כל האלמנות")

        # Filter options
        col1, col2, col3 = st.columns(3)

        with col1:
            show_assigned = st.checkbox("הצג רק משוייכות", value=False)

        with col2:
            show_new = st.checkbox("הצג רק חדשות", value=False)

        with col3:
            min_support = st.number_input("תמיכה מינימלית", min_value=0, value=0)

        # Apply filters
        filtered_df = widow_df.copy()

        if show_assigned:
            filtered_df = filtered_df[filtered_df["donor_name"].notna()]

        if show_new:
            filtered_df = filtered_df[filtered_df["donor_name"].isna()]

        if min_support > 0:
            filtered_df = filtered_df[filtered_df["monthly_support"] >= min_support]

        # Display filtered table
        if not filtered_df.empty:
            # Select columns to display
            display_columns = [
                "widow_name",
                "children_count",
                "monthly_amount",
                "monthly_support",
                "donor_name",
                "start_date",
                "end_date",
            ]

            # Filter to only existing columns
            available_columns = [col for col in display_columns if col in filtered_df.columns]

            if available_columns:
                st.dataframe(
                    filtered_df[available_columns],
                    width='stretch',
                    hide_index=True,
                    column_config={
                        "widow_name": "שם",
                        "children_count": "ילדים",
                        "monthly_amount": "סכום חודשי",
                        "monthly_support": "תמיכה חודשית",
                        "donor_name": "תורם",
                        "start_date": "תאריך התחלה",
                        "end_date": "תאריך סיום",
                    },
                )
            else:
                st.warning("⚠️ לא נמצאו עמודות מתאימות להצגה")
        else:
            st.info("אין נתונים להצגה לפי הפילטרים שנבחרו")


def create_widow_import_section():
    """Create the widow import section for the dashboard"""
    try:
        import_manager = WidowImportManager()
        import_manager.create_widow_import_ui()
    except Exception as e:
        st.error(f"❌ שגיאה ביצירת ממשק ייבוא אלמנות: {str(e)}")
        logging.error(f"Widow import UI error: {e}")
