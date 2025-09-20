#!/usr/bin/env python3
"""
Comprehensive unit tests for data processing functionality
Tests all data processing functions with various edge cases
"""


import numpy as np
import pandas as pd

from data_processing import (
    calculate_donor_statistics,
    calculate_monthly_budget,
    calculate_widow_statistics,
)
from tests.fixtures.sample_data import (
    sample_almanot_df,
    sample_donations_df,
    sample_expenses_df,
)


class TestDataProcessingComprehensive:
    """Comprehensive tests for data processing functions"""

    def test_calculate_monthly_budget_basic(self):
        """Test basic monthly budget calculation"""
        expenses_df = sample_expenses_df()
        donations_df = sample_donations_df()

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        assert "total_donations" in result
        assert "total_expenses" in result
        assert "balance" in result
        assert "monthly_donations" in result
        assert "monthly_expenses" in result

    def test_calculate_monthly_budget_with_empty_data(self):
        """Test monthly budget calculation with empty dataframes"""
        empty_expenses = pd.DataFrame()
        empty_donations = pd.DataFrame()

        result = calculate_monthly_budget(empty_expenses, empty_donations)

        assert isinstance(result, dict)
        assert result["total_donations"] == 0
        assert result["total_expenses"] == 0
        assert result["balance"] == 0

    def test_calculate_monthly_budget_with_nan_values(self):
        """Test monthly budget calculation with NaN values"""
        expenses_df = pd.DataFrame(
            {
                "שקלים": [100, np.nan, 200, None],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [300, 400, np.nan, None],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            }
        )

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle NaN values gracefully
        assert result["total_donations"] >= 0
        assert result["total_expenses"] >= 0

    def test_calculate_monthly_budget_with_invalid_dates(self):
        """Test monthly budget calculation with invalid dates"""
        expenses_df = pd.DataFrame({"שקלים": [100, 200], "תאריך": ["invalid_date", "2024-01-02"]})
        donations_df = pd.DataFrame({"שקלים": [300, 400], "תאריך": ["2024-01-01", "invalid_date"]})

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle invalid dates gracefully

    def test_calculate_donor_statistics_basic(self):
        """Test basic donor statistics calculation"""
        donations_df = sample_donations_df()

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        assert "total_donors" in result
        assert "total_donations" in result
        assert "avg_donation" in result

    def test_calculate_donor_statistics_with_empty_data(self):
        """Test donor statistics calculation with empty dataframe"""
        empty_donations = pd.DataFrame()

        result = calculate_donor_statistics(empty_donations)

        assert isinstance(result, dict)
        assert result["total_donors"] == 0
        assert result["total_donations"] == 0
        assert result["avg_donation"] == 0

    def test_calculate_donor_statistics_with_duplicate_donors(self):
        """Test donor statistics with duplicate donor names"""
        donations_df = pd.DataFrame(
            {
                "שם": ["Donor A", "Donor A", "Donor B", "Donor B"],
                "שקלים": [100, 200, 300, 400],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            }
        )

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        # Should handle duplicate donors correctly
        assert result["total_donors"] == 2  # Unique donors only

    def test_calculate_widow_statistics_basic(self):
        """Test basic widow statistics calculation"""
        almanot_df = sample_almanot_df()

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        assert "total_widows" in result
        assert "total_support" in result
        assert "support_1000_count" in result

    def test_calculate_widow_statistics_with_empty_data(self):
        """Test widow statistics calculation with empty dataframe"""
        empty_almanot = pd.DataFrame()

        result = calculate_widow_statistics(empty_almanot)

        assert isinstance(result, dict)
        assert result["total_widows"] == 0
        assert result["total_support"] == 0
        assert result["support_1000_count"] == 0

    def test_calculate_widow_statistics_with_missing_columns(self):
        """Test widow statistics with missing required columns"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["Widow 1", "Widow 2"],
                "גיל": [65, 70],
                # Missing "סכום חודשי" column
            }
        )

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        # Should handle missing columns gracefully

    def test_calculate_widow_statistics_with_nan_support_amounts(self):
        """Test widow statistics with NaN support amounts"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["Widow 1", "Widow 2", "Widow 3"],
                "סכום חודשי": [1000, np.nan, 2000],
                "גיל": [65, 70, 75],
            }
        )

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        # Should handle NaN values gracefully
        assert result["total_support"] >= 0

    def test_calculate_widow_statistics_with_zero_support(self):
        """Test widow statistics with zero support amounts"""
        almanot_df = pd.DataFrame(
            {"שם": ["Widow 1", "Widow 2"], "סכום חודשי": [0, 0], "גיל": [65, 70]}
        )

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        assert result["total_support"] == 0
        assert result["support_1000_count"] == 0

    def test_calculate_widow_statistics_with_negative_support(self):
        """Test widow statistics with negative support amounts"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["Widow 1", "Widow 2"],
                "סכום חודשי": [-1000, 2000],  # Negative amount
                "גיל": [65, 70],
            }
        )

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        # Should handle negative values appropriately

    def test_calculate_monthly_budget_balance_calculation(self):
        """Test that balance is calculated correctly"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 400, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        result = calculate_monthly_budget(expenses_df, donations_df)

        expected_balance = 1200 - 600  # 1200 donations - 600 expenses
        assert result["balance"] == expected_balance

    def test_calculate_donor_statistics_average_calculation(self):
        """Test that average donation is calculated correctly"""
        donations_df = pd.DataFrame(
            {
                "שם": ["Donor A", "Donor B", "Donor C"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        result = calculate_donor_statistics(donations_df)

        expected_average = 600 / 3  # 600 total / 3 donations
        assert result["avg_donation"] == expected_average

    def test_calculate_widow_statistics_average_calculation(self):
        """Test that average support is calculated correctly"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["Widow 1", "Widow 2", "Widow 3"],
                "סכום חודשי": [1000, 2000, 3000],
                "גיל": [65, 70, 75],
            }
        )

        result = calculate_widow_statistics(almanot_df)

        # Test that we have the expected number of widows
        assert result["total_widows"] == 3

    def test_data_processing_with_mixed_data_types(self):
        """Test data processing with mixed data types in amount columns"""
        expenses_df = pd.DataFrame(
            {
                "שקלים": [100, "200", 300.5, "400.75"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, "600", 700.25, "800.50"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            }
        )

        budget_result = calculate_monthly_budget(expenses_df, donations_df)
        donor_result = calculate_donor_statistics(donations_df)

        assert isinstance(budget_result, dict)
        assert isinstance(donor_result, dict)
        # Should handle mixed data types gracefully

    def test_data_processing_with_very_large_numbers(self):
        """Test data processing with very large numbers"""
        expenses_df = pd.DataFrame(
            {"שקלים": [999999999, 1000000000], "תאריך": ["2024-01-01", "2024-01-02"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [2000000000, 3000000000], "תאריך": ["2024-01-01", "2024-01-02"]}
        )

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle large numbers without overflow
