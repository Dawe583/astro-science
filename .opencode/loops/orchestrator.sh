#!/usr/bin/env bash
# =============================================================================
# astro-science — orchestrator
# runs all loops in sequence and writes one combined log + status JSON
#
# Order matters: data refresh changes sources -> notebook health validates the
# results -> graph refresh detects what the /understand agent must re-analyze.
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
LOG_DIR="$ROOT/.opencode/loops/logs"
mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
ORCH_LOG="$LOG_DIR/orchestrator-$TS.log"
STATUS="$LOG_DIR/latest-status.json"

declare -A RESULT
echo "[orchestrator] started $(date -Is)" | tee -a "$ORCH_LOG"

run_loop() {
  local loop="$1"
  echo "=== $loop ===" | tee -a "$ORCH_LOG"
  if "$ROOT/.opencode/loops/$loop.sh" >>"$ORCH_LOG" 2>&1; then
    RESULT["$loop"]="ok"
    echo "[orchestrator] $loop OK" | tee -a "$ORCH_LOG"
  else
    RESULT["$loop"]="failed"
    echo "[orchestrator] $loop FAILED (continuing)" | tee -a "$ORCH_LOG"
  fi
}

run_loop refresh-data
run_loop notebook-health
run_loop refresh-graphs

# --- graph work queue ---------------------------------------------------------
echo "=== graphs (agent queue) ===" | tee -a "$ORCH_LOG"
if [ -f "$ROOT/.ua/refresh-requested.json" ]; then
  echo "[orchestrator] graph drift detected -> .ua/refresh-requested.json" | tee -a "$ORCH_LOG"
  echo "[orchestrator] next agent session must run /understand (and the subdomain merge)" | tee -a "$ORCH_LOG"
else
  echo "[orchestrator] graphs up to date" | tee -a "$ORCH_LOG"
fi

# --- combined status ----------------------------------------------------------
python3 - "$STATUS" "$ORCH_LOG" "${RESULT[refresh-data]}" "${RESULT[notebook-health]}" \
  "${RESULT[refresh-graphs]}" "$ROOT/.ua/refresh-requested.json" <<'PYEOF'
import json, os, sys, time

status_path, log_path, data, notebooks, graphs, request_path = sys.argv[1:7]
status = {
    "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "log": log_path,
    "loops": {
        "refresh-data": data,
        "notebook-health": notebooks,
        "refresh-graphs": graphs,
    },
    "graphRefreshRequested": os.path.exists(request_path),
    "researchLoop": "agent-driven: .opencode/loops/research-loop.sh \"<topic>\"",
}
with open(status_path, "w") as fh:
    json.dump(status, fh, indent=2)
print(f"[orchestrator] status -> {status_path}")
PYEOF

echo "[orchestrator] finished $(date -Is)" | tee -a "$ORCH_LOG"
echo "[orchestrator] log: $ORCH_LOG"
