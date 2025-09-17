# 🛠️ Development Setup

## Prerequisites
- Python 3.10+
- Git
- Code editor (VS Code recommended)

## Setup Development Environment
```bash
# Clone repository
git clone https://github.com/your-username/Omri-Association.git
cd Omri-Association

# Install runtime + development dependencies
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt

# (Optional) install pre-commit hooks for consistent formatting
pre-commit install

# Run installation script
./install.sh
```

## Code Style
- Run `ruff check .` and `black .` before committing
- Follow PEP 8 guidelines
- Add type hints where possible

## Testing
```bash
# Run tests
pytest

# Format code
black .

# Lint code
ruff check .
