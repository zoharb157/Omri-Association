#!/usr/bin/env python3
"""
Unit tests for dashboard core functionality
Tests the main dashboard logic and data processing
"""

from unittest.mock import MagicMock, patch

import pandas as pd

from tests.fixtures.sample_data import (
    sample_almanot_df,
    sample_donations_df,
    sample_expenses_df,
    sample_investors_df,
)
from ui.dashboard_core import (
    load_dashboard_data,
    process_dashboard_data,
    render_home_tab,
    render_network_tab,
    run_dashboard,
)


class TestDashboardCore:
    """Test dashboard core functionality"""

    def test_load_dashboard_data_success(self):
        """Test successful data loading"""
        with patch("ui.dashboard_core.fetch_dashboard_frames") as mock_fetch:
            # Mock successful data fetch - returns a dictionary
            mock_fetch.return_value = {
                "Expenses": sample_expenses_df(),
                "Donations": sample_donations_df(),
                "Almanot": sample_almanot_df(),
                "Investors": sample_investors_df(),
            }

            expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()

            assert expenses_df is not None
            assert donations_df is not None
            assert almanot_df is not None
            assert investors_df is not None
            assert isinstance(expenses_df, pd.DataFrame)
            assert isinstance(donations_df, pd.DataFrame)
            assert isinstance(almanot_df, pd.DataFrame)
            assert isinstance(investors_df, pd.DataFrame)

    def test_load_dashboard_data_failure(self):
        """Test data loading failure"""
        with patch("ui.dashboard_core.fetch_dashboard_frames") as mock_fetch:
            # Mock data fetch failure
            mock_fetch.return_value = {}

            expenses_df, donations_df, almanot_df, investors_df = load_dashboard_data()

            assert expenses_df is not None  # Returns empty DataFrame, not None
            assert donations_df is not None
            assert almanot_df is not None
            assert investors_df is not None

    def test_process_dashboard_data_success(self):
        """Test successful data processing"""
        expenses_df = sample_expenses_df()
        donations_df = sample_donations_df()
        almanot_df = sample_almanot_df()

        budget_status, donor_stats, widow_stats = process_dashboard_data(
            expenses_df, donations_df, almanot_df
        )

        # Test budget status structure
        assert isinstance(budget_status, dict)
        assert "total_donations" in budget_status
        assert "total_expenses" in budget_status
        assert "balance" in budget_status

        # Test donor stats structure
        assert isinstance(donor_stats, dict)
        assert "total_donors" in donor_stats
        assert "total_donations" in donor_stats

        # Test widow stats structure
        assert isinstance(widow_stats, dict)
        assert "total_widows" in widow_stats
        assert "total_support" in widow_stats

    def test_process_dashboard_data_with_nan_values(self):
        """Test data processing with NaN values"""
        expenses_df = sample_expenses_df()
        donations_df = sample_donations_df()
        almanot_df = sample_almanot_df()

        # Add some NaN values
        almanot_df.loc[0, "סכום חודשי"] = None

        budget_status, donor_stats, widow_stats = process_dashboard_data(
            expenses_df, donations_df, almanot_df
        )

        # Should handle NaN values gracefully
        assert isinstance(budget_status, dict)
        assert isinstance(donor_stats, dict)
        assert isinstance(widow_stats, dict)

    @patch("ui.dashboard_core.st")
    def test_run_dashboard_success(self, mock_st):
        """Test successful dashboard run"""
        # Mock Streamlit components
        mock_st.session_state = {}
        mock_st.error = MagicMock()
        mock_st.info = MagicMock()
        mock_st.stop = MagicMock()

        with patch("ui.dashboard_core.load_dashboard_data") as mock_load:
            with patch("ui.dashboard_core.process_dashboard_data") as mock_process:
                with patch("ui.dashboard_core.create_main_tabs") as mock_tabs:
                    with patch("ui.dashboard_core.check_service_account_validity") as mock_check:
                        # Mock successful data loading
                        mock_load.return_value = (
                            sample_expenses_df(),
                            sample_donations_df(),
                            sample_almanot_df(),
                            sample_investors_df(),
                        )
                        mock_process.return_value = ({}, {}, {})
                        mock_check.return_value = True
                        mock_tabs.return_value = (
                            MagicMock(),
                            MagicMock(),
                            MagicMock(),
                            MagicMock(),
                            MagicMock(),
                            MagicMock(),
                        )

                        # Should not raise any exceptions
                        run_dashboard()

    @patch("ui.dashboard_core.st")
    def test_run_dashboard_data_loading_failure(self, mock_st):
        """Test dashboard run with data loading failure"""
        mock_st.session_state = {}
        mock_st.error = MagicMock()
        mock_st.stop = MagicMock()

        with patch("ui.dashboard_core.load_dashboard_data") as mock_load:
            with patch("ui.dashboard_core.check_service_account_validity") as mock_check:
                # Mock data loading failure
                mock_load.return_value = (None, None, None, None)
                mock_check.return_value = True

                run_dashboard()

                # Should call st.error for data loading failure
                mock_st.error.assert_called()

    @patch("ui.dashboard_core.st")
    def test_run_dashboard_service_account_failure(self, mock_st):
        """Test dashboard run with service account failure"""
        mock_st.session_state = {}
        mock_st.error = MagicMock()
        mock_st.stop = MagicMock()

        with patch("ui.dashboard_core.check_service_account_validity") as mock_check:
            # Mock service account failure
            mock_check.return_value = False

            run_dashboard()

            # Should call st.error and st.stop
            mock_st.error.assert_called()
            mock_st.stop.assert_called()

    def test_render_home_tab_structure(self):
        """Test home tab rendering structure"""
        expenses_df = sample_expenses_df()
        donations_df = sample_donations_df()
        almanot_df = sample_almanot_df()
        budget_status = {"total_donations": 1000, "total_expenses": 800, "balance": 200}
        donor_stats = {"total_donors": 5, "total_donations": 1000}
        widow_stats = {"total_widows": 3, "total_support": 500}

        # Should not raise any exceptions
        render_home_tab(
            expenses_df, donations_df, almanot_df, budget_status, donor_stats, widow_stats
        )

    def test_render_network_tab_structure(self):
        """Test network tab rendering structure"""
        expenses_df = sample_expenses_df()
        donations_df = sample_donations_df()
        almanot_df = sample_almanot_df()
        investors_df = sample_investors_df()

        # Should not raise any exceptions
        render_network_tab(expenses_df, donations_df, almanot_df, investors_df)
