#!/usr/bin/env python3
"""
Modern Design System for Omri Association Dashboard
Comprehensive design tokens following modern design principles
"""

class ModernDesignSystem:
    """Centralized design system with modern tokens"""
    
    # Modern Color Palette (Light Theme Only)
    COLORS = {
        # Primary Brand
        'primary': '#2563eb',           # Modern blue
        'primary_50': '#eff6ff',
        'primary_100': '#dbeafe', 
        'primary_500': '#3b82f6',
        'primary_600': '#2563eb',
        'primary_700': '#1d4ed8',
        
        # Semantic Colors
        'success': '#10b981',           # Emerald
        'success_50': '#ecfdf5',
        'success_100': '#d1fae5',
        'warning': '#f59e0b',           # Amber
        'warning_50': '#fffbeb',
        'warning_100': '#fef3c7',
        'error': '#ef4444',             # Red
        'error_50': '#fef2f2',
        'error_100': '#fee2e2',
        'info': '#06b6d4',              # Cyan
        'info_50': '#ecfeff',
        'info_100': '#cffafe',
        
        # Neutral Scale
        'gray_50': '#f9fafb',
        'gray_100': '#f3f4f6',
        'gray_200': '#e5e7eb',
        'gray_300': '#d1d5db',
        'gray_400': '#9ca3af',
        'gray_500': '#6b7280',
        'gray_600': '#4b5563',
        'gray_700': '#374151',
        'gray_800': '#1f2937',
        'gray_900': '#111827',
        
        # Surface Colors
        'background': '#ffffff',
        'surface': '#f8fafc',
        'surface_elevated': '#ffffff',
        'border': '#e2e8f0',
        'border_light': '#f1f5f9',
    }
    
    # Modern Typography Scale
    TYPOGRAPHY = {
        'font_family': '"Inter", "Noto Sans Hebrew", system-ui, sans-serif',
        'font_hebrew': '"Noto Sans Hebrew", "Assistant", system-ui, sans-serif',
        
        'text_xs': {'size': '0.75rem', 'line_height': '1rem', 'weight': '400'},
        'text_sm': {'size': '0.875rem', 'line_height': '1.25rem', 'weight': '400'},
        'text_base': {'size': '1rem', 'line_height': '1.5rem', 'weight': '400'},
        'text_lg': {'size': '1.125rem', 'line_height': '1.75rem', 'weight': '400'},
        'text_xl': {'size': '1.25rem', 'line_height': '1.75rem', 'weight': '500'},
        'text_2xl': {'size': '1.5rem', 'line_height': '2rem', 'weight': '600'},
        'text_3xl': {'size': '1.875rem', 'line_height': '2.25rem', 'weight': '700'},
        'text_4xl': {'size': '2.25rem', 'line_height': '2.5rem', 'weight': '800'},
    }
    
    # Spacing Scale (4px base unit) - expose both numeric and `space_` keys
    _SPACING_BASE = {
        '0': '0px', '1': '4px', '2': '8px', '3': '12px', '4': '16px',
        '5': '20px', '6': '24px', '8': '32px', '10': '40px', '12': '48px',
        '16': '64px', '20': '80px', '24': '96px', '32': '128px'
    }
    SPACING = {**_SPACING_BASE, **{f'space_{key}': value for key, value in _SPACING_BASE.items()}}
    
    # Border Radius Scale
    _BORDER_RADIUS_BASE = {
        'none': '0px', 'sm': '4px', 'md': '8px', 'lg': '12px', 
        'xl': '16px', '2xl': '24px', 'full': '9999px'
    }
    BORDER_RADIUS = {**_BORDER_RADIUS_BASE, **{f'radius_{key}': value for key, value in _BORDER_RADIUS_BASE.items()}}
    
    # Shadow Scale
    _SHADOWS_BASE = {
        'none': 'none',
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    }
    SHADOWS = {**_SHADOWS_BASE, **{f'shadow_{key}': value for key, value in _SHADOWS_BASE.items()}}
    
    # Breakpoints
    BREAKPOINTS = {
        'mobile': '768px',
        'tablet': '1024px',
        'desktop': '1200px',
        'wide': '1400px'
    }

