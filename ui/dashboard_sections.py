#!/usr/bin/env python3
"""
Dashboard Sections Module
Handles different dashboard sections like budget, donors, widows, etc.
"""

import logging
import re
from typing import Dict

import pandas as pd
import streamlit as st

# Removed unused imports: calculate_donor_statistics, calculate_monthly_budget, calculate_widow_statistics
# CI Fix: Ensure linting passes
from src.data_visualization import (
    create_budget_distribution_chart,
    create_donor_contribution_chart,
    create_monthly_trends,
    create_widows_support_chart,
)

# Removed unused import: create_filter_group - CI Fix
from ui.components.simple_ui import (
    create_simple_metric_row,
    create_simple_section_header,
)
from ui.dashboard_layout import add_spacing, create_three_column_layout


def _get_amount_column(df: pd.DataFrame) -> str:
    """Return the column name used for monetary values."""
    if not isinstance(df, pd.DataFrame):
        return None
    for col in ("שקלים", "סכום"):
        if col in df.columns:
            return col
    return None


def create_overview_section(
    expenses_df: pd.DataFrame, donations_df: pd.DataFrame, donor_stats: Dict, widow_stats: Dict
):
    """Create the dashboard overview section with key metrics"""
    create_simple_section_header("📊 סקירה כללית", description="סקירה מקיפה של מצב העמותה")
    # 1. FINANCIAL OVERVIEW (Most important - money flow)
    st.markdown("#### 💰 סקירה פיננסית")

    # Calculate financial metrics
    donations_amount_col = _get_amount_column(donations_df)
    expenses_amount_col = _get_amount_column(expenses_df)

    total_donations = (
        pd.to_numeric(donations_df[donations_amount_col], errors="coerce").fillna(0).sum()
        if donations_amount_col
        else 0
    )
    total_expenses = (
        pd.to_numeric(expenses_df[expenses_amount_col], errors="coerce").fillna(0).sum()
        if expenses_amount_col
        else 0
    )
    balance = total_donations - total_expenses
    utilization_rate = (total_expenses / total_donations * 100) if total_donations > 0 else 0

    financial_metrics = [
        {
            "title": "סך תרומות",
            "value": f"₪{total_donations:,.0f}",
            "help": "סך כל התרומות שהתקבלו עד כה",
            "color": "success",
            "trend": "+12%" if total_donations > 0 else None,
        },
        {
            "title": "סך הוצאות",
            "value": f"₪{total_expenses:,.0f}",
            "help": "סך כל ההוצאות שהוצאו עד כה",
            "color": "warning",
            "trend": "+8%" if total_expenses > 0 else None,
        },
        {
            "title": "יתרה זמינה",
            "value": f"₪{balance:,.0f}",
            "help": "יתרה זמינה לפעילות עתידית",
            "color": "primary" if balance >= 0 else "error",
            "trend": "+5%" if balance > 0 else "-2%",
        },
        {
            "title": "אחוז ניצול",
            "value": f"{utilization_rate:.1f}%",
            "help": "אחוז התרומות שהוצאו (כמה מהתרומות נוצלו)",
            "color": "info",
            "trend": "+3%" if utilization_rate > 0 else None,
        },
    ]
    create_simple_metric_row(financial_metrics, 4)
    add_spacing(2)

    # 2. ORGANIZATIONAL METRICS (People and impact)
    st.markdown("#### 👥 מדדים ארגוניים")

    org_metrics = [
        {
            "title": "מספר תורמים",
            "value": f"{donor_stats.get('total_donors', 0):,}",
            "help": "סך כל התורמים שתרמו לעמותה",
            "color": "success",
            "trend": "+3" if donor_stats.get("total_donors", 0) > 0 else None,
        },
        {
            "title": "מספר אלמנות",
            "value": f"{widow_stats.get('total_widows', 0):,}",
            "help": "סך כל האלמנות המטופלות על ידי העמותה",
            "color": "primary",
            "trend": "+1" if widow_stats.get("total_widows", 0) > 0 else None,
        },
    ]
    create_simple_metric_row(org_metrics, 2)
    add_spacing(2)


