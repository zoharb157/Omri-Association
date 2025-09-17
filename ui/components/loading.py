#!/usr/bin/env python3
"""
Loading Components for Dashboard
Enhanced loading states and progress indicators
"""

import time

import streamlit as st

from ui.design_tokens import DesignSystem


def create_loading_spinner(message: str = "טוען...", size: str = "large"):
    """Create a styled loading spinner"""

    spinner_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: {DesignSystem.SPACING['xxl']};
        text-align: center;
    ">
        <div class="spinner" style="
            width: {DesignSystem.SPACING['xl'] if size == 'large' else DesignSystem.SPACING['lg']};
            height: {DesignSystem.SPACING['xl'] if size == 'large' else DesignSystem.SPACING['lg']};
            border: 4px solid {DesignSystem.COLORS['border']};
            border-top: 4px solid {DesignSystem.COLORS['primary']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: {DesignSystem.SPACING['md']};
        "></div>
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
            margin: 0;
        ">
            {message}
        </p>
    </div>

    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """

    return st.markdown(spinner_html, unsafe_allow_html=True)

def create_progress_bar(message: str = "מעבד נתונים...", progress: float = 0.0):
    """Create a styled progress bar"""

    progress_html = f"""
    <div style="
        background: {DesignSystem.COLORS['surface']};
        border: 1px solid {DesignSystem.COLORS['border']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin: {DesignSystem.SPACING['md']} 0;
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: {DesignSystem.SPACING['sm']};
        ">
            <span style="
                color: {DesignSystem.COLORS['text']};
                font-weight: 500;
            ">
                {message}
            </span>
            <span style="
                color: {DesignSystem.COLORS['text_secondary']};
                font-size: {DesignSystem.TYPOGRAPHY['body_small']['size']};
            ">
                {int(progress * 100)}%
            </span>
        </div>

        <div style="
            width: 100%;
            height: 8px;
            background: {DesignSystem.COLORS['border']};
            border-radius: {DesignSystem.BORDER_RADIUS['sm']};
            overflow: hidden;
        ">
            <div style="
                width: {progress * 100}%;
                height: 100%;
                background: linear-gradient(90deg, {DesignSystem.COLORS['primary']}, {DesignSystem.COLORS['primary_light']});
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """

    return st.markdown(progress_html, unsafe_allow_html=True)

def create_skeleton_card(title: str = "טוען...", lines: int = 3):
    """Create a skeleton loading card"""

    skeleton_lines = ""
    for _i in range(lines):
        skeleton_lines += f"""
        <div style="
            height: 16px;
            background: {DesignSystem.COLORS['surface_dark']};
            border-radius: {DesignSystem.BORDER_RADIUS['sm']};
            margin-bottom: {DesignSystem.SPACING['sm']};
            animation: pulse 1.5s ease-in-out infinite;
        "></div>
        """

    skeleton_html = f"""
    <div style="
        background: {DesignSystem.COLORS['background']};
        border: 1px solid {DesignSystem.COLORS['border']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin-bottom: {DesignSystem.SPACING['md']};
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <div style="
            height: 24px;
            background: {DesignSystem.COLORS['surface_dark']};
            border-radius: {DesignSystem.BORDER_RADIUS['sm']};
            margin-bottom: {DesignSystem.SPACING['md']};
            animation: pulse 1.5s ease-in-out infinite;
        "></div>
        {skeleton_lines}
    </div>

    <style>
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; }}
    }}
    </style>
    """

    return st.markdown(skeleton_html, unsafe_allow_html=True)

def create_data_loading_state():
    """Create a comprehensive data loading state"""

    with st.container():
        st.markdown("### 📊 טוען נתונים...")

        # Progress steps
        steps = [
            "מתחבר ל-Google Sheets...",
            "טוען נתוני הוצאות...",
            "טוען נתוני תרומות...",
            "טוען נתוני אלמנות...",
            "מעבד נתונים...",
            "יוצר ויזואליזציות..."
        ]

        progress_container = st.container()

        for i, step in enumerate(steps):
            with progress_container:
                create_progress_bar(step, (i + 1) / len(steps))
                time.sleep(0.5)  # Simulate loading time

        st.success("✅ הנתונים נטענו בהצלחה!")

def create_chart_loading_state():
    """Create a loading state for charts"""

    loading_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: {DesignSystem.SPACING['xxl']};
        background: {DesignSystem.COLORS['surface']};
        border: 1px solid {DesignSystem.COLORS['border']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        margin: {DesignSystem.SPACING['md']} 0;
    ">
        <div style="
            width: 48px;
            height: 48px;
            border: 4px solid {DesignSystem.COLORS['border']};
            border-top: 4px solid {DesignSystem.COLORS['primary']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: {DesignSystem.SPACING['md']};
        "></div>
        <p style="
            color: {DesignSystem.COLORS['text_secondary']};
            font-size: {DesignSystem.TYPOGRAPHY['body']['size']};
            margin: 0;
        ">
            יוצר גרף...
        </p>
    </div>

    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """

    return st.markdown(loading_html, unsafe_allow_html=True)
