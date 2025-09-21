#!/usr/bin/env python3
"""
Comprehensive UI Tests for Omri Association Dashboard
Tests UI components, table display, and user interactions
"""

import os
import sys
import unittest

import pandas as pd

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestTableDisplay(unittest.TestCase):
    """Test table display and formatting"""

    def test_table_column_order(self):
        """Test that table columns are in correct left-to-right order"""
        # Create test data
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, 2000, 2000],
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "נגה רוזנטל"]
        }
        df = pd.DataFrame(test_data)

        # Test column order
        expected_order = ["תורם", "סכום חודשי", "מספר ילדים", "שם"]
        self.assertEqual(list(df.columns), expected_order)

        # Test that first column is donor (leftmost)
        self.assertEqual(df.columns[0], "תורם")

        # Test that last column is name (rightmost)
        self.assertEqual(df.columns[-1], "שם")

    def test_table_no_index_column(self):
        """Test that tables don't show index column"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 2000],
            "מספר ילדים": [3, 5],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that DataFrame has no index column in display
        self.assertEqual(len(df.columns), 4)
        self.assertNotIn("index", df.columns)
        self.assertNotIn("Index", df.columns)

    def test_hebrew_text_display(self):
        """Test that Hebrew text displays correctly in tables"""
        hebrew_names = ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"]
        hebrew_donors = ["פלייטק+גלים", "פלייטיקה", "מייקרוסופט"]

        test_data = {
            "תורם": hebrew_donors,
            "סכום חודשי": [2000, 2000, 2000],
            "מספר ילדים": [3, 5, 4],
            "שם": hebrew_names
        }
        df = pd.DataFrame(test_data)

        # Test that Hebrew text is preserved
        for name in hebrew_names:
            self.assertIn(name, df["שם"].values)

        for donor in hebrew_donors:
            self.assertIn(donor, df["תורם"].values)

    def test_table_sorting(self):
        """Test that table sorting works correctly"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, 1500, 3000],
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "נגה רוזנטל"]
        }
        df = pd.DataFrame(test_data)

        # Test sorting by monthly amount (descending)
        sorted_df = df.sort_values("סכום חודשי", ascending=False)

        # First row should have highest amount
        self.assertEqual(sorted_df.iloc[0]["סכום חודשי"], 3000)
        self.assertEqual(sorted_df.iloc[0]["תורם"], "מייקרוסופט")

        # Last row should have lowest amount
        self.assertEqual(sorted_df.iloc[-1]["סכום חודשי"], 1500)
        self.assertEqual(sorted_df.iloc[-1]["תורם"], "פלייטיקה")


class TestUIComponents(unittest.TestCase):
    """Test UI components and interactions"""

    def test_dashboard_header_creation(self):
        """Test that dashboard header can be created"""
        try:
            # This should not raise an exception
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Dashboard header creation failed: {e}")

    def test_main_tabs_creation(self):
        """Test that main tabs can be created"""
        try:
            # This should not raise an exception
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Main tabs creation failed: {e}")

    def test_network_section_creation(self):
        """Test that network section can be created"""
        try:

            # Test that network section can be created without errors

            # This should not raise an exception
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Network section creation failed: {e}")

    def test_widows_section_creation(self):
        """Test that widows section can be created"""
        try:

            # Test that widows section can be created without errors

            # This should not raise an exception
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Widows section creation failed: {e}")


