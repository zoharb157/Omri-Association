#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_sheets_io import read_sheet, gc, SPREADSHEET_ID

def test_google_sheets():
    print("=== Google Sheets Test ===")
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"Google Sheets client: {'Connected' if gc else 'Not connected'}")
    
    if not gc:
        print("❌ Google Sheets client not available")
        return
    
    try:
        # Test reading each sheet
        sheets_to_test = ["Expenses", "Donations", "Investors", "Widows"]
        
        for sheet_name in sheets_to_test:
            print(f"\n--- Testing {sheet_name} ---")
            try:
                df = read_sheet(sheet_name)
                print(f"✅ Successfully loaded {sheet_name}")
                print(f"   Shape: {df.shape}")
                print(f"   Columns: {list(df.columns)}")
                if not df.empty:
                    print(f"   First row: {df.iloc[0].tolist()}")
                else:
                    print("   Sheet is empty")
            except Exception as e:
                print(f"❌ Error loading {sheet_name}: {e}")
                
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    test_google_sheets() 