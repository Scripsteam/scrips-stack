#!/usr/bin/env bash
# scrips-stack team-setup
# Installs everything a Scrips engineer needs beyond the base scrips-stack `./setup`.
# Idempotent. Dry-run by default. Pass --apply to actually write.
#
# Adds on top of the base setup:
#   1. figma-console MCP (requires FIGMA_ACCESS_TOKEN env var — never embedded)
#   2. ~/scrips-repos/.worktrees/ base for parallel sub-agent work
#   3. ~/.claude/settings.local.json with deny rules (brain / QuickBooks / Attio / Outlook)
#   4. Optional Anthropic API key bootstrap for CronCreate (--with-cron flag)
#   5. Post-install smoke test via readiness-check.sh
#
# Usage:
#   bash team-setup.sh              # dry-run, shows what would change
#   bash team-setup.sh --apply      # apply
#   bash team-setup.sh --apply --with-cron  # also bootstrap Anthropic API key file
#   FIGMA_ACCESS_TOKEN=figd_xxx bash team-setup.sh --apply

set -u
shopt -s nullglob

APPLY=0
WITH_CRON=0
for arg in "$@"; do
  case "$arg" in
    --apply)     APPLY=1 ;;
    --dry-run)   APPLY=0 ;;
    --with-cron) WITH_CRON=1 ;;
    --help|-h)
      sed -n '2,20p' "$0"
      exit 0
      ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

CHANGES=0
SKIPS=0
ERRORS=0

mode_tag() { if [ $APPLY -eq 1 ]; then echo "APPLY"; else echo "DRY-RUN"; fi; }

step() { echo ""; echo "── $1 ─────────────────────────────────"; }
ok()   { echo "  ✓ $1"; }
add()  { echo "  + $1"; CHANGES=$((CHANGES+1)); }
skip() { echo "  · $1"; SKIPS=$((SKIPS+1)); }
err()  { echo "  ✗ $1"; ERRORS=$((ERRORS+1)); }

echo "scrips-stack team-setup · mode=$(mode_tag)"
echo "Run with --apply to actually write changes."

# ─────────────────────────────────────────────────────────────
step "1. Prereqs"
need_cmds=(claude jq npx git curl python3)
for c in "${need_cmds[@]}"; do
  if command -v "$c" >/dev/null 2>&1; then
    ok "$c present"
  else
    err "$c missing — install before continuing"
  fi
done
if [ $ERRORS -gt 0 ]; then
  echo ""
  echo "Resolve missing commands first, then re-run. Common installs:"
  echo "    jq      → macOS: brew install jq   ·   Windows: winget install jqlang.jq   ·   Linux: apt install jq"
  echo "    npx/node→ install Node.js LTS (https://nodejs.org)"
  echo "    claude  → npm i -g @anthropic-ai/claude-code"
  exit 1
fi

# ─────────────────────────────────────────────────────────────
step "2. Base scrips-stack ./setup"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_SETUP="$SCRIPT_DIR/setup"
if [ -x "$BASE_SETUP" ]; then
  if [ $APPLY -eq 1 ]; then
    "$BASE_SETUP" | sed 's/^/    /'
    add "ran ./setup"
  else
    skip "would run: $BASE_SETUP"
  fi
else
  err "$BASE_SETUP not found or not executable"
fi

# ─────────────────────────────────────────────────────────────
step "3. figma-console MCP"
CLAUDE_JSON="$HOME/.claude.json"
if [ ! -f "$CLAUDE_JSON" ]; then
  err "$CLAUDE_JSON missing — open Claude Code once to initialize it"
elif python3 -c "import json,sys; cfg=json.load(sys.stdin); sys.exit(0 if 'figma-console' in cfg.get('mcpServers',{}) else 1)" < "$CLAUDE_JSON" 2>/dev/null; then
  skip "figma-console MCP already configured"
else
  TOK="${FIGMA_ACCESS_TOKEN:-}"
  if [ -z "$TOK" ]; then
    echo "  ! FIGMA_ACCESS_TOKEN not set."
    echo "    Generate one at https://www.figma.com/settings → Personal access tokens (scopes: file_content:read, library_assets:read)."
    echo "    Then re-run: FIGMA_ACCESS_TOKEN=figd_xxx bash $0 --apply"
    err "figma-console MCP not added (no token)"
  else
    if [ $APPLY -eq 1 ]; then
      # Shell owns the path (read via stdin, write via stdout) so this works on
      # Windows Git Bash too — never pass an MSYS path to native Python.
      cp "$CLAUDE_JSON" "$CLAUDE_JSON.bak.team-setup"
      if python3 -c '
