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
#
# The shell owns the path (read via stdin, write via stdout) so native Windows
# Python never sees an MSYS /c/Users/... path — the bug class PR #7 killed in
# team-setup.sh, which silently dropped the guardrails on every Windows machine
# while reporting ✓. The read also decodes utf-8-sig: PowerShell's Out-File
# writes a UTF-8 BOM that otherwise makes json.load choke at char 0, leaving the
# hooks unregistered even once the path is fixed. After the write we re-read and
# assert every wanted hook is present — it can no longer claim success it didn't
# achieve. Registers BOTH the guardrail gates AND the telemetry instruments the
# Windows-safe way, so neither silently drops on Windows.
_merge_hooks() {
  HOOKS_DIR="$HOOKS_DST" TELEM_DIR="$TELEM_DST" python3 -c '
import json, os, sys
raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()   # tolerate a PowerShell BOM
settings = json.loads(raw) if raw else {}
hooks_dir = os.environ["HOOKS_DIR"]
telem_dir = os.environ["TELEM_DIR"]
hooks = settings.setdefault("hooks", {})

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

# 2) Telemetry instruments — matcher-scoped so they fire only on the right tools.
#    agent-track logs every PreToolUse it sees, so it MUST be scoped to Agent.
#    task-gate self-filters but we scope it too to avoid firing on every call.
#    push.sh ships this machine events to the sink on session end.
def ensure(event, matcher, cmd, basename):
    """Idempotent + migrating: purge ANY prior hook referencing this instrument
    by basename (e.g. an older differently-pathed copy), then add the canonical
    one exactly once. Prevents the double-count that two Agent hooks would cause."""
    arr = hooks.setdefault(event, [])
    arr[:] = [e for e in arr
              if not any(basename in hk.get("command", "") for hk in e.get("hooks", []))]
    entry = {"hooks": [{"type": "command", "command": cmd}]}
    if matcher is not None:
        entry["matcher"] = matcher
    arr.append(entry)

ensure("PreToolUse", "Agent", f"python3 {telem_dir}/agent-track.py", "agent-track.py")
ensure("PreToolUse", "TaskCreate|TaskUpdate", f"python3 {telem_dir}/task-gate.py", "task-gate.py")
ensure("SessionEnd", None, f"bash {telem_dir}/push.sh", "push.sh")

json.dump(settings, sys.stdout, indent=2)   # plain utf-8, no BOM
'
}

_verify_hooks() {
  python3 -c '
import json, sys
raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
settings = json.loads(raw) if raw else {}
WANT = {
    "PreToolUse": ["bash-destructive-gate.py", "ds-color-gate.py", "agent-track.py", "task-gate.py"],
    "UserPromptSubmit": ["fhir-architecture-trigger.py"],
    "SessionEnd": ["push.sh"],
}
blob = json.dumps(settings.get("hooks", {}))
missing = [f"{e}:{s}" for e, ss in WANT.items() for s in ss if s not in blob]
if missing:
    sys.stderr.write("missing hooks: " + ", ".join(missing) + "\n")
    sys.exit(1)
'
}

if [ -f "$SETTINGS" ]; then
  bak="$SETTINGS.bak.$(date +%s)"
  cp "$SETTINGS" "$bak"
  echo "✓ backed up settings → $bak"
  _src="$bak"
else
  _src=/dev/null
fi

if _merge_hooks < "$_src" > "$SETTINGS.tmp" && _verify_hooks < "$SETTINGS.tmp"; then
  mv "$SETTINGS.tmp" "$SETTINGS"
  echo "✓ settings updated (gates + telemetry registered + verified present; existing hooks untouched)"
else
  rm -f "$SETTINGS.tmp"
  echo "✗ hook wiring failed or did not verify — $SETTINGS left unchanged. GUARDRAILS NOT REGISTERED." >&2
  exit 1
fi

echo ""
echo "Done. Restart Claude Code to load the hooks."
echo "Installed gates: ds-color-gate (blocks rejected DS hex) · bash-destructive-gate · fhir-architecture advisor."
echo "Installed telemetry: the-talk (agent dispatches) · estimate-vs-actual · session-end push to the sink."
echo "Budget (token/\$ via OTEL) is opt-in — see scrips-telemetry/otel/README once a collector endpoint exists."
