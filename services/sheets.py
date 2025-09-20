"""Service layer helpers for loading dashboard data from Google Sheets."""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

from config import Config
from google_sheets_io import load_all_data

LOGGER = logging.getLogger(__name__)


def _empty_frames() -> dict[str, pd.DataFrame]:
    """Return empty dataframes for the expected sheets."""
    return {
        "Expenses": pd.DataFrame(),
        "Donations": pd.DataFrame(),
        "Investors": pd.DataFrame(),
        "Widows": pd.DataFrame(),
    }


@st.cache_data(ttl=Config.DATA_CACHE_TTL)  # Cache for 5 minutes
def fetch_dashboard_frames() -> dict[str, pd.DataFrame]:
    """Fetch all dashboard sheets, normalising missing data.

    Returns a dict keyed by sheet name with pandas DataFrames. Any failures are
    logged and replaced with empty frames so callers can degrade gracefully.
    """
    try:
        all_data = load_all_data()
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.exception("Failed to load data from Google Sheets: %s", exc)
        return _empty_frames()

    if not all_data:
        LOGGER.warning("Google Sheets returned no data; using empty frames")
        return _empty_frames()

    frames = _empty_frames()

    expenses = all_data.get("Expenses")
    if isinstance(expenses, pd.DataFrame):
        frames["Expenses"] = expenses

    donations = all_data.get("Donations")
    if isinstance(donations, pd.DataFrame):
        frames["Donations"] = donations

    investors = all_data.get("Investors")
    if isinstance(investors, pd.DataFrame):
        frames["Investors"] = investors

    # Support both the legacy "Almanot" sheet and the newer "Widows" sheet name.
    widows = all_data.get("Widows")
    if widows is None:
        widows = all_data.get("Almanot")
    if isinstance(widows, pd.DataFrame):
        frames["Widows"] = widows

    return frames
