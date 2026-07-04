#!/usr/bin/env bash
# Replicates the "build" job in .github/workflows/jekyll-gh-pages.yml
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

rm -rf ./junk/md_reports
uv run generate-reports ./junk/md_reports
ls -l ./junk/md_reports
