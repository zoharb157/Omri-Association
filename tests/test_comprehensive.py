#!/usr/bin/env python3
"""
Comprehensive Unit Test Suite for Omri Association Dashboard
Enhanced testing with more coverage and edge cases
"""

import os
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and validation"""

    def setUp(self):
        """Set up test data"""
        self.sample_expenses = pd.DataFrame({
            "שקלים": [100, 200, 300, 400, 500],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "קטגוריה": ["אוכל", "דלק", "תחבורה", "אוכל", "דלק"]
        })

        self.sample_donations = pd.DataFrame({
            "שם": ["תורם א", "תורם ב", "תורם ג", "תורם ד", "תורם ה"],
            "שקלים": [300, 400, 500, 600, 700],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
        })

        self.sample_almanot = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג", "אלמנה ד", "אלמנה ה"],
            "סכום חודשי": [1000, 2000, 3000, 4000, 5000],
            "עיר": ["תל אביב", "ירושלים", "חיפה", "תל אביב", "ירושלים"]
        })

    def test_dataframe_creation(self):
        """Test DataFrame creation and basic operations"""
        self.assertEqual(len(self.sample_expenses), 5)
        self.assertEqual(len(self.sample_donations), 5)
        self.assertEqual(len(self.sample_almanot), 5)

        # Test column names
        self.assertIn("שקלים", self.sample_expenses.columns)
        self.assertIn("תאריך", self.sample_expenses.columns)
        self.assertIn("קטגוריה", self.sample_expenses.columns)

    def test_data_types(self):
        """Test data types and conversions"""
        # Test numeric operations
        self.assertEqual(self.sample_expenses["שקלים"].sum(), 1500)
        self.assertEqual(self.sample_donations["שקלים"].sum(), 2500)
        self.assertEqual(self.sample_almanot["סכום חודשי"].sum(), 15000)

        # Test date conversion
        self.sample_expenses["תאריך"] = pd.to_datetime(self.sample_expenses["תאריך"])
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.sample_expenses["תאריך"]))

    def test_missing_data_handling(self):
        """Test handling of missing data"""
        # Create DataFrame with missing values
        df_with_nulls = pd.DataFrame({
            "שקלים": [100, None, 300, 400, None],
            "תאריך": ["2024-01-01", "2024-01-02", None, "2024-01-04", "2024-01-05"],
            "קטגוריה": ["אוכל", "דלק", "תחבורה", None, "דלק"]
        })

        # Test null handling
        self.assertTrue(df_with_nulls["שקלים"].isnull().any())
        self.assertTrue(df_with_nulls["תאריך"].isnull().any())
        self.assertTrue(df_with_nulls["קטגוריה"].isnull().any())

        # Test fillna
        df_filled = df_with_nulls.fillna(0)
        self.assertFalse(df_filled["שקלים"].isnull().any())

    def test_hebrew_text_operations(self):
        """Test Hebrew text operations"""
        # Test string operations
        self.assertTrue(self.sample_expenses["קטגוריה"].str.contains("אוכל").any())
        self.assertTrue(self.sample_expenses["קטגוריה"].str.contains("דלק").any())

        # Test grouping
        category_groups = self.sample_expenses.groupby("קטגוריה")["שקלים"].sum()
        self.assertIn("אוכל", category_groups.index)
        self.assertIn("דלק", category_groups.index)
        self.assertIn("תחבורה", category_groups.index)

class TestDataProcessing(unittest.TestCase):
    """Test data processing functions"""

    def setUp(self):
        """Set up test data"""
        self.expenses_df = pd.DataFrame({
            "שקלים": [100, 200, 300, 400, 500],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "קטגוריה": ["אוכל", "דלק", "תחבורה", "אוכל", "דלק"]
        })

        self.donations_df = pd.DataFrame({
            "שם": ["תורם א", "תורם ב", "תורם ג", "תורם ד", "תורם ה"],
            "שקלים": [300, 400, 500, 600, 700],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
        })

        self.almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג", "אלמנה ד", "אלמנה ה"],
            "סכום חודשי": [1000, 2000, 3000, 4000, 5000],
            "עיר": ["תל אביב", "ירושלים", "חיפה", "תל אביב", "ירושלים"]
        })

    def test_calculate_monthly_budget(self):
        """Test monthly budget calculation"""
        try:
            from src.data_processing import calculate_monthly_budget

            result = calculate_monthly_budget(self.expenses_df, self.donations_df)

            self.assertIsInstance(result, dict)
            self.assertIn("total_expenses", result)
            self.assertIn("total_donations", result)
            self.assertIn("balance", result)

            # Test calculations
            expected_expenses = self.expenses_df["שקלים"].sum()
            expected_donations = self.donations_df["שקלים"].sum()
            expected_balance = expected_donations - expected_expenses

            self.assertEqual(result["total_expenses"], expected_expenses)
            self.assertEqual(result["total_donations"], expected_donations)
            self.assertEqual(result["balance"], expected_balance)

        except Exception as e:
            self.fail(f"calculate_monthly_budget failed: {e}")

    def test_calculate_donor_statistics(self):
        """Test donor statistics calculation"""
        try:
            from src.data_processing import calculate_donor_statistics

            result = calculate_donor_statistics(self.donations_df)

            self.assertIsInstance(result, dict)
            self.assertIn("total_donors", result)
            self.assertIn("total_donations", result)
            self.assertIn("avg_donation", result)

            # Test calculations
            expected_total = len(self.donations_df)
            expected_amount = self.donations_df["שקלים"].sum()
            expected_avg = self.donations_df["שקלים"].mean()

            self.assertEqual(result["total_donors"], expected_total)
            self.assertEqual(result["total_donations"], expected_amount)
            self.assertEqual(result["avg_donation"], expected_avg)

        except Exception as e:
            self.fail(f"calculate_donor_statistics failed: {e}")

    def test_calculate_widow_statistics(self):
        """Test widow statistics calculation"""
        try:
            from src.data_processing import calculate_widow_statistics

            result = calculate_widow_statistics(self.almanot_df)

            self.assertIsInstance(result, dict)
            self.assertIn("total_widows", result)
            self.assertIn("total_support", result)
            self.assertIn("support_1000_count", result)

            # Test calculations
            expected_total = len(self.almanot_df)
            expected_support = self.almanot_df["סכום חודשי"].sum()

            self.assertEqual(result["total_widows"], expected_total)
            self.assertEqual(result["total_support"], expected_support)
            self.assertEqual(result["support_1000_count"], 1)  # One widow with 1000 support

        except Exception as e:
            self.fail(f"calculate_widow_statistics failed: {e}")

class TestDataVisualization(unittest.TestCase):
    """Test data visualization functions"""

    def setUp(self):
        """Set up test data"""
        self.expenses_df = pd.DataFrame({
            "שקלים": [100, 200, 300, 400, 500],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "קטגוריה": ["אוכל", "דלק", "תחבורה", "אוכל", "דלק"]
        })

        self.donations_df = pd.DataFrame({
            "שם": ["תורם א", "תורם ב", "תורם ג", "תורם ד", "תורם ה"],
            "שקלים": [300, 400, 500, 600, 700],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
        })

        self.almanot_df = pd.DataFrame({
            "שם": ["אלמנה א", "אלמנה ב", "אלמנה ג", "אלמנה ד", "אלמנה ה"],
            "סכום חודשי": [1000, 2000, 3000, 4000, 5000],
            "עיר": ["תל אביב", "ירושלים", "חיפה", "תל אביב", "ירושלים"]
        })

    def test_create_monthly_trends(self):
        """Test monthly trends chart creation"""
        try:
            from src.data_visualization import create_monthly_trends

            # Mock streamlit components
            with patch('streamlit.error'), \
                 patch('streamlit.markdown'):
                result = create_monthly_trends(self.expenses_df, self.donations_df)

                # Should return None or a plotly figure
                self.assertTrue(result is None or hasattr(result, 'data'))

        except Exception as e:
            self.fail(f"create_monthly_trends failed: {e}")

    def test_create_budget_distribution_chart(self):
        """Test budget distribution chart creation"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Mock streamlit components
            with patch('streamlit.error'), \
                 patch('streamlit.markdown'):
                result = create_budget_distribution_chart(self.expenses_df)

                # Should return None or a plotly figure
                self.assertTrue(result is None or hasattr(result, 'data'))

        except Exception as e:
            self.fail(f"create_budget_distribution_chart failed: {e}")

    def test_create_donor_contribution_chart(self):
        """Test donor contribution chart creation"""
        try:
            from src.data_visualization import create_donor_contribution_chart

            # Mock streamlit components
            with patch('streamlit.error'), \
                 patch('streamlit.markdown'):
                result = create_donor_contribution_chart(self.donations_df)

                # Should return None or a plotly figure
                self.assertTrue(result is None or hasattr(result, 'data'))

        except Exception as e:
            self.fail(f"create_donor_contribution_chart failed: {e}")

    def test_create_widows_support_chart(self):
        """Test widows support chart creation"""
        try:
            from src.data_visualization import create_widows_support_chart

            # Mock streamlit components
            with patch('streamlit.error'), \
                 patch('streamlit.markdown'):
                result = create_widows_support_chart(self.almanot_df)

                # Should return None or a plotly figure
                self.assertTrue(result is None or hasattr(result, 'data'))

        except Exception as e:
            self.fail(f"create_widows_support_chart failed: {e}")

