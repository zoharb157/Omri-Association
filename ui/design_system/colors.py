"""
Color System for Omri Association Dashboard
Centralized color definitions and utilities
"""

from typing import Dict


class ColorSystem:
    """Centralized color system for consistent theming"""

    # Primary Colors
    PRIMARY_BLUE = "#2563eb"
    PRIMARY_BLUE_LIGHT = "#3b82f6"
    PRIMARY_BLUE_DARK = "#1d4ed8"

    # Secondary Colors
    SECONDARY_GRAY = "#64748b"
    SECONDARY_GRAY_LIGHT = "#94a3b8"
    SECONDARY_GRAY_DARK = "#475569"

    # Accent Colors
    ACCENT_GREEN = "#059669"
    ACCENT_ORANGE = "#ea580c"
    ACCENT_RED = "#dc2626"
    ACCENT_PURPLE = "#7c3aed"

    # Neutral Colors
    WHITE = "#ffffff"
    GRAY_50 = "#f8fafc"
    GRAY_100 = "#f1f5f9"
    GRAY_200 = "#e2e8f0"
    GRAY_300 = "#cbd5e1"
    GRAY_400 = "#94a3b8"
    GRAY_500 = "#64748b"
    GRAY_600 = "#475569"
    GRAY_700 = "#334155"
    GRAY_800 = "#1e293b"
    GRAY_900 = "#0f172a"

    # Semantic Colors
    SUCCESS = ACCENT_GREEN
    WARNING = ACCENT_ORANGE
    ERROR = ACCENT_RED
    INFO = PRIMARY_BLUE

    @classmethod
    def get_color_palette(cls) -> Dict[str, str]:
        """Get complete color palette"""
        return {
            "primary": cls.PRIMARY_BLUE,
            "primary_light": cls.PRIMARY_BLUE_LIGHT,
            "primary_dark": cls.PRIMARY_BLUE_DARK,
            "secondary": cls.SECONDARY_GRAY,
            "secondary_light": cls.SECONDARY_GRAY_LIGHT,
            "secondary_dark": cls.SECONDARY_GRAY_DARK,
            "accent_green": cls.ACCENT_GREEN,
            "accent_orange": cls.ACCENT_ORANGE,
            "accent_red": cls.ACCENT_RED,
            "accent_purple": cls.ACCENT_PURPLE,
            "white": cls.WHITE,
            "gray_50": cls.GRAY_50,
            "gray_100": cls.GRAY_100,
            "gray_200": cls.GRAY_200,
            "gray_300": cls.GRAY_300,
            "gray_400": cls.GRAY_400,
            "gray_500": cls.GRAY_500,
            "gray_600": cls.GRAY_600,
            "gray_700": cls.GRAY_700,
            "gray_800": cls.GRAY_800,
            "gray_900": cls.GRAY_900,
            "success": cls.SUCCESS,
            "warning": cls.WARNING,
            "error": cls.ERROR,
            "info": cls.INFO,
        }

    @classmethod
    def get_semantic_colors(cls) -> Dict[str, str]:
        """Get semantic color mappings"""
        return {
            "success": cls.SUCCESS,
            "warning": cls.WARNING,
            "error": cls.ERROR,
            "info": cls.INFO,
        }

    @classmethod
    def get_chart_colors(cls) -> list:
        """Get color palette for charts"""
        return [
            cls.PRIMARY_BLUE,
            cls.ACCENT_GREEN,
            cls.ACCENT_ORANGE,
            cls.ACCENT_RED,
            cls.ACCENT_PURPLE,
            cls.SECONDARY_GRAY,
            cls.PRIMARY_BLUE_LIGHT,
            cls.ACCENT_GREEN + "80",  # With transparency
        ]
