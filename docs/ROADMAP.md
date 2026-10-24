---
title: Development Roadmap
date: 2026-10-24
tags:
  - roadmap
  - plan
  - development
aliases:
  - ROADMAP
  - Dev Plan
---

# Development Roadmap — astro-science

> Status (2026-10-24, autonomous pass): Phases A (mostly), B (data refresh + notebooks + formulas), D (site publish) completed. Phase C (exoplanets) partially (verify_formulas added, notebooks 11/11 pass). Phase E (Obsidian) deferred per user. Phase F/G in progress.

> Detailed plan for further development, derived from a full pass over the workspace:
> Understand-Anything graphs (code / domain / wiki), graphify (1295 nodes / 1717 edges),
> Obsidian vault setup, and the existing loops. All outputs in **English** (project convention).

## 0. Status snapshot (2026-10-24)

| Area | State |
|---|---|
| Workspace | 4 research projects: `exotic-compact-objects` (flagship), `black-holes`, `black-holes-wormholes`, **`exoplanets`** (NEW, not in CONTEXT.md) |
| Understand-Anything | 3 graphs committed (code 184n/233e, domain 58n/59e, wiki 82n/176e); drift reports **2 changed premium docs** + intermediate noise |
| graphify | New: 1295 nodes / 1717 edges / 274 communities; HTML `graphify-out/graph.html`; Obsidian export 1569 notes in `graphify-out/obsidian/` |
| Obsidian | App 1.14.5 installed (`~/Applications/Obsidian-1.14.5.AppImage`); vault = project root (`.obsidian/`); `Home.md` MOC added |
| obsidian-skills | Installed at `~/.opencode/skills/obsidian-skills` (6 skills discovered by OpenCode) |
| graphify | Installed via `uv tool` (0.9.95); `graphify-mcp` available |
| Loops | 5 loops present (`refresh-data`, `notebook-health`, `publish-site`, `research`, `refresh-graphs`); orchestrator writes `latest-status.json` |
| CI | `.github/workflows/ci.yml` exists in the nested repo |
| Notebooks | 23 in `exotic-compact-objects/notebooks/` (01..24_quantum_gravity); 1 in `exoplanets` |

## 1. Phase A — Graph & documentation hygiene (immediate, ~1 day)

**Goal:** make the three Understand-Anything graphs and CONTEXT.md truthful again.

1. **Refresh the Understand-Anything subdomain graph** (drift queued 2 premium docs):
   ```bash
   .opencode/loops/refresh-graphs.sh            # confirm work list
   # then run /understand (incremental) for the queued files
   python3 ~/.agents/skills/understand/merge-subdomain-graphs.py
   .venv/bin/python .ua/tools/add-cohesion-edges.py
   ```
   - Re-run `refresh-graphs.sh` afterwards; expect `DRIFT root=0 subdomain=0`.
2. **Exclude `graphify-out/` from the Understand-Anything scan** — add `graphify-out/` to `.ua/.understandignore` (and root `.understandignore`) so the drift loop stops reporting the sidecar.
3. **Document the `exoplanets` project**:
   - Add a `4.4 exoplanets` subsection to `CONTEXT.md` (mirroring §4.1) — models (`models/equations.py`), scripts (`download_exoplanets.py`, `process_exoplanets.py`), notebooks (`01_exoplanet_catalog.ipynb`), premium theory (5 docs), reports (`demographics.md`).
   - Add `exoplanets` row to the research-projects table in the `astro-science` skill.
4. **Clean graphify dangling edges** (423 dangling endpoints from cross-chunk ID mismatches):
   - Re-run `add-cohesion-edges.py`-equivalent? graphify has no cohesion script; instead re-run extraction with `--update` after fixing the wiki node IDs to the `{stem}_{entity}` convention consistently (chunk 4 already uses it; verify chunk 3a wiki IDs match).
   - Re-run `graphify . --update` and confirm dangling count drops.
5. **Verify** `GRAPH_REPORT.md` God Nodes / Surprising Connections / Suggested Questions sections are sane; paste into chat for review.

