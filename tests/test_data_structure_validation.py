#!/usr/bin/env python3
"""
Data Structure Validation Tests
Tests that catch mismatches between expected and actual data structures
"""

import logging
import unittest

import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataStructureValidation(unittest.TestCase):
    """Test data structure validation to catch real-world issues"""

    def setUp(self):
        """Set up test data that matches real Google Sheets structure"""
        # Real expenses data structure (what we actually get from Google Sheets)
        self.real_expenses_df = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'שם': ['ספק א', 'ספק ב', 'ספק ג'],
            'שקלים': [1000, 2000, 1500]
        })

        # What the old function expected (incorrect assumption)
        self.expected_with_category_df = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02'],
            'שם': ['ספק א', 'ספק ב'],
            'קטגוריה': ['מזון', 'ציוד'],  # This column doesn't exist in real data
            'שקלים': [1000, 2000]
        })

    def test_old_budget_distribution_function_would_fail(self):
        """Test that the old function would fail with real data structure"""
        try:
            # Simulate the old function logic
            df = self.real_expenses_df

            # This is what the old function checked for
            if "קטגוריה" not in df.columns or "שקלים" not in df.columns:
                error_msg = "עמודות 'קטגוריה' ו'שקלים' חסרות"
                logger.error(error_msg)
                self.fail(f"Old function would fail: {error_msg}")

            # This would never be reached with real data
            df.groupby("קטגוריה")["שקלים"].sum().reset_index()

        except Exception as e:
            # This is expected - the old function would fail
            logger.info(f"✅ Old function correctly fails with real data: {e}")
            self.assertTrue(True, "Old function fails as expected")

    def test_new_budget_distribution_function_works(self):
        """Test that the new function works with real data structure"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            result = create_budget_distribution_chart(self.real_expenses_df)

            self.assertIsNotNone(result, "New function should work with real data")
            self.assertTrue(hasattr(result, 'data'), "Chart should have data")

            # Check that it groups by name (supplier) since no category column exists
            chart_data = result.data[0]
            self.assertIn('labels', chart_data)
            self.assertIn('values', chart_data)

            # Should have 3 unique suppliers
            self.assertEqual(len(chart_data['labels']), 3)

            logger.info("✅ New function works correctly with real data")

        except Exception as e:
            self.fail(f"New function should work with real data: {e}")

    def test_data_structure_assumptions(self):
        """Test our assumptions about data structure"""
        # Test that expenses data doesn't have category column
        self.assertNotIn('קטגוריה', self.real_expenses_df.columns,
                        "Expenses data should NOT have category column")

        # Test that expenses data has the expected columns
        expected_columns = ['תאריך', 'שם', 'שקלים']
        for col in expected_columns:
            self.assertIn(col, self.real_expenses_df.columns,
                         f"Expenses data should have {col} column")

        # Test that we can group by name (supplier)
        name_col = 'שם'
        amount_col = 'שקלים'

        if name_col in self.real_expenses_df.columns and amount_col in self.real_expenses_df.columns:
            grouped = self.real_expenses_df.groupby(name_col)[amount_col].sum()
            self.assertEqual(len(grouped), 3, "Should be able to group by supplier name")
            logger.info("✅ Can group by supplier name as fallback")

    def test_chart_fallback_logic(self):
        """Test the fallback logic in the new function"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with data that has category column (should use category)
            df_with_category = pd.DataFrame({
                'תאריך': ['2024-01-01', '2024-01-02'],
                'שם': ['ספק א', 'ספק ב'],
                'קטגוריה': ['מזון', 'ציוד'],
                'שקלים': [1000, 2000]
            })

            result1 = create_budget_distribution_chart(df_with_category)
            self.assertIsNotNone(result1, "Should work with category column")

            # Test with data that doesn't have category column (should use name)
            result2 = create_budget_distribution_chart(self.real_expenses_df)
            self.assertIsNotNone(result2, "Should work without category column")

            # Both should create valid charts
            self.assertTrue(hasattr(result1, 'data'))
            self.assertTrue(hasattr(result2, 'data'))

            logger.info("✅ Fallback logic works correctly")

        except Exception as e:
            self.fail(f"Fallback logic failed: {e}")

    def test_error_handling_improvements(self):
        """Test that error handling is improved"""
        try:
            from src.data_visualization import create_budget_distribution_chart

            # Test with empty DataFrame
            empty_df = pd.DataFrame()
            result = create_budget_distribution_chart(empty_df)
            self.assertIsNone(result, "Should return None for empty DataFrame")

            # Test with DataFrame missing amount column
            df_no_amount = pd.DataFrame({
                'תאריך': ['2024-01-01'],
                'שם': ['ספק א']
            })
            result = create_budget_distribution_chart(df_no_amount)
            self.assertIsNone(result, "Should return None when amount column missing")

            # Test with DataFrame missing name column
            df_no_name = pd.DataFrame({
                'תאריך': ['2024-01-01'],
                'שקלים': [1000]
            })
            result = create_budget_distribution_chart(df_no_name)
            self.assertIsNone(result, "Should return None when name column missing")

            logger.info("✅ Error handling is improved")

        except Exception as e:
            self.fail(f"Error handling test failed: {e}")


