#!/usr/bin/env bash
# =============================================================================
# astro-science — orchestrator
# runs all three loops in sequence and writes one combined log
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
LOG_DIR="$ROOT/.opencode/loops/logs"
mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
ORCH_LOG="$LOG_DIR/orchestrator-$TS.log"

echo "[orchestrator] started $(date -Is)" | tee -a "$ORCH_LOG"

for loop in refresh-data notebook-health; do
  echo "=== $loop ===" | tee -a "$ORCH_LOG"
  if "$ROOT/.opencode/loops/$loop.sh" >>"$ORCH_LOG" 2>&1; then
    echo "[orchestrator] $loop OK" | tee -a "$ORCH_LOG"
  else
    echo "[orchestrator] $loop FAILED (continuing)" | tee -a "$ORCH_LOG"
  fi
done

echo "=== graphs (incremental) ===" | tee -a "$ORCH_LOG"
echo "[orchestrator] run /understand and /understand-knowledge to refresh graphs" | tee -a "$ORCH_LOG"

echo "[orchestrator] finished $(date -Is)" | tee -a "$ORCH_LOG"
echo "[orchestrator] log: $ORCH_LOG"
