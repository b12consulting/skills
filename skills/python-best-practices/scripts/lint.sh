#!/usr/bin/env bash
# lint.sh — Run the full linting suite for a Python project.
#
# Usage:
#   ./scripts/lint.sh [path]
#
# Arguments:
#   path   Directory or file to lint (default: current directory)
#
# Requires: ruff, black, mypy, bandit
# Install:  pip install ruff black mypy bandit
#           or:  uv add --dev ruff black mypy bandit

set -euo pipefail

TARGET="${1:-.}"

echo "==> Checking formatting with Black..."
black --check --diff "$TARGET"

echo ""
echo "==> Linting with Ruff..."
ruff check "$TARGET"

echo ""
echo "==> Type-checking with mypy..."
mypy "$TARGET"

echo ""
echo "==> Security scan with Bandit..."
bandit -r "$TARGET" -ll

echo ""
echo "All checks passed."
