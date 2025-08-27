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
