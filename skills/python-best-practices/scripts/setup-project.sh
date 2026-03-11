#!/usr/bin/env bash
# setup-project.sh — Scaffold a new Python project with the recommended structure.
#
# Usage:
#   ./scripts/setup-project.sh <project-name>
#
# Creates:
#   <project-name>/
#   ├── src/<package_name>/__init__.py
#   ├── tests/__init__.py
#   ├── pyproject.toml          (from references/pyproject-template.toml)
#   ├── .gitignore
#   └── README.md

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-name>"
  exit 1
fi

PROJECT_NAME="$1"
PACKAGE_NAME="${PROJECT_NAME//-/_}"   # kebab-case → snake_case
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFERENCES_DIR="$SCRIPT_DIR/../references"

echo "==> Creating project '$PROJECT_NAME'..."

mkdir -p "$PROJECT_NAME/src/$PACKAGE_NAME"
mkdir -p "$PROJECT_NAME/tests"

# src package init
cat > "$PROJECT_NAME/src/$PACKAGE_NAME/__init__.py" << EOF
"""$PROJECT_NAME package."""
EOF

# tests init
cat > "$PROJECT_NAME/tests/__init__.py" << EOF
EOF

# pyproject.toml — copy template and substitute project name / package name
if [[ -f "$REFERENCES_DIR/pyproject-template.toml" ]]; then
  sed \
    -e "s/YOUR-PROJECT-NAME/$PROJECT_NAME/g" \
    -e "s/your_package_name/$PACKAGE_NAME/g" \
    "$REFERENCES_DIR/pyproject-template.toml" \
    > "$PROJECT_NAME/pyproject.toml"
else
  echo "Warning: references/pyproject-template.toml not found; skipping pyproject.toml"
fi

# .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'EOF'
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.mypy_cache/
.ruff_cache/
.pytest_cache/
htmlcov/
.coverage
EOF

# README
cat > "$PROJECT_NAME/README.md" << EOF
# $PROJECT_NAME

## Installation

\`\`\`bash
uv venv && uv pip install -e ".[dev]"
\`\`\`

## Development

\`\`\`bash
# Lint and type-check
bash scripts/lint.sh

# Run tests
pytest
\`\`\`
EOF

echo ""
echo "Project '$PROJECT_NAME' created successfully."
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  uv venv && uv pip install -e '.[dev]'"
