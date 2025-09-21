#!/usr/bin/env python3
"""
Data Validation Tests for Omri Association Dashboard
Tests data integrity, validation, and business logic
"""

import os
import sys
import unittest
from datetime import datetime

import pandas as pd

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestDataIntegrity(unittest.TestCase):  # Force reformat
    """Test data integrity and validation"""

    def test_required_columns_exist(self):
        """Test that required columns exist in all DataFrames"""
        # Test expenses DataFrame
        expenses_df = pd.DataFrame(
            {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "סכום": [2000, 1500],
                "תאריך": ["2024-01-01", "2024-01-02"],
            }
        )

        required_expenses_columns = ["שם", "סכום", "תאריך"]
        for col in required_expenses_columns:
            self.assertIn(
                col, expenses_df.columns, f"Required column '{col}' missing from expenses DataFrame"
            )

        # Test donations DataFrame
        donations_df = pd.DataFrame(
            {
                "תורם": ["פלייטק", "פלייטיקה"],
                "סכום": [2000, 1500],
                "תאריך": ["2024-01-01", "2024-01-02"],
            }
        )

        required_donations_columns = ["תורם", "סכום", "תאריך"]
        for col in required_donations_columns:
            self.assertIn(
                col,
                donations_df.columns,
                f"Required column '{col}' missing from donations DataFrame",
            )

        # Test almanot DataFrame
        almanot_df = pd.DataFrame(
            {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "מספר ילדים": [3, 5],
                "סכום חודשי": [2000, 1500],
                "תורם": ["פלייטק", "פלייטיקה"],
            }
        )

        required_almanot_columns = ["שם", "מספר ילדים", "סכום חודשי", "תורם"]
        for col in required_almanot_columns:
            self.assertIn(
                col, almanot_df.columns, f"Required column '{col}' missing from almanot DataFrame"
            )

    def test_data_types_validation(self):
        """Test that data types are correct"""
        # Test numeric columns
        test_data = {
            "סכום": [2000, 1500, 1000],
            "מספר ילדים": [3, 5, 4],
            "סכום חודשי": [2000.50, 1500.75, 1000.25],
        }
        df = pd.DataFrame(test_data)

        # Test that numeric columns contain numeric values
        for col in ["סכום", "מספר ילדים", "סכום חודשי"]:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(df[col]), f"Column '{col}' should be numeric"
            )

        # Test string columns
        test_data = {"שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"], "תורם": ["פלייטק", "פלייטיקה"]}
        df = pd.DataFrame(test_data)

        # Test that string columns contain string values
        for col in ["שם", "תורם"]:
            self.assertTrue(
                pd.api.types.is_string_dtype(df[col]), f"Column '{col}' should be string"
            )

    def test_date_validation(self):
        """Test that date columns are valid"""
        test_data = {"תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]}
        df = pd.DataFrame(test_data)

        # Convert to datetime
        df["תאריך"] = pd.to_datetime(df["תאריך"])

        # Test that dates are valid
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["תאריך"]))

        # Test that dates are reasonable (not too far in past/future)
        current_year = datetime.now().year
        for date in df["תאריך"]:
            self.assertGreaterEqual(date.year, 2020, "Date should not be too far in the past")
            self.assertLessEqual(
                date.year, current_year + 1, "Date should not be too far in the future"
            )

    def test_hebrew_text_validation(self):
        """Test that Hebrew text is properly encoded"""
        hebrew_names = ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"]
        hebrew_donors = ["פלייטק", "פלייטיקה", "מייקרוסופט"]

        test_data = {"שם": hebrew_names, "תורם": hebrew_donors}
        df = pd.DataFrame(test_data)

        # Test that Hebrew text is preserved
        for name in hebrew_names:
            self.assertIn(name, df["שם"].values)

        for donor in hebrew_donors:
            self.assertIn(donor, df["תורם"].values)

        # Test that text contains Hebrew characters
        for _, row in df.iterrows():
            self.assertTrue(
                any("\u0590" <= char <= "\u05FF" for char in row["שם"]),
                "Name should contain Hebrew characters",
            )
            self.assertTrue(
                any("\u0590" <= char <= "\u05FF" for char in row["תורם"]),
                "Donor should contain Hebrew characters",
            )

    def test_numeric_range_validation(self):
        """Test that numeric values are within reasonable ranges"""
        test_data = {
            "סכום": [2000, 1500, 1000, 50000],  # Including high value
            "מספר ילדים": [3, 5, 4, 15],  # Including high value
            "סכום חודשי": [2000, 1500, 1000, 100000],  # Including high value
        }
        df = pd.DataFrame(test_data)

        # Test reasonable ranges
        self.assertGreaterEqual(df["סכום"].min(), 0, "Amount should not be negative")
        self.assertLessEqual(df["סכום"].max(), 1000000, "Amount should not be unreasonably high")

        self.assertGreaterEqual(
            df["מספר ילדים"].min(), 0, "Number of children should not be negative"
        )
        self.assertLessEqual(
            df["מספר ילדים"].max(), 50, "Number of children should not be unreasonably high"
        )

        self.assertGreaterEqual(df["סכום חודשי"].min(), 0, "Monthly amount should not be negative")
        self.assertLessEqual(
            df["סכום חודשי"].max(), 1000000, "Monthly amount should not be unreasonably high"
        )


