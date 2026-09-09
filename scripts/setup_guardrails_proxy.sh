#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/setup_guardrails_proxy.sh [/path/to/guardrails-proxy]
# Default path assumes OpenClaw repo was cloned under ~/.openclaw/openclaw
TARGET_DIR=${1:-"$HOME/.openclaw/openclaw/guardrails-proxy"}
SECRETS_FILE="$HOME/.openclaw/config/secrets.env"
VENV_DIR="$TARGET_DIR/.venv"

if [ ! -d "$TARGET_DIR" ]; then
  echo "[!] guardrails-proxy directory not found at: $TARGET_DIR"
  echo "    Pass the correct path as the first argument."
  exit 1
fi

echo "[1/5] Installing system dependencies (python3, pip, venv)..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

echo "[2/5] Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "[3/5] Installing Python requirements..."
if [ -f "$TARGET_DIR/requirements.txt" ]; then
  pip install --upgrade pip
  pip install -r "$TARGET_DIR/requirements.txt"
else
  echo "    requirements.txt not found. Skipping pip install."
fi

echo "[4/5] Linking secrets file..."
if [ ! -f "$SECRETS_FILE" ]; then
  echo "    $SECRETS_FILE not found. Create it and add your API keys (OPENROUTER_API_KEY=...)."
else
  echo "    Using secrets from $SECRETS_FILE"
fi

cat <<'EOF'

[5/5] To run guardrails-proxy manually, execute:

  cd $TARGET_DIR
  set -a && source $SECRETS_FILE && set +a
  source .venv/bin/activate
  python3 main.py

You can also add an alias or systemd service for long-running usage.
EOF
