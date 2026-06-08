---
name: figma-design-sweep
description: Sweep a Figma file via the figma-console MCP — capture components, canvases, business rules, FHIR mappings, and produce an HTML inventory artifact. Used when Samer opens a Figma file in Desktop and wants it catalogued for the React port.
when-to-use: User says "sweep this", "check now", "I'm on <file>", "I'm in <file>", "do <file>" while a Figma file is open in Desktop Bridge. Also use when explicitly invoked as /figma-design-sweep.
related-skills: html-artifact (output format), flutter-to-signal-ds-port (downstream consumer of contracts produced here)
---

# Figma Design Sweep — Recurring Process

When Samer opens a Figma file and asks to sweep it, run the standard pipeline below. Every sweep produces one HTML artifact in `~/claude-os/artifacts/`.

## The pipeline (every sweep)

### 1. Detect the file (parallel calls)

Run these 4 in one tool batch:

- `mcp__figma-console__figma_get_status` with `probe: true` — gets file key + active page + selection
- `mcp__figma-console__figma_audit_design_system` — gets Health/Naming/Tokens/Metadata/A11y/Consistency/Coverage scores
- `mcp__figma-console__figma_get_design_system_summary` — gets component categories + counts (cached when possible)
- `mcp__figma-console__figma_get_file_data` with `verbosity: "summary"`, `depth: 1` — gets canvases
- `mcp__figma-console__figma_search_components` with `limit: 25` — gets local components

### 2. Identify canonical vs deprecated canvases

Standard Scrips curation markers (sort canvases by these):
- **CANONICAL** — `(Use this)`, `(Use these)`, `(Live)`, `(In Master)`, `(New UI)`
- **PARTNER** — `HOPE`, `Tabibi`, `AXA` (in name)
- **DEPRECATED** — `(Don't Use)`, `(Old)`, `Back up`, `Not used`, `(Out of Scope)`, `(Paused)`, `Ignore`
- **JIRA TICKET** — `MSP1-<NNN>` in name = shipped + linked to ticket
- **CURRENCY** — `EGP` = Egypt era, `AED` = UAE era
- **POINTER** — canvas named with URL or "Refer to ..." → captures separate file/Confluence
- **SCRATCH** — `Page N`, `Cover`, `=======`, `Test`

### 3. Drill the canonical canvases at depth 2

In one batch call:
```
figma_get_file_data(nodeIds: [canonical_canvas_id, ...], depth: 2, verbosity: "summary")
```

**Token-budget guardrail:** if the response exceeds the model limit, delegate parsing to a `general-purpose` subagent. Give the subagent a self-contained prompt: file path + the canvas list + what to extract (named frames, DEV NOTE verbatim, external URLs, state variants, FHIR-relevant terms). Cap response under 1200 words.

### 4. Capture DEV NOTE text frames VERBATIM

Frames named starting with `DEV NOTE` are embedded business rules. Always quote them verbatim in the artifact — never paraphrase. They contain canonical product spec the engineer/agent must implement.

Look for these patterns:
- Math formulas (invoice calculation, copayment, etc.)
- State machines (status transitions, approval flows)
- Region splits (UK / UAE / Egypt rules)
- External Confluence URLs (`scrips.atlassian.net/wiki/...`) — these are spec pages

### 5. Render components (handle the variant trap)

**TRAP:** `figma_get_component_image` returns `COMPONENT_SET_NOT_RENDERABLE` for component SETS. You must render individual VARIANT nodeIds.

Workflow:
1. From `figma_search_components`, identify the `type` field — `componentSet` vs `component`
2. For `componentSet`, call `figma_get_component_details` first → get `variants[].nodeId` array
3. Render specific variant nodeIds with `figma_get_component_image`
4. Always render the *most variant-rich* set first (highest signal)

Batch renders parallel — typical sweep is 10–20 images.

### 6. State / variant taxonomy

The error message from `COMPONENT_SET_NOT_RENDERABLE` returns the full `availableVariants` list. Use it to extract the variant axis without needing a second call. Example: "Property 1=HPI / Risk / RoS / Docs / A/P / Wrap-up" → these are React state-prop values.

Variant naming conventions in Scrips files:
- **Semantic** (`Default / Selected`, `Collapsed / Expanded`, `View / Edit`, `Empty / Filled`) → real product states → React `state` prop
- **Unlocked alternates** (`Default / Variant2`) → design exploration, not reconciled → ask Samer which is canonical
- **Multi-variant** (5+ variants) → high-signal taxonomy worth identifying

### 7. FHIR mapping (always when clinical)

If the file contains clinical content (Encounter, Patient, Medication, Diagnosis, Vitals, Labs, etc.), produce an explicit FHIR resource map per the knowledge-schema:

| Concept | fhir-primary | fhir-secondary | Code systems |

