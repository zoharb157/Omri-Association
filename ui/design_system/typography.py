"""
Typography System for Omri Association Dashboard
Centralized font definitions and text styles
"""

from typing import Dict, Any

class TypographySystem:
    """Centralized typography system for consistent text styling"""
    
    # Font Families
    FONT_PRIMARY = "'Segoe UI', 'Noto Sans Hebrew', 'Arial Hebrew', sans-serif"
    FONT_MONO = "'Consolas', 'Monaco', 'Courier New', monospace"
    
    # Font Sizes (rem units)
    TEXT_XS = "0.75rem"      # 12px
    TEXT_SM = "0.875rem"     # 14px
    TEXT_BASE = "1rem"       # 16px
    TEXT_LG = "1.125rem"     # 18px
    TEXT_XL = "1.25rem"      # 20px
    TEXT_2XL = "1.5rem"      # 24px
    TEXT_3XL = "1.875rem"    # 30px
    TEXT_4XL = "2.25rem"     # 36px
    TEXT_5XL = "3rem"        # 48px
    
    # Font Weights
    FONT_LIGHT = "300"
    FONT_NORMAL = "400"
    FONT_MEDIUM = "500"
    FONT_SEMIBOLD = "600"
    FONT_BOLD = "700"
    FONT_EXTRABOLD = "800"
    
    # Line Heights
    LEADING_TIGHT = "1.25"
    LEADING_SNUG = "1.375"
    LEADING_NORMAL = "1.5"
    LEADING_RELAXED = "1.625"
    LEADING_LOOSE = "2"
    
    @classmethod
    def get_font_sizes(cls) -> Dict[str, str]:
        """Get all font sizes"""
        return {
            'xs': cls.TEXT_XS,
            'sm': cls.TEXT_SM,
            'base': cls.TEXT_BASE,
            'lg': cls.TEXT_LG,
            'xl': cls.TEXT_XL,
            '2xl': cls.TEXT_2XL,
            '3xl': cls.TEXT_3XL,
            '4xl': cls.TEXT_4XL,
            '5xl': cls.TEXT_5XL,
        }
    
    @classmethod
    def get_font_weights(cls) -> Dict[str, str]:
        """Get all font weights"""
        return {
            'light': cls.FONT_LIGHT,
            'normal': cls.FONT_NORMAL,
            'medium': cls.FONT_MEDIUM,
            'semibold': cls.FONT_SEMIBOLD,
            'bold': cls.FONT_BOLD,
            'extrabold': cls.FONT_EXTRABOLD,
        }
    
    @classmethod
    def get_text_styles(cls) -> Dict[str, Dict[str, str]]:
        """Get predefined text styles"""
        return {
            'heading_1': {
                'font_size': cls.TEXT_5XL,
                'font_weight': cls.FONT_BOLD,
                'line_height': cls.LEADING_TIGHT,
                'font_family': cls.FONT_PRIMARY,
            },
            'heading_2': {
                'font_size': cls.TEXT_4XL,
                'font_weight': cls.FONT_BOLD,
                'line_height': cls.LEADING_TIGHT,
                'font_family': cls.FONT_PRIMARY,
            },
            'heading_3': {
                'font_size': cls.TEXT_3XL,
                'font_weight': cls.FONT_SEMIBOLD,
                'line_height': cls.LEADING_SNUG,
                'font_family': cls.FONT_PRIMARY,
            },
            'heading_4': {
                'font_size': cls.TEXT_2XL,
                'font_weight': cls.FONT_SEMIBOLD,
                'line_height': cls.LEADING_SNUG,
                'font_family': cls.FONT_PRIMARY,
            },
            'body_large': {
                'font_size': cls.TEXT_LG,
                'font_weight': cls.FONT_NORMAL,
                'line_height': cls.LEADING_RELAXED,
                'font_family': cls.FONT_PRIMARY,
            },
            'body': {
                'font_size': cls.TEXT_BASE,
                'font_weight': cls.FONT_NORMAL,
                'line_height': cls.LEADING_NORMAL,
                'font_family': cls.FONT_PRIMARY,
            },
            'body_small': {
                'font_size': cls.TEXT_SM,
                'font_weight': cls.FONT_NORMAL,
                'line_height': cls.LEADING_NORMAL,
                'font_family': cls.FONT_PRIMARY,
            },
            'caption': {
                'font_size': cls.TEXT_XS,
                'font_weight': cls.FONT_NORMAL,
                'line_height': cls.LEADING_NORMAL,
                'font_family': cls.FONT_PRIMARY,
            },
            'button': {
                'font_size': cls.TEXT_BASE,
                'font_weight': cls.FONT_MEDIUM,
                'line_height': cls.LEADING_NORMAL,
                'font_family': cls.FONT_PRIMARY,
            },
            'code': {
                'font_size': cls.TEXT_SM,
                'font_weight': cls.FONT_NORMAL,
                'line_height': cls.LEADING_NORMAL,
                'font_family': cls.FONT_MONO,
            },
        }
    
    @classmethod
    def get_css_variables(cls) -> str:
        """Get CSS custom properties for typography"""
        return f"""
        :root {{
            --font-primary: {cls.FONT_PRIMARY};
            --font-mono: {cls.FONT_MONO};
            
            --text-xs: {cls.TEXT_XS};
            --text-sm: {cls.TEXT_SM};
            --text-base: {cls.TEXT_BASE};
            --text-lg: {cls.TEXT_LG};
            --text-xl: {cls.TEXT_XL};
            --text-2xl: {cls.TEXT_2XL};
            --text-3xl: {cls.TEXT_3XL};
            --text-4xl: {cls.TEXT_4XL};
            --text-5xl: {cls.TEXT_5XL};
            
            --font-light: {cls.FONT_LIGHT};
            --font-normal: {cls.FONT_NORMAL};
            --font-medium: {cls.FONT_MEDIUM};
            --font-semibold: {cls.FONT_SEMIBOLD};
            --font-bold: {cls.FONT_BOLD};
            --font-extrabold: {cls.FONT_EXTRABOLD};
            
            --leading-tight: {cls.LEADING_TIGHT};
            --leading-snug: {cls.LEADING_SNUG};
            --leading-normal: {cls.LEADING_NORMAL};
            --leading-relaxed: {cls.LEADING_RELAXED};
            --leading-loose: {cls.LEADING_LOOSE};
        }}
        """