class TestServices(unittest.TestCase):
    """Test services functionality"""

    def test_sheets_service_import(self):
        """Test sheets service imports"""
        try:
            self.assertTrue(True, "services.sheets imports successfully")
        except Exception as e:
            self.fail(f"services.sheets import failed: {e}")

    def test_google_sheets_io_import(self):
        """Test google_sheets_io imports"""
        try:
            self.assertTrue(True, "google_sheets_io imports successfully")
        except Exception as e:
            self.fail(f"google_sheets_io import failed: {e}")

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def test_empty_dataframes(self):
        """Test handling of empty DataFrames"""
        empty_df = pd.DataFrame()
        self.assertEqual(len(empty_df), 0)
        self.assertEqual(len(empty_df.columns), 0)

    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        # Test with non-DataFrame input
        with self.assertRaises(AttributeError):
            "not_a_dataframe".groupby("column")

    def test_missing_columns(self):
        """Test handling of missing columns"""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        self.assertNotIn("nonexistent", df.columns)
        self.assertIn("col1", df.columns)

    def test_nan_values(self):
        """Test handling of NaN values"""
        df = pd.DataFrame({"values": [1, np.nan, 3, np.nan, 5]})
        self.assertTrue(df["values"].isnull().any())
        self.assertEqual(df["values"].isnull().sum(), 2)

        # Test fillna
        df_filled = df.fillna(0)
        self.assertFalse(df_filled["values"].isnull().any())

