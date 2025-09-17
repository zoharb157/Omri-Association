#!/usr/bin/env python3
"""
Responsive Design Components for Omri Association Dashboard
Mobile-first responsive design system
"""

import streamlit as st


def create_responsive_container():
    """Create a responsive container with proper breakpoints"""

    container_css = """
    <style>
    /* Mobile-first responsive container */
    .responsive-container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--space-4);
    }

    @media (min-width: 768px) {
        .responsive-container {
            padding: var(--space-6) var(--space-8);
        }
    }

    @media (min-width: 1024px) {
        .responsive-container {
            padding: var(--space-8) var(--space-12);
        }
    }

    @media (min-width: 1200px) {
        .responsive-container {
            padding: var(--space-8) var(--space-16);
        }
    }
    </style>
    """

    st.markdown(container_css, unsafe_allow_html=True)

def create_responsive_grid(items: list, columns: int = 4, gap: str = "md"):
    """Create a responsive grid that adapts to screen size"""

    # Define responsive column configurations
    responsive_configs = {
        4: {
            'mobile': 1,
            'tablet': 2,
            'desktop': 4
        },
        3: {
            'mobile': 1,
            'tablet': 2,
            'desktop': 3
        },
        2: {
            'mobile': 1,
            'tablet': 2,
            'desktop': 2
        },
        1: {
            'mobile': 1,
            'tablet': 1,
            'desktop': 1
        }
    }

    config = responsive_configs.get(columns, {1: 1, 2: 2, 4: 4})

    # Create CSS for responsive grid
    grid_css = f"""
    <style>
    .responsive-grid {{
        display: grid;
        gap: var(--space-{gap});
        grid-template-columns: repeat({config['mobile']}, 1fr);
    }}

    @media (min-width: 768px) {{
        .responsive-grid {{
            grid-template-columns: repeat({config['tablet']}, 1fr);
        }}
    }}

    @media (min-width: 1024px) {{
        .responsive-grid {{
            grid-template-columns: repeat({config['desktop']}, 1fr);
        }}
    }}
    </style>
    """

    st.markdown(grid_css, unsafe_allow_html=True)

    # Create the grid using Streamlit columns
    cols = st.columns(columns)
    return cols

def create_mobile_navigation():
    """Create mobile-optimized navigation"""

    mobile_nav_html = """
    <div class="mobile-navigation">
        <div class="mobile-nav-header">
            <h1 class="mobile-nav-title">עמותת עמרי</h1>
            <button class="mobile-nav-toggle" onclick="toggleMobileNav()">
                <span class="hamburger"></span>
            </button>
        </div>

        <nav class="mobile-nav-menu" id="mobileNavMenu">
            <ul class="mobile-nav-list">
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link active">
                        <span class="mobile-nav-icon">🏠</span>
                        <span class="mobile-nav-text">דף הבית</span>
                    </a>
                </li>
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link">
                        <span class="mobile-nav-icon">💰</span>
                        <span class="mobile-nav-text">תקציב</span>
                    </a>
                </li>
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link">
                        <span class="mobile-nav-icon">👥</span>
                        <span class="mobile-nav-text">תורמים</span>
                    </a>
                </li>
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link">
                        <span class="mobile-nav-icon">👩</span>
                        <span class="mobile-nav-text">אלמנות</span>
                    </a>
                </li>
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link">
                        <span class="mobile-nav-icon">🕸️</span>
                        <span class="mobile-nav-text">מפת קשרים</span>
                    </a>
                </li>
                <li class="mobile-nav-item">
                    <a href="#" class="mobile-nav-link">
                        <span class="mobile-nav-icon">🏘️</span>
                        <span class="mobile-nav-text">אזורי מגורים</span>
                    </a>
                </li>
            </ul>
        </nav>
    </div>
    """

    st.markdown(mobile_nav_html, unsafe_allow_html=True)

    # Add CSS for mobile navigation
    mobile_nav_css = """
    <style>
    .mobile-navigation {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: var(--surface-elevated);
        border-bottom: 1px solid var(--border);
        z-index: 1000;
        padding: var(--space-4);
    }

    .mobile-nav-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .mobile-nav-title {
        font-size: var(--text-lg);
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
        font-family: var(--font-hebrew);
    }

    .mobile-nav-toggle {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--space-2);
    }

    .hamburger {
        display: block;
        width: 24px;
        height: 2px;
        background: var(--gray-600);
        position: relative;
        transition: all 0.3s ease;
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
        top: -8px;
    }

    .hamburger::after {
        top: 8px;
    }

    .mobile-nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--surface-elevated);
        border-bottom: 1px solid var(--border);
        box-shadow: var(--shadow-lg);
    }

    .mobile-nav-menu.open {
        display: block;
    }

    .mobile-nav-list {
        list-style: none;
        margin: 0;
        padding: var(--space-4);
    }

    .mobile-nav-item {
        margin-bottom: var(--space-2);
    }

    .mobile-nav-link {
        display: flex;
        align-items: center;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-md);
        text-decoration: none;
        color: var(--gray-700);
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }

    .mobile-nav-link:hover {
        background: var(--gray-100);
        color: var(--gray-900);
    }

    .mobile-nav-link.active {
        background: var(--primary-50);
        color: var(--primary-700);
    }

    .mobile-nav-icon {
        margin-left: var(--space-3);
        font-size: var(--text-lg);
    }

    .mobile-nav-text {
        font-size: var(--text-sm);
        font-weight: 500;
    }

    @media (max-width: 768px) {
        .mobile-navigation {
            display: block;
        }
    }
    </style>

    <script>
    function toggleMobileNav() {
        const menu = document.getElementById('mobileNavMenu');
        menu.classList.toggle('open');
    }
    </script>
    """

    st.markdown(mobile_nav_css, unsafe_allow_html=True)

