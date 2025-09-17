"""
Theme System for Omri Association Dashboard
Centralized theme definitions and management
"""

from typing import Any, Dict

from .colors import ColorSystem
from .spacing import SpacingSystem
from .typography import TypographySystem


class ThemeManager:
    """Centralized theme management system"""

    def __init__(self):
        self.colors = ColorSystem()
        self.typography = TypographySystem()
        self.spacing = SpacingSystem()

    def get_light_theme(self) -> Dict[str, Any]:
        """Get light theme configuration"""
        return {
            "name": "light",
            "colors": {
                "primary": self.colors.PRIMARY_BLUE,
                "primary_light": self.colors.PRIMARY_BLUE_LIGHT,
                "primary_dark": self.colors.PRIMARY_BLUE_DARK,
                "secondary": self.colors.SECONDARY_GRAY,
                "secondary_light": self.colors.SECONDARY_GRAY_LIGHT,
                "secondary_dark": self.colors.SECONDARY_GRAY_DARK,
                "background": self.colors.WHITE,
                "surface": self.colors.GRAY_50,
                "surface_variant": self.colors.GRAY_100,
                "text_primary": self.colors.GRAY_900,
                "text_secondary": self.colors.GRAY_600,
                "text_disabled": self.colors.GRAY_400,
                "border": self.colors.GRAY_200,
                "border_light": self.colors.GRAY_100,
                "success": self.colors.SUCCESS,
                "warning": self.colors.WARNING,
                "error": self.colors.ERROR,
                "info": self.colors.INFO,
            },
            "typography": self.typography.get_text_styles(),
            "spacing": self.spacing.get_spacing_scale(),
        }

    def get_dark_theme(self) -> Dict[str, Any]:
        """Get dark theme configuration"""
        return {
            "name": "dark",
            "colors": {
                "primary": self.colors.PRIMARY_BLUE_LIGHT,
                "primary_light": self.colors.PRIMARY_BLUE,
                "primary_dark": self.colors.PRIMARY_BLUE_DARK,
                "secondary": self.colors.SECONDARY_GRAY_LIGHT,
                "secondary_light": self.colors.SECONDARY_GRAY,
                "secondary_dark": self.colors.SECONDARY_GRAY_DARK,
                "background": self.colors.GRAY_900,
                "surface": self.colors.GRAY_800,
                "surface_variant": self.colors.GRAY_700,
                "text_primary": self.colors.WHITE,
                "text_secondary": self.colors.GRAY_300,
                "text_disabled": self.colors.GRAY_500,
                "border": self.colors.GRAY_600,
                "border_light": self.colors.GRAY_700,
                "success": self.colors.SUCCESS,
                "warning": self.colors.WARNING,
                "error": self.colors.ERROR,
                "info": self.colors.INFO,
            },
            "typography": self.typography.get_text_styles(),
            "spacing": self.spacing.get_spacing_scale(),
        }

    def get_blue_theme(self) -> Dict[str, Any]:
        """Get blue theme configuration"""
        return {
            "name": "blue",
            "colors": {
                "primary": self.colors.PRIMARY_BLUE_DARK,
                "primary_light": self.colors.PRIMARY_BLUE,
                "primary_dark": self.colors.GRAY_800,
                "secondary": self.colors.SECONDARY_GRAY,
                "secondary_light": self.colors.SECONDARY_GRAY_LIGHT,
                "secondary_dark": self.colors.SECONDARY_GRAY_DARK,
                "background": self.colors.GRAY_50,
                "surface": self.colors.WHITE,
                "surface_variant": self.colors.GRAY_100,
                "text_primary": self.colors.GRAY_800,
                "text_secondary": self.colors.GRAY_600,
                "text_disabled": self.colors.GRAY_400,
                "border": self.colors.GRAY_200,
                "border_light": self.colors.GRAY_100,
                "success": self.colors.SUCCESS,
                "warning": self.colors.WARNING,
                "error": self.colors.ERROR,
                "info": self.colors.INFO,
            },
            "typography": self.typography.get_text_styles(),
            "spacing": self.spacing.get_spacing_scale(),
        }

    def get_theme_css(self, theme_name: str = "light") -> str:
        """Generate CSS for specified theme"""
        if theme_name == "dark":
            theme = self.get_dark_theme()
        elif theme_name == "blue":
            theme = self.get_blue_theme()
        else:
            theme = self.get_light_theme()

        colors = theme["colors"]

        return f"""
        <style>
        :root {{
            /* Color Variables */
            --color-primary: {colors['primary']};
            --color-primary-light: {colors['primary_light']};
            --color-primary-dark: {colors['primary_dark']};
            --color-secondary: {colors['secondary']};
            --color-secondary-light: {colors['secondary_light']};
            --color-secondary-dark: {colors['secondary_dark']};
            --color-background: {colors['background']};
            --color-surface: {colors['surface']};
            --color-surface-variant: {colors['surface_variant']};
            --color-text-primary: {colors['text_primary']};
            --color-text-secondary: {colors['text_secondary']};
            --color-text-disabled: {colors['text_disabled']};
            --color-border: {colors['border']};
            --color-border-light: {colors['border_light']};
            --color-success: {colors['success']};
            --color-warning: {colors['warning']};
            --color-error: {colors['error']};
            --color-info: {colors['info']};
        }}

        /* Typography Variables */
        {self.typography.get_css_variables()}

        /* Spacing Variables */
        {self.spacing.get_css_variables()}

        /* Base Styles */
        .stApp {{
            background-color: var(--color-background);
            color: var(--color-text-primary);
            font-family: var(--font-primary);
        }}

        .main .block-container {{
            background-color: var(--color-background);
            color: var(--color-text-primary);
        }}

        /* Typography Styles */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--color-text-primary);
            font-family: var(--font-primary);
        }}

        h1 {{ font-size: var(--text-5xl); font-weight: var(--font-bold); }}
        h2 {{ font-size: var(--text-4xl); font-weight: var(--font-bold); }}
        h3 {{ font-size: var(--text-3xl); font-weight: var(--font-semibold); }}
        h4 {{ font-size: var(--text-2xl); font-weight: var(--font-semibold); }}
        h5 {{ font-size: var(--text-xl); font-weight: var(--font-medium); }}
        h6 {{ font-size: var(--text-lg); font-weight: var(--font-medium); }}

        p, div, span {{
            color: var(--color-text-primary);
            font-family: var(--font-primary);
        }}

        /* Component Styles */
        .metric-card {{
            background-color: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--space-2);
            padding: var(--space-4);
            margin: var(--space-2) 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        .metric-card:hover {{
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transform: translateY(-1px);
            transition: all 0.2s ease;
        }}

        .metric-card h3 {{
            color: var(--color-text-secondary);
            font-size: var(--text-sm);
            font-weight: var(--font-medium);
            margin-bottom: var(--space-2);
        }}

        .metric-card h2 {{
            color: var(--color-primary);
            font-size: var(--text-2xl);
            font-weight: var(--font-bold);
            margin: 0;
        }}

        /* Button Styles */
        .stButton > button {{
            background-color: var(--color-primary);
            color: white;
            border: none;
            border-radius: var(--space-2);
            padding: var(--space-2) var(--space-4);
            font-weight: var(--font-medium);
            transition: all 0.2s ease;
        }}

        .stButton > button:hover {{
            background-color: var(--color-primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: var(--color-surface);
            border-bottom: 1px solid var(--color-border);
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--color-text-secondary);
            font-weight: var(--font-medium);
            padding: var(--space-3) var(--space-4);
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--color-text-primary);
            background-color: var(--color-surface-variant);
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            color: var(--color-primary);
            border-bottom-color: var(--color-primary);
            background-color: var(--color-background);
        }}

        /* Table Styles */
        .stDataFrame {{
            background-color: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--space-2);
            overflow: hidden;
        }}

        .stDataFrame table {{
            background-color: var(--color-surface);
        }}

        .stDataFrame th {{
            background-color: var(--color-primary);
            color: white;
            font-weight: var(--font-semibold);
        }}

        .stDataFrame td {{
            background-color: var(--color-surface);
            color: var(--color-text-primary);
        }}

        /* Chart Styles */
        .stPlotlyChart {{
            background-color: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--space-2);
            padding: var(--space-4);
        }}

        /* Alert Styles */
        .stAlert {{
            border-radius: var(--space-2);
            border-left: 4px solid var(--color-primary);
            background-color: var(--color-surface);
        }}

        .stSuccess {{
            border-left-color: var(--color-success);
            background-color: rgba(5, 150, 105, 0.1);
        }}

        .stWarning {{
            border-left-color: var(--color-warning);
            background-color: rgba(234, 88, 12, 0.1);
        }}

        .stError {{
            border-left-color: var(--color-error);
            background-color: rgba(220, 38, 38, 0.1);
        }}

        .stInfo {{
            border-left-color: var(--color-info);
            background-color: rgba(37, 99, 235, 0.1);
        }}

        /* RTL Support */
        .stApp {{
            direction: rtl;
            text-align: right;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .metric-card {{
                margin: var(--space-1) 0;
            }}

            h1 {{ font-size: var(--text-4xl); }}
            h2 {{ font-size: var(--text-3xl); }}
            h3 {{ font-size: var(--text-2xl); }}
        }}
        </style>
        """
