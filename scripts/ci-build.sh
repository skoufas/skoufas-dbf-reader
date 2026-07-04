#!/usr/bin/env bash
# Replicates the "build" job in .github/workflows/CI.yml (without mutating the
# project version the way the release/PR/push steps do on GitHub Actions).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv build