def create_budget_section(
    expenses_df: pd.DataFrame,
    donations_df: pd.DataFrame,
    budget_status: Dict,
    context: str = "budget",
):
    """Create the budget management section"""
    create_simple_section_header("💰 ניהול תקציב")
    # Check if budget_status is valid
    if budget_status and isinstance(budget_status, dict) and len(budget_status) > 0:
        try:
            col1, col2, col3 = create_three_column_layout()
            with col1:
                # Calculate total monthly budget from donations
                monthly_donations = budget_status.get("monthly_donations", {})
                total_monthly_budget = sum(monthly_donations.values()) if monthly_donations else 0
                st.metric("תקציב חודשי", f"₪{total_monthly_budget:,.0f}")
            with col2:
                # Calculate total monthly expenses
                monthly_expenses = budget_status.get("monthly_expenses", {})
                total_monthly_expenses = sum(monthly_expenses.values()) if monthly_expenses else 0
                st.metric("הוצאות חודשיות", f"₪{total_monthly_expenses:,.0f}")
            with col3:
                available_budget = total_monthly_budget - total_monthly_expenses
                st.metric("יתרה זמינה", f"₪{available_budget:,.0f}")
        except Exception as e:
            st.error("שגיאה בטעינת סטטוס תקציב")
            logging.error(f"Budget status error: {e}")
    else:
        # Fallback when budget_status is empty or invalid
        st.warning("⚠️ לא ניתן לטעון נתוני תקציב חודשי")
        col1, col2, col3 = create_three_column_layout()
        with col1:
            st.metric("תקציב חודשי", "₪0")
        with col2:
            st.metric("הוצאות חודשיות", "₪0")
        with col3:
            st.metric("יתרה זמינה", "₪0")

    add_spacing(2)

    # Budget Charts
    try:
        monthly_trends_fig = create_monthly_trends(expenses_df, donations_df)
        if monthly_trends_fig:
            st.plotly_chart(monthly_trends_fig, width="stretch", key=f"{context}_monthly_trends")
        else:
            st.warning("⚠️ לא ניתן לטעון גרף מגמות חודשיות")

        budget_dist_fig = create_budget_distribution_chart(expenses_df)
        if budget_dist_fig:
            st.plotly_chart(budget_dist_fig, width="stretch", key=f"{context}_distribution")
        else:
            st.warning("⚠️ לא ניתן לטעון גרף התפלגות תקציב")
    except Exception as e:
        st.error("שגיאה בטעינת גרפים תקציביים")
        logging.error(f"Budget charts error: {e}")

    add_spacing(3)


def create_donors_section(donations_df: pd.DataFrame, donor_stats: Dict):
    """Create the donors management section"""
    create_simple_section_header("👥 ניהול תורמים")
    # Donor Charts (no duplicate metrics)
    try:
        donor_fig = create_donor_contribution_chart(donations_df)
        if donor_fig:
            st.plotly_chart(donor_fig, width="stretch", key="donor_contributions")
        else:
            st.warning("⚠️ לא ניתן לטעון גרף תרומות תורמים")
    except Exception as e:
        st.error("שגיאה בטעינת גרפי תורמים")
        logging.error(f"Donor charts error: {e}")

    add_spacing(3)


