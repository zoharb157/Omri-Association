#!/usr/bin/env python3
"""
Modern Navigation Components for Omri Association Dashboard
Navigation system with modern UX
"""

import streamlit as st


def create_modern_tab_navigation():
    """Create modern tab navigation with better styling"""

    # Define tabs with icons and labels
    tabs_data = [
        {"label": "🏠 דף הבית", "key": "home"},
        {"label": "💰 תקציב", "key": "budget"},
        {"label": "👥 תורמים", "key": "donors"},
        {"label": "👩 אלמנות", "key": "widows"},
        {"label": "🕸️ מפת קשרים", "key": "network"},
        {"label": "🏘️ אזורי מגורים", "key": "residential"}
    ]

    # Create custom tab navigation
    tab_html = """
    <div class="modern-tab-navigation">
        <div class="tab-list">
    """

    for i, tab in enumerate(tabs_data):
        active_class = "active" if i == 0 else ""
        tab_html += f"""
            <button class="tab-button {active_class}" data-tab="{tab['key']}">
                <span class="tab-icon">{tab['label'].split(' ')[0]}</span>
                <span class="tab-label">{tab['label'].split(' ', 1)[1]}</span>
            </button>
        """

    tab_html += """
        </div>
    </div>
    """

    st.markdown(tab_html, unsafe_allow_html=True)

    # Add CSS for tab navigation
    tab_css = """
    <style>
    .modern-tab-navigation {
        background: var(--surface-elevated);
        border-bottom: 1px solid var(--border);
        margin-bottom: var(--space-6);
        padding: 0 var(--space-4);
    }

    .tab-list {
        display: flex;
        gap: var(--space-1);
        overflow-x: auto;
        padding: var(--space-2) 0;
    }

    .tab-button {
        display: flex;
        align-items: center;
        gap: var(--space-2);
        padding: var(--space-3) var(--space-4);
        border: none;
        background: transparent;
        color: var(--gray-600);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
        font-family: var(--font-hebrew);
        font-size: var(--text-sm);
        font-weight: 500;
    }

    .tab-button:hover {
        background: var(--gray-100);
        color: var(--gray-900);
    }

    .tab-button.active {
        background: var(--primary-50);
        color: var(--primary-700);
    }

    .tab-icon {
        font-size: var(--text-lg);
    }

    .tab-label {
        font-size: var(--text-sm);
    }

    @media (max-width: 768px) {
        .tab-list {
            gap: var(--space-0);
        }

        .tab-button {
            padding: var(--space-2) var(--space-3);
        }

        .tab-label {
            display: none;
        }
    }
    </style>
    """

    st.markdown(tab_css, unsafe_allow_html=True)

def create_modern_breadcrumb(current_page: str, parent_pages: list = None):
    """Create modern breadcrumb navigation"""

    if parent_pages is None:
        parent_pages = []

    breadcrumb_html = """
    <nav class="modern-breadcrumb" aria-label="ניווט">
        <ol class="breadcrumb-list">
    """

    # Add home link
    breadcrumb_html += """
            <li class="breadcrumb-item">
                <a href="#" class="breadcrumb-link">🏠 דף הבית</a>
            </li>
    """

    # Add parent pages
    for page in parent_pages:
        breadcrumb_html += f"""
            <li class="breadcrumb-separator">›</li>
            <li class="breadcrumb-item">
                <a href="#" class="breadcrumb-link">{page}</a>
            </li>
        """

    # Add current page
    breadcrumb_html += f"""
            <li class="breadcrumb-separator">›</li>
            <li class="breadcrumb-item current">
                <span class="breadcrumb-current">{current_page}</span>
            </li>
        </ol>
    </nav>
    """

    st.markdown(breadcrumb_html, unsafe_allow_html=True)

    # Add CSS for breadcrumb
    breadcrumb_css = """
    <style>
    .modern-breadcrumb {
        margin-bottom: var(--space-4);
        padding: var(--space-2) 0;
    }

    .breadcrumb-list {
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        padding: 0;
        font-size: var(--text-sm);
        font-family: var(--font-hebrew);
    }

    .breadcrumb-item {
        display: flex;
        align-items: center;
    }

    .breadcrumb-separator {
        margin: 0 var(--space-2);
        color: var(--gray-400);
    }

    .breadcrumb-link {
        color: var(--gray-600);
        text-decoration: none;
        transition: color 0.2s ease;
    }

    .breadcrumb-link:hover {
        color: var(--primary-600);
    }

    .breadcrumb-current {
        color: var(--gray-900);
        font-weight: 500;
    }

    @media (max-width: 768px) {
        .breadcrumb-list {
            font-size: var(--text-xs);
        }

        .breadcrumb-separator {
            margin: 0 var(--space-1);
        }
    }
    </style>
    """

    st.markdown(breadcrumb_css, unsafe_allow_html=True)

