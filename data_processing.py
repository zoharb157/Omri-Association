import logging
import traceback
from typing import Dict, List, Optional, Union

import pandas as pd
import streamlit as st

# Config import moved to avoid circular imports


def _get_amount_column(df: pd.DataFrame) -> Optional[str]:
    """Return the standard amount column name used across sheets."""
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ("שקלים", "סכום"):
        if col in df.columns:
            return col
    return None


def _get_name_column(df: pd.DataFrame) -> Optional[str]:
    """Return the standard name column for donor/expense tables."""
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ("שם", "שם התורם", "שם לקוח"):
        if col in df.columns:
            return col
    return None


@st.cache_data(ttl=600)  # Cache for 10 minutes
def calculate_monthly_averages(df: pd.DataFrame, value_column: str = "שקלים") -> Dict[str, Union[int, float]]:
    """Calculate monthly averages and statistics"""
    if not isinstance(df, pd.DataFrame) or value_column not in df.columns or df.empty:
        return {"monthly_avg": 0, "min_monthly": 0, "max_monthly": 0, "total_months": 0}
    try:
        # Group by month and calculate totals - ensure dates are properly converted
        try:
            df_copy = df.copy()
            df_copy["תאריך"] = pd.to_datetime(df_copy["תאריך"], errors="coerce")
            # Filter out rows with invalid dates
            valid_df = df_copy.dropna(subset=["תאריך"])
            if valid_df.empty:
                return {"monthly_avg": 0, "min_monthly": 0, "max_monthly": 0, "total_months": 0}
            monthly_totals = valid_df.groupby(valid_df["תאריך"].dt.strftime("%Y-%m"))[
                value_column
            ].sum()
        except Exception as e:
            logging.warning(f"Could not calculate monthly totals: {e}")
            return {"monthly_avg": 0, "min_monthly": 0, "max_monthly": 0, "total_months": 0}

        # Calculate statistics
        monthly_avg = monthly_totals.mean() if len(monthly_totals) > 0 else 0
        min_monthly = monthly_totals.min() if len(monthly_totals) > 0 else 0
        max_monthly = monthly_totals.max() if len(monthly_totals) > 0 else 0
        total_months = len(monthly_totals)

        return {
            "monthly_avg": monthly_avg,
            "min_monthly": min_monthly,
            "max_monthly": max_monthly,
            "total_months": total_months,
        }
    except Exception as e:
        logging.error(f"Error calculating monthly averages: {str(e)}")
        return {"monthly_avg": 0, "min_monthly": 0, "max_monthly": 0, "total_months": 0}


def calculate_total_support(df: pd.DataFrame, value_column: str = "סכום חודשי") -> dict:
    """Calculate total support statistics"""
    if not isinstance(df, pd.DataFrame) or value_column not in df.columns or df.empty:
        return {
            "total_support": 0,
            "avg_support": 0,
            "min_support": 0,
            "max_support": 0,
            "support_count": 0,
        }
    try:
        # Calculate statistics
        total_support = df[value_column].sum()
        try:
            avg_support = total_support / len(df) if len(df) > 0 else 0
        except (ZeroDivisionError, TypeError):
            avg_support = 0
        min_support = float(df[value_column].min())
        max_support = float(df[value_column].max())
        support_count = len(df)

        return {
            "total_support": total_support,
            "avg_support": avg_support,
            "min_support": min_support,
            "max_support": max_support,
            "support_count": support_count,
        }
    except Exception as e:
        logging.error(f"Error calculating total support: {str(e)}")
        return {
            "total_support": 0,
            "avg_support": 0,
            "min_support": 0,
            "max_support": 0,
            "support_count": 0,
        }


