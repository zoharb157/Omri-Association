#!/bin/bash
# Helper script to set up the Omri Association project, run tests, and launch the dashboard.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# ----- Helpers ------------------------------------------------------------- #
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

header() {
  echo "\n================================================================"
  echo "🔹 $1"
  echo "================================================================\n"
}

# ----- Python & Dependencies --------------------------------------------- #

if ! command_exists python3; then
  echo "❌ python3 not found. Please install Python 3.10 or newer before running this script."
  exit 1
fi

PYTHON="$(command -v python3)"
PIP="${PYTHON%python3}pip3"

header "Installing runtime dependencies"
"$PIP" install --upgrade pip
"$PIP" install -r requirements.txt

header "Installing development dependencies"
"$PIP" install -r requirements-dev.txt

# ----- Code Quality ------------------------------------------------------- #

header "Running Ruff lint"
"$PYTHON" -m ruff check .

header "Running Black format check"
"$PYTHON" -m black --check .

header "Running pytest"
"$PYTHON" -m pytest

# ----- Launch Dashboard --------------------------------------------------- #

header "Starting Streamlit dashboard"
export STREAMLIT_SERVER_PORT="${STREAMLIT_SERVER_PORT:-8501}"
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"

echo "🌐 Dashboard will be available at: http://localhost:${STREAMLIT_SERVER_PORT}"
echo "🛑 Press Ctrl+C to stop"

exec "$PYTHON" -m streamlit run dashboard.py