**DoD:** `refresh-graphs.sh` reports zero drift; `CONTEXT.md` lists 4 projects; graphify `--update` runs clean.

## 2. Phase B — Data refresh & notebook health (~2 days)

**Goal:** bring catalogs and notebooks to a known-good state.

1. **Data refresh loop:**
   ```bash
   .opencode/loops/refresh-data.sh
   ```
   - Downloads: GWOSC/GWTC, HEASARC (XRB/ULX/M87/Sgr A*), SXS, EHT, Planck, SDSS, Gaia DR3, BlackCAT, GWB/strain, X-ray binaries.
   - Rebuilds: `build_theoretical_data.py`, `process_blackcat.py`, `add_bh_derived_quantities.py`, 3 dashboards.
   - **Back up** `research/projects/black-holes/data/black_holes.sqlite` first (script replaces the table).
2. **Notebook health loop:**
   ```bash
   .opencode/loops/notebook-health.sh
   ```
   - Executes all 24 exotic-compact-objects notebooks + exoplanets notebook; fixes root causes; writes report.
   - Use `/understand-explain <notebook>` to locate failures.
3. **Formula verification:** run `verify_formulas.py` and `compute_with_data.py`; reconcile any drift in `reports/derivations_report.md`.
4. **Refresh graphs** after the data sweep (paths moved, new scripts).

**DoD:** all notebooks execute end-to-end; dashboards regenerate; `verify_formulas.py` passes.

## 3. Phase C — Exoplanets project catch-up (~3 days)

**Goal:** bring the undocumented `exoplanets` project up to flagship standards.

1. **Audit** what exists: `models/equations.py`, scripts (`download_exoplanets.py`, `process_exoplanets.py`), `notebooks/01_exoplanet_catalog.ipynb`, 5 premium theory docs, `reports/demographics.md`.
2. **Extend notebooks** (target: 6–8): atmospheric retrieval, transit spectroscopy, habitability metrics, demographic occurrence rates, orbital dynamics, detection methods.
3. **Add validation**: `verify_formulas.py`-equivalent for exoplanet equations (escape velocity, equilibrium temperature, Jeans parameter, atmospheric mass loss).
4. **Integrate into the premium site**: extend `build_premium_site.py` to include exoplanets theory + figures; add a project switcher.
5. **Add to data refresh loop**: `download_exoplanets.py` + `process_exoplanets.py` steps in `refresh-data.sh`.
6. **Document** in `CONTEXT.md`, `astro-science` skill, and `Home.md` MOC.

**DoD:** exoplanets has ≥6 passing notebooks, verified formulas, and appears in the published site.

## 4. Phase D — Premium site publish & portfolio (~1 day)

**Goal:** ship the research site.

1. **Build + publish:**
   ```bash
   cd research/projects/exotic-compact-objects
   $PY scripts/build_premium_site.py --publish   # syncs premium/ -> docs/ (GitHub Pages)
   ```
2. **Add exoplanets** section (Phase C.4).
3. **Verify** dark-observatory design, dashboard tables, model gallery, Plotly figures, auto TOC render.
4. **Update** `docs/` (root-level) cross-links if new top-level docs added.

**DoD:** GitHub Pages site builds and renders all 4 projects.

## 5. Phase E — Obsidian vault adoption (~1 day)

**Goal:** make the vault the daily driver for notes.

1. **Open the vault**: launch `~/Applications/Obsidian-1.14.5.AppImage`, "Open folder as vault" → `/home/dawe/Projects/astro-science`.
2. **Enable the Obsidian CLI** (for `obsidian-cli` skill): Settings → General → Command line interface → register → restart terminal. Then `obsidian version` should work.
3. **Open the graphify export as a separate vault**: `graphify-out/obsidian/` (1569 notes + `graph.canvas`) for the knowledge-graph view.
4. **Adopt the MOC**: `Home.md` is the entry point; add daily notes under `research/notes/`.
5. **Optional plugins**: Dataview (query frontmatter), Templater, Git (auto-commit notes).
6. **Keep vault hygiene**: `.obsidian/` stays gitignored; generated `graphify-out/` stays ignored.