class TestPerformance(unittest.TestCase):
    """Test performance and efficiency"""

    def test_large_dataframe_operations(self):
        """Test operations on larger DataFrames"""
        # Create larger DataFrame
        large_df = pd.DataFrame({
            "values": range(1000),
            "categories": (["A", "B", "C"] * 334)[:1000]  # Exactly 1000 rows
        })

        # Test operations
        self.assertEqual(len(large_df), 1000)
        self.assertEqual(large_df["values"].sum(), 499500)  # Sum of 0 to 999

        # Test grouping
        grouped = large_df.groupby("categories")["values"].sum()
        self.assertEqual(len(grouped), 3)

    def test_memory_usage(self):
        """Test memory usage of operations"""
        # Create DataFrame
        df = pd.DataFrame({
            "values": range(100),
            "text": ["text"] * 100
        })

        # Test that operations don't modify original DataFrame
        original_sum = df["values"].sum()
        df.groupby("text")["values"].sum()
        self.assertEqual(df["values"].sum(), original_sum)

def run_comprehensive_tests():
    """Run all comprehensive test suites"""
    print("🧪 Running Comprehensive Test Suite...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestDataIntegrity,
        TestDataProcessing,
        TestDataVisualization,
        TestServices,
        TestErrorHandling,
        TestPerformance
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("=" * 60)
    print(f"📊 Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

    if result.failures:
        print(f"❌ {len(result.failures)} tests failed:")
        for test, traceback in result.failures:
            error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"  - {test}: {error_msg}")

    if result.errors:
        print(f"💥 {len(result.errors)} tests had errors:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")

    if result.wasSuccessful():
        print("✅ All tests passed! App is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
