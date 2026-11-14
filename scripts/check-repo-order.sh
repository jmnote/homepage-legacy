#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/check-repo-order.py" "${1:-index.html}"
