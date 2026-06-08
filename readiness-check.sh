#!/usr/bin/env bash
# scrips-stack readiness check
# Verifies a new engineer's environment is ready for /onboard.
# Run BEFORE day 1.

set -u
shopt -s nullglob

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✓ $1"; PASS=$((PASS+1)); }
bad()  { echo "  ✗ $1"; FAIL=$((FAIL+1)); }
warn() { echo "  ! $1"; WARN=$((WARN+1)); }

section() { echo ""; echo "── $1 ─────────────────────────────────"; }

# ─────────────────────────────────────────────────────────────
section "1. Claude Code CLI"
if command -v claude >/dev/null 2>&1; then
  v=$(claude --version 2>/dev/null | head -1)
  ok "claude installed ($v)"
else
  bad "claude not installed — run: npm install -g @anthropic-ai/claude-code"
fi

# ─────────────────────────────────────────────────────────────
section "2. scrips-stack skills"
SKILLS_DIR="$HOME/.claude/skills"
if [ ! -d "$SKILLS_DIR" ]; then
  bad "$SKILLS_DIR does not exist"
else
  ok "$SKILLS_DIR exists"
fi

REQUIRED_SKILLS=(onboard sprint ship review investigate qa brief retro design-sync checkpoint port-spec synth decompose-strategy admin-sprint-runner be-sprint-runner)
for s in "${REQUIRED_SKILLS[@]}"; do
  if [ -e "$SKILLS_DIR/$s/SKILL.md" ]; then
    ok "$s skill present"
  else
    bad "$s skill missing — re-run scrips-stack setup"
  fi
done

# umbrella link
if [ -L "$SKILLS_DIR/scrips" ]; then
  ok "scrips-stack umbrella link present (→ $(readlink "$SKILLS_DIR/scrips"))"
else
  warn "$SKILLS_DIR/scrips umbrella link missing (not critical, but expected)"
fi

# ─────────────────────────────────────────────────────────────
section "2b. Engineering skills (design system · SDLC · disciplines)"
# The full engineering toolset the team uses day to day. These ship as
# top-level <name>/SKILL.md so the setup glob installs them as slash commands.
ENG_SKILLS=(html-artifact design-to-dev-pipeline scrips-design-sdlc \
  signal-ds-graduation signal-ds-judge signal-system-sweep \
  figma-design-sweep figma-doc-sync ds-parity-maintenance \
  sdlc-handoff source-of-truth-discipline operational-protocols \
  decision-lock-hygiene slide-library)
for s in "${ENG_SKILLS[@]}"; do
  if [ -f "$SKILLS_DIR/$s/SKILL.md" ]; then
    ok "$s skill present"
  else
    bad "$s skill missing — re-run scrips-stack setup"
  fi
done
echo "  → smoke/stress test: in a Claude session type '/' (or run /find-skills) and confirm each command above is invocable, not just present on disk."

# Methodology collection — now installed flat as slash commands (setup scans methodology/*/SKILL.md).
METHODOLOGY_SKILLS=(brainstorming dispatching-parallel-agents executing-plans \
  finishing-a-development-branch receiving-code-review requesting-code-review \
  subagent-driven-development systematic-debugging test-driven-development \
  using-git-worktrees verification-before-completion writing-plans)
for s in "${METHODOLOGY_SKILLS[@]}"; do
  if [ -f "$SKILLS_DIR/$s/SKILL.md" ]; then
    ok "$s skill present"
  else
    bad "$s skill missing — re-run scrips-stack setup"
  fi
done

# ─────────────────────────────────────────────────────────────
section "3. Repos in ~/scrips-repos/"
REPOS=(
  # universal
  scrips-stack
  # FE / Flutter (only needed for FE-stream engineers)
  scrips-react scrips-signal-ds scrips_msp1_pa scrips_msp1_pm scrips_msp1_flutter_shared
  # BE .NET services
  Scrips.Patient Scrips.Persons Scrips.Provider Scrips.Billing
  Scrips.PracticeManagement Scrips.Practice.Aggregator Scrips.QuestionBank
  Scrips.Core Scrips.Common Scrips.Integration.Fhir
)
REPO_BASE="$HOME/scrips-repos"
if [ ! -d "$REPO_BASE" ]; then
  bad "$REPO_BASE does not exist — clone repos here, NOT OneDrive"
