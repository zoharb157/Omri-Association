"""
Spacing System for Omri Association Dashboard
Centralized spacing definitions and utilities
"""

from typing import Dict


class SpacingSystem:
    """Centralized spacing system for consistent layouts"""

    # Spacing Scale (8px base)
    SPACE_1 = "0.25rem"    # 4px
    SPACE_2 = "0.5rem"     # 8px
    SPACE_3 = "0.75rem"    # 12px
    SPACE_4 = "1rem"       # 16px
    SPACE_5 = "1.25rem"    # 20px
    SPACE_6 = "1.5rem"     # 24px
    SPACE_8 = "2rem"       # 32px
    SPACE_10 = "2.5rem"    # 40px
    SPACE_12 = "3rem"      # 48px
    SPACE_16 = "4rem"      # 64px
    SPACE_20 = "5rem"      # 80px
    SPACE_24 = "6rem"      # 96px
    SPACE_32 = "8rem"      # 128px
    SPACE_40 = "10rem"     # 160px
    SPACE_48 = "12rem"     # 192px
    SPACE_56 = "14rem"     # 224px
    SPACE_64 = "16rem"     # 256px

    @classmethod
    def get_spacing_scale(cls) -> Dict[str, str]:
        """Get complete spacing scale"""
        return {
            '1': cls.SPACE_1,
            '2': cls.SPACE_2,
            '3': cls.SPACE_3,
            '4': cls.SPACE_4,
            '5': cls.SPACE_5,
            '6': cls.SPACE_6,
            '8': cls.SPACE_8,
            '10': cls.SPACE_10,
            '12': cls.SPACE_12,
            '16': cls.SPACE_16,
            '20': cls.SPACE_20,
            '24': cls.SPACE_24,
            '32': cls.SPACE_32,
            '40': cls.SPACE_40,
            '48': cls.SPACE_48,
            '56': cls.SPACE_56,
            '64': cls.SPACE_64,
        }

    @classmethod
    def get_component_spacing(cls) -> Dict[str, str]:
        """Get predefined spacing for common components"""
        return {
            # Padding
            'padding_small': cls.SPACE_2,
            'padding_medium': cls.SPACE_4,
            'padding_large': cls.SPACE_6,
            'padding_xlarge': cls.SPACE_8,

            # Margin
            'margin_small': cls.SPACE_2,
            'margin_medium': cls.SPACE_4,
            'margin_large': cls.SPACE_6,
            'margin_xlarge': cls.SPACE_8,

            # Gap
            'gap_small': cls.SPACE_2,
            'gap_medium': cls.SPACE_4,
            'gap_large': cls.SPACE_6,
            'gap_xlarge': cls.SPACE_8,

            # Border radius
            'radius_small': cls.SPACE_1,
            'radius_medium': cls.SPACE_2,
            'radius_large': cls.SPACE_3,
            'radius_xlarge': cls.SPACE_4,
        }

    @classmethod
    def get_css_variables(cls) -> str:
        """Get CSS custom properties for spacing"""
        return f"""
        :root {{
            --space-1: {cls.SPACE_1};
            --space-2: {cls.SPACE_2};
            --space-3: {cls.SPACE_3};
            --space-4: {cls.SPACE_4};
            --space-5: {cls.SPACE_5};
            --space-6: {cls.SPACE_6};
            --space-8: {cls.SPACE_8};
            --space-10: {cls.SPACE_10};
            --space-12: {cls.SPACE_12};
            --space-16: {cls.SPACE_16};
            --space-20: {cls.SPACE_20};
            --space-24: {cls.SPACE_24};
            --space-32: {cls.SPACE_32};
            --space-40: {cls.SPACE_40};
            --space-48: {cls.SPACE_48};
            --space-56: {cls.SPACE_56};
            --space-64: {cls.SPACE_64};
        }}
        """
