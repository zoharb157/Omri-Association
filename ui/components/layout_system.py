def create_modern_navbar(active_section: str = "overview"):
    """Create a modern navigation bar/header for the dashboard."""
    nav_items = [
        {"id": "overview", "label": "סקירה", "icon": "🏠"},
        {"id": "charts", "label": "תרשימים", "icon": "📊"},
        {"id": "activity", "label": "פעילות", "icon": "🕒"},
        {"id": "alerts", "label": "התראות", "icon": "⚠️"},
    ]
    nav_html = """
    <nav class="modern-navbar">
        <div class="navbar-brand">עמותת עמרי</div>
        <ul class="navbar-list">
    """
    import streamlit as st
    nav_html_items = ""
    for item in nav_items:
        active_class = "active" if item["id"] == active_section else ""
        nav_html_items += (
            f"<li class='navbar-item {active_class}'>"
            f"<a href='#' class='navbar-link' onclick=\"window.location.hash='#{{}}';window.location.reload();return false;\">{{}} {{}}</a></li>".format(item['id'], item['icon'], item['label'])
        )
    nav_html += nav_html_items
    nav_html += """
        </ul>
    </nav>
    <style>
    .modern-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #fff;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        font-family: inherit;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .navbar-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2563eb;
        letter-spacing: 0.02em;
    }
    .navbar-list {
        display: flex;
        gap: 2rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    .navbar-item {}
    .navbar-link {
        text-decoration: none;
        color: #374151;
        font-size: 1.1rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        transition: background 0.2s, color 0.2s;
    }
    .navbar-item.active .navbar-link,
    .navbar-link:hover {
        background: #2563eb;
        color: #fff;
    }
    </style>
    """
    st.markdown(nav_html, unsafe_allow_html=True)


def create_modern_sidebar():
    """Create a modern sidebar navigation"""

    sidebar_html = """
    <div class="sidebar-modern">
        <div class="sidebar-header">
            <h1 class="sidebar-title">עמותת עמרי</h1>
            <p class="sidebar-subtitle">מערכת ניהול</p>
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
    </div>
    """

    st.markdown(sidebar_html, unsafe_allow_html=True)

def create_modern_header():
    """Create a modern dashboard header"""

    header_html = """
    <div class="modern-header">
        <div class="header-content">
            <div class="header-title">
                <h1>מערכת ניהול עמותת עמרי</h1>
                <p>סקירה מקיפה של מצב העמותה</p>
            </div>
            <div class="header-actions">
                <button class="header-button">🔄 רענן נתונים</button>
                <button class="header-button">⚙️ הגדרות</button>
            </div>
        </div>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

def create_responsive_grid(items: list, columns: int = 4):
    """Create a responsive grid layout"""

    # Determine responsive columns based on screen size
    if columns == 4:
        pass
    elif columns == 3:
        pass
    elif columns == 2:
        pass
    else:
        pass

    # Create columns
    cols = st.columns(columns)

    return cols

def create_card_section(title: str, content: str, actions: list = None):
    """Create a card section with title and content"""

    actions_html = ""
    if actions:
        actions_html = f'<div class="card-actions">{"".join(actions)}</div>'

    section_html = f"""
    <div class="card-section">
        <div class="card-section-header">
            <h3 class="card-section-title">{title}</h3>
            {actions_html}
        </div>
        <div class="card-section-content">
            {content}
        </div>
    </div>
    """

    st.markdown(section_html, unsafe_allow_html=True)

def create_modern_alert(message: str, alert_type: str = "info"):
    """Create a modern alert component"""

    # Map alert types to colors
    alert_colors = {
        'info': ModernDesignSystem.COLORS['info'],
        'success': ModernDesignSystem.COLORS['success'],
        'warning': ModernDesignSystem.COLORS['warning'],
        'error': ModernDesignSystem.COLORS['error']
    }

    alert_icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }

    color = alert_colors.get(alert_type, ModernDesignSystem.COLORS['info'])
    icon = alert_icons.get(alert_type, 'ℹ️')

    alert_html = f"""
    <div class="modern-alert" style="border-left: 4px solid {color};">
        <div class="alert-content">
            <span class="alert-icon">{icon}</span>
            <span class="alert-message">{message}</span>
        </div>
    </div>
    """

    st.markdown(alert_html, unsafe_allow_html=True)

def create_modern_button(text: str, button_type: str = "primary", size: str = "md"):
    """Create a modern button component"""

    # Button type styles
    button_styles = {
        'primary': 'background: var(--primary); color: white;',
        'secondary': 'background: var(--gray-100); color: var(--gray-700);',
        'success': 'background: var(--success); color: white;',
        'warning': 'background: var(--warning); color: white;',
        'error': 'background: var(--error); color: white;'
    }

    # Button sizes
    button_sizes = {
        'sm': 'padding: var(--space-1) var(--space-3); font-size: var(--text-sm);',
        'md': 'padding: var(--space-2) var(--space-4); font-size: var(--text-base);',
        'lg': 'padding: var(--space-3) var(--space-6); font-size: var(--text-lg);'
    }

    style = button_styles.get(button_type, button_styles['primary'])
    size_style = button_sizes.get(size, button_sizes['md'])

    button_html = f"""
    <button class="modern-button" style="{style} {size_style}">
        {text}
    </button>
    """

    st.markdown(button_html, unsafe_allow_html=True)

def create_modern_progress_bar(progress: float, label: str = None):
    """Create a modern progress bar"""

    progress_html = f"""
    <div class="modern-progress">
        {f'<div class="progress-label">{label}</div>' if label else ''}
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
        <div class="progress-text">{progress:.1f}%</div>
    </div>
    """

    st.markdown(progress_html, unsafe_allow_html=True)

def create_section_header(title: str, subtitle: str = None, actions: list = None):
    """Create a modern section header"""
    actions_html = ""
    if actions:
        actions_html = f'<div class="section-actions">{"".join(actions)}</div>'

    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ''

    header_html = f"""
    <div class="section-header-modern">
        <div class="section-header-content">
            <h2 class="section-title">{title}</h2>
            {subtitle_html}
        </div>
        {actions_html}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def create_metrics_grid(metrics: list, columns: int = 4):
    """Create a responsive metrics grid"""
    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        with cols[i]:
            create_metric_card(
                title=metric['title'],
                value=metric['value'],
                change=metric.get('change'),
                change_type=metric.get('change_type', 'neutral'),
                icon=metric.get('icon')
            )

def create_metric_card(title: str, value: str, change: str = None,
                      change_type: str = "positive", icon: str = None):
    """Create a modern metric card with proper styling"""

    # Determine change color and icon
    change_colors = {
        'positive': ModernDesignSystem.COLORS['success'],
        'negative': ModernDesignSystem.COLORS['error'],
        'neutral': ModernDesignSystem.COLORS['gray_600'],
        'warning': ModernDesignSystem.COLORS['warning']
    }

    change_icons = {
        'positive': '↗️',
        'negative': '↘️',
        'neutral': '→',
        'warning': '⚠️'
    }

    change_color = change_colors.get(change_type, ModernDesignSystem.COLORS['gray_600'])
    change_icon = change_icons.get(change_type, '→')

    icon_html = f'<span class="metric-card-icon">{icon}</span>' if icon else ''
    change_html = f'''<div class="metric-card-change" style="color: {change_color}">
        {change_icon} {change}
    </div>''' if change else ''
    card_html = f"""
    <div class="metric-card-modern">
        <div class="metric-card-header">
            <span class="metric-card-title">{title}</span>
            {icon_html}
        </div>
        <div class="metric-card-value">{value}</div>
        {change_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)



