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
	python3 -m streamlit run streamlit_app.py

run-port: ## Run on specific port (usage: make run-port PORT=8080)
	python3 -m streamlit run streamlit_app.py --server.port $(PORT)

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
