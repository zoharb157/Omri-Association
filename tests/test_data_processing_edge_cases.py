import numpy as np
import pandas as pd
import pytest

from data_processing import (
    calculate_monthly_budget,
    calculate_donor_statistics,
    calculate_widow_statistics,
)


class TestDataProcessingEdgeCases:
    """Test edge cases and error conditions in data processing"""

    def test_calculate_monthly_budget_with_mixed_data_types(self):
        """Test monthly budget calculation with mixed data types"""
        expenses_df = pd.DataFrame({
            "שקלים": [100, "200.5", 300.75, "400"],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, "600.25", 700.5, "800.75"],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        assert "total_expenses" in result
        assert "total_donations" in result
        assert "balance" in result
        # Should handle mixed data types gracefully
        assert result["total_expenses"] > 0
        assert result["total_donations"] > 0

    def test_calculate_monthly_budget_with_negative_values(self):
        """Test monthly budget calculation with negative values"""
        expenses_df = pd.DataFrame({
            "שקלים": [100, -50, 200],  # Negative expense (refund?)
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, 600, -100],  # Negative donation (return?)
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle negative values appropriately
        assert result["total_expenses"] == 250  # 100 + (-50) + 200
        assert result["total_donations"] == 1000  # 500 + 600 + (-100)

    def test_calculate_donor_statistics_with_special_characters(self):
        """Test donor statistics with special characters in names"""
        donations_df = pd.DataFrame({
            "שם": ["תורם א", "תורם-ב", "תורם_ג", "תורם.ד"],
            "שקלים": [100, 200, 300, 400],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
        })

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        assert result["total_donors"] == 4
        assert result["total_donations"] == 1000

    def test_calculate_widow_statistics_with_unicode_names(self):
        """Test widow statistics with unicode names"""
        almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג", "אלמנה ד"],
            "סכום חודשי": [1000, 2000, 3000, 4000],
            "גיל": [65, 70, 75, 80]
        })

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        assert result["total_widows"] == 4
        assert result["total_support"] == 10000

    def test_calculate_monthly_budget_with_duplicate_dates(self):
        """Test monthly budget calculation with duplicate dates"""
        expenses_df = pd.DataFrame({
            "שקלים": [100, 200, 300],
            "תאריך": ["2024-01-01", "2024-01-01", "2024-01-02"]  # Duplicate date
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, 600],
            "תאריך": ["2024-01-01", "2024-01-02"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle duplicate dates gracefully
        assert result["total_expenses"] == 600
        assert result["total_donations"] == 1100

    def test_calculate_donor_statistics_with_empty_strings(self):
        """Test donor statistics with empty strings in data"""
        donations_df = pd.DataFrame({
            "שם": ["תורם א", "", "תורם ג", None],
            "שקלים": [100, 200, 300, 400],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
        })

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        # Should handle empty strings and None values gracefully
        assert result["total_donations"] == 1000

    def test_calculate_widow_statistics_with_missing_ages(self):
        """Test widow statistics with missing age data"""
        almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג"],
            "סכום חודשי": [1000, 2000, 3000],
            "גיל": [65, None, 75]  # Missing age
        })

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        assert result["total_widows"] == 3
        assert result["total_support"] == 6000

    def test_calculate_monthly_budget_with_future_dates(self):
        """Test monthly budget calculation with future dates"""
        expenses_df = pd.DataFrame({
            "שקלים": [100, 200],
            "תאריך": ["2025-01-01", "2025-01-02"]  # Future dates
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, 600],
            "תאריך": ["2025-01-01", "2025-01-02"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle future dates gracefully
        assert result["total_expenses"] == 300
        assert result["total_donations"] == 1100

    def test_calculate_donor_statistics_with_very_long_names(self):
        """Test donor statistics with very long names"""
        long_name = "תורם עם שם מאוד מאוד ארוך שמכיל הרבה תווים ומילים כדי לבדוק איך המערכת מטפלת בשמות ארוכים"
        donations_df = pd.DataFrame({
            "שם": [long_name, "תורם ב"],
            "שקלים": [100, 200],
            "תאריך": ["2024-01-01", "2024-01-02"]
        })

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        assert result["total_donors"] == 2
        assert result["total_donations"] == 300

    def test_calculate_widow_statistics_with_extreme_ages(self):
        """Test widow statistics with extreme age values"""
        almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג"],
            "סכום חודשי": [1000, 2000, 3000],
            "גיל": [18, 120, 65]  # Very young and very old
        })

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        assert result["total_widows"] == 3
        assert result["total_support"] == 6000

    def test_calculate_monthly_budget_with_zero_values(self):
        """Test monthly budget calculation with zero values"""
        expenses_df = pd.DataFrame({
            "שקלים": [0, 100, 0],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, 0, 300],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        assert result["total_expenses"] == 100
        assert result["total_donations"] == 800

    def test_calculate_donor_statistics_with_duplicate_names(self):
        """Test donor statistics with duplicate donor names"""
        donations_df = pd.DataFrame({
            "שם": ["תורם א", "תורם א", "תורם ב", "תורם ב", "תורם ב"],
            "שקלים": [100, 200, 300, 400, 500],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
        })

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        # Should count unique donors only
        assert result["total_donors"] == 2
        assert result["total_donations"] == 1500

    def test_calculate_widow_statistics_with_duplicate_names(self):
        """Test widow statistics with duplicate widow names"""
        almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה א", "אלמנה ב"],
            "סכום חודשי": [1000, 2000, 3000],
            "גיל": [65, 70, 75]
        })

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        # Should count unique widows only
        assert result["total_widows"] == 2
        assert result["total_support"] == 6000

    def test_calculate_monthly_budget_with_invalid_dates(self):
        """Test monthly budget calculation with invalid date formats"""
        expenses_df = pd.DataFrame({
            "שקלים": [100, 200],
            "תאריך": ["invalid-date", "2024-01-02"]
        })
        donations_df = pd.DataFrame({
            "שקלים": [500, 600],
            "תאריך": ["2024-01-01", "invalid-date"]
        })

        result = calculate_monthly_budget(expenses_df, donations_df)

        assert isinstance(result, dict)
        # Should handle invalid dates gracefully
        assert result["total_expenses"] >= 0
        assert result["total_donations"] >= 0

    def test_calculate_donor_statistics_with_whitespace_names(self):
        """Test donor statistics with names containing only whitespace"""
        donations_df = pd.DataFrame({
            "שם": ["תורם א", "   ", "\t", "תורם ב"],
            "שקלים": [100, 200, 300, 400],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
        })

        result = calculate_donor_statistics(donations_df)

        assert isinstance(result, dict)
        # Should handle whitespace-only names gracefully
        assert result["total_donations"] == 1000

    def test_calculate_widow_statistics_with_negative_support(self):
        """Test widow statistics with negative support amounts"""
        almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג"],
            "סכום חודשי": [1000, -500, 2000],  # Negative support amount
            "גיל": [65, 70, 75]
        })

        result = calculate_widow_statistics(almanot_df)

        assert isinstance(result, dict)
        # Should handle negative support amounts appropriately
        assert result["total_support"] == 2500  # 1000 + (-500) + 2000
