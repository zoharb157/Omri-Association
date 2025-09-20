# 🛡️ UI Protection Guide - DO NOT BREAK!

## ⚠️ CRITICAL WARNING
This file documents all UI components that MUST NOT be removed or modified. Breaking these will cause user complaints and break the dashboard functionality.

## 🔒 PROTECTED COMPONENTS

### 1. Network Section Filters (ui/dashboard_sections.py)
**Location:** `create_network_section()` function
**Status:** 🚨 CRITICAL - User specifically requested these never disappear

**Protected Elements:**
- `show_connected` checkbox - "הצג קשרים קיימים"
- `show_unconnected_donors` checkbox - "הצג תורמים ללא קשרים"  
- `show_unconnected_widows` checkbox - "הצג אלמנות ללא קשרים"

**Protection Keys:**
- `network_show_connected`
- `network_show_unconnected_donors`
- `network_show_unconnected_widows`

### 2. Main Dashboard Header (ui/dashboard_layout.py)
**Location:** `create_dashboard_header()` function
**Status:** 🚨 CRITICAL - Essential for dashboard identity

**Protected Elements:**
- Main title: "מערכת ניהול עמותת עמרי"
- Theme toggle button
- Header styling and layout

### 3. Main Navigation Tabs (ui/dashboard_layout.py)
**Location:** `create_main_tabs()` function
**Status:** 🚨 CRITICAL - Essential for navigation

**Protected Elements:**
- 6 main tabs in exact order:
  1. "🏠 דף הבית"
  2. "💰 תקציב"
  3. "👥 תורמים"
  4. "👩 אלמנות"
  5. "🕸️ מפת קשרים"
  6. "🏘️ אזורי מגורים"

## 🚫 WHAT NOT TO DO

### ❌ NEVER Remove:
- Network section checkboxes
- Main dashboard header
- Any of the 6 main tabs
- Tab navigation structure
- Essential UI components

### ❌ NEVER Modify:
- Checkbox keys in network section
- Tab names and order
- Header title and styling
- Core navigation structure

### ❌ NEVER Break:
- User experience flow
- Navigation between tabs
- Network visualization functionality
- Dashboard identity and branding

## ✅ SAFE TO REMOVE

### Files that can be safely deleted:
- Unused documentation files
- Unused test files
- Unused configuration files
- Unused deployment configs
- Unused Python modules not imported anywhere

### Code that can be safely removed:
- Unused functions not called anywhere
- Unused imports
- Dead code paths
- Unused variables
- Unused classes

## 🔍 HOW TO VERIFY SAFETY

Before removing any code:
1. Check if it's in the PROTECTED COMPONENTS list above
2. Search for imports/usage across the codebase
3. Test the dashboard after changes
4. Verify all tabs work correctly
5. Verify network section works correctly

## 📞 CONTACT

If you're unsure about removing something, check this guide first. When in doubt, DON'T REMOVE IT!
