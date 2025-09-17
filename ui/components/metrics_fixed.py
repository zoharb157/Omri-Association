#!/usr/bin/env python3
"""
Fixed Metric Components for Dashboard
Simplified version that should render properly
"""

import streamlit as st

from ui.design_tokens import DesignSystem


def create_metric_card(
    label: str, value: str, help_text: str = "", trend: str = None, color: str = "primary"
):
    """Create a simplified metric card that renders properly"""

    # Get color based on theme
    color_map = {
        "primary": DesignSystem.COLORS["primary"],
        "success": DesignSystem.COLORS["success"],
        "warning": DesignSystem.COLORS["warning"],
        "error": DesignSystem.COLORS["error"],
        "info": DesignSystem.COLORS["info"],
    }

    card_color = color_map.get(color, DesignSystem.COLORS["primary"])

    # Create a simplified metric card using Streamlit's native components
    with st.container():
        # Create a custom container with background
        st.markdown(
            f"""
        <div style="
            background: {DesignSystem.COLORS['background']};
            border: 1px solid {DesignSystem.COLORS['border']};
            border-radius: {DesignSystem.BORDER_RADIUS['md']};
            padding: {DesignSystem.SPACING['lg']};
            margin: {DesignSystem.SPACING['sm']} 0;
            box-shadow: {DesignSystem.SHADOWS['sm']};
            text-align: center;
            position: relative;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: {card_color};
                border-radius: {DesignSystem.BORDER_RADIUS['md']} {DesignSystem.BORDER_RADIUS['md']} 0 0;
            "></div>

            <div style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                font-weight: 500;
                margin: 8px 0 4px 0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">
                {label}
            </div>

            <div style="
                color: {DesignSystem.COLORS['text']};
                font-size: 2rem;
                font-weight: 700;
                margin: 4px 0;
                line-height: 1.2;
            ">
                {value}
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Add trend and help text using Streamlit components
        if trend:
            trend_color = (
                DesignSystem.COLORS["success"]
                if trend.startswith("+")
                else DesignSystem.COLORS["error"]
            )
            st.markdown(
                f"""
            <div style="
                color: {trend_color};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
                font-weight: 600;
                margin: 4px 0;
            ">
                {trend}
            </div>
            """,
                unsafe_allow_html=True,
            )

        if help_text:
            st.markdown(
                f"""
            <div style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['caption']['size']};
                margin: 4px 0;
                line-height: 1.4;
            ">
                {help_text}
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


def create_metric_row(metrics: list, columns: int = 4, gap: str = "md"):
    """Create a row of metric cards with consistent spacing"""

    # Create columns
    cols = st.columns(columns)

    for i, metric in enumerate(metrics):
        with cols[i]:
            # Extract metric data
            label = metric.get("label", "")
            value = metric.get("value", "")
            help_text = metric.get("help", "")
            trend = metric.get("trend", None)
            color = metric.get("color", "primary")

            # Create and display metric card
            create_metric_card(label, value, help_text, trend, color)


def create_simple_metric_card(
    label: str, value: str, help_text: str = "", trend: str = None, color: str = "primary"
):
    """Create a very simple metric card using only Streamlit components"""

    # Use Streamlit's native metric component as base
    if trend:
        st.metric(label=label, value=value, delta=trend, help=help_text)
    else:
        st.metric(label=label, value=value, help=help_text)
