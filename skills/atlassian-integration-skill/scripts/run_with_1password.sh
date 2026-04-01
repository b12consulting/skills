#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${SKILL_DIR}/.env"

if ! command -v op >/dev/null 2>&1; then
  echo "Error: 1Password CLI 'op' is required but was not found on PATH." >&2
  exit 1
fi

if [[ $# -eq 0 ]]; then
  echo "Usage: scripts/run_with_1password.sh <command> [args...]" >&2
  exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Error: ${ENV_FILE} was not found. Create it with op:// secret references first." >&2
  exit 1
fi

exec op run --env-file="${ENV_FILE}" -- "$@"
