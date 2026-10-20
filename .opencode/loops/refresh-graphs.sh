#!/usr/bin/env bash
# =============================================================================
# astro-science — graph refresh loop (deterministic drift detector)
#
# Compares the current source tree against the committed knowledge graphs and
# writes .ua/refresh-requested.json when an agent-driven /understand refresh is
# needed. This script NEVER invokes the LLM itself — it only detects drift and
# prepares the exact work list, keeping graph refreshes cheap and auditable.
#
# Drift sources:
#   root       — content hashes vs .ua/fingerprints.json (added/changed/removed)
#   subdomain  — file list vs .ua/exotic-compact-objects-knowledge-graph.json
#                plus mtime newer than the graph build (changed files)
#
# Outputs:
#   .ua/refresh-requested.json   (present only while drift exists)
#   logs/graph-refresh-<ts>.log
#
# Exit codes: 0 = ran fine (drift or not), 1 = tooling failure
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
UA="$ROOT/.ua"
EXO="$ROOT/research/projects/exotic-compact-objects"
SCAN="$HOME/.understand-anything/repo/understand-anything-plugin/skills/understand/scan-project.mjs"
LOG_DIR="$ROOT/.opencode/loops/logs"
mkdir -p "$LOG_DIR" "$UA/tmp"
LOG="$LOG_DIR/graph-refresh-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "[graph-refresh] started $(date -Is)"

if [ ! -f "$SCAN" ]; then
  echo "[graph-refresh] FAIL: scanner not found at $SCAN"
  exit 1
fi

# --- 1. Deterministic scans --------------------------------------------------
node "$SCAN" "$ROOT" "$UA/tmp/ua-scan-current.json" --exclude-analysis-data
if [ $? -ne 0 ]; then
  echo "[graph-refresh] FAIL: root scan failed"
  exit 1
fi

node "$SCAN" "$EXO" "$UA/tmp/ua-scan-subdomain-current.json" \
  --exclude 'data/**,figures/**,results/**,docs/**,premium/figures/**,*.fits,*.npz,*.npy,*.h5,*.hdf5,*.zarr,*.csv,*.tsv,*.zip,*.png,*.jpg,*.jpeg,*.pdf,*.html,*.css'
if [ $? -ne 0 ]; then
  echo "[graph-refresh] FAIL: subdomain scan failed"
  exit 1
fi

# --- 2. Drift comparison -----------------------------------------------------
"$ROOT/.venv/bin/python" - "$ROOT" <<'PYEOF'
import hashlib
import json
import os
import sys
import time
from pathlib import Path

root = Path(sys.argv[1])
ua = root / ".ua"
request_path = ua / "refresh-requested.json"

def load(p):
    return json.loads(Path(p).read_text())

def sha256(path):
    # Mirror the plugin's prepare-incremental.mjs: hash the UTF-8 decoded content
    # (readFileSync(path, 'utf-8')), NOT raw bytes — binary files hash as text.
    content = open(path, "rb").read().decode("utf-8", errors="replace")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def scan_paths(p):
    return {f["path"] for f in load(p)["files"]}

root_current = scan_paths(ua / "tmp/ua-scan-current.json")
fingerprints = {
    p: v for p, v in load(ua / "fingerprints.json")["files"].items()
    if not p.startswith(".ua/")  # generated analysis data, excluded from scans
}

root_added = sorted(root_current - set(fingerprints))
root_removed = sorted(set(fingerprints) - root_current)
root_changed = []
for rel in sorted(root_current & set(fingerprints)):
    fp = root / rel
    try:
        if sha256(fp) != fingerprints[rel]["contentHash"]:
            root_changed.append(rel)
    except OSError:
        root_changed.append(rel)

# Subdomain: compare against the node file list of the committed subgraph.
sub_graph_path = ua / "exotic-compact-objects-knowledge-graph.json"
sub_added = sub_removed = sub_changed = []
if sub_graph_path.exists():
    sub_graph = load(sub_graph_path)
    exo = root / "research/projects/exotic-compact-objects"
    graph_mtime = sub_graph_path.stat().st_mtime
    scanned = scan_paths(ua / "tmp/ua-scan-subdomain-current.json")
    graph_files = set()
    prefix = "research/projects/exotic-compact-objects/"
    for node in sub_graph.get("nodes", []):
        fp = node.get("filePath")
        if fp:
            # The merge namespaced the project README; normalize back to the
            # subdomain-relative path used by scans.
            graph_files.add(fp[len(prefix):] if fp.startswith(prefix) else fp)
    sub_added = sorted(scanned - graph_files)
    sub_removed = sorted(f for f in graph_files if f not in scanned)
    for rel in sorted(scanned & graph_files):
        try:
            if (exo / rel).stat().st_mtime > graph_mtime:
                sub_changed.append(rel)
        except OSError:
            sub_changed.append(rel)

drift = {
    "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "root": {"added": root_added, "changed": root_changed, "removed": root_removed},
    "subdomain": {"added": sub_added, "changed": sub_changed, "removed": sub_removed},
}

counts = {k: sum(len(v) for v in drift[k].values()) for k in ("root", "subdomain")}
total = counts["root"] + counts["subdomain"]

if total:
    drift["actions"] = [
        "root: run /understand (incremental) — it will re-analyze the listed files",
        "subdomain: run /understand with research/projects/exotic-compact-objects as root, "
        "then merge with merge-subdomain-graphs.py",
        "after refresh: re-run .ua/tools/add-cohesion-edges.py (idempotent) "
        "and update layer/tour counts in docs/GRAPHS.md",
    ]
    request_path.write_text(json.dumps(drift, indent=2) + "\n")
    print(f"[graph-refresh] DRIFT root={counts['root']} subdomain={counts['subdomain']}")
    for scope in ("root", "subdomain"):
        for kind in ("added", "changed", "removed"):
            items = drift[scope][kind]
            if items:
                shown = ", ".join(items[:5]) + (f" (+{len(items)-5} more)" if len(items) > 5 else "")
                print(f"  {scope}.{kind}: {shown}")
    print(f"[graph-refresh] work list -> {request_path}")
    print("[graph-refresh] agent action required: run /understand (see actions[])")
else:
    if request_path.exists():
        request_path.unlink()
        print("[graph-refresh] stale refresh-requested.json removed")
    print("[graph-refresh] graphs up to date — no drift")
PYEOF

echo "[graph-refresh] finished $(date -Is)"
echo "[graph-refresh] log: $LOG"
exit 0
