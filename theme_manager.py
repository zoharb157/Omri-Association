#!/usr/bin/env python3
"""
Theme Manager for Omri Association Dashboard
Provides dark/light mode switching and theme customization
"""

import streamlit as st

from config import get_setting, set_setting


class ThemeManager:
    """Manages dashboard themes and appearance"""

    def __init__(self):
        self.themes = {
            'light': {
                'name': 'אור',
                'primary_color': '#1f77b4',
                'background_color': '#ffffff',
                'secondary_background_color': '#f0f2f6',
                'text_color': '#000000',
                'accent_color': '#ff6b6b',
                'success_color': '#28a745',
                'warning_color': '#ffc107',
                'error_color': '#dc3545',
                'info_color': '#17a2b8'
            },
            'dark': {
                'name': 'כהה',
                'primary_color': '#4da6ff',
                'background_color': '#0e1117',
                'secondary_background_color': '#262730',
                'text_color': '#fafafa',
                'accent_color': '#ff8e8e',
                'success_color': '#4ade80',
                'warning_color': '#fbbf24',
                'error_color': '#f87171',
                'info_color': '#60a5fa'
            },
            'blue': {
                'name': 'כחול',
                'primary_color': '#1e40af',
                'background_color': '#eff6ff',
                'secondary_background_color': '#dbeafe',
                'text_color': '#1e293b',
                'accent_color': '#3b82f6',
                'success_color': '#059669',
                'warning_color': '#d97706',
                'error_color': '#dc2626',
                'info_color': '#0891b2'
            }
        }

    def get_current_theme(self) -> str:
        """Get current theme name"""
        return get_setting('ENABLE_DARK_MODE', False) and 'dark' or 'light'

    def get_theme_colors(self, theme_name: str = None) -> dict:
        """Get colors for specified theme"""
        if theme_name is None:
            theme_name = self.get_current_theme()

        return self.themes.get(theme_name, self.themes['light'])

    def switch_theme(self, theme_name: str):
        """Switch to specified theme"""
        if theme_name == 'dark':
            set_setting('ENABLE_DARK_MODE', True)
        else:
            set_setting('ENABLE_DARK_MODE', False)

    def apply_theme_css(self):
        """Apply theme CSS to Streamlit"""
        theme_colors = self.get_theme_colors()

        css = f"""
        <style>
        .stApp {{
            background-color: {theme_colors['background_color']};
            color: {theme_colors['text_color']};
        }}

        .main .block-container {{
            background-color: {theme_colors['background_color']};
        }}

        .stTabs [data-baseweb="tab-list"] {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stTabs [aria-selected="true"] {{
            background-color: {theme_colors['primary_color']};
            color: white;
        }}

        .stButton > button {{
            background-color: {theme_colors['primary_color']};
            color: white;
            border: none;
        }}

        .stButton > button:hover {{
            background-color: {theme_colors['accent_color']};
        }}

        .stMetric {{
            background-color: {theme_colors['secondary_background_color']};
            padding: 1rem;
            border-radius: 0.5rem;
        }}

        .stAlert {{
            background-color: {theme_colors['secondary_background_color']};
            border-left: 4px solid {theme_colors['primary_color']};
        }}

        .stSuccess {{
            background-color: {theme_colors['success_color']}20;
            border-left: 4px solid {theme_colors['success_color']};
        }}

        .stWarning {{
            background-color: {theme_colors['warning_color']}20;
            border-left: 4px solid {theme_colors['warning_color']};
        }}

        .stError {{
            background-color: {theme_colors['error_color']}20;
            border-left: 4px solid {theme_colors['error_color']};
        }}

        .stInfo {{
            background-color: {theme_colors['info_color']}20;
            border-left: 4px solid {theme_colors['info_color']};
        }}

        .stDataFrame {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stDataFrame table {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stDataFrame th {{
            background-color: {theme_colors['primary_color']};
            color: white;
        }}

        .stDataFrame td {{
            background-color: {theme_colors['background_color']};
            color: {theme_colors['text_color']};
        }}

        .stSelectbox {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stTextInput > div > div > input {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stNumberInput > div > div > input {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stTextArea > div > div > textarea {{
            background-color: {theme_colors['secondary_background_color']};
            color: {theme_colors['text_color']};
        }}

        .stCheckbox {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stRadio {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stSidebar {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stSidebar .sidebar-content {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        .stSidebar .sidebar-content .block-container {{
            background-color: {theme_colors['secondary_background_color']};
        }}

        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: {theme_colors['secondary_background_color']};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {theme_colors['primary_color']};
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {theme_colors['accent_color']};
        }}

        /* Animations */
        .stMetric, .stButton > button, .stAlert {{
            transition: all 0.3s ease;
        }}

        .stMetric:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .stMetric {{
                margin-bottom: 1rem;
            }}
        }}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)

    def show_theme_selector(self):
        """Show theme selection UI"""
        st.markdown("#### 🎨 בחירת עיצוב")

        current_theme = self.get_current_theme()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("☀️ עיצוב בהיר",
                        use_container_width=True,
                        type="primary" if current_theme == 'light' else "secondary"):
                self.switch_theme('light')
                st.success("✅ עוצב בהיר הופעל")
                st.rerun()

        with col2:
            if st.button("🌙 עיצוב כהה",
                        use_container_width=True,
                        type="primary" if current_theme == 'dark' else "secondary"):
                self.switch_theme('dark')
                st.success("✅ עיצוב כהה הופעל")
                st.rerun()

        with col3:
            if st.button("🔵 עיצוב כחול",
                        use_container_width=True,
                        type="primary" if current_theme == 'blue' else "secondary"):
                self.switch_theme('blue')
                st.success("✅ עיצוב כחול הופעל")
                st.rerun()

        # Show current theme info
        st.info(f"🎨 עיצוב נוכחי: **{self.themes[current_theme]['name']}**")

        # Theme preview
        st.markdown("#### 👁️ תצוגה מקדימה")
        theme_colors = self.get_theme_colors()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style="
                background-color: {theme_colors['primary_color']};
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
            ">
                צבע ראשי
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background-color: {theme_colors['success_color']};
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
            ">
                צבע הצלחה
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background-color: {theme_colors['warning_color']};
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
            ">
                צבע אזהרה
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="
                background-color: {theme_colors['error_color']};
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
            ">
                צבע שגיאה
            </div>
            """, unsafe_allow_html=True)

# Global theme manager instance
theme_manager = ThemeManager()

def get_theme_manager() -> ThemeManager:
    """Get global theme manager instance"""
    return theme_manager

def apply_current_theme():
    """Apply current theme to Streamlit"""
    theme_manager.apply_theme_css()

def show_theme_selector():
    """Show theme selection UI"""
    theme_manager.show_theme_selector()

def get_current_theme_colors() -> dict:
    """Get current theme colors"""
    return theme_manager.get_theme_colors()
