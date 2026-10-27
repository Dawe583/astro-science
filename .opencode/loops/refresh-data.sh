#!/usr/bin/env bash
# =============================================================================
# astro-science — data refresh loop
# download -> process -> rebuild dashboards/figures -> report
#
# CWD POLICY: every `run` call must execute with the working directory of the
# project that owns the script:
#   - exotic-compact-objects (ECO) scripts: cwd = $EXO
#   - black-holes scripts:                  cwd = $BH
#   - exoplanets + workspace scripts:       cwd = $ROOT
# (Fix 2026-10-27: section 3 previously ran after `cd $ROOT`, so the relative
#  ECO script paths "scripts/build_*.py" failed with "No such file or directory".)
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
# ECO downloads: cwd = $EXO so relative "scripts/..." paths resolve.
cd "$EXO" || exit 1
run "gwosc-download"    "$PY" scripts/download_gwosc.py
run "heasarc-download"  "$PY" scripts/download_heasarc.py
run "blackcat-download" "$PY" scripts/download_blackcat.py

# Quick, idempotent ECO extras (cwd still $EXO):
#   - strain-marquee: 4-kHz HDF5 strain for GW170817/GW190814/GW190521; keeps
#     existing files, so re-runs only refresh the manifest and fetch metadata.
#   - gwb-literature: writes PTA (NANOGrav 15yr / EPTA DR2 / PPTA DR2 / IPTA DR2)
#     summary + posterior files from PUBLISHED values with deterministic
#     synthetic posterior sampling; contains NO network fetch. It is therefore a
#     literature/local regeneration, not a real download.
run "strain-marquee"    "$PY" scripts/download_strain_marquee.py
run "gwb-literature"    "$PY" scripts/download_gwb.py

cd "$BH" || exit 1
run "bh-gwosc-update"   "$PY" scripts/update_gwosc.py

# --- 2. Process --------------------------------------------------------------
cd "$EXO" || exit 1
run "blackcat-process"  "$PY" scripts/process_blackcat.py
run "bh-derived"        "$PY" scripts/add_bh_derived_quantities.py

run "theoretical-data"  "$PY" scripts/build_theoretical_data.py

# --- Exoplanet data download and processing (run from ROOT) ------------------
cd "$ROOT" || exit 1
run "exo-download"    "$PY" research/projects/exoplanets/scripts/download_exoplanets.py
run "exo-process"     "$PY" research/projects/exoplanets/scripts/process_exoplanets.py

# --- 3. Rebuild dashboards/figures ------------------------------------------
# ECO dashboards and figure generators: cwd = $EXO (was $ROOT — the bug).
cd "$EXO" || exit 1
run "gwtc-dashboard"      "$PY" scripts/build_gwtc_remnant_dashboard.py
run "agn-dashboard"       "$PY" scripts/build_agn_reverberation_dashboard.py
run "agn-demographics"    "$PY" scripts/agn_demographics.py
run "premium-figures"     "$PY" scripts/make_premium_figures.py
run "corbet-dashboard"    "$PY" scripts/build_corbet_dashboard.py
run "blackcat-dashboard"  "$PY" scripts/build_blackcat_dashboard.py

# Deliberately NOT part of this loop:
#  - scripts/download_gwosc_o4.py: re-downloads ~10 x ~130 MB O4 strain HDF5
#    files on EVERY run (no skip-if-exists logic) — not idempotent/quick; its
#    metadata CSV also duplicates gwosc-download. Run manually if needed.
#  - scripts/download_gaia_dr3.py: Gaia TAP async queries (TOP 20000 + TOP
#    100000 rows) take minutes and are rate-limit sensitive; they feed no
#    dashboards here. Run manually if needed.
#  - scripts/build_premium_site.py: writes the full premium site HTML (incl.
#    top-level pages/style). Owned by a separate site-redesign workstream;
#    never regenerated from this loop.

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
