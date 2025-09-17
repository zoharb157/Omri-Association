#!/usr/bin/env python3
"""
Modern Dashboard Components for Omri Association Dashboard
Main dashboard components with modern styling
"""

import pandas as pd
import streamlit as st

from ui.components.layout_system import create_modern_alert, create_responsive_grid
from ui.components.modern_cards import (
    create_dashboard_kpis,
    create_section_header,
)
from ui.components.modern_charts import (
    create_modern_donations_chart,
    create_modern_donors_chart,
    create_modern_expenses_pie_chart,
    create_modern_widows_chart,
)


def _get_amount_column(df: pd.DataFrame) -> str:
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ('שקלים', 'סכום'):
        if col in df.columns:
            return col
    return None


def _get_name_column(df: pd.DataFrame) -> str:
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ('שם', 'שם התורם', 'שם לקוח'):
        if col in df.columns:
            return col
    return None

def create_modern_overview_section(budget_status: dict, donor_stats: dict, widow_stats: dict):
    """Create the modern overview section with KPIs and charts"""

    # Create KPI cards
    create_dashboard_kpis(budget_status, donor_stats, widow_stats)

    # Add spacing
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

def create_modern_charts_section(expenses_df: pd.DataFrame, donations_df: pd.DataFrame,
                                donors_df: pd.DataFrame, widows_df: pd.DataFrame):
    """Create the modern charts section"""

    create_section_header("תרשימים וניתוח נתונים", "סקירה ויזואלית של הנתונים")

    # Create charts grid
    cols = create_responsive_grid([], columns=2)  # Create responsive grid layout

    with cols[0]:
        # Donations chart
        donations_chart = create_modern_donations_chart(donations_df)
        if donations_chart:
            chart_html = st.plotly_chart(donations_chart, use_container_width=True, key="donations_chart", output_format="div")
            from ui.components.modern_cards import create_chart_card
            create_chart_card(
                title="תרשים תרומות",
                subtitle="מגמות תרומות לאורך זמן",
                empty=False,
                chart_html=chart_html,
                caption=None
            )
        else:
            from ui.components.modern_cards import create_chart_card
            create_chart_card(
                title="תרשים תרומות",
                subtitle="מגמות תרומות לאורך זמן",
                empty=True,
                chart_html="",
                caption=None
            )

    with cols[1]:
        # Expenses pie chart
        expenses_chart = create_modern_expenses_pie_chart(expenses_df)
        from ui.components.modern_cards import create_chart_card
        if expenses_chart:
            chart_html = st.plotly_chart(expenses_chart, use_container_width=True, key="expenses_chart", output_format="div")
            create_chart_card(
                title="תרשים הוצאות",
                subtitle="התפלגות הוצאות",
                empty=False,
                chart_html=chart_html,
                caption=None
            )
        else:
            create_chart_card(
                title="תרשים הוצאות",
                subtitle="התפלגות הוצאות",
                empty=True,
                chart_html="",
                caption=None
            )

    # Second row of charts
    st.markdown(
        """
        <style>
        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
        @media (max-width: 900px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="chart-grid">', unsafe_allow_html=True)

    with cols2[0]:
        # Donors chart
        donors_chart = create_modern_donors_chart(donors_df)
        from ui.components.modern_cards import create_chart_card
        if donors_chart:
            chart_html = st.plotly_chart(donors_chart, use_container_width=True, key="donors_chart", output_format="div")
            create_chart_card(
                title="תרשים תורמים",
                subtitle="פילוח תורמים",
                empty=False,
                chart_html=chart_html,
                caption=None
            )
        else:
            create_chart_card(
                title="תרשים תורמים",
                subtitle="פילוח תורמים",
                empty=True,
                chart_html="",
                caption=None
            )

    with cols2[1]:
        # Widows chart
        widows_chart = create_modern_widows_chart(widows_df)
        from ui.components.modern_cards import create_chart_card
        if widows_chart:
            chart_html = st.plotly_chart(widows_chart, use_container_width=True, key="widows_chart", output_format="div")
            create_chart_card(
                title="תרשים אלמנות",
                subtitle="פילוח אלמנות",
                empty=False,
                chart_html=chart_html,
                caption=None
            )
        else:
            create_chart_card(
                title="תרשים אלמנות",
                subtitle="פילוח אלמנות",
                empty=True,
                chart_html="",
                caption=None
            )

    st.markdown('</div>', unsafe_allow_html=True)

def create_modern_recent_activity_section(expenses_df: pd.DataFrame, donations_df: pd.DataFrame):
    """Create the modern recent activity section"""

    create_section_header("פעילות אחרונה", "תרומות והוצאות אחרונות")

    # Create two columns for recent activities
    cols = create_responsive_grid([], columns=2)

    with cols[0]:
        st.markdown("### 🎁 תרומות אחרונות")
        try:
            name_col = _get_name_column(donations_df)
            amount_col = _get_amount_column(donations_df)
            if not donations_df.empty and 'תאריך' in donations_df.columns and name_col and amount_col:
                recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                if len(recent_donations) > 0:
                    for _, donation in recent_donations.iterrows():
                        donation_date = donation['תאריך']
                        date_str = donation_date.strftime('%d/%m/%Y') if pd.notna(donation_date) else 'תאריך לא מוגדר'
                        amount = pd.to_numeric(donation.get(amount_col, 0), errors='coerce')
                        if pd.isna(amount):
                            amount = 0
                        donation_html = f"""
                        <div class="activity-item">
                            <div class="activity-content">
                                <strong>{donation.get(name_col, '')}</strong>
                                <span class="activity-amount">₪{amount:,.0f}</span>
                            </div>
                            <div class="activity-date">{date_str}</div>
                        </div>
                        """
                        st.markdown(donation_html, unsafe_allow_html=True)
                else:
                    create_modern_alert("אין תרומות להצגה", "info")
            else:
                create_modern_alert("אין נתוני תרומות זמינים", "warning")
        except Exception as e:
            create_modern_alert(f"שגיאה בטעינת תרומות: {str(e)}", "error")

    with cols[1]:
        st.markdown("### 💸 הוצאות אחרונות")
        try:
            expense_name_col = _get_name_column(expenses_df)
            expense_amount_col = _get_amount_column(expenses_df)
            if not expenses_df.empty and 'תאריך' in expenses_df.columns and expense_name_col and expense_amount_col:
                recent_expenses = expenses_df.sort_values('תאריך', ascending=False).head(5)
                if len(recent_expenses) > 0:
                    for _, expense in recent_expenses.iterrows():
                        expense_date = expense['תאריך']
                        date_str = expense_date.strftime('%d/%m/%Y') if pd.notna(expense_date) else 'תאריך לא מוגדר'
                        amount = pd.to_numeric(expense.get(expense_amount_col, 0), errors='coerce')
                        if pd.isna(amount):
                            amount = 0
                        expense_html = f"""
                        <div class="activity-item">
                            <div class="activity-content">
                                <strong>{expense.get(expense_name_col, '')}</strong>
                                <span class="activity-amount">₪{amount:,.0f}</span>
                            </div>
                            <div class="activity-date">{date_str}</div>
                        </div>
                        """
                        st.markdown(expense_html, unsafe_allow_html=True)
                else:
                    create_modern_alert("אין הוצאות להצגה", "info")
            else:
                create_modern_alert("אין נתוני הוצאות זמינים", "warning")
        except Exception as e:
            create_modern_alert(f"שגיאה בטעינת הוצאות: {str(e)}", "error")

def create_modern_alerts_section(budget_status: dict, donor_stats: dict, widow_stats: dict):
    """Create the modern alerts section"""

    create_section_header("התראות ומידע חשוב", "עדכונים על מצב העמותה")

    # Check for alerts
    alerts = []

    # Budget alerts
    if budget_status.get('total_donations', 0) < budget_status.get('total_expenses', 0):
        alerts.append(("⚠️", "יתרה שלילית", "ההוצאות עולות על התרומות", "warning"))

    # Utilization rate alert
    utilization_rate = (budget_status.get('total_expenses', 0) / budget_status.get('total_donations', 1)) * 100
    if utilization_rate > 90:
        alerts.append(("🚨", "ניצול גבוה", f"אחוז הניצול הוא {utilization_rate:.1f}%", "error"))
    elif utilization_rate > 80:
        alerts.append(("⚠️", "ניצול גבוה", f"אחוז הניצול הוא {utilization_rate:.1f}%", "warning"))

    # Donor alerts
    if donor_stats.get('total_donors', 0) < 10:
        alerts.append(("ℹ️", "מעט תורמים", "מספר התורמים נמוך", "info"))

    # Widow alerts
    if widow_stats.get('total_widows', 0) > 100:
        alerts.append(("ℹ️", "מספר גבוה של אלמנות", f"יש {widow_stats.get('total_widows', 0)} אלמנות במערכת", "info"))

    # Display alerts
    if alerts:
        for icon, title, message, alert_type in alerts:
            create_modern_alert(f"{icon} {title}: {message}", alert_type)
    else:
        create_modern_alert("✅ הכל תקין - אין התראות", "success")