**DoD:** vault opens cleanly; CLI registered; MOC links resolve.

## 6. Phase F — Research loop: new theory (~ongoing)

**Goal:** produce new derivations, figures, and theory docs.

Candidate threads (from `GRAPH_REPORT.md` Suggested Questions + wiki gaps):
- Exotic compact object discrimination (Kerr vs. wormhole vs. boson star) — extend `exotic_discrimination.md`.
- Quantum gravity phenomenology (Planck-scale corrections to ringdown/QNM).
- Early SMBH growth (JWST candidates: CEERS-1019, GN-z11, Abell 2744-QSO1).
- Exoplanet atmospheric escape & habitability (cross-link to black-hole accretion wiki).
- Remnant energetics & spin distributions from GWTC.

Loop per thread (`research-loop.sh` / `/astro-research`):
hypothesis → derivation (`models/derivations.py`) → figure (`make_premium_figures.py`) → report (`reports/`) → theory doc (`premium/theory_*.md`) → wiki article (`research/wiki/`) → link back via `add-cohesion-edges.py`.

**DoD:** each thread ends with a theory doc + figure + report + wiki article + graph refresh.

## 7. Phase G — Automation & reproducibility (~1 day)

1. **Schedule loops** via cron/heartbeat (see `astro-loops` skill): data refresh weekly, notebook health weekly, publish-site on push, graph refresh after every commit.
2. **Orchestrator**: run `orchestrator.sh` end-to-end once; verify `latest-status.json` shows `graphRefreshRequested` correctly.
3. **Reproducibility**: pin `.venv` versions into `requirements.txt` (currently only 5 lines); record in `SETUP_GUIDE.md`; verify `check-environment.sh`.
4. **CI**: confirm `.github/workflows/ci.yml` runs notebook smoke tests on PR.
5. **Auto-update graphs on commit**: `/understand --auto-update` (sets `autoUpdate: true` in `.ua/config.json`).

**DoD:** a clean clone + `start.sh` reproduces the workspace; CI green.

## 8. Risks & blockers

| Risk | Mitigation |
|---|---|
| `exoplanets` undocumented → knowledge loss | Phase A.3 + C |
| Graphify dangling edges (423) reduce graph fidelity | Phase A.4; track count in `GRAPH_REPORT.md` |
| 438 MB `GW150914_28.zip` (gitignored) — re-download cost | Keep `download_strain_marquee.py` idempotent; cache in `data/raw/` |
| Black-holes SQLite replaced on refresh (data loss) | Back up before `update_gwosc.py` (Phase B.1) |
| Obsidian CLI needs app running + registration | Phase E.2; document in SETUP_GUIDE |
| Understand-Anything drift noise from `graphify-out/` | Phase A.2 |
| Free-tier subagent limits (graphify semantic extraction) | Run subagents sequentially, not in parallel; or set `GEMINI_API_KEY` |

## 9. Success metrics

- `refresh-graphs.sh` → 0 drift (root + subdomain).
- All notebooks execute (notebook-health loop green).
- `verify_formulas.py` passes for both exotic-compact-objects and exoplanets.
- Premium site builds & publishes (GitHub Pages) with 4 projects.
- Obsidian vault opens; MOC links resolve; CLI registered.
- graphify `--update` runs with dangling-edge count < 50.
- `requirements.txt` pins all runtime deps; clean clone reproduces.

## 10. Immediate next actions (this session)

1. Refresh Understand-Anything subdomain graph (Phase A.1).
2. Add `graphify-out/` to `.understandignore` (Phase A.2).
3. Document `exoplanets` in `CONTEXT.md` (Phase A.3).
4. Run data refresh + notebook health (Phase B) — *requires network + time; schedule*.
5. Open Obsidian vault & enable CLI (Phase E).
EOF
echo "ROADMAP.md written"