@st.cache_data(ttl=600)  # Cache for 10 minutes
def calculate_monthly_budget(expenses_df: pd.DataFrame, donations_df: pd.DataFrame) -> dict:
    """Calculate monthly budget statistics"""
    try:
        if not isinstance(expenses_df, pd.DataFrame) or not isinstance(donations_df, pd.DataFrame):
            raise ValueError("הנתונים חייבים להיות DataFrame")

        expense_amount_col = _get_amount_column(expenses_df)
        donation_amount_col = _get_amount_column(donations_df)

        # Convert amount columns to numeric, handling mixed data types
        if expense_amount_col:
            expenses_df[expense_amount_col] = pd.to_numeric(
                expenses_df[expense_amount_col], errors="coerce"
            ).fillna(0)
        if donation_amount_col:
            donations_df[donation_amount_col] = pd.to_numeric(
                donations_df[donation_amount_col], errors="coerce"
            ).fillna(0)

        total_expenses = expenses_df[expense_amount_col].sum() if expense_amount_col else 0
        total_donations = donations_df[donation_amount_col].sum() if donation_amount_col else 0
        balance = total_donations - total_expenses

        monthly_expenses = {}
        monthly_donations = {}

        if expense_amount_col:
            try:
                expenses_df_copy = expenses_df.copy()
                date_col = expenses_df_copy.columns[0]
                expenses_df_copy["תאריך"] = pd.to_datetime(
                    expenses_df_copy[date_col], errors="coerce"
                )
                valid_expenses = expenses_df_copy.dropna(subset=["תאריך"])
                if not valid_expenses.empty:
                    monthly_expenses = (
                        valid_expenses.groupby(valid_expenses["תאריך"].dt.strftime("%Y-%m"))[
                            expense_amount_col
                        ]
                        .sum()
                        .to_dict()
                    )
            except Exception as exc:
                logging.warning(f"Could not calculate monthly expenses: {exc}")

        if donation_amount_col:
            try:
                donations_df_copy = donations_df.copy()
                date_col = donations_df_copy.columns[0]
                donations_df_copy["תאריך"] = pd.to_datetime(
                    donations_df_copy[date_col], errors="coerce"
                )
                valid_donations = donations_df_copy.dropna(subset=["תאריך"])
                if not valid_donations.empty:
                    monthly_donations = (
                        valid_donations.groupby(valid_donations["תאריך"].dt.strftime("%Y-%m"))[
                            donation_amount_col
                        ]
                        .sum()
                        .to_dict()
                    )
            except Exception as exc:
                logging.warning(f"Could not calculate monthly donations: {exc}")

        try:
            utilization_percentage = (
                (total_expenses / total_donations * 100) if total_donations > 0 else 0
            )
        except (ZeroDivisionError, TypeError):
            utilization_percentage = 0

        if balance >= 0:
            if total_expenses == 0:
                status = "מספק"
            elif balance >= total_expenses * 0.2:
                status = "מצוין"
            elif balance >= total_expenses * 0.1:
                status = "טוב"
            else:
                status = "מספק"
        else:
            denominator = total_donations if total_donations > 0 else 1
            deficit_ratio = abs(balance) / denominator
            if deficit_ratio > 0.2:
                status = "קריטי"
            elif deficit_ratio > 0.1:
                status = "מדאיג"
            else:
                status = "טעון שיפור"

        return {
            "total_expenses": float(total_expenses),
            "total_donations": float(total_donations),
            "balance": float(balance),
            "status": status,
            "utilization_percentage": float(utilization_percentage),
            "monthly_expenses": monthly_expenses,
            "monthly_donations": monthly_donations,
            "donation_trend": "increasing" if utilization_percentage < 80 else "stable",
            "expense_trend": "stable",
        }

    except Exception as exc:
        logging.error(f"Error calculating monthly budget: {exc}")
        logging.error(traceback.format_exc())
        return {
            "total_expenses": 0,
            "total_donations": 0,
            "balance": 0,
            "status": "שגיאה",
            "utilization_percentage": 0,
            "monthly_expenses": {},
            "monthly_donations": {},
            "donation_trend": "stable",
            "expense_trend": "stable",
        }


