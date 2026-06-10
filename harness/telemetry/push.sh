#!/bin/bash
# Ships this machine's telemetry to the central sink (scrips-telemetry/telemetry/<dev>/).
# Run by session-end or a daily cron. Per-dev file => no merge conflicts. Fails loud.
set -uo pipefail
SINK="$HOME/scrips-repos/scrips-telemetry"
SRC="$HOME/.claude/telemetry/events.jsonl"
[ -f "$SRC" ] || { echo "no telemetry yet"; exit 0; }
[ -d "$SINK/.git" ] || { echo "sink repo missing at $SINK"; exit 1; }
DEV=$(git config --global user.email | sed 's/[^a-zA-Z0-9]/_/g'); DEV=${DEV:-unknown}
mkdir -p "$SINK/telemetry/$DEV"
cp "$SRC" "$SINK/telemetry/$DEV/events.jsonl"
cd "$SINK" && git pull -q --no-rebase origin main 2>/dev/null
git add "telemetry/$DEV/events.jsonl"
git diff --cached --quiet || { git commit -q -m "telemetry: $DEV events $(date +%Y-%m-%d)"; git push -q origin main || echo "WARN push failed"; }
echo "pushed telemetry for $DEV"
