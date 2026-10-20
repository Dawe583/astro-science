#!/usr/bin/env bash
# =============================================================================
# astro-science — publish the research website
#
# Rebuilds the premium site from the catalogues and copies it into docs/ so
# GitHub Pages always reflects the current data. Deterministic: no LLM, no
# network. Safe to run on every data refresh.
# =============================================================================
set -euo pipefail

ROOT="/home/dawe/Projects/astro-science"
PROJECT="$ROOT/research/projects/exotic-compact-objects"
PY="$ROOT/.venv/bin/python"

if [ ! -f "$PROJECT/scripts/build_premium_site.py" ]; then
  echo "[publish-site] no site builder at $PROJECT/scripts/build_premium_site.py"
  exit 0
fi

echo "[publish-site] building $(date -Is)"
"$PY" "$PROJECT/scripts/build_premium_site.py" --publish
"$PY" "$PROJECT/scripts/style_notebook_renders.py"

echo "[publish-site] done"
