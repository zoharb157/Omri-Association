#!/bin/bash

echo "🚀 Starting Omri Association Dashboard..."
echo "📊 This will open the dashboard in your browser at http://localhost:8501"
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking required packages..."
python3 -c "import streamlit, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    pip3 install -r requirements.txt
fi

# Kill any existing Streamlit processes
echo "🔄 Stopping any existing dashboard instances..."
pkill -f "streamlit run dashboard.py" 2>/dev/null

# Start the dashboard
echo "🌟 Starting dashboard..."
echo "🌐 Open your browser and go to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the dashboard"
echo ""

python3 -m streamlit run dashboard.py