@st.cache_data(ttl=600)  # Cache for 10 minutes
def calculate_donor_statistics(df: pd.DataFrame, value_column: str = "שקלים") -> Dict[str, Union[int, float, List[Dict[str, Union[str, int, float]]]]]:
    """Calculate donor statistics"""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return {
            "total_donors": 0,
            "total_donations": 0,
            "avg_donation": 0,
            "min_donation": 0,
            "max_donation": 0,
            "top_donors": [],
        }
    amount_col = value_column if value_column in df.columns else _get_amount_column(df)
    name_col = _get_name_column(df)
    if not amount_col or not name_col:
        return {
            "total_donors": 0,
            "total_donations": 0,
            "avg_donation": 0,
            "min_donation": 0,
            "max_donation": 0,
            "top_donors": [],
        }
    try:
        total_donors = df[name_col].nunique()
        total_donations = df[amount_col].sum()
        try:
            avg_donation = total_donations / total_donors if total_donors > 0 else 0
        except (ZeroDivisionError, TypeError):
            avg_donation = 0

        top_donors_df = (
            df.groupby(name_col)[amount_col]
            .agg(["sum", "count"])
            .sort_values("sum", ascending=False)
            .head(10)
            .reset_index()
        )
        top_donors_df.columns = ["name", "sum", "count"]
        top_donors = top_donors_df.to_dict("records")

        return {
            "total_donors": total_donors,
            "total_donations": total_donations,
            "avg_donation": avg_donation,
            "min_donation": float(df[amount_col].min()) if not df[amount_col].empty else 0,
            "max_donation": float(df[amount_col].max()) if not df[amount_col].empty else 0,
            "top_donors": top_donors,
        }
    except Exception as e:
        logging.error(f"Error calculating donor statistics: {str(e)}")
        return {
            "total_donors": 0,
            "total_donations": 0,
            "avg_donation": 0,
            "min_donation": 0,
            "max_donation": 0,
            "top_donors": [],
        }


def calculate_expense_statistics(df: pd.DataFrame, value_column: str = "שקלים") -> dict:
    """Calculate expense statistics with detailed analysis"""
    if not isinstance(df, pd.DataFrame) or value_column not in df.columns or df.empty:
        return {
            "total_expenses": 0,
            "avg_expense": 0,
            "min_expense": 0,
            "max_expense": 0,
            "expense_categories": {},
            "monthly_expenses": [],
        }
    try:
        # Basic statistics
        total_expenses = df[value_column].sum()
        try:
            avg_expense = total_expenses / len(df) if len(df) > 0 else 0
        except (ZeroDivisionError, TypeError):
            avg_expense = 0

        # Expense categories - use the correct column name
        name_col = "שם" if "שם" in df.columns else df.columns[1] if len(df.columns) > 1 else "שם"
        if name_col in df.columns:
            expense_categories = (
                df.groupby(name_col)[value_column].sum().sort_values(ascending=False)
            )
            expense_categories = expense_categories.to_dict()
        else:
            expense_categories = {}

        # Monthly expenses
        if "תאריך" in df.columns:
            df["תאריך"] = pd.to_datetime(df["תאריך"], format="%d.%m.%Y", errors="coerce")
            monthly_expenses = df.groupby(df["תאריך"].dt.strftime("%Y-%m"))[value_column].sum()
            monthly_expenses = monthly_expenses.to_dict()
        else:
            monthly_expenses = {}

        return {
            "total_expenses": total_expenses,
            "avg_expense": avg_expense,
            "min_expense": float(df[value_column].min()),
            "max_expense": float(df[value_column].max()),
            "expense_categories": expense_categories,
            "monthly_expenses": monthly_expenses,
        }
    except Exception as e:
        logging.error(f"Error calculating expense statistics: {str(e)}")
        return {
            "total_expenses": 0,
            "avg_expense": 0,
            "min_expense": 0,
            "max_expense": 0,
            "expense_categories": {},
            "monthly_expenses": [],
        }


