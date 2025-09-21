#!/usr/bin/env python3
"""
Integration Tests for Omri Association Dashboard
Tests the complete data flow from Google Sheets to UI components
"""

import logging
import unittest

import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataFlowIntegration(unittest.TestCase):
    """Test complete data flow integration"""

    def setUp(self):
        """Set up test data that matches real Google Sheets structure"""
        # Real expenses data structure (no category column)
        self.expenses_df = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'שם': ['ספק א', 'ספק ב', 'ספק ג', 'ספק א'],
            'שקלים': [1000, 2000, 1500, 800]
        })

        # Real donations data structure
        self.donations_df = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'שם': ['תורם א', 'תורם ב', 'תורם ג'],
            'שקלים': [5000, 3000, 4000]
        })

        # Real widows data structure
        self.widows_df = pd.DataFrame({
            'שם ': ['אלמנה א', 'אלמנה ב', 'אלמנה ג'],
            'סכום חודשי': [2000, 1500, 3000],
            'מספר ילדים': [2, 1, 3],
            'תורם': ['תורם א', 'תורם ב', 'תורם ג']
        })

        # Real investors data structure
        self.investors_df = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02'],
            'שם': ['משקיע א', 'משקיע ב'],
            'שקלים': [10000, 15000]
        })

    def test_budget_distribution_chart_with_real_data(self):
        """Test budget distribution chart with real data structure"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            result = create_budget_distribution_chart(self.expenses_df)

            self.assertIsNotNone(result, "Budget distribution chart should be created with real data")
            self.assertTrue(hasattr(result, 'data'), "Chart should have data attribute")

            # Check that it groups by name (supplier) since no category column exists
            chart_data = result.data[0]
            self.assertIn('labels', chart_data, "Chart should have labels")
            self.assertIn('values', chart_data, "Chart should have values")

            # Should have 3 unique suppliers
            self.assertEqual(len(chart_data['labels']), 3, "Should group by unique suppliers")

            logger.info("✅ Budget distribution chart works with real data structure")

        except Exception as e:
            self.fail(f"Budget distribution chart failed with real data: {e}")

    def test_monthly_trends_with_real_data(self):
        """Test monthly trends chart with real data"""
        try:
            from src.data_visualization import create_monthly_trends

            result = create_monthly_trends(self.expenses_df, self.donations_df)

            self.assertIsNotNone(result, "Monthly trends chart should be created")
            self.assertTrue(hasattr(result, 'data'), "Chart should have data attribute")

            logger.info("✅ Monthly trends chart works with real data")

        except Exception as e:
            self.fail(f"Monthly trends chart failed with real data: {e}")

    def test_donor_contribution_chart_with_real_data(self):
        """Test donor contribution chart with real data"""
        try:
            from src.data_visualization import create_donor_contribution_chart

            result = create_donor_contribution_chart(self.donations_df)

            self.assertIsNotNone(result, "Donor contribution chart should be created")
            self.assertTrue(hasattr(result, 'data'), "Chart should have data attribute")

            logger.info("✅ Donor contribution chart works with real data")

        except Exception as e:
            self.fail(f"Donor contribution chart failed with real data: {e}")

    def test_widows_support_chart_with_real_data(self):
        """Test widows support chart with real data"""
        try:
            from src.data_visualization import create_widows_support_chart

            result = create_widows_support_chart(self.widows_df)

            self.assertIsNotNone(result, "Widows support chart should be created")
            self.assertTrue(hasattr(result, 'data'), "Chart should have data attribute")

            logger.info("✅ Widows support chart works with real data")

        except Exception as e:
            self.fail(f"Widows support chart failed with real data: {e}")

    def test_data_processing_with_real_data(self):
        """Test data processing functions with real data"""
        try:
            from src.data_processing import (
                calculate_donor_statistics,
                calculate_monthly_budget,
                calculate_widow_statistics,
            )

            # Test donor statistics
            donor_stats = calculate_donor_statistics(self.donations_df)
            self.assertIsInstance(donor_stats, dict)
            self.assertIn('total_donors', donor_stats)
            self.assertIn('total_donations', donor_stats)
            self.assertEqual(donor_stats['total_donors'], 3)
            self.assertEqual(donor_stats['total_donations'], 12000)

            # Test widow statistics
            widow_stats = calculate_widow_statistics(self.widows_df)
            self.assertIsInstance(widow_stats, dict)
            self.assertIn('total_widows', widow_stats)
            self.assertIn('total_support', widow_stats)
            self.assertEqual(widow_stats['total_widows'], 3)
            self.assertEqual(widow_stats['total_support'], 6500)

            # Test monthly budget
            budget_stats = calculate_monthly_budget(self.expenses_df, self.donations_df)
            self.assertIsInstance(budget_stats, dict)
            self.assertIn('total_expenses', budget_stats)
            self.assertIn('total_donations', budget_stats)

            logger.info("✅ Data processing functions work with real data")

        except Exception as e:
            self.fail(f"Data processing failed with real data: {e}")

    def test_dashboard_sections_with_real_data(self):
        """Test dashboard sections with real data"""
        try:
            from ui.dashboard_sections import create_budget_section, create_overview_section

            # Test overview section
            donor_stats = {'total_donors': 3, 'total_donations': 12000}
            widow_stats = {'total_widows': 3, 'total_support': 6500}

            # This should not raise an exception
            create_overview_section(self.expenses_df, self.donations_df, donor_stats, widow_stats)

            # Test budget section
            budget_status = {'total_expenses': 5300, 'total_donations': 12000}
            create_budget_section(self.expenses_df, self.donations_df, budget_status, "test")

            logger.info("✅ Dashboard sections work with real data")

        except Exception as e:
            self.fail(f"Dashboard sections failed with real data: {e}")

    def test_empty_data_handling(self):
        """Test handling of empty DataFrames"""
        try:
            from src.data_visualization import create_budget_distribution_chart, create_monthly_trends

            # Test with empty DataFrame
            empty_df = pd.DataFrame()

            result1 = create_budget_distribution_chart(empty_df)
            self.assertIsNone(result1, "Should return None for empty DataFrame")

            result2 = create_monthly_trends(empty_df, empty_df)
            self.assertIsNone(result2, "Should return None for empty DataFrames")

            logger.info("✅ Empty data handling works correctly")

        except Exception as e:
            self.fail(f"Empty data handling failed: {e}")

    def test_missing_columns_handling(self):
        """Test handling of missing columns"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with DataFrame missing amount column
            df_no_amount = pd.DataFrame({
                'תאריך': ['2024-01-01'],
                'שם': ['ספק א']
                # Missing 'שקלים' column
            })

            result = create_budget_distribution_chart(df_no_amount)
            self.assertIsNone(result, "Should return None when amount column is missing")

            # Test with DataFrame missing name column
            df_no_name = pd.DataFrame({
                'תאריך': ['2024-01-01'],
                'שקלים': [1000]
                # Missing 'שם' column
            })

            result = create_budget_distribution_chart(df_no_name)
            self.assertIsNone(result, "Should return None when name column is missing")

            logger.info("✅ Missing columns handling works correctly")

        except Exception as e:
            self.fail(f"Missing columns handling failed: {e}")

    def test_google_sheets_data_structure(self):
        """Test that our data structure matches what Google Sheets provides"""
        try:
            # Test expenses data structure
            self.assertIn('תאריך', self.expenses_df.columns)
            self.assertIn('שם', self.expenses_df.columns)
            self.assertIn('שקלים', self.expenses_df.columns)
            self.assertNotIn('קטגוריה', self.expenses_df.columns, "Expenses should not have category column")

            # Test donations data structure
            self.assertIn('תאריך', self.donations_df.columns)
            self.assertIn('שם', self.donations_df.columns)
            self.assertIn('שקלים', self.donations_df.columns)

            # Test widows data structure
            self.assertIn('שם ', self.widows_df.columns)
            self.assertIn('סכום חודשי', self.widows_df.columns)
            self.assertIn('מספר ילדים', self.widows_df.columns)

            logger.info("✅ Data structure matches Google Sheets format")

        except Exception as e:
            self.fail(f"Data structure validation failed: {e}")