def get_modern_css():
    """Generate modern CSS with design system tokens"""
    return f"""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@400;500;600;700&display=swap');
    
    /* CSS Variables for Design System */
    :root {{
        /* Colors */
        --primary: {ModernDesignSystem.COLORS['primary']};
        --primary-50: {ModernDesignSystem.COLORS['primary_50']};
        --primary-100: {ModernDesignSystem.COLORS['primary_100']};
        --primary-500: {ModernDesignSystem.COLORS['primary_500']};
        --primary-600: {ModernDesignSystem.COLORS['primary_600']};
        --primary-700: {ModernDesignSystem.COLORS['primary_700']};
        
        --success: {ModernDesignSystem.COLORS['success']};
        --success-50: {ModernDesignSystem.COLORS['success_50']};
        --success-100: {ModernDesignSystem.COLORS['success_100']};
        --warning: {ModernDesignSystem.COLORS['warning']};
        --warning-50: {ModernDesignSystem.COLORS['warning_50']};
        --warning-100: {ModernDesignSystem.COLORS['warning_100']};
        --error: {ModernDesignSystem.COLORS['error']};
        --error-50: {ModernDesignSystem.COLORS['error_50']};
        --error-100: {ModernDesignSystem.COLORS['error_100']};
        --info: {ModernDesignSystem.COLORS['info']};
        --info-50: {ModernDesignSystem.COLORS['info_50']};
        --info-100: {ModernDesignSystem.COLORS['info_100']};
        
        --gray-50: {ModernDesignSystem.COLORS['gray_50']};
        --gray-100: {ModernDesignSystem.COLORS['gray_100']};
        --gray-200: {ModernDesignSystem.COLORS['gray_200']};
        --gray-300: {ModernDesignSystem.COLORS['gray_300']};
        --gray-400: {ModernDesignSystem.COLORS['gray_400']};
        --gray-500: {ModernDesignSystem.COLORS['gray_500']};
        --gray-600: {ModernDesignSystem.COLORS['gray_600']};
        --gray-700: {ModernDesignSystem.COLORS['gray_700']};
        --gray-800: {ModernDesignSystem.COLORS['gray_800']};
        --gray-900: {ModernDesignSystem.COLORS['gray_900']};
        
        --background: {ModernDesignSystem.COLORS['background']};
        --surface: {ModernDesignSystem.COLORS['surface']};
        --surface-elevated: {ModernDesignSystem.COLORS['surface_elevated']};
        --border: {ModernDesignSystem.COLORS['border']};
        --border-light: {ModernDesignSystem.COLORS['border_light']};
        
        /* Typography */
        --font-family: {ModernDesignSystem.TYPOGRAPHY['font_family']};
        --font-hebrew: {ModernDesignSystem.TYPOGRAPHY['font_hebrew']};
        
        /* Spacing */
        --space-0: {ModernDesignSystem.SPACING['0']};
        --space-1: {ModernDesignSystem.SPACING['1']};
        --space-2: {ModernDesignSystem.SPACING['2']};
        --space-3: {ModernDesignSystem.SPACING['3']};
        --space-4: {ModernDesignSystem.SPACING['4']};
        --space-5: {ModernDesignSystem.SPACING['5']};
        --space-6: {ModernDesignSystem.SPACING['6']};
        --space-8: {ModernDesignSystem.SPACING['8']};
        --space-10: {ModernDesignSystem.SPACING['10']};
        --space-12: {ModernDesignSystem.SPACING['12']};
        --space-16: {ModernDesignSystem.SPACING['16']};
        --space-20: {ModernDesignSystem.SPACING['20']};
        --space-24: {ModernDesignSystem.SPACING['24']};
        --space-32: {ModernDesignSystem.SPACING['32']};
        
        /* Border Radius */
        --radius-none: {ModernDesignSystem.BORDER_RADIUS['none']};
        --radius-sm: {ModernDesignSystem.BORDER_RADIUS['sm']};
        --radius-md: {ModernDesignSystem.BORDER_RADIUS['md']};
        --radius-lg: {ModernDesignSystem.BORDER_RADIUS['lg']};
        --radius-xl: {ModernDesignSystem.BORDER_RADIUS['xl']};
        --radius-2xl: {ModernDesignSystem.BORDER_RADIUS['2xl']};
        --radius-full: {ModernDesignSystem.BORDER_RADIUS['full']};
        
        /* Shadows */
        --shadow-none: {ModernDesignSystem.SHADOWS['none']};
        --shadow-sm: {ModernDesignSystem.SHADOWS['sm']};
        --shadow-md: {ModernDesignSystem.SHADOWS['md']};
        --shadow-lg: {ModernDesignSystem.SHADOWS['lg']};
        --shadow-xl: {ModernDesignSystem.SHADOWS['xl']};
    }}
    
    /* Global Reset and Base Styles */
    * {{
        box-sizing: border-box;
    }}
    
    /* RTL Support */
    [data-testid="stAppViewContainer"] {{
        direction: rtl;
        text-align: right;
        font-family: var(--font-hebrew);
        background-color: var(--surface);
        color: var(--gray-900);
    }}
    
    /* Modern Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--gray-900);
        font-weight: 600;
        margin-bottom: var(--space-4);
        font-family: var(--font-hebrew);
    }}
    
    h1 {{ font-size: {ModernDesignSystem.TYPOGRAPHY['text_4xl']['size']}; }}
    h2 {{ font-size: {ModernDesignSystem.TYPOGRAPHY['text_3xl']['size']}; }}
    h3 {{ font-size: {ModernDesignSystem.TYPOGRAPHY['text_2xl']['size']}; }}
    h4 {{ font-size: {ModernDesignSystem.TYPOGRAPHY['text_xl']['size']}; }}
    
    /* Modern Cards */
    .metric-card-modern {{
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: var(--space-4);
    }}
    
    .metric-card-modern:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }}
    
    .metric-card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-2);
    }}
    
    .metric-card-title {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']['size']};
        font-weight: 500;
        color: var(--gray-600);
        margin: 0;
    }}
    
    .metric-card-icon {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_lg']['size']};
        opacity: 0.7;
    }}
    
    .metric-card-value {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_3xl']['size']};
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: var(--space-1);
        line-height: 1.2;
    }}
    
    .metric-card-change {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']['size']};
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: var(--space-1);
    }}
    
    /* Info Cards */
    .info-card-modern {{
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        margin-bottom: var(--space-4);
    }}
    
    .info-card-title {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_lg']['size']};
        font-weight: 600;
        color: var(--gray-900);
        margin: 0 0 var(--space-3) 0;
    }}
    
    .info-card-content {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_base']['size']};
        color: var(--gray-600);
        margin: 0 0 var(--space-4) 0;
        line-height: 1.5;
    }}
    
    .info-card-action {{
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-2) var(--space-4);
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']['size']};
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .info-card-action:hover {{
        background: var(--primary-700);
        transform: translateY(-1px);
    }}
    
    /* Page Layout */
    .page-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--space-6) var(--space-4);
    }}
    
    .section-header-modern {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--space-8);
        padding-bottom: var(--space-4);
        border-bottom: 1px solid var(--border);
    }}
    
    .section-title {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_2xl']['size']};
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
        font-family: var(--font-hebrew);
    }}
    
    .section-subtitle {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_base']['size']};
        color: var(--gray-600);
        margin: var(--space-1) 0 0 0;
        font-family: var(--font-hebrew);
    }}
    
    .section-actions {{
        display: flex;
        gap: var(--space-2);
        align-items: center;
    }}
    
    /* Modern Sidebar */
    .sidebar-modern {{
        background: var(--surface-elevated);
        border-left: 1px solid var(--border);
        height: 100vh;
        padding: var(--space-6);
        position: fixed;
        right: 0;
        top: 0;
        width: 280px;
        z-index: 1000;
        overflow-y: auto;
    }}
    
    .sidebar-header {{
        margin-bottom: var(--space-8);
        padding-bottom: var(--space-4);
        border-bottom: 1px solid var(--border);
    }}
    
    .sidebar-title {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_xl']['size']};
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
        font-family: var(--font-hebrew);
    }}
    
    .sidebar-subtitle {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']['size']};
        color: var(--gray-600);
        margin: var(--space-1) 0 0 0;
        font-family: var(--font-hebrew);
    }}
    
    .nav-list {{
        list-style: none;
        margin: 0;
        padding: 0;
    }}
    
    .nav-item {{
        margin-bottom: var(--space-1);
    }}
    
    .nav-link {{
        display: flex;
        align-items: center;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-md);
        text-decoration: none;
        color: var(--gray-700);
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }}
    
    .nav-link:hover {{
        background: var(--gray-100);
        color: var(--gray-900);
    }}
    
    .nav-item.active .nav-link {{
        background: var(--primary-50);
        color: var(--primary-700);
    }}
    
    .nav-icon {{
        margin-left: var(--space-3);
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_lg']['size']};
    }}
    
    .nav-text {{
        font-size: {ModernDesignSystem.TYPOGRAPHY['text_sm']['size']};
        font-weight: 500;
    }}
    
    /* Responsive Design */
    @media (max-width: {ModernDesignSystem.BREAKPOINTS['mobile']}) {{
        .page-container {{
            padding: var(--space-4) var(--space-3);
        }}
        
        .metric-card-modern {{
            margin-bottom: var(--space-3);
            padding: var(--space-4);
        }}
        
        .section-header-modern {{
            flex-direction: column;
            gap: var(--space-4);
        }}
        
        .section-title {{
            font-size: {ModernDesignSystem.TYPOGRAPHY['text_xl']['size']};
        }}
        
        .sidebar-modern {{
            transform: translateX(100%);
            transition: transform 0.3s ease;
        }}
        
        .sidebar-modern.open {{
            transform: translateX(0);
        }}
    }}
    
    @media (max-width: 480px) {{
        .page-container {{
            padding: var(--space-3) var(--space-2);
        }}
        
        .metric-card-modern {{
            padding: var(--space-4);
        }}
        
        .metric-card-value {{
            font-size: {ModernDesignSystem.TYPOGRAPHY['text_2xl']['size']};
        }}
    }}
    
    /* Micro-interactions */
    .loading-shimmer {{
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    /* Override Streamlit default styles */
    .stButton > button {{
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-2) var(--space-4);
        font-weight: 500;
        transition: all 0.2s ease;
        font-family: var(--font-hebrew);
    }}
    
    .stButton > button:hover {{
        background-color: var(--primary-700);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }}
    
    .stMetric {{
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        box-shadow: var(--shadow-sm);
    }}
    
    .stDataFrame {{
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }}
    
    .stAlert {{
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-sm);
    }}
    
    /* Main Content Area */
    .main .block-container {{
        padding-top: var(--space-8);
        padding-bottom: var(--space-8);
        max-width: 1200px;
    }}
    
    /* Activity Items */
    .activity-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-3) var(--space-4);
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        margin-bottom: var(--space-2);
        transition: all 0.2s ease;
    }}
    
    .activity-item:hover {{
        background: var(--gray-50);
        border-color: var(--primary-200);
    }}
    
    .activity-content {{
        display: flex;
        flex-direction: column;
        gap: var(--space-1);
    }}
    
    .activity-amount {{
        font-weight: 600;
        color: var(--gray-900);
        font-size: var(--text-base);
    }}
    
    .activity-date {{
        font-size: var(--text-sm);
        color: var(--gray-500);
    }}
    
    /* Modern Alerts */
    .modern-alert {{
        padding: var(--space-4);
        border-radius: var(--radius-lg);
        margin-bottom: var(--space-3);
        display: flex;
        align-items: center;
        gap: var(--space-3);
        background: var(--surface-elevated);
        box-shadow: var(--shadow-sm);
    }}
    
    .alert-content {{
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }}
    
    .alert-icon {{
        font-size: var(--text-lg);
    }}
    
    .alert-message {{
        font-size: var(--text-sm);
        color: var(--gray-700);
        font-family: var(--font-hebrew);
    }}
    
    /* Chart Cards */
    .chart-card {{
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--space-4);
    }}
    
    .chart-card-title {{
        font-size: var(--text-lg);
        font-weight: 600;
        color: var(--gray-900);
        margin: 0 0 var(--space-4) 0;
        font-family: var(--font-hebrew);
    }}
    
    .chart-empty-state {{
        text-align: center;
        padding: var(--space-8);
        color: var(--gray-500);
    }}
    
    /* Page Actions */
    .page-action-button {{
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
    }}
    
    .page-action-button:hover {{
        background: var(--primary-700);
        transform: translateY(-1px);
    }}
    
    .page-action-button.secondary {{
        background: var(--gray-100);
        color: var(--gray-700);
    }}
    
    .page-action-button.secondary:hover {{
        background: var(--gray-200);
    }}
    </style>
    """
