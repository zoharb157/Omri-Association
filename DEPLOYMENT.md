# 🚀 Deployment Guide

## Production Deployment

### Option 1: Local Server
```bash
# Run with production settings
python3 -m streamlit run dashboard.py --server.port 80 --server.address 0.0.0.0
```

### Option 2: Docker (Recommended)
```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Option 3: Cloudflare Tunnel
```bash
# Install cloudflared
brew install cloudflared

# Create persistent tunnel
cloudflared tunnel create omri-dashboard
cloudflared tunnel route dns omri-dashboard your-domain.com
cloudflared tunnel run omri-dashboard
```

## Environment Variables
- `DASHBOARD_PORT`: Port to run on (default: 8501)
- `DASHBOARD_HOST`: Host to bind to (default: 0.0.0.0)
- `GOOGLE_SHEETS_SPREADSHEET_ID`: Your spreadsheet ID
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)

## Security Considerations
- Use HTTPS in production
- Implement authentication if needed
- Secure your service account key
- Monitor access logs
