---
name: signal-ds-judge
description: "Judge agent that reviews Signal DS canonical changes before they ship. Pre-commit / pre-PR gate for any work touching signal-portal, scrips-signal-ds, or scrips-react component code. Verifies proposed changes against the upstream hierarchy of authority and blocks drift bugs. Reduces Samer's review load by catching mechanical violations automatically — only true policy ambiguity escalates."
trigger: "judge ds, signal ds review, before commit signal-portal, before commit scrips-signal-ds, before commit scrips-react, ds gate, design system gate, canonical check, signal-ds-judge"
---

# Signal DS Judge — pre-commit canonical-check gate

This skill runs before any commit / PR / canonical-doc edit touching the Signal DS surfaces. Its job is to catch the class of drift bugs that Samer caught manually on 2026-05-13 (purple type identifier propagated from a downstream ADR even though the upstream palette rejected purple). The principle: **mechanical violations get blocked by the judge; only true policy ambiguity reaches Samer.**

## When this skill activates

- Before any commit to `~/scrips-repos/signal-portal/` (index.html, llms.txt, cards.html, contracts/, annexes/)
- Before any commit to `~/scrips-repos/scrips-signal-ds/` (tokens/, contracts/, DESIGN-STATE.md, captures/)
- Before any commit to `~/scrips-repos/scrips-react/src/components/` (Signal DS React component code)
- Before drafting any vault ADR in `06-decisions/design-system/`
- When the executing agent has just finished a Signal DS sweep and is about to report "done"

The executing agent (the agent that made the changes) **must invoke this skill** before reporting back to Samer. If invoked correctly, the judge produces one of three verdicts:

- **PASS** — proceed. Note: paste the verdict into the commit message footer.
- **FIX** — list of mechanical violations + suggested fixes. Executing agent applies fixes and re-runs the judge.
- **ESCALATE** — true policy ambiguity (the system itself disagrees with itself, or a new policy is needed). Surface to Samer with citations.

## The checks (run all, report each)

### Check 1 — Palette compliance

For each new/modified hex color in the diff:

1. Read `~/scrips-repos/scrips-signal-ds/tokens/design-tokens.ts`.
2. Read `~/scrips-repos/scrips-signal-ds/DESIGN-STATE.md`.
3. Find the hex in `design-tokens.ts`. If missing, check if it's a documented exception (e.g. surface bg `#0d0d18` for Stage).
4. Find the hex in `DESIGN-STATE.md`'s rejected-colors list. If present → **FIX**.

Report: `PALETTE | <hex> | IN_TOKENS=Y/N | REJECTED=Y/N | VERDICT=PASS/FIX`

### Check 2 — Terminology lock

For each text string in the diff:

1. **Internal docs** (llms.txt, ADRs, commit messages, code comments, contracts JSON): "Orb" is OK. "Scrips Intelligence" also OK. **"The Mark", "[I]", "AI badge", "AI insight"** = FIX (deprecated 2026-05-13).
2. **User-facing strings** (HTML body text in portal demos, UI copy, aria-labels, titles): "Scrips Intelligence" is canonical. "Orb" in user-facing copy = FIX. "AI", "AI suggested", "AI draft" used in pure brand attribution (vs. data-lineage labels in `dc-prov` row) = FIX → "Scrips Intelligence" variant.
3. **Cactus** in any canonical doc (signal-portal, scrips-signal-ds, llms.txt, contracts) = FIX. Allowed only in `06-decisions/` vault ADRs as comparison foil with explicit provenance.

Report: `TERMINOLOGY | <string> | CONTEXT=<file:line> | VERDICT=PASS/FIX`

### Check 3 — Orb canonical visual

For any `.de-avatar.ai`, `.dc-orb`, `.dc-orb-inline`, or surface-level Orb instance in the diff:

1. Verify the markup is white-circle + Scrips icon (SVG `<use href="#scrips-icon"/>`) + NO text content.
2. Verify aria-label and title = "Scrips Intelligence".
3. Verify border / icon fill / bg are from the locked 3-context contrast table (Light / Dark-Stage / Surface-Orb).
4. Verify state semantics (Resting/Working/Ready/Attention/Critical) appear ONLY on surface-level Orbs, not on card-head or inline Orbs.

