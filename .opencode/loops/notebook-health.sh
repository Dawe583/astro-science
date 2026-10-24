#!/usr/bin/env bash
# =============================================================================
# astro-science — notebook health loop
# execute every notebook -> collect failures -> report
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
PY="$ROOT/.venv/bin/python"
LOG_DIR="$ROOT/.opencode/loops/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/notebook-health-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

TIMEOUT="${NOTEBOOK_TIMEOUT:-900}"

echo "[notebook-health] started $(date -Is)"

"$PY" - "$ROOT" "$TIMEOUT" "$LOG_DIR/notebook-health-latest.json" <<'PYEOF'
import json, os, subprocess, sys, time
from pathlib import Path

root = Path(sys.argv[1])
timeout = int(sys.argv[2])
report_path = Path(sys.argv[3])

projects = [
    root / "research/projects/exotic-compact-objects/notebooks",
    root / "research/projects/black-holes-wormholes/notebooks",
    root / "research/projects/exoplanets/notebooks",
]
results = []
for pdir in projects:
    if not pdir.is_dir():
        continue
    for nb in sorted(pdir.glob("*.ipynb")):
        if nb.name.startswith("."):
            continue
        out = nb.with_suffix(".health-check.ipynb")
        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute",
                 "--ExecutePreprocessor.timeout=%d" % timeout,
                 "--output", out.name, str(nb)],
                cwd=str(nb.parent), capture_output=True, text=True,
                timeout=timeout + 120,
            )
            ok = proc.returncode == 0
            err = (proc.stderr or "").strip().splitlines()[-1:] or [""]
            results.append({"notebook": str(nb.relative_to(root)), "status": "ok" if ok else "failed",
                            "seconds": round(time.time() - t0, 1), "error": err[0]})
            out.unlink(missing_ok=True)
        except subprocess.TimeoutExpired:
            results.append({"notebook": str(nb.relative_to(root)), "status": "timeout",
                            "seconds": timeout, "error": "exceeded %ds" % timeout})
        except Exception as e:
            results.append({"notebook": str(nb.relative_to(root)), "status": "error",
                            "seconds": 0, "error": str(e)})

report = {
    "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "timeoutSeconds": timeout,
    "total": len(results),
    "ok": sum(1 for r in results if r["status"] == "ok"),
    "failed": sum(1 for r in results if r["status"] == "failed"),
    "timeout": sum(1 for r in results if r["status"] == "timeout"),
    "error": sum(1 for r in results if r["status"] == "error"),
    "results": results,
}
print(json.dumps(report, indent=2))
report_path.write_text(json.dumps(report, indent=2) + "\n")
failures = report["failed"] + report["timeout"] + report["error"]
print("[notebook-health] %d/%d ok, %d not ok" % (report["ok"], report["total"], failures))
sys.exit(0 if failures == 0 else 1)
PYEOF
STATUS=$?

echo "[notebook-health] finished $(date -Is)"
exit "$STATUS"
