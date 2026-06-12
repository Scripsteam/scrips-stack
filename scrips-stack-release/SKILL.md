---
name: scrips-stack-release
description: "The release discipline for the team kit. Whenever scrips-stack is updated (a skill added, changed, or removed), this skill MUST run: write a release note, produce friendly plain-language education material for the team, post it to the team channel, and request explicit acknowledgement from each member. A team-kit change never ships silently — the team learns what changed, why, and what they do differently, and acknowledges it. Fires on any merge/update to Scripsteam/scrips-stack."
type: procedure
---

# scrips-stack-release — no team-kit change ships silently

**Samer's rule (2026-06-12):** the team kit (`scrips-stack`) is the team's shared operating layer.
When it changes, people are now operating under a new rule or tool they may not know about. So every
update carries three obligations, always, in order:

1. **Release note** — a durable record in the repo (`RELEASES.md`).
2. **Friendly education material** — plain-language, non-jargon: what this is, why it matters, what
   you do differently, one concrete example. Written for a busy engineer, not a spec reader.
3. **Acknowledgement request** — posted to the team channel; each member explicitly acknowledges they
   read and understood it. Track who has / hasn't acked as an open-loops-ledger row until everyone has.

A team-kit change with no release note, no education, or no ack is incomplete — say so; don't report "shipped."

## When this fires
Any change to `Scripsteam/scrips-stack`: a new skill, a changed skill, a removed skill, an install/harness
change. Runs **with** the change (same PR or immediately on merge), never as an afterthought.

## Procedure
1. **Release note** — append an entry to `scrips-stack/RELEASES.md` (newest first):
   ```
   ## <YYYY-MM-DD> — <one-line title>  (PR #N)
   **What changed:** <skills added/changed/removed, one line each>
   **Why:** <the problem it solves, plainly>
   **What you do differently:** <the new habit / command / rule for the team>
   **Owner / questions:** <who to ask>
   ```
2. **Education material** — write the friendly explainer. Default surface = a well-formatted Slack
   message (mrkdwn) the team actually reads. For a bigger change, also drop an HTML one-pager in
   `~/claude-os/artifacts/<date>-<slug>-team-brief.html` and link it. Plain language, no internal jargon,
   one worked example. Lead with "what changes for you," not the implementation.
3. **Post + request ack** — post to `#current-active-team-scrips` (C052WJ0NL1J). End with an explicit
   ask: "React ✅ or reply `ack` to confirm you've read and understand this." Audit every factual claim
   (PR #, what shipped) against live `gh` data before posting (source-of-truth gate).
4. **Track acks** — open an open-loops-ledger row: "Team ack of <release> — owner: <each member> —
   tracker: the Slack thread — status: open until all acked." The daily reconcile chases stragglers.
5. **Report** — release note path + the Slack permalink + who still owes an ack.

## Notes
- If the Slack MCP is down, write the release note + education material, stage the post, and open a
  ledger row (status `blocked` on Slack) so the ack request is not lost.
- Keep it human. The point is the team genuinely understands the new loop, not that a box was ticked.
- Pairs with `open-loops-ledger` (the ack is itself a tracked loop) and `decision-lock-hygiene` (if the
  change encodes a decision).

**Origin:** 2026-06-12 — Samer: whenever we update the team stack, create friendly education material
the team can read + request their acknowledgement of the activated loop, and always write a release note.
