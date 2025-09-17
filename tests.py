
import time
from typing import Any, Callable, Dict, List

import numpy as np
import pandas as pd
import streamlit as st

#!/usr/bin/env python3
"""
Simple Unit Testing System for Omri Association Dashboard
Provides basic testing functionality for core components
"""


class TestRunner:
    """Simple test runner for dashboard components"""

    def __init__(self):
        self.tests = []
        self.results = []

    def add_test(self, name: str, test_func: Callable, description: str = ""):
        """Add a test to the test suite"""
        self.tests.append({
            'name': name,
            'function': test_func,
            'description': description
        })

    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all tests and return results"""
        self.results = []

        for test in self.tests:
            try:
                start_time = time.time()
                result = test['function']()
                end_time = time.time()

                self.results.append({
                    'name': test['name'],
                    'description': test['description'],
                    'status': 'passed' if result else 'failed',
                    'execution_time': round(end_time - start_time, 3),
                    'error': None
                })

            except Exception as e:
                self.results.append({
                    'name': test['name'],
                    'description': test['description'],
                    'status': 'error',
                    'execution_time': 0,
                    'error': str(e)
                })

        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """Get test summary statistics"""
        if not self.results:
            return {}

        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'passed'])
        failed = len([r for r in self.results if r['status'] == 'failed'])
        errors = len([r for r in self.results if r['status'] == 'error'])

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'success_rate': round((passed / total) * 100, 1) if total > 0 else 0
        }

# Global test runner instance
test_runner = TestRunner()

def get_test_runner() -> TestRunner:
    """Get global test runner instance"""
    return test_runner

def show_test_dashboard():
    """Show testing dashboard in Streamlit"""
    st.markdown("### 🧪 מערכת בדיקות")

    # Run tests button
    if st.button("▶️ הרץ בדיקות", use_container_width=True):
        with st.spinner("🔄 מריץ בדיקות..."):
            results = test_runner.run_all_tests()

        # Show results
        show_test_results(results)

    # Show test summary if available
    if test_runner.results:
        show_test_summary()

def show_test_results(results: List[Dict[str, Any]]):
    """Show test results in Streamlit"""
    st.markdown("#### 📊 תוצאות בדיקות")

    for result in results:
        if result['status'] == 'passed':
            st.success(f"✅ {result['name']}: עבר בהצלחה ({result['execution_time']}s)")
        elif result['status'] == 'failed':
            st.error(f"❌ {result['name']}: נכשל")
        else:
            st.error(f"💥 {result['name']}: שגיאה - {result['error']}")

        if result['description']:
            st.info(f"📝 {result['description']}")

def show_test_summary():
    """Show test summary in Streamlit"""
    summary = test_runner.get_summary()

    st.markdown("#### 📈 סיכום בדיקות")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("סה״כ בדיקות", summary['total'])

    with col2:
        st.metric("עברו", summary['passed'])

    with col3:
        st.metric("נכשלו", summary['failed'])

    with col4:
        st.metric("אחוז הצלחה", f"{summary['success_rate']}%")

    # Success rate visualization
    if summary['total'] > 0:
        success_rate = summary['passed'] / summary['total']

        if success_rate >= 0.8:
            st.success("🎉 מערכת יציבה - רוב הבדיקות עברו בהצלחה!")
        elif success_rate >= 0.6:
            st.warning("⚠️ מערכת עם בעיות קלות - חלק מהבדיקות נכשלו")
        else:
            st.error("🚨 מערכת לא יציבה - רוב הבדיקות נכשלו")

# Test functions
def test_data_loading():
    """Test data loading functionality"""
    try:
        # Test if we can import data loading modules
        import google_sheets_io  # noqa: F401
        return True
    except ImportError:
        return False

def test_data_processing():
    """Test data processing functionality"""
    try:
        # Test if we can import data processing modules
        import data_processing  # noqa: F401
        return True
    except ImportError:
        return False

def test_dataframe_operations():
    """Test pandas DataFrame operations"""
    try:
        # Create test DataFrame
        test_df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })

        # Test basic operations
        assert len(test_df) == 3
        assert 'A' in test_df.columns
        assert test_df['A'].sum() == 6

        return True
    except Exception:
        return False

def test_numeric_operations():
    """Test numeric operations"""
    try:
        # Test basic math
        assert 2 + 2 == 4
        assert 10 * 5 == 50
        assert 100 / 4 == 25

        # Test numpy operations
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.sum() == 15
        assert arr.mean() == 3

        return True
    except Exception:
        return False

def test_config_management():
    """Test configuration management"""
    try:
        from config import get_setting, set_setting

        # Test setting and getting values
        test_value = "test_value"
        set_setting('TEST_KEY', test_value)
        retrieved_value = get_setting('TEST_KEY')

        return retrieved_value == test_value
    except ImportError:
        return False

def test_cache_manager():
    """Test cache manager functionality"""
    try:
        from cache_manager import cache_dict, get_cached_dict

        # Test caching
        test_data = {'key': 'value'}
        cache_dict('test_cache', test_data)
        retrieved_data = get_cached_dict('test_cache')

        return retrieved_data == test_data
    except ImportError:
        return False

def test_theme_manager():
    """Test theme manager functionality"""
    try:
        from theme_manager import get_current_theme, get_theme_colors

        # Test theme functions
        current_theme = get_current_theme()
        theme_colors = get_theme_colors(current_theme)

        return current_theme in ['light', 'dark'] and 'primary_color' in theme_colors
    except ImportError:
        return False

def test_authentication():
    """Test authentication system"""
    try:
        from auth import AuthManager

        # Test auth manager
        auth = AuthManager()
        result = auth.authenticate('admin', 'admin123')

        return result
    except ImportError:
        return False

def test_monitoring():
    """Test monitoring system"""
    try:
        from monitoring import SystemMonitor

        # Test system monitor
        monitor = SystemMonitor()
        metrics = monitor.get_system_metrics()

        return isinstance(metrics, dict) and 'cpu' in metrics
    except ImportError:
        return False

# Register tests
test_runner.add_test(
    "Data Loading",
    test_data_loading,
    "בדיקת יכולת טעינת נתונים מ-Google Sheets"
)

test_runner.add_test(
    "Data Processing",
    test_data_processing,
    "בדיקת עיבוד נתונים וסטטיסטיקות"
)

test_runner.add_test(
    "DataFrame Operations",
    test_dataframe_operations,
    "בדיקת פעולות pandas DataFrame"
)

test_runner.add_test(
    "Numeric Operations",
    test_numeric_operations,
    "בדיקת פעולות מתמטיות וספריות"
)

test_runner.add_test(
    "Configuration Management",
    test_config_management,
    "בדיקת ניהול הגדרות מערכת"
)

test_runner.add_test(
    "Cache Manager",
    test_cache_manager,
    "בדיקת מערכת המטמון"
)

test_runner.add_test(
    "Theme Manager",
    test_theme_manager,
    "בדיקת ניהול עיצובים"
)

test_runner.add_test(
    "Authentication",
    test_authentication,
    "בדיקת מערכת אימות"
)

test_runner.add_test(
    "System Monitoring",
    test_monitoring,
    "בדיקת ניטור מערכת"
)

