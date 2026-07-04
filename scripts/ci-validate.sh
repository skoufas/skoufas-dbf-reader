#!/usr/bin/env bash
# Replicates the "validation" job in .github/workflows/CI.yml
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv sync --locked --all-extras --dev

uv run ruff check ./src
uv run ruff format --check --diff
uv run bandit .
uv run pytest
