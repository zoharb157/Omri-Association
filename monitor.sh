#!/bin/bash

# Omri Dashboard Monitoring Script

echo "🔍 Omri Dashboard Status Check"
echo "=============================="
echo ""

# Check if dashboard is running
if pgrep -f "streamlit run dashboard.py" > /dev/null; then
    echo "✅ Dashboard is running"
    
    # Get process info
    PID=$(pgrep -f "streamlit run dashboard.py" | head -1)
    echo "   Process ID: $PID"
    
    # Check port usage
    PORT=$(lsof -i -P -n | grep "streamlit" | grep "LISTEN" | awk '{print $9}' | cut -d: -f2 | head -1)
    echo "   Port: $PORT"
    
    # Check memory usage
    MEMORY=$(ps -o rss= -p $PID | awk '{print $1/1024}')
    echo "   Memory Usage: ${MEMORY} MB"
    
    # Check uptime
    UPTIME=$(ps -o etime= -p $PID)
    echo "   Uptime: $UPTIME"
else
    echo "❌ Dashboard is not running"
fi

echo ""

# Check system resources
echo "💻 System Resources:"
echo "   CPU Usage: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d% -f1)%"
echo "   Memory Usage: $(top -l 1 | grep "PhysMem" | awk '{print $2}')"
echo "   Disk Usage: $(df -h / | tail -1 | awk '{print $5}')"

echo ""

# Check Google Sheets connection
if [ -f "service_account.json" ]; then
    echo "🔗 Google Sheets: ✅ Configured"
else
    echo "🔗 Google Sheets: ❌ Not configured"
fi

# Check recent logs
echo ""
echo "📋 Recent Activity:"
tail -5 *.log 2>/dev/null || echo "No log files found"