Report: `ORB | <element> | TEXT_INSIDE=Y/N | ARIA=PASS/FAIL | CONTRAST_VARIANT=<ctx> | VERDICT=PASS/FIX`

### Check 4 — CardInsight composition pattern

If any new CardInsight markup (header icon `🔗`, `dc-aitag "AI insight"`, `dc-dot insight`, purple stripe):

1. Verify no `dc-dot.insight` in head (deprecated 2026-05-13).
2. Verify no purple anywhere on the card.
3. Verify the head carries an Orb (`.dc-orb`) signalling Scrips Intelligence authorship.
4. Verify the body shows the two-CardData composition pattern with connector glyph.

Report: `CARDINSIGHT | <demo> | PURPLE=Y/N | ORB_PRESENT=Y/N | COMPOSITION=Y/N | VERDICT=PASS/FIX`

### Check 5 — Provenance pill (`dc-aitag`) placement

For each `.dc-aitag` in the diff:

1. Verify it lives in a `dc-prov` row at card bottom (data-lineage axis) — NOT in card head, NOT as standalone presence indicator.
2. Verify label vocab: `AI extracted`, `AI synthesised`, `✓ confirmed`, `awaiting confirmation`, `human entered`, `device`, `OCR`.
3. If label is `AI`, `AI insight`, `AI draft` standalone in head → FIX (collapse into Orb or move to dc-prov row).

Report: `DCAITAG | <element> | IN_DC_PROV=Y/N | LABEL=<text> | VERDICT=PASS/FIX`

### Check 6 — ADR-amendment provenance

If a vault ADR in `06-decisions/` is being edited:

1. Verify the amendment has dated `[HUMAN]` or `[CLAUDE]` provenance per `feedback_canonical_doc_gap_provenance.md`.
2. Verify `supersedes:` / `amends:` frontmatter is filled correctly.
3. If Claude-authored, verify `status-draft` + DRAFT FOR REVIEW header per `feedback_drafts_not_decisions.md`.

Report: `ADR | <file> | PROVENANCE=PASS/FAIL | STATUS=<value> | VERDICT=PASS/FIX`

### Check 7 — Upstream / downstream drift

Cross-check downstream docs against upstream tokens:

1. For each canonical claim in modified `signal-portal/llms.txt`, `index.html`, or `cards.html`, verify against `scrips-signal-ds/tokens/design-tokens.ts` + `DESIGN-STATE.md`.
2. If downstream contradicts upstream → ESCALATE (this is the bug class that triggered creating this judge).

Report: `DRIFT | <claim> | UPSTREAM=<value> | DOWNSTREAM=<value> | VERDICT=PASS/ESCALATE`

## Output

The judge writes its verdict report to `~/scrips-repos/signal-portal/.judge-reports/<timestamp>-<branch>.md` (gitignored — create the .gitignore entry if it doesn't exist). For PR-bound work, the verdict goes into the PR description as a `<details>` block.

For PASS: the executing agent proceeds with the commit + push.
For FIX: the executing agent applies the fixes and re-invokes the judge.
For ESCALATE: the executing agent surfaces to Samer with a one-paragraph summary citing the specific check that escalated.

## Why this skill exists

Samer's directive 2026-05-13: "I don't want to become a person who validates every decision. We improve the system, we introduce guardrails, we create judge agents who oversee the execution agents." This skill is the agent layer of that ask. Memory + context (`signal-ds-authority.md`, `feedback_authority_hierarchy_check_upstream_first.md`) is the *knowledge* layer. The pre-commit hook (proposed in same session) would be the *code* layer. Together they form a 3-layer enforcement stack: knowledge → judge → hook. Each one independently catches the class of drift bug that Samer caught manually today.

## Roadmap (not yet built)

- `~/scrips-repos/signal-portal/.git/hooks/pre-commit` — bash script that fails commits introducing non-token hex codes (the code layer).
- A scheduled cron task that runs the judge across the full repo weekly and reports drift to Samer (regression detection).
- A judge invocation in the `scrips-design-sdlc` Phase 5 (ship gate) — the SDLC already has phases, this becomes the locked gate before phase complete.