else
  ok "$REPO_BASE exists"
  for r in "${REPOS[@]}"; do
    if [ -d "$REPO_BASE/$r" ]; then
      ok "$r cloned"
    else
      warn "$r not cloned (only needed if your epic touches it)"
    fi
  done
fi

# OneDrive check — fatal
if [ -d "$HOME/OneDrive" ] && find "$HOME/OneDrive" -maxdepth 3 -name ".git" -type d 2>/dev/null | grep -q .; then
  bad "Found git repos inside OneDrive — MOVE THEM. OneDrive sync breaks git worktrees."
fi

# ─────────────────────────────────────────────────────────────
section "4. Git config"
GIT_NAME=$(git config --global user.name 2>/dev/null)
GIT_EMAIL=$(git config --global user.email 2>/dev/null)
if [ -n "$GIT_NAME" ]; then ok "git user.name = $GIT_NAME"; else bad "git user.name not set"; fi
if [ -n "$GIT_EMAIL" ]; then
  if [[ "$GIT_EMAIL" == *"@scrips.com" ]]; then
    ok "git user.email = $GIT_EMAIL"
  else
    warn "git user.email = $GIT_EMAIL (not a @scrips.com address — confirm with Samer)"
  fi
else
  bad "git user.email not set"
fi

# ─────────────────────────────────────────────────────────────
section "5. Figma MCP"
CLAUDE_JSON="$HOME/.claude.json"
if [ -f "$CLAUDE_JSON" ]; then
  if grep -q "figma-dev-mode" "$CLAUDE_JSON" 2>/dev/null; then
    ok "figma-dev-mode MCP configured in ~/.claude.json"
  else
    warn "figma-dev-mode MCP not in ~/.claude.json (only needed for design work)"
  fi
else
  warn "~/.claude.json not found"
fi

# Probe Figma local MCP if Desktop is running
if curl -s --max-time 1 http://127.0.0.1:3845/sse >/dev/null 2>&1; then
  ok "Figma Desktop MCP server reachable at 127.0.0.1:3845"
else
  warn "Figma Desktop MCP not reachable — start Figma Desktop + enable MCP in Preferences (only needed for design work)"
fi

# ─────────────────────────────────────────────────────────────
section "6. Node + scrips-react dev server"
if command -v node >/dev/null 2>&1; then
  ok "node installed ($(node --version))"
else
  bad "node not installed"
fi
if command -v npm >/dev/null 2>&1; then
  ok "npm installed ($(npm --version))"
else
  bad "npm not installed"
fi

if [ -d "$REPO_BASE/scrips-react" ]; then
  if [ -d "$REPO_BASE/scrips-react/node_modules" ]; then
    ok "scrips-react node_modules present (npm install has run)"
  else
    warn "scrips-react/node_modules missing — run: cd $REPO_BASE/scrips-react && npm install"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "7. .NET / dotnet (BE engineers)"
if command -v dotnet >/dev/null 2>&1; then
  ok "dotnet installed ($(dotnet --version 2>/dev/null))"
  # Check at least one BE repo is present + restorable
  for be_repo in Scrips.Common Scrips.Core Scrips.Patient; do
    if [ -d "$REPO_BASE/$be_repo" ]; then
      ok "$be_repo present (run 'dotnet restore' inside it before first build)"
      break
    fi
  done
else
  warn "dotnet not installed (only needed for BE engineers — install .NET 8 SDK from dotnet.microsoft.com)"
fi

# ─────────────────────────────────────────────────────────────
section "8. Atlassian access"
if command -v atlassian-cli >/dev/null 2>&1 || [ -f "$HOME/.atlassian-mcp.toml" ] || grep -q "atlassian" "$CLAUDE_JSON" 2>/dev/null; then
  ok "Atlassian access configured"
else
  warn "Atlassian MCP not detected — confirm with Samer that Jira + Confluence access is provisioned"
fi

# ─────────────────────────────────────────────────────────────
section "Summary"
echo "  PASS: $PASS"
echo "  WARN: $WARN"
echo "  FAIL: $FAIL"
echo ""

if [ $FAIL -gt 0 ]; then
  echo "❌ NOT READY — fix the $FAIL failures above before starting /onboard"
  exit 1
elif [ $WARN -gt 0 ]; then
  echo "⚠️  READY WITH WARNINGS — review the $WARN warnings above"
  exit 0
else
  echo "✅ READY — proceed with /onboard"
  exit 0
fi
