---
name: astro-loops
description: How the three automation loops (data refresh, notebook health, research) run in astro-science and how to trigger them. Use to start, schedule, or debug a loop.
---

# astro-loops

Three loops orchestrate the workspace. All scripts live in
`/home/dawe/Projects/astro-science/.opencode/loops/`.

## The three loops

| Loop | Script | What it does |
|---|---|---|
| Data refresh | `refresh-data.sh` | Downloads new data → processes → rebuilds dashboards/figures |
| Notebook health | `notebook-health.sh` | Executes every notebook → collects failures → writes a report |
| Research | `research-loop.sh` | Hypothesis → derivation → figure → report → theory doc |

## Trigger modes

**Manual (recommended for research):**

```bash
.opencode/loops/refresh-data.sh          # or: /astro-refresh-data
.opencode/loops/notebook-health.sh       # or: /astro-notebook-health
.opencode/loops/research-loop.sh         # or: /astro-research
```

**Autonomous (cron / heartbeat):** the scripts are self-contained and log to
`.opencode/loops/logs/`. To run them on a schedule, add entries to crontab, e.g.:

```cron
# refresh data weekly (Sundays 03:00)
0 3 * * 0 cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-data.sh
# notebook health nightly
30 1 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/notebook-health.sh
```

Or, inside an agent session, use an RLM heartbeat (see the `rlm-heartbeat` skill) to
prompt the session to run a loop on an interval.

## Orchestrator

`.opencode/loops/orchestrator.sh` runs all three loops in sequence and writes a single
`.opencode/loops/logs/orchestrator-<timestamp>.log`. Use it for a full sweep.

## Rules

- Always run from the project root (`cd /home/dawe/Projects/astro-science`).
- Use the absolute venv python: `/home/dawe/Projects/astro-science/.venv/bin/python`.
- A loop must never silently fail: it writes a status line and exits non-zero on error.
- After any data refresh, re-run the graphs (see `astro-graphs`) so the graph stays fresh.
