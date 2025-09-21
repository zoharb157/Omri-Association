#!/usr/bin/env python3
"""
Dashboard Layout Module
Handles the main dashboard structure, tabs, and layout
"""


import pandas as pd
import streamlit as st


def _get_amount_column(df: pd.DataFrame) -> str:
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ("שקלים", "סכום"):
        if col in df.columns:
            return col
    return None


def create_main_tabs():
    """Create the main tab structure"""
    try:
        return st.tabs(
            ["🏠 דף הבית", "💰 תקציב", "👥 תורמים", "👩 אלמנות", "🕸️ מפת קשרים", "🏘️ אזורי מגורים"]
        )
    except Exception:
        # Return empty list if tabs creation fails
        return []


def create_dashboard_header():
    """Create the main dashboard header with refresh button and system status"""
    try:
        # ============================================================================
        # PROTECTED HEADER - DO NOT REMOVE OR MODIFY!
        # ============================================================================
        # WARNING: This header is essential for the dashboard identity
        # Removing it will break the user experience
        # ============================================================================

        # Main title - PROTECTED
        st.markdown(
            "<h1 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>מערכת ניהול עמותת עמרי</h1>",
            unsafe_allow_html=True,
        )

        # Clean, professional header with just theme toggle
        col1, col2 = st.columns([4, 1])

        with col1:
            # Empty space for clean look
            pass

        with col2:
            # Quick theme toggle and performance info
            try:
                from theme_manager import get_current_theme, switch_theme

                current_theme = get_current_theme()

                if st.button("🌙" if current_theme == "light" else "☀️", help="החלף עיצוב"):
                    new_theme = "dark" if current_theme == "light" else "light"
                    switch_theme(new_theme)
                    st.rerun()
            except ImportError:
                pass  # Theme manager not available

            # Performance info (only in debug mode)
            if st.session_state.get("debug_mode", False):
                # Simple performance info
                def show_performance_info():
                    st.info("ℹ️ מידע על ביצועים: טעינה מהירה")

                show_performance_info()

        add_spacing(1)
    except Exception:
        # Handle any errors in header creation gracefully
        pass


def create_section_header(title: str, icon: str = ""):
    """Create a consistent section header using design system tokens"""
    icon_text = f"{icon} " if icon else ""
    st.markdown(
        f"""
    <h2 style='
        color: var(--color-text-primary, #0f172a);
        border-bottom: 2px solid var(--color-border, #e2e8f0);
        padding-bottom: var(--space-2, 0.5rem);
        margin-bottom: var(--space-6, 1.5rem);
        font-family: var(--font-primary, "Segoe UI", "Noto Sans Hebrew", "Arial Hebrew", sans-serif);
        font-size: var(--text-2xl, 1.5rem);
        font-weight: var(--font-semibold, 600);
    '>{icon_text}{title}</h2>
    """,
        unsafe_allow_html=True,
    )


def create_metric_row(metrics: list, columns: int = 4):
    """Create a row of metrics with specified number of columns using design system components"""

    # Simple metric cards
    def create_metric_cards(metrics):
        """Create simple metric cards"""
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.metric(
                    label=metric.get("label", ""),
                    value=metric.get("value", ""),
                    help=metric.get("help", ""),
                )

    create_metric_cards(metrics)


def create_two_column_layout():
    """Create a two-column layout"""
    return st.columns(2)


def create_three_column_layout():
    """Create a three-column layout"""
    return st.columns(3)


def add_spacing(rem: float = 2):
    """Add consistent spacing between sections using design system tokens"""
    try:
        # Convert rem to design system spacing scale
        spacing_map = {
            0.5: "var(--space-2, 0.5rem)",
            1: "var(--space-4, 1rem)",
            1.5: "var(--space-6, 1.5rem)",
            2: "var(--space-8, 2rem)",
            3: "var(--space-12, 3rem)",
            4: "var(--space-16, 4rem)",
        }
        spacing_value = spacing_map.get(rem, f"{rem}rem")
        st.markdown(f"<div style='margin: {spacing_value} 0;'></div>", unsafe_allow_html=True)
    except Exception:
        # Handle any errors in spacing creation gracefully
        pass


