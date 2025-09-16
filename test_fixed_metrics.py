#!/usr/bin/env python3
"""
Test fixed metric components
"""

import streamlit as st
from ui.components.metrics import create_metric_row, create_metric_card
from ui.design_tokens import get_global_css

# Set page config
st.set_page_config(
    page_title="Test Fixed Metrics",
    page_icon="🔧",
    layout="wide"
)

# Apply global CSS
st.markdown(get_global_css(), unsafe_allow_html=True)

# Test data
test_metrics = [
    {
        'label': 'אחוז ניצול',
        'value': '85%',
        'help': 'אחוז ניצול התקציב',
        'color': 'primary'
    },
    {
        'label': 'יתרה זמינה',
        'value': '₪15,000',
        'help': 'יתרה זמינה לתקציב',
        'color': 'success'
    },
    {
        'label': 'סך הוצאות',
        'value': '₪45,000',
        'help': 'סך הוצאות החודש',
        'color': 'warning'
    },
    {
        'label': 'סך תרומות',
        'value': '₪60,000',
        'help': 'סך תרומות החודש',
        'color': 'info'
    }
]

st.title("🔧 Test Fixed Metrics")

st.subheader("Test 1: Single Metric Card")
create_metric_card("Test Label", "Test Value", "Test Help", "+5%", "primary")

st.subheader("Test 2: Metric Row")
st.markdown("This should show 4 properly styled metric cards:")
create_metric_row(test_metrics, 4)

st.subheader("Test 3: Different Colors")
color_metrics = [
    {'label': 'Primary', 'value': '100', 'color': 'primary'},
    {'label': 'Success', 'value': '200', 'color': 'success'},
    {'label': 'Warning', 'value': '300', 'color': 'warning'},
    {'label': 'Error', 'value': '400', 'color': 'error'}
]
create_metric_row(color_metrics, 4)



