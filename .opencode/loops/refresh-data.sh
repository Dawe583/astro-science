#!/usr/bin/env bash
# =============================================================================
# astro-science — data refresh loop
# download -> process -> rebuild dashboards/figures -> report
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
PY="$ROOT/.venv/bin/python"
EXO="$ROOT/research/projects/exotic-compact-objects"
BH="$ROOT/research/projects/black-holes"
LOG_DIR="$ROOT/.opencode/loops/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/refresh-data-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

FAIL=0
run() {
  local label="$1"; shift
  echo "==> [$label] $*"
  if "$@"; then
    echo "    ok: $label"
  else
    echo "    FAIL: $label" >&2
    FAIL=1
  fi
}

echo "[refresh-data] started $(date -Is)"

# --- 1. Download -------------------------------------------------------------
cd "$EXO" || exit 1
run "gwosc-download"   "$PY" scripts/download_gwosc.py
run "heasarc-download" "$PY" scripts/download_heasarc.py
run "blackcat-download" "$PY" scripts/download_blackcat.py

cd "$BH" || exit 1
run "bh-gwosc-update"  "$PY" scripts/update_gwosc.py

# --- 2. Process --------------------------------------------------------------
cd "$EXO" || exit 1
run "blackcat-process" "$PY" scripts/process_blackcat.py
run "bh-derived"       "$PY" scripts/add_bh_derived_quantities.py
run "theoretical-data" "$PY" scripts/build_theoretical_data.py

# Exoplanet data download and processing
run "exo-download"     "$PY" research/projects/exoplanets/scripts/download_exoplanets.py
run "exo-process"      "$PY" research/projects/exoplanets/scripts/process_exoplanets.py

# --- 3. Rebuild dashboards/figures ------------------------------------------
run "gwtc-dashboard"   "$PY" scripts/build_gwtc_remnant_dashboard.py
run "agn-dashboard"    "$PY" scripts/build_agn_reverberation_dashboard.py
run "blackcat-dashboard" "$PY" scripts/build_blackcat_dashboard.py

# --- 4. Report ---------------------------------------------------------------
REPORT="$EXO/reports/refresh-$(date +%Y%m%d-%H%M%S).md"
{
  echo "# Data refresh — $(date -Is)"
  echo
  echo "Overall: $([ "$FAIL" -eq 0 ] && echo OK || echo FAILED)"
  echo
  echo "Log: \`$LOG\`"
} > "$REPORT"
echo "[refresh-data] report -> $REPORT"
echo "[refresh-data] finished $(date -Is)"

exit "$FAIL"