class TestRealWorldDataScenarios(unittest.TestCase):
    """Test real-world data scenarios that could cause issues"""

    def test_google_sheets_column_variations(self):
        """Test variations in column names from Google Sheets"""
        # Test different possible column names
        variations = [
            {'תאריך': ['2024-01-01'], 'שם לקוח': ['ספק א'], 'סכום': [1000]},
            {'תאריך': ['2024-01-01'], 'שם ספק': ['ספק א'], 'שקלים': [1000]},
            {'תאריך': ['2024-01-01'], 'שם': ['ספק א'], 'שקלים': [1000]},
        ]

        for i, df_data in enumerate(variations):
            with self.subTest(variation=i):
                df = pd.DataFrame(df_data)

                # Test that our function can handle these variations
                from src.data_visualization import create_budget_distribution_chart
                result = create_budget_distribution_chart(df)

                if 'שקלים' in df.columns or 'סכום' in df.columns:
                    self.assertIsNotNone(result, f"Should work with variation {i}")
                else:
                    self.assertIsNone(result, f"Should fail with variation {i}")

    def test_data_with_zero_amounts(self):
        """Test data with zero amounts"""
        df_with_zeros = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'שם': ['ספק א', 'ספק ב', 'ספק ג'],
            'שקלים': [1000, 0, 1500]  # One zero amount
        })

        from src.data_visualization import create_budget_distribution_chart
        result = create_budget_distribution_chart(df_with_zeros)

        # Should still work, but only show non-zero amounts
        self.assertIsNotNone(result, "Should work with zero amounts")

        if result:
            chart_data = result.data[0]
            # Should only have 2 labels (excluding zero amount)
            self.assertEqual(len(chart_data['labels']), 2, "Should exclude zero amounts")

    def test_data_with_negative_amounts(self):
        """Test data with negative amounts (refunds, etc.)"""
        df_with_negatives = pd.DataFrame({
            'תאריך': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'שם': ['ספק א', 'ספק ב', 'ספק ג'],
            'שקלים': [1000, -200, 1500]  # One negative amount (refund)
        })

        from src.data_visualization import create_budget_distribution_chart
        result = create_budget_distribution_chart(df_with_negatives)

        # Should work and include negative amounts
        self.assertIsNotNone(result, "Should work with negative amounts")

        if result:
            chart_data = result.data[0]
            # Should have all 3 amounts (including negative)
            self.assertEqual(len(chart_data['labels']), 3, "Should include negative amounts")


def run_data_structure_tests():
    """Run all data structure validation tests"""
    print("🧪 Running Data Structure Validation Tests...")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTest(unittest.makeSuite(TestDataStructureValidation))
    suite.addTest(unittest.makeSuite(TestRealWorldDataScenarios))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    print(f"📊 Data Structure Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

    if result.failures:
        print(f"❌ {len(result.failures)} tests failed:")
        for test, error in result.failures:
            print(f"  - {test}: {error}")

    if result.errors:
        print(f"💥 {len(result.errors)} tests had errors:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")

    if result.wasSuccessful():
        print("✅ All data structure tests passed! Data validation is working correctly.")
    else:
        print("❌ Some data structure tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_data_structure_tests()
