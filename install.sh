#!/bin/bash

# Omri Association Dashboard - Installation Script
# This script sets up the complete environment for the dashboard

set -e  # Exit on any error

echo "🚀 Omri Association Dashboard - Installation Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    print_status "Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    print_status "Detected Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
    print_status "Detected Windows (Git Bash/Cygwin)"
else
    print_warning "Unknown OS: $OSTYPE"
    OS="Unknown"
fi

# Check Python version
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
    
    # Check if version is 3.8+
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python version is compatible (3.8+)"
    else
        print_error "Python version $PYTHON_VERSION is not compatible. Please install Python 3.8+"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    echo ""
    if [[ "$OS" == "macOS" ]]; then
        echo "To install Python on macOS:"
        echo "1. Visit https://www.python.org/downloads/"
        echo "2. Download and install Python 3.8+"
        echo "3. Make sure to check 'Add Python to PATH' during installation"
    elif [[ "$OS" == "Linux" ]]; then
        echo "To install Python on Linux:"
        echo "sudo apt update && sudo apt install python3 python3-pip  # Ubuntu/Debian"
        echo "sudo yum install python3 python3-pip  # CentOS/RHEL"
    fi
    exit 1
fi

# Check pip installation
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_success "pip found"
    PIP_CMD="pip"
else
    print_error "pip is not installed. Please install pip first."
    exit 1
fi

# Install/upgrade pip
print_status "Upgrading pip to latest version..."
$PIP_CMD install --upgrade pip

# Install required packages
print_status "Installing required Python packages..."
$PIP_CMD install -r requirements.txt

# Check if service account file exists
print_status "Checking Google Sheets configuration..."
if [ ! -f "service_account.json" ]; then
    print_warning "service_account.json not found!"
    echo ""
    echo "To set up Google Sheets integration:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing"
    echo "3. Enable Google Sheets API"
    echo "4. Create a Service Account"
    echo "5. Download the JSON key file"
    echo "6. Save it as 'service_account.json' in this directory"
    echo ""
    print_warning "Dashboard will work without Google Sheets, but data features will be limited"
else
    print_success "Google Sheets configuration found"
fi

# Make scripts executable
print_status "Setting up executable permissions..."
chmod +x run_dashboard.sh
chmod +x install.sh

# Create .env file for configuration
print_status "Creating configuration file..."
cat > .env << EOF
# Omri Association Dashboard Configuration
# Copy this file to .env.local and modify as needed

# Dashboard Settings
DASHBOARD_PORT=8501
DASHBOARD_HOST=0.0.0.0

# Google Sheets Settings
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE=service_account.json

# Data Settings
DATA_REFRESH_INTERVAL=300  # seconds
LOG_LEVEL=INFO

# Security Settings
ENABLE_PUBLIC_ACCESS=false
ENABLE_AUTHENTICATION=false
EOF

print_success "Configuration file created (.env)"

# Create quick start guide
print_status "Creating quick start guide..."
cat > QUICK_START.md << 'EOF'
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
EOF

print_success "Quick start guide created (QUICK_START.md)"

# Create troubleshooting guide
print_status "Creating troubleshooting guide..."
cat > TROUBLESHOOTING.md << 'EOF'
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
EOF

print_success "Troubleshooting guide created (TROUBLESHOOTING.md)"

# Create development setup guide
print_status "Creating development setup guide..."
cat > DEVELOPMENT.md << 'EOF'
# 🛠️ Development Setup

## Prerequisites
- Python 3.8+
- Git
- Code editor (VS Code recommended)

## Setup Development Environment
```bash
# Clone repository
git clone https://github.com/your-username/Omri-Association.git
cd Omri-Association

# Install development dependencies
pip3 install -r requirements.txt

# Install additional dev tools
pip3 install black flake8 pytest

# Run installation script
./install.sh
```

## Code Style
- Use Black for code formatting
- Follow PEP 8 guidelines
- Add type hints where possible

