"""Utility fixtures for tests."""

from __future__ import annotations

import pandas as pd


def sample_donations_df() -> pd.DataFrame:
    """Return a tiny donations dataframe used for smoke tests."""
    return pd.DataFrame(
        {
            "תאריך": pd.to_datetime(["2024-01-01", "2024-02-01"]),
            "שם": ["תורם א", "תורם ב"],
            "שקלים": [1500, 1200],
        }
    )


def sample_expenses_df() -> pd.DataFrame:
    """Return a tiny expenses dataframe used for smoke tests."""
    return pd.DataFrame(
        {
            "תאריך": pd.to_datetime(["2024-01-03", "2024-02-05"]),
            "שם": ["שירות א", "שירות ב"],
            "שקלים": [700, 500],
        }
    )
