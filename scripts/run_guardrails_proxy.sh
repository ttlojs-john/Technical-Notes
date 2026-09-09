#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
TARGET_DIR=${1:-"$HOME/.openclaw/openclaw/guardrails-proxy"}
SECRETS_FILE="$HOME/.openclaw/config/secrets.env"
SETUP_SCRIPT="$SCRIPT_DIR/setup_guardrails_proxy.sh"
VENV_DIR="$TARGET_DIR/.venv"

if [ ! -d "$TARGET_DIR" ]; then
  echo "[!] guardrails-proxy directory not found at: $TARGET_DIR"
  echo "    Pass the correct path as the first argument."
  exit 1
fi

if [ ! -f "$SECRETS_FILE" ]; then
  echo "[!] $SECRETS_FILE not found. Create it and add OPENROUTER_API_KEY=..."
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "[i] Virtualenv not found. Running setup script first..."
  "$SETUP_SCRIPT" "$TARGET_DIR"
fi

set -a
source "$SECRETS_FILE"
set +a

source "$VENV_DIR/bin/activate"

cd "$TARGET_DIR"
echo "[i] Starting guardrails-proxy from $(pwd)"
python3 main.py
