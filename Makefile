# Variables (optional but useful)
FLASK_APP = flaskr
PYTHON = python
PIP = pip

# Default target (runs when you just type 'make')
.DEFAULT_GOAL := help

# Phony targets (targets that don't create files)
.PHONY: dev install test clean help init-db requirements

# Development server
dev:
    @echo "Starting Flask development server..."
    flask --app $(FLASK_APP) run --reload --debug --host=0.0.0.0 --port=5000

# Install dependencies
install:
    @echo "Installing Python dependencies..."
    $(PIP) install -r requirements.txt

# Create/update requirements.txt
requirements:
    @echo "Generating requirements.txt..."
    $(PIP) freeze > requirements.txt

# Initialize database
init-db:
    @echo "Initializing database..."
    flask --app $(FLASK_APP) init-db

# Run tests
test:
    @echo "Running tests..."
    $(PYTHON) -m pytest tests/ -v

# Clean up cache files
clean:
    @echo "Cleaning up..."
    find . -type d -name "__pycache__" -delete
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +

# Set up virtual environment
venv:
    @echo "Creating virtual environment..."
    $(PYTHON) -m venv .venv
    @echo "Activate with: .venv\\Scripts\\activate (Windows) or source .venv/bin/activate (Mac/Linux)"

# Install project in development mode
dev-install:
    $(PIP) install -e .

# Show available commands
help:
    @echo "Available commands:"
    @echo "  make dev          - Start development server"
    @echo "  make install      - Install dependencies"
    @echo "  make venv         - Create virtual environment"
    @echo "  make init-db      - Initialize database"
    @echo "  make test         - Run tests"
    @echo "  make clean        - Remove cache files"
    @echo "  make requirements - Generate requirements.txt"
    @echo "  make help         - Show this help"