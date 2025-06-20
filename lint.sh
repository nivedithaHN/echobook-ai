#!/bin/bash

# Make this script executable
# chmod +x lint.sh

# Run the script with:
# ./lint.sh

echo "🔍 Running Black formatter..."
black .

echo "🧹 Running Ruff linter..."
ruff check .

echo "🛠️  Auto-fixing with Ruff..."
ruff check . --fix

echo "📦 Sorting imports with isort..."
isort .

echo "🔎 Running mypy for type checking..."
mypy backend/

echo "✅ All checks completed."