def create_recent_activity_section(expenses_df: pd.DataFrame, donations_df: pd.DataFrame):
    """Create the recent activity section"""
    col1, col2 = create_two_column_layout()

    with col1:
        st.markdown("<h4>🎁 תרומות אחרונות</h4>", unsafe_allow_html=True)
        try:
            name_col = (
                "שם"
                if "שם" in donations_df.columns
                else "שם התורם" if "שם התורם" in donations_df.columns else None
            )
            amount_col = _get_amount_column(donations_df)
            if name_col and amount_col:
                recent_donations = donations_df.sort_values("תאריך", ascending=False).head(5)
                if len(recent_donations) > 0:
                    for _, donation in recent_donations.iterrows():
                        donation_date = donation["תאריך"]
                        amount = pd.to_numeric(donation.get(amount_col, 0), errors="coerce")
                        if pd.isna(amount):
                            amount = 0
                        label = donation.get(name_col, "")
                        if pd.notna(donation_date):
                            st.write(
                                f"**{label}** - ₪{amount:,.0f} ({donation_date.strftime('%d/%m/%Y')})"
                            )
                        else:
                            st.write(f"**{label}** - ₪{amount:,.0f} (תאריך לא מוגדר)")
                else:
                    st.info("אין תרומות להצגה")
            else:
                st.warning("אין נתוני תרומות זמינים")
        except Exception:
            st.error("שגיאה בטעינת תרומות אחרונות")

    with col2:
        st.markdown("<h4>💸 הוצאות אחרונות</h4>", unsafe_allow_html=True)
        try:
            name_col = (
                "שם"
                if "שם" in expenses_df.columns
                else "שם לקוח" if "שם לקוח" in expenses_df.columns else None
            )
            amount_col = _get_amount_column(expenses_df)
            if name_col and amount_col:
                recent_expenses = expenses_df.sort_values("תאריך", ascending=False).head(5)
                if len(recent_expenses) > 0:
                    for _, expense in recent_expenses.iterrows():
                        expense_date = expense["תאריך"]
                        amount = pd.to_numeric(expense.get(amount_col, 0), errors="coerce")
                        if pd.isna(amount):
                            amount = 0
                        label = expense.get(name_col, "")
                        if pd.notna(expense_date):
                            st.write(
                                f"**{label}** - ₪{amount:,.0f} ({expense_date.strftime('%d/%m/%Y')})"
                            )
                        else:
                            st.write(f"**{label}** - ₪{amount:,.0f} (תאריך לא מוגדר)")
                else:
                    st.info("אין הוצאות להצגה")
            else:
                st.warning("אין נתוני הוצאות זמינים")
        except Exception:
            st.error("שגיאה בטעינת הוצאות אחרונות")


def create_reports_section(
    expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame
):
    """Create the reports and data export section"""
    create_section_header("📋 דוחות וייצוא נתונים")

    # Data Export Section (Quick access to raw data)
    st.markdown("#### 📥 ייצוא נתונים גולמיים")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 ייצוא סקירה כללית", width="stretch"):
            try:
                # Create summary data
                donations_amount_col = _get_amount_column(donations_df)
                expenses_amount_col = _get_amount_column(expenses_df)
                total_donations = (
                    pd.to_numeric(donations_df[donations_amount_col], errors="coerce")
                    .fillna(0)
                    .sum()
                    if donations_amount_col
                    else 0
                )
                total_expenses = (
                    pd.to_numeric(expenses_df[expenses_amount_col], errors="coerce").fillna(0).sum()
                    if expenses_amount_col
                    else 0
                )
                donor_name_col = (
                    "שם"
                    if "שם" in donations_df.columns
                    else "שם התורם" if "שם התורם" in donations_df.columns else None
                )
                summary_data = {
                    "סך תרומות": [total_donations],
                    "סך הוצאות": [total_expenses],
                    "יתרה זמינה": [total_donations - total_expenses],
                    "מספר תורמים": [
                        len(donations_df[donor_name_col].unique()) if donor_name_col else 0
                    ],
                    "מספר אלמנות": [
                        len(almanot_df["שם "].unique()) if "שם " in almanot_df.columns else 0
                    ],
                }

                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    label="💾 הורד CSV",
                    data=csv,
                    file_name=f"omri_summary_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"שגיאה בייצוא: {e}")

    with col2:
        if st.button("👥 ייצוא נתוני תורמים", width="stretch"):
            try:
                if not donations_df.empty:
                    csv = donations_df.to_csv(index=False, encoding="utf-8-sig")
                    st.download_button(
                        label="💾 הורד CSV",
                        data=csv,
                        file_name=f"omri_donors_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("אין נתוני תורמים לייצוא")
            except Exception as e:
                st.error(f"שגיאה בייצוא: {e}")

    with col3:
        if st.button("👩 ייצוא נתוני אלמנות", width="stretch"):
            try:
                if not almanot_df.empty:
                    csv = almanot_df.to_csv(index=False, encoding="utf-8-sig")
                    st.download_button(
                        label="💾 הורד CSV",
                        data=csv,
                        file_name=f"omri_widows_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("אין נתוני אלמנות לייצוא")
            except Exception as e:
                st.error(f"שגיאה בייצוא: {e}")

    add_spacing(2)

    # Detailed Reports Section
    st.markdown("#### 📊 דוחות מפורטים")
    col1, col2 = create_two_column_layout()

    with col1:
        if st.button("📊 דוח חודשי מפורט", width="stretch"):
            try:
                from reports.reports import generate_monthly_report

                filename = generate_monthly_report(expenses_df, donations_df, almanot_df)
                if filename:
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="הורד דוח חודשי",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf",
                        )
            except Exception:
                st.error("שגיאה ביצירת דוח חודשי")

        if st.button("👥 דוח תורמים מפורט", width="stretch"):
            try:
                from reports.reports import generate_donor_report

                filename = generate_donor_report(donations_df)
                if filename:
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="הורד דוח תורמים",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf",
                        )
            except Exception:
                st.error("שגיאה ביצירת דוח תורמים")

    with col2:
        if st.button("👩 דוח אלמנות מפורט", width="stretch"):
            try:
                from reports.reports import generate_widows_report

                filename = generate_widows_report(almanot_df)
                if filename:
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="הורד דוח אלמנות",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf",
                        )
            except Exception:
                st.error("שגיאה ביצירת דוח אלמנות")

        if st.button("💰 דוח תקציב מפורט", width="stretch"):
            try:
                from reports.reports import generate_budget_report

                filename = generate_budget_report(expenses_df, donations_df)
                if filename:
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="הורד דוח תקציב",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf",
                        )
            except Exception:
                st.error("שגיאה ביצירת דוח תקציב")
