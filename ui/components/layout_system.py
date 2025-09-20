#!/usr/bin/env python3
"""
Minimal Layout System for Omri Association Dashboard
Only contains functions that are actually used
"""

import streamlit as st

from ui.design_system.modern_tokens import ModernDesignSystem


def create_section_header(title: str, subtitle: str = None, actions: list = None):
    """Create a modern section header with optional subtitle and actions."""
    icon_text = f"{title} " if title else ""
    
    header_html = f"""
    <div class="section-header">
        <h2 class="section-title">{icon_text}</h2>
        {f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    <style>
    .section-header {{
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }}
    .section-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }}
    .section-subtitle {{
        font-size: 1rem;
        color: #6b7280;
        margin: 0.5rem 0 0 0;
    }}
    </style>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)


def create_metrics_grid(metrics: list, columns: int = 4):
    """Create a responsive grid of metric cards."""
    if not metrics:
        return
    
    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        with cols[i % columns]:
            create_metric_card(
                title=metric.get("title", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta", None),
                help_text=metric.get("help", None)
            )


def create_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """Create a modern metric card component."""
    delta_html = ""
    if delta:
        delta_class = "positive" if delta.startswith("+") else "negative"
        delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>'
    
    help_html = f'<div class="metric-help">{help_text}</div>' if help_text else ''
    
    card_html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
        {help_html}
    </div>
    <style>
    .metric-card {{
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.2s;
    }}
    .metric-card:hover {{
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .metric-title {{
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }}
    .metric-delta {{
        font-size: 0.875rem;
        font-weight: 500;
    }}
    .metric-delta.positive {{
        color: #059669;
    }}
    .metric-delta.negative {{
        color: #dc2626;
    }}
    .metric-help {{
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 0.5rem;
    }}
    </style>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
