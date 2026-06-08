---
name: design-to-dev-pipeline
description: "FORCIBLE owner of ALL UI design work (DESIGN-WORK GATE). Use for designing/building/prototyping any component, screen, panel, inspector, card, or UI; 'design it with me'; 'Claude Design'; or graduating a component to Figma. Mandatory rule: create the design in Claude Design (claude.ai/design) via the browser — never hand-build HTML/React mockups as a substitute. Owns the full cycle: ground the DS prop contract → drive Claude Design WITH Samer (continue the existing prototype for consistency; demand PRODUCTION React, not HTML) → pull via Handoff URL → production React importing @scripsteam/scrips-signal-ds → Storybook → wired-in-app (functional gate) → graduate reusable primitives to Figma + Signal DS via signal-ds-graduation / figma-doc-sync."
type: procedure
---

# Skill: design-to-dev-pipeline

**Trigger:** Building a new UI component/screen for a Scrips React app when it should start as a design, become a production React component, get a Storybook story, and land in development. Also when a build surfaces a *missing* UI/UX component. For Samer + the team (esp. Andrew).

**One-line:** Turn intent → Claude Design → production React (importing the published DS) → Storybook → wired into the app → **proven functional**, with the gotchas that cost a day baked in.

---

## FORCIBLE — this skill owns the whole design cycle + graduation

This skill is **forcibly auto-invoked** for ANY design work by the `skill-suggester.py` UserPromptSubmit hook (design / build / prototype / mock-up a component / screen / panel / inspector / UI, "design it with me", "Claude Design", "graduate … to Figma"). When it fires, the **DESIGN-WORK GATE** applies:

- **Claude Design is mandatory.** All UI/component/screen/prototype design is created in **Claude Design (claude.ai/design)** via the connected browser. **Do NOT hand-build the UI in HTML/React/code, and do NOT produce an HTML mockup as a substitute.** Hand-building is allowed only if Samer explicitly says to skip Claude Design.
- **Design WITH Samer.** Open/locate Claude Design in his browser, prompt it, drive it, iterate together — he watches and steers in real time. Screenshot each result back to him.
- **Then graduate.** The design cycle has one owner — this skill — and ends in graduation, never at a screenshot:
  1. **Design** in Claude Design (drive + iterate with Samer).
  2. **Pull code** via the Handoff URL (step 4 below) → production `.tsx` + `.module.css`.
  3. **Graduate to dev** — place + typecheck + Storybook + wire-in + prove functional (steps 5–7 below).
  4. **Graduate to Figma + Signal DS** — for a reusable primitive, hand off to `signal-ds-graduation` (lock as DS-NNN) and `figma-doc-sync` (land in the Figma library, Code Connect). Component-specific one-offs stop at dev.

The pipeline below is that cycle in detail.

---

## Division of labor — Claude Design vs Claude Code (name the layer every exercise)

Claude Design and Claude Code own different SDLC layers. State which layer a given pass is in, so "is this design / product / dev?" never stays muddy (Samer, 2026-06-05).

| Layer | Owner | Deliverable |
|---|---|---|
| **Design / UI components** | **Claude Design** | The visual + interaction design — components at DS levels, states, layout, fidelity. Its "logic" (validation ticks, computed values, a simulated run) is **PRESENTATIONAL — a mock, not real** (e.g. green-on-any-binding; invented "operands resolved"). Treat CD output as the design *spec*, never as working logic. |
| **Product framing** | **Claude Code** | Capability definition, feature flags + tiering, packaging, spec/BRD, catalog placement. |
| **Development** | **Claude Code + backend** | The real logic CD only mocked: evaluators, validation, API wiring, persistence, the sandbox/simulation engine. Usually a backend dependency. |
| **Graduation + verification** | **Claude Code** | Handoff → production React (faithful 1:1 port) → Storybook → wired-in-app → functional gate (behaviour test, not render). |

**Rule of thumb: if it must actually compute, validate, call, or persist → that's development (Claude Code), not design.** Claude Design shows what it looks like + how it behaves on the surface; Claude Code makes it real. A single feature usually spans all four layers — each Claude Design pass addresses only the *design-components* layer; the rest are Claude Code's.

---

## The Claude Design brief template (paste-and-fill — NEVER prompt Claude Design without it)

Every prompt sent to Claude Design MUST carry these four blocks. A bare "design X" prompt is a defect — it produces throwaway HTML and breaks visual continuity.

```
CONTINUITY (so it extends the existing system, not a fresh look):
- This belongs to the EXISTING <project/prototype name> (e.g. "Studio — WorkflowStepNode (MVP)", file signal/<name>.html).
- REUSE the existing structures already in this project: <list the real CSS/components — e.g. pathway-canvas.css, WorkflowStepNode/WorkflowCanvasEdge, rule-condition-row.css>.
- Match the established layout, spacing, type scale, and interaction patterns already on the canvas. Net-new is ONLY <the genuinely new part>. Do not restyle what exists.

OUTPUT CONTRACT (production React, not HTML):
- Emit PRODUCTION React .tsx components, one per primitive, importing from @scripsteam/scrips-signal-ds (ES modules, no window globals).
- Styling via CSS Modules using var(--color-*) / var(--radius-*) / var(--motion-*). ZERO hex literals. primary = #005FD4 (DS-015); never #0076F8/#007AFF/#00B8E3/#5C41B5/#8B5CF6.
- Use the REAL DS prop signatures below — do not invent props.
- The component must be Storybook-ready (named export, typed props interface) and Figma-graduation-ready (clean variant axes, no hard-coded content).
- TAXONOMY & NAMING (so it graduates as a real DS asset, not an orphan): declare each component's Signal DS LEVEL — component | card | block | template | frame (Tokens = L0 foundation). Clinical surfaces are FHIR-resource-named (VitalCard, LabValue, AllergyChip, ObservationCard, MedicationActiveRow…); generic primitives stay generic (Button, Select, Tag). PascalCase, no DS/Signal/Scrips/atom affixes. "Observation panel" → an Observation-bound card or block, named per FHIR.

DS PROP CONTRACT (verified from the .d.ts — paste the real shapes):
- <e.g. StatusChip {semantic, tone}; Button variant=primary|secondary|tertiary|destructive; Select {options:{label,value}[], onChange}>

SPEC / BRIEFING (so the asset is documentable on graduation):
- Component name(s) + one-line purpose each.
- Props/variants matrix (the axes that become Figma variants + Storybook stories).
- States to render (default, empty, loading, error, open/active…).
- The exact scenario to show in the canvas (real content, e.g. "render OPEN with a form mid-edit").
```

Fill it from steps 1–2 below before driving Claude Design in step 3. The CONTINUITY block is what keeps every iteration on the same design language; the OUTPUT CONTRACT + SPEC blocks are what make the result a graduatable production asset rather than a screenshot.

## The pipeline (repeatable)

1. **Ground the contract BEFORE designing.** Read the exact prop signatures from the installed package — `~/scrips-repos/scrips-react/node_modules/@scripsteam/scrips-signal-ds/dist/atoms/*/*.d.ts` (and `molecules/*`). Never guess an API. Capture: real exports, each component's props + variant axes (e.g. `Tag` has NO variant — it's `{children}`; state colour lives on `StatusChip {semantic, tone}`; `Button` variants are `primary|secondary|tertiary|destructive`, no `ghost`; `Select`/`Segmented` are `{options:{label,value}[], onChange:(value)=>void}`; `EmptyState.icon` required).
2. **Token contract = the app's real CSS vars.** scrips-react globals live in `src/tokens/tokens.css` (imported in `main.tsx`): `--color-*` / `--radius-*` / `--motion-*` / `--ease-functional`. There is **no `--semantic-color-*`** and the DS package ships **no `tokens.css`/`fonts.css`** (atoms self-style via runtime CSS-in-JS). Components must NOT import a global token sheet. Zero hex literals in CSS. Never the rejected colours (#0076F8 #007AFF #00B8E3 #5C41B5 #8B5CF6); primary is #005FD4 (DS-015).
3. **Drive Claude Design** (claude.ai/design, the connected "Signal Design System (Scrips)" project) with: the verified prop signatures + the token contract + "emit **production `.tsx`** importing `@scripsteam/scrips-signal-ds` (ES modules, no window globals), CSS Modules using `var(--color-*)`, no literals." Improve the *input* when it guesses — feed it the real `.d.ts` shapes; re-emit.
4. **Pull the code via the Handoff URL (the MCP browser can't download to disk).** Share → "Handoff to Claude Code" → copy the `https://api.anthropic.com/v1/design/h/<token>` URL → `curl -sSL -o bundle.tar.gz "<URL>"` (gzip tarball, no auth) → extract → the production `.tsx` + `.module.css` are under `project/studio/components/`.
5. **Place + typecheck.** Copy into the repo module. Add deps (canvas = `@xyflow/react` v12 for React 19 — **named** `ReactFlow` import, Node/Edge data as `type`, `NodeProps<Node<Data>>`, `nodeTypes`/`edgeTypes` `as NodeTypes`). `npm run typecheck` (`tsc -p tsconfig.app.json --noEmit`) → filter to your module → **zero errors**.
6. **Storybook story** per component (`Studio/<Name>`, ≥2 states) — for isolated visual review (Storybook reachable at `localhost:6007` via the `scrips-react-storybook` launch config).
7. **Wire into the app + PROVE IT WORKS.** Storybook/render is NOT done. See the functional gate below.

---

## The functional gate (the lesson — non-negotiable)

**"Compiles + renders + uses the DS" ≠ delivered.** A facade renders perfectly and does nothing (cosmetic trigger dropdown, read-only inspector, no persistence, no undo). To call a component/feature done it must be **functional + wired + demonstrable in the running app**:
- A **behaviour test** (vitest) proves the interaction: editing updates state, onChange fires, serialize↔deserialize round-trips *with edits*, the action actually persists. Not a render assert.
- An **interactive smoke** in the running app/Storybook: drag/edit/save and observe the state change (screenshot it).
- If it talks to a backend, the call hits a real endpoint (or a clearly-marked, removable mock — never a silent mock masquerading as real).

Verification must check **what it does**, not that it mounted.

---

## Fidelity gate (Claude Design IS the spec — production must match it, not approximate it)

**The recurring failure (Samer, 2026-06-05):** Claude Design's output is more polished than the production port — icon choice, icon placement, spacing, micro-detail. Production comes out subpar because it gets **rebuilt by eye** instead of **ported faithfully**. The whole point of Claude Design is lost if production reinterprets it.

Rules:
1. **Claude Design's Handoff `.tsx` is the source, not the screenshot.** Graduate by porting the actual emitted code (step 4), translating its classes→DS tokens and its icons→DS icon components **1:1**. Never rebuild the layout from a screenshot — that's where the polish dies.
2. **Icons are named, never improvised.** The brief must specify the exact icon for every element (by name, from the DS/lucide set Claude Design uses). The port uses the *same* icon, same size, same position. If the DS lacks an equivalent, flag it — don't silently substitute a worse one.
3. **Spacing/size/colour come from tokens Claude Design already used** — read its `.module.css`/inline styles and map each value to the matching `var(--*)`. Don't round to "close enough."
4. **Pixel-diff gate before "done":** screenshot the production render (Storybook) and Claude Design's canvas at the same size, side by side. They must visually match — same density, same icon placement, same hierarchy. A material visual gap = not done; fix the port, don't ship the approximation.
5. **If production *can't* match** (a DS limit, a missing icon, a token gap), that's a **Signal DS gap to file** (signal-ds-graduation), not a reason to degrade the design.

The brief carries the spec *in*; this gate keeps the spec intact *out*.

### Re-derivation is NOT a port (the 2026-06-05 drift — twice)
A "port" that re-authors thin components is a facade, even with green tests. Two tells, both caught only by Samer:
1. **Structural diff, not self-grade.** Compare the port's element inventory + size against the prototype. If the prototype's `inspector-panels.jsx` is ~1,200 lines (node detail · assignee · milestones dropdown · schedule · condition editor · 31 selects) and the port is ~450, it dropped the fidelity — that's drift, not a port. Convert the prototype `.jsx`/`.css` **verbatim** (preserve every field, dropdown, token, icon); do not "DS-reconcile into a simpler version."
2. **The verifier opens BOTH and diffs, element by element** (node-click detail, dropdowns, chrome, colors, icons) — the main agent does this, never relays a sub-agent's "N/N pass." A self-graded pass on a re-derived model is exactly the facade the functional gate is meant to stop (`feedback_self_grading_goodhart_broken`).
3. **Reconcile with already-delivered code.** If the app already ships `NodePalette`/`PublishControl`/`StudioShell`, extend them — never build a parallel thin studio that ignores delivered work.

---

## Signal DS taxonomy (what Claude Design must emit + how it graduates as a library asset)

**Why this matters (Samer, 2026-06-05):** if Claude Design output isn't named/levelled in the DS's own vocabulary, it can't graduate to Figma as a proper library asset — it lands as an orphan. The DS has a **locked 6-level hierarchy** (DS-002, DS-008 — verify upstream in `~/scrips-repos/scrips-signal-ds/DESIGN-STATE.md` + `decisions/DS-008-hierarchy-vocabulary-lock.md` before quoting):

| Level | Term (closed enum) | What it is |
|---|---|---|
| L0 | `Tokens` | colour/space/radius/motion/type — foundation, imported by all |
| L1 | `component` | reusable UI primitive (Button, Select, Tag, Icon). Generic-named. |
| L2 | `card` | typed display of ONE FHIR resource (VitalCard, LabValue, AllergyChip), xs–xl sizes |
| L3 | `block` | 4-zone anatomy (Header/Content/AI/Footer), anchored to a FHIR ResourceType |
| L4 | `template` | selects + sequences blocks for one clinical/financial task |
| L5 | `frame` | surrounding chrome (nav, sidebar, motion budget); hosts templates |

Retired terms: `atom`, `primitive`, `molecule`, `organism` — do NOT use; the enum is exactly `component | card | block | template | frame`.

**FHIR-semantic naming (clinical surfaces only):** cards/blocks that display clinical data are named by their **FHIR ResourceType**, not descriptive English. So "observation panel" → an **Observation-bound `card`/`block`** (e.g. `ObservationCard` / `VitalCard` / `LabValue`). Generic UI primitives (`component`) stay generic. PascalCase, no `DS`/`Signal`/`Scrips` affixes. Each clinical component declares its `fhir.primary` ResourceType (see `contracts/*.json`).

**Graduation mapping (DS-level → Figma → contract), locked sequence (DS-010):**
`spec (md) → Figma frame (Samer-approved) → React → design-map.json entry`. A component is only **LOCKED** when its `design-map.json` `figmaNodeId != null` and resolves; otherwise it stays `experimental`. Graduate via `signal-ds-graduation` (DS-NNN + contract) + `figma-doc-sync` (frame + design-map). New clinical component → file a contract (`contracts/<Name>.json` with `hierarchyLevel`, `scope`, `fhir`, `decisionRefs`).

**✅ Canonical Figma file (resolved 2026-06-05):** graduate into **`qrKkhVA3eRXn4hxOlw13pS`** ("Scrips Design System" · 165 components + 102 token variables · Blue-Depth). Confirmed by two authorities: `tokens/design-map.json#designSystemFileKey` (= qrKkhV) + Samer's 2026-05-31 re-anchoring (PROD-964). `IzvV9OCSeIQ3yKS3aNpYOJzL` is **retired** (was the April v2.2 file). The stale `DESIGN-STATE.md` DS-007 that still named IzvV9 was amended via scrips-signal-ds PR #39. figma-console is the authoritative live surface — verify the file is open there before graduating.

---

## Missing-UI handoff (for the team)

When a build needs a UI component the DS doesn't have:
1. Confirm it's genuinely absent (grep the package `.d.ts`).
2. Design it in Claude Design from tokens (steps 1–4), or — if it's a net-new DS primitive — PR it into `Scripsteam/scrips-signal-ds` (not into consumer domain code).
3. Bring back as production `.tsx`, Storybook story, then wire + functional-gate it.
4. The interactive Claude Design browser is **not headless** — the design step needs a human/session driving it; a background workflow can't do step 3. So: workflows build against *existing* DS components and **flag** missing UI for an interactive design pass.

---

## Provenance
Origin: 2026-06-01 — Samer asked to codify the design→code→Storybook→dev loop after the Pathway Studio build, and to have a skill so the team (Andrew) can use it. Hard lessons folded in: read `.d.ts` before designing (don't guess APIs), the real `--color-*` token contract, `@xyflow/react` v12 for React 19, the Handoff-URL curl bypass for the sandboxed browser, and the functional gate (a render is not a delivery). See `feedback_no_fiction_ports`, `feedback_prototype_ds_first`, `feedback_smoke_test_before_done`.
