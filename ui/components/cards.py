"""
Card Components for Omri Association Dashboard
Reusable card components with consistent styling
"""

import streamlit as st
from typing import Optional, Dict, Any
from ..design_system.colors import ColorSystem
from ..design_system.typography import TypographySystem
from ..design_system.spacing import SpacingSystem

class MetricCard:
    """Modern metric card component"""
    
    def __init__(self, title: str, value: str, delta: Optional[str] = None, 
                 help_text: Optional[str] = None, icon: Optional[str] = None,
                 color: str = "primary"):
        self.title = title
        self.value = value
        self.delta = delta
        self.help_text = help_text
        self.icon = icon
        self.color = color
        self.colors = ColorSystem()
        self.typography = TypographySystem()
        self.spacing = SpacingSystem()
    
    def render(self):
        """Render the metric card"""
        # Get color based on type
        color_map = {
            'primary': self.colors.PRIMARY_BLUE,
            'success': self.colors.SUCCESS,
            'warning': self.colors.WARNING,
            'error': self.colors.ERROR,
            'info': self.colors.INFO,
        }
        card_color = color_map.get(self.color, self.colors.PRIMARY_BLUE)
        
        # Create card HTML with design system tokens
        icon_html = f'<span style="font-size: 1.2rem; margin-left: var(--space-2, 8px);">{self.icon}</span>' if self.icon else ''
        delta_html = f'<span style="color: var(--color-text-secondary, #64748b); font-size: var(--text-sm, 0.875rem); font-weight: var(--font-medium, 500);">{self.delta}</span>' if self.delta else ''
        help_html = f'<p style="color: var(--color-text-secondary, #64748b); font-size: var(--text-xs, 0.75rem); margin: var(--space-1, 4px) 0 0 0;">{self.help_text}</p>' if self.help_text else ''
        
        card_html = f"""
        <div class="metric-card" style="
            background-color: var(--color-surface, #f8fafc);
            border: 1px solid var(--color-border, #e2e8f0);
            border-radius: var(--radius-md, 8px);
            padding: var(--space-4, 16px);
            margin: var(--space-2, 8px) 0;
            box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.1));
            transition: all 0.2s ease;
        ">
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: var(--space-2, 8px);
            ">
                {icon_html}
                <h3 style="
                    color: var(--color-text-secondary, #64748b);
                    font-size: var(--text-sm, 0.875rem);
                    font-weight: var(--font-medium, 500);
                    margin: 0;
                    font-family: var(--font-primary, "Segoe UI", "Noto Sans Hebrew", "Arial Hebrew", sans-serif);
                ">{self.title}</h3>
            </div>
            <div style="
                display: flex;
                align-items: baseline;
                gap: var(--space-2, 8px);
            ">
                <h2 style="
                    color: {card_color};
                    font-size: var(--text-2xl, 1.5rem);
                    font-weight: var(--font-bold, 700);
                    margin: 0;
                    font-family: var(--font-primary, "Segoe UI", "Noto Sans Hebrew", "Arial Hebrew", sans-serif);
                ">{self.value}</h2>
                {delta_html}
            </div>
            {help_html}
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)

class InfoCard:
    """Information card component for displaying content"""
    
    def __init__(self, title: str, content: str, icon: Optional[str] = None,
                 variant: str = "default"):
        self.title = title
        self.content = content
        self.icon = icon
        self.variant = variant
        self.colors = ColorSystem()
    
    def render(self):
        """Render the info card"""
        # Get variant colors
        variant_colors = {
            'default': {
                'background': 'var(--color-surface)',
                'border': 'var(--color-border)',
                'title_color': 'var(--color-text-primary)',
                'content_color': 'var(--color-text-secondary)',
            },
            'success': {
                'background': 'rgba(5, 150, 105, 0.1)',
                'border': 'var(--color-success)',
                'title_color': 'var(--color-success)',
                'content_color': 'var(--color-text-primary)',
            },
            'warning': {
                'background': 'rgba(234, 88, 12, 0.1)',
                'border': 'var(--color-warning)',
                'title_color': 'var(--color-warning)',
                'content_color': 'var(--color-text-primary)',
            },
            'error': {
                'background': 'rgba(220, 38, 38, 0.1)',
                'border': 'var(--color-error)',
                'title_color': 'var(--color-error)',
                'content_color': 'var(--color-text-primary)',
            },
        }
        
        colors = variant_colors.get(self.variant, variant_colors['default'])
        
        icon_html = f'<span style="font-size: 1.2rem; margin-left: 8px;">{self.icon}</span>' if self.icon else ''
        
        card_html = f"""
        <div style="
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        ">
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 8px;
            ">
                {icon_html}
                <h3 style="
                    color: {colors['title_color']};
                    font-size: 1.125rem;
                    font-weight: 600;
                    margin: 0;
                ">{self.title}</h3>
            </div>
            <div style="
                color: {colors['content_color']};
                font-size: 1rem;
                line-height: 1.625;
            ">
                {self.content}
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)

def create_metric_cards(metrics: list, columns: int = 4):
    """Create a row of metric cards"""
    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        if i < len(cols):
            with cols[i]:
                card = MetricCard(
                    title=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta'),
                    help_text=metric.get('help'),
                    icon=metric.get('icon'),
                    color=metric.get('color', 'primary')
                )
                card.render()

def create_info_cards(cards: list, columns: int = 2):
    """Create a grid of info cards"""
    cols = st.columns(columns)
    for i, card_data in enumerate(cards):
        if i < len(cols):
            with cols[i]:
                card = InfoCard(
                    title=card_data.get('title', ''),
                    content=card_data.get('content', ''),
                    icon=card_data.get('icon'),
                    variant=card_data.get('variant', 'default')
                )
                card.render()
