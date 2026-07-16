#!/bin/bash

set -euo pipefail

mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt

cd /app

# Activate pre-built test venv from Dockerfile
# Venv is pre-built in Dockerfile via: uv venv /app/.tbench-testing && uv pip install pytest==8.4.1
# shellcheck disable=SC1091
source /app/.tbench-testing/bin/activate

# Run tests
set +e

PYTHONPATH=/app pytest /tests/test_outputs.py -rA
test_exit_code=$?

set -e

if [ "$test_exit_code" -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
fi