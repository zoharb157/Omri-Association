import streamlit as st
import logging
from ui.components.layout_system import create_modern_navbar
def render_dashboard():
    # Now 'st' and 'logging' are available from the start

    # Load data
    expenses_df, donations_df, widows_df, investors_df = load_dashboard_data()
    st.write(f"[DEBUG] DataFrames loaded: expenses_df={expenses_df is not None and not expenses_df.empty}, donations_df={donations_df is not None and not donations_df.empty}, widows_df={widows_df is not None and not widows_df.empty}")
    logging.info(f"[DEBUG] DataFrames loaded: expenses_df={expenses_df is not None and not expenses_df.empty}, donations_df={donations_df is not None and not donations_df.empty}, widows_df={widows_df is not None and not widows_df.empty}")
    budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, widows_df)
    st.write(f"[DEBUG] budget_status: {budget_status}")
    st.write(f"[DEBUG] donor_stats: {donor_stats}")
    st.write(f"[DEBUG] widow_stats: {widow_stats}")
    logging.info(f"[DEBUG] budget_status: {budget_status}")
    logging.info(f"[DEBUG] donor_stats: {donor_stats}")
    logging.info(f"[DEBUG] widow_stats: {widow_stats}")
    """Render the main dashboard with navigation bar and all sections."""
    if "active_section" not in st.session_state:
        st.session_state["active_section"] = "overview"
    active_section = st.session_state["active_section"]
    from ui.components.layout_system import create_modern_navbar
    create_modern_navbar(active_section=active_section)

    # Load data
    expenses_df, donations_df, widows_df, investors_df = load_dashboard_data()
    budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, widows_df)

    # Render only the selected section
    if active_section == "overview":
        _render_home_tab(expenses_df, donations_df, widows_df, budget_status, donor_stats, widow_stats)
    elif active_section == "charts":
        create_modern_charts_section(expenses_df, donations_df, donations_df, widows_df)
    elif active_section == "activity":
        create_modern_recent_activity_section(expenses_df, donations_df)
    elif active_section == "alerts":
        create_modern_alerts_section(budget_status, donor_stats, widow_stats)
    elif active_section == "alerts":
        # ...existing code to render alerts section...
        pass
#!/usr/bin/env python3
"""
Modern Dashboard Core Module
Handles core dashboard logic with modern UI components
"""

import logging
import textwrap
from typing import Dict, Tuple

import pandas as pd
import streamlit as st

from data_processing import (
    calculate_donor_statistics,
    calculate_monthly_budget,
    calculate_widow_statistics,
)
from google_sheets_io import check_service_account_validity
from services.sheets import fetch_dashboard_frames
from ui.components.headers import create_page_title
from ui.components.micro_interactions import (
    create_focus_states,
    create_hover_effects,
    create_interactive_feedback,
    create_loading_animations,
    create_transition_animations,
)
from ui.components.modern_dashboard import (
    create_modern_alerts_section,
    create_modern_charts_section,
    create_modern_overview_section,
    create_modern_recent_activity_section,
)
from ui.components.responsive_design import (
    create_mobile_navigation,
    create_responsive_container,
    create_responsive_spacing,
    create_responsive_typography,
    create_touch_friendly_buttons,
)
from ui.dashboard_sections import (
    create_budget_section,
    create_donors_section,
    create_network_section,
    create_residential_breakdown_section,
    create_widows_section,
    create_widows_table_section,
)


def _format_currency(value: float | int | None) -> str:
    if value is None:
        value = 0
    try:
        return f"₪{float(value):,.0f}"
    except (TypeError, ValueError):
        return "₪0"


def _format_delta(current: float, previous: float) -> str:
    if previous in (0, None):
        return "חדש"
    delta = current - previous
    sign = "+" if delta >= 0 else "-"
    return f"{sign}₪{abs(delta):,.0f}"