class TestErrorHandlingIntegration(unittest.TestCase):
    """Test error handling in integration scenarios"""

    def test_chart_creation_with_invalid_data(self):
        """Test chart creation with various invalid data scenarios"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with None
            result = create_budget_distribution_chart(None)
            self.assertIsNone(result)

            # Test with non-DataFrame
            result = create_budget_distribution_chart("not a dataframe")
            self.assertIsNone(result)

            # Test with DataFrame with all zero amounts
            df_zeros = pd.DataFrame({
                'שם': ['ספק א', 'ספק ב'],
                'שקלים': [0, 0]
            })
            result = create_budget_distribution_chart(df_zeros)
            self.assertIsNone(result)

            logger.info("✅ Error handling works correctly")

        except Exception as e:
            self.fail(f"Error handling failed: {e}")


def run_integration_tests():
    """Run all integration tests"""
    print("🧪 Running Integration Tests...")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTest(unittest.makeSuite(TestDataFlowIntegration))
    suite.addTest(unittest.makeSuite(TestErrorHandlingIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    print(f"📊 Integration Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

    if result.failures:
        print(f"❌ {len(result.failures)} tests failed:")
        for test, error in result.failures:
            print(f"  - {test}: {error}")

    if result.errors:
        print(f"💥 {len(result.errors)} tests had errors:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")

    if result.wasSuccessful():
        print("✅ All integration tests passed! Data flow is working correctly.")
    else:
        print("❌ Some integration tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_integration_tests()