import json, os, sys
cfg = json.load(sys.stdin)
cfg.setdefault("mcpServers", {})["figma-console"] = {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "figma-console-mcp@latest"],
  "env": {
    "FIGMA_ACCESS_TOKEN": os.environ["FIGMA_ACCESS_TOKEN"],
    "ENABLE_MCP_APPS": "true"
  }
}
json.dump(cfg, sys.stdout, indent=2)
' < "$CLAUDE_JSON.bak.team-setup" > "$CLAUDE_JSON.tmp" \
        && python3 -c "import json,sys; sys.exit(0 if 'figma-console' in json.load(sys.stdin).get('mcpServers',{}) else 1)" < "$CLAUDE_JSON.tmp"; then
        mv "$CLAUDE_JSON.tmp" "$CLAUDE_JSON"
        add "figma-console MCP added to ~/.claude.json (backup .bak.team-setup written)"
        echo "    Restart Claude Code (cmd-q + reopen) to load the new MCP."
      else
        rm -f "$CLAUDE_JSON.tmp"
        err "figma-console write failed or did not verify — ~/.claude.json left unchanged (backup at .bak.team-setup)"
        exit 1
      fi
    else
      skip "would add figma-console MCP to ~/.claude.json"
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────
step "4. Worktree base ~/scrips-repos/.worktrees/"
WT_BASE="$HOME/scrips-repos/.worktrees"
if [ -d "$WT_BASE" ]; then
  skip "$WT_BASE exists"
else
  if [ $APPLY -eq 1 ]; then
    mkdir -p "$WT_BASE"
    add "created $WT_BASE"
  else
    skip "would create: $WT_BASE"
  fi
fi

# Also add a gitignore so worktree dirs don't leak into commits if accidentally placed inside a repo
WT_GITIGNORE="$WT_BASE/.gitignore"
if [ -f "$WT_GITIGNORE" ]; then
  skip "$WT_GITIGNORE exists"
else
  if [ $APPLY -eq 1 ] && [ -d "$WT_BASE" ]; then
    echo "*" > "$WT_GITIGNORE"
    add "wrote $WT_GITIGNORE (worktree dirs are local-only)"
  fi
fi

# ─────────────────────────────────────────────────────────────
step "5. ~/.claude/settings.local.json — permissions + deny rules"
SETTINGS_DIR="$HOME/.claude"
SETTINGS_LOCAL="$SETTINGS_DIR/settings.local.json"
mkdir -p "$SETTINGS_DIR" 2>/dev/null

# Build the desired settings shape
DESIRED='{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(git:*)",
      "Bash(gh:*)",
      "Bash(vite:*)",
      "Bash(vitest:*)",
      "Bash(tsc:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(rg:*)",
      "Bash(cd:*)",
      "Bash(pwd)"
    ],
    "deny": [
      "mcp__open-brain__*",
      "mcp__054f9675-3ada-42a5-9ea5-2540c590bd80__*",
      "mcp__e6a781a3-9fd7-4651-9e82-64b57515fd1a__*",
      "mcp__489aa7e8-3be1-49ad-9bcf-5d408c5deb7b__*",
      "mcp__33e6f2fe-46f7-4bf8-a872-5045ab025621__outlook_email_search",
      "mcp__6ce931b2-f490-42ba-8740-23c89c9704ed__*",
      "mcp__mcp-obsidian__*",
      "Bash(az:*)",
      "Bash(kubectl:*)",
      "Bash(terraform:*)"
    ]
  }
}'

if [ -f "$SETTINGS_LOCAL" ]; then
  # Merge: preserve any existing permissions the engineer added, but ensure our denies + allows are present.
  # Shell owns the path (read via stdin, write via stdout) so native Windows Python never sees an MSYS
  # path — the bug that silently dropped the deny guardrails on every Windows machine while reporting ✓.
  if [ $APPLY -eq 1 ]; then
    cp "$SETTINGS_LOCAL" "$SETTINGS_LOCAL.bak.team-setup"
    if DESIRED_JSON="$DESIRED" python3 -c '
