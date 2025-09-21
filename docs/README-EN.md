# Omri Association Management System

A comprehensive management system for the Omri Association, enabling donor management, widow support tracking, expenses, and budget management.

## 🚀 Quick Start (30 seconds)

```bash
# 1. Clone/download the project
# 2. Navigate to project folder
cd Omri-Association

# 3. Run the dashboard (choose one):
./run_dashboard.sh                    # macOS/Linux (recommended)
# OR
python3 -m streamlit run streamlit_app.py # Direct command

# 4. Open browser to: http://localhost:8501
```

**That's it!** The dashboard will start automatically. 🎉

## 🎯 Key Features

- 📊 **Interactive Dashboard** with real-time statistics
- 👥 **Donor Management** - Track donations and donor history
- 👩 **Widow Support Management** - Track widow details and monthly support
- 💰 **Budget Management** - Track expenses and budget forecasts
- 📈 **Advanced Reports** - Monthly, donor, and widow reports
- 🔗 **Relationship Mapping** - Visualize donor-widow relationships
- ⚠️ **Smart Alerts** - Budget and data quality alerts

## 📋 Installation & Setup

### System Requirements
- Python 3.8+
- Google Cloud Project with Google Sheets API enabled
- Service Account Key from Google Cloud Console

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the System

#### For macOS/Linux:
```bash
# Option 1: Use the shell script (recommended)
chmod +x run_dashboard.sh
./run_dashboard.sh

# Option 2: Direct command
python3 -m streamlit run streamlit_app.py
```

#### For Windows:
```bash
# Option 1: Use the batch file
run_dashboard.bat

# Option 2: Direct command
python -m streamlit run dashboard.py
```

### Access the Dashboard
Once running, open your browser and go to: **http://localhost:8501**

### Stop the Dashboard
Press `Ctrl+C` in the terminal where it's running.

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
If you see "Port 8501 is already in use":
```bash
# Kill existing Streamlit processes
pkill -f "streamlit run streamlit_app.py"
# Then run again
./run_dashboard.sh
```

#### Python Version Issues
Make sure you have Python 3.8+:
```bash
python3 --version
# If not found, try:
python --version
```

#### Missing Dependencies
If you get import errors:
```bash
pip install -r requirements.txt
# Or for Python 3:
pip3 install -r requirements.txt
```

#### Permission Denied (macOS/Linux)
```bash
chmod +x run_dashboard.sh
```

### Dashboard Not Loading?
1. Check if Streamlit is running: `ps aux | grep streamlit`
2. Verify the port: `lsof -i :8501`
3. Check browser console for errors
4. Ensure Google Sheets connection is working

## 📁 Project Structure

```
Omri-Association/
├── streamlit_app.py          # Main dashboard file
├── google_sheets_io.py       # Google Sheets read/write functions
├── data_loading.py           # Data loading
├── data_processing.py        # Data processing and statistics
├── data_visualization.py     # Charts and visualizations
├── reports.py                # PDF report generation
├── alerts.py                 # Alert system
├── requirements.txt          # Python dependencies
├── service_account.json      # Google Service Account key (not in Git)
├── run_dashboard.sh          # Shell script for easy startup
├── run_dashboard.bat         # Windows batch file
└── README.md                 # Hebrew documentation
```

## 🌐 Google Sheets Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Sheets API

2. **Create Service Account:**
   - Go to IAM & Admin > Service Accounts
   - Create new Service Account
   - Download JSON key file

3. **Setup Spreadsheet:**
   - Create new Google Spreadsheet
   - Share with Service Account email (with edit permissions)
   - Copy Spreadsheet ID from URL

4. **Configure Files:**
   - Save JSON key as `service_account.json` in project folder
   - Update Spreadsheet ID in `google_sheets_io.py`

## 📞 Support

For technical issues or questions, please contact the Omri Association development team.

## 📄 License

This project is intended for internal use by the Omri Association only.
