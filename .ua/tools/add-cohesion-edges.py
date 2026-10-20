#!/usr/bin/env python3
"""Add evidence-based cohesion edges to .ua/knowledge-graph.json.

Goal: reduce isolated nodes and connected-component count in the merged code
graph by ADDING edges that are backed by real, auditable evidence:

  (a) documents <-> code relations: loop scripts (.opencode/loops/*.sh) and
      docs/AUTOMATION.md -> the files each loop touches; OpenCode commands ->
      the agents/loops/skills they invoke; project READMEs -> their project
      files; top-level docs -> the files they name.
  (b) file<->file relations derived from .ua/domain-graph.json: the nodes a
      flow's steps reference (entry point + step filePath + summary file
      references) are chained with "related" edges.
  (c) wiki-article <-> code-level topical links, ONLY where the article text
      explicitly discusses machinery that exists as a script/notebook, plus
      wiki index -> article relations (the index literally lists them).

Hard rules enforced by this script:
  * node set, `layers` and `tour` arrays are NOT modified;
  * no self-loops; no dangling endpoints; no duplicate (source, target, type)
    edges; an edge whose (source, target) pair already exists in ANY form is
    not re-added with another type;
  * default filter: keep an edge only if it rescues an isolated node or
    connects two different components (plus a small capped "seed" group list
    that carries documented-but-intra-component edges);
  * every added edge carries a one-sentence `description` with the evidence;
  * idempotent: a second run adds nothing.

Outputs:
  * .ua/knowledge-graph.json  (modified in place: `edges` array only)
  * .ua/cohesion-edges.json   (array of added edges with rationales)

Run:  python3 .ua/tools/add-cohesion-edges.py [--dry-run]
"""

from __future__ import annotations

import copy
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = ROOT / ".ua"
KG_PATH = UA / "knowledge-graph.json"
DG_PATH = UA / "domain-graph.json"
OUT_ADDED = UA / "cohesion-edges.json"
ECO_SUBDOMAIN = "research/projects/exotic-compact-objects"

# Edge-type -> default weight, mirroring the weights already used in the graph.
DEFAULT_WEIGHT = {
    "documents": 0.5,
    "depends_on": 0.6,
    "related": 0.5,
    "triggers": 0.6,
    "writes_to": 0.5,
}


# ----------------------------------------------------------------------------
# graph helpers
# ----------------------------------------------------------------------------


