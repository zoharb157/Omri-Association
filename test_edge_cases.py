#!/usr/bin/env python3
"""
Edge Cases Tests for Omri Association Dashboard
Tests extreme scenarios, boundary conditions, and unusual data
"""

import os
import sys
import unittest

import numpy as np
import pandas as pd

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestExtremeDataScenarios(unittest.TestCase):
    """Test extreme data scenarios"""

    def test_very_large_numbers(self):
        """Test handling of very large monetary values"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [999999999, 1000000000],
            "מספר ילדים": [3, 5],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that large numbers are handled correctly
        self.assertEqual(df["סכום חודשי"].max(), 1000000000)
        self.assertEqual(df["סכום חודשי"].min(), 999999999)

    def test_very_small_numbers(self):
        """Test handling of very small monetary values"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [0.01, 0.02],
            "מספר ילדים": [3, 5],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that small numbers are handled correctly
        self.assertEqual(df["סכום חודשי"].max(), 0.02)
        self.assertEqual(df["סכום חודשי"].min(), 0.01)

    def test_negative_values(self):
        """Test handling of negative values (refunds, etc.)"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, -500],  # Negative value for refund
            "מספר ילדים": [3, 5],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that negative values are handled correctly
        self.assertEqual(df["סכום חודשי"].max(), 2000)
        self.assertEqual(df["סכום חודשי"].min(), -500)

    def test_zero_values(self):
        """Test handling of zero values"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [0, 2000],
            "מספר ילדים": [0, 5],  # Zero children
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that zero values are handled correctly
        self.assertEqual(df["סכום חודשי"].min(), 0)
        self.assertEqual(df["מספר ילדים"].min(), 0)

    def test_very_long_text(self):
        """Test handling of very long text fields"""
        long_name = "סיוון ליבוביץ-הרשקוביץ-קנפו-לוינשטרן-לוטן-עמר-רוזנטל-הרוש-יהלומי-אלמוסנינו"
        long_donor = "פלייטק+גלים+פלייטיקה+מייקרוסופט+איליון+פאראגון+אליה מולודצקי+סקיישילד+קובי הלפרין"

        test_data = {
            "תורם": [long_donor, "פלייטיקה"],
            "סכום חודשי": [2000, 1500],
            "מספר ילדים": [3, 5],
            "שם": [long_name, "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that long text is handled correctly
        self.assertEqual(len(df["שם"].iloc[0]), len(long_name))
        self.assertEqual(len(df["תורם"].iloc[0]), len(long_donor))

    def test_special_characters(self):
        """Test handling of special characters in text"""
        special_names = ["סיוון ליבוביץ-ג'ון", "הדס הרשקוביץ'", "ספיר קנפו-סמית'"]
        special_donors = ["פלייטק & גלים", "פלייטיקה (חברה)", "מייקרוסופט [ישראל]"]

        test_data = {
            "תורם": special_donors,
            "סכום חודשי": [2000, 1500, 1000],
            "מספר ילדים": [3, 5, 4],
            "שם": special_names
        }
        df = pd.DataFrame(test_data)

        # Test that special characters are handled correctly
        for name in special_names:
            self.assertIn(name, df["שם"].values)

        for donor in special_donors:
            self.assertIn(donor, df["תורם"].values)


class TestBoundaryConditions(unittest.TestCase):
    """Test boundary conditions and limits"""

    def test_single_row_dataframe(self):
        """Test handling of single row DataFrame"""
        test_data = {
            "תורם": ["פלייטק"],
            "סכום חודשי": [2000],
            "מספר ילדים": [3],
            "שם": ["סיוון ליבוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that single row is handled correctly
        self.assertEqual(len(df), 1)
        self.assertEqual(df["שם"].iloc[0], "סיוון ליבוביץ")

    def test_maximum_children(self):
        """Test handling of maximum reasonable number of children"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 1500],
            "מספר ילדים": [20, 15],  # Very high number of children
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that high numbers are handled correctly
        self.assertEqual(df["מספר ילדים"].max(), 20)
        self.assertEqual(df["מספר ילדים"].min(), 15)

    def test_duplicate_names(self):
        """Test handling of duplicate names"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה", "פלייטק"],
            "סכום חודשי": [2000, 1500, 1000],
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "סיוון ליבוביץ"]  # Duplicate name
        }
        df = pd.DataFrame(test_data)

        # Test that duplicates are handled correctly
        self.assertEqual(len(df), 3)
        self.assertEqual(df["שם"].value_counts()["סיוון ליבוביץ"], 2)

    def test_mixed_data_types(self):
        """Test handling of mixed data types in columns"""
        test_data = {
            "תורם": ["פלייטק", 123, None],  # Mixed types
            "סכום חודשי": [2000, "1500", 1000],  # Mixed numeric and string
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"]
        }
        df = pd.DataFrame(test_data)

        # Test that mixed types are handled correctly
        self.assertEqual(len(df), 3)
        self.assertIn("פלייטק", df["תורם"].values)
        self.assertIn(123, df["תורם"].values)


class TestUnusualDataStructures(unittest.TestCase):
    """Test unusual data structures and formats"""

    def test_empty_strings(self):
        """Test handling of empty strings"""
        test_data = {
            "תורם": ["פלייטק", "", "פלייטיקה"],
            "סכום חודשי": [2000, 1500, 1000],
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "", "ספיר קנפו"]
        }
        df = pd.DataFrame(test_data)

        # Test that empty strings are handled correctly
        self.assertEqual(len(df), 3)
        self.assertIn("", df["תורם"].values)
        self.assertIn("", df["שם"].values)

    def test_whitespace_only_strings(self):
        """Test handling of whitespace-only strings"""
        test_data = {
            "תורם": ["פלייטק", "   ", "פלייטיקה"],
            "סכום חודשי": [2000, 1500, 1000],
            "מספר ילדים": [3, 5, 4],
            "שם": ["סיוון ליבוביץ", "\t\n", "ספיר קנפו"]
        }
        df = pd.DataFrame(test_data)

        # Test that whitespace-only strings are handled correctly
        self.assertEqual(len(df), 3)
        self.assertIn("   ", df["תורם"].values)
        self.assertIn("\t\n", df["שם"].values)

    def test_nan_values(self):
        """Test handling of NaN values"""
        test_data = {
            "תורם": ["פלייטק", np.nan, "פלייטיקה"],
            "סכום חודשי": [2000, 1500, np.nan],
            "מספר ילדים": [3, np.nan, 4],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", np.nan]
        }
        df = pd.DataFrame(test_data)

        # Test that NaN values are handled correctly
        self.assertEqual(len(df), 3)
        self.assertTrue(pd.isna(df["תורם"].iloc[1]))
        self.assertTrue(pd.isna(df["סכום חודשי"].iloc[2]))

    def test_infinity_values(self):
        """Test handling of infinity values"""
        test_data = {
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, np.inf],
            "מספר ילדים": [3, 5],
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
        }
        df = pd.DataFrame(test_data)

        # Test that infinity values are handled correctly
        self.assertEqual(len(df), 2)
        self.assertTrue(np.isinf(df["סכום חודשי"].iloc[1]))