Standard mappings to reach for:
- Patient → `Patient` + RelatedPerson + Coverage
- Encounter / SOAP → `Encounter` + Composition (note)
- HPI / ROS / PE → `Observation` (vital-signs / symptom group)
- Diagnoses → `Condition` (ICD-10 / SNOMED-CT)
- Medications → `MedicationRequest`, `MedicationAdministration` (MAR), `MedicationStatement`
- Orders (Lab/Rad/Procedure) → `ServiceRequest` + Procedure + DiagnosticReport
- Risk → `RiskAssessment`
- Pain (Wong Baker) → `Observation` with LOINC 38208-5
- Invoice → `Invoice` + ChargeItem + ChargeItemDefinition
- Receipt / Payment → `PaymentReconciliation` + PaymentNotice
- Insurance → `Coverage` + InsurancePlan + Organization
- Contract / Agreement → `Contract`
- Claim → `Claim` + ClaimResponse + ExplanationOfBenefit (flag if missing!)

### 8. Write the HTML artifact

**Location:** `~/claude-os/artifacts/YYYY-MM-DD-<file-slug>-inventory.html` (or `-deep-dive`, `-FULL-inventory` for major files)

**Style stack** (follow `~/.claude/skills/html-artifact.md`):
- Background `#F3F7F8`
- Header band `#1F3888` (navy) with white text
- Card-based body, `border-radius: 10px`, `box-shadow: 0 1px 3px rgba(0,0,0,0.07)`
- Cyan accent `#00B8E3` for nav + links
- Use `<table>` for inventories, `<div class="gallery">` for rendered images
- Light theme — no dark mode (per feedback memory `feedback_no_dark_theme_default`)
- HTML, NOT Markdown (per `feedback_html_default_output`)

**Required sections:**
1. **Headline** — 3–5 callout boxes with critical findings (currency pivots, role splits, new features, FHIR gaps, partner refs)
2. **Stats grid** — Audit scores (Health/Naming/Tokens/Metadata/A11y/Consistency/Coverage) + Components/ComponentSets/Canvases counts
3. **Components gallery** — rendered components with nodeId, size, proposed React name, FHIR binding
4. **Canvas inventory** — table of all canvases with status badge (CANONICAL/DEPRECATED/PARTNER/etc.)
5. **State / variant map** — Figma variants → React state props
6. **FHIR Mapping** — if clinical
7. **DEV NOTES** — verbatim quotes
8. **Open Questions** — anything that needs Samer's call (currency, taxonomy, partner scope)
9. **Port Priority** — numbered actions for Andrew's agent

### 9. Open in browser (NOT preview panel)

Per `feedback_no_launch_panel_references`:
```bash
open ~/claude-os/artifacts/<slug>.html
```
Never mention "the Launch preview panel" — Samer reads in browser.

### 10. Archive S3 image URLs (30-day expiry)

Figma S3 URLs expire ~30 days. For high-value sweeps, also download images locally:
- Destination: `~/scrips-repos/scrips-signal-ds/contracts/visuals/`
- Filename: slugified component name (e.g. `appointment-card-booked.png`)
- Maintain `manifest.json` mapping UUID → url, alt, filename, source_artifact

### 11. Log activity

Append to `~/claude-os/daily-activity-log.md`:
```
[YYYY-MM-DD HH:MM] [HUMAN] [SKILL] figma-design-sweep — <FileName> (<fileKey>) → <artifact-path>
```

## Standard agent rules + traps

- **Figma file size limit alert:** if you see "Alert: reached size limit" in Assets panel, note this in the artifact — the file is at capacity and a successor file likely exists.
- **Library detection:** check Assets panel listing (Cmd+Opt+2 in Figma Desktop). Library names tell you what file the components consume from. Cross-file = use `figma_search_components` with `libraryFileKey` or `libraryFileUrl`.
- **"missing in app" component:** designers sometimes literally label gaps. Flag as backlog signal.
- **"v2" / "v3" prefixes:** newer iteration; older non-versioned frame likely deprecated.
- **"@" naming pattern:** `surface@subsurface@state` is Scrips convention. Maps 1:1 to React route path.
- **"(alt)" suffix:** unreconciled design alternates. Pick canonical before porting — surface in Open Questions section.
- **External URL canvases:** sometimes a canvas IS a URL (Confluence link, MSP-ticket). Treat as pointer, not content.
- **Currency markers:** "EGP" = Egypt era (Jan '21 baseline), "AED" = UAE era (post-June '22). React port must use FHIR Money type.

## What this skill does NOT do

- Build React components (that's `flutter-to-signal-ds-port`)
- Write contract.json files (that's a separate `contract-author` skill yet to be built)
- Fetch Confluence pages (that's Atlassian MCP — separate)
- Modify the Figma file (read-only sweep)

## Output channel

Artifact path goes back to Samer as a markdown link: `[<slug>.html](artifacts/<slug>.html)`. Open it via `open` shell command (not via preview panel).

## After-sweep summary structure (for the chat reply)

Always end the sweep with:
1. One-line file identification: `**File** (fileKey) — N components, M canvases`
2. 3–10 numbered headlines (the most material findings)
3. List of "Still in queue" — files referenced but not yet swept (pointers, partner files, newer versions)
4. Any Open Questions that need Samer's decision before next step