def union_find_components(node_ids, edges):
    """Union-find over node ids; returns dict root -> members."""
    parent = {i: i for i in node_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        if e["source"] in parent and e["target"] in parent:
            rs, rt = find(e["source"]), find(e["target"])
            if rs != rt:
                parent[rs] = rt
    comps = defaultdict(list)
    for i in node_ids:
        comps[find(i)].append(i)
    return comps


def isolated_nodes(node_ids, edges):
    inc = set()
    for e in edges:
        inc.add(e["source"])
        inc.add(e["target"])
    return sorted(i for i in node_ids if i not in inc)


def graph_stats(nodes, edges):
    """Node/edge counts, components, isolated nodes, per-type counts,
    dangling edges and duplicate edges — all computed locally."""
    ids = {n["id"] for n in nodes}
    comps = union_find_components(ids, edges)
    iso = isolated_nodes(ids, edges)
    dangling = [e for e in edges if e["source"] not in ids or e["target"] not in ids]
    seen = Counter((e["source"], e["target"], e["type"]) for e in edges)
    dupes = {k: v for k, v in seen.items() if v > 1}
    return {
        "nodes": len(ids),
        "edges": len(edges),
        "components": len(comps),
        "isolated": len(iso),
        "by_type": dict(Counter(e["type"] for e in edges)),
        "dangling": dangling,
        "dupes": dupes,
    }


# ----------------------------------------------------------------------------
# node -> filesystem resolution (proven by testing both bases, not guessed)
# ----------------------------------------------------------------------------


def node_raw_path(node_id):
    return node_id.split(":", 1)[1]


def resolve_node_fs(node):
    """Filesystem path of a node's underlying file, or None.

    Merge quirk: subdomain nodes carry subdomain-relative paths (models/,
    scripts/, notebooks/, premium/, reports/) while root nodes carry
    root-relative paths.  Which base applies is proven by testing the
    filesystem, so no path guessing is involved.
    """
    raw = node_raw_path(node["id"])
    root_cand = ROOT / raw
    if root_cand.exists():
        return root_cand
    eco_cand = ROOT / ECO_SUBDOMAIN / raw
    if eco_cand.exists():
        return eco_cand
    return None


def readable_source(path):
    """Lowercase text content for evidence scanning, else None."""
    if path is None or not path.exists():
        return None
    name = path.name
    if name.endswith((".md", ".sh", ".py", ".tex")):
        try:
            return path.read_text(errors="replace")
        except OSError:
            return None
    if name.endswith(".ipynb"):
        try:
            nb = json.loads(path.read_text(errors="replace"))
        except (OSError, json.JSONDecodeError):
            return None
        chunks = []
        for cell in nb.get("cells", []):
            if isinstance(cell, dict) and cell.get("cell_type") in ("code", "markdown"):
                chunks.append("".join(cell.get("source", [])))
        return "\n".join(chunks)
    return None


# ----------------------------------------------------------------------------
# fragment index (unambiguous basename/path fragments only)
# ----------------------------------------------------------------------------


class FragmentIndex:
    """Maps unambiguous path fragments (full path + basename) to nodes."""

    def __init__(self, nodes):
        frag_map = defaultdict(list)
        for n in nodes:
            if n["type"] == "function":
                continue
            frag = node_raw_path(n["id"])
            frag_map[frag].append(n)
            frag_map[frag.rsplit("/", 1)[-1]].append(n)
        # ambiguous fragments are ignored -> the graph grows without guesses
        self.unambiguous = {
            frag: group[0]
            for frag, group in frag_map.items()
            if len(group) == 1 and len(frag) >= 5
        }


# ----------------------------------------------------------------------------
# candidate generation
# ----------------------------------------------------------------------------


def add_candidate(cands, source_id, target_id, etype, description, groups):
    if source_id == target_id:
        return
    cands.append(
        {
            "source": source_id,
            "target": target_id,
            "type": etype,
            "description": " ".join(description.split()),
            "weight": DEFAULT_WEIGHT.get(etype, 0.5),
            "_groups": tuple(groups),
        }
    )


def generate_candidates(
    kg, dg, fragment_index, node_by_id, comps_before, comp_of, iso_before
):
    """Deterministically build all candidate edges with evidence text."""
    cands = []

    # --- (a) loop scripts <-> docs/AUTOMATION.md ---------------------------
    automation = "document:docs/AUTOMATION.md"
    for loop_id in [
        "file:.opencode/loops/refresh-data.sh",
        "file:.opencode/loops/notebook-health.sh",
        "file:.opencode/loops/research-loop.sh",
        "file:.opencode/loops/orchestrator.sh",
    ]:
        if loop_id in node_by_id and automation in node_by_id:
            add_candidate(
                cands,
                automation,
                loop_id,
                "documents",
                "AUTOMATION.md documents this loop script as the operator-level entry point for one of the three Loops.",
                ("loop-doc",),
            )

    # --- (a) commands -> agents / loops / skills ---------------------------
    command_rules = [
        (
            "document:.opencode/command/astro-refresh-data.md",
            [
                (
                    "triggers",
                    "document:.opencode/agent/astro-data-engineer.md",
                    "this command's frontmatter pins agent: astro-data-engineer",
                ),
                (
                    "triggers",
                    "file:.opencode/loops/refresh-data.sh",
                    "this command's instructions execute .opencode/loops/refresh-data.sh",
                ),
                (
                    "documents",
                    "document:CONTEXT.md",
                    "this command's instructions say to read CONTEXT.md",
                ),
                (
                    "documents",
                    "document:.opencode/skill/astro-science.md",
                    "this command's instructions say to read the astro-science skill",
                ),
            ],
        ),
        (
            "document:.opencode/command/astro-notebook-health.md",
            [
                (
                    "triggers",
                    "document:.opencode/agent/astro-validator.md",
                    "this command's frontmatter pins agent: astro-validator",
                ),
                (
                    "triggers",
                    "file:.opencode/loops/notebook-health.sh",
                    "this command's instructions execute .opencode/loops/notebook-health.sh",
                ),
            ],
        ),
        (
            "document:.opencode/command/astro-research.md",
            [
                (
                    "triggers",
                    "document:.opencode/agent/astro-theoretician.md",
                    "AUTOMATION.md maps /astro-research to the astro-theoretician agent",
                ),
                (
                    "documents",
                    "document:CONTEXT.md",
                    "this command's instructions say to read CONTEXT.md",
                ),
            ],
        ),
        (
            "document:.opencode/command/astro-graphs.md",
            [
                (
                    "related",
                    "document:.opencode/skill/astro-graphs.md",
                    "this command's step 1 reads the astro-graphs skill",
                ),
            ],
        ),
    ]
    for cmd_id, rules in command_rules:
        for etype, tgt, why in rules:
            if cmd_id in node_by_id and tgt in node_by_id:
                add_candidate(cands, cmd_id, tgt, etype, why, ("cmd",))

    # --- (a) agents reference the artifacts they work on -------------------
    agent_rules = [
        (
            "document:.opencode/agent/astro-data-engineer.md",
            [
                (
                    "documents",
                    "document:CONTEXT.md",
                    "the agent's workflow step 1 says 'Read CONTEXT.md'",
                ),
                (
                    "documents",
                    "document:.opencode/skill/astro-science.md",
                    "the agent's workflow step 1 names the project skill astro-science",
                ),
                (
                    "documents",
                    "document:.opencode/skill/astro-graphs.md",
                    "the agent's gates re-run the knowledge graphs via the astro-graphs skill",
                ),
            ],
        ),
        (
            "document:.opencode/agent/astro-validator.md",
            [
                (
                    "related",
                    "file:.opencode/loops/notebook-health.sh",
                    "the agent names .opencode/loops/notebook-health.sh as the notebook suite runner",
                ),
                (
                    "related",
                    "file:scripts/verify_formulas.py",
                    "the agent's step 4 runs targeted checks like verify_formulas.py",
                ),
            ],
        ),
        (
            "document:.opencode/agent/astro-theoretician.md",
            [
                (
                    "related",
                    "file:scripts/verify_formulas.py",
                    "the agent's step 4 sanity-checks formulas via verify_formulas.py",
                ),
                (
                    "documents",
                    "document:premium/theory_black_holes.md",
                    "AUTOMATION.md assigns theory-doc upkeep to this agent; theory_black_holes.md is the representative doc",
                ),
            ],
        ),
        (
            "document:.opencode/agent/astro-reviewer.md",
            [
                (
                    "documents",
                    "document:reports/summary.md",
                    "the reviewer audits reports for soundness/reproducibility; summary.md is the report hub",
                ),
            ],
        ),
    ]
    for agent_id, rules in agent_rules:
        for etype, tgt, why in rules:
            if agent_id in node_by_id and tgt in node_by_id:
                add_candidate(cands, agent_id, tgt, etype, why, ())

    # --- (a) skills (the project map) document every downloader/generator ---
    skill_science = "document:.opencode/skill/astro-science.md"
    for tgt, why in [
        ("file:scripts/download_sxs.py", "skill download group names download_sxs.py"),
        ("file:scripts/download_eht.py", "skill download group names download_eht.py"),
        (
            "file:scripts/download_planck.py",
            "skill download group names download_planck.py",
        ),
        (
            "file:scripts/download_sdss.py",
            "skill download group names download_sdss.py",
        ),
        (
            "file:scripts/download_gaia_dr3.py",
            "skill download group names download_gaia_dr3.py",
        ),
        ("file:scripts/download_gwb.py", "skill download group names download_gwb.py"),
        (
            "file:scripts/download_strain_marquee.py",
            "skill download group names download_strain_marquee.py",
        ),
        (
            "file:scripts/download_xray_binaries.py",
            "skill download group names download_xray_binaries.py",
        ),
        (
            "file:scripts/download_gwosc_o4.py",
            "skill download group names download_gwosc_o4.py",
        ),
        (
            "file:scripts/create_animations.py",
            "skill generators group names create_animations.py",
        ),
        (
            "file:scripts/make_notebook.py",
            "skill generators group names make_notebook*.py; make_notebook.py is the first generator",
        ),
        (
            "document:research/projects/black-holes/README.md",
            "skill project table names the black-holes project",
        ),
        (
            "document:research/projects/exotic-compact-objects/README.md",
            "skill project table names the flagship project",
        ),
    ]:
        if skill_science in node_by_id and tgt in node_by_id:
            add_candidate(cands, skill_science, tgt, "documents", why, ())

    skill_graphs = "document:.opencode/skill/astro-graphs.md"
    for tgt, etype, why in [
        (
            "config:.ua/config.json",
            "documents",
            "skill configuration section names .ua/config.json (outputLanguage en)",
        ),
        (
            "document:docs/GRAPHS.md",
            "related",
            "the skill and GRAPHS.md document the same three graph commands",
        ),
    ]:
        if skill_graphs in node_by_id and tgt in node_by_id:
            add_candidate(cands, skill_graphs, tgt, etype, why, ())

    # --- (a) refresh loop -> the files its body executes --------------------
    refresh = "file:.opencode/loops/refresh-data.sh"
    for tgt, why in [
        (
            "file:scripts/download_heasarc.py",
            "refresh-data.sh 'heasarc-download' step runs scripts/download_heasarc.py",
        ),
        (
            "file:scripts/download_blackcat.py",
            "refresh-data.sh 'blackcat-download' step runs scripts/download_blackcat.py",
        ),
        (
            "file:scripts/process_blackcat.py",
            "refresh-data.sh 'blackcat-process' step runs scripts/process_blackcat.py",
        ),
        (
            "file:scripts/add_bh_derived_quantities.py",
            "refresh-data.sh 'bh-derived' step runs scripts/add_bh_derived_quantities.py",
        ),
        (
            "file:scripts/build_theoretical_data.py",
            "refresh-data.sh 'theoretical-data' step runs scripts/build_theoretical_data.py",
        ),
        (
            "file:scripts/build_gwtc_remnant_dashboard.py",
            "refresh-data.sh 'gwtc-dashboard' step runs scripts/build_gwtc_remnant_dashboard.py",
        ),
        (
            "file:scripts/build_agn_reverberation_dashboard.py",
            "refresh-data.sh 'agn-dashboard' step runs scripts/build_agn_reverberation_dashboard.py",
        ),
        (
            "file:scripts/build_blackcat_dashboard.py",
            "refresh-data.sh 'blackcat-dashboard' step runs scripts/build_blackcat_dashboard.py",
        ),
    ]:
        if refresh in node_by_id and tgt in node_by_id:
            add_candidate(cands, refresh, tgt, "depends_on", why, ("loop-touch",))

    # --- (a) notebook-health loop -> every notebook suite member -------------
    nbhealth = "file:.opencode/loops/notebook-health.sh"
    # derived from the node set, not hardcoded: every notebook under the two
    # project notebook directories the loop enumerates
    nb_re = re.compile(
        r"^file:(notebooks/\d{2}_[a-z0-9_]+\.ipynb"
        r"|research/projects/black-holes-wormholes/notebooks/[a-z0-9_]+\.ipynb)$"
    )
    for tgt in sorted(
        n["id"] for n in kg["nodes"] if n["type"] == "file" and nb_re.match(n["id"])
    ):
        add_candidate(
            cands,
            nbhealth,
            tgt,
            "depends_on",
            "notebook-health.sh enumerates and executes every notebook under the two project notebook directories.",
            ("loop-touch",),
        )

    # --- (a) research-loop -> docs/wiki/derivation machinery ------------------
    rloop = "file:.opencode/loops/research-loop.sh"
    for tgt, etype, why in [
        (
            "file:models/derivations.py",
            "related",
            "domain flow 'research-loop' step derive-symbolically assigns models/derivations.py",
        ),
        (
            "file:scripts/verify_formulas.py",
            "related",
            "domain flow 'research-loop' step validate-formulas assigns scripts/verify_formulas.py",
        ),
        (
            "document:premium/theory_black_holes.md",
            "related",
            "loop's final step updates premium/theory_*.md (representative doc from the domain-graph flow)",
        ),
        (
            "document:research/wiki/index.md",
            "related",
            "loop's final step updates research/wiki/ (index is the wiki root)",
        ),
        (
            "document:CONTEXT.md",
            "documents",
            "loop output says 'Read CONTEXT.md and the astro-science skill'",
        ),
        (
            "document:.opencode/skill/astro-science.md",
            "documents",
            "loop output names the astro-science skill",
        ),
    ]:
        if rloop in node_by_id and tgt in node_by_id:
            add_candidate(cands, rloop, tgt, etype, why, ())

    # --- (a) CONTEXT.md anchors ------------------------------------------------
    ctx = "document:CONTEXT.md"
    for tgt, why in [
        (
            "file:research/projects/black-holes-wormholes/notebooks/01_black_hole_fundamentals.ipynb",
            "CONTEXT.md section 4.3 names 01_black_hole_fundamentals.ipynb",
        ),
        (
            "file:research/projects/black-holes-wormholes/notebooks/02_geodesics_orbits.ipynb",
            "CONTEXT.md section 4.3 names 02_geodesics_orbits.ipynb",
        ),
        (
            "document:.opencode/skill/astro-science.md",
            "CONTEXT.md header: use the project skill astro-science for path-level detail",
        ),
        (
            "file:start-research.sh",
            "CONTEXT.md directory map lists start-research.sh at the root",
        ),
    ]:
        if ctx in node_by_id and tgt in node_by_id:
            add_candidate(cands, ctx, tgt, "documents", why, ())

    # --- (a) research/projects hub ---------------------------------------------
    projects_hub = "document:research/projects/README.md"
    for tgt, why in [
        (
            "document:research/projects/exotic-compact-objects/README.md",
            "project README lives directly under the research/projects/ folder described by that README",
        ),
        (
            "document:research/projects/black-holes/README.md",
            "project README lives directly under the research/projects/ folder described by that README",
        ),
    ]:
        if projects_hub in node_by_id and tgt in node_by_id:
            add_candidate(cands, projects_hub, tgt, "related", why, ())

    # --- (a) ECO README documents the project's machinery -----------------------
    eco_readme = "document:research/projects/exotic-compact-objects/README.md"
    for tgt, why in [
        (
            "file:models/equations.py",
            "README structure tree names models/equations.py as the core equations module",
        ),
        (
            "file:scripts/make_notebook2.py",
            "README setup block runs scripts/make_notebook2.py",
        ),
        (
            "file:scripts/build_theoretical_data.py",
            "README setup block runs scripts/build_theoretical_data.py",
        ),
        (
            "file:scripts/download_gwosc.py",
            "README data section names scripts/download_gwosc.py",
        ),
        (
            "file:scripts/download_heasarc.py",
            "README data section names scripts/download_heasarc.py",
        ),
        (
            "file:scripts/add_bh_derived_quantities.py",
            "README: 'Recompute with scripts/add_bh_derived_quantities.py'",
        ),
    ]:
        if eco_readme in node_by_id and tgt in node_by_id:
            add_candidate(cands, eco_readme, tgt, "documents", why, ())

    # --- (a) top-level docs cross-reference each other --------------------------
    doc_cross = [
        (
            "document:FINAL_REPORT.md",
            "document:SETUP_GUIDE.md",
            "FINAL_REPORT doc list item 2 names SETUP_GUIDE.md",
        ),
        (
            "document:FINAL_REPORT.md",
            "document:TOOLS_LIST.md",
            "FINAL_REPORT doc list item 3 names TOOLS_LIST.md",
        ),
        (
            "document:FINAL_REPORT.md",
            "document:NEW_TOOLS_SUMMARY.md",
            "FINAL_REPORT doc list item 4 names NEW_TOOLS_SUMMARY.md",
        ),
        (
            "document:FINAL_REPORT.md",
            "document:INSTALLATION_SUMMARY.md",
            "FINAL_REPORT doc list item 5 names INSTALLATION_SUMMARY.md",
        ),
        (
            "document:FINAL_REPORT.md",
            "document:requirements.txt",
            "FINAL_REPORT doc list item 6: requirements.txt - Python dependencies",
        ),
        (
            "document:FINAL_REPORT.md",
            "file:start.sh",
            "FINAL_REPORT doc list item 7: start.sh - start script",
        ),
        (
            "document:INSTALLATION_SUMMARY.md",
            "document:SETUP_GUIDE.md",
            "INSTALLATION_SUMMARY checks off SETUP_GUIDE.md",
        ),
        (
            "document:INSTALLATION_SUMMARY.md",
            "document:TOOLS_LIST.md",
            "INSTALLATION_SUMMARY checks off TOOLS_LIST.md",
        ),
        (
            "document:INSTALLATION_SUMMARY.md",
            "document:requirements.txt",
            "INSTALLATION_SUMMARY checks off requirements.txt",
        ),
        (
            "document:INSTALLATION_SUMMARY.md",
            "file:start.sh",
            "INSTALLATION_SUMMARY checks off start.sh",
        ),
    ]
    for s, t, why in doc_cross:
        if s in node_by_id and t in node_by_id:
            add_candidate(cands, s, t, "documents", why, ())

    # --- (a/b) data scripts -> the sample artifacts they produce ----------------
    for s, t, why in [
        (
            "file:data/download_direct_data.py",
            "file:catalogs/galaxy_catalog.fits",
            "the script's output list writes catalogs/galaxy_catalog.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:catalogs/star_catalog.fits",
            "the script's output list writes catalogs/star_catalog.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:cmb/cmb_map.fits",
            "the script's output list writes cmb/cmb_map.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:cmb/cmb_power_spectrum.fits",
            "the script's output list writes cmb/cmb_power_spectrum.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:fits/synthetic_galaxy.fits",
            "the script's output list writes fits/synthetic_galaxy.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:simulations/gw_strain.fits",
            "the script's output list writes simulations/gw_strain.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:simulations/nbody_snapshot.fits",
            "the script's output list writes simulations/nbody_snapshot.fits",
        ),
        (
            "file:data/download_direct_data.py",
            "file:simulations/xray_spectrum.fits",
            "the script's output list writes simulations/xray_spectrum.fits",
        ),
        (
            "file:data/download_sample_data.py",
            "file:catalogs/sample_galaxies.fits",
            "the script's output list writes catalogs/sample_galaxies.fits",
        ),
        (
            "file:data/download_sample_data.py",
            "file:cmb/synthetic_cmb_map.fits",
            "the script's output list writes cmb/synthetic_cmb_map.fits",
        ),
        (
            "file:notebooks/19_gw_strain_analysis.ipynb",
            "file:simulations/gw_strain.fits",
            "notebook code reads simulations/gw_strain.fits for strain analysis",
        ),
    ]:
        if s in node_by_id and t in node_by_id:
            etype = "writes_to" if s.startswith("file:data/") else "related"
            add_candidate(cands, s, t, etype, why, ("data-gen",))

    # --- (c) wiki articles <-> code machinery (explicit text evidence only) -----
    for s, t, why in [
        (
            "document:research/wiki/Gravitational-Wave Catalogs.md",
            "file:scripts/update_gwosc_gwtc5.py",
            "the article's '391-event snapshot' (line 13) is the deduplicated GWTC-1..5 snapshot this script builds",
        ),
        (
            "document:research/wiki/Black Hole Accretion.md",
            "file:scripts/process_blackcat.py",
            "article line 21 discusses the BlackCAT dynamical BH sample this script processes",
        ),
        (
            "document:research/wiki/Black Hole Accretion.md",
            "file:scripts/build_agn_reverberation_dashboard.py",
            "article line 24 discusses AGN reverberation mapping; this script builds the AGN mass dashboard",
        ),
    ]:
        if s in node_by_id and t in node_by_id:
            add_candidate(cands, s, t, "related", why, ("wiki-code",))

    # --- (a) wiki index lists every article (README-of-the-wiki) ----------------
    wiki_index = "document:research/wiki/index.md"
    index_text = (
        readable_source(resolve_node_fs(node_by_id.get(wiki_index, {})))
        if wiki_index in node_by_id
        else None
    )
    if index_text:
        for n in kg["nodes"]:
            if (
                n["type"] != "document"
                or not n["id"].startswith("document:research/wiki/")
                or n["id"] == wiki_index
            ):
                continue
            art = n["name"][:-3] if n["name"].endswith(".md") else n["name"]
            if f"[[{art}]]" in index_text:
                add_candidate(
                    cands,
                    wiki_index,
                    n["id"],
                    "documents",
                    f"index.md lists this article as a wiki entry ('[[{art}]]').",
                    ("wiki-index",),
                )

    # --- (b) domain-graph flow chains --------------------------------------------
    flow_step_primary = {}
    flow_ids = []
    for e in dg["edges"]:
        if e["type"] == "flow_step":
            flow_step_primary[e["target"]] = e["source"]
            if e["source"] not in flow_ids:
                flow_ids.append(e["source"])

    def path_to_nodeid(fp):
        """Map a domain-graph step filePath to a graph node id.

        Steps carry root-relative paths or the full nested subdomain path
        (research/projects/exotic-compact-objects/...); the merged graph stores
        subdomain nodes relative to the subdomain root.  Only the known
        subdomain prefix is ever stripped, so the mapping never guesses.
        """
        fp = fp.strip()
        for pref in ("file:", "document:"):
            if f"{pref}{fp}" in node_by_id:
                return f"{pref}{fp}"
        if fp.startswith(ECO_SUBDOMAIN + "/"):
            stripped = fp[len(ECO_SUBDOMAIN) + 1 :]
            for pref in ("file:", "document:"):
                if f"{pref}{stripped}" in node_by_id:
                    return f"{pref}{stripped}"
        return None

    def summary_refs(summary):
        """Node ids matched by unambiguous fragments inside a step summary."""
        found = []
        for frag in sorted(fragment_index.unambiguous):
            if frag.count("/") > 3:
                continue
            node = fragment_index.unambiguous[frag]
            if re.search(rf"(?<![A-Za-z0-9_./]){re.escape(frag)}\b", summary):
                if node["id"] not in found:
                    found.append(node["id"])
        return found

    flow_nodes = {fid: [] for fid in flow_ids}
    for nd in dg["nodes"]:
        if nd["type"] != "step":
            continue
        flow_id = flow_step_primary.get(nd["id"])
        if flow_id is None:
            continue
        entries = []
        pnode = path_to_nodeid(nd.get("filePath", "")) if nd.get("filePath") else None
        if pnode:
            entries.append(pnode)
        entries.extend(x for x in summary_refs(nd.get("summary", "")) if x != pnode)
        flow_nodes[flow_id].extend(dict.fromkeys(entries))

    # seed each flow with its entryPoint node (skip if a step already carries it)
    for nd in dg["nodes"]:
        if nd["type"] == "flow":
            ep = (nd.get("domainMeta") or {}).get("entryPoint")
            if ep:
                nid = path_to_nodeid(ep)
                seq = flow_nodes.get(nd["id"])
                if nid and nid not in seq:
                    flow_nodes.setdefault(nd["id"], []).insert(0, nid)

    for flow_id, seq in flow_nodes.items():
        ordered = list(dict.fromkeys(x for x in seq if x in node_by_id))
        flowname = flow_id.split(":", 1)[1]
        for a, b in zip(ordered, ordered[1:]):
            add_candidate(
                cands,
                a,
                b,
                "related",
                f"domain flow '{flowname}' chains {node_raw_path(a)} through {node_raw_path(b)}.",
                ("domain-flow",),
            )

    return cands


# ----------------------------------------------------------------------------
# filtering + application
# ----------------------------------------------------------------------------


def structural_value(c, iso_before, comp_of):
    """True if the edge rescues an isolated node or crosses components."""
    s_iso, t_iso = c["source"] in iso_before, c["target"] in iso_before
    crosses = comp_of.get(c["source"]) != comp_of.get(c["target"])
    return s_iso or t_iso or crosses


GROUP_CAPS = {
    "loop-doc": 4,  # AUTOMATION.md documents all four loop scripts
    "loop-touch": 40,  # the loops literally execute these files
    "cmd": 12,  # command manifests (frontmatter/instructions)
    "domain-flow": 24,  # documented flow pipelines
    "data-gen": 12,  # literal write/read statements
    "wiki-index": 16,  # the wiki index literally lists 16 articles
    "wiki-code": 3,  # explicit article-text evidence only
}


def main(argv):
    dry = "--dry-run" in argv
    kg = json.loads(KG_PATH.read_text())
    dg = json.loads(DG_PATH.read_text())

    # full snapshot for the no-collateral-damage validation
    snap_nodes, snap_layers, snap_tour = (
        copy.deepcopy(kg["nodes"]),
        copy.deepcopy(kg["layers"]),
        copy.deepcopy(kg["tour"]),
    )
    before = graph_stats(kg["nodes"], kg["edges"])
    iso_before = set(isolated_nodes({n["id"] for n in kg["nodes"]}, kg["edges"]))
    comps_before = union_find_components({n["id"] for n in kg["nodes"]}, kg["edges"])
    comp_of = {i: r for r, members in comps_before.items() for i in members}

    node_by_id = {n["id"]: n for n in kg["nodes"]}
    existing_triples = {(e["source"], e["target"], e["type"]) for e in kg["edges"]}
    existing_pairs = {(e["target"], e["source"]) for e in kg["edges"]} | {
        (e["source"], e["target"]) for e in kg["edges"]
    }
    fragment_index = FragmentIndex(kg["nodes"])
    candidates = generate_candidates(
        kg, dg, fragment_index, node_by_id, comps_before, comp_of, iso_before
    )

    group_used = Counter()
    added, skipped = [], []
    for c in candidates:
        triple = (c["source"], c["target"], c["type"])
        D = node_by_id
        if c["source"] not in D or c["target"] not in D:
            skipped.append((c, "dangling"))
        elif c["source"] == c["target"]:
            skipped.append((c, "self-loop"))
        elif triple in existing_triples:
            skipped.append((c, "edge-exists"))
        elif (c["source"], c["target"]) in existing_pairs:
            skipped.append((c, "pair-connected-already"))
        elif not structural_value(c, iso_before, comp_of):
            # intra-component edges only survive if a capped declared seed group claims them
            over_cap = (
                all(group_used[g] >= GROUP_CAPS.get(g, 0) for g in c["_groups"])
                or not c["_groups"]
            )
            if over_cap:
                skipped.append((c, "redundant-in-component"))
            else:
                added.append(c)
                existing_triples.add(triple)
                existing_pairs.add((c["source"], c["target"]))
                existing_pairs.add((c["target"], c["source"]))
                for g in set(c["_groups"]):
                    group_used[g] += 1
        else:
            added.append(c)
            existing_triples.add(triple)
            existing_pairs.add((c["source"], c["target"]))
            existing_pairs.add((c["target"], c["source"]))
            for g in set(c["_groups"]):
                group_used[g] += 1

    final_added = sorted(
        (
            {k: e[k] for k in ("source", "target", "type", "description", "weight")}
            for e in added
        ),
        key=lambda e: (e["type"], e["source"], e["target"]),
    )

    print(
        f"candidates generated: {len(candidates)} | kept: {len(final_added)} | skipped: {len(skipped)}"
    )
    print("skip reasons:", dict(Counter(r for _, r in skipped)))
    if dry:
        for e in final_added:
            print(f"  + {e['type']:<10s} {e['source']} -> {e['target']}")
        return 0
    if not final_added:
        print("nothing to add (graph already cohesive — idempotent no-op)")
        return 0

    kg["edges"].extend(final_added)
    KG_PATH.write_text(json.dumps(kg, indent=2) + "\n")
    OUT_ADDED.write_text(json.dumps(final_added, indent=2) + "\n")

    # --- validation pass ------------------------------------------------------
    kg2 = json.loads(KG_PATH.read_text())
    after = graph_stats(kg2["nodes"], kg2["edges"])
    assert [n["id"] for n in kg2["nodes"]] == [n["id"] for n in snap_nodes], (
        "node set changed!"
    )
    assert kg2["layers"] == snap_layers, "layers changed!"
    assert kg2["tour"] == snap_tour, "tour changed!"

    print("\n=== VALIDATION ===")
    print(
        f"nodes:        {before['nodes']} -> {after['nodes']} (must be equal: {before['nodes'] == after['nodes']})"
    )
    print(
        f"edges:        {before['edges']} -> {after['edges']} (delta = {after['edges'] - before['edges']})"
    )
    print(f"components:   {before['components']} -> {after['components']}")
    print(f"isolated:     {before['isolated']} -> {after['isolated']}")
    print(
        f"dangling:     before={len(before['dangling'])} after={len(after['dangling'])} (must be 0)"
    )
    print(
        f"dup edges:    before={len(before['dupes'])} after={len(after['dupes'])} (must be 0)"
    )
    assert not after["dangling"] and not after["dupes"], "validation failed"

    print("\nedge counts by type (before -> after):")
    all_types = sorted(
        set(before["by_type"]) | set(after["by_type"]) | set(DEFAULT_WEIGHT)
    )
    for t in all_types:
        b, a = before["by_type"].get(t, 0), after["by_type"].get(t, 0)
        if b or a:
            print(f"  {t:<12s} {b:>4d} -> {a:>4d} (delta {a - b:+d})")
    print(f"\nadded edges saved to {OUT_ADDED}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
