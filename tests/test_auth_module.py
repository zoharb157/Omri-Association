#!/usr/bin/env python3
"""
Unit tests for authentication module
Tests authentication functionality and edge cases
"""

import pytest
from unittest.mock import MagicMock, patch

from auth import (
    check_auth_and_redirect,
    is_authenticated,
    show_user_info,
    show_login_form,
    login_user,
)


class TestAuthModule:
    """Test authentication module functionality"""

    @patch("auth.st")
    def test_check_auth_and_redirect_authenticated(self, mock_st):
        """Test check_auth_and_redirect when user is authenticated"""
        mock_st.session_state = {"authenticated": True}
        
        result = check_auth_and_redirect()
        
        assert result is True

    @patch("auth.st")
    @patch("auth.is_authenticated")
    def test_check_auth_and_redirect_not_authenticated(self, mock_is_authenticated, mock_st):
        """Test check_auth_and_redirect when user is not authenticated"""
        mock_is_authenticated.return_value = False
        mock_st.session_state = {"authenticated": False}
        mock_st.markdown = MagicMock()
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="test_user")
        mock_st.text_input.return_value = "test_user"
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        
        result = check_auth_and_redirect()
        
        assert result is False

    @patch("auth.st")
    def test_is_authenticated_true(self, mock_st):
        """Test is_authenticated returns True when user is authenticated"""
        mock_st.session_state = {"authenticated": True}
        
        result = is_authenticated()
        
        assert result is True

    @patch("auth.st")
    def test_is_authenticated_false(self, mock_st):
        """Test is_authenticated returns False when user is not authenticated"""
        mock_session_state = MagicMock()
        mock_session_state.get = MagicMock(side_effect=lambda key, default: {"ENABLE_AUTHENTICATION": True, "authenticated": False}.get(key, default))
        mock_session_state.authenticated = False
        mock_st.session_state = mock_session_state
        
        result = is_authenticated()
        
        assert result is False

    @patch("auth.st")
    def test_is_authenticated_missing_key(self, mock_st):
        """Test is_authenticated returns False when key is missing"""
        mock_session_state = MagicMock()
        mock_session_state.get = MagicMock(side_effect=lambda key, default: {"ENABLE_AUTHENTICATION": True}.get(key, default))
        mock_st.session_state = mock_session_state
        
        result = is_authenticated()
        
        assert result is False

    @patch("auth.st")
    @patch("auth.is_authenticated")
    @patch("auth.get_current_user_info")
    def test_show_user_info(self, mock_get_user_info, mock_is_authenticated, mock_st):
        """Test show_user_info displays user information"""
        mock_is_authenticated.return_value = True
        mock_get_user_info.return_value = {"name": "test_user", "role": "admin", "permissions": ["read", "write"]}
        mock_st.session_state = {"username": "test_user", "role": "admin"}
        mock_st.sidebar = MagicMock()
        mock_st.sidebar.markdown = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        
        show_user_info()
        
        mock_st.sidebar.markdown.assert_called()

    @patch("auth.st")
    @patch("auth.is_authenticated")
    @patch("auth.get_current_user_info")
    def test_show_user_info_no_username(self, mock_get_user_info, mock_is_authenticated, mock_st):
        """Test show_user_info handles missing username"""
        mock_is_authenticated.return_value = True
        mock_get_user_info.return_value = None
        mock_st.session_state = {"role": "admin"}
        mock_st.sidebar = MagicMock()
        mock_st.sidebar.markdown = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        
        show_user_info()
        
        # When get_current_user_info returns None, markdown should not be called
        mock_st.sidebar.markdown.assert_not_called()

    @patch("auth.st")
    def test_show_login_form(self, mock_st):
        """Test show_login_form creates login form"""
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="test_user")
        mock_st.text_input.return_value = "test_user"
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        
        show_login_form()
        
        mock_st.form.assert_called_once()

    def test_login_user_valid(self):
        """Test login_user with valid credentials"""
        result = login_user("admin", "admin123")
        
        assert result is True

    def test_login_user_invalid(self):
        """Test login_user with invalid credentials"""
        result = login_user("wrong_user", "wrong_pass")
        
        assert result is False

    def test_login_user_empty(self):
        """Test login_user with empty credentials"""
        result = login_user("", "")
        
        assert result is False

    def test_login_user_none(self):
        """Test login_user with None credentials"""
        result = login_user(None, None)
        
        assert result is False

    @patch("auth.st")
    def test_auth_module_error_handling(self, mock_st):
        """Test authentication module error handling"""
        mock_st.session_state = MagicMock(side_effect=Exception("Session error"))
        
        # Should handle errors gracefully
        result = is_authenticated()
        assert result is False

    @patch("auth.st")
    def test_check_auth_and_redirect_exception(self, mock_st):
        """Test check_auth_and_redirect handles exceptions"""
        mock_st.session_state = MagicMock(side_effect=Exception("Session error"))
        mock_st.markdown = MagicMock()
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="test_user")
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        
        result = check_auth_and_redirect()
        
        assert result is False

    @patch("auth.st")
    def test_show_user_info_exception(self, mock_st):
        """Test show_user_info handles exceptions"""
        mock_st.session_state = MagicMock(side_effect=Exception("Session error"))
        mock_st.sidebar = MagicMock()
        mock_st.sidebar.markdown = MagicMock()
        
        # Should not raise exception
        show_user_info()
