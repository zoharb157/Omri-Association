# 🔧 Troubleshooting Guide

## Common Issues

### Port Already in Use
```bash
# Kill existing processes
pkill -f "streamlit run dashboard.py"

# Check what's using the port
lsof -i :8501
```

### Python Version Issues
```bash
# Check Python version
python3 --version

# Should be 3.8+
```

### Missing Dependencies
```bash
# Reinstall requirements
pip3 install -r requirements.txt --force-reinstall
```

### Permission Issues
```bash
# Fix script permissions
chmod +x run_dashboard.sh
chmod +x install.sh
```

### Google Sheets Connection
- Ensure service_account.json exists
- Check internet connection
- Verify API is enabled in Google Cloud Console

### Dashboard Not Loading
1. Check if Streamlit is running: `ps aux | grep streamlit`
2. Verify port: `lsof -i :8501`
3. Check browser console for errors
4. Ensure Google Sheets connection is working

## Getting Help
- Check the logs in the terminal
- Review README.md and README-EN.md
- Check Google Sheets API status
