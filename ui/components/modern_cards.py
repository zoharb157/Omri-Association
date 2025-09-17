def create_chart_card(title: str, subtitle: str = None, empty: bool = False, chart_html: str = "", caption: str = None):
    """Render a chart inside a modern card with title, subtitle, and empty state."""
    header_html = f"""
        <header class="chart-card-header">
            <h3 class="chart-card-title">{title}</h3>
            {f'<p class="chart-card-subtitle">{subtitle}</p>' if subtitle else ''}
        </header>
    """
    if empty:
        body_html = '<div class="chart-empty-state">אין נתונים להצגה</div>'
    else:
        body_html = chart_html
    caption_html = f'<div class="chart-card-caption">{caption}</div>' if caption else ''
    card_html = f"""
        <section class="chart-card">
            {header_html}
            {body_html}
            {caption_html}
        </section>
    """
    st.markdown(card_html, unsafe_allow_html=True)
#!/usr/bin/env python3
"""
Modern Card Components for Omri Association Dashboard
High-quality card components with modern styling
"""

import textwrap

import streamlit as st

from ui.components.layout_system import create_section_header


def create_info_card(title: str, content: str, action_button: str = None, action_callback=None):
    """Create an informational card"""
    action_html = ""
    if action_button:
        action_html = f'<button class="info-card-action" onclick="alert(\'Action clicked!\')">{action_button}</button>'

    card_html = f"""
    <div class="info-card-modern">
        <h3 class="info-card-title">{title}</h3>
        <p class="info-card-content">{content}</p>
        {action_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def create_dashboard_kpis(budget_status: dict, donor_stats: dict, widow_stats: dict):
    """Create the main dashboard KPIs with modern styling"""

    # Calculate key metrics
    total_donations = budget_status.get('total_donations', 0)
    total_expenses = budget_status.get('total_expenses', 0)
    available_balance = total_donations - total_expenses
    utilization_rate = (total_expenses / total_donations * 100) if total_donations > 0 else 0

    # Format currency
    def format_currency(amount):
        return f"₪{amount:,.0f}"

    def format_change(value):
        if value is None:
            return "", "neutral"
        try:
            float_value = float(value)
        except (TypeError, ValueError):
            return str(value), "neutral"
        status = "positive" if float_value > 0 else "negative" if float_value < 0 else "neutral"
        return f"{float_value:+.1f}%", status

    metrics_have_data = any([
        total_donations,
        total_expenses,
        available_balance,
        donor_stats.get('total_donations'),
        widow_stats.get('total_support'),
    ])

    metrics = []
    if metrics_have_data:
        donations_change, donations_status = format_change(
            budget_status.get('donations_growth')
        )
        expenses_change, expenses_status = format_change(
            budget_status.get('expenses_growth')
        )
        balance_change, balance_status = format_change(
            budget_status.get('balance_growth')
        )
        utilization_change, utilization_status = format_change(
            budget_status.get('utilization_change')
        )

        if available_balance <= 0:
            balance_status = "negative"
        if utilization_rate >= 90:
            utilization_status = "negative"
        elif utilization_rate >= 80:
            utilization_status = "warning"

        metrics = [
            {
                "title": "סך תרומות",
                "value": format_currency(total_donations),
                "change": donations_change,
                "change_type": donations_status,
                "icon": "💰",
            },
            {
                "title": "סך הוצאות",
                "value": format_currency(total_expenses),
                "change": expenses_change,
                "change_type": expenses_status,
                "icon": "💸",
            },
            {
                "title": "יתרה זמינה",
                "value": format_currency(available_balance),
                "change": balance_change,
                "change_type": balance_status,
                "icon": "💳",
            },
            {
                "title": "אחוז ניצול",
                "value": f"{utilization_rate:.1f}%",
                "change": utilization_change,
                "change_type": utilization_status,
                "icon": "📊",
            },
        ]
    else:
        metrics = [{"empty": True}]

    create_section_header("סקירה כללית", "נתונים עדכניים על מצב העמותה")
    if metrics and metrics[0].get("empty"):
        st.info("אין נתונים להצגה עדיין. <a href='#quick-actions'>הוספת נתונים</a>", unsafe_allow_html=True)
    create_metrics_grid(metrics)



def create_metrics_grid(metrics: list) -> None:
    """Render metric cards inside a responsive grid."""

    if not metrics:
        st.info("ℹ️ אין נתוני מדדים להצגה")
        return

    cards_markup = []
    for metric in metrics:
        if metric.get("empty"):
            placeholder = textwrap.dedent(
                """
                <div class="metric-card-modern metric-card-empty">
                    אין נתונים זמינים כרגע
                </div>
                """
            )
            cards_markup.append(placeholder)
            continue

        icon_html = (
            f'<span class="metric-card-icon">{metric.get("icon")}</span>'
            if metric.get("icon")
            else ""
        )

        change_text = metric.get("change", "")
        change_type = metric.get("change_type", "neutral")
        change_html = (
            textwrap.dedent(
                f"""
                <span class="metric-change-badge {change_type}">
                    {change_text}
                </span>
                """
            )
            if change_text
            else ""
        )

        card_html = textwrap.dedent(
            f"""
            <div class="metric-card-modern">
                <div class="metric-card-header">
                    <span class="metric-card-title">{metric['title']}</span>
                    {icon_html}
                </div>
                <div class="metric-card-value">{metric['value']}</div>
                {change_html}
            </div>
            """
        )
        cards_markup.append(card_html)

    grid_html = textwrap.dedent(
        f"""
        <div class="metric-grid">
            {''.join(cards_markup)}
        </div>
        """
    )
    st.markdown(grid_html, unsafe_allow_html=True)


def create_page_container():
    """Create the main page container with proper max-width and centering"""
    container_html = """
    <div class="page-container">
        <div class="page-content">
    """
    st.markdown(container_html, unsafe_allow_html=True)

def create_loading_card():
    """Create a loading state card"""
    loading_html = """
    <div class="metric-card-modern loading-shimmer">
        <div class="metric-card-header">
            <div style="width: 60%; height: 16px; background: #e0e0e0; border-radius: 4px;"></div>
        </div>
        <div style="width: 80%; height: 32px; background: #e0e0e0; border-radius: 4px; margin: 8px 0;"></div>
        <div style="width: 40%; height: 14px; background: #e0e0e0; border-radius: 4px;"></div>
    </div>
    """
    st.markdown(loading_html, unsafe_allow_html=True)
