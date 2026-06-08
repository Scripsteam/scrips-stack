---
name: decision-lock-hygiene
description: Mandatory post-lock cleanup — after any decision locks, find and archive everything it supersedes, then verify no conflicting answers remain in any source
trigger: "decision locked, locked, archive stale, hygiene check, knowledge cleanup, retire superseded"
---

# Decision Lock Hygiene

Run this skill every time a decision locks or a canonical fact changes. This is the **backward pass** — the forward pass (capture, decide, lock) already exists. This skill handles what comes after: retire what's now wrong, verify the search space is clean.

**This is not optional.** Every decision session must end with this skill. If it doesn't run, stale files will cause hallucination in the next session.

## When to trigger

- A design decision locks (DS-XXX)
- A canonical value changes (color, font, hierarchy, architecture)
- A spec supersedes a previous spec
- A project state changes (tool adopted, tool rejected, person joins/leaves)
- Explicitly requested: "hygiene check", "clean up after lock"
- As the final step of the `session-capture` skill

## Inputs

Before running, you must know:
1. **What locked** — the specific decision or fact (e.g., "primary color is #0076F8")
2. **Where the canonical source is** — the file that holds the locked truth
3. **What terms to search** — keywords that would surface competing answers

If these aren't clear from context, ask before proceeding.

## STEP 1: Identify the blast radius

For the locked decision, determine the **search terms** that would surface competing or stale information. Be thorough — think about synonyms, old names, hex values, etc.

Example for "primary color locked as #0076F8":
- Search terms: `primary color`, `#0076F8`, `#007AFF`, `#233D93`, `#5C41B5`, `#061AB3`, `color-primary`, `Brand/Primary`, `blue depth`

## STEP 2: Search ALL sources

Run searches across every knowledge layer. These must all be checked — no shortcuts.

### 2a. Obsidian vault
- `obsidian_simple_search` for each search term
- Check: `00-inbox/`, `03-knowledge-base/`, `04-references/`, `05-memory/`, `06-decisions/`, `10-session-memos/`

### 2b. Second Brain
- `search_brain` for each search term

### 2c. Claude memory
- Read `MEMORY.md` index
- Read any memory files whose descriptions match the topic

### 2d. Confluence
- `searchConfluenceUsingCql` for each search term

### 2e. Repository docs
- Check CLAUDE.md, README.md, and any design-system/architecture docs in relevant repos
- Check: `scrips-react`, `scrips-signal-ds`, `signal-portal`, and any other active repos

### 2f. Figma (if design-related)
- `figma_get_variables` or `figma_browse_tokens` to verify Figma matches the locked value

## STEP 3: Classify each result

For every file/page/entry that mentions the topic, classify it:

| Classification | Meaning | Action |
|---|---|---|
| **CANONICAL** | This IS the locked source of truth | Leave as-is. There must be exactly ONE. |
| **CONSISTENT** | States the same value as canonical | Leave as-is. Note it as a valid reference. |
| **STALE** | States an old/wrong value | Archive or update (Step 4) |
| **CONTRADICTS** | States a different value as if current | Archive or update (Step 4) |
| **CONTEXT** | Historical reference that doesn't claim to be current | Leave as-is if clearly dated. Add deprecation note if ambiguous. |

## STEP 4: Retire stale/contradicting sources

For each STALE or CONTRADICTS file:

### Obsidian vault files
- If the entire file is superseded: add a deprecation banner at line 1:
  ```
  > [!warning] ARCHIVED [DATE]
  > This file is superseded by [[canonical-file-name]]. Do not use for current values.
  ```
- If only specific values are wrong: update them inline with a note: `~~old value~~ → new value (updated [DATE], see [[canonical-file]])`
- If the file should be moved: move to `_archive/` subdirectory within the same section

### Claude memory files
- If the memory is now wrong: update the file content and description
- If the memory is entirely superseded: delete the file and remove from MEMORY.md

### Confluence pages
- If the page has a mix of current and stale: update the stale sections
- If the entire page is stale: add a banner at the top and note it for archival
- Do NOT delete Confluence pages without asking Samer first (team-visible)

### Repository docs
- Update inline. These are code — treat them like code changes.

### Brain captures
- Brain captures are immutable (no edit API). If a brain entry is stale, capture a NEW thought that explicitly corrects it: "CORRECTION: [old claim] is superseded by [new claim] as of [date]. Canonical source: [file]."

## STEP 5: Verify uniqueness

After all retirements, re-run the searches from Step 2 for the **core fact** (e.g., "what is the primary color?").

The test: **only ONE authoritative answer should come back.** Other results should be clearly marked as archived, historical, or pointing to the canonical source.

If multiple authoritative answers still exist → you're not done. Go back to Step 4.

## STEP 6: Report

Print a summary:

```
DECISION LOCK HYGIENE — [DATE]

Decision: [what locked]
Canonical source: [file path]

| Source | File/Page | Status | Action Taken |
|--------|-----------|--------|--------------|
| Vault  | design-system-tokens.md | CANONICAL | — |
| Vault  | scrips-design-system.md | STALE | Archived with banner |
| Memory | project_design_system_state.md | CONTRADICTS | Updated |
| Confluence | Figma Workspace Index | CONSISTENT | — |
| Brain  | thought-xyz | STALE | Correction captured |

Uniqueness test: PASS / FAIL
Remaining conflicts: [list any unresolved]
```

## STEP 7: Update session-capture integration

If this skill was triggered by a decision lock during a session, ensure the `session-capture` skill (when it runs at session end) knows about this cleanup. Add a comment to the relevant vault memo:
```
<!-- decision-lock-hygiene: ran [DATE], archived N files, uniqueness: PASS/FAIL -->
```

## Rules

1. **One canonical source per fact.** If two files both claim to be authoritative, one of them is wrong. Determine which by date and decision chain.
2. **Never silently skip a source.** If a search layer is unreachable (API error, etc.), report it as SKIPPED with reason. Do not claim the hygiene passed.
3. **Archive, don't delete.** Stale files get deprecation banners and move to `_archive/`. Deletion loses provenance.
4. **Brain corrections must be explicit.** Since brain captures are immutable, always capture a new corrective thought rather than hoping the old one won't surface.
5. **Confluence changes are team-visible.** Flag any Confluence changes to Samer before executing, unless it's clearly a factual correction (wrong hex value → right hex value).
6. **This skill is the LAST step of any decision session.** It runs after the decision doc is written, after the spec is updated, after the brain capture. It is the cleanup crew, not the decision-maker.