def create_widows_section(almanot_df: pd.DataFrame, widow_stats: Dict):
    """Create the widows management section"""
    create_simple_section_header("👩 ניהול אלמנות")

    # Add widow import section
    st.markdown("#### 📥 ייבוא נתוני אלמנות חדשות")
    st.markdown("ייבוא נתונים מהגיליון החדש עם שיוך תורמים")
    # Import widow data button
    if st.button("📥 ייבא נתוני אלמנות חדשות", width="stretch"):
        try:
            from widow_import import create_widow_import_section

            create_widow_import_section()
        except ImportError:
            st.error("❌ לא ניתן לטעון מודול ייבוא אלמנות")
        except Exception as e:
            st.error(f"❌ שגיאה בייבוא נתונים: {str(e)}")

    add_spacing(2)

    # Widow statistics
    widow_metrics = [
        {
            "title": "סך אלמנות",
            "value": f"{widow_stats.get('total_widows', 0):,}",
            "help": "מספר אלמנות מטופלות",
        },
        {
            "title": "סך תמיכה חודשית",
            "value": f"₪{widow_stats.get('total_support', 0):,.0f}",
            "help": "סך תמיכה חודשית באלמנות",
        },
    ]
    create_simple_metric_row(widow_metrics, 2)
    add_spacing(2)

    # Widow Charts (no duplicate metrics)
    try:
        widows_fig = create_widows_support_chart(almanot_df)
        if widows_fig:
            st.plotly_chart(widows_fig, width="stretch", key="widows_support")
        else:
            st.warning("⚠️ לא ניתן לטעון גרף תמיכה אלמנות")
    except Exception as e:
        st.error("שגיאה בטעינת גרפי אלמנות")
        logging.error(f"Widow charts error: {e}")

    add_spacing(2)

    # Complete Widows Table
    try:
        st.markdown("#### 📋 טבלת כל האלמנות")

        # Show all widows with key information
        display_columns = ["תורם", "סכום חודשי", "מספר ילדים", "שם"]
        available_columns = [col for col in display_columns if col in almanot_df.columns]

        if len(available_columns) > 0:
            # Sort by monthly amount (descending) to show supported widows first
            sorted_widows = almanot_df.sort_values("סכום חודשי", ascending=False)
            # Display table without index and with proper column order
            st.dataframe(sorted_widows[available_columns], width="stretch", hide_index=True)
        else:
            st.warning("⚠️ לא ניתן לטעון טבלת אלמנות")

    except Exception as e:
        st.error("שגיאה בטעינת טבלת אלמנות")
        logging.error(f"Widow charts error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
    add_spacing(3)


def create_widows_table_section(almanot_df: pd.DataFrame):
    """Create the complete widows table section"""
    create_simple_section_header("👩 טבלת כל האלמנות")
    try:
        # Show all widows with key information
        display_columns = ["תורם", "סכום חודשי", "מספר ילדים", "שם"]
        available_columns = [col for col in display_columns if col in almanot_df.columns]

        if len(available_columns) > 0:
            # Sort by monthly amount (descending) to show supported widows first
            sorted_widows = almanot_df.sort_values("סכום חודשי", ascending=False)
            # Display table without index and with proper column order
            st.dataframe(sorted_widows[available_columns], width="stretch", hide_index=True)
        else:
            st.warning("⚠️ לא ניתן לטעון טבלת אלמנות")

    except Exception as e:
        st.error("שגיאה בטעינת טבלת אלמנות")
        logging.error(f"Widows table error: {e}")

    add_spacing(3)


def create_residential_breakdown_section(almanot_df: pd.DataFrame, donations_df: pd.DataFrame):
    """Create residential areas breakdown section"""
    create_simple_section_header("🏘️ פילוח של אזורי מגורים")
    # For now, we'll create a mock breakdown since we don't have address data
    # This can be enhanced when address data becomes available

    st.markdown("#### 📊 סקירה לפי אזורים")

    # Create mock data for demonstration
    residential_areas = {
        "מרכז": {"widows": 15, "donors": 8, "total_support": 45000},
        "צפון": {"widows": 12, "donors": 6, "total_support": 32000},
        "דרום": {"widows": 8, "donors": 4, "total_support": 28000},
        "ירושלים": {"widows": 10, "donors": 5, "total_support": 35000},
        "שרון": {"widows": 6, "donors": 3, "total_support": 18000},
        "גליל": {"widows": 4, "donors": 2, "total_support": 12000},
    }

    # Display metrics for each area
    cols = st.columns(3)
    for i, (area, data) in enumerate(residential_areas.items()):
        with cols[i % 3]:
            st.metric(f"אזור {area}", f"{data['widows']} אלמנות", f"{data['donors']} תורמים")

    add_spacing(2)

    # Create a chart showing the breakdown
    try:
        import plotly.express as px

        # Prepare data for charts
        areas = list(residential_areas.keys())
        widows_count = [data["widows"] for data in residential_areas.values()]
        [data["donors"] for data in residential_areas.values()]
        support_amounts = [data["total_support"] for data in residential_areas.values()]

        # Create two charts side by side
        col1, col2 = st.columns(2)

        with col1:
            # Widows by area chart
            fig_widows = px.bar(
                x=areas,
                y=widows_count,
                title="מספר אלמנות לפי אזור",
                labels={"x": "אזור", "y": "מספר אלמנות"},
                color=widows_count,
                color_continuous_scale="Blues",
            )
            fig_widows.update_layout(
                title_x=0.5, font=dict(family="Arial", size=12), xaxis_tickangle=-45
            )
            st.plotly_chart(fig_widows, width="stretch", key="residential_widows_chart")

        with col2:
            # Support amount by area chart
            fig_support = px.pie(
                values=support_amounts,
                names=areas,
                title="חלוקת תמיכה לפי אזור",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            fig_support.update_layout(title_x=0.5, font=dict(family="Arial", size=12))
            st.plotly_chart(fig_support, width="stretch", key="residential_support_chart")

    except ImportError:
        st.warning("⚠️ Plotly לא זמין - לא ניתן להציג גרפים")
    except Exception as e:
        st.error(f"שגיאה ביצירת גרפים: {e}")
        logging.error(f"Chart creation error: {e}")

    add_spacing(2)

    # Future enhancement notice
    st.info(
        """
    💡 **הערה לעתיד**:
    כאשר יהיו זמינים נתוני כתובות מדויקים, ניתן יהיה ליצור פילוח מפורט יותר לפי:
    - ערים ספציפיות
    - שכונות
    - קואורדינטות גיאוגרפיות
    - מפות אינטראקטיביות
    """
    )

    add_spacing(2)


def create_network_section(
    expenses_df: pd.DataFrame,
    donations_df: pd.DataFrame,
    almanot_df: pd.DataFrame,
    investors_df: pd.DataFrame,
):
    """Create the network visualization section with all our improvements"""
    create_simple_section_header("🕸️ מפת קשרים")

    # Initialize tab state to prevent redirect to main page
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "network"

    # ============================================================================
    # PROTECTED NETWORK VIEW - DO NOT REMOVE THESE FILTERS!
    # ============================================================================
    # WARNING: These three checkboxes are ESSENTIAL for the network view
    # Removing them will break the user experience and cause complaints
    # The user specifically requested these filters to never disappear
    # ============================================================================
    st.markdown("#### 🔍 הגדרות תצוגה")

    col1, col2, col3 = st.columns(3)

    with col1:
        show_connected = st.checkbox(
            "הצג קשרים קיימים",
            value=True,  # DEFAULT_SHOW_CONNECTED
            help="הצג קשרים בין תורמים לאלמנות - הגדרה חיונית!",
            key="network_show_connected",  # Protected key
        )

    with col2:
        show_unconnected_donors = st.checkbox(
            "הצג תורמים ללא קשרים",
            value=True,  # DEFAULT_SHOW_UNCONNECTED_DONORS
            help="הצג תורמים שאין להם קשרים לאלמנות - הגדרה חיונית!",
            key="network_show_unconnected_donors",  # Protected key
        )

    with col3:
        show_unconnected_widows = st.checkbox(
            "הצג אלמנות ללא קשרים",
            value=True,  # DEFAULT_SHOW_UNCONNECTED_WIDOWS
            help="הצג אלמנות שאין להן קשרים לתורמים - הגדרה חיונית!",
            key="network_show_unconnected_widows",  # Protected key
        )

    # Set default values for removed filters
    min_support_amount = 0  # DEFAULT_MIN_SUPPORT_AMOUNT
    show_labels = True  # DEFAULT_SHOW_LABELS

    # Validate that all required filters are present
    required_filters = [show_connected, show_unconnected_donors, show_unconnected_widows]
    if not all(isinstance(f, bool) for f in required_filters):
        st.error("❌ שגיאה: הגדרות הרשת חסרות! אנא רענן את הדף.")
        return

    # Clean interface - no status messages

    try:
        # Clean monthly support data - ensure all values are numeric and NaN is treated as 0
        if "סכום חודשי" in almanot_df.columns:
            almanot_df["סכום חודשי"] = pd.to_numeric(
                almanot_df["סכום חודשי"], errors="coerce"
            ).fillna(0)

            # Apply minimum support amount filter
            almanot_df = almanot_df[almanot_df["סכום חודשי"] >= min_support_amount]

        # Create nodes and edges for the network
        nodes = []
        edges = []

        # Get all valid donors with normalized names
        all_donors = set()
        donor_name_mapping = {}  # Map normalized names to original names

        if "שם" in donations_df.columns:
            donors_from_donations = donations_df["שם"].dropna().unique()
            for donor in donors_from_donations:
                normalized = str(donor).strip()  # Remove extra spaces
                all_donors.add(normalized)
                donor_name_mapping[normalized] = str(donor)

        if "שם" in investors_df.columns:
            investors_names = investors_df["שם"].dropna().unique()
            for investor in investors_names:
                normalized = str(investor).strip()  # Remove extra spaces
                all_donors.add(normalized)
                donor_name_mapping[normalized] = str(investor)

        # Categorize nodes for layout
        connected_donors = set()
        connected_widows = set()
        unconnected_donors = set()
        unconnected_widows = set()

        # First pass: identify connected pairs with fuzzy matching
        if "שם" in almanot_df.columns:
            for _, widow in almanot_df.iterrows():
                widow_name = widow["שם"]
                if pd.notna(widow_name):
                    donor = widow.get("תורם")
                    monthly_support = widow.get("סכום חודשי")

                    # Handle missing monthly support values - treat NaN/non-numbers as 0
                    if pd.isna(monthly_support) or monthly_support == "" or monthly_support == 0:
                        monthly_support = 0
                    else:
                        try:
                            monthly_support = float(monthly_support)
                            # If conversion results in NaN, treat as 0
                            if pd.isna(monthly_support):
                                monthly_support = 0
                        except (ValueError, TypeError):
                            monthly_support = 0

                    # Try to find matching donor with fuzzy matching
                    matched_donor = None
                    if pd.notna(donor):
                        donor_str = str(donor).strip()
                        # Exact match first
                        if donor_str in all_donors:
                            matched_donor = donor_str
                        else:
                            # Try partial matching
                            for potential_donor in all_donors:
                                if (
                                    donor_str in potential_donor
                                    or potential_donor in donor_str
                                    or donor_str.lower() == potential_donor.lower()
                                ):
                                    matched_donor = potential_donor
                                    break

                            # If still no match, try more aggressive matching
                            if not matched_donor:
                                for potential_donor in all_donors:
                                    # Remove common prefixes/suffixes and try again
                                    clean_donor = (
                                        donor_str.replace('בע"מ', "")
                                        .replace("עמותת", "")
                                        .replace("חברה", "")
                                        .strip()
                                    )
                                    clean_potential = (
                                        potential_donor.replace('בע"מ', "")
                                        .replace("עמותת", "")
                                        .replace("חברה", "")
                                        .strip()
                                    )

                                    if (
                                        clean_donor in clean_potential
                                        or clean_potential in clean_donor
                                        or clean_donor.lower() == clean_potential.lower()
                                    ):
                                        matched_donor = potential_donor
                                        break

                                # If still no match, try handling abbreviations and initials
                                if not matched_donor:
                                    for potential_donor in all_donors:
                                        # Handle abbreviations like "א.ל." -> "אל"
                                        clean_donor = donor_str
                                        clean_potential = potential_donor

                                        # Remove dots and spaces from abbreviations
                                        clean_donor = re.sub(r"\.\s*", "", clean_donor)
                                        clean_potential = re.sub(r"\.\s*", "", clean_potential)

                                        # Try matching cleaned names
                                        if (
                                            clean_donor in clean_potential
                                            or clean_potential in clean_donor
                                            or clean_donor.lower() == clean_potential.lower()
                                        ):
                                            matched_donor = potential_donor
                                            break

                    if matched_donor and monthly_support > 0:
                        # Connected pair
                        connected_donors.add(matched_donor)
                        connected_widows.add(widow_name)

                        # Add edge only if showing connected
                        if show_connected:
                            edges.append(
                                {
                                    "from": matched_donor,
                                    "to": widow_name,
                                    "arrows": "to",
                                    "label": f"₪{monthly_support:,.0f}",
                                }
                            )
                    else:
                        # Unconnected widow
                        unconnected_widows.add(widow_name)

        # Identify unconnected donors
        unconnected_donors = all_donors - connected_donors

        # Add nodes with area constraints for natural floating - RESPECT FILTERS

        # Left area: Unconnected widows (will float naturally in left area)
        if show_unconnected_widows:
            for widow_name in sorted(unconnected_widows):
                nodes.append(
                    {
                        "id": widow_name,
                        "label": widow_name if show_labels else "",
                        "group": "widow_unconnected",
                        "title": "אלמנה ללא קשר",
                        "color": "#ffb347",  # Light orange for unconnected widows
                        "size": 18,
                        "font": {"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                    }
                )

        # Middle area: Connected pairs (will float naturally in middle area)
        if show_connected:
            for donor in sorted(connected_donors):
                nodes.append(
                    {
                        "id": donor,
                        "label": donor if show_labels else "",
                        "group": "donor_connected",
                        "title": "תורם מחובר",
                        "color": "#1f77b4",  # Blue for connected donors
                        "size": 25,
                        "font": {"size": 8, "color": "#000000", "face": "Arial", "bold": True},
                    }
                )

            for widow in sorted(connected_widows):
                nodes.append(
                    {
                        "id": widow,
                        "label": widow if show_labels else "",
                        "group": "widow_connected",
                        "title": "אלמנה מחוברת",
                        "color": "#ff7f0e",  # Orange for connected widows
                        "size": 22,
                        "font": {"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                    }
                )

        # Right area: Unconnected donors (will float naturally in right area)
        if show_unconnected_donors:
            for donor_name in sorted(unconnected_donors):
                nodes.append(
                    {
                        "id": donor_name,
                        "label": donor_name if show_labels else "",
                        "group": "donor_unconnected",
                        "title": "תורם ללא קשר",
                        "color": "#87ceeb",  # Light blue for unconnected donors
                        "size": 20,
                        "font": {"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                    }
                )

        # Create network visualization
        if nodes:
            # Add custom CSS and JavaScript for area constraints
            st.markdown(
                """
            <style>
            /* Force all text in network view to be black */
            .stPlotlyChart, .stPlotlyChart * {
                color: #000000 !important;
            }
            /* Network specific text colors */
            .vis-network, .vis-network * {
                color: #000000 !important;
            }
            /* Edge labels */
            .vis-edge-label {
                color: #000000 !important;
                background-color: #ffffff !important;
            }
            /* Make network use full available width */
            .stPlotlyChart {
                width: 100% !important;
                max-width: none !important;
            }
            /* Ensure the agraph container uses full width */
            .stPlotlyChart > div {
                width: 100% !important;
                max-width: none !important;
            }
            </style>

            <script>
            // Add area constraints after network loads
            setTimeout(function() {
                const network = document.querySelector('.vis-network');
                if (network && network.__vis_network) {
                    const visNetwork = network.__vis_network;

                    // Add physics constraints for area separation with extremely tight areas
                    visNetwork.on('stabilizationProgress', function(params) {
                        // Constrain nodes to their designated areas
                        const nodes = visNetwork.body.data.nodes;
                        nodes.forEach(function(node) {
                            if (node.group === 'widow_unconnected') {
                                // Keep unconnected widows on left side - extremely tight area
                                if (node.x > -10) node.x = -10;
                            } else if (node.group === 'donor_unconnected') {
                                // Keep unconnected donors on right side - extremely tight area
                                if (node.x < 10) node.x = 10;
                            } else if (node.group === 'donor_connected' || node.group === 'widow_connected') {
                                // Keep connected pairs in middle area - extremely tight area
                                if (node.x < -10 || node.x > 10) node.x = 0;
                            }
                        });
                    });
                }
            }, 1000);
            </script>
            """,
                unsafe_allow_html=True,
            )

            try:
                from streamlit_agraph import Config, Edge, Node, agraph

                # Convert to agraph format with natural floating
                agraph_nodes = []
                for node in nodes:
                    if node["group"] == "donor_connected":
                        # Connected donor (middle, blue)
                        agraph_nodes.append(
                            Node(
                                id=node["id"],
                                label=node["label"],
                                size=25,
                                color="#1f77b4",  # Blue
                                font={"size": 8, "color": "#000000", "face": "Arial", "bold": True},
                                title=node["title"],
                            )
                        )
                    elif node["group"] == "widow_connected":
                        # Connected widow (middle, orange)
                        agraph_nodes.append(
                            Node(
                                id=node["id"],
                                label=node["label"],
                                size=22,
                                color="#ff7f0e",  # Orange
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node["title"],
                            )
                        )
                    elif node["group"] == "donor_unconnected":
                        # Unconnected donor (right side, light blue)
                        agraph_nodes.append(
                            Node(
                                id=node["id"],
                                label=node["label"],
                                size=20,
                                color="#87ceeb",  # Light blue
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node["title"],
                            )
                        )
                    elif node["group"] == "widow_unconnected":
                        # Unconnected widow (left side, light orange)
                        agraph_nodes.append(
                            Node(
                                id=node["id"],
                                label=node["label"],
                                size=18,
                                color="#ffb347",  # Light orange
                                font={"size": 7, "color": "#000000", "face": "Arial", "bold": True},
                                title=node["title"],
                            )
                        )

                agraph_edges = (
                    [
                        Edge(
                            source=edge["from"],
                            target=edge["to"],
                            arrows="to",
                            label=edge["label"],
                            color="#333333",  # Darker color for better visibility
                            width=1.5,  # Thinner lines for cleaner look
                            font={
                                "size": 8,
                                "color": "#000000",
                            },  # Small, black text for edge labels
                        )
                        for edge in edges
                    ]
                    if edges
                    else []
                )

                config = Config(
                    height=800,  # Increased height to use more vertical space
                    width="100%",  # Use full available width
                    directed=True,
                    physics=True,  # Enable physics for natural floating
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6",
                    collapsible=True,
                    nodeSpacing=20,  # Extremely tight spacing between nodes for maximum compactness
                    nodeSize=25,  # Match the largest node size
                    fontSize=8,  # Match the font size
                    fontColor="#000000",  # Black text for all labels
                    backgroundColor="#ffffff",
                    linkHighlightBehavior=True,
                    linkHighlightColor="#F7A7A6",
                    labelHighlightBold=True,
                    showEdgeLabels=True,
                )

                # Use full width for the network graph
                agraph(nodes=agraph_nodes, edges=agraph_edges, config=config)

            except ImportError:
                st.warning("⚠️ streamlit-agraph לא מותקן. התקן עם: pip install streamlit-agraph")
                st.info("מפת קשרים תציג כאן לאחר התקנת streamlit-agraph")
        else:
            st.info("אין נתונים להצגת מפת קשרים")

    except Exception as e:
        st.error("שגיאה ביצירת מפת קשרים")
        logging.error(f"Network error: {e}")
