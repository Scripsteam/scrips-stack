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
#
# The shell owns the path (read via stdin, write via stdout) so native Windows
# Python never sees an MSYS /c/Users/... path — the bug class PR #7 killed in
# team-setup.sh, which silently dropped the guardrails on every Windows machine
# while reporting ✓. The read also decodes utf-8-sig: PowerShell's Out-File
# writes a UTF-8 BOM that otherwise makes json.load choke at char 0, leaving the
# hooks unregistered even once the path is fixed. After the write we re-read and
# assert every wanted hook is present — it can no longer claim success it didn't
# achieve.
_merge_hooks() {
  HOOKS_DIR="$HOOKS_DST" python3 -c '
import json, os, sys
raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()   # tolerate a PowerShell BOM
settings = json.loads(raw) if raw else {}
hooks_dir = os.environ["HOOKS_DIR"]
WANT = {
    "PreToolUse": ["bash-destructive-gate.py", "ds-color-gate.py"],
    "UserPromptSubmit": ["fhir-architecture-trigger.py"],
}
hooks = settings.setdefault("hooks", {})
for event, scripts in WANT.items():
    matchers = hooks.setdefault(event, [])
    present = json.dumps(matchers)
    for s in scripts:
        if s in present:
            continue
        matchers.append({"hooks": [{"type": "command",
            "command": f"python3 {hooks_dir}/{s}"}]})
json.dump(settings, sys.stdout, indent=2)   # plain utf-8, no BOM
'
}

_verify_hooks() {
  python3 -c '
import json, sys
raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
settings = json.loads(raw) if raw else {}
WANT = {
    "PreToolUse": ["bash-destructive-gate.py", "ds-color-gate.py"],
    "UserPromptSubmit": ["fhir-architecture-trigger.py"],
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
  echo "✓ settings updated (hooks registered + verified present; existing hooks untouched)"
else
  rm -f "$SETTINGS.tmp"
  echo "✗ hook wiring failed or did not verify — $SETTINGS left unchanged. GUARDRAILS NOT REGISTERED." >&2
  exit 1
fi

echo ""
echo "Done. Restart Claude Code to load the hooks."
echo "Installed gates: ds-color-gate (blocks rejected DS hex) · bash-destructive-gate · fhir-architecture advisor."