def create_touch_friendly_buttons():
    """Create touch-friendly buttons for mobile devices"""

    button_css = """
    <style>
    /* Touch-friendly button styles */
    .touch-button {
        min-height: 44px;
        min-width: 44px;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-md);
        border: none;
        background: var(--primary);
        color: white;
        font-size: var(--text-base);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--space-2);
    }

    .touch-button:hover {
        background: var(--primary-700);
        transform: translateY(-1px);
    }

    .touch-button:active {
        transform: translateY(0);
    }

    .touch-button.secondary {
        background: var(--gray-100);
        color: var(--gray-700);
    }

    .touch-button.secondary:hover {
        background: var(--gray-200);
    }

    .touch-button.large {
        min-height: 56px;
        padding: var(--space-4) var(--space-6);
        font-size: var(--text-lg);
    }

    .touch-button.small {
        min-height: 36px;
        padding: var(--space-2) var(--space-3);
        font-size: var(--text-sm);
    }

    /* Ensure all interactive elements are touch-friendly */
    button, .stButton > button, .touch-button {
        min-height: 44px;
        min-width: 44px;
    }

    @media (max-width: 768px) {
        .touch-button {
            width: 100%;
            margin-bottom: var(--space-2);
        }
    }
    </style>
    """

    st.markdown(button_css, unsafe_allow_html=True)

def create_responsive_typography():
    """Create responsive typography system"""

    typography_css = """
    <style>
    /* Responsive typography */
    h1 {
        font-size: var(--text-2xl);
        line-height: 1.2;
    }

    h2 {
        font-size: var(--text-xl);
        line-height: 1.3;
    }

    h3 {
        font-size: var(--text-lg);
        line-height: 1.4;
    }

    h4 {
        font-size: var(--text-base);
        line-height: 1.4;
    }

    p, .text-body {
        font-size: var(--text-sm);
        line-height: 1.5;
    }

    .text-small {
        font-size: var(--text-xs);
        line-height: 1.4;
    }

    @media (min-width: 768px) {
        h1 {
            font-size: var(--text-3xl);
        }

        h2 {
            font-size: var(--text-2xl);
        }

        h3 {
            font-size: var(--text-xl);
        }

        h4 {
            font-size: var(--text-lg);
        }

        p, .text-body {
            font-size: var(--text-base);
        }
    }

    @media (min-width: 1024px) {
        h1 {
            font-size: var(--text-4xl);
        }

        h2 {
            font-size: var(--text-3xl);
        }

        h3 {
            font-size: var(--text-2xl);
        }

        h4 {
            font-size: var(--text-xl);
        }
    }
    </style>
    """

    st.markdown(typography_css, unsafe_allow_html=True)

def create_responsive_spacing():
    """Create responsive spacing system"""

    spacing_css = """
    <style>
    /* Responsive spacing */
    .spacing-xs { margin: var(--space-1); }
    .spacing-sm { margin: var(--space-2); }
    .spacing-md { margin: var(--space-4); }
    .spacing-lg { margin: var(--space-6); }
    .spacing-xl { margin: var(--space-8); }

    .padding-xs { padding: var(--space-1); }
    .padding-sm { padding: var(--space-2); }
    .padding-md { padding: var(--space-4); }
    .padding-lg { padding: var(--space-6); }
    .padding-xl { padding: var(--space-8); }

    /* Responsive margins */
    .margin-mobile { margin: var(--space-2); }
    .margin-tablet { margin: var(--space-4); }
    .margin-desktop { margin: var(--space-6); }

    @media (min-width: 768px) {
        .margin-mobile { margin: var(--space-4); }
        .margin-tablet { margin: var(--space-6); }
        .margin-desktop { margin: var(--space-8); }
    }

    @media (min-width: 1024px) {
        .margin-mobile { margin: var(--space-6); }
        .margin-tablet { margin: var(--space-8); }
        .margin-desktop { margin: var(--space-12); }
    }
    </style>
    """

    st.markdown(spacing_css, unsafe_allow_html=True)



