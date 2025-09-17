"""
Layout Components for Omri Association Dashboard
Reusable layout components with consistent styling
"""

from typing import Dict, List, Optional

import streamlit as st

from ..design_system.colors import ColorSystem
from ..design_system.spacing import SpacingSystem
from ..design_system.typography import TypographySystem


class SectionHeader:
    """Modern section header component"""

    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        icon: Optional[str] = None,
        actions: Optional[List] = None,
    ):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.actions = actions or []
        self.colors = ColorSystem()
        self.typography = TypographySystem()
        self.spacing = SpacingSystem()

    def render(self):
        """Render the section header"""
        icon_html = f'<span style="font-size: 1.5rem;">{self.icon}</span>' if self.icon else ""
        actions_html = "".join(
            [f'<div style="margin-left: var(--space-2);">{action}</div>' for action in self.actions]
        )
        subtitle_html = (
            f'<p style="color: var(--color-text-secondary); font-size: var(--text-base); margin: 0;">{self.subtitle}</p>'
            if self.subtitle
            else ""
        )

        header_html = f"""
        <div style="
            margin-bottom: var(--space-6);
            padding-bottom: var(--space-4);
            border-bottom: 2px solid var(--color-border);
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: var(--space-2);
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: var(--space-3);
                ">
                    {icon_html}
                    <h2 style="
                        color: var(--color-text-primary);
                        font-size: var(--text-3xl);
                        font-weight: var(--font-bold);
                        margin: 0;
                    ">{self.title}</h2>
                </div>
                <div style="
                    display: flex;
                    gap: var(--space-2);
                ">
                    {actions_html}
                </div>
            </div>
            {subtitle_html}
        </div>
        """

        st.markdown(header_html, unsafe_allow_html=True)


class Container:
    """Container component for consistent spacing and layout"""

    def __init__(self, max_width: str = "1200px", padding: str = "var(--space-4)"):
        self.max_width = max_width
        self.padding = padding
        self.colors = ColorSystem()

    def render(self, content_func):
        """Render container with content"""
        container_html = f"""
        <div style="
            max-width: {self.max_width};
            margin: 0 auto;
            padding: {self.padding};
        ">
        """

        st.markdown(container_html, unsafe_allow_html=True)
        content_func()
        st.markdown("</div>", unsafe_allow_html=True)


class Grid:
    """Grid system for responsive layouts"""

    def __init__(self, columns: int = 12, gap: str = "var(--space-4)"):
        self.columns = columns
        self.gap = gap
        self.spacing = SpacingSystem()

    def create_columns(self, sizes: List[int]) -> List:
        """Create columns with specified sizes"""
        if sum(sizes) != self.columns:
            # Normalize sizes to fit grid
            total = sum(sizes)
            sizes = [int((size / total) * self.columns) for size in sizes]

        return st.columns(sizes)

    def create_responsive_columns(self, breakpoints: Dict[str, List[int]]) -> List:
        """Create responsive columns based on breakpoints"""
        # For now, use the default breakpoint
        default_sizes = breakpoints.get("default", [6, 6])
        return self.create_columns(default_sizes)


def create_section_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    actions: Optional[List] = None,
):
    """Create a section header"""
    header = SectionHeader(title, subtitle, icon, actions)
    header.render()


def create_container(max_width: str = "1200px", padding: str = "var(--space-4)"):
    """Create a container wrapper"""
    return Container(max_width, padding)


def create_grid(columns: int = 12, gap: str = "var(--space-4)"):
    """Create a grid system"""
    return Grid(columns, gap)


def add_spacing(rem: float = 2):
    """Add consistent spacing between sections"""
    st.markdown(f"<div style='margin: {rem}rem 0;'></div>", unsafe_allow_html=True)


def create_metric_row(metrics: list, columns: int = 4):
    """Create a row of metrics with proper spacing"""
    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        if i < len(cols):
            with cols[i]:
                st.metric(
                    metric.get("label", ""),
                    metric.get("value", ""),
                    metric.get("delta"),
                    help=metric.get("help"),
                )


def create_two_column_layout():
    """Create a two-column layout"""
    return st.columns(2)


def create_three_column_layout():
    """Create a three-column layout"""
    return st.columns(3)


def create_four_column_layout():
    """Create a four-column layout"""
    return st.columns(4)