import json, os, sys
existing = json.load(sys.stdin)
desired = json.loads(os.environ["DESIRED_JSON"])
existing.setdefault("permissions", {})
for bucket in ("allow", "deny"):
    cur = set(existing["permissions"].get(bucket, []))
    cur.update(desired["permissions"].get(bucket, []))
    existing["permissions"][bucket] = sorted(cur)
json.dump(existing, sys.stdout, indent=2)
' < "$SETTINGS_LOCAL.bak.team-setup" > "$SETTINGS_LOCAL.tmp" \
      && DESIRED_JSON="$DESIRED" python3 -c '
import json, os, sys
got = set(json.load(sys.stdin).get("permissions", {}).get("deny", []))
want = json.loads(os.environ["DESIRED_JSON"])["permissions"]["deny"]
missing = [r for r in want if r not in got]
sys.exit(1 if missing else 0)
' < "$SETTINGS_LOCAL.tmp"; then
      mv "$SETTINGS_LOCAL.tmp" "$SETTINGS_LOCAL"
      add "merged allow + deny rules into $SETTINGS_LOCAL (verified all deny rules present; backup .bak.team-setup written)"
    else
      rm -f "$SETTINGS_LOCAL.tmp"
      err "deny-rule merge failed or did not verify — $SETTINGS_LOCAL left unchanged (backup at .bak.team-setup). SECURITY GUARDRAILS NOT APPLIED."
      exit 1
    fi
  else
    skip "would merge allow + deny rules into existing $SETTINGS_LOCAL"
  fi
else
  if [ $APPLY -eq 1 ]; then
    echo "$DESIRED" > "$SETTINGS_LOCAL"
    add "wrote new $SETTINGS_LOCAL"
  else
    skip "would write new $SETTINGS_LOCAL"
  fi
fi

# Sanity-check: do NOT write permissions to settings.json — that breaks remote MCPs (learned 2026-04-12)
SETTINGS_GLOBAL="$SETTINGS_DIR/settings.json"
if [ -f "$SETTINGS_GLOBAL" ] && python3 -c "import json,sys; c=json.load(open('$SETTINGS_GLOBAL')); sys.exit(0 if 'permissions' in c else 1)" 2>/dev/null; then
  echo "  ! WARNING: $SETTINGS_GLOBAL has a permissions block."
  echo "    Per learned-2026-04-12, this breaks remote MCPs."
  echo "    Move the permissions block to settings.local.json manually, then restart Claude Code."
fi

# ─────────────────────────────────────────────────────────────
step "6. Anthropic API key (optional · --with-cron)"
if [ $WITH_CRON -eq 1 ]; then
  KEY_FILE="$HOME/.anthropic-api-key"
  if [ -f "$KEY_FILE" ]; then
    skip "$KEY_FILE already exists"
  else
    if [ $APPLY -eq 1 ]; then
      touch "$KEY_FILE"
      chmod 600 "$KEY_FILE"
      add "created empty $KEY_FILE (chmod 600) — paste your scoped key in. Get one from console.anthropic.com → API Keys"
    else
      skip "would create $KEY_FILE (chmod 600)"
    fi
  fi
else
  skip "skipped (pass --with-cron to bootstrap)"
fi

# ─────────────────────────────────────────────────────────────
step "7. Smoke test · readiness-check.sh"
RC="$SCRIPT_DIR/readiness-check.sh"
if [ -x "$RC" ]; then
  if [ $APPLY -eq 1 ]; then
    echo ""
    "$RC" || true
  else
    skip "would run: $RC"
  fi
else
  err "$RC not found or not executable"
fi

# ─────────────────────────────────────────────────────────────
step "Summary · mode=$(mode_tag)"
echo "  changes proposed: $CHANGES"
echo "  skipped:          $SKIPS"
echo "  errors:           $ERRORS"
echo ""
if [ $APPLY -eq 0 ] && [ $CHANGES -gt 0 ]; then
  echo "Re-run with --apply to write the changes."
fi
if [ $ERRORS -gt 0 ]; then
  exit 1
fi
