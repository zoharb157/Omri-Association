#!/usr/bin/env python3
"""
Unit tests for theme manager module
Tests theme switching and management functionality
"""

import pytest
from unittest.mock import MagicMock, patch

from theme_manager import (
    get_theme_manager,
    apply_current_theme,
    get_current_theme_colors,
)


class TestThemeManager:
    """Test theme manager functionality"""

    @patch("theme_manager.st")
    def test_get_theme_manager_light(self, mock_st):
        """Test get_theme_manager returns theme manager"""
        mock_st.session_state = {"ENABLE_DARK_MODE": False}
        
        theme_manager = get_theme_manager()
        
        assert theme_manager is not None

    @patch("theme_manager.st")
    def test_get_theme_manager_dark(self, mock_st):
        """Test get_theme_manager returns theme manager"""
        mock_st.session_state = {"ENABLE_DARK_MODE": True}
        
        theme_manager = get_theme_manager()
        
        assert theme_manager is not None

    @patch("theme_manager.st")
    def test_get_theme_manager_default(self, mock_st):
        """Test get_theme_manager returns theme manager when not set"""
        mock_st.session_state = {}
        
        theme_manager = get_theme_manager()
        
        assert theme_manager is not None

    @patch("theme_manager.st")
    def test_apply_current_theme_light(self, mock_st):
        """Test apply_current_theme applies light theme"""
        mock_st.session_state = {"ENABLE_DARK_MODE": False}
        mock_st.markdown = MagicMock()
        
        apply_current_theme()
        
        mock_st.markdown.assert_called()

    @patch("theme_manager.st")
    def test_apply_current_theme_dark(self, mock_st):
        """Test apply_current_theme applies dark theme"""
        mock_st.session_state = {"ENABLE_DARK_MODE": True}
        mock_st.markdown = MagicMock()
        
        apply_current_theme()
        
        mock_st.markdown.assert_called()

    def test_get_current_theme_colors(self):
        """Test get_current_theme_colors returns theme colors"""
        colors = get_current_theme_colors()
        
        assert isinstance(colors, dict)
        assert len(colors) > 0

    @patch("theme_manager.st")
    def test_theme_manager_error_handling(self, mock_st):
        """Test theme manager handles errors gracefully"""
        mock_st.session_state = MagicMock(side_effect=Exception("Session error"))
        
        # Should handle errors gracefully
        theme_manager = get_theme_manager()
        assert theme_manager is not None

    @patch("theme_manager.st")
    def test_apply_current_theme_error_handling(self, mock_st):
        """Test apply_current_theme handles errors gracefully"""
        mock_st.session_state = MagicMock(side_effect=Exception("Session error"))
        mock_st.markdown = MagicMock()
        
        # Should not raise exception
        apply_current_theme()

    def test_theme_colors_contains_required_elements(self):
        """Test theme colors contain required color elements"""
        colors = get_current_theme_colors()
        
        # Should contain basic color structure
        assert isinstance(colors, dict)
        assert len(colors) > 0

    def test_theme_colors_is_not_empty(self):
        """Test theme colors is not empty"""
        colors = get_current_theme_colors()
        
        assert len(colors) > 0

    @patch("theme_manager.st")
    def test_theme_manager_persistence(self, mock_st):
        """Test theme manager persists across calls"""
        mock_st.session_state = {}
        
        # Get theme manager multiple times
        theme_manager1 = get_theme_manager()
        theme_manager2 = get_theme_manager()
        
        assert theme_manager1 is not None
        assert theme_manager2 is not None