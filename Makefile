# Install dependencies using uv
install:
	uv sync

# Development server with debug mode
dev:
	uv run flask --debug --app page_analyzer:app run

# Default port configuration
PORT ?= 8000

# Production server for local use
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# Build script for deployment
build:
	./build.sh

# Start production server on Render.com
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# Run tests using pytest
# test:
# 	uv run pytest

# Check code style with ruff
lint:
	uv run ruff check page_analyzer

# Run both tests and linting
check: lint

# Declare phony targets
.PHONY: install dev start build render-start