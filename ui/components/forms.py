#!/usr/bin/env python3
"""
Form Components for Dashboard
Accessible form elements with consistent styling
"""

import streamlit as st

from ui.design_tokens import DesignSystem


def create_accessible_checkbox(label: str, value: bool = False, help_text: str = "", key: str = None, disabled: bool = False):
    """Create accessible checkbox with proper ARIA attributes"""
    return st.checkbox(
        label=label,
        value=value,
        help=help_text,
        key=key,
        disabled=disabled,
        # Add accessibility attributes
        kwargs={
            'aria-label': f"{label}. {help_text}" if help_text else label,
            'role': 'checkbox',
            'aria-checked': str(value).lower(),
            'aria-disabled': str(disabled).lower()
        }
    )

def create_accessible_selectbox(label: str, options: list, index: int = 0, help_text: str = "", key: str = None, disabled: bool = False):
    """Create accessible selectbox with proper ARIA attributes"""
    return st.selectbox(
        label=label,
        options=options,
        index=index,
        help=help_text,
        key=key,
        disabled=disabled,
        kwargs={
            'aria-label': f"{label}. {help_text}" if help_text else label,
            'role': 'combobox',
            'aria-expanded': 'false',
            'aria-disabled': str(disabled).lower()
        }
    )

def create_accessible_slider(label: str, min_value: float, max_value: float, value: float = None, help_text: str = "", key: str = None, disabled: bool = False):
    """Create accessible slider with proper ARIA attributes"""
    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        help=help_text,
        key=key,
        disabled=disabled,
        kwargs={
            'aria-label': f"{label}. {help_text}" if help_text else label,
            'role': 'slider',
            'aria-valuemin': str(min_value),
            'aria-valuemax': str(max_value),
            'aria-valuenow': str(value) if value else str((min_value + max_value) / 2),
            'aria-disabled': str(disabled).lower()
        }
    )

def create_filter_group(title: str, filters: list, columns: int = 3):
    """Create a group of filters with consistent styling"""

    # Create section header
    st.markdown(f"""
    <div style="
        background: {DesignSystem.COLORS['surface']};
        border: 1px solid {DesignSystem.COLORS['border']};
        border-radius: {DesignSystem.BORDER_RADIUS['md']};
        padding: {DesignSystem.SPACING['lg']};
        margin-bottom: {DesignSystem.SPACING['lg']};
        box-shadow: {DesignSystem.SHADOWS['sm']};
    ">
        <h4 style="
            color: {DesignSystem.COLORS['primary']};
            font-size: {DesignSystem.TYPOGRAPHY['h4']['size']};
            font-weight: {DesignSystem.TYPOGRAPHY['h4']['weight']};
            margin: 0 0 {DesignSystem.SPACING['md']} 0;
            display: flex;
            align-items: center;
            gap: {DesignSystem.SPACING['sm']};
        ">
            🔍 {title}
        </h4>
    """, unsafe_allow_html=True)

    # Create filter columns
    cols = st.columns(columns)

    for i, filter_config in enumerate(filters):
        with cols[i % columns]:
            filter_type = filter_config.get('type', 'checkbox')

            if filter_type == 'checkbox':
                create_accessible_checkbox(
                    label=filter_config.get('label', ''),
                    value=filter_config.get('value', False),
                    help_text=filter_config.get('help', ''),
                    key=filter_config.get('key', f"filter_{i}"),
                    disabled=filter_config.get('disabled', False)
                )
            elif filter_type == 'selectbox':
                create_accessible_selectbox(
                    label=filter_config.get('label', ''),
                    options=filter_config.get('options', []),
                    index=filter_config.get('index', 0),
                    help_text=filter_config.get('help', ''),
                    key=filter_config.get('key', f"filter_{i}"),
                    disabled=filter_config.get('disabled', False)
                )
            elif filter_type == 'slider':
                create_accessible_slider(
                    label=filter_config.get('label', ''),
                    min_value=filter_config.get('min_value', 0),
                    max_value=filter_config.get('max_value', 100),
                    value=filter_config.get('value', None),
                    help_text=filter_config.get('help', ''),
                    key=filter_config.get('key', f"filter_{i}"),
                    disabled=filter_config.get('disabled', False)
                )

    st.markdown("</div>", unsafe_allow_html=True)

def create_search_input(label: str = "חיפוש", placeholder: str = "הקלד לחיפוש...", key: str = None):
    """Create accessible search input with proper styling"""

    # Add search icon and styling
    search_html = f"""
    <style>
    .search-input {{
        position: relative;
    }}

    .search-input::before {{
        content: "🔍";
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        color: {DesignSystem.COLORS['text_secondary']};
        z-index: 1;
    }}

    .search-input input {{
        padding-left: 40px !important;
        border-radius: {DesignSystem.BORDER_RADIUS['md']} !important;
        border: 1px solid {DesignSystem.COLORS['border']} !important;
        font-size: {DesignSystem.TYPOGRAPHY['body']['size']} !important;
    }}

    .search-input input:focus {{
        border-color: {DesignSystem.COLORS['primary']} !important;
        box-shadow: 0 0 0 2px {DesignSystem.COLORS['primary']}20 !important;
    }}
    </style>
    """

    st.markdown(search_html, unsafe_allow_html=True)

    return st.text_input(
        label=label,
        placeholder=placeholder,
        key=key,
        kwargs={
            'aria-label': f"{label}. {placeholder}",
            'role': 'searchbox',
            'autocomplete': 'off'
        }
    )

def create_date_range_picker(label: str = "טווח תאריכים", key: str = None):
    """Create accessible date range picker"""

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "תאריך התחלה",
            key=f"{key}_start" if key else None,
            kwargs={
                'aria-label': 'תאריך התחלה',
                'role': 'textbox'
            }
        )

    with col2:
        end_date = st.date_input(
            "תאריך סיום",
            key=f"{key}_end" if key else None,
            kwargs={
                'aria-label': 'תאריך סיום',
                'role': 'textbox'
            }
        )

    return start_date, end_date

def create_action_buttons(buttons: list, columns: int = None):
    """Create a row of action buttons with consistent styling"""

    if columns is None:
        columns = len(buttons)

    cols = st.columns(columns)

    for i, button_config in enumerate(buttons):
        with cols[i]:
            button_type = button_config.get('type', 'primary')
            DesignSystem.COLORS.get(button_type, DesignSystem.COLORS['primary'])

            if st.button(
                button_config.get('label', ''),
                key=button_config.get('key', f"button_{i}"),
                disabled=button_config.get('disabled', False),
                help=button_config.get('help', ''),
                use_container_width=True
            ):
                # Execute button action if provided
                action = button_config.get('action')
                if action and callable(action):
                    action()
                elif action:
                    st.write(f"Button clicked: {action}")
