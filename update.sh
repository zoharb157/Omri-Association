#!/bin/bash

# Omri Dashboard Update Script

echo "🔄 Updating Omri Dashboard..."

# Backup current version
./backup.sh

# Pull latest changes
git pull origin main

# Update dependencies
pip3 install -r requirements.txt --upgrade

# Restart dashboard if running
if pgrep -f "streamlit run dashboard.py" > /dev/null; then
    echo "🔄 Restarting dashboard..."
    pkill -f "streamlit run dashboard.py"
    sleep 2
    ./run_dashboard.sh &
    echo "✅ Dashboard restarted"
fi

echo "✅ Update completed!"
