#!/usr/bin/env python3
"""
Monitoring and Health Check System for Omri Association Dashboard
Provides system health monitoring, performance metrics, and alerts
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List

import psutil
import streamlit as st

from cache_manager import get_cache_stats


class SystemMonitor:
    """Monitors system health and performance"""

    def __init__(self):
        self.start_time = time.time()
        self.metrics_history = []
        self.max_history_size = 100
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time_ms': 5000.0
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = round(memory.used / (1024**3), 2)
            memory_total_gb = round(memory.total / (1024**3), 2)

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = round(disk.used / (1024**3), 2)
            disk_total_gb = round(disk.total / (1024**3), 2)

            # Network metrics
            network = psutil.net_io_counters()
            bytes_sent = network.bytes_sent
            bytes_recv = network.bytes_recv

            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()

            # Uptime
            uptime = time.time() - self.start_time
            uptime_hours = round(uptime / 3600, 2)

            metrics = {
                'timestamp': datetime.now(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency_mhz': round(cpu_freq.current if cpu_freq else 0, 2)
                },
                'memory': {
                    'percent': memory_percent,
                    'used_gb': memory_used_gb,
                    'total_gb': memory_total_gb,
                    'available_gb': round(memory.available / (1024**3), 2)
                },
                'disk': {
                    'percent': disk_percent,
                    'used_gb': disk_used_gb,
                    'total_gb': disk_total_gb,
                    'free_gb': round(disk.free / (1024**3), 2)
                },
                'network': {
                    'bytes_sent_mb': round(bytes_sent / (1024**2), 2),
                    'bytes_recv_mb': round(bytes_recv / (1024**2), 2)
                },
                'process': {
                    'memory_mb': round(process_memory.rss / (1024**2), 2),
                    'cpu_percent': process_cpu
                },
                'uptime_hours': uptime_hours
            }

            # Store in history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history.pop(0)

            return metrics

        except Exception as e:
            logging.error(f"Error getting system metrics: {e}")
            return {}

    def check_health(self) -> Dict[str, Any]:
        """Check system health and return status"""
        metrics = self.get_system_metrics()
        if not metrics:
            return {'status': 'error', 'message': 'Unable to get system metrics'}

        alerts = []
        status = 'healthy'

        # Check CPU usage
        if metrics['cpu']['percent'] > self.alert_thresholds['cpu_percent']:
            alerts.append(f"CPU usage high: {metrics['cpu']['percent']}%")
            status = 'warning'

        # Check memory usage
        if metrics['memory']['percent'] > self.alert_thresholds['memory_percent']:
            alerts.append(f"Memory usage high: {metrics['memory']['percent']}%")
            status = 'warning'

        # Check disk usage
        if metrics['disk']['percent'] > self.alert_thresholds['disk_percent']:
            alerts.append(f"Disk usage high: {metrics['disk']['percent']}%")
            status = 'critical'

        # Check if process memory is reasonable
        if metrics['process']['memory_mb'] > 1000:  # More than 1GB
            alerts.append(f"Process memory high: {metrics['process']['memory_mb']}MB")
            status = 'warning'

        return {
            'status': status,
            'timestamp': metrics['timestamp'],
            'alerts': alerts,
            'metrics': metrics
        }

    def get_performance_trends(self) -> Dict[str, List[float]]:
        """Get performance trends over time"""
        if len(self.metrics_history) < 2:
            return {}

        trends = {
            'cpu_percent': [],
            'memory_percent': [],
            'disk_percent': [],
            'process_memory_mb': []
        }

        for metric in self.metrics_history:
            trends['cpu_percent'].append(metric['cpu']['percent'])
            trends['memory_percent'].append(metric['memory']['percent'])
            trends['disk_percent'].append(metric['disk']['percent'])
            trends['process_memory_mb'].append(metric['process']['memory_mb'])

        return trends

    def get_uptime_stats(self) -> Dict[str, Any]:
        """Get uptime statistics"""
        current_time = time.time()
        uptime = current_time - self.start_time

        return {
            'start_time': datetime.fromtimestamp(self.start_time),
            'current_time': datetime.fromtimestamp(current_time),
            'uptime_seconds': uptime,
            'uptime_hours': round(uptime / 3600, 2),
            'uptime_days': round(uptime / (3600 * 24), 2)
        }

class DashboardHealthChecker:
    """Checks dashboard-specific health metrics"""

    def __init__(self):
        self.health_checks = []
        self.last_check_time = None

    def add_health_check(self, name: str, check_func, critical: bool = False):
        """Add a custom health check"""
        self.health_checks.append({
            'name': name,
            'function': check_func,
            'critical': critical
        })

    def run_health_checks(self) -> List[Dict[str, Any]]:
        """Run all health checks"""
        results = []
        self.last_check_time = datetime.now()

        for check in self.health_checks:
            try:
                result = check['function']()
                results.append({
                    'name': check['name'],
                    'status': result.get('status', 'unknown'),
                    'message': result.get('message', ''),
                    'critical': check['critical'],
                    'timestamp': self.last_check_time
                })
            except Exception as e:
                results.append({
                    'name': check['name'],
                    'status': 'error',
                    'message': f"Check failed: {str(e)}",
                    'critical': check['critical'],
                    'timestamp': self.last_check_time
                })

        return results

    def get_overall_health(self) -> str:
        """Get overall health status"""
        if not self.health_checks:
            return 'unknown'

        results = self.run_health_checks()

        # Check for critical failures
        critical_failures = [r for r in results if r['critical'] and r['status'] != 'healthy']
        if critical_failures:
            return 'critical'

        # Check for any failures
        failures = [r for r in results if r['status'] != 'healthy']
        if failures:
            return 'warning'

        return 'healthy'

# Global instances
system_monitor = SystemMonitor()
health_checker = DashboardHealthChecker()

def get_system_monitor() -> SystemMonitor:
    """Get global system monitor instance"""
    return system_monitor

def get_health_checker() -> DashboardHealthChecker:
    """Get global health checker instance"""
    return health_checker

def show_monitoring_dashboard():
    """Show monitoring dashboard in Streamlit"""
    st.markdown("### 📊 מערכת ניטור ובדיקת בריאות")

    # System Health Status
    col1, col2, col3 = st.columns(3)

    with col1:
        health_status = health_checker.get_overall_health()
        if health_status == 'healthy':
            st.success("✅ מערכת בריאה")
        elif health_status == 'warning':
            st.warning("⚠️ מערכת עם אזהרות")
        else:
            st.error("❌ מערכת קריטית")

    with col2:
        system_health = system_monitor.check_health()
        if system_health['status'] == 'healthy':
            st.success("✅ מערכת יציבה")
        elif system_health['status'] == 'warning':
            st.warning("⚠️ מערכת עם אזהרות")
        else:
            st.error("❌ בעיות מערכת")

    with col3:
        uptime_stats = system_monitor.get_uptime_stats()
        st.metric("זמן פעילות", f"{uptime_stats['uptime_hours']} שעות")

    # System Metrics
    st.markdown("#### 🖥️ מדדי מערכת")
    metrics = system_monitor.get_system_metrics()

    if metrics:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("CPU", f"{metrics['cpu']['percent']}%")
            st.metric("זיכרון", f"{metrics['memory']['percent']}%")

        with col2:
            st.metric("דיסק", f"{metrics['disk']['percent']}%")
            st.metric("זיכרון תהליך", f"{metrics['process']['memory_mb']}MB")

        with col3:
            st.metric("זיכרון זמין", f"{metrics['memory']['available_gb']}GB")
            st.metric("דיסק חופשי", f"{metrics['disk']['free_gb']}GB")

        with col4:
            st.metric("שלח רשת", f"{metrics['network']['bytes_sent_mb']}MB")
            st.metric("קבל רשת", f"{metrics['network']['bytes_recv_mb']}MB")

    # Health Check Results
    st.markdown("#### 🔍 בדיקות בריאות")
    health_results = health_checker.run_health_checks()

    for result in health_results:
        if result['status'] == 'healthy':
            st.success(f"✅ {result['name']}: {result['message']}")
        elif result['status'] == 'warning':
            st.warning(f"⚠️ {result['name']}: {result['message']}")
        else:
            st.error(f"❌ {result['name']}: {result['message']}")

    # Cache Statistics
    st.markdown("#### 💾 סטטיסטיקות מטמון")
    cache_stats = get_cache_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("פריטים במטמון", cache_stats['total_entries'])
        st.metric("פריטים פעילים", cache_stats['active_entries'])

    with col2:
        st.metric("גודל מטמון", f"{cache_stats['estimated_size_mb']}MB")
        st.metric("זמן חיים", f"{cache_stats['cache_ttl']}s")

    with col3:
        if st.button("🗑️ נקה מטמון"):
            from cache_manager import clear_cache
            clear_cache()
            st.success("✅ המטמון נוקה")
            st.rerun()

    # Performance Trends
    st.markdown("#### 📈 מגמות ביצועים")
    trends = system_monitor.get_performance_trends()

    if trends and len(trends['cpu_percent']) > 1:
        import plotly.graph_objects as go

        fig = go.Figure()

        # Add CPU trend
        fig.add_trace(go.Scatter(
            y=trends['cpu_percent'],
            name='CPU %',
            line=dict(color='red')
        ))

        # Add Memory trend
        fig.add_trace(go.Scatter(
            y=trends['memory_percent'],
            name='Memory %',
            line=dict(color='blue')
        ))

        # Add Disk trend
        fig.add_trace(go.Scatter(
            y=trends['disk_percent'],
            name='Disk %',
            line=dict(color='green')
        ))

        fig.update_layout(
            title="מגמות ביצועים לאורך זמן",
            xaxis_title="מדידות",
            yaxis_title="אחוזים",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # System Alerts
    if system_health.get('alerts'):
        st.markdown("#### 🚨 התראות מערכת")
        for alert in system_health['alerts']:
            st.warning(f"⚠️ {alert}")

# Add default health checks
def check_google_sheets_connection():
    """Check Google Sheets connection"""
    try:
        from google_sheets_io import check_service_account_validity
        if check_service_account_validity():
            return {'status': 'healthy', 'message': 'Google Sheets connection OK'}
        else:
            return {'status': 'critical', 'message': 'Google Sheets connection failed'}
    except Exception as e:
        return {'status': 'error', 'message': f'Google Sheets check error: {e}'}

def check_data_availability():
    """Check if data is available"""
    try:
        if 'expenses_df' in st.session_state and 'donations_df' in st.session_state:
            return {'status': 'healthy', 'message': 'Data available in session'}
        else:
            return {'status': 'warning', 'message': 'No data in session'}
    except Exception as e:
        return {'status': 'error', 'message': f'Data check error: {e}'}

# Register default health checks
health_checker.add_health_check("Google Sheets Connection", check_google_sheets_connection, critical=True)
health_checker.add_health_check("Data Availability", check_data_availability, critical=False)
