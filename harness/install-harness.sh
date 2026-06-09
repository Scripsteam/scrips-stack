#!/bin/bash
# scrips-stack harness installer — gives a dev the same engineering guardrails
# the team runs: the DS-color gate, the destructive-bash gate, and the FHIR
# architecture advisor. Idempotent. Run from anywhere.
#
#   bash harness/install-harness.sh
#
# What it does:
#  - copies the portable hooks into ~/.claude/hooks/
#  - copies the fhir-architecture-advisor agent into ~/.claude/agents/
#  - merges the hook wiring into ~/.claude/settings.json (creates a backup first;
#    never clobbers existing hooks — appends only the ones not already present)
#
# These hooks are machine-agnostic (they resolve paths via $HOME). The DS-color
# gate reads its denylist live from ~/scrips-repos/scrips-signal-ds/tokens/
# design-tokens.ts — clone that repo for full enforcement (it degrades gracefully
# to a built-in fallback list if absent).
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOKS_DST="$HOME/.claude/hooks"
AGENTS_DST="$HOME/.claude/agents"
SETTINGS="$HOME/.claude/settings.json"

mkdir -p "$HOOKS_DST" "$AGENTS_DST"
cp "$SCRIPT_DIR"/hooks/*.py "$HOOKS_DST"/
cp "$SCRIPT_DIR"/agents/*.md "$AGENTS_DST"/
echo "✓ hooks → $HOOKS_DST"
echo "✓ agents → $AGENTS_DST"

# Merge hook wiring into settings.json without clobbering existing hooks.
python3 - "$SETTINGS" "$HOOKS_DST" <<'PY'
import json, os, sys, time
settings_path, hooks_dir = sys.argv[1], sys.argv[2]
settings = {}
if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
    bak = f"{settings_path}.bak.{int(time.time())}"
    with open(bak, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"✓ backed up settings → {bak}")

hooks = settings.setdefault("hooks", {})
# event -> list of hook command basenames to ensure present
WANT = {
    "PreToolUse": ["bash-destructive-gate.py", "ds-color-gate.py"],
    "UserPromptSubmit": ["fhir-architecture-trigger.py"],
}
added = 0
for event, scripts in WANT.items():
    matchers = hooks.setdefault(event, [])
    present = json.dumps(matchers)
    for s in scripts:
        if s in present:
            continue
        matchers.append({"hooks": [{"type": "command",
            "command": f"python3 {hooks_dir}/{s}"}]})
        added += 1
        print(f"  + {event}: {s}")
with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
print(f"✓ settings updated ({added} hook(s) added; existing hooks untouched)")
PY

echo ""
echo "Done. Restart Claude Code to load the hooks."
echo "Installed gates: ds-color-gate (blocks rejected DS hex) · bash-destructive-gate · fhir-architecture advisor."
