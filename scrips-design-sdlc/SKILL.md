---
name: scrips-design-sdlc
description: "Scrips Design SDLC — repeatable design process with AI validation gates. Use when designing new screens, components, cards, blocks, templates, or frames. Also use whenever quoting a canonical DS fact (color, token, decision, type identifier) in chat / Slack / artifact / commit — Phase 0 below is mandatory before stating any DS canonical."
trigger: "design, UX, new screen, new component, new card, design review, design validation, design system, token, color, palette, DS canonical, what color, what's the token"
---

# Scrips Design SDLC

## When This Skill Activates
- User asks to design a new screen, component, card, block, template, or frame
- User asks to review a design against the design system
- User asks to validate a design before shipping
- **You are about to quote a canonical DS fact** (color hex, token name, locked decision DS-NNN, type identifier, motion duration, surface name) — Phase 0 below is mandatory

---

## Phase 0: VERIFY CANONICAL (mandatory before any DS statement)

**Hierarchy of authority** (full spec: `~/.claude/context/signal-ds-authority.md`, auto-loaded every session):

| Tier | File | Authority |
|---|---|---|
| 1. Tokens (UPSTREAM) | `~/scrips-repos/scrips-signal-ds/tokens/design-tokens.ts` | Wins all conflicts |
| 2. State doc | `~/scrips-repos/scrips-signal-ds/DESIGN-STATE.md` | Locked DS-NNN decisions |
| 3. Contracts | `~/scrips-repos/scrips-signal-ds/contracts/*.json` | Per-component specs |
| 4. Agent contract | `~/scrips-repos/signal-portal/llms.txt` | Cache — must match upstream |
| 5. Portal HTML | `~/scrips-repos/signal-portal/index.html` + `cards.html` | Demos — may have drift bugs |
| 6. Vault ADRs | `Scrips Vault/06-decisions/design-system/*.md` | Locked decisions — but if they carve out an exception that contradicts tokens, surface the conflict |

**Pre-statement gate:**
1. Read `design-tokens.ts` — verify the value/concept exists upstream.
2. Read `DESIGN-STATE.md` — verify no locked decision contradicts.
3. THEN consult llms.txt / portal HTML / ADR for the worded version.
4. If steps 1–2 disagree with downstream, **flag the conflict to Samer before quoting**. Don't propagate the downstream silently.

**If you find drift,** log it in the activity log + propose either an amendment (with dated `[HUMAN]|[CLAUDE]` provenance per `feedback_canonical_doc_gap_provenance`) or a new superseding ADR. Never leave the conflict unflagged.

**Concrete example (2026-05-13 — the trigger for this Phase 0):** `llms.txt §5` + ADR `2026-04-07-card-type-variants-locked-html-prototype-sds-v22.md` both said "purple #8B5CF6 is the CardInsight type identifier." `design-tokens.ts:207` said `// Purple (Sasha) — never approved`. `DESIGN-STATE.md:23` said `Purple: REJECTED`. Downstream had drifted. Phase 0 would have caught it.

---

## Phase 1: INTENT
Before designing anything, answer:
1. **Who is this for?** (role from JTBD matrix: clinician/nurse/patient/admin)
2. **Write one sentence:** "The [role] needs to [job] in [time constraint]"
3. **What clinical workflow does this serve?** Map before screen.
4. **What FHIR resources are involved?** (check fhir-design-system/ in Obsidian vault)
5. **What can't fail?** (identify can't-fail moments from Commandment #2)

## Phase 2: COMPOSE
1. **Which hierarchy level?** Card / Block / Template / Frame
2. **What mode × modality?** capture|display|edit|review × keyboard|voice|structured
3. **What size variants?** xs→xl, justify each
4. **What existing components can be reused?** (check design-system-complete.md)
5. **What's new?** Only build what doesn't exist.

## Phase 3: DESIGN
1. **Tokens only** — no hardcoded values. Reference design-system-tokens.md.
2. **Blue Depth color system** — no decorative color ever.
3. **Status colors = clinical meaning only:**
   - Red `#CD3232` = danger, allergy, critical
   - Amber `#E5A000` = warning, borderline, pending
   - Green `#41AE55` = normal, resolved, completed