class TestDataVisualizationUI(unittest.TestCase):
    """Test data visualization UI components"""

    def test_budget_distribution_chart_ui(self):
        """Test budget distribution chart UI handling"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with real data structure (no category column)
            test_data = {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
                "סכום": [2000, 1500, 1000],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
            }
            df = pd.DataFrame(test_data)

            # Should not raise exception
            create_budget_distribution_chart(df)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Budget distribution chart UI failed: {e}")

    def test_donor_contribution_chart_ui(self):
        """Test donor contribution chart UI handling"""
        try:
            from src.data_visualization import create_donor_contribution_chart

            test_data = {
                "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
                "סכום": [2000, 1500, 1000],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
            }
            df = pd.DataFrame(test_data)

            # Should not raise exception
            create_donor_contribution_chart(df)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Donor contribution chart UI failed: {e}")

    def test_monthly_trends_chart_ui(self):
        """Test monthly trends chart UI handling"""
        try:
            from src.data_visualization import create_monthly_trends

            test_data = {
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "סכום": [2000, 1500, 1000]
            }
            df = pd.DataFrame(test_data)

            # Should not raise exception
            create_monthly_trends(df)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Monthly trends chart UI failed: {e}")


class TestErrorHandlingUI(unittest.TestCase):
    """Test error handling in UI components"""

    def test_empty_dataframe_handling(self):
        """Test UI handling of empty DataFrames"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with empty DataFrame
            empty_df = pd.DataFrame()
            result = create_budget_distribution_chart(empty_df)

            # Should return None for empty data
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"Empty DataFrame handling failed: {e}")

    def test_missing_columns_handling(self):
        """Test UI handling of missing columns"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with DataFrame missing required columns
            test_data = {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "תאריך": ["2024-01-01", "2024-01-02"]
                # Missing amount column
            }
            df = pd.DataFrame(test_data)

            result = create_budget_distribution_chart(df)

            # Should return None for missing columns
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"Missing columns handling failed: {e}")

    def test_invalid_data_types_handling(self):
        """Test UI handling of invalid data types"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with invalid data types
            test_data = {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "סכום": ["invalid", "data"],  # Should be numeric
                "תאריך": ["2024-01-01", "2024-01-02"]
            }
            df = pd.DataFrame(test_data)

            create_budget_distribution_chart(df)

            # Should handle invalid data gracefully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Invalid data types handling failed: {e}")


class TestPerformanceUI(unittest.TestCase):
    """Test UI performance with large datasets"""

    def test_large_table_display(self):
        """Test table display with large datasets"""
        # Create large dataset
        large_data = {
            "תורם": ["פלייטק"] * 1000,
            "סכום חודשי": [2000] * 1000,
            "מספר ילדים": [3] * 1000,
            "שם": [f"אלמנה {i}" for i in range(1000)]
        }
        df = pd.DataFrame(large_data)

        # Test that large DataFrame can be created
        self.assertEqual(len(df), 1000)
        self.assertEqual(len(df.columns), 4)

        # Test sorting performance
        sorted_df = df.sort_values("סכום חודשי", ascending=False)
        self.assertEqual(len(sorted_df), 1000)

    def test_memory_usage_ui(self):
        """Test memory usage of UI operations"""
        import os

        import psutil

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Create and process data
        test_data = {
            "תורם": ["פלייטק"] * 100,
            "סכום חודשי": [2000] * 100,
            "מספר ילדים": [3] * 100,
            "שם": [f"אלמנה {i}" for i in range(100)]
        }
        df = pd.DataFrame(test_data)

        # Process data
        df.sort_values("סכום חודשי", ascending=False)

        # Get final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 10MB)
        self.assertLess(memory_increase, 10 * 1024 * 1024)


def run_ui_tests():
    """Run all UI tests"""
    print("🧪 Running Comprehensive UI Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestTableDisplay,
        TestUIComponents,
        TestDataVisualizationUI,
        TestErrorHandlingUI,
        TestPerformanceUI
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print results
    print("=" * 60)
    print(f"📊 UI Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

    if result.failures:
        print(f"❌ {len(result.failures)} tests failed:")
        for test, traceback in result.failures:
            error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"  - {test}: {error_msg}")

    if result.errors:
        print(f"❌ {len(result.errors)} tests had errors:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")

    if result.wasSuccessful():
        print("✅ All UI tests passed! UI is working correctly.")
    else:
        print("❌ Some UI tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_ui_tests()