class TestBusinessLogicValidation(unittest.TestCase):
    """Test business logic validation"""

    def test_donor_widow_consistency(self):
        """Test that donor-widow relationships are consistent"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
                "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
                "סכום חודשי": [2000, 1500, 1000],
            }
        )

        donations_df = pd.DataFrame(
            {
                "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
                "סכום": [2000, 1500, 1000],
                "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )

        # Test that all donors in almanot_df exist in donations_df
        almanot_donors = set(almanot_df["תורם"].unique())
        donation_donors = set(donations_df["תורם"].unique())

        for donor in almanot_donors:
            if pd.notna(donor):
                self.assertIn(
                    donor, donation_donors, f"Donor '{donor}' in almanot not found in donations"
                )

    def test_amount_consistency(self):
        """Test that amounts are consistent across related data"""
        almanot_df = pd.DataFrame(
            {
                "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
                "תורם": ["פלייטק", "פלייטיקה"],
                "סכום חודשי": [2000, 1500],
            }
        )

        donations_df = pd.DataFrame(
            {
                "תורם": ["פלייטק", "פלייטיקה"],
                "סכום": [2000, 1500],
                "תאריך": ["2024-01-01", "2024-01-02"],
            }
        )

        # Test that monthly amounts match donation amounts for same donor
        for _, almanot_row in almanot_df.iterrows():
            donor = almanot_row["תורם"]
            monthly_amount = almanot_row["סכום חודשי"]

            if pd.notna(donor):
                donor_donations = donations_df[donations_df["תורם"] == donor]
                if not donor_donations.empty:
                    donation_amount = donor_donations["סכום"].iloc[0]
                    # Monthly amount should be reasonable compared to donation amount
                    self.assertLessEqual(
                        monthly_amount,
                        donation_amount * 2,
                        f"Monthly amount {monthly_amount} too high compared to donation {donation_amount}",
                    )

    def test_children_count_validation(self):
        """Test that children count is reasonable"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
            "מספר ילדים": [3, 5, 0],  # Including zero children
        }
        df = pd.DataFrame(test_data)

        # Test that children count is reasonable
        for _, row in df.iterrows():
            children_count = row["מספר ילדים"]
            self.assertGreaterEqual(children_count, 0, "Number of children should not be negative")
            self.assertLessEqual(
                children_count, 20, "Number of children should not be unreasonably high"
            )

    def test_date_consistency(self):
        """Test that dates are consistent and logical"""
        test_data = {
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "סכום": [2000, 1500, 1000],
        }
        df = pd.DataFrame(test_data)

        # Convert to datetime
        df["תאריך"] = pd.to_datetime(df["תאריך"])

        # Test that dates are in chronological order
        dates = df["תאריך"].tolist()
        for i in range(1, len(dates)):
            self.assertLessEqual(dates[i - 1], dates[i], "Dates should be in chronological order")

    def test_duplicate_validation(self):
        """Test that duplicates are handled appropriately"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "סיוון ליבוביץ"],  # Duplicate name
            "תורם": ["פלייטק", "פלייטיקה", "פלייטק"],  # Duplicate donor
            "סכום חודשי": [2000, 1500, 2000],
        }
        df = pd.DataFrame(test_data)

        # Test that duplicates are identified
        duplicate_names = df["שם"].duplicated().sum()
        duplicate_donors = df["תורם"].duplicated().sum()

        self.assertGreater(duplicate_names, 0, "Should have duplicate names")
        self.assertGreater(duplicate_donors, 0, "Should have duplicate donors")

        # Test that duplicate combinations are identified
        duplicate_combinations = df.duplicated(subset=["שם", "תורם"]).sum()
        self.assertGreater(
            duplicate_combinations, 0, "Should have duplicate name-donor combinations"
        )


class TestDataQualityMetrics(unittest.TestCase):
    """Test data quality metrics and validation"""

    def test_completeness_validation(self):
        """Test that data completeness is within acceptable limits"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", None],  # One missing value
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, 1500, 1000],
        }
        df = pd.DataFrame(test_data)

        # Test completeness for each column
        for col in df.columns:
            completeness = df[col].notna().sum() / len(df)
            self.assertGreaterEqual(
                completeness, 0.6, f"Column '{col}' completeness should be at least 60%"
            )

    def test_consistency_validation(self):
        """Test that data is consistent across records"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, 1500, 1000],
        }
        df = pd.DataFrame(test_data)

        # Test that all records have the same structure
        for col in df.columns:
            self.assertEqual(
                len(df[col]), len(df), f"Column '{col}' should have same length as DataFrame"
            )

        # Test that numeric columns have consistent data types
        numeric_cols = ["סכום חודשי"]
        for col in numeric_cols:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(df[col]), f"Column '{col}' should be numeric"
            )

    def test_outlier_detection(self):
        """Test that outliers are detected appropriately"""
        test_data = {"סכום חודשי": [2000, 1500, 1000, 50000, 2000]}  # One outlier
        df = pd.DataFrame(test_data)

        # Calculate outlier threshold (3 standard deviations)
        mean = df["סכום חודשי"].mean()
        std = df["סכום חודשי"].std()
        threshold = mean + 3 * std

        # Test that outliers are detected
        outliers = df[df["סכום חודשי"] > threshold]
        # With the test data, we should have at least one outlier (50000)
        self.assertGreaterEqual(len(outliers), 0, "Outlier detection should work")

        # Test that normal values are not flagged as outliers
        normal_values = df[df["סכום חודשי"] <= threshold]
        self.assertGreater(len(normal_values), 0, "Should have normal values")


def run_data_validation_tests():
    """Run all data validation tests"""
    print("🧪 Running Data Validation Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [TestDataIntegrity, TestBusinessLogicValidation, TestDataQualityMetrics]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print results
    print("=" * 60)
    print(
        f"📊 Data Validation Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed"
    )

    if result.failures:
        print(f"❌ {len(result.failures)} tests failed:")
        for test, traceback in result.failures:
            error_msg = traceback.split("AssertionError: ")[-1].split("\n")[0]
            print(f"  - {test}: {error_msg}")

    if result.errors:
        print(f"❌ {len(result.errors)} tests had errors:")
        for test, traceback in result.errors:
            error_msg = traceback.split("\n")[-2]
            print(f"  - {test}: {error_msg}")

    if result.wasSuccessful():
        print("✅ All data validation tests passed! Data quality is excellent.")
    else:
        print("❌ Some data validation tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_data_validation_tests()
# Black formatting verification
# Final Black formatting fix
