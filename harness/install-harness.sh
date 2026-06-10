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
TELEM_DST="$HOME/.claude/telemetry"
SETTINGS="$HOME/.claude/settings.json"

mkdir -p "$HOOKS_DST" "$AGENTS_DST" "$TELEM_DST"
cp "$SCRIPT_DIR"/hooks/*.py "$HOOKS_DST"/
cp "$SCRIPT_DIR"/agents/*.md "$AGENTS_DST"/
# Team observability instruments: the talk (agent dispatches) + estimate-vs-actual
# + the push to the central sink. Machine-agnostic ($HOME / git email keyed).
cp "$SCRIPT_DIR"/telemetry/*.py "$TELEM_DST"/
cp "$SCRIPT_DIR"/telemetry/push.sh "$TELEM_DST"/ && chmod +x "$TELEM_DST"/push.sh
echo "✓ hooks → $HOOKS_DST"
echo "✓ agents → $AGENTS_DST"
echo "✓ telemetry → $TELEM_DST"

# Merge hook wiring into settings.json without clobbering existing hooks.
python3 - "$SETTINGS" "$HOOKS_DST" "$TELEM_DST" <<'PY'
import json, os, sys, time
settings_path, hooks_dir, telem_dir = sys.argv[1], sys.argv[2], sys.argv[3]
settings = {}
if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
    bak = f"{settings_path}.bak.{int(time.time())}"
    with open(bak, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"✓ backed up settings → {bak}")

hooks = settings.setdefault("hooks", {})
added = 0

# 1) Guardrail gates — matcher-less (the Python self-filters on tool name).
WANT = {
    "PreToolUse": ["bash-destructive-gate.py", "ds-color-gate.py"],
    "UserPromptSubmit": ["fhir-architecture-trigger.py"],
}
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

# 2) Telemetry instruments — matcher-scoped so they fire only on the right tools.
#    agent-track logs every PreToolUse it sees, so it MUST be scoped to Agent.
#    task-gate self-filters but we scope it too to avoid firing on every call.
#    push.sh ships this machine's events to the sink on session end.
def ensure(event, matcher, cmd, basename):
    """Idempotent + migrating: purge ANY prior hook referencing this instrument
    by basename (e.g. an older differently-pathed copy), then add the canonical
    one exactly once. Prevents the double-count that two Agent hooks would cause."""
    global added
    arr = hooks.setdefault(event, [])
    before = len(arr)
    arr[:] = [e for e in arr
              if not any(basename in hk.get("command", "") for hk in e.get("hooks", []))]
    purged = before - len(arr)
    if purged:
        print(f"  ~ {event}: purged {purged} stale '{basename}' hook(s)")
    entry = {"hooks": [{"type": "command", "command": cmd}]}
    if matcher is not None:
        entry["matcher"] = matcher
    arr.append(entry)
    added += 1
    print(f"  + {event}{'/'+matcher if matcher else ''}: {basename}")

ensure("PreToolUse", "Agent", f"python3 {telem_dir}/agent-track.py", "agent-track.py")
ensure("PreToolUse", "TaskCreate|TaskUpdate", f"python3 {telem_dir}/task-gate.py", "task-gate.py")
ensure("SessionEnd", None, f"bash {telem_dir}/push.sh", "push.sh")

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
print(f"✓ settings updated ({added} hook(s) added; existing hooks untouched)")
PY

echo ""
echo "Done. Restart Claude Code to load the hooks."
echo "Installed gates: ds-color-gate (blocks rejected DS hex) · bash-destructive-gate · fhir-architecture advisor."
echo "Installed telemetry: the-talk (agent dispatches) · estimate-vs-actual · session-end push to the sink."
echo "Budget (token/\$ via OTEL) is opt-in — see scrips-telemetry/otel/README once a collector endpoint exists."