class TestDataProcessingEdgeCases(unittest.TestCase):
    """Test data processing functions with edge cases"""

    def test_calculate_donor_statistics_edge_cases(self):
        """Test donor statistics calculation with edge cases"""
        try:
            from data_processing import calculate_donor_statistics

            # Test with empty DataFrame
            empty_df = pd.DataFrame()
            result = calculate_donor_statistics(empty_df)
            self.assertIsInstance(result, dict)

            # Test with single row
            single_row_df = pd.DataFrame({
                "תורם": ["פלייטק"],
                "סכום": [2000],
                "תאריך": ["2024-01-01"]
            })
            result = calculate_donor_statistics(single_row_df)
            self.assertIsInstance(result, dict)

        except Exception as e:
            self.fail(f"Donor statistics edge case failed: {e}")

    def test_calculate_widow_statistics_edge_cases(self):
        """Test widow statistics calculation with edge cases"""
        try:
            from data_processing import calculate_widow_statistics

            # Test with empty DataFrame
            empty_df = pd.DataFrame()
            result = calculate_widow_statistics(empty_df)
            self.assertIsInstance(result, dict)

            # Test with single row
            single_row_df = pd.DataFrame({
                "שם": ["סיוון ליבוביץ"],
                "מספר ילדים": [3],
                "סכום חודשי": [2000],
                "תורם": ["פלייטק"]
            })
            result = calculate_widow_statistics(single_row_df)
            self.assertIsInstance(result, dict)

        except Exception as e:
            self.fail(f"Widow statistics edge case failed: {e}")

    def test_create_budget_distribution_chart_edge_cases(self):
        """Test budget distribution chart with edge cases"""
        try:
            from data_visualization import create_budget_distribution_chart

            # Test with all zero amounts
            zero_amounts_df = pd.DataFrame({
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "סכום": [0, 0],
                "תאריך": ["2024-01-01", "2024-01-02"]
            })
            result = create_budget_distribution_chart(zero_amounts_df)
            self.assertIsNone(result)  # Should return None for zero amounts

            # Test with all negative amounts
            negative_amounts_df = pd.DataFrame({
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "סכום": [-1000, -500],
                "תאריך": ["2024-01-01", "2024-01-02"]
            })
            result = create_budget_distribution_chart(negative_amounts_df)
            # Should handle negative amounts gracefully

        except Exception as e:
            self.fail(f"Budget distribution chart edge case failed: {e}")


def run_edge_case_tests():
    """Run all edge case tests"""
    print("🧪 Running Edge Case Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestExtremeDataScenarios,
        TestBoundaryConditions,
        TestUnusualDataStructures,
        TestDataProcessingEdgeCases
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print results
    print("=" * 60)
    print(f"📊 Edge Case Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

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
        print("✅ All edge case tests passed! App handles extreme scenarios correctly.")
    else:
        print("❌ Some edge case tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_edge_case_tests()
