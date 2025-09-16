#!/usr/bin/env python3
"""
Micro-interactions and Animations for Omri Association Dashboard
Subtle animations and interactive feedback
"""

import streamlit as st
from ui.design_system.modern_tokens import ModernDesignSystem

def create_loading_animations():
    """Create loading animations and states"""
    
    loading_css = """
    <style>
    /* Loading animations */
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius-md);
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .loading-spinner {
        width: 20px;
        height: 20px;
        border: 2px solid var(--gray-200);
        border-top: 2px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 1.5s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }
    
    /* Pulse animation for important elements */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Fade in animation */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Slide in animation */
    .slide-in-right {
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
    """
    
    st.markdown(loading_css, unsafe_allow_html=True)

def create_hover_effects():
    """Create hover effects for interactive elements"""
    
    hover_css = """
    <style>
    /* Hover effects for cards */
    .hover-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .hover-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Hover effects for buttons */
    .hover-button {
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .hover-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .hover-button:hover::before {
        left: 100%;
    }
    
    .hover-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Hover effects for links */
    .hover-link {
        position: relative;
        transition: color 0.2s ease;
    }
    
    .hover-link::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--primary);
        transition: width 0.3s ease;
    }
    
    .hover-link:hover::after {
        width: 100%;
    }
    
    .hover-link:hover {
        color: var(--primary);
    }
    
    /* Hover effects for icons */
    .hover-icon {
        transition: all 0.2s ease;
    }
    
    .hover-icon:hover {
        transform: scale(1.1);
        color: var(--primary);
    }
    
    /* Hover effects for metric cards */
    .metric-card-hover {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card-hover:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary-200);
    }
    
    /* Hover effects for navigation items */
    .nav-item-hover {
        transition: all 0.2s ease;
        position: relative;
    }
    
    .nav-item-hover::before {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        width: 0;
        height: 100%;
        background: var(--primary-50);
        transition: width 0.3s ease;
        z-index: -1;
    }
    
    .nav-item-hover:hover::before {
        width: 100%;
    }
    
    .nav-item-hover:hover {
        color: var(--primary-700);
    }
    </style>
    """
    
    st.markdown(hover_css, unsafe_allow_html=True)

def create_focus_states():
    """Create focus states for accessibility"""
    
    focus_css = """
    <style>
    /* Focus states for accessibility */
    .focus-visible {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
        border-radius: var(--radius-sm);
    }
    
    .focus-button:focus {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
    }
    
    .focus-link:focus {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
        border-radius: var(--radius-sm);
    }
    
    .focus-card:focus {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
        box-shadow: var(--shadow-md);
    }
    
    /* Skip to content link */
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: var(--radius-sm);
        z-index: 1000;
        transition: top 0.3s;
    }
    
    .skip-link:focus {
        top: 6px;
    }
    </style>
    """
    
    st.markdown(focus_css, unsafe_allow_html=True)

def create_transition_animations():
    """Create smooth transition animations"""
    
    transition_css = """
    <style>
    /* Smooth transitions for all interactive elements */
    * {
        transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, 
                   box-shadow 0.2s ease, transform 0.2s ease, opacity 0.2s ease;
    }
    
    /* Page transitions */
    .page-transition {
        animation: pageFadeIn 0.5s ease-in-out;
    }
    
    @keyframes pageFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Card entrance animations */
    .card-entrance {
        animation: cardSlideIn 0.6s ease-out;
    }
    
    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(30px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* Staggered animations for lists */
    .stagger-item {
        animation: staggerFadeIn 0.5s ease-out forwards;
        opacity: 0;
    }
    
    .stagger-item:nth-child(1) { animation-delay: 0.1s; }
    .stagger-item:nth-child(2) { animation-delay: 0.2s; }
    .stagger-item:nth-child(3) { animation-delay: 0.3s; }
    .stagger-item:nth-child(4) { animation-delay: 0.4s; }
    .stagger-item:nth-child(5) { animation-delay: 0.5s; }
    
    @keyframes staggerFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Modal animations */
    .modal-enter {
        animation: modalFadeIn 0.3s ease-out;
    }
    
    @keyframes modalFadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .modal-exit {
        animation: modalFadeOut 0.3s ease-in;
    }
    
    @keyframes modalFadeOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.9); }
    }
    
    /* Toast notifications */
    .toast-enter {
        animation: toastSlideIn 0.3s ease-out;
    }
    
    @keyframes toastSlideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .toast-exit {
        animation: toastSlideOut 0.3s ease-in;
    }
    
    @keyframes toastSlideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    </style>
    """
    
    st.markdown(transition_css, unsafe_allow_html=True)

def create_loading_states():
    """Create loading states for different components"""
    
    def create_loading_card():
        """Create a loading card component"""
        loading_html = """
        <div class="loading-card">
            <div class="loading-header">
                <div class="loading-shimmer" style="width: 60%; height: 16px; margin-bottom: 8px;"></div>
                <div class="loading-shimmer" style="width: 40%; height: 14px;"></div>
            </div>
            <div class="loading-content">
                <div class="loading-shimmer" style="width: 80%; height: 24px; margin-bottom: 12px;"></div>
                <div class="loading-shimmer" style="width: 60%; height: 16px; margin-bottom: 8px;"></div>
                <div class="loading-shimmer" style="width: 70%; height: 16px;"></div>
            </div>
        </div>
        """
        return loading_html
    
    def create_loading_metric():
        """Create a loading metric component"""
        loading_html = """
        <div class="loading-metric">
            <div class="loading-shimmer" style="width: 50%; height: 14px; margin-bottom: 8px;"></div>
            <div class="loading-shimmer" style="width: 80%; height: 32px; margin-bottom: 8px;"></div>
            <div class="loading-shimmer" style="width: 30%; height: 12px;"></div>
        </div>
        """
        return loading_html
    
    def create_loading_chart():
        """Create a loading chart component"""
        loading_html = """
        <div class="loading-chart">
            <div class="loading-shimmer" style="width: 40%; height: 20px; margin-bottom: 16px;"></div>
            <div class="loading-chart-content">
                <div class="loading-shimmer" style="width: 100%; height: 200px; border-radius: var(--radius-md);"></div>
            </div>
        </div>
        """
        return loading_html
    
    return {
        'card': create_loading_card,
        'metric': create_loading_metric,
        'chart': create_loading_chart
    }

def create_interactive_feedback():
    """Create interactive feedback components"""
    
    feedback_css = """
    <style>
    /* Interactive feedback styles */
    .click-feedback {
        position: relative;
        overflow: hidden;
    }
    
    .click-feedback::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .click-feedback:active::after {
        width: 300px;
        height: 300px;
    }
    
    /* Success feedback */
    .success-feedback {
        animation: successPulse 0.6s ease-out;
    }
    
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); background-color: var(--success-50); }
        100% { transform: scale(1); }
    }
    
    /* Error feedback */
    .error-feedback {
        animation: errorShake 0.6s ease-out;
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Warning feedback */
    .warning-feedback {
        animation: warningBounce 0.6s ease-out;
    }
    
    @keyframes warningBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* Progress feedback */
    .progress-feedback {
        position: relative;
    }
    
    .progress-feedback::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: progressSweep 2s infinite;
    }
    
    @keyframes progressSweep {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    </style>
    """
    
    st.markdown(feedback_css, unsafe_allow_html=True)