@st.cache_data(ttl=600)  # Cache for 10 minutes
def calculate_widow_statistics(df: pd.DataFrame, value_column: str = "סכום חודשי") -> dict:
    """Calculate widow statistics with detailed analysis"""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return {
            "total_widows": 0,
            "total_support": 0,
            "support_1000_count": 0,
            "support_2000_count": 0,
            "support_distribution": {},
            "monthly_support": [],
        }

    # Check if value_column exists, if not try alternative columns
    if value_column not in df.columns:
        # Try alternative column names
        alternative_columns = ["סכום חודשי", "כמה מקבלת בכל חודש", "סכום", "שקלים"]
        for alt_col in alternative_columns:
            if alt_col in df.columns:
                value_column = alt_col
                break
        else:
            # If no value column found, return basic stats
            name_col = (
                "שם"
                if "שם" in df.columns
                else (
                    "שם " if "שם " in df.columns else df.columns[0] if len(df.columns) > 0 else "שם"
                )
            )
            total_widows = df[name_col].nunique() if name_col in df.columns else 0
            return {
                "total_widows": total_widows,
                "total_support": 0,
                "support_1000_count": 0,
                "support_2000_count": 0,
                "support_distribution": {},
                "monthly_support": [],
            }
    try:
        # Basic statistics - use the correct column name
        name_col = "שם" if "שם" in df.columns else df.columns[0] if len(df.columns) > 0 else "שם"
        total_widows = df[name_col].nunique() if name_col in df.columns else 0

        # Ensure value_column contains numeric data
        try:
            # Convert to numeric, handling any non-numeric values
            numeric_values = pd.to_numeric(df[value_column], errors="coerce")
            # Fill NaN with 0 for calculation purposes
            numeric_values = numeric_values.fillna(0)
            total_support = numeric_values.sum()

            # Count widows by support amount (only 1000 or 2000)
            support_1000_count = int((numeric_values == 1000).sum())
            support_2000_count = int((numeric_values == 2000).sum())
        except Exception as e:
            logging.warning(f"Error processing support values: {e}")
            total_support = 0
            support_1000_count = 0
            support_2000_count = 0

        # Support distribution
        if "שם " in df.columns:
            try:
                # Use numeric values for distribution
                df_copy = df.copy()
                df_copy[value_column] = numeric_values
                support_distribution = (
                    df_copy.groupby("שם ")[value_column].sum().sort_values(ascending=False)
                )
                support_distribution = support_distribution.to_dict()
            except Exception as e:
                logging.warning(f"Error calculating support distribution: {e}")
                support_distribution = {}
        else:
            support_distribution = {}

        # Monthly support
        if "חודש התחלה" in df.columns:
            df["חודש התחלה"] = pd.to_datetime(df["חודש התחלה"], format="%d.%m.%Y", errors="coerce")
            monthly_support = df.groupby(df["חודש התחלה"].dt.strftime("%Y-%m"))[value_column].sum()
            monthly_support = monthly_support.to_dict()
        else:
            monthly_support = {}

        return {
            "total_widows": total_widows,
            "total_support": total_support,
            "support_1000_count": support_1000_count,
            "support_2000_count": support_2000_count,
            "support_distribution": support_distribution,
            "monthly_support": monthly_support,
        }
    except Exception as e:
        logging.error(f"Error calculating widow statistics: {str(e)}")
        return {
            "total_widows": 0,
            "total_support": 0,
            "support_1000_count": 0,
            "support_2000_count": 0,
            "support_distribution": {},
            "monthly_support": [],
        }


def calculate_monthly_trends(expenses_df: pd.DataFrame, donations_df: pd.DataFrame) -> dict:
    """Calculate monthly trends for expenses and donations"""
    try:
        if not isinstance(expenses_df, pd.DataFrame) or not isinstance(donations_df, pd.DataFrame):
            raise ValueError("הנתונים חייבים להיות DataFrame")

        # Calculate monthly trends for expenses
        expense_amount_col = _get_amount_column(expenses_df)
        donation_amount_col = _get_amount_column(donations_df)

        if "תאריך" in expenses_df.columns and expense_amount_col:
            expenses_df = expenses_df.copy()
            expenses_df["תאריך"] = pd.to_datetime(
                expenses_df["תאריך"], format="%d.%m.%Y", errors="coerce"
            )
            monthly_expenses = expenses_df.groupby(expenses_df["תאריך"].dt.strftime("%Y-%m"))[
                expense_amount_col
            ].sum()

            # Calculate trend and change
            if len(monthly_expenses) > 1:
                expenses_trend = (
                    "עולה" if monthly_expenses.iloc[-1] > monthly_expenses.iloc[0] else "יורד"
                )
                expenses_change = (
                    (
                        (monthly_expenses.iloc[-1] - monthly_expenses.iloc[0])
                        / monthly_expenses.iloc[0]
                        * 100
                    )
                    if monthly_expenses.iloc[0] != 0
                    else 0
                )
            else:
                expenses_trend = "יציב"
                expenses_change = 0
        else:
            monthly_expenses = pd.Series()
            expenses_trend = "לא ניתן לחשב"
            expenses_change = 0

        # Calculate monthly trends for donations
        if "תאריך" in donations_df.columns and donation_amount_col:
            donations_df = donations_df.copy()
            donations_df["תאריך"] = pd.to_datetime(
                donations_df["תאריך"], format="%d.%m.%Y", errors="coerce"
            )
            monthly_donations = donations_df.groupby(donations_df["תאריך"].dt.strftime("%Y-%m"))[
                donation_amount_col
            ].sum()

            # Calculate trend and change
            if len(monthly_donations) > 1:
                donations_trend = (
                    "עולה" if monthly_donations.iloc[-1] > monthly_donations.iloc[0] else "יורד"
                )
                donations_change = (
                    (
                        (monthly_donations.iloc[-1] - monthly_donations.iloc[0])
                        / monthly_donations.iloc[0]
                        * 100
                    )
                    if monthly_donations.iloc[0] != 0
                    else 0
                )
            else:
                donations_trend = "יציב"
                donations_change = 0
        else:
            monthly_donations = pd.Series()
            donations_trend = "לא ניתן לחשב"
            donations_change = 0

        # Calculate monthly comparison
        monthly_comparison = {}
        if not monthly_expenses.empty and not monthly_donations.empty:
            common_months = set(monthly_expenses.index).intersection(set(monthly_donations.index))
            for month in common_months:
                monthly_comparison[month] = {
                    "expenses": monthly_expenses[month],
                    "donations": monthly_donations[month],
                    "balance": monthly_donations[month] - monthly_expenses[month],
                }

        return {
            "expenses_trend": expenses_trend,
            "donations_trend": donations_trend,
            "expenses_change": expenses_change,
            "donations_change": donations_change,
            "monthly_expenses": monthly_expenses.to_dict(),
            "monthly_donations": monthly_donations.to_dict(),
            "monthly_comparison": monthly_comparison,
        }

    except Exception as e:
        logging.error(f"Error calculating monthly trends: {str(e)}")
        return {
            "expenses_trend": "שגיאה",
            "donations_trend": "שגיאה",
            "expenses_change": 0,
            "donations_change": 0,
            "monthly_expenses": {},
            "monthly_donations": {},
            "monthly_comparison": {},
        }


