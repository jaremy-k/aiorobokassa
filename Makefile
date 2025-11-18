.PHONY: help format format-check lint lint-fix type-check all-checks install-dev clean test test-cov

# Python interpreter - use venv if available, otherwise system
ifneq ($(wildcard .venv/bin/python),)
    PYTHON := .venv/bin/python
else
    PYTHON := python3
endif

# Use uv if available, otherwise pip
UV := $(shell which uv 2>/dev/null)
ifdef UV
    PIP := uv pip
else
    PIP := $(PYTHON) -m pip
endif

# Directories
SRC_DIR := aiorobokassa
TESTS_DIR := tests

# Tools
BLACK := $(PYTHON) -m black
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install-dev: ## Install development dependencies with uv
	@echo "Installing development dependencies with uv..."
	uv pip install -e ".[dev]"

format: ## Format code with black
	@echo "Formatting code with black..."
	$(BLACK) $(SRC_DIR) || true
	@if [ -d "tests" ]; then $(BLACK) tests || true; fi
	@if [ -d "examples" ]; then $(BLACK) examples || true; fi

format-check: ## Check code formatting without making changes
	@echo "Checking code formatting..."
	$(BLACK) --check $(SRC_DIR)
	@if [ -d "tests" ]; then $(BLACK) --check tests || true; fi
	@if [ -d "examples" ]; then $(BLACK) --check examples || true; fi

lint: ## Run ruff linter
	@echo "Running ruff linter..."
	$(RUFF) check $(SRC_DIR)
	@if [ -d "tests" ]; then $(RUFF) check tests || true; fi
	@if [ -d "examples" ]; then $(RUFF) check examples || true; fi

lint-fix: ## Run ruff linter and auto-fix issues
	@echo "Running ruff linter with auto-fix..."
	$(RUFF) check --fix $(SRC_DIR)
	@if [ -d "tests" ]; then $(RUFF) check --fix tests || true; fi
	@if [ -d "examples" ]; then $(RUFF) check --fix examples || true; fi

type-check: ## Run mypy type checker
	@echo "Running mypy type checker..."
	$(MYPY) $(SRC_DIR)

all-checks: format-check lint type-check ## Run all checks (format, lint, type-check)
	@echo "All checks passed!"

clean: ## Clean cache and temporary files
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	@echo "Clean complete!"

test: ## Run tests
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest tests/ --cov=$(SRC_DIR) --cov-report=html --cov-report=term

