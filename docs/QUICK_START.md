# 🚀 Quick Start Guide

## Start Dashboard (30 seconds)

```bash
# Option 1: Use the shell script (recommended)
./run_dashboard.sh

# Option 2: Direct command
python3 -m streamlit run dashboard.py

# Option 3: Custom port
python3 -m streamlit run dashboard.py --server.port 8080
```

## Access Dashboard
- **Local**: http://localhost:8501
- **Network**: http://10.100.102.12:8501
- **Public**: Use Cloudflare Tunnel (see below)

## Make Public (Optional)
```bash
# Install cloudflared
brew install cloudflared  # macOS
# or
sudo apt install cloudflared  # Ubuntu

# Create tunnel
cloudflared tunnel --url http://localhost:8501
```

## Stop Dashboard
Press `Ctrl+C` in the terminal