def calculate_trend_percentage(monthly_data: pd.Series) -> float:
    """Calculate percentage change for a trend"""
    if len(monthly_data) > 1:
        first_month = monthly_data.iloc[0]
        last_month = monthly_data.iloc[-1]
        return ((last_month - first_month) / first_month * 100) if first_month != 0 else 0
    return 0


def determine_trend(percentage_change: float) -> str:
    """Determine trend based on percentage change"""
    if percentage_change > 5:
        return "עולה"
    elif percentage_change < -5:
        return "יורד"
    else:
        return "יציב"


def calculate_36_month_budget(widows_df: pd.DataFrame, current_support: float) -> dict:
    """Calculate 36-month budget projection with detailed analysis"""
    try:
        # Calculate total required support
        total_required = current_support * 36

        # Calculate current support for 36 months
        support_36_months = widows_df["סכום חודשי"].sum() * 36

        # Calculate difference and percentage
        diff = support_36_months - total_required
        coverage_percentage = (
            (support_36_months / total_required * 100) if total_required > 0 else 0
        )

        # Calculate monthly breakdown
        monthly_breakdown = []
        if "חודש התחלה" in widows_df.columns:
            widows_df["חודש התחלה"] = pd.to_datetime(
                widows_df["חודש התחלה"], format="%d.%m.%Y", errors="coerce"
            )
            monthly_support = widows_df.groupby(widows_df["חודש התחלה"].dt.strftime("%Y-%m"))[
                "סכום חודשי"
            ].sum()

            for month, amount in monthly_support.items():
                monthly_breakdown.append(
                    {
                        "month": month,
                        "amount": amount,
                        "required": current_support,
                        "difference": amount - current_support,
                    }
                )

        return {
            "support_36_months": support_36_months,
            "total_required": total_required,
            "diff": diff,
            "coverage_percentage": coverage_percentage,
            "monthly_breakdown": monthly_breakdown,
            "status": "מספיק" if coverage_percentage >= 100 else "חסר",
        }
    except Exception as e:
        logging.error(f"Error calculating 36-month budget: {str(e)}")
        return {
            "support_36_months": 0,
            "total_required": 0,
            "diff": 0,
            "coverage_percentage": 0,
            "monthly_breakdown": [],
            "status": "שגיאה",
        }


# Removed unused functions: calculate_monthly_averages_old, calculate_total_support_old, 
# calculate_monthly_budget_old, calculate_budget_forecast