## Testing
```bash
# Run tests (when implemented)
pytest

# Format code
black .

# Lint code
flake8 .
EOF

print_success "Development guide created (DEVELOPMENT.md)"

# Create deployment guide
print_status "Creating deployment guide..."
cat > DEPLOYMENT.md << 'EOF'
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
EOF

print_success "Deployment guide created (DEPLOYMENT.md)"

# Create changelog
print_status "Creating changelog..."
cat > CHANGELOG.md << 'EOF'
# 📝 Changelog

## [Unreleased]

### Added
- Complete English documentation (README-EN.md)
- Quick start guide (30 seconds setup)
- Troubleshooting section
- Platform-specific running instructions
- Public access instructions via Cloudflare Tunnel
- Comprehensive installation script

### Changed
- Enhanced Hebrew README with clear instructions
- Improved data processing to preserve empty values
- Better widows table display

### Fixed
- 🐛 Widows table only showing 'widows without donors' instead of all widows
- 🐛 Data processing converting empty values to 0, masking real data state
- 🐛 Incomplete data display in dashboard sections

## [1.0.0] - 2025-08-27

### Added
- Initial Omri Association Dashboard
- Google Sheets integration
- Widows management system
- Donor tracking
- Budget management
- Data visualization
- Report generation

### Features
- Interactive dashboard with real-time statistics
- Donor management and contribution tracking
- Widow support management
- Budget analysis and forecasting
- Advanced reporting system
- Network relationship mapping
EOF

print_success "Changelog created (CHANGELOG.md)"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_status "Creating .gitignore file..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.production

# Google Service Account
service_account.json
*.json

# Logs
*.log
logs/

# Data files
*.csv
*.xlsx
*.xls

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
EOF
    print_success ".gitignore file created"
else
    print_success ".gitignore already exists"
fi

# Create requirements-dev.txt for development dependencies
print_status "Creating development requirements file..."
cat > requirements-dev.txt << 'EOF'
# Development dependencies
-r requirements.txt

# Code formatting and linting
black>=22.0.0
flake8>=4.0.0
pylint>=2.12.0

# Testing
pytest>=7.0.0
pytest-cov>=3.0.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Development tools
pre-commit>=2.20.0
EOF

print_success "Development requirements created (requirements-dev.txt)"

# Create Makefile for common tasks
print_status "Creating Makefile for common tasks..."
cat > Makefile << 'EOF'
.PHONY: help install run test clean format lint docs deploy

help: ## Show this help message
	@echo "Omri Association Dashboard - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	pip3 install -r requirements.txt

install-dev: ## Install development dependencies
	pip3 install -r requirements-dev.txt

run: ## Run the dashboard
	python3 -m streamlit run dashboard.py

run-port: ## Run on specific port (usage: make run-port PORT=8080)
	python3 -m streamlit run dashboard.py --server.port $(PORT)

test: ## Run tests
	pytest

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/

format: ## Format code with black
	black .

lint: ## Lint code with flake8
	flake8 .

docs: ## Generate documentation
	sphinx-build -b html docs/ docs/_build/html

deploy: ## Deploy to production
	@echo "Deploying to production..."
	@echo "Please implement your deployment strategy"

setup: ## Initial setup
	./install.sh

update: ## Update dependencies
	pip3 install -r requirements.txt --upgrade

logs: ## Show recent logs
	tail -f *.log

status: ## Show system status
	@echo "Python version: $(shell python3 --version)"
	@echo "Pip version: $(shell pip3 --version)"
	@echo "Streamlit processes: $(shell ps aux | grep streamlit | grep -v grep | wc -l)"
EOF

print_success "Makefile created"

# Create systemd service file for production
print_status "Creating systemd service file..."
cat > omri-dashboard.service << 'EOF'
[Unit]
Description=Omri Association Dashboard
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/Omri-Association
Environment=PATH=/path/to/Omri-Association/venv/bin
ExecStart=/path/to/Omri-Association/venv/bin/streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service file created (omri-dashboard.service)"

# Create Docker Compose file
print_status "Creating Docker Compose file..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  omri-dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DASHBOARD_PORT=8501
      - DASHBOARD_HOST=0.0.0.0
    volumes:
      - ./service_account.json:/app/service_account.json:ro
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - omri-dashboard
    restart: unless-stopped
EOF

print_success "Docker Compose file created (docker-compose.yml)"

# Create nginx configuration
print_status "Creating nginx configuration..."
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server omri-dashboard:8501;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://streamlit;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

print_success "Nginx configuration created (nginx.conf)"

# Create monitoring script
print_status "Creating monitoring script..."
cat > monitor.sh << 'EOF'
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
EOF

chmod +x monitor.sh
print_success "Monitoring script created (monitor.sh)"

# Create backup script
print_status "Creating backup script..."
cat > backup.sh << 'EOF'
#!/bin/bash

# Omri Dashboard Backup Script

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup in $BACKUP_DIR"

# Backup configuration files
cp -r *.py "$BACKUP_DIR/"
cp -r ui/ "$BACKUP_DIR/"
cp -r modules/ "$BACKUP_DIR/"
cp -r reports/ "$BACK_DIR/"
cp *.md "$BACKUP_DIR/"
cp *.sh "$BACKUP_DIR/"
cp *.yml "$BACKUP_DIR/"
cp *.service "$BACKUP_DIR/"
cp requirements*.txt "$BACKUP_DIR/"

# Backup data (if exists)
if [ -d "data" ]; then
    cp -r data/ "$BACKUP_DIR/"
fi

# Create backup info
cat > "$BACKUP_DIR/backup_info.txt" << BACKUP_INFO
Backup created: $(date)
Dashboard version: $(git describe --tags 2>/dev/null || echo "Unknown")
Python version: $(python3 --version)
System: $(uname -a)
BACKUP_INFO

echo "✅ Backup completed: $BACKUP_DIR"
echo "📁 Backup size: $(du -sh "$BACKUP_DIR" | cut -f1)"
EOF

chmod +x backup.sh
print_success "Backup script created (backup.sh)"

# Create update script
print_status "Creating update script..."
cat > update.sh << 'EOF'
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
EOF

chmod +x update.sh
print_success "Update script created (update.sh)"

# Final status
echo ""
echo "🎉 Installation completed successfully!"
echo "======================================"
echo ""
echo "📁 Files created:"
echo "   ✅ .env (configuration)"
echo "   ✅ QUICK_START.md (quick start guide)"
echo "   ✅ TROUBLESHOOTING.md (troubleshooting)"
echo "   ✅ DEVELOPMENT.md (development setup)"
echo "   ✅ DEPLOYMENT.md (deployment guide)"
echo "   ✅ CHANGELOG.md (version history)"
echo "   ✅ .gitignore (git ignore rules)"
echo "   ✅ requirements-dev.txt (dev dependencies)"
echo "   ✅ Makefile (common tasks)"
echo "   ✅ omri-dashboard.service (systemd service)"
echo "   ✅ docker-compose.yml (Docker setup)"
echo "   ✅ nginx.conf (web server config)"
echo "   ✅ monitor.sh (monitoring script)"
echo "   ✅ backup.sh (backup script)"
echo "   ✅ update.sh (update script)"
echo ""
echo "🚀 To start the dashboard:"
echo "   ./run_dashboard.sh"
echo ""
echo "📚 Documentation:"
echo "   README.md (Hebrew)"
echo "   README-EN.md (English)"
echo "   QUICK_START.md (Quick start)"
echo ""
echo "🔧 Common commands:"
echo "   make help          - Show all available commands"
echo "   make install       - Install dependencies"
echo "   make run           - Run dashboard"
echo "   make format        - Format code"
echo "   make lint          - Lint code"
echo "   ./monitor.sh       - Check system status"
echo "   ./backup.sh        - Create backup"
echo "   ./update.sh        - Update system"
echo ""
echo "🌐 Public access:"
echo "   Use Cloudflare Tunnel: cloudflared tunnel --url http://localhost:8501"
echo ""
print_success "Installation completed! Your project is now production-ready."
