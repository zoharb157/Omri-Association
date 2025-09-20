#!/usr/bin/env python3
"""
Simplified UI Components - Bulletproof Streamlit Components
Uses only native Streamlit components to avoid HTML rendering issues
"""

import streamlit as st


def create_simple_metric_card(
    label: str, value: str, help_text: str = "", trend: str = None, color: str = "primary"
):
    """Create a simple metric card using only Streamlit native components"""

    # Use Streamlit's native metric component
    if trend:
        st.metric(label=label, value=value, delta=trend, help=help_text)
    else:
        st.metric(label=label, value=value, help=help_text)


def create_simple_metric_row(metrics: list, columns: int = 4):
    """Create a row of metric cards using native Streamlit components"""

    # Handle None or empty metrics
    if not metrics:
        return

    try:
        # Create columns
        cols = st.columns(columns)

        for i, metric in enumerate(metrics):
            with cols[i % len(cols)]:
                # Extract metric data
                label = metric.get("label", "")
                value = metric.get("value", "")
                help_text = metric.get("help", "")
                trend = metric.get("trend", None)

                # Create metric card
                create_simple_metric_card(label, value, help_text, trend)
    except Exception:
        # Handle any errors in metric row creation gracefully
        pass


def create_simple_section_header(title: str, description: str = "", icon: str = ""):
    """Create a simple section header using native Streamlit components"""

    try:
        # Add icon if provided
        if icon:
            st.subheader(f"{icon} {title}")
        else:
            st.subheader(title)

        # Add description if provided
        if description:
            st.caption(description)

        # Add some spacing
        st.markdown("---")
    except Exception:
        # Handle any errors in section header creation gracefully
        pass


def create_simple_info_card(title: str, content: str, icon: str = ""):
    """Create a simple info card using Streamlit's expander"""

    with st.expander(f"{icon} {title}" if icon else title, expanded=True):
        st.write(content)


def create_simple_alert(message: str, type: str = "info"):
    """Create a simple alert using Streamlit's native alerts"""

    if type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    elif type == "success":
        st.success(message)
    else:
        st.info(message)


def create_simple_progress_bar(progress: float, message: str = "טוען..."):
    """Create a simple progress bar"""

    st.progress(progress)
    st.caption(message)
