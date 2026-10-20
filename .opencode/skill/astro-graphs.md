---
name: astro-graphs
description: How to run, refresh, and use the three Understand-Anything knowledge graphs (code, domain, wiki) for the astro-science workspace.
---

# astro-graphs

Understand-Anything is installed globally (`~/.understand-anything/repo`, skills in
`~/.agents/skills`, plugin built). Data dir for this project: `.ua/` (English).

## The three graphs

| Graph | Command | Output |
|---|---|---|
| Code graph | `/understand` | `.ua/knowledge-graph.json` |
| Domain flows | `/understand-domain` | domain flow graph |
| Knowledge wiki graph | `/understand-knowledge research/wiki` | wiki entity/claim graph |

## Workflow

1. **First build (full):**

   ```
   /understand --language en
   /understand-domain
   /understand-knowledge research/wiki
   ```

2. **Later updates (incremental by default):** just re-run `/understand` — only changed
   files are re-analyzed. Use `/understand --full` to force a full rebuild, or
   `/understand --review` for a full LLM graph review.

3. **Explore:**

   ```
   /understand-dashboard
   ```

4. **Ask / diff / explain:**

   ```
   /understand-chat How does the GWTC remnant pipeline work?
   /understand-diff
   /understand-explain research/projects/exotic-compact-objects/scripts/download_gwosc.py
   /understand-onboard
   ```

## Configuration

- `.ua/config.json` — `outputLanguage: "en"`, `autoUpdate: false`.
- `.ua/.understandignore` — excludes `.venv`, caches, cloned upstream repos
  (`notebooks/`, `mast_notebooks/`, `gaia-jupyter-notebooks/`, `AstroInteractives/`),
  and large binaries (`.zip`, `.npz`, `.npy`, ...).
- The nested `exotic-compact-objects` repo **is** analyzed (code/models/scripts), but its
  large data files are excluded.

## Keeping it fresh

After a data refresh or notebook change, re-run `/understand`. To auto-update on every
commit, run `/understand --auto-update` once (writes `autoUpdate: true` to config).

## Sharing

Commit `.ua/` (minus `intermediate/`, `tmp/`, `.trash-*`, `diff-overlay.json`). Teammates
can then view the graph without an LLM:

```
npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /home/dawe/Projects/astro-science
```

For graphs >10 MB, use git-lfs (see the Understand-Anything README).
