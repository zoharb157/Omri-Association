import logging

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_monthly_trends(expenses_df: pd.DataFrame, donations_df: pd.DataFrame):
    """Create monthly trends chart for expenses and donations"""
    try:
        if not isinstance(expenses_df, pd.DataFrame) or not isinstance(donations_df, pd.DataFrame):
            st.error("הנתונים חייבים להיות DataFrame")
            return None

        if "תאריך" not in expenses_df.columns or "שקלים" not in expenses_df.columns:
            st.error("עמודות 'תאריך' ו'שקלים' חסרות בנתוני ההוצאות")
            return None

        if "תאריך" not in donations_df.columns or "שקלים" not in donations_df.columns:
            st.error("עמודות 'תאריך' ו'שקלים' חסרות בנתוני התרומות")
            return None

        # Process expenses data
        expenses_df["תאריך"] = pd.to_datetime(expenses_df["תאריך"], errors="coerce")
        expenses_df = expenses_df.dropna(subset=["תאריך"])
        expenses_df["חודש"] = expenses_df["תאריך"].dt.to_period("M")
        monthly_expenses = expenses_df.groupby("חודש")["שקלים"].sum().reset_index()
        monthly_expenses["חודש"] = monthly_expenses["חודש"].astype(str)

        # Process donations data
        donations_df["תאריך"] = pd.to_datetime(donations_df["תאריך"], errors="coerce")
        donations_df = donations_df.dropna(subset=["תאריך"])
        donations_df["חודש"] = donations_df["תאריך"].dt.to_period("M")
        monthly_donations = donations_df.groupby("חודש")["שקלים"].sum().reset_index()
        monthly_donations["חודש"] = monthly_donations["חודש"].astype(str)

        # Create the chart
        fig = go.Figure()

        # Add expenses line
        fig.add_trace(
            go.Scatter(
                x=monthly_expenses["חודש"],
                y=monthly_expenses["שקלים"],
                mode="lines+markers",
                name="הוצאות",
                line=dict(color="#e74c3c", width=3),
                marker=dict(size=8),
            )
        )

        # Add donations line
        fig.add_trace(
            go.Scatter(
                x=monthly_donations["חודש"],
                y=monthly_donations["שקלים"],
                mode="lines+markers",
                name="תרומות",
                line=dict(color="#27ae60", width=3),
                marker=dict(size=8),
            )
        )

        # Update layout
        fig.update_layout(
            title="מגמות חודשיות - הוצאות ותרומות",
            xaxis_title="חודש",
            yaxis_title="שקלים",
            hovermode="x unified",
            template="plotly_white",
            font=dict(family="Arial", size=12),
            height=400,
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating monthly trends chart: {e}")
        st.error(f"שגיאה ביצירת תרשים המגמות: {e}")
        return None


def create_budget_distribution_chart(df: pd.DataFrame):
    """Create budget distribution pie chart"""
    try:
        if not isinstance(df, pd.DataFrame) or df.empty:
            logging.warning("Empty or invalid DataFrame provided to budget distribution chart")
            return None

        # Check if we have the required amount column
        amount_col = None
        for col in ("שקלים", "סכום"):
            if col in df.columns:
                amount_col = col
                break

        if not amount_col:
            logging.warning("No amount column found in DataFrame")
            return None

        # If we have a category column, use it
        if "קטגוריה" in df.columns:
            # Group by category and sum amounts
            category_totals = df.groupby("קטגוריה")[amount_col].sum().reset_index()
            names_col = "קטגוריה"
            title = "התפלגות הוצאות לפי קטגוריה"
        else:
            # Fallback: group by name (supplier/client) if no category column
            name_col = None
            for col in ("שם", "שם לקוח", "שם ספק"):
                if col in df.columns:
                    name_col = col
                    break

            if not name_col:
                logging.warning("No name or category column found for grouping")
                return None

            # Group by name and sum amounts
            category_totals = df.groupby(name_col)[amount_col].sum().reset_index()
            names_col = name_col
            title = "התפלגות הוצאות לפי ספק/לקוח"

        # Filter out empty or zero amounts
        category_totals = category_totals[category_totals[amount_col] > 0]

        if category_totals.empty:
            logging.warning("No valid data for budget distribution chart")
            return None

        # Create pie chart
        fig = px.pie(
            category_totals,
            values=amount_col,
            names=names_col,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>סכום: ₪%{value:,.0f}<br>אחוז: %{percent}<extra></extra>",
        )

        fig.update_layout(
            font=dict(family="Arial", size=12),
            height=400,
            showlegend=True,
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating budget distribution chart: {e}")
        return None


def create_widows_support_chart(df: pd.DataFrame):
    """Create widows support chart"""
    try:
        if not isinstance(df, pd.DataFrame):
            st.error("הנתונים חייבים להיות DataFrame")
            return None

        if "סכום חודשי" not in df.columns:
            st.error("עמודת 'סכום חודשי' חסרה")
            return None

        # Create histogram
        fig = px.histogram(
            df,
            x="סכום חודשי",
            title="התפלגות סכומי תמיכה חודשיים",
            nbins=20,
            color_discrete_sequence=["#3498db"],
        )

        fig.update_layout(
            xaxis_title="סכום חודשי (שקלים)",
            yaxis_title="מספר אלמנות",
            font=dict(family="Arial", size=12),
            height=400,
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating widows support chart: {e}")
        st.error(f"שגיאה ביצירת תרשים תמיכה באלמנות: {e}")
        return None


def create_donor_contribution_chart(donations_df: pd.DataFrame):
    """Create donor contribution chart"""
    try:
        if not isinstance(donations_df, pd.DataFrame):
            st.error("הנתונים חייבים להיות DataFrame")
            return None

        if "שם" not in donations_df.columns or "שקלים" not in donations_df.columns:
            st.error("עמודות 'שם' ו'שקלים' חסרות")
            return None

        # Group by donor and sum amounts
        donor_totals = donations_df.groupby("שם")["שקלים"].sum().reset_index()
        donor_totals = donor_totals.sort_values("שקלים", ascending=False).head(10)

        # Create bar chart
        fig = px.bar(
            donor_totals,
            x="שקלים",
            y="שם",
            orientation="h",
            title="10 התורמים הגדולים",
            color="שקלים",
            color_continuous_scale="Blues",
        )

        fig.update_layout(
            xaxis_title="סכום תרומה (שקלים)",
            yaxis_title="תורם",
            font=dict(family="Arial", size=12),
            height=400,
        )

        return fig

    except Exception as e:
        logging.error(f"Error creating donor contribution chart: {e}")
        st.error(f"שגיאה ביצירת תרשים תרומות: {e}")
        return None
