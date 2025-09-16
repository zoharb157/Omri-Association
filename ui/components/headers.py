#!/usr/bin/env python3
"""
Header Components for Dashboard
Consistent header creation with design system integration
"""

import streamlit as st
from ui.design_system.modern_tokens import ModernDesignSystem

def create_section_header(title: str, icon: str = "", level: int = 3, description: str = ""):
    """Create consistent section headers with proper styling"""
    icon_text = f"{icon} " if icon else ""
    
    # Create header using Streamlit's native components
    if level == 1:
        st.title(f"{icon_text}{title}")
    elif level == 2:
        st.header(f"{icon_text}{title}")
    elif level == 3:
        st.subheader(f"{icon_text}{title}")
    else:
        st.markdown(f"### {icon_text}{title}")
    
    # Add description if provided
    if description:
        st.markdown(f"""
        <p style="
            color: {ModernDesignSystem.COLORS['gray_600']};
            font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']};
            margin: 0 0 {ModernDesignSystem.SPACING['space_6']} 0;
            line-height: 1.5;
        ">
            {description}
        </p>
        """, unsafe_allow_html=True)
    else:
        # Add spacing if no description
        st.markdown(f"<div style='margin-bottom: {ModernDesignSystem.SPACING['space_6']};'></div>", unsafe_allow_html=True)

def create_page_title(title: str, subtitle: str = "", icon: str = ""):
    """Create main page title with optional subtitle"""
    icon_text = f"{icon} " if icon else ""
    
    if subtitle:
        title_html = f"""
        <div class="page-title-container" style="
            text-align: center;
            margin-bottom: {ModernDesignSystem.SPACING['space_8']};
            padding: {ModernDesignSystem.SPACING['space_6']} 0;
            background: linear-gradient(135deg, {ModernDesignSystem.COLORS['primary']}, {ModernDesignSystem.COLORS['primary_500']});
            color: white;
            border-radius: {ModernDesignSystem.BORDER_RADIUS['radius_lg']};
            box-shadow: {ModernDesignSystem.SHADOWS['shadow_lg']};
        ">
            <h1 style="
                font-size: {ModernDesignSystem.TYPOGRAPHY['text_3xl']};
                font-weight: 700;
                margin: 0 0 {ModernDesignSystem.SPACING['space_2']} 0;
                color: white;
            ">
                {icon_text}{title}
            </h1>
            <p style="
                font-size: {ModernDesignSystem.TYPOGRAPHY['text_base']};
                margin: 0;
                opacity: 0.9;
            ">
                {subtitle}
            </p>
        </div>
        """
    else:
        title_html = f"""
        <div class="page-title-container" style="
            text-align: center;
            margin-bottom: {ModernDesignSystem.SPACING['space_8']};
            padding: {ModernDesignSystem.SPACING['space_6']} 0;
            background: linear-gradient(135deg, {ModernDesignSystem.COLORS['primary']}, {ModernDesignSystem.COLORS['primary_500']});
            color: white;
            border-radius: {ModernDesignSystem.BORDER_RADIUS['radius_lg']};
            box-shadow: {ModernDesignSystem.SHADOWS['shadow_lg']};
        ">
            <h1 style="
                font-size: {ModernDesignSystem.TYPOGRAPHY['text_3xl']};
                font-weight: 700;
                margin: 0;
                color: white;
            ">
                {icon_text}{title}
            </h1>
        </div>
        """
    
    st.markdown(title_html, unsafe_allow_html=True)

def create_subsection_header(title: str, icon: str = ""):
    """Create subsection headers for smaller sections"""
    icon_text = f"{icon} " if icon else ""
    
    st.markdown(f"""
    <h4 style="
        color: {ModernDesignSystem.COLORS['gray_900']};
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_lg']};
        font-weight: 600;
        margin: {ModernDesignSystem.SPACING['space_6']} 0 {ModernDesignSystem.SPACING['space_4']} 0;
        padding-left: {ModernDesignSystem.SPACING['space_4']};
        border-left: 4px solid {ModernDesignSystem.COLORS['primary']};
    ">
        {icon_text}{title}
    </h4>
    """, unsafe_allow_html=True)
