import logging
import uuid

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_comparison_chart(expenses_df: pd.DataFrame, donations_df: pd.DataFrame) -> None:
    """Create a comparison chart between expenses and donations"""
    try:
        if not isinstance(expenses_df, pd.DataFrame) or not isinstance(donations_df, pd.DataFrame):
            st.error("הנתונים חייבים להיות DataFrame")
            return

        if 'תאריך' not in expenses_df.columns or 'שקלים' not in expenses_df.columns or 'תאריך' not in donations_df.columns or 'שקלים' not in donations_df.columns:
            st.error("חסרות עמודות נדרשות")
            return

        # Calculate monthly totals - ensure dates are properly converted
        try:
            expenses_df_copy = expenses_df.copy()
            expenses_df_copy['תאריך'] = pd.to_datetime(expenses_df_copy['תאריך'], errors='coerce')
            valid_expenses = expenses_df_copy.dropna(subset=['תאריך'])

            donations_df_copy = donations_df.copy()
            donations_df_copy['תאריך'] = pd.to_datetime(donations_df_copy['תאריך'], errors='coerce')
            valid_donations = donations_df_copy.dropna(subset=['תאריך'])

            if valid_expenses.empty or valid_donations.empty:
                st.warning("אין נתונים תאריכים תקינים להצגה")
                return

            monthly_expenses = valid_expenses.groupby(valid_expenses['תאריך'].dt.strftime('%Y-%m'))['שקלים'].sum().reset_index()
            monthly_donations = valid_donations.groupby(valid_donations['תאריך'].dt.strftime('%Y-%m'))['שקלים'].sum().reset_index()
        except Exception as e:
            st.error(f"שגיאה בעיבוד תאריכים: {str(e)}")
            return

        # Create the chart
        fig = go.Figure()

        # Add expenses bars
        fig.add_trace(go.Bar(
            x=monthly_expenses['תאריך'],
            y=monthly_expenses['שקלים'],
            name='הוצאות',
            marker_color='red',
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add donations bars
        fig.add_trace(go.Bar(
            x=monthly_donations['תאריך'],
            y=monthly_donations['שקלים'],
            name='תרומות',
            marker_color='green',
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title='השוואת הוצאות ותרומות חודשיות',
            xaxis_title='חודש',
            yaxis_title='סכום (₪)',
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig, use_container_width=True, key=f'comparison_chart_{uuid.uuid4().hex[:8]}')

    except Exception as e:
        st.error(f"שגיאה ביצירת גרף השוואה: {str(e)}")
        logging.error(f"Error creating comparison chart: {str(e)}")

def create_monthly_trends(expenses_df: pd.DataFrame, donations_df: pd.DataFrame):
    """Create monthly trends chart"""
    try:
        if not isinstance(expenses_df, pd.DataFrame) or not isinstance(donations_df, pd.DataFrame):
            logging.error("Data must be DataFrames")
            return None

        # Check for required columns with flexible mapping
        expenses_amount_col = 'סכום' if 'סכום' in expenses_df.columns else 'שקלים'
        donations_amount_col = 'סכום' if 'סכום' in donations_df.columns else 'שקלים'

        if 'תאריך' not in expenses_df.columns or expenses_amount_col not in expenses_df.columns or 'תאריך' not in donations_df.columns or donations_amount_col not in donations_df.columns:
            logging.error("Missing required columns")
            return None

        # Calculate monthly totals - ensure dates are properly converted
        try:
            expenses_df_copy = expenses_df.copy()
            expenses_df_copy['תאריך'] = pd.to_datetime(expenses_df_copy['תאריך'], errors='coerce')
            valid_expenses = expenses_df_copy.dropna(subset=['תאריך'])

            donations_df_copy = donations_df.copy()
            donations_df_copy['תאריך'] = pd.to_datetime(donations_df_copy['תאריך'], errors='coerce')
            valid_donations = donations_df_copy.dropna(subset=['תאריך'])

            if valid_expenses.empty or valid_donations.empty:
                logging.warning("No valid date data to display")
                return None

            monthly_expenses = valid_expenses.groupby(valid_expenses['תאריך'].dt.strftime('%Y-%m'))[expenses_amount_col].sum().reset_index()
            monthly_donations = valid_donations.groupby(valid_donations['תאריך'].dt.strftime('%Y-%m'))[donations_amount_col].sum().reset_index()
        except Exception as e:
            logging.error(f"Error processing dates: {str(e)}")
            return None

        # Create the chart
        fig = go.Figure()

        # Add expenses line
        fig.add_trace(go.Scatter(
            x=monthly_expenses['תאריך'],
            y=monthly_expenses[expenses_amount_col],
            name='הוצאות',
            line=dict(color='red', width=2),
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add donations line
        fig.add_trace(go.Scatter(
            x=monthly_donations['תאריך'],
            y=monthly_donations[donations_amount_col],
            name='תרומות',
            line=dict(color='green', width=2),
            hovertemplate='חודש: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title='מגמות חודשיות בהוצאות ותרומות',
            xaxis_title='חודש',
            yaxis_title='סכום (₪)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating monthly trends chart: {str(e)}")
        return None

def create_budget_distribution_chart(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame) or df.empty:
        logging.error("Invalid or missing data - DataFrame is empty or invalid")
        return None

    # Map column names to expected names - prioritize mapped names
    name_col = None
    amount_col = None

    # Check for mapped column names first (from google_sheets_io mapping)
    if 'שם' in df.columns:
        name_col = 'שם'
    elif 'שם לקוח' in df.columns:
        name_col = 'שם לקוח'
    elif 'שם התורם' in df.columns:
        name_col = 'שם התורם'

    if 'שקלים' in df.columns:
        amount_col = 'שקלים'
    elif 'סכום' in df.columns:
        amount_col = 'סכום'

    if not name_col or not amount_col:
        logging.error(f"Invalid or missing data - required columns not found. Available: {list(df.columns)}")
        return None

    try:
        # Group by name and calculate totals
        budget_data = df.groupby(name_col)[amount_col].sum().reset_index()

        # Sort by amount
        budget_data = budget_data.sort_values(amount_col, ascending=False)

        # Create figure
        fig = px.pie(
            budget_data,
            values=amount_col,
            names=name_col,
            title='התפלגות תקציב',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
            width=800,  # Fixed width for better control
            height=600   # Fixed height for better control
        )

        # Update layout
        fig.update_layout(
            title={
                'text': 'התפלגות תקציב',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            showlegend=True,
            legend=dict(
                orientation="v",  # Changed to vertical to prevent overlapping
                yanchor="top",
                y=1.0,
                xanchor="left",
                x=1.05,  # Position legend to the right of the chart
                bgcolor='rgba(255,255,255,0.8)',  # Semi-transparent background
                bordercolor='rgba(0,0,0,0.1)',  # Light border
                borderwidth=1,
                font=dict(size=10),  # Smaller font to fit better
                itemsizing='constant'  # Consistent item sizes
            ),
            margin=dict(l=50, r=150, t=80, b=50)  # Increased right margin for legend
        )

        # Update traces
        fig.update_traces(
            textposition='outside',  # Changed to outside to prevent overlapping
            textinfo='percent+label',
            textfont=dict(size=10),  # Smaller text to fit better
            hovertemplate='קטגוריה: %{label}<br>סכום: ₪%{value:,.0f}<br>אחוז: %{percent:.1%}<extra></extra>'
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating budget distribution chart: {str(e)}")
        logging.error(f"Error type: {type(e).__name__}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        return None

def create_widows_support_chart(df: pd.DataFrame):
    # Check for both possible column names
    name_col = 'שם ' if 'שם ' in df.columns else 'שם'

    if not isinstance(df, pd.DataFrame) or name_col not in df.columns or 'סכום חודשי' not in df.columns or df.empty:
        logging.error(f"Invalid or missing data - name_col: {name_col}, available columns: {list(df.columns)}")
        return None
    try:
        # Group by name and calculate totals
        support_data = df.groupby(name_col)['סכום חודשי'].sum().reset_index()

        # Sort by amount
        support_data = support_data.sort_values('סכום חודשי', ascending=False)

        # Create figure
        fig = px.bar(
            support_data,
            x=name_col,
            y='סכום חודשי',
            title='תמיכה באלמנות',
            color='סכום חודשי',
            color_continuous_scale='Viridis'
        )

        # Update layout
        fig.update_layout(
            title={
                'text': 'תמיכה באלמנות',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='שם',
            yaxis_title='סכום חודשי (₪)',
            showlegend=False,
            template='plotly_white',
            margin=dict(l=50, r=50, t=80, b=50)
        )

        # Update traces
        fig.update_traces(
            hovertemplate='שם: %{x}<br>סכום חודשי: ₪%{y:,.0f}<extra></extra>'
        )

        # Format y-axis ticks
        fig.update_yaxes(tickformat=",.0f")

        return fig

    except Exception as e:
        logging.error(f"Error creating widows support chart: {str(e)}")
        return None

def create_donor_contribution_chart(donations_df: pd.DataFrame):
    """Create a chart showing donor contributions"""
    try:
        if not isinstance(donations_df, pd.DataFrame):
            logging.error("Data must be DataFrame")
            return None

        # Map column names to expected names - prioritize mapped names
        name_col = None
        amount_col = None

        # Check for mapped column names first (from google_sheets_io mapping)
        if 'שם' in donations_df.columns:
            name_col = 'שם'
        elif 'שם התורם' in donations_df.columns:
            name_col = 'שם התורם'

        if 'שקלים' in donations_df.columns:
            amount_col = 'שקלים'
        elif 'סכום' in donations_df.columns:
            amount_col = 'סכום'

        if not name_col or not amount_col:
            logging.error("Missing required columns")
            return None

        # Calculate total donations by donor
        donor_totals = donations_df.groupby(name_col)[amount_col].sum().sort_values(ascending=False)

        # Create the chart
        fig = go.Figure()

        # Add bars
        fig.add_trace(go.Bar(
            x=donor_totals.index,
            y=donor_totals.values,
            marker_color='green',
            hovertemplate='תורם: %{x}<br>סכום: %{y:,.0f} ₪<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title='סכום תרומות לפי תורם',
            xaxis_title='תורם',
            yaxis_title='סכום (₪)',
            hovermode='x unified',
            showlegend=False
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating donor contribution chart: {str(e)}")
        return None

def create_forecast_chart(forecast: dict) -> None:
    """Create a forecast chart"""
    try:
        if not isinstance(forecast, dict) or 'monthly_forecast' not in forecast:
            st.error("נתוני תחזית לא תקינים")
            return

        monthly_data = forecast['monthly_forecast']
        if not monthly_data:
            st.warning("אין נתוני תחזית להצגה")
            return

        # Create DataFrame
        df = pd.DataFrame(monthly_data)

        # Create the chart
        fig = go.Figure()

        # Add expenses line
        fig.add_trace(go.Scatter(
            x=df['חודש'],
            y=df['הוצאות'],
            name='הוצאות צפויות',
            line=dict(color='red', width=2, dash='dash'),
            hovertemplate='חודש: %{x}<br>הוצאות: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add donations line
        fig.add_trace(go.Scatter(
            x=df['חודש'],
            y=df['תרומות'],
            name='תרומות צפויות',
            line=dict(color='green', width=2, dash='dash'),
            hovertemplate='חודש: %{x}<br>תרומות: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add balance line
        fig.add_trace(go.Scatter(
            x=df['חודש'],
            y=df['יתרה'],
            name='יתרה צפויה',
            line=dict(color='blue', width=2),
            hovertemplate='חודש: %{x}<br>יתרה: %{y:,.0f} ₪<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title='תחזית תקציב',
            xaxis_title='חודש',
            yaxis_title='סכום (₪)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig, use_container_width=True, key=f'forecast_chart_{uuid.uuid4().hex[:8]}')

    except Exception as e:
        st.error(f"שגיאה ביצירת גרף תחזית: {str(e)}")
        logging.error(f"Error creating forecast chart: {str(e)}")

def create_monthly_budget_chart(budget_status: dict) -> None:
    """Create a monthly budget chart"""
    try:
        if not isinstance(budget_status, dict) or 'monthly_budget' not in budget_status:
            st.error("נתוני תקציב לא תקינים")
            return

        monthly_data = budget_status['monthly_budget']
        if not monthly_data:
            st.warning("אין נתוני תקציב חודשי להצגה")
            return

        # Create DataFrame
        df = pd.DataFrame(monthly_data)

        # Create the chart
        fig = go.Figure()

        # Add expenses bars
        fig.add_trace(go.Bar(
            x=df['חודש'],
            y=df['הוצאות'],
            name='הוצאות',
            marker_color='red',
            hovertemplate='חודש: %{x}<br>הוצאות: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add donations bars
        fig.add_trace(go.Bar(
            x=df['חודש'],
            y=df['תרומות'],
            name='תרומות',
            marker_color='green',
            hovertemplate='חודש: %{x}<br>תרומות: %{y:,.0f} ₪<extra></extra>'
        ))

        # Add balance line
        fig.add_trace(go.Scatter(
            x=df['חודש'],
            y=df['יתרה'],
            name='יתרה',
            line=dict(color='blue', width=3),
            yaxis='y2',
            hovertemplate='חודש: %{x}<br>יתרה: %{y:,.0f} ₪<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title='תקציב חודשי',
            xaxis_title='חודש',
            yaxis_title='סכום (₪)',
            yaxis2=dict(
                title='יתרה (₪)',
                overlaying='y',
                side='right'
            ),
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig, use_container_width=True, key=f'monthly_budget_{uuid.uuid4().hex[:8]}')

    except Exception as e:
        st.error(f"שגיאה ביצירת גרף תקציב חודשי: {str(e)}")
        logging.error(f"Error creating monthly budget chart: {str(e)}")
