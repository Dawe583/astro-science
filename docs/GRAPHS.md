# astro-science Graphs

Understand-Anything is installed globally and built. It turns the workspace into
machine-readable knowledge graphs.

- Repo: `~/.understand-anything/repo`
- Skills: `~/.agents/skills/understand*`
- Project data dir: `/home/dawe/Projects/astro-science/.ua/`

---

## Architecture — three graphs

| # | Graph | Command | What it captures |
|---|---|---|---|
| 1 | **Code graph** | `/understand` | Files, functions, classes, imports, architecture layers, guided tour |
| 2 | **Domain flows** | `/understand-domain` | Research domains, flows, process steps |
| 3 | **Knowledge wiki graph** | `/understand-knowledge research/wiki` | Entities, claims, implicit relationships from the Karpathy wiki |

The code graph is split into two parts that are **merged**:

- Root graph — the workspace itself (`research/`, `data/`, top-level docs, `.opencode/`).
- Subdomain graph — `research/projects/exotic-compact-objects/` (a separate git repo),
  built independently and merged via `merge-subdomain-graphs.py`.

---

## Data directory layout

```
.ua/
├── config.json              # outputLanguage: en
├── .understandignore        # scan exclusions
├── knowledge-graph.json     # the merged code graph (committed)
├── meta.json                # git hash + scan metadata (committed)
├── fingerprints.json        # change detection (committed)
├── <subdomain>-knowledge-graph.json   # subdomain inputs (transient)
├── intermediate/            # scratch (gitignored)
└── tmp/                     # scratch (gitignored)
```

`.gitignore` keeps everything in `.ua/` except `intermediate/`, `tmp/`, `.trash-*`,
and `diff-overlay.json`.

---

## Refresh procedure

```bash
cd /home/dawe/Projects/astro-science

# Incremental (default — only changed files re-analyzed)
/understand
/understand-domain
/understand-knowledge research/wiki

# Full rebuild
/understand --full

# LLM review of the graph
/understand --review
```

Explore the result:

```
/understand-dashboard
```

Ask / diff / explain:

```
/understand-chat How does the GWTC remnant pipeline work?
/understand-diff
/understand-explain research/projects/black-holes/scripts/update_gwosc.py
/understand-onboard
```

---

## Exclusions (`.understandignore`)

- `.venv/`, caches, `__pycache__/`, `.ipynb_checkpoints/`, `catboost_info/`
- Cloned upstream tutorial repos: `/notebooks/`, `/mast_notebooks/`,
  `/gaia-jupyter-notebooks/`, `/AstroInteractives/` (anchored to root)
- Large binaries: `*.zip`, `*.npz`, `*.npy`, `*.h5`, `*.hdf5`, `*.zarr`
- The nested `exotic-compact-objects` repo (handled as a subdomain graph)

---

## Keeping it fresh

- Re-run `/understand` after any code or notebook change.
- To auto-update on every commit, run `/understand --auto-update` once.
- The orchestrator loop reminds you to refresh the graphs after a data sweep.

## Sharing

Commit `.ua/` (minus scratch). Teammates can view the graph with no LLM:

```bash
npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /home/dawe/Projects/astro-science
```

For graphs > 10 MB, use git-lfs.
