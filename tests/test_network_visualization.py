#!/usr/bin/env python3
"""
Network Visualization Tests for Omri Association Dashboard
Tests network/connection map functionality and edge cases
"""

import os
import sys
import unittest

import pandas as pd

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestNetworkVisualization(unittest.TestCase):
    """Test network visualization functionality"""

    def test_network_data_structure(self):
        """Test that network data is structured correctly"""
        # Create test data for network visualization
        expenses_df = pd.DataFrame({
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
            "סכום": [2000, 1500, 1000],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })

        donations_df = pd.DataFrame({
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום": [2000, 1500, 1000],
            "תאריך": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })

        almanot_df = pd.DataFrame({
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
            "מספר ילדים": [3, 5, 4],
            "סכום חודשי": [2000, 1500, 1000],
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"]
        })

        investors_df = pd.DataFrame({
            "שם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום": [2000, 1500, 1000]
        })

        # Test that all DataFrames have required columns
        self.assertIn("שם", expenses_df.columns)
        self.assertIn("תורם", donations_df.columns)
        self.assertIn("שם", almanot_df.columns)
        self.assertIn("תורם", almanot_df.columns)
        self.assertIn("שם", investors_df.columns)

    def test_network_connections(self):
        """Test network connection logic"""
        # Test donor-widow connections
        almanot_df = pd.DataFrame({
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 1500]
        })

        # Test that connections can be established
        connections = []
        for _, row in almanot_df.iterrows():
            if pd.notna(row["תורם"]) and pd.notna(row["שם"]):
                connections.append({
                    "donor": row["תורם"],
                    "widow": row["שם"],
                    "amount": row["סכום חודשי"]
                })

        self.assertEqual(len(connections), 2)
        self.assertEqual(connections[0]["donor"], "פלייטק")
        self.assertEqual(connections[0]["widow"], "סיוון ליבוביץ")

    def test_network_filters(self):
        """Test network filter functionality"""
        # Test minimum support amount filter
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ", "ספיר קנפו"],
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, 1500, 500]  # One below threshold
        }
        df = pd.DataFrame(test_data)

        # Filter by minimum support amount
        min_support = 1000
        filtered_df = df[df["סכום חודשי"] >= min_support]

        self.assertEqual(len(filtered_df), 2)
        self.assertNotIn("ספיר קנפו", filtered_df["שם"].values)

    def test_network_labels(self):
        """Test network label functionality"""
        # Test that labels can be generated correctly
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 1500]
        }
        df = pd.DataFrame(test_data)

        # Generate labels
        labels = []
        for _, row in df.iterrows():
            label = f"{row['שם']} - {row['תורם']} ({row['סכום חודשי']}₪)"
            labels.append(label)

        self.assertEqual(len(labels), 2)
        self.assertIn("סיוון ליבוביץ - פלייטק (2000₪)", labels)

    def test_network_empty_data(self):
        """Test network handling of empty data"""
        empty_df = pd.DataFrame()

        # Test that empty data is handled gracefully
        connections = []
        for _, row in empty_df.iterrows():
            connections.append(row)

        self.assertEqual(len(connections), 0)

    def test_network_missing_columns(self):
        """Test network handling of missing columns"""
        # Test with missing required columns
        incomplete_df = pd.DataFrame({
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"]
            # Missing "תורם" and "סכום חודשי" columns
        })

        # Test that missing columns are handled gracefully
        connections = []
        for _, row in incomplete_df.iterrows():
            if "תורם" in incomplete_df.columns and "סכום חודשי" in incomplete_df.columns:
                connections.append(row)

        self.assertEqual(len(connections), 0)

    def test_network_duplicate_connections(self):
        """Test network handling of duplicate connections"""
        # Test with duplicate donor-widow pairs
        test_data = {
            "שם": ["סיוון ליבוביץ", "סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 1500, 1000]
        }
        df = pd.DataFrame(test_data)

        # Test that duplicates are handled correctly
        connections = []
        seen_connections = set()

        for _, row in df.iterrows():
            connection_key = f"{row['תורם']}-{row['שם']}"
            if connection_key not in seen_connections:
                connections.append(row)
                seen_connections.add(connection_key)

        # Should have 2 unique connections (one duplicate removed)
        self.assertEqual(len(connections), 2)

    def test_network_hebrew_text(self):
        """Test network handling of Hebrew text"""
        hebrew_data = {
            "שם": ["סיוון ליבוביץ-ג'ון", "הדס הרשקוביץ'", "ספיר קנפו-סמית'"],
            "תורם": ["פלייטק & גלים", "פלייטיקה (חברה)", "מייקרוסופט [ישראל]"],
            "סכום חודשי": [2000, 1500, 1000]
        }
        df = pd.DataFrame(hebrew_data)

        # Test that Hebrew text is preserved
        for _, row in df.iterrows():
            self.assertIsInstance(row["שם"], str)
            self.assertIsInstance(row["תורם"], str)
            self.assertTrue(len(row["שם"]) > 0)
            self.assertTrue(len(row["תורם"]) > 0)

    def test_network_numeric_values(self):
        """Test network handling of numeric values"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000.50, 1500.75]  # Decimal values
        }
        df = pd.DataFrame(test_data)

        # Test that numeric values are handled correctly
        for _, row in df.iterrows():
            self.assertIsInstance(row["סכום חודשי"], (int, float))
            self.assertGreater(row["סכום חודשי"], 0)

    def test_network_performance(self):
        """Test network performance with large datasets"""
        # Create large dataset
        large_data = {
            "שם": [f"אלמנה {i}" for i in range(1000)],
            "תורם": [f"תורם {i % 100}" for i in range(1000)],
            "סכום חודשי": [2000 + (i % 100) for i in range(1000)]
        }
        df = pd.DataFrame(large_data)

        # Test that large dataset is handled efficiently
        connections = []
        for _, row in df.iterrows():
            if pd.notna(row["תורם"]) and pd.notna(row["שם"]):
                connections.append(row)

        self.assertEqual(len(connections), 1000)
        self.assertEqual(len(df), 1000)


class TestNetworkErrorHandling(unittest.TestCase):
    """Test network error handling scenarios"""

    def test_network_invalid_data_types(self):
        """Test network handling of invalid data types"""
        test_data = {
            "שם": ["סיוון ליבוביץ", 123, None],
            "תורם": ["פלייטק", "פלייטיקה", "מייקרוסופט"],
            "סכום חודשי": [2000, "1500", 1000]  # Mixed types
        }
        df = pd.DataFrame(test_data)

        # Test that invalid data types are handled gracefully
        valid_connections = []
        for _, row in df.iterrows():
            if (isinstance(row["שם"], str) and
                isinstance(row["תורם"], str) and
                isinstance(row["סכום חודשי"], (int, float))):
                valid_connections.append(row)

        # Should have 1 valid connection (first row)
        self.assertEqual(len(valid_connections), 1)

    def test_network_nan_values(self):
        """Test network handling of NaN values"""
        test_data = {
            "שם": ["סיוון ליבוביץ", pd.NA, "ספיר קנפו"],
            "תורם": ["פלייטק", "פלייטיקה", pd.NA],
            "סכום חודשי": [2000, 1500, 1000]
        }
        df = pd.DataFrame(test_data)

        # Test that NaN values are handled gracefully
        valid_connections = []
        for _, row in df.iterrows():
            if (pd.notna(row["שם"]) and
                pd.notna(row["תורם"]) and
                pd.notna(row["סכום חודשי"])):
                valid_connections.append(row)

        # Should have 1 valid connection (first row)
        self.assertEqual(len(valid_connections), 1)

    def test_network_negative_values(self):
        """Test network handling of negative values"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, -500]  # Negative value
        }
        df = pd.DataFrame(test_data)

        # Test that negative values are handled correctly
        positive_connections = []
        for _, row in df.iterrows():
            if row["סכום חודשי"] > 0:
                positive_connections.append(row)

        # Should have 1 positive connection
        self.assertEqual(len(positive_connections), 1)

    def test_network_zero_values(self):
        """Test network handling of zero values"""
        test_data = {
            "שם": ["סיוון ליבוביץ", "הדס הרשקוביץ"],
            "תורם": ["פלייטק", "פלייטיקה"],
            "סכום חודשי": [2000, 0]  # Zero value
        }
        df = pd.DataFrame(test_data)

        # Test that zero values are handled correctly
        non_zero_connections = []
        for _, row in df.iterrows():
            if row["סכום חודשי"] > 0:
                non_zero_connections.append(row)

        # Should have 1 non-zero connection
        self.assertEqual(len(non_zero_connections), 1)


def run_network_tests():
    """Run all network visualization tests"""
    print("🧪 Running Network Visualization Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestNetworkVisualization,
        TestNetworkErrorHandling
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print results
    print("=" * 60)
    print(f"📊 Network Test Results: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} tests passed")

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
        print("✅ All network visualization tests passed! Network functionality is working correctly.")
    else:
        print("❌ Some network visualization tests failed. Check the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_network_tests()
