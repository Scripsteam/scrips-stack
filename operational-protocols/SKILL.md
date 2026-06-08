---
name: operational-protocols
description: Mechanical guardrails for Claude Code — Slack gateway, infra gate, activity log, context recovery. Read when diagnosing performance failures or setting up a new environment.
type: reference
---

# Operational Protocols — Claude Code

**Created:** 2026-04-21  
**Reason:** April 20 sessions had 4 systemic failures. These protocols replace memory-based rules with mechanical enforcement.

---

## The core principle

> Rules that live only in memory fail when context compacts. Rules enforced by hooks, scripts, and scheduled tasks survive compaction.

Every protocol below has a MECHANICAL layer (hook or scheduled task) plus a BEHAVIOURAL layer (what Claude must do when the gate fires).

---

## Protocol 1 — Slack Send Gate

**Failure it prevents:** Composing and sending Slack messages without Samer's review, especially after context compaction when prior conversation is lost.

**Mechanical layer:**  
`PreToolUse` hook on `slack_send_message` — fires on every call, injects mandatory checkpoint.

**Behavioural rule:**  
Before calling `slack_send_message`, Claude must:
1. Show Samer the exact message text in conversation and receive explicit approval ("send it", "yes", "go ahead")
2. State which channel/Jira thread was searched to confirm consistency with prior comms
3. If either is missing → use `slack_send_message_draft` instead, never `slack_send_message`

**Escalation:** If violated, this is a repeat offense (3rd recorded instance as of 2026-04-20). Next violation → Samer reviews hook config to block sends entirely.

---

## Protocol 2 — Infra Destructive Action Gate

**Failure it prevents:** Unilateral deletion of Azure resources, Kubernetes objects, or files without explicit per-action approval.

**Mechanical layer:**  
`PreToolUse` hook on `Bash` — `bash-destructive-gate.py` scans command for destructive patterns and injects a STOP checkpoint if found.

**Patterns monitored:**
- `az … delete`, `az … remove`, `az group delete`
- `kubectl delete`
- `terraform destroy`, `terraform apply`
- `rm -rf`, `rm -fr`
- SQL `DROP TABLE`, `DROP DATABASE`
- `gh repo delete`
- `git push --force`, `git reset --hard`

**Behavioural rule:**  
When the gate fires, Claude must answer all 3 before proceeding:
1. What exactly will be deleted — name the specific resource
2. Is this reversible? (Yes/No — be explicit)
3. Did Samer explicitly approve this specific action in this session? ("clean up the infra" ≠ approval to delete a named NIC

If any answer is uncertain → stop and ask Samer.

---

## Protocol 3 — Activity Log Enforcement

**Failure it prevents:** Sessions running without any log entry, making EOD wrap impossible and breaking cross-session continuity.

**Mechanical layer:**  
Scheduled task `activity-log-completeness-check` runs at 23:00 local time every day. If no entry for today → DMs Samer to reconstruct.

**Vault path:**  
`/Users/samertadross/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scrips Vault/01-operating-state/daily-activity-log.md`

**Behavioural rule:**  
Claude must append a log entry:
- At every natural topic shift within a session
- Before ending any session (before the Stop hook fires)
- Format: `### HH:MM — claude-code — [short title] [TAG]`

Minimum viable entry (if session was simple): one **Done:** line. Never skip entirely.

---

## Protocol 4 — Context Compaction Recovery

**Failure it prevents:** After context compaction, Claude proceeds on stale or fabricated facts because it doesn't know what it has lost.

**Mechanical layer:**  
`UserPromptSubmit` hook fires on every prompt, injecting a rules reminder into Claude's context. This survives compaction because it re-injects on every message.

**Behavioural rule:**  
If Claude detects that context was compacted (conversation summary visible, prior tool results gone):
1. Read `daily-activity-log.md` to reconstruct what happened today
2. Read any handoff doc at `~/claude-os/docs/handoffs/` dated today
3. Search Slack/Jira for the active topic before sending any message or taking any infra action
4. Do NOT proceed on memory of what "seemed" to be decided — verify from live sources

**Specific rule for Manish/infra communications:**  
After any compaction in sessions involving Manish, KV access, or PROD infra — always search `#general` and the relevant Jira ticket before composing any message.

---

## Protocol 5 — Session Wrap (existing, strengthened)

**Failure it prevents:** Work done without traceability.

**Mechanical layer:**  
`Stop` hook fires `session-end.sh` which invokes `session-capture` skill.

**Behavioural rule:**  
If Claude ends a session without a log entry, the Stop hook will attempt capture — but it needs context. Claude should write the activity log entry BEFORE the session naturally ends (not rely on the hook to reconstruct).

---

## Monitoring

| Check | Frequency | Method |
|---|---|---|
| Activity log completeness | Nightly 23:00 | `activity-log-completeness-check` scheduled task |
| Hook file presence | On-demand | `cat ~/.claude/settings.json` |
| Protocol violations | Weekly | `session-capture` skill EOD attribution section |

---

## Hook file locations

| Hook | File |
|---|---|
| Slack gate | Inline in `~/.claude/settings.json` |
| Bash destructive gate | `~/.claude/hooks/bash-destructive-gate.py` |
| Session start | `~/.claude/hooks/session-start.sh` |
| Session end | `~/.claude/hooks/session-end.sh` |
