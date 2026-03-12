#!/usr/bin/env bash
# lint.sh — Run the full linting suite for a Python project.
#
# Usage:
#   ./scripts/lint.sh [path]
#
# Arguments:
#   path   Directory or file to lint (default: current directory)
#
# Requires: ruff, ty, bandit
# Install:  uv add --dev ruff ty bandit

set -euo pipefail

TARGET="${1:-.}"

echo "==> Checking formatting with Ruff..."
ruff format --check --diff "$TARGET"

echo ""
echo "==> Linting with Ruff..."
ruff check "$TARGET"

echo ""
echo "==> Type-checking with ty..."
ty check "$TARGET"

echo ""
echo "==> Security scan with Bandit..."
bandit -r "$TARGET" -ll

echo ""
echo "All checks passed."
