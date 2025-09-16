#!/usr/bin/env python3
"""
Improved Dashboard Layout Module
Modern, responsive layout with design system integration
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional
from .design_system.themes import ThemeManager
from .components.layout import (
    create_section_header, create_container, create_grid,
    add_spacing, create_metric_row, create_two_column_layout,
    create_three_column_layout, create_four_column_layout
)
from .components.cards import create_metric_cards, create_info_cards

class ImprovedDashboardLayout:
    """Modern dashboard layout with design system integration"""
    
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.colors
        self.typography = self.theme_manager.typography
        self.spacing = self.theme_manager.spacing
    
    def create_main_tabs(self) -> List:
        """Create modern tab structure"""
        return st.tabs([
            "🏠 דף הבית", 
            "💰 תקציב", 
            "👥 תורמים", 
            "👩 אלמנות", 
            "🕸️ מפת קשרים",
            "📊 דוחות"
        ])
    
    def create_dashboard_header(self):
        """Create modern dashboard header"""
        # Apply theme CSS
        theme_css = self.theme_manager.get_theme_css('light')
        st.markdown(theme_css, unsafe_allow_html=True)
        
        # Main header
        header_html = f"""
        <div style="
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: white;
            padding: var(--space-6) var(--space-4);
            margin-bottom: var(--space-6);
            border-radius: var(--space-2);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                max-width: 1200px;
                margin: 0 auto;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: var(--space-4);
                ">
                    <div style="
                        background: rgba(255, 255, 255, 0.2);
                        padding: var(--space-3);
                        border-radius: var(--space-2);
                        font-size: 2rem;
                    ">🏢</div>
                    <div>
                        <h1 style="
                            color: white;
                            font-size: var(--text-4xl);
                            font-weight: var(--font-bold);
                            margin: 0;
                        ">מערכת ניהול עמותת עמרי</h1>
                        <p style="
                            color: rgba(255, 255, 255, 0.9);
                            font-size: var(--text-lg);
                            margin: var(--space-1) 0 0 0;
                        ">ניהול תקציב, תורמים ואלמנות</p>
                    </div>
                </div>
                <div style="
                    display: flex;
                    gap: var(--space-2);
                ">
                    {self._create_theme_toggle()}
                    {self._create_refresh_button()}
                </div>
            </div>
        </div>
        """
        
        st.markdown(header_html, unsafe_allow_html=True)
    
    def _create_theme_toggle(self) -> str:
        """Create theme toggle button"""
        return """
        <button onclick="toggleTheme()" style="
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: var(--space-2) var(--space-3);
            border-radius: var(--space-2);
            cursor: pointer;
            font-size: var(--text-sm);
            transition: all 0.2s ease;
        " onmouseover="this.style.background='rgba(255, 255, 255, 0.3)'" 
           onmouseout="this.style.background='rgba(255, 255, 255, 0.2)'">
            🌙 עיצוב
        </button>
        """
    
    def _create_refresh_button(self) -> str:
        """Create refresh button"""
        return """
        <button onclick="window.location.reload()" style="
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: var(--space-2) var(--space-3);
            border-radius: var(--space-2);
            cursor: pointer;
            font-size: var(--text-sm);
            transition: all 0.2s ease;
        " onmouseover="this.style.background='rgba(255, 255, 255, 0.3)'" 
           onmouseout="this.style.background='rgba(255, 255, 255, 0.2)'">
            🔄 רענן
        </button>
        """
    
    def create_overview_section(self, expenses_df: pd.DataFrame, donations_df: pd.DataFrame, 
                               donor_stats: Dict, widow_stats: Dict):
        """Create modern overview section"""
        create_section_header(
            title="📊 סקירה כללית",
            subtitle="תצוגת נתונים מהירה של המצב הנוכחי",
            icon="📊"
        )
        
        # Financial metrics with modern cards
        financial_metrics = [
            {
                'label': 'סך תרומות',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל התרומות שהתקבלו עד כה',
                'icon': '💰',
                'color': 'success'
            },
            {
                'label': 'סך הוצאות',
                'value': f"₪{pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'סך כל ההוצאות שהוצאו עד כה',
                'icon': '💸',
                'color': 'warning'
            },
            {
                'label': 'יתרה זמינה',
                'value': f"₪{pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() - pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum():,.0f}",
                'help': 'יתרה זמינה לפעילות עתידית',
                'icon': '💳',
                'color': 'primary'
            },
            {
                'label': 'אחוז ניצול',
                'value': f"{(pd.to_numeric(expenses_df['שקלים'], errors='coerce').fillna(0).sum() / pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() * 100) if pd.to_numeric(donations_df['שקלים'], errors='coerce').fillna(0).sum() > 0 else 0:.1f}%",
                'help': 'אחוז התרומות שהוצאו',
                'icon': '📈',
                'color': 'info'
            }
        ]
        
        create_metric_cards(financial_metrics, 4)
        add_spacing(3)
        
        # Organizational metrics
        org_metrics = [
            {
                'label': 'מספר תורמים',
                'value': f"{donor_stats.get('total_donors', 0):,}",
                'help': 'סך כל התורמים שתרמו לעמותה',
                'icon': '👥',
                'color': 'success'
            },
            {
                'label': 'מספר אלמנות',
                'value': f"{widow_stats.get('total_widows', 0):,}",
                'help': 'סך כל האלמנות המטופלות על ידי העמותה',
                'icon': '👩',
                'color': 'primary'
            }
        ]
        
        create_metric_cards(org_metrics, 2)
        add_spacing(3)
    
    def create_budget_section(self, expenses_df: pd.DataFrame, donations_df: pd.DataFrame, 
                             budget_status: Dict):
        """Create modern budget section"""
        create_section_header(
            title="💰 ניהול תקציב",
            subtitle="ניתוח תקציבי מפורט והוצאות חודשיות",
            icon="💰"
        )
        
        # Budget status cards
        if budget_status and isinstance(budget_status, dict) and len(budget_status) > 0:
            try:
                monthly_donations = budget_status.get('monthly_donations', {})
                monthly_expenses = budget_status.get('monthly_expenses', {})
                total_monthly_budget = sum(monthly_donations.values()) if monthly_donations else 0
                total_monthly_expenses = sum(monthly_expenses.values()) if monthly_expenses else 0
                available_budget = total_monthly_budget - total_monthly_expenses
                
                budget_metrics = [
                    {
                        'label': 'תקציב חודשי',
                        'value': f"₪{total_monthly_budget:,.0f}",
                        'help': 'סך תקציב חודשי מתרומות',
                        'icon': '📊',
                        'color': 'success'
                    },
                    {
                        'label': 'הוצאות חודשיות',
                        'value': f"₪{total_monthly_expenses:,.0f}",
                        'help': 'סך הוצאות חודשיות',
                        'icon': '💸',
                        'color': 'warning'
                    },
                    {
                        'label': 'יתרה זמינה',
                        'value': f"₪{available_budget:,.0f}",
                        'help': 'יתרה זמינה לחודש הנוכחי',
                        'icon': '💳',
                        'color': 'primary' if available_budget >= 0 else 'error'
                    }
                ]
                
                create_metric_cards(budget_metrics, 3)
                
            except Exception as e:
                st.error("שגיאה בטעינת סטטוס תקציב")
                logging.error(f"Budget status error: {e}")
        else:
            st.warning("⚠️ לא ניתן לטעון נתוני תקציב חודשי")
        
        add_spacing(3)
    
    def create_donors_section(self, donations_df: pd.DataFrame, donor_stats: Dict):
        """Create modern donors section"""
        create_section_header(
            title="👥 ניהול תורמים",
            subtitle="ניתוח תרומות ותורמים",
            icon="👥"
        )
        
        # Donor statistics
        donor_metrics = [
            {
                'label': 'סך תורמים',
                'value': f"{donor_stats.get('total_donors', 0):,}",
                'help': 'מספר תורמים פעילים',
                'icon': '👥',
                'color': 'primary'
            },
            {
                'label': 'תרומה ממוצעת',
                'value': f"₪{donor_stats.get('avg_donation', 0):,.0f}",
                'help': 'תרומה ממוצעת לתורם',
                'icon': '💰',
                'color': 'success'
            },
            {
                'label': 'תרומה מקסימלית',
                'value': f"₪{donor_stats.get('max_donation', 0):,.0f}",
                'help': 'התרומה הגבוהה ביותר',
                'icon': '🏆',
                'color': 'info'
            }
        ]
        
        create_metric_cards(donor_metrics, 3)
        add_spacing(3)
    
    def create_widows_section(self, almanot_df: pd.DataFrame, widow_stats: Dict):
        """Create modern widows section"""
        create_section_header(
            title="👩 ניהול אלמנות",
            subtitle="ניהול ותמיכה באלמנות",
            icon="👩"
        )
        
        # Widow statistics
        widow_metrics = [
            {
                'label': 'סך אלמנות',
                'value': f"{widow_stats.get('total_widows', 0):,}",
                'help': 'מספר אלמנות מטופלות',
                'icon': '👩',
                'color': 'primary'
            },
            {
                'label': 'סך תמיכה חודשית',
                'value': f"₪{widow_stats.get('total_support', 0):,.0f}",
                'help': 'סך תמיכה חודשית באלמנות',
                'icon': '💝',
                'color': 'success'
            }
        ]
        
        create_metric_cards(widow_metrics, 2)
        add_spacing(3)
    
    def create_recent_activity_section(self, expenses_df: pd.DataFrame, donations_df: pd.DataFrame):
        """Create modern recent activity section"""
        create_section_header(
            title="📈 פעילות אחרונה",
            subtitle="תרומות והוצאות אחרונות",
            icon="📈"
        )
        
        col1, col2 = create_two_column_layout()
        
        with col1:
            st.markdown("#### 🎁 תרומות אחרונות")
            try:
                recent_donations = donations_df.sort_values('תאריך', ascending=False).head(5)
                if len(recent_donations) > 0:
                    for _, donation in recent_donations.iterrows():
                        donation_date = donation['תאריך']
                        date_str = donation_date.strftime('%d/%m/%Y') if pd.notna(donation_date) else 'תאריך לא מוגדר'
                        
                        activity_html = f"""
                        <div style="
                            background: var(--color-surface);
                            border: 1px solid var(--color-border);
                            border-radius: var(--space-2);
                            padding: var(--space-3);
                            margin: var(--space-2) 0;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div>
                                <strong>{donation['שם']}</strong>
                                <br>
                                <small style="color: var(--color-text-secondary);">{date_str}</small>
                            </div>
                            <div style="
                                color: var(--color-success);
                                font-weight: var(--font-bold);
                                font-size: var(--text-lg);
                            ">
                                ₪{donation['שקלים']:,.0f}
                            </div>
                        </div>
                        """
                        st.markdown(activity_html, unsafe_allow_html=True)
                else:
                    st.info("אין תרומות להצגה")
            except Exception as e:
                st.error("שגיאה בטעינת תרומות אחרונות")
        
        with col2:
            st.markdown("#### 💸 הוצאות אחרונות")
            try:
                recent_expenses = expenses_df.sort_values('תאריך', ascending=False).head(5)
                if len(recent_expenses) > 0:
                    for _, expense in recent_expenses.iterrows():
                        expense_date = expense['תאריך']
                        date_str = expense_date.strftime('%d/%m/%Y') if pd.notna(expense_date) else 'תאריך לא מוגדר'
                        
                        activity_html = f"""
                        <div style="
                            background: var(--color-surface);
                            border: 1px solid var(--color-border);
                            border-radius: var(--space-2);
                            padding: var(--space-3);
                            margin: var(--space-2) 0;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div>
                                <strong>{expense['שם']}</strong>
                                <br>
                                <small style="color: var(--color-text-secondary);">{date_str}</small>
                            </div>
                            <div style="
                                color: var(--color-warning);
                                font-weight: var(--font-bold);
                                font-size: var(--text-lg);
                            ">
                                ₪{expense['שקלים']:,.0f}
                            </div>
                        </div>
                        """
                        st.markdown(activity_html, unsafe_allow_html=True)
                else:
                    st.info("אין הוצאות להצגה")
            except Exception as e:
                st.error("שגיאה בטעינת הוצאות אחרונות")
        
        add_spacing(3)

# Convenience functions for backward compatibility
def create_main_tabs():
    """Create main tab structure"""
    layout = ImprovedDashboardLayout()
    return layout.create_main_tabs()

def create_dashboard_header():
    """Create dashboard header"""
    layout = ImprovedDashboardLayout()
    layout.create_dashboard_header()

def create_section_header(title: str, subtitle: str = None, icon: str = None):
    """Create section header"""
    create_section_header(title, subtitle, icon)

def add_spacing(rem: float = 2):
    """Add spacing"""
    add_spacing(rem)

def create_metric_row(metrics: list, columns: int = 4):
    """Create metric row"""
    create_metric_row(metrics, columns)

def create_two_column_layout():
    """Create two column layout"""
    return create_two_column_layout()

def create_three_column_layout():
    """Create three column layout"""
    return create_three_column_layout()
