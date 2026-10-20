# astro-science loops

Three automation loops for the workspace. All scripts are self-contained, log to
`logs/`, and exit non-zero on failure.

| Script | Loop | Purpose |
|---|---|---|
| `refresh-data.sh` | Data refresh | Download → process → rebuild dashboards/figures |
| `notebook-health.sh` | Notebook health | Execute every notebook → collect failures |
| `research-loop.sh "<topic>"` | Research | Set up a research work dir + hypothesis template |
| `orchestrator.sh` | All | Runs the loops in sequence |

## Run manually

```bash
cd /home/dawe/Projects/astro-science
.opencode/loops/refresh-data.sh
.opencode/loops/notebook-health.sh
.opencode/loops/research-loop.sh "ISCO radius vs spin"
.opencode/loops/orchestrator.sh
```

Or via OpenCode commands: `/astro-refresh-data`, `/astro-notebook-health`,
`/astro-research`, `/astro-graphs`.

## Schedule autonomously

The scripts are cron/heartbeat-ready. Example crontab:

```cron
0 3 * * 0 cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-data.sh
30 1 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/notebook-health.sh
```

Inside an agent session, an RLM heartbeat (see the `rlm-heartbeat` skill) can prompt
the session to run a loop on an interval.

## Environment

- Python: `/home/dawe/Projects/astro-science/.venv/bin/python`
- Logs: `.opencode/loops/logs/`
- Notebooks execute with a 900 s timeout (override with `NOTEBOOK_TIMEOUT`).
