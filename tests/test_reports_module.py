#!/usr/bin/env python3
"""
Unit tests for reports module
Tests report generation functionality
"""

import pandas as pd

from reports.reports import (
    clean_text_for_pdf,
    generate_budget_report,
    generate_donor_report,
    generate_monthly_report,
    generate_widows_report,
)


class TestReportsModule:
    """Test reports module functionality"""

    def test_clean_text_for_pdf_basic(self):
        """Test clean_text_for_pdf with basic text"""
        result = clean_text_for_pdf("Hello World")
        assert isinstance(result, str)

    def test_clean_text_for_pdf_unicode(self):
        """Test clean_text_for_pdf with unicode text"""
        result = clean_text_for_pdf("שלום עולם")
        assert isinstance(result, str)

    def test_clean_text_for_pdf_special_chars(self):
        """Test clean_text_for_pdf with special characters"""
        result = clean_text_for_pdf("Test!@#$%^&*()")
        assert isinstance(result, str)

    def test_generate_monthly_report_basic(self):
        """Test generate_monthly_report with basic data"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, 700], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        almanot_df = pd.DataFrame({"שם": ["Widow 1", "Widow 2"], "סכום חודשי": [1000, 2000]})

        filename = generate_monthly_report(expenses_df, donations_df, almanot_df)

        assert isinstance(filename, str)

    def test_generate_monthly_report_empty(self):
        """Test generate_monthly_report with empty data"""
        empty_df = pd.DataFrame()

        filename = generate_monthly_report(empty_df, empty_df, empty_df)

        assert isinstance(filename, str)

    def test_generate_budget_report_basic(self):
        """Test generate_budget_report with basic data"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, 700], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )

        filename = generate_budget_report(expenses_df, donations_df)

        assert isinstance(filename, str)

    def test_generate_budget_report_empty(self):
        """Test generate_budget_report with empty data"""
        empty_df = pd.DataFrame()

        filename = generate_budget_report(empty_df, empty_df)

        assert isinstance(filename, str)

    def test_generate_donor_report_basic(self):
        """Test generate_donor_report with basic data"""
        donations_df = pd.DataFrame(
            {
                "שקלים": [100, 200, 300],
                "שם": ["Donor 1", "Donor 2", "Donor 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        filename = generate_donor_report(donations_df)

        assert isinstance(filename, str)

    def test_generate_donor_report_empty(self):
        """Test generate_donor_report with empty data"""
        empty_df = pd.DataFrame()

        filename = generate_donor_report(empty_df)

        assert isinstance(filename, str)

    def test_generate_widows_report_basic(self):
        """Test generate_widows_report with basic data"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["Widow 1", "Widow 2", "Widow 3"],
                "סכום חודשי": [1000, 2000, 3000],
                "גיל": [65, 70, 75],
            }
        )

        filename = generate_widows_report(almanot_df)

        assert isinstance(filename, str)

    def test_generate_widows_report_empty(self):
        """Test generate_widows_report with empty data"""
        empty_df = pd.DataFrame()

        filename = generate_widows_report(empty_df)

        assert isinstance(filename, str)

    def test_reports_with_nan_values(self):
        """Test reports handle NaN values gracefully"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, float("nan"), 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {"שקלים": [500, 600, float("nan")], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        almanot_df = pd.DataFrame(
            {"שם": ["Widow 1", "Widow 2"], "סכום חודשי": [1000, float("nan")]}
        )

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)

    def test_reports_with_negative_values(self):
        """Test reports handle negative values gracefully"""
        expenses_df = pd.DataFrame(
            {
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
        almanot_df = pd.DataFrame(
            {"שם": ["Widow 1", "Widow 2"], "סכום חודשי": [1000, -500]}  # Negative support (debt?)
        )

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)

    def test_reports_with_unicode_names(self):
        """Test reports handle unicode names gracefully"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": ["תורם 1", "תורם 2", "תורם 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        almanot_df = pd.DataFrame({"שם": ["אלמנה 1", "אלמנה 2"], "סכום חודשי": [1000, 2000]})

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)

    def test_reports_with_special_characters(self):
        """Test reports handle special characters gracefully"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": ["Donor!@#$%", "Donor^&*()", "Donor_+-=[]"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        almanot_df = pd.DataFrame({"שם": ["Widow!@#$%", "Widow^&*()"], "סכום חודשי": [1000, 2000]})

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)

    def test_reports_with_very_long_names(self):
        """Test reports handle very long names gracefully"""
        long_name = "A" * 1000
        expenses_df = pd.DataFrame(
            {"שקלים": [100, 200, 300], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, 600, 700],
                "שם": [long_name, "Donor 2", "Donor 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        almanot_df = pd.DataFrame({"שם": [long_name, "Widow 2"], "סכום חודשי": [1000, 2000]})

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)

    def test_reports_with_mixed_data_types(self):
        """Test reports handle mixed data types gracefully"""
        expenses_df = pd.DataFrame(
            {"שקלים": [100, "200", 300.5], "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        )
        donations_df = pd.DataFrame(
            {
                "שקלים": [500, "600", 700.25],
                "שם": ["Donor 1", "Donor 2", "Donor 3"],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        almanot_df = pd.DataFrame({"שם": ["Widow 1", "Widow 2"], "סכום חודשי": [1000, "2000.75"]})

        budget_filename = generate_budget_report(expenses_df, donations_df)
        donor_filename = generate_donor_report(donations_df)
        widows_filename = generate_widows_report(almanot_df)

        assert isinstance(budget_filename, str)
        assert isinstance(donor_filename, str)
        assert isinstance(widows_filename, str)
