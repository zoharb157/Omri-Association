#!/usr/bin/env python3
"""
Test file to debug metric rendering
"""

import streamlit as st

from ui.components.metrics import create_metric_card, create_metric_row
from ui.design_tokens import get_global_css

# Set page config
st.set_page_config(
    page_title="Test Metrics",
    page_icon="🧪",
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

st.title("🧪 Test Metrics Rendering")

st.subheader("Test 1: Single Metric Card")
card_html = create_metric_card("Test Label", "Test Value", "Test Help", "+5%", "primary")
st.markdown("Raw HTML:")
st.code(card_html)
st.markdown("Rendered:")
st.markdown(card_html, unsafe_allow_html=True)

st.subheader("Test 2: Metric Row")
st.markdown("This should show 4 metric cards in a row:")
create_metric_row(test_metrics, 4)

st.subheader("Test 3: Simple HTML Test")
st.markdown("""
<div style="background: #f0f0f0; padding: 20px; border-radius: 8px; text-align: center;">
    <h3>Simple HTML Test</h3>
    <p>This should be rendered as HTML, not as text.</p>
</div>
""", unsafe_allow_html=True)



