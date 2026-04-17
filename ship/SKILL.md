---
name: ship
description: Create a PR with full Scrips conventions — branch name, commit format, Jira link, changelog entry, reviewer assignment. Use when the user says "ship", "create PR", "push", or "open a pull request".
---

# /ship — Scrips Release Workflow

You are the Scrips release engineer. Ship clean, traceable PRs every time.

## Step 1: Confirm state

```bash
git status --porcelain
git branch --show-current
git log --oneline -5
```

If working tree is dirty with uncommitted changes, ask: "You have uncommitted changes. Commit them as part of this PR, or stash first?"

## Step 2: Identify the Jira ticket

Extract from:
1. Current branch name (format: `feat/DEV-XXXX-description`)
2. Recent commit messages (`[DEV-XXXX]` prefix)
3. Ask the user if neither is clear

If no ticket is found, ask for one. Every Scrips PR must link a Jira ticket.

## Step 3: Validate branch name

Branch must follow: `{type}/{jira-ticket}-{slug}`

Types: `feat` · `fix` · `chore` · `refactor` · `hotfix`

If wrong format, rename:
```bash
git branch -m <current> <correct-name>
```

## Step 4: Validate commit messages

All commits must follow: `[DEV-XXXX] Short description (imperative)`

Check recent commits:
```bash
git log origin/main..HEAD --oneline
```

If commits don't follow format, offer to rewrite the last one:
```bash
git commit --amend -m "[DEV-XXXX] Description"
```

## Step 5: Push and create PR

```bash
git push -u origin HEAD
```

Then create PR via gh CLI. Use this exact format:

```bash
gh pr create \
  --title "[DEV-XXXX] Feature description" \
  --body "$(cat <<'EOF'
## Jira
[DEV-XXXX](https://scrips.atlassian.net/browse/DEV-XXXX)

## What changed
<!-- 1-3 bullets: what this PR does -->

## Why
<!-- The Jira story or bug context -->

## Test plan
<!-- How to verify this works -->
- [ ] Verified on staging
- [ ] No Signal DS token regressions
- [ ] No breaking changes to API contracts

## Checklist
- [ ] Linked Jira ticket
- [ ] Self-reviewed diff
- [ ] Tests added/updated
EOF
)" \
  --reviewer "Scripsteam/eng"
```

## Step 6: Report

After creating the PR, output:
- PR URL
- Jira ticket link
- Files changed count
- Any outstanding items (failing CI, missing tests, etc.)

## Rules

- Never push directly to `main` or `develop`
- Never skip the Jira link
- Never bundle unrelated changes — one ticket, one PR
- If CI is failing, say so before calling it done
