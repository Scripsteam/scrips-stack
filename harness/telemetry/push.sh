#!/bin/bash
# Ships this machine's telemetry to the central sink (scrips-telemetry/telemetry/<dev>/).
# Run by session-end or a daily cron. Per-dev file => no cross-dev merge conflicts.
# UNION-MERGE (never overwrite): the sink file = local events ∪ whatever is already
# in the sink, deduped by exact line. This is clobber-proof — a local file that is
# empty, partial, or behind the sink (e.g. backfilled history that never touched this
# machine) can never erase events that are already centralised. Fails loud.
set -uo pipefail
SINK="$HOME/scrips-repos/scrips-telemetry"
SRC="$HOME/.claude/telemetry/events.jsonl"
# Refresh the budget snapshot (tokens/$ harvested from local transcripts) before
# shipping, so it travels with this push. Best-effort — never blocks the push.
BT="$HOME/.claude/telemetry/budget-track.py"
[ -f "$BT" ] && python3 "$BT" >/dev/null 2>&1 || true
[ -f "$SRC" ] || { echo "no telemetry yet"; exit 0; }
[ -d "$SINK/.git" ] || { echo "sink repo missing at $SINK"; exit 1; }
# EFFECTIVE email (local > includeIf > global), NOT --global — computed in the
# session cwd (a scrips repo) BEFORE we cd into the sink, so includeIf applies.
DEV=$(git config user.email | sed 's/[^a-zA-Z0-9]/_/g'); DEV=${DEV:-unknown}
DST_DIR="$SINK/telemetry/$DEV"; DST="$DST_DIR/events.jsonl"
mkdir -p "$DST_DIR"
cd "$SINK" && git pull -q --no-rebase origin main 2>/dev/null || true
# union-merge local + existing sink, drop blank lines, dedupe preserving first-seen order
MERGED="$(mktemp)"
cat "$SRC" "$DST" 2>/dev/null | awk 'NF && !seen[$0]++' > "$MERGED"
# never write fewer events than the sink already has (hard clobber guard)
OLD=$( [ -f "$DST" ] && grep -c . "$DST" || echo 0 ); NEW=$(grep -c . "$MERGED")
if [ "$NEW" -lt "$OLD" ]; then echo "ABORT: merge ($NEW) < sink ($OLD) — refusing to shrink"; rm -f "$MERGED"; exit 1; fi
mv "$MERGED" "$DST"
git add "telemetry/$DEV/events.jsonl"
git diff --cached --quiet || { git commit -q -m "telemetry: $DEV events $(date +%Y-%m-%d)"; git push -q origin main || echo "WARN push failed"; }
echo "pushed telemetry for $DEV ($NEW events)"
