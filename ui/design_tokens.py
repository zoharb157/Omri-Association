#!/usr/bin/env python3
"""
Design System for Omri Association Dashboard
Centralized design tokens and styling utilities
"""

class DesignSystem:
    """Centralized design system with consistent tokens"""
    
    # Color Palette
    COLORS = {
        'primary': '#1f77b4',           # Blue
        'primary_light': '#4a9eff',     # Light Blue
        'primary_dark': '#1565c0',      # Dark Blue
        'secondary': '#ff7f0e',         # Orange
        'secondary_light': '#ffb74d',   # Light Orange
        'secondary_dark': '#f57c00',    # Dark Orange
        'success': '#2ecc71',           # Green
        'warning': '#f39c12',           # Yellow
        'error': '#e74c3c',             # Red
        'info': '#3498db',              # Light Blue
        'background': '#ffffff',        # White
        'surface': '#f8f9fa',           # Light Gray
        'surface_dark': '#e9ecef',      # Darker Gray
        'text': '#2c3e50',              # Dark Gray
        'text_secondary': '#7f8c8d',    # Medium Gray
        'text_light': '#bdc3c7',        # Light Gray
        'border': '#dee2e6',            # Border Gray
        'shadow': 'rgba(0, 0, 0, 0.1)', # Shadow
    }
    
    # Spacing Scale (8px grid system)
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px',
        'xxxl': '64px',
    }
    
    # Typography Scale
    TYPOGRAPHY = {
        'h1': {
            'size': '2.5rem',
            'weight': '700',
            'line_height': '1.2',
            'margin_bottom': '24px'
        },
        'h2': {
            'size': '2rem',
            'weight': '600',
            'line_height': '1.3',
            'margin_bottom': '20px'
        },
        'h3': {
            'size': '1.5rem',
            'weight': '600',
            'line_height': '1.4',
            'margin_bottom': '16px'
        },
        'h4': {
            'size': '1.25rem',
            'weight': '600',
            'line_height': '1.4',
            'margin_bottom': '12px'
        },
        'body': {
            'size': '1rem',
            'weight': '400',
            'line_height': '1.5',
            'margin_bottom': '8px'
        },
        'body_small': {
            'size': '0.875rem',
            'weight': '400',
            'line_height': '1.4',
            'margin_bottom': '6px'
        },
        'caption': {
            'size': '0.75rem',
            'weight': '400',
            'line_height': '1.4',
            'margin_bottom': '4px'
        }
    }
    
    # Border Radius
    BORDER_RADIUS = {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'full': '50%'
    }
    
    # Shadows
    SHADOWS = {
        'sm': '0 1px 3px rgba(0, 0, 0, 0.1)',
        'md': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px rgba(0, 0, 0, 0.1)'
    }
    
    # Breakpoints
    BREAKPOINTS = {
        'mobile': '768px',
        'tablet': '1024px',
        'desktop': '1200px',
        'wide': '1400px'
    }

def get_global_css():
    """Generate global CSS with modern design system tokens"""
    from ui.design_system.modern_tokens import get_modern_css
    return get_modern_css()
