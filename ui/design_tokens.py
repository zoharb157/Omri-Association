#!/usr/bin/env python3
"""Legacy design token interface that maps to ModernDesignSystem."""

from __future__ import annotations

from ui.design_system.modern_tokens import ModernDesignSystem


def _spacing(name: str) -> str:
    mapping = {
        "xs": "space_1",
        "sm": "space_2",
        "md": "space_4",
        "lg": "space_6",
        "xl": "space_8",
        "xxl": "space_12",
        "xxxl": "space_16",
    }
    return ModernDesignSystem.SPACING[mapping[name]]


def _typography(name: str) -> dict[str, str]:
    mapping = {
        "h1": "text_4xl",
        "h2": "text_3xl",
        "h3": "text_2xl",
        "h4": "text_xl",
        "body": "text_base",
        "body_small": "text_sm",
        "caption": "text_xs",
    }
    token = ModernDesignSystem.TYPOGRAPHY[mapping[name]]
    return {
        "size": token["size"],
        "weight": token["weight"],
        "line_height": token.get("line_height", "1.5"),
        "margin_bottom": _spacing("sm"),
    }


class DesignSystem:
    """Backwards-compatible wrapper around the modern design system."""

    COLORS = {
        "primary": ModernDesignSystem.COLORS["primary"],
        "primary_light": ModernDesignSystem.COLORS["primary_500"],
        "primary_dark": ModernDesignSystem.COLORS["primary_700"],
        "secondary": ModernDesignSystem.COLORS["info"],
        "secondary_light": ModernDesignSystem.COLORS["info_100"],
        "secondary_dark": ModernDesignSystem.COLORS["info"],
        "success": ModernDesignSystem.COLORS["success"],
        "warning": ModernDesignSystem.COLORS["warning"],
        "error": ModernDesignSystem.COLORS["error"],
        "info": ModernDesignSystem.COLORS["info"],
        "background": ModernDesignSystem.COLORS["background"],
        "surface": ModernDesignSystem.COLORS["surface"],
        "surface_dark": ModernDesignSystem.COLORS["gray_100"],
        "text": ModernDesignSystem.COLORS["gray_800"],
        "text_secondary": ModernDesignSystem.COLORS["gray_500"],
        "text_light": ModernDesignSystem.COLORS["gray_400"],
        "border": ModernDesignSystem.COLORS["border"],
    }

    SPACING = {
        "xs": _spacing("xs"),
        "sm": _spacing("sm"),
        "md": _spacing("md"),
        "lg": _spacing("lg"),
        "xl": _spacing("xl"),
        "xxl": _spacing("xxl"),
        "xxxl": _spacing("xxxl"),
    }

    TYPOGRAPHY = {
        key: _typography(key) for key in ["h1", "h2", "h3", "h4", "body", "body_small", "caption"]
    }

    BORDER_RADIUS = {
        "sm": ModernDesignSystem.BORDER_RADIUS["radius_sm"],
        "md": ModernDesignSystem.BORDER_RADIUS["radius_md"],
        "lg": ModernDesignSystem.BORDER_RADIUS["radius_lg"],
        "xl": ModernDesignSystem.BORDER_RADIUS["radius_xl"],
        "full": ModernDesignSystem.BORDER_RADIUS["radius_full"],
    }

    SHADOWS = {
        "sm": ModernDesignSystem.SHADOWS["shadow_sm"],
        "md": ModernDesignSystem.SHADOWS["shadow_md"],
        "lg": ModernDesignSystem.SHADOWS["shadow_lg"],
        "xl": ModernDesignSystem.SHADOWS["shadow_xl"],
    }

    BREAKPOINTS = ModernDesignSystem.BREAKPOINTS


def get_global_css():
    """Generate global CSS with modern design system tokens"""
    from ui.design_system.modern_tokens import get_modern_css

    return get_modern_css()
