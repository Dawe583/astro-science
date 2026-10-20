#!/usr/bin/env bash
# =============================================================================
# astro-science — research loop
# question -> hypothesis -> derivation -> figure -> report -> theory doc
#
# This loop is agent-driven. The script sets up a research work directory and a
# hypothesis template, then hands off to the astro-theoretician agent.
# =============================================================================
set -uo pipefail

ROOT="/home/dawe/Projects/astro-science"
TOPIC="${1:-}"
if [ -z "$TOPIC" ]; then
  echo "Usage: research-loop.sh \"<research question / topic>\""
  echo
  echo "Example:"
  echo "  .opencode/loops/research-loop.sh \"ISCO radius vs spin for Kerr black holes\""
  exit 2
fi

SLUG="$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | cut -c1-60 | sed 's/^-//;s/-$//')"
WORK="$ROOT/research/work/$(date +%Y%m%d)-$SLUG"
mkdir -p "$WORK"

cat > "$WORK/hypothesis.md" <<EOF
# Research topic

**Question:** $TOPIC

## Hypothesis

<!-- one sentence -->

## Sources

<!-- data source, cadence, provenance -->

## Method

<!-- equations, code path, assumptions -->

## Results

<!-- with units, uncertainties, caveats -->

## Reproducibility

<!-- exact commands, versions, output paths -->
EOF

echo "[research-loop] work dir: $WORK"
echo
echo "Next steps (agent-driven):"
echo "  1. Read CONTEXT.md and the astro-science skill."
echo "  2. Open the astro-theoretician agent and fill hypothesis.md."
echo "  3. Derive, verify (units + limiting case + numeric check), figure, report."
echo "  4. Update premium/theory_*.md and research/wiki/."
echo
echo "  /astro-research   (runs the theoretician workflow interactively)"