def load_dashboard_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all dashboard data from Google Sheets with enhanced loading states and error handling"""
    try:
        # Check if data is already in session state
        if ('expenses_df' in st.session_state and 'donations_df' in st.session_state and
            'almanot_df' in st.session_state and 'investors_df' in st.session_state):

            # Use cached data
            expenses_df = st.session_state.expenses_df
            donations_df = st.session_state.donations_df
            almanot_df = st.session_state.almanot_df
            investors_df = st.session_state.investors_df

            # Validate cached data
            if (expenses_df is not None and donations_df is not None and
                almanot_df is not None and investors_df is not None):
                return expenses_df, donations_df, almanot_df, investors_df

        frames = fetch_dashboard_frames()
        expenses_df = frames.get('Expenses', pd.DataFrame())
        donations_df = frames.get('Donations', pd.DataFrame())
        investors_df = frames.get('Investors', pd.DataFrame())
        almanot_df = frames.get('Widows', pd.DataFrame())

        # Store in session state
        st.session_state.expenses_df = expenses_df
        st.session_state.donations_df = donations_df
        st.session_state.almanot_df = almanot_df
        st.session_state.investors_df = investors_df

        # Validate data integrity
        if expenses_df.empty and donations_df.empty and almanot_df.empty:
            st.error("❌ לא ניתן לטעון נתונים. אנא בדוק את חיבור Google Sheets")
            return None, None, None, None

        return expenses_df, donations_df, almanot_df, investors_df

    except Exception as e:
        error_msg = f"שגיאה בטעינת נתונים: {str(e)}"
        st.error(f"❌ {error_msg}")
        logging.error(f"Data loading error: {e}")

        # Show helpful troubleshooting tips
        st.info("💡 טיפים לפתרון בעיות:")
        st.info("• בדוק חיבור לאינטרנט")
        st.info("• ודא שקובץ service_account.json קיים ותקין")
        st.info("• בדוק הרשאות Google Sheets")

        return None, None, None, None

def process_dashboard_data(expenses_df: pd.DataFrame, donations_df: pd.DataFrame, almanot_df: pd.DataFrame) -> Tuple[Dict, Dict, Dict]:
    """Process dashboard data and calculate statistics with enhanced error handling"""
    try:
        # Fix data types with validation (silent processing)
        for _df_name, df in [('expenses_df', expenses_df), ('donations_df', donations_df)]:
            if df is not None and not df.empty:
                amount_col = 'שקלים' if 'שקלים' in df.columns else 'סכום' if 'סכום' in df.columns else None
                if amount_col:
                    df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
                if len(df.columns) > 0:
                    date_col = df.columns[0]
                    df['תאריך'] = pd.to_datetime(df[date_col], errors='coerce')

        if almanot_df is not None and not almanot_df.empty:
            if 'מספר ילדים' in almanot_df.columns:
                almanot_df['מספר ילדים'] = pd.to_numeric(almanot_df['מספר ילדים'], errors='coerce').fillna(0)
            if 'סכום חודשי' in almanot_df.columns:
                almanot_df['סכום חודשי'] = pd.to_numeric(almanot_df['סכום חודשי'], errors='coerce').fillna(0)
                # Fill missing values with 0 (intended behavior)

        # Calculate statistics (silent processing) - only if DataFrames have data
        if expenses_df is not None and donations_df is not None and not expenses_df.empty and not donations_df.empty:
            budget_status = calculate_monthly_budget(expenses_df, donations_df)
        else:
            budget_status = {
                'total_donations': 0,
                'total_expenses': 0,
                'balance': 0,
                'utilization_percentage': 0,
                'monthly_donations': {},
                'monthly_expenses': {},
                'donation_trend': 'stable',
                'expense_trend': 'stable'
            }

        if donations_df is not None and not donations_df.empty:
            donor_stats = calculate_donor_statistics(donations_df)
        else:
            donor_stats = {
                'total_donors': 0,
                'total_donations': 0,
                'avg_donation': 0,
                'min_donation': 0,
                'max_donation': 0,
                'top_donors': []
            }

        if almanot_df is not None and not almanot_df.empty:
            widow_stats = calculate_widow_statistics(almanot_df)
        else:
            widow_stats = {
                'total_widows': 0,
                'total_support': 0,
                'support_1000_count': 0,
                'support_2000_count': 0,
                'support_distribution': {},
                'monthly_support': []
            }

        return budget_status, donor_stats, widow_stats

    except Exception as e:
        logging.error(f"Error processing dashboard data: {e}")
        st.warning("⚠️ שגיאה בעיבוד נתונים")

        # Return empty stats
        return {
            'total_donations': 0,
            'total_expenses': 0,
            'balance': 0,
            'utilization_percentage': 0,
            'monthly_donations': {},
            'monthly_expenses': {},
            'donation_trend': 'stable',
            'expense_trend': 'stable'
        }, {
            'total_donors': 0,
            'total_donations': 0,
            'avg_donation': 0,
            'min_donation': 0,
            'max_donation': 0,
            'top_donors': []
        }, {
            'total_widows': 0,
            'total_support': 0,
            'support_1000_count': 0,
            'support_2000_count': 0,
            'support_distribution': {},
            'monthly_support': []
        }

def run_modern_dashboard():
    """Main modern dashboard function that orchestrates all modern components"""
    try:
        logging.info("=== STARTING MODERN DASHBOARD ===")

        # Initialize modern components
        create_responsive_container()
        create_mobile_navigation()
        create_touch_friendly_buttons()
        create_responsive_typography()
        create_responsive_spacing()
        create_loading_animations()
        create_hover_effects()
        create_focus_states()
        create_transition_animations()
        create_interactive_feedback()

        # Create page title
        create_page_title("מערכת ניהול עמותת עמרי", "סקירה מקיפה של מצב העמותה")

        # Check service account validity
        if not check_service_account_validity():
            st.error("Service account validation failed")
            st.stop()

        # Load data
        expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()

        if expenses_df is None or donations_df is None or almanot_df is None:
            st.error("❌ לא ניתן לטעון נתונים. אנא נסה שוב מאוחר יותר.")
            return

        # Check for empty dataframes
        empty_dataframes = []
        if expenses_df is not None and expenses_df.empty:
            empty_dataframes.append("הוצאות")
        if donations_df is not None and donations_df.empty:
            empty_dataframes.append("תרומות")
        if almanot_df is not None and almanot_df.empty:
            empty_dataframes.append("אלמנות")

        if empty_dataframes:
            st.warning(f"⚠️ הנתונים הבאים ריקים: {', '.join(empty_dataframes)}. יוצגו רק הנתונים הזמינים.")

        # Process data - only if we have non-empty DataFrames
        if expenses_df is not None and donations_df is not None and not expenses_df.empty and not donations_df.empty:
            try:
                budget_status, donor_stats, widow_stats = process_dashboard_data(expenses_df, donations_df, almanot_df)
            except Exception as e:
                logging.error(f"Error in process_dashboard_data: {e}")
                st.error(f"❌ שגיאה בעיבוד נתונים: {str(e)}")
                # Create empty stats as fallback
                budget_status = {
                    'total_donations': 0,
                    'total_expenses': 0,
                    'balance': 0,
                    'utilization_percentage': 0,
                    'monthly_donations': {},
                    'monthly_expenses': {},
                    'donation_trend': 'stable',
                    'expense_trend': 'stable'
                }
                donor_stats = {
                    'total_donors': 0,
                    'total_donations': 0,
                    'avg_donation': 0,
                    'min_donation': 0,
                    'max_donation': 0,
                    'top_donors': []
                }
                widow_stats = {
                    'total_widows': 0,
                    'total_support': 0,
                    'support_1000_count': 0,
                    'support_2000_count': 0,
                    'support_distribution': {},
                    'monthly_support': []
                }
        else:
            # Create empty stats for empty DataFrames
            budget_status = {
                'total_donations': 0,
                'total_expenses': 0,
                'balance': 0,
                'utilization_percentage': 0,
                'monthly_donations': {},
                'monthly_expenses': {},
                'donation_trend': 'stable',
                'expense_trend': 'stable'
            }
            donor_stats = {
                'total_donors': 0,
                'total_donations': 0,
                'avg_donation': 0,
                'min_donation': 0,
                'max_donation': 0,
                'top_donors': []
            }
            widow_stats = {
                'total_widows': 0,
                'total_support': 0,
                'support_1000_count': 0,
                'support_2000_count': 0,
                'support_distribution': {},
                'monthly_support': []
            }



    except Exception as e:
        import traceback
        st.error(f"❌ שגיאה כללית: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        logging.error(f"Modern dashboard error: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")


def _render_home_tab(
    expenses_df: pd.DataFrame,
    donations_df: pd.DataFrame,
    widows_df: pd.DataFrame,
    budget_status: Dict,
    donor_stats: Dict,
    widow_stats: Dict,
):
    """Render the modern home dashboard with a hero section and quick actions."""

    total_donations = budget_status.get('total_donations', 0)
    available_balance = budget_status.get('balance', 0)

    monthly_map = budget_status.get('monthly_donations', {}) or {}
    month_items = sorted(monthly_map.items())
    latest_month_value = month_items[-1][1] if month_items else 0
    previous_month_value = month_items[-2][1] if len(month_items) > 1 else 0

    active_donors = donor_stats.get('total_donors', 0)
    avg_donation = donor_stats.get('avg_donation', 0)
    widow_support = widow_stats.get('total_support', 0)
    widow_count = widow_stats.get('total_widows', 0)

    hero_cards = [
        {
            "label": "סה\"כ תרומות",
            "value": _format_currency(total_donations),
            "meta": f"יתרה זמינה {_format_currency(available_balance)}",
        },
        {
            "label": "תרומות בחודש האחרון",
            "value": _format_currency(latest_month_value),
            "meta": _format_delta(latest_month_value, previous_month_value) + " לעומת חודש קודם",
        },
        {
            "label": "סיוע חודשי לאלמנות",
            "value": _format_currency(widow_support),
            "meta": f"{widow_count:,} אלמנות מקבלות סיוע",
        },
        {
            "label": "תורמים פעילים",
            "value": f"{active_donors:,}",
            "meta": f"תרומה ממוצעת {_format_currency(avg_donation)}",
        },
    ]

    hero_cards_html = "".join(
        textwrap.dedent(
            f"""
            <div class=\"hero-stat-card\">
                <span class=\"hero-stat-label\">{card['label']}</span>
                <span class=\"hero-stat-value\">{card['value']}</span>
                {f"<span class='hero-stat-meta'>{card['meta']}</span>" if card.get('meta') else ''}
            </div>
            """
        )
        for card in hero_cards
    )

    hero_html = textwrap.dedent(
        f"""
        <div class="page-container">
            <section class="hero-banner">
                <div class="hero-content">
                    <div class="hero-heading">
                        <h1>ניהול נתוני העמותה בצורה חכמה ומעודכנת</h1>
                        <p>מעקב בזמן אמת אחר תרומות, הוצאות וסיוע לאלמנות מאפשר קבלת החלטות מדויקת.</p>
                    </div>
                    <div class="hero-stats">
                        {hero_cards_html}
                    </div>
                    <div class="hero-actions">
                        <button class="hero-button primary">🔄 רענון נתונים</button>
                        <button class="hero-button secondary">📥 ייצוא דוחות</button>
                    </div>
                </div>
            </section>
        """
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    create_modern_overview_section(budget_status, donor_stats, widow_stats)

    quick_actions_html = textwrap.dedent(
        """
        <section id="quick-actions" class="quick-actions">
            <div class="quick-action-card">
                <div class="quick-action-icon">📊</div>
                <div class="quick-action-content">
                    <h3 class="quick-action-title">דוחות חודשיים</h3>
                    <p class="quick-action-meta">ייצוא סיכומי PDF ומעקב ביצועים</p>
                </div>
            </div>
            <div class="quick-action-card">
                <div class="quick-action-icon">👥</div>
                <div class="quick-action-content">
                    <h3 class="quick-action-title">ניהול תורמים</h3>
                    <p class="quick-action-meta">הוספה, עדכון ומעקב אחרי תרומות</p>
                </div>
            </div>
            <div class="quick-action-card">
                <div class="quick-action-icon">🤝</div>
                <div class="quick-action-content">
                    <h3 class="quick-action-title">ליווי אלמנות</h3>
                    <p class="quick-action-meta">בדיקת תמיכה חודשית והשלמת נתונים חסרים</p>
                </div>
            </div>
            <div class="quick-action-card">
                <div class="quick-action-icon">⚙️</div>
                <div class="quick-action-content">
                    <h3 class="quick-action-title">תהליכי בקרה</h3>
                    <p class="quick-action-meta">גילוי נתונים חריגים והתראות בזמן אמת</p>
                </div>
            </div>
        </section>
        """
    )
    st.markdown(quick_actions_html, unsafe_allow_html=True)

    if (expenses_df is not None and not expenses_df.empty) or (donations_df is not None and not donations_df.empty):
        create_modern_charts_section(expenses_df, donations_df, donations_df, widows_df)
    else:
        st.info("ℹ️ אין נתונים להצגת תרשימים")

    if (expenses_df is not None and not expenses_df.empty) or (donations_df is not None and not donations_df.empty):
        create_modern_recent_activity_section(expenses_df, donations_df)
    else:
        st.info("ℹ️ אין נתונים להצגת פעילות אחרונה")

    create_modern_alerts_section(budget_status, donor_stats, widow_stats)

    st.markdown("</div>", unsafe_allow_html=True)