def create_modern_page_header(title: str, subtitle: str = None, actions: list = None):
    """Create modern page header with actions"""

    actions_html = ""
    if actions:
        actions_html = f'<div class="page-actions">{"".join(actions)}</div>'

    header_html = f"""
    <div class="modern-page-header">
        <div class="page-header-content">
            <h1 class="page-title">{title}</h1>
            {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        {actions_html}
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

    # Add CSS for page header
    header_css = """
    <style>
    .modern-page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--space-8);
        padding-bottom: var(--space-4);
        border-bottom: 1px solid var(--border);
    }

    .page-title {
        font-size: var(--text-3xl);
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
        font-family: var(--font-hebrew);
    }

    .page-subtitle {
        font-size: var(--text-lg);
        color: var(--gray-600);
        margin: var(--space-2) 0 0 0;
        font-family: var(--font-hebrew);
    }

    .page-actions {
        display: flex;
        gap: var(--space-2);
        align-items: center;
    }

    .page-action-button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-2) var(--space-4);
        font-size: var(--text-sm);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }

    .page-action-button:hover {
        background: var(--primary-700);
        transform: translateY(-1px);
    }

    .page-action-button.secondary {
        background: var(--gray-100);
        color: var(--gray-700);
    }

    .page-action-button.secondary:hover {
        background: var(--gray-200);
    }

    @media (max-width: 768px) {
        .modern-page-header {
            flex-direction: column;
            gap: var(--space-4);
        }

        .page-title {
            font-size: var(--text-2xl);
        }

        .page-actions {
            width: 100%;
            justify-content: flex-start;
        }
    }
    </style>
    """

    st.markdown(header_css, unsafe_allow_html=True)

def create_modern_sidebar_navigation():
    """Create modern sidebar navigation"""

    sidebar_html = """
    <div class="modern-sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo">
                <h1 class="sidebar-title">עמותת עמרי</h1>
                <p class="sidebar-subtitle">מערכת ניהול</p>
            </div>
            <button class="sidebar-toggle" onclick="toggleSidebar()">
                <span class="hamburger"></span>
            </button>
        </div>

        <nav class="sidebar-nav">
            <ul class="nav-list">
                <li class="nav-item active">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">🏠</span>
                        <span class="nav-text">דף הבית</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">💰</span>
                        <span class="nav-text">תקציב</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">👥</span>
                        <span class="nav-text">תורמים</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">👩</span>
                        <span class="nav-text">אלמנות</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">🕸️</span>
                        <span class="nav-text">מפת קשרים</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <span class="nav-icon">🏘️</span>
                        <span class="nav-text">אזורי מגורים</span>
                    </a>
                </li>
            </ul>
        </nav>

        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar">👤</div>
                <div class="user-details">
                    <div class="user-name">מנהל מערכת</div>
                    <div class="user-role">מנהל</div>
                </div>
            </div>
            <button class="logout-button">🚪 התנתק</button>
        </div>
    </div>
    """

    st.markdown(sidebar_html, unsafe_allow_html=True)

    # Add CSS and JavaScript for sidebar
    sidebar_css = """
    <style>
    .modern-sidebar {
        position: fixed;
        top: 0;
        right: 0;
        width: 280px;
        height: 100vh;
        background: var(--surface-elevated);
        border-left: 1px solid var(--border);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease;
    }

    .sidebar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-6);
        border-bottom: 1px solid var(--border);
    }

    .sidebar-title {
        font-size: var(--text-xl);
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
        font-family: var(--font-hebrew);
    }

    .sidebar-subtitle {
        font-size: var(--text-sm);
        color: var(--gray-600);
        margin: var(--space-1) 0 0 0;
        font-family: var(--font-hebrew);
    }

    .sidebar-toggle {
        display: none;
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--space-2);
    }

    .hamburger {
        display: block;
        width: 20px;
        height: 2px;
        background: var(--gray-600);
        position: relative;
    }

    .hamburger::before,
    .hamburger::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 2px;
        background: var(--gray-600);
        transition: all 0.3s ease;
    }

    .hamburger::before {
        top: -6px;
    }

    .hamburger::after {
        top: 6px;
    }

    .sidebar-nav {
        flex: 1;
        padding: var(--space-4);
        overflow-y: auto;
    }

    .nav-list {
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .nav-item {
        margin-bottom: var(--space-1);
    }

    .nav-link {
        display: flex;
        align-items: center;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-md);
        text-decoration: none;
        color: var(--gray-700);
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }

    .nav-link:hover {
        background: var(--gray-100);
        color: var(--gray-900);
    }

    .nav-item.active .nav-link {
        background: var(--primary-50);
        color: var(--primary-700);
    }

    .nav-icon {
        margin-left: var(--space-3);
        font-size: var(--text-lg);
    }

    .nav-text {
        font-size: var(--text-sm);
        font-weight: 500;
    }

    .sidebar-footer {
        padding: var(--space-4);
        border-top: 1px solid var(--border);
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: var(--space-3);
        margin-bottom: var(--space-3);
    }

    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: var(--radius-full);
        background: var(--primary-100);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: var(--text-lg);
    }

    .user-name {
        font-size: var(--text-sm);
        font-weight: 500;
        color: var(--gray-900);
        font-family: var(--font-hebrew);
    }

    .user-role {
        font-size: var(--text-xs);
        color: var(--gray-600);
        font-family: var(--font-hebrew);
    }

    .logout-button {
        width: 100%;
        background: var(--gray-100);
        color: var(--gray-700);
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-2) var(--space-4);
        font-size: var(--text-sm);
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }

    .logout-button:hover {
        background: var(--gray-200);
    }

    @media (max-width: 768px) {
        .modern-sidebar {
            transform: translateX(100%);
        }

        .modern-sidebar.open {
            transform: translateX(0);
        }

        .sidebar-toggle {
            display: block;
        }
    }
    </style>

    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('.modern-sidebar');
        sidebar.classList.toggle('open');
    }
    </script>
    """

    st.markdown(sidebar_css, unsafe_allow_html=True)



