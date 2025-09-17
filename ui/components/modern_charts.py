#!/usr/bin/env python3
"""
Modern Chart Components for Omri Association Dashboard
High-quality chart components with modern styling
"""

import pandas as pd
import plotly.graph_objects as go

from ui.design_system.modern_tokens import ModernDesignSystem


def _get_amount_column(df: pd.DataFrame) -> str:
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ('שקלים', 'סכום'):
        if col in df.columns:
            return col
    return None


def _get_name_column(df: pd.DataFrame) -> str:
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ('שם', 'שם התורם', 'שם לקוח'):
        if col in df.columns:
            return col
    return None

def create_modern_donations_chart(donations_df):
    """Create a modern donations chart with proper styling"""

    if donations_df.empty:
        return None

    # Prepare data
    try:
        # Handle date column - first column is usually the date
        if len(donations_df.columns) > 0:
            date_col = donations_df.columns[0]  # First column is the date
            donations_df['תאריך'] = pd.to_datetime(donations_df[date_col], errors='coerce', format='%d/%m/%Y')

        amount_col = _get_amount_column(donations_df)
        if not amount_col:
            return None

        # Group by month
        monthly_data = donations_df.groupby(donations_df['תאריך'].dt.to_period('M'))[amount_col].sum()

        if monthly_data.empty:
            return None

        # Create chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=monthly_data.index.astype(str),
            y=monthly_data.values,
            marker_color=ModernDesignSystem.COLORS['primary'],
            marker_line_color=ModernDesignSystem.COLORS['primary_700'],
            marker_line_width=1,
            hovertemplate='<b>%{x}</b><br>סכום: ₪%{y:,.0f}<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': 'תרומות חודשיות',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
            },
            xaxis={
                'title': 'חודש',
                'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']},
                'tickfont': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
            },
            yaxis={
                'title': 'סכום (₪)',
                'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']},
                'tickformat': '₪,.0f'
            },
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family=ModernDesignSystem.TYPOGRAPHY['font_hebrew'],
            margin={'l': 60, 'r': 60, 't': 80, 'b': 60},
            height=400
        )

        return fig

    except Exception as e:
        print(f"Error creating donations chart: {e}")
        return None

def create_modern_expenses_pie_chart(expenses_df):
    """Create a modern pie chart for expenses"""

    if expenses_df.empty:
        return None

    try:
        # Prepare data
        amount_col = _get_amount_column(expenses_df)
        if not amount_col:
            return None

        # Use the second column as category (בגין מה בוצע התשלום?)
        category_col = 'בגין מה בוצע התשלום?' if 'בגין מה בוצע התשלום?' in expenses_df.columns else expenses_df.columns[1] if len(expenses_df.columns) > 1 else 'קטגוריה'
        category_data = expenses_df.groupby(category_col)[amount_col].sum()

        if category_data.empty:
            return None

        # Define modern color palette
        colors = [
            ModernDesignSystem.COLORS['primary'],
            ModernDesignSystem.COLORS['success'],
            ModernDesignSystem.COLORS['warning'],
            ModernDesignSystem.COLORS['error'],
            ModernDesignSystem.COLORS['info']
        ]

        fig = go.Figure(data=[go.Pie(
            labels=category_data.index,
            values=category_data.values,
            marker_colors=colors,
            textinfo='label+percent',
            textfont={'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']},
            hovertemplate='<b>%{label}</b><br>סכום: ₪%{value:,.0f}<br>אחוז: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title={
                'text': 'חלוקת הוצאות לפי קטגוריות',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
            },
            font_family=ModernDesignSystem.TYPOGRAPHY['font_hebrew'],
            height=400,
            margin={'l': 60, 'r': 60, 't': 80, 'b': 60}
        )

        return fig

    except Exception as e:
        print(f"Error creating expenses pie chart: {e}")
        return None

def create_modern_donors_chart(donors_df):
    """Create a modern chart for donor statistics"""

    if donors_df.empty:
        return None

    try:
        name_col = _get_name_column(donors_df)
        amount_col = _get_amount_column(donors_df)

        if name_col and amount_col:
            top_donors = donors_df.groupby(name_col)[amount_col].sum().nlargest(10)

            if top_donors.empty:
                return None

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=top_donors.values,
                y=top_donors.index,
                orientation='h',
                marker_color=ModernDesignSystem.COLORS['success'],
                marker_line_color=ModernDesignSystem.COLORS['success'],
                marker_line_width=1,
                hovertemplate='<b>%{y}</b><br>סכום: ₪%{x:,.0f}<extra></extra>'
            ))

            fig.update_layout(
                title={
                    'text': 'עשרת התורמים המובילים',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
                },
                xaxis={
                    'title': 'סכום (₪)',
                    'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']},
                    'tickformat': '₪,.0f'
                },
                yaxis={
                    'title': 'תורם',
                    'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']},
                    'tickfont': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
                },
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family=ModernDesignSystem.TYPOGRAPHY['font_hebrew'],
                margin={'l': 100, 'r': 60, 't': 80, 'b': 60},
                height=400
            )

            return fig

    except Exception as e:
        print(f"Error creating donors chart: {e}")
        return None

def create_modern_widows_chart(widows_df):
    """Create a modern chart for widow statistics"""

    if widows_df.empty:
        return None

    try:
        # Prepare data - children distribution
        if 'מספר ילדים' in widows_df.columns:
            children_dist = widows_df['מספר ילדים'].value_counts().sort_index()

            if children_dist.empty:
                return None

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=children_dist.index,
                y=children_dist.values,
                marker_color=ModernDesignSystem.COLORS['warning'],
                marker_line_color=ModernDesignSystem.COLORS['warning'],
                marker_line_width=1,
                hovertemplate='<b>%{x} ילדים</b><br>מספר אלמנות: %{y}<extra></extra>'
            ))

            fig.update_layout(
                title={
                    'text': 'התפלגות אלמנות לפי מספר ילדים',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
                },
                xaxis={
                    'title': 'מספר ילדים',
                    'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
                },
                yaxis={
                    'title': 'מספר אלמנות',
                    'title_font': {'family': ModernDesignSystem.TYPOGRAPHY['font_hebrew']}
                },
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family=ModernDesignSystem.TYPOGRAPHY['font_hebrew'],
                margin={'l': 60, 'r': 60, 't': 80, 'b': 60},
                height=400
            )

            return fig

    except Exception as e:
        print(f"Error creating widows chart: {e}")
        return None

def create_chart_card(title: str, chart_fig, height: int = 400):
    """Create a card wrapper for charts"""

    if chart_fig is None:
        # Show empty state
        empty_html = f"""
        <div class="chart-card">
            <h3 class="chart-card-title">{title}</h3>
            <div class="chart-empty-state">
                <p>אין נתונים להצגה</p>
            </div>
        </div>
        """
        return empty_html

    # Create chart card HTML
    chart_html = f"""
    <div class="chart-card">
        <h3 class="chart-card-title">{title}</h3>
        <div class="chart-container">
            <!-- Chart will be rendered here -->
        </div>
    </div>
    """

    return chart_html