4. **Progressive disclosure** — 30-second rule on every element
5. **Keyboard-first**, mouse-optional
6. **Stress test:** "Doctor mid-conversation, gets interrupted, comes back 30 seconds later. Can they pick up?"

## Phase 4: VALIDATE
**Nothing ships without ALL checks passing:**
- [ ] Role identified — who uses this and what's their job?
- [ ] Can't-fail moments identified — what errors are unacceptable?
- [ ] Workflow mapped — what happens before/after this screen?
- [ ] Four questions answered — what does this mean, good/bad, what to do, who to contact?
- [ ] Stress-tested — works with interruptions, one hand, time pressure?
- [ ] Color meaningful — no decorative red/green/yellow?
- [ ] Token compliant — no hardcoded colors, spacing, or typography?
- [ ] Hierarchy conformant — uses v2.2 terms only (Card, Component, Block)?
- [ ] FHIR mapping present — every data field maps to a resource?
- [ ] Role-based visibility defined?
- [ ] WCAG AA — 4.5:1 contrast, focus indicators, screen reader?
- [ ] Keyboard navigable — all actions reachable without mouse?
- [ ] Progressive disclosure — summary first, detail on demand?
- [ ] Click count documented — how many clicks per job?

## Phase 5: BUILD
1. Write CardRegistry spec (YAML) if it's a new card
2. Figma component with all variants
3. React/Tailwind implementation with Storybook story
4. Screenshot validation

## Phase 6: REVIEW
1. Visual diff against inspiration (Linear/Vercel/Mercury)
2. Anti-pattern check — does NOT look like Epic/Cerner/DrChrono
3. Samer sign-off on clinical accuracy
4. Promote status: [DESIGNED] → [IMPLEMENTED]

---

## AI-Specific Checks and Balances
When AI (Claude) is generating design:

| Risk | Filter |
|---|---|
| AI invents colors | Any hex not in design-system-tokens.md = **BLOCKED** |
| AI uses wrong hierarchy terms | "Widget", "Molecule", "Organism" = **BLOCKED** |
| AI over-designs | 30-second rule gate: justify every element |
| AI misses clinical safety | Can't-fail moments checklist mandatory |
| AI hallucinates FHIR mappings | Cross-reference against fhir-design-system/ |
| AI creates inaccessible design | WCAG AA contrast check on every color pair |
| AI ignores role context | JTBD sentence required — no screen without it |
| AI drifts from brand | Visual diff against Linear, Mercury references |
| Design works in isolation | Workflow map required — no orphan screens |

---

## Design-to-Dev Feasibility Gate
Before committing any design decision, verify:
- **Can this be built with shadcn/ui primitives?** If custom, flag it.
- **Does the data fit the card size?** If CardHbA1c at xs needs 4 elements but only fits 2, flag it.
- **Does the FHIR mapping exist in the backend?** If not, flag it.
- **Is the layout achievable with CSS grid/flex?** If exotic, flag it.

---

## Quick Reference

### Design Tokens
- Primary: `#0076F8` | Depth: `#004795`
- Text: `#151B20` (primary), `#809099` (muted), `#AFBAC0` (hint)
- Error: `#CD3232` | Warning: `#E5A000` | Success: `#41AE55`
- Background: `#F7F9FA` | Card: `#FFFFFF` | Sidebar: `#0D1B4B`
- Font: Inter (web), Roboto (mobile)
- Radius: 8px default | Spacing: 4px base

### v2.2 Hierarchy
Grid → Atom → Component → Card[xs→xl] → Block → Template → Frame → Layout

### Card Sizes
| Size | Width | Capture? |
|---|---|---|
| xs | ~120px | Display only |
| sm | ~240px | Display only |
| md | ~340px | Keyboard capture (minimum) |
| lg | ~480px | Full capture |
| xl | ~640px+ | Power mode |

### Rejected Colors (NEVER USE)
`#5C41B5` `#5FC6D4` `#00B8E3` `#EE6464` `#65D24A` `#FCC001` `#007AFF` `#061AB3`

### 12 Commandments (summary)
I. Role-based JTBD | II. Can't-fail moments | III. Workflows before screens
IV. What happens next (4 questions) | V. Build for stress | VI. Dashboards for decisions
VII. Privacy as UX | VIII. Color = meaning only | IX. 30-second rule + trust before density
X. Consumer-grade craft | XI. Click metric | XII. AI source attribution
