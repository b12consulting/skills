#!/usr/bin/env bash
# setup-project.sh — Scaffold a new Python project with the recommended structure.
#
# Usage:
#   ./scripts/setup-project.sh <project-name>

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-name>"
  exit 1
fi

PROJECT_NAME="$1"

echo "==> Creating project '$PROJECT_NAME'..."
uv init --lib "$PROJECT_NAME"

echo ""
echo "Project '$PROJECT_NAME' created successfully."
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  uv sync"
