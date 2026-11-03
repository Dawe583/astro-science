# Subdomain graph refresh report — 2026-11-03

## Scope
Deferred subdomain (`research/projects/exotic-compact-objects`) incremental refresh
completed per astro-graphs skill. Patched pipeline used from
`/tmp/opencode/ua-refresh/` (worktree-inclusive diff, subdomain path
normalization); plugin at `~/.understand-anything/repo` left untouched.

## Subdomain graph
- Before: 302 nodes / 195 edges (commit e6aaf54)
- After:  344 nodes / 227 edges (commit f768018)
- Changed files analyzed: 31 (models/derivations.py, notebooks 25/28, premium/js/*,
  reports/*, scripts/*, premium/theory_wormholes.md, etc.)
- Merge: exotic-compact-objects-knowledge-graph.json updated and copied to
  root `.ua/`.

## Root merged graph
- Before: 1188 nodes / 1105 edges
- After:  1231 nodes / 1134 edges (6 layers, 8 tour steps)
- Cohesion edges: 1133 -> 1134 (idempotent re-run added 1 edge; 68 skipped as
  already present).

## Drift check (refresh-graphs.sh)
- subdomain: 0 (target met)
- root: 4 (not cleared) — reasons documented:
  - root.added: research/projects/local-volume/scripts/download_local_volume_gaia.py
  - root.changed: docs/DATA_PROVENANCE.md, docs/GRAPHS.md (this report's edit),
    research/wiki/Wormholes.md
  These are pre-existing/data-refresh drift outside this task's subdomain scope;
  root incremental refresh not run (root was marked complete; no commit made).

## Provenance / units
- Subdomain graph rebuilt from source via patched prepare-incremental +
  extract-structure + merge-batch-graphs; no data fabricated.
- Backups: /tmp/opencode/backup-graphs/{subdomain,root-exotic,root}-kg-before.json
