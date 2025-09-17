#!/usr/bin/env python3
"""
Metric Components for Dashboard
Enhanced metric cards with consistent styling
"""

import streamlit as st

from ui.components.headers import create_section_header
from ui.design_tokens import DesignSystem


def create_metric_card(label: str, value: str, help_text: str = "", trend: str = None, color: str = "primary"):
    """Create a styled metric card using Streamlit's native components with custom styling"""

    # Get color based on theme
    color_map = {
        'primary': DesignSystem.COLORS['primary'],
        'success': DesignSystem.COLORS['success'],
        'warning': DesignSystem.COLORS['warning'],
        'error': DesignSystem.COLORS['error'],
        'info': DesignSystem.COLORS['info']
    }

    card_color = color_map.get(color, DesignSystem.COLORS['primary'])

    # Create a container with custom styling
    with st.container():
        # Add color accent bar
        st.markdown(f"""
        <div style="
            height: 4px;
            background: {card_color};
            border-radius: {DesignSystem.BORDER_RADIUS['md']} {DesignSystem.BORDER_RADIUS['md']} 0 0;
            margin: 0;
        "></div>
        """, unsafe_allow_html=True)

        # Create the main card container
        st.markdown(f"""
        <div style="
            background: {DesignSystem.COLORS['background']};
            border: 1px solid {DesignSystem.COLORS['border']};
            border-top: none;
            border-radius: 0 0 {DesignSystem.BORDER_RADIUS['md']} {DesignSystem.BORDER_RADIUS['md']};
            padding: {DesignSystem.SPACING['lg']};
            margin: 0 0 {DesignSystem.SPACING['md']} 0;
            box-shadow: {DesignSystem.SHADOWS['sm']};
            text-align: center;
        ">
        """, unsafe_allow_html=True)

        # Label
        st.markdown(f"""
        <div style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            font-weight: 500;
            margin: 0 0 {DesignSystem.SPACING['sm']} 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        ">
            {label}
        </div>
        """, unsafe_allow_html=True)

        # Value
        st.markdown(f"""
        <div style="
            color: {DesignSystem.COLORS['text']};
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 {DesignSystem.SPACING['xs']} 0;
            line-height: 1.2;
        ">
            {value}
        </div>
        """, unsafe_allow_html=True)

        # Trend indicator
        if trend:
            trend_color = DesignSystem.COLORS['success'] if trend.startswith('+') else DesignSystem.COLORS['error']
            st.markdown(f"""
            <div style="
                color: {trend_color};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                font-weight: 600;
                margin: {DesignSystem.SPACING['xs']} 0;
            ">
                {trend}
            </div>
            """, unsafe_allow_html=True)

        # Help text
        if help_text:
            st.markdown(f"""
            <div style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['caption']['size']};
                margin: {DesignSystem.SPACING['xs']} 0 0 0;
                line-height: 1.4;
            ">
                {help_text}
            </div>
            """, unsafe_allow_html=True)

        # Close the container
        st.markdown("</div>", unsafe_allow_html=True)

def create_metric_row(metrics: list, columns: int = 4, gap: str = "md"):
    """Create a row of metric cards with consistent spacing"""

    # Create columns
    cols = st.columns(columns)

    for i, metric in enumerate(metrics):
        with cols[i]:
            # Extract metric data
            label = metric.get('label', '')
            value = metric.get('value', '')
            help_text = metric.get('help', '')
            trend = metric.get('trend', None)
            color = metric.get('color', 'primary')

            # Create and display metric card
            create_metric_card(label, value, help_text, trend, color)

def create_kpi_dashboard(kpis: list):
    """Create a comprehensive KPI dashboard with multiple metric rows"""

    # Group KPIs by category if provided
    if isinstance(kpis[0], dict) and 'category' in kpis[0]:
        categories = {}
        for kpi in kpis:
            category = kpi.get('category', 'General')
            if category not in categories:
                categories[category] = []
            categories[category].append(kpi)

        # Display each category
        for category, category_kpis in categories.items():
            create_section_header(f"📊 {category}", level=4)
            create_metric_row(category_kpis, columns=4)
            st.markdown("---")
    else:
        # Display all KPIs in rows
        create_metric_row(kpis, columns=4)

def create_comparison_metrics(metrics: list, title: str = "השוואה"):
    """Create comparison metrics with before/after or target/actual values"""

    st.markdown(f"""
    <h4 style="
        color: {DesignSystem.COLORS['text']};
        font-size: {DesignSystem.TYPOGRAPHY['h4']['size']};
        font-weight: {DesignSystem.TYPOGRAPHY['h4']['weight']};
        margin: {DesignSystem.SPACING['lg']} 0 {DesignSystem.SPACING['md']} 0;
        text-align: center;
    ">
        {title}
    </h4>
    """, unsafe_allow_html=True)

    # Create comparison cards
    cols = st.columns(len(metrics))

    for i, metric in enumerate(cols):
        with metric:
            comparison_html = f"""
            <div style="
                background: {DesignSystem.COLORS['surface']};
                border: 1px solid {DesignSystem.COLORS['border']};
                border-radius: {DesignSystem.BORDER_RADIUS['md']};
                padding: {DesignSystem.SPACING['lg']};
                text-align: center;
                box-shadow: {DesignSystem.SHADOWS['sm']};
            ">
                <div style="
                    color: {DesignSystem.COLORS['text_secondary']};
                    font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                    margin-bottom: {DesignSystem.SPACING['sm']};
                ">
                    {metrics[i].get('label', '')}
                </div>
                <div style="
                    color: {DesignSystem.COLORS['text']};
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: {DesignSystem.SPACING['xs']};
                ">
                    {metrics[i].get('value', '')}
                </div>
                <div style="
                    color: {DesignSystem.COLORS['text_secondary']};
                    font-size: {DesignSystem.TYPOGRAPHY['caption']['size']};
                ">
                    {metrics[i].get('subtitle', '')}
                </div>
            </div>
            """
            st.markdown(comparison_html, unsafe_allow_html=True)
