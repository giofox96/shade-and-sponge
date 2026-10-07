#!/bin/bash
# Cloud sessions only: install the Python deps for scripts/. Local Windows uses the conda env.
set -euo pipefail
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
pip install --quiet --disable-pip-version-check --break-system-packages -r "$CLAUDE_PROJECT_DIR/requirements.txt"
echo 'export PYTHONIOENCODING=utf-8' >> "$CLAUDE_ENV_FILE"
