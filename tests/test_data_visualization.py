#!/usr/bin/env python3
"""
Unit tests for data visualization module
Tests chart creation and visualization functionality
"""

import pandas as pd

from data_visualization import (
    create_budget_distribution_chart,
    create_comparison_chart,
    create_donor_contribution_chart,
    create_monthly_trends,
    create_widows_support_chart,
)


class TestDataVisualization:
    """Test data visualization functionality"""

    def test_create_budget_distribution_chart_basic(self):
        """Test create_budget_distribution_chart with basic data"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart = create_budget_distribution_chart(expenses_df)

        assert chart is not None

    def test_create_budget_distribution_chart_empty_data(self):
        """Test create_budget_distribution_chart with empty data"""
        empty_df = pd.DataFrame()

        chart = create_budget_distribution_chart(empty_df)

        assert chart is None

    def test_create_monthly_trends_basic(self):
        """Test create_monthly_trends with basic data"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, 700], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        chart = create_monthly_trends(expenses_df, donations_df)

        assert chart is not None

    def test_create_monthly_trends_empty_data(self):
        """Test create_monthly_trends with empty data"""
        empty_df = pd.DataFrame()

        chart = create_monthly_trends(empty_df, empty_df)

        assert chart is None

    def test_create_widows_support_chart_basic(self):
        """Test create_widows_support_chart with basic data"""
        almanot_df = pd.DataFrame(
            {"סכום חודשי": [1000, 2000, 3000], "שם": ["Widow 1", "Widow 2", "Widow 3"]}
        )

        chart = create_widows_support_chart(almanot_df)

        assert chart is not None

    def test_create_widows_support_chart_empty_data(self):
        """Test create_widows_support_chart with empty data"""
        empty_df = pd.DataFrame()

        chart = create_widows_support_chart(empty_df)

        assert chart is None

    def test_create_donor_contribution_chart_basic(self):
        """Test create_donor_contribution_chart with basic data"""
        donations_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "שם": ["Donor 1", "Donor 2", "Donor 3"]}
        )

        chart = create_donor_contribution_chart(donations_df)

        assert chart is not None

    def test_create_donor_contribution_chart_empty_data(self):
        """Test create_donor_contribution_chart with empty data"""
        empty_df = pd.DataFrame()

        chart = create_donor_contribution_chart(empty_df)

        assert chart is None

    def test_create_comparison_chart_basic(self):
        """Test create_comparison_chart with basic data"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, 700], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        create_comparison_chart(expenses_df, donations_df)

        # Function doesn't return anything, just creates chart
        assert True

    def test_create_comparison_chart_empty_data(self):
        """Test create_comparison_chart with empty data"""
        empty_df = pd.DataFrame()

        create_comparison_chart(empty_df, empty_df)

        # Function doesn't return anything, just creates chart
        assert True

    def test_charts_with_nan_values(self):
        """Test charts handle NaN values gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, float("nan"), 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, float("nan")], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_negative_values(self):
        """Test charts handle negative values gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, -50, 300],  # Negative expense (refund?)
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, -100],  # Negative donation (return?)
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_very_large_values(self):
        """Test charts handle very large values gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [1000000, 2000000, 3000000],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [5000000, 6000000, 7000000],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_mixed_data_types(self):
        """Test charts handle mixed data types gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, "200", 300.5],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, "600", 700.25], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_duplicate_dates(self):
        """Test charts handle duplicate dates gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-01", "2024-01-02"],  # Duplicate date
            }
        )
        donations_df = pd.DataFrame({"שקלים": [500, 600], "תאריך": ["2024-01-01", "2024-01-02"]})

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_invalid_dates(self):
        """Test charts handle invalid dates gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense 1", "Expense 2", "Expense 3"],
                "שקלים": [100, 200, 300],
                "תאריך": ["invalid_date", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, 700], "תאריך": ["2024-01-01", "invalid_date", "2024-01-03"]}
        )

        chart1 = create_budget_distribution_chart(expenses_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_unicode_names(self):
        """Test charts handle unicode names gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["הוצאה 1", "הוצאה 2", "הוצאה 3"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": ["תורם 1", "תורם 2", "תורם 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart1 = create_donor_contribution_chart(donations_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_very_long_names(self):
        """Test charts handle very long names gracefully"""
        long_name = "A" * 1000
        expenses_df = pd.DataFrame(
            {
                "שם": [long_name, "Expense 2", "Expense 3"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": [long_name, "Donor 2", "Donor 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart1 = create_donor_contribution_chart(donations_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None

    def test_charts_with_special_characters(self):
        """Test charts handle special characters gracefully"""
        expenses_df = pd.DataFrame(
            {
                "שם": ["Expense!@#$%", "Expense^&*()", "Expense_+-=[]"],
                "שקלים": [100, 200, 300],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": ["Donor!@#$%", "Donor^&*()", "Donor_+-=[]"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        chart1 = create_donor_contribution_chart(donations_df)
        chart2 = create_monthly_trends(expenses_df, donations_df)

        assert chart1 is not None
        assert chart2 is not None
