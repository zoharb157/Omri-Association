#!/usr/bin/env python3
"""
Modern Card Components for Omri Association Dashboard
High-quality card components with modern styling
"""

import streamlit as st
from ui.design_system.modern_tokens import ModernDesignSystem
from ui.components.layout_system import create_section_header, create_metric_card, create_metrics_grid

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
    
    # Create metrics
    metrics = [
        {
            'title': 'סך תרומות',
            'value': format_currency(total_donations),
            'change': f"+{budget_status.get('donations_growth', 0):.1f}%",
            'change_type': 'positive',
            'icon': '💰'
        },
        {
            'title': 'סך הוצאות', 
            'value': format_currency(total_expenses),
            'change': f"+{budget_status.get('expenses_growth', 0):.1f}%",
            'change_type': 'neutral',
            'icon': '💸'
        },
        {
            'title': 'יתרה זמינה',
            'value': format_currency(available_balance),
            'change': f"{budget_status.get('balance_growth', 0):+.1f}%",
            'change_type': 'positive' if available_balance > 0 else 'negative',
            'icon': '💳'
        },
        {
            'title': 'אחוז ניצול',
            'value': f"{utilization_rate:.1f}%",
            'change': f"{budget_status.get('utilization_change', 0):+.1f}%",
            'change_type': 'positive' if utilization_rate < 80 else 'warning',
            'icon': '📊'
        }
    ]
    
    # Create section header
    create_section_header("סקירה כללית", "נתונים עדכניים על מצב העמותה")
    
    # Create metrics grid
    create_metrics_grid(metrics, columns=4)



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
