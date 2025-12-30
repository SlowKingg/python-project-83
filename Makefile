# Load environment variables from .env file
-include .env

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

# Check code style with ruff
lint:
	uv run ruff check page_analyzer

# Initialize database from database.sql
db-init:
	psql -a $(DATABASE_URL) -f database.sql

# Drop tables if manual cleanup is required
db-drop:
	psql -a $(DATABASE_URL) -c "DROP TABLE IF EXISTS url_checks; DROP TABLE IF EXISTS urls;"

# Babel / i18n settings
BABEL_CFG ?= babel.cfg
TRANS_DIR ?= page_analyzer/translations
POT_FILE ?= $(TRANS_DIR)/messages.pot

# Extract messages into POT
babel-extract:
	uv run pybabel extract -F $(BABEL_CFG) -o $(POT_FILE) .

# Initialize a locale, usage: make babel-init LOCALE=ru
babel-init:
	@if [ -z "$(LOCALE)" ]; then echo "LOCALE is required (e.g., make babel-init LOCALE=ru)"; exit 1; fi
	uv run pybabel init -i $(POT_FILE) -d $(TRANS_DIR) -l $(LOCALE)

# Update existing locales from POT
babel-update:
	uv run pybabel update -i $(POT_FILE) -d $(TRANS_DIR)

# Compile MO files for all locales
babel-compile:
	uv run pybabel compile -d $(TRANS_DIR)

# Declare phony targets
.PHONY: install dev start build render-start db-init db-drop babel-extract babel-init babel-update babel-compile