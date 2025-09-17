#!/usr/bin/env python3
"""
Debug HTML rendering issue
"""

import streamlit as st

# Set page config
st.set_page_config(page_title="Debug HTML", page_icon="🐛", layout="wide")

st.title("🐛 HTML Rendering Debug")

# Test 1: Simple HTML
st.subheader("Test 1: Simple HTML")
st.markdown(
    """
<div style="background: #f0f0f0; padding: 20px; border-radius: 8px; text-align: center;">
    <h3>Simple HTML Test</h3>
    <p>This should be rendered as HTML.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Test 2: Complex HTML (like our metric card)
st.subheader("Test 2: Complex HTML")
complex_html = """
<div class="metric-card" style="
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: #1f77b4;
    "></div>
    <div style="
        color: #7f8c8d;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
    ">
        Test Label
    </div>
    <div style="
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
    ">
        Test Value
    </div>
</div>
"""

st.markdown("Raw HTML:")
st.code(complex_html)

st.markdown("Rendered:")
st.markdown(complex_html, unsafe_allow_html=True)

# Test 3: Using our actual function
st.subheader("Test 3: Using create_metric_card function")
try:
    from ui.components.metrics import create_metric_card

    card_html = create_metric_card("Test Label", "Test Value", "Test Help", "+5%", "primary")
    st.markdown("Raw HTML:")
    st.code(card_html)
    st.markdown("Rendered:")
    st.markdown(card_html, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error: {e}")

# Test 4: Check if it's a Streamlit version issue
st.subheader("Test 4: Streamlit Info")
st.info(f"Streamlit version: {st.__version__}")
