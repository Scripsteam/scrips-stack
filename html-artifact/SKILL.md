---
name: html-artifact
description: Use when generating any artifact for Samer to READ (briefings, plans, reports, code reviews, exploration grids, research synthesis, prototypes, custom editors with copy-as-prompt buttons). Defines where files go, how to share, visual taste, and the round-trip pattern. Default output format is HTML — see memory `feedback_html_default_output.md`. Don't invoke for vault-class .md (ADRs, session memos, decisions), code/config files, Confluence, Slack, or email — those keep their native formats.
---

# html-artifact

## THREE NON-NEGOTIABLES (read before writing a single line of HTML)

**1. Use the canonical boilerplate.** Copy the CSS block from the "CANONICAL HTML BOILERPLATE" section below verbatim. Do not start from scratch. Do not invent colors. The only correct primary blue is `#005FD4`. Everything else is wrong.

**2. Diagrams before prose.** Any sequence, hierarchy, comparison, or distribution must be an inline SVG or CSS diagram. If you are about to write 3+ sentences explaining a structure, stop and draw it instead. Prose supports diagrams; diagrams do not support prose.

**3. Comment rail on every consumption artifact.** Left sidebar, fixed, localStorage persistence, copy-as-prompt at the bottom. Not optional. Not a "nice to have." Every brief, plan, ADR render, report.

If you cannot commit to all three before writing, read the full skill first.

## When to use

Default to HTML whenever you'd otherwise produce a multi-section Markdown document for Samer to read or share.

Use cases (from Thariq, refined for Samer):
- **Reports & research** — synthesis, retros, weekly reviews, status, incident postmortems → SVG diagrams + executive summary on top + drill-down sections.
- **Specs & plans** — BRDs (working drafts), implementation plans, exploration → TOC + section anchors + mockup placeholders + open-questions callout.
- **Code review & PR explainers** — render diff with inline annotations, severity color coding, files-touched sidebar.
- **Multi-option exploration** — N approaches in a grid, each card labeled with its tradeoff.
- **Custom editors** — drag-to-reorder, picker, tuner, side-by-side editor — purpose-built single-use, ALWAYS ends with a "copy as JSON / markdown / prompt" button so Samer can round-trip the result back into Claude Code.

Anti-cases (stay Markdown / native):
- ADRs, session memos, decisions, person/org files, project _index, executive summaries → vault `.md` per knowledge-schema (Obsidian + Dataview)
- CLAUDE.md, skills, memory → `.md`
- Code, config, structured data → native format
- Confluence (use Confluence storage format) / Slack (use Slack mrkdwn) / Email (use plain or HTML email body, not a file)
- Jira ticket bodies → Jira ADF

## Where to save

| Scope | Location |
|---|---|
| Personal / scratch / one-shot for Samer | `~/claude-os/artifacts/<YYYY-MM-DD>-<slug>.html` |
| Tied to a vault decision/project (companion to a .md) | `~/claude-os/artifacts/<YYYY-MM-DD>-<slug>.html` + cross-link from the .md |
| Shareable to team / advisors / vendors | Deploy to Vercel — see "Sharing" below |
| Inside a worktree branch (PR-bound artifact) | `<worktree>/artifacts/<slug>.html` |

`~/claude-os/artifacts/` is the canonical local home. If it doesn't exist, create it on first write.

NEVER put HTML artifacts in:
- The Obsidian vault (vault is Markdown by design — knowledge schema, Dataview, graph)
- OneDrive (sync conflicts, locks)
- Inside another repo's source tree unless the artifact is part of that repo's deliverable

## Sharing

Three tiers:

1. **Local-only**: `open ~/claude-os/artifacts/<file>.html` — opens in browser, no upload.
2. **Shareable link** (default for anything Samer wants to send to a person): deploy to Vercel.
   - Initial setup (one-time, Samer to confirm): create `claude-artifacts.vercel.app` Vercel project pointing at `~/claude-os/artifacts/`. Until that's set up, fall back to `signal-portal/public/artifacts/<slug>.html` and the existing `signal-ds.vercel.app` deployment.
   - Per artifact: `vercel deploy --prod` from the artifacts dir, return the URL.
3. **Confluence-shared** (external audience — vendors, partners, RFPs): per memory `feedback_centralize_knowledge_in_confluence.md`, the delivery surface is Confluence with page-level external sharing. HTML can still be the AUTHORING source — render as Confluence storage format on copy-paste, or attach the HTML file.

Default channel for the link: Slack DM to Samer (UANT64XRQ in CoS Briefing workspace per memory `feedback_n8n_slack_user_id.md`).

### Sharing gotchas (learned 2026-05-29 — apply to every shared file)

1. **A shared HTML *file* is a frozen snapshot.** When you send the file (AirDrop / WhatsApp / email / Drive-as-file), the recipient gets a static copy fixed at send time. Editing the source afterward does NOT propagate — the recipient keeps the old version. After any post-share fix, the artifact must be **re-sent**. Always tell Samer this explicitly; never imply a fix reaches an already-delivered copy. (A live Vercel *link* does update — but that's the only tier that does, and family/personal-medical artifacts are local-only, never hosted.)
2. **Verify render outside Chrome before sharing.** A file that renders in the authoring Chrome can break in a recipient's viewer (mobile app, mail/Drive preview, sanitised HTML). The classic breaker: SVG drawn via `<symbol>` + `<use href="#…">` indirection to a hidden `<defs>` block — it vanishes when shared. **Inline brand/icon SVGs directly** at each occurrence with their own `xmlns` + `viewBox` + explicit `fill` (no `<use>`, no `currentColor`/`var()` dependency, no CDN). Confirm with a headless screenshot (`Google Chrome --headless=new --window-size=W,H --screenshot=out.png file://…`) or by AirDropping the file to a phone — *that* is the recipient's path.

## Slides-format default (mandatory)

**Default layout = presentation / slides, not long-scroll page.** See `feedback_html_presentation_format.md`.

- Each `<section>` is one viewport: `min-height: 100vh; scroll-snap-align: start`
- Container: `scroll-snap-type: y mandatory; overflow-y: scroll; height: 100vh`
- Slide counter (top-right, fixed): "03 / 18" with progress dots
- Title slide → content slides → closing slide
- One memorable takeaway line per slide, not a paragraph
- Print-friendly: each slide page-breaks for PDF

**Long-form is opt-in.** Use only for reference docs the reader scrolls through searching for specifics (component catalogs, full ISO registers, audit trails). When unclear, ask once. Then ship slides.

## Visual-first (mandatory)

**Default to visual. Prose is the fallback.** Any quantitative, structural, sequential, or relational content MUST be expressed as a CSS or inline-SVG diagram before being expressed as prose. See `feedback_visualize_long_text.md`.

**Always visualize:**
- Sequences → timeline · swim lane · flow diagram · step ladder
- Hierarchies → tree · org chart · nested boxes
- Distributions / tallies → CSS bar chart · donut · stacked bar
- Comparisons → side-by-side cards · matrix · quadrant
- Lifecycles / state machines → box-and-arrow diagram (request lifecycle, agent flow)
- Thresholds / scales → horizontal scale with labeled bands
- Cost composition → stacked bar · treemap
- Process flows → BPMN-lite (rectangle = action, diamond = decision)

**The test:** if a section has 4+ consecutive sentences explaining *what the structure is*, it needs a visual. The prose then reduces to the takeaway sentence + the visual.

**Implementation rules:**
- CSS (flexbox/grid + borders + fills) for boxes, swim lanes, timelines, simple flows
- Inline SVG for charts, curves, precise geometry
- Never link to external image generators
- All visuals use Signal DS tokens (no hand-picked values)
- Every visual carries a 1-line caption ("what to look at first")

**For Scrips artifacts:** combine with `~/.claude/skills/scrips/voice/SKILL.md` (which already says "lead with the diagram, support with prose").

## Visual taste

Hard rules from memory:
- **Light theme by default** (`feedback_no_dark_theme_default.md`) — light backgrounds, strong typographic hierarchy, card-based ADHD-friendly layout. Dark mode is opt-in only.
- **No internal-only Scrips names in external artifacts** (`feedback_no_internal_names_in_external_artifacts.md`).
- **No "Reveal" on external surfaces** — translate to "Story / Story stage" (`feedback_avoid_reveal_term_external.md`).
- **Consumer surface is "consumer / citizen", not "patient app"** unless clinical-episode context (`feedback_consumer_citizen_over_patient.md`).
- **Scrips legal name is "Scrips Inc. Ltd."** — only in copyright/trademark/contract contexts (`feedback_scrips_legal_name.md`).
- **No fabricated citations** (`feedback_no_fabricated_citations_in_pitch_artifacts.md`) — if you cite, audit it; if you can't audit it, don't cite.
- **Brand fonts: DS-017 (locked 2026-05-16).** Latin = Inter Variable, Arabic = Readex Pro Variable, Mono = JetBrains Mono Variable. Self-hosted at `signal-ds.vercel.app`. **DO NOT link the CDN** — artifacts must be self-contained (zero network). Use the system font stack from the canonical boilerplate: `-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`. If brand fonts are critical for a given artifact, base64-embed `@font-face` — do not link the CDN URL.
- **Brand primary blue: `#005FD4`** (DS-015, locked 2026-05-16). The old `#0076F8` is REJECTED — failed WCAG AA at 4.25:1.

## CANONICAL HTML BOILERPLATE — copy verbatim, do not rewrite

**This block is a contract, not an example.** Copy it exactly. Do not substitute variable names, hex values, or font stacks. Every HTML artifact starts from this template. The only things you fill in are `<title>`, `.meta` content, and the `<main>` body.

Rationale: inconsistent colors and fonts across artifacts is a regression. The gate hook (`html-write-gate.py`) will inject these token values at write time regardless — start from here to avoid the correction round-trip.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><!-- fill in --></title>
  <style>
    :root {
      --bg:          #fafafa;
      --surface:     #ffffff;
      --ink:         #1a1a1a;
      --ink-muted:   #5a5a5a;
      --border:      #e5e5e5;
      --accent:      #005FD4;   /* DS-015 locked 2026-05-16 — ONLY correct primary blue */
      --accent-soft: #e6f1ff;
      --good:        #047857;
      --good-soft:   #d1fae5;
      --warn:        #b45309;
      --warn-soft:   #fef3c7;
      --danger:      #b91c1c;
      --danger-soft: #fee2e2;
      --code-bg:     #f5f5f5;
      --maxw:        760px;
      /* REJECTED primaries — never use: #0076F8 #0082CA #00B8E3 #007AFF #5C41B5 */
    }
    *, *::before, *::after { box-sizing: border-box; }
    body {
      margin: 0; padding: 32px 24px;
      background: var(--bg); color: var(--ink);
      font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    }
    main  { max-width: var(--maxw); margin: 0 auto; }
    h1    { font-size: 28px; line-height: 1.2; margin: 0 0 4px; letter-spacing: -0.01em; }
    h2    { font-size: 20px; margin: 32px 0 8px; letter-spacing: -0.005em; }
    h3    { font-size: 13px; margin: 20px 0 6px; color: var(--ink-muted);
            text-transform: uppercase; letter-spacing: 0.06em; }
    .meta { color: var(--ink-muted); font-size: 14px; margin-bottom: 24px; }
    .card { background: var(--surface); border: 1px solid var(--border);
            border-radius: 10px; padding: 20px; margin: 12px 0; }
    .grid { display: grid; gap: 12px;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
    .pill { display: inline-block; padding: 2px 10px; border-radius: 999px;
            background: var(--accent-soft); color: var(--accent);
            font-size: 12px; font-weight: 500; }
    .pill.good    { background: var(--good-soft);   color: var(--good); }
    .pill.warn    { background: var(--warn-soft);   color: var(--warn); }
    .pill.danger  { background: var(--danger-soft); color: var(--danger); }
    .callout { border-left: 3px solid var(--accent); padding: 12px 16px;
               background: var(--accent-soft); border-radius: 6px; margin: 16px 0; }
    .callout.warn   { border-color: var(--warn);   background: var(--warn-soft); }
    .callout.danger { border-color: var(--danger); background: var(--danger-soft); }
    code, pre { font: 14px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
                background: var(--code-bg); border-radius: 4px; }
    code { padding: 1px 6px; }
    pre  { padding: 12px 16px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; }
    th, td { padding: 8px 12px; border-bottom: 1px solid var(--border);
             text-align: left; vertical-align: top; }
    th { font-size: 13px; color: var(--ink-muted); font-weight: 600; }
    a  { color: var(--accent); }
    button { background: var(--accent); color: white; border: 0;
             border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }
    @media print { body { background: white; padding: 0; }
                   .card { border: none; padding: 0; } }
  </style>
</head>
<body>
  <main>
    <h1><!-- title --></h1>
    <div class="meta"><!-- YYYY-MM-DD · class · [HUMAN]|[SKILL]|[SCHEDULED]|[AGENT] --></div>
    <!-- content -->
  </main>
</body>
</html>
```

For product-related work (Signal DS feature, design exploration), use Signal DS tokens and components from `~/scrips-repos/signal-portal/` instead of the default stack.

## Required structure

Every HTML artifact:
- Title + date + class + attribution `[HUMAN]|[SKILL]|[SCHEDULED]|[AGENT]` in the `.meta` line
- Top-of-page summary (one paragraph or 3-bullet TL;DR) before drilling in
- Mobile-responsive viewport meta
- Print-friendly `@media print`
- For plans / exploration / editors: a copy-as-prompt button at the bottom that round-trips the contents back into a Claude Code-pasteable form

### MANDATORY for any analytical artifact (quotes numbers, costs, metrics, dates, counts, status)

The final slide/section MUST be a **Sources & confidence** block — a table mapping every load-bearing number to its provenance tier and source. This is non-negotiable for reports, briefs, financial/cost analysis, retros, audits, or anything where a wrong number misleads.

```html
<h2>Sources &amp; confidence</h2>
<table>
  <thead><tr><th>Claim</th><th>Value</th><th>Tier</th><th>Source (command / screen)</th><th>Re-verify by</th></tr></thead>
  <tbody>
    <tr><td>April Profile 1 bill</td><td>$4,760</td><td>PRIMARY</td><td>invoice G156842392</td><td>open the PDF</td></tr>
    <tr><td>May Profile 1 projection</td><td>$2,904</td><td>DERIVED</td><td>Prod $2,690 + IHL $47 + $29</td><td>re-run profile cost query</td></tr>
  </tbody>
</table>
```

Tiers: **PRIMARY** (live query of generating system) · **DERIVED** (arithmetic on primary, show inputs) · **FORECAST** (projection — never shown as actual) · **CACHE** (downstream copy, reconcile first) · **ASSUMED** (your inference, lowest trust). Full protocol: `~/.claude/skills/source-of-truth-discipline.md`. Filling this table IS the validation pass — a row reading "current cost / FORECAST" is a caught bug before the reader sees it.

## Agent-readable embed (hybrid artifacts only)

When the artifact will plausibly be re-read by a future Claude session — long-lived plans, ADR-adjacent decisions, shared specs — embed a JSON-LD block in `<head>` so an agent can extract metadata cheaply without parsing the rendered page:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "<title>",
  "datePublished": "<YYYY-MM-DD>",
  "author": "Claude (agent: claude-code, attribution: [HUMAN]|[SKILL]|...)",
  "about": ["<topic>", "<topic>"],
  "isPartOf": "<vault decision/project slug if linked>",
  "claudeOSClass": "<plan|report|review|exploration|prototype|editor>",
  "tags": ["domain-*", "artifact-*", "status-*"]
}
</script>
```

Skip for one-shot artifacts (a single brief, a throwaway editor) — the JSON-LD adds noise without payback.

Do NOT inline a full `<script type="text/markdown">` mirror of the body — that IS dual-write. The JSON-LD captures structured metadata; the body stays HTML; if a vault index is needed, write a separate `.md` per knowledge-schema and cross-link.

## Copy-as-prompt pattern

```html
<button onclick="navigator.clipboard.writeText(document.getElementById('export-payload').textContent).then(() => this.textContent = 'Copied ✓')">Copy as prompt</button>
<pre id="export-payload" hidden>
[The actual prompt text — bullet list of decisions, picked option, open questions, etc.]
</pre>
```

## LOCKED PATTERNS — do not improvise

These are the patterns that have been corrected multiple times. Apply verbatim. Do not invent variants. Do not freelance the colour, do not edit the wordmark paths, do not move the comment rail.

### Scrips wordmark — embed verbatim, never edit

The canonical wordmark SVG lives at `~/scrips-repos/signal-portal/scrips-logo-blue.svg`. Always read the file and embed the **entire** SVG block (including the 7 internal `<path>` elements) verbatim into the artifact. Never copy a subset of paths. Never shorten path `d=` data. Never replace the colour. The wordmark is the SVG; it is not interpretive.

```html
<!-- Embed the file contents of ~/scrips-repos/signal-portal/scrips-logo-blue.svg here, complete -->
<svg width="..." height="..." viewBox="0 0 309 122" ...>
  <!-- all 7 paths exactly as in the source file -->
</svg>
```

Caught at least 3 times (2026-05-18 wordmark decoration · 2026-05-20 path truncation in ADR-006 slides). The wordmark is a contract, not a sketch.

### Brand primary blue is `#005FD4` (DS-015, 2026-05-16)

**REJECTED** primaries (never use as `--primary`, brand surface, or chip colour):
- `#0076F8` — old DS-001 value; WCAG AA fail (4.25:1). Superseded.
- `#0082CA` — wordmark fill colour only. NOT a brand primary token.
- `#00B8E3`, `#007AFF`, `#5C41B5`, `#0046A5` — all rejected upstream.

If you find an existing Scrips artifact that uses `#0076F8`, that artifact predates DS-015 and is stale. Do not propagate.

### Comment rail — LEFT side, fixed sidebar (all slide-format artifacts)

For every multi-slide consumption artifact (ADR HTML render, plan, briefing, deck), the comment surface lives in a **fixed left-side sidebar**. Never: floating button, `position:fixed` overlapping button, per-slide inline textarea appended to slide content.

Anatomy (implement exactly):
- CSS custom property: `:root { --rail: 272px; }` — makes it easy to collapse on mobile
- Rail: `position: fixed; top:0; left:0; width: var(--rail); height:100vh; display:flex; flex-direction:column; background: var(--surface); border-right: 1px solid var(--border); z-index: 200`
- Body offset: `body { margin-left: var(--rail); }`
- Rail header: eyebrow `font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-muted)`
- Rail body: `flex:1; overflow-y:auto` — JS-generated `.rail-block` per slide
- Each block: slide number + title label + `<textarea>` with `border: 1px dashed var(--border)`
- `localStorage` persistence keyed by `'<artifact-slug>-fb-' + slide.id` — **every slide must have a unique `id`**
- IntersectionObserver scroll-spy: active slide's `.rail-block` gets `.active { background: var(--accent-soft) }` and its label changes to `color: var(--accent)`
- Rail footer: `position` in flex flow (NOT fixed), sticky via `flex-shrink: 0`, contains one full-width "Copy all as prompt" button
- Copy function: collects all non-empty textareas, builds structured prompt, writes to clipboard

```html
<aside id="rail">
  <div id="rail-header">Slide feedback</div>
  <div id="rail-body"></div>
  <div id="rail-footer">
    <button id="copy-btn" onclick="copyFeedback()">Copy all as prompt</button>
  </div>
</aside>
```

Responsive: `@media (max-width: 880px) { :root { --rail: 0px; } #rail { display: none; } body { margin-left: 0; } }`

Caught 2026-05-20 — bottom-right floating button was wrong. Caught again 2026-05-20 — per-slide inline textarea was also wrong. Left rail is the only locked pattern for slide-format artifacts.

### Self-contained — no external CDN

Per memory `feedback_html_artifacts_self_contained.md`: the artifact must work with zero network access. No external `<link>` to fonts CDN, no external scripts, no external images. If brand fonts matter visually, base64-embed `@font-face`. Otherwise system font stack is the fallback.

This supersedes the older `<link rel="stylesheet" href="https://signal-ds.vercel.app/fonts/scrips-fonts.css">` pattern earlier in this skill — do not use that link.

## Content presentation — the patterns that pay

Optimize for two things: **scan speed** (Samer absorbs in seconds) and **information capture** (he remembers what mattered after closing the tab). All patterns below are vanilla HTML+CSS+SVG, no libraries.

### 1. Hero metrics row (status / report / brief)

Top of page, 3–5 stat cards. Big number, small label, optional delta. Always above the fold.

```html
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0;">
  <div class="card" style="text-align:center;padding:16px;">
    <div style="font-size:32px;font-weight:600;color:var(--ink);letter-spacing:-0.02em;">$487K</div>
    <div style="font-size:12px;color:var(--ink-muted);text-transform:uppercase;letter-spacing:0.06em;">Runway</div>
    <div style="font-size:12px;color:var(--good);margin-top:4px;">▲ 2.1 mo</div>
  </div>
  <!-- repeat -->
</div>
```

### 2. Color-coded status pills (consistent across all artifacts)

```css
.pill { display:inline-block; padding:2px 10px; border-radius:999px; font-size:12px; font-weight:500; }
.pill.draft   { background:#f5f5f5; color:#5a5a5a; }
.pill.ready   { background:#e6f1ff; color:#005FD4; }
.pill.shipped { background:#d1fae5; color:#047857; }
.pill.warn    { background:#fef3c7; color:#b45309; }
.pill.block   { background:#fee2e2; color:#b91c1c; }
.pill.deprecated { background:#f5f5f5; color:#9ca3af; text-decoration:line-through; }
```

Same vocabulary every artifact = pattern recognition. Don't reinvent labels.

### 3. Comparison / decision matrix (options × criteria)

Use when picking between 2–6 options. Sticky header column for criteria, ✓/✗/~ glyphs in cells, recommendation row at bottom.

```html
<table>
  <thead><tr><th></th><th>Option A</th><th>Option B</th><th>Option C</th></tr></thead>
  <tbody>
    <tr><td>Cost</td><td>$$</td><td>$</td><td>$$$</td></tr>
    <tr><td>Time-to-ship</td><td>2w</td><td>1w</td><td>4w</td></tr>
    <tr><td>Reversible</td><td>✓</td><td>✓</td><td>✗</td></tr>
    <tr style="background:var(--accent-soft);font-weight:600;">
      <td>Recommend</td><td></td><td>✓</td><td></td>
    </tr>
  </tbody>
</table>
```

### 4. SVG flowchart / state machine (instead of paragraph explanation)

```html
<svg viewBox="0 0 600 120" width="100%" style="max-width:600px;">
  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/>
    </marker>
  </defs>
  <!-- nodes -->
  <rect x="10"  y="40" width="120" height="40" rx="6" fill="#fff" stroke="#e5e5e5"/>
  <text x="70"  y="65" text-anchor="middle" font-size="13">Draft</text>
  <rect x="180" y="40" width="120" height="40" rx="6" fill="#e6f1ff" stroke="#005FD4"/>
  <text x="240" y="65" text-anchor="middle" font-size="13" fill="#005FD4">In review</text>
  <rect x="350" y="40" width="120" height="40" rx="6" fill="#d1fae5" stroke="#047857"/>
  <text x="410" y="65" text-anchor="middle" font-size="13" fill="#047857">Shipped</text>
  <!-- edges -->
  <line x1="135" y1="60" x2="175" y2="60" stroke="#5a5a5a" marker-end="url(#ar)"/>
  <line x1="305" y1="60" x2="345" y2="60" stroke="#5a5a5a" marker-end="url(#ar)"/>
</svg>
```

Use for: state machines, data flow, sequence, dependency graphs, journey maps. Always include marker arrows; always label edges if not self-evident.

### 5. Inline SVG bar chart / sparkline (no chart libraries)

Bar:
```html
<svg viewBox="0 0 300 60" width="100%" style="max-width:300px;">
  <rect x="0"   y="20" width="40" height="30" fill="#005FD4"/>
  <rect x="50"  y="10" width="40" height="40" fill="#005FD4"/>
  <rect x="100" y="25" width="40" height="25" fill="#005FD4"/>
  <text x="20"  y="58" text-anchor="middle" font-size="10" fill="#5a5a5a">W1</text>
</svg>
```

Sparkline (one-line trend):
```html
<svg viewBox="0 0 200 30" width="200" height="30">
  <polyline points="0,20 30,15 60,18 90,10 120,12 150,5 180,8" fill="none" stroke="#005FD4" stroke-width="2"/>
  <circle cx="180" cy="8" r="3" fill="#005FD4"/>
</svg>
```

For multi-series or interactive charts, still vanilla SVG — just scale up. Avoid Chart.js / D3 unless the artifact is a real prototype.

### 6. Annotated diff (code review)

Two-column flex layout, removed (red bg) on left, added (green bg) on right, margin annotations below.

```html
<div style="font:14px/1.5 ui-monospace,monospace;border:1px solid var(--border);border-radius:6px;overflow:hidden;">
  <div style="background:#fee2e2;padding:6px 12px;"><span style="color:#b91c1c;">- const x = old()</span></div>
  <div style="background:#d1fae5;padding:6px 12px;"><span style="color:#047857;">+ const x = await new()</span></div>
  <div style="background:#fef3c7;padding:8px 12px;font:13px/1.4 -apple-system,sans-serif;color:#b45309;">
    ⚠ Note: this changes the call site to async — 3 callers updated, see L42 / L78 / L91.
  </div>
</div>
```

### 7. Progress / capacity bar

```html
<div style="margin:8px 0;">
  <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
    <span>Sprint 4</span><span>67% (8/12)</span>
  </div>
  <div style="height:8px;background:#f5f5f5;border-radius:4px;overflow:hidden;">
    <div style="height:100%;width:67%;background:#005FD4;"></div>
  </div>
</div>
```

### 8. Side-by-side compare (before/after, A/B, then/now)

```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
  <div class="card"><h3>Before</h3>...</div>
  <div class="card" style="border-color:var(--accent);"><h3>After</h3>...</div>
</div>
```

### 9. Sticky TOC with active-section highlight (long pages > 5 sections)

```html
<aside style="position:sticky;top:24px;float:right;width:200px;font-size:13px;margin-left:24px;">
  <strong style="color:var(--ink-muted);font-size:11px;text-transform:uppercase;letter-spacing:0.06em;">On this page</strong>
  <ol style="padding-left:18px;margin:8px 0;">
    <li><a href="#section-1">Section title</a></li>
  </ol>
</aside>
```

For very long pages, add a 5-line JS scroll-spy to highlight the active anchor.

### 10. Callouts (one per page, max two)

```html
<div class="callout"><strong>TL;DR.</strong> Key insight in one sentence.</div>
<div class="callout" style="border-color:var(--warn);background:#fef3c7;"><strong>Watch.</strong> Caveat.</div>
```

Don't pepper callouts everywhere — they lose force. One TL;DR at the top, one watch/risk box where relevant, that's it.

### Visual hierarchy — the cheat sheet

| Importance | Treatment |
|---|---|
| Headline / KPI | 28–32px, weight 600, letter-spacing -0.01em |
| Section header (h2) | 20px, weight 600, top margin 32px |
| Eyebrow label (h3) | 13px, weight 600, uppercase, color muted, letter-spacing 0.06em |
| Body | 16px / 1.55 line height, max-width 760px |
| Caption / meta | 13–14px, color muted |
| Code | 14px ui-monospace, code-bg fill |

Color hierarchy: ink (primary) → ink-muted (secondary) → border (tertiary). Accent (#005FD4) only for: links, primary action, "you are here" markers, key callouts. Status colors (good/warn/block) only on pills, badges, status icons — never on body text.

### Information capture — the rule of three

Every artifact answers three questions in this order:
1. **What is this?** (title + 1-line meta + TL;DR callout)
2. **What changed / what's the call?** (hero metrics row OR recommendation card)
3. **Why / how?** (sections with diagrams)

Reader can stop at #1 (knows what they're looking at), #2 (knows the answer), or #3 (understands the reasoning). Don't bury #2 behind paragraph 7.

## Anti-patterns

- ASCII diagrams (use SVG)
- Color names as text — render the actual swatch with `<span style="background:#xxx">`
- 100+ line MD files when HTML would let the reader scan
- Mixed HTML inside `.md` — pick one
- Heavy frameworks (React, Vue, Tailwind via CDN) — vanilla JS + inline CSS unless it's a real prototype
- External CDN dependencies — keep artifacts self-contained so they work offline / archived
- Inventing visual identity — use the default style stack above or Signal DS, never a third look
- Chart libraries (Chart.js, D3) for static reports — vanilla SVG renders smaller, faster, archives cleanly
- Decorative emoji as data — if it's information, render it as a pill/icon/swatch; emoji is for emphasis only
- Walls of text where a 4-row table would do — if you find yourself writing "first... second... third...", you wanted a table

## Dual-agent review cycle (the full workflow)

Every consumption artifact (plan, brief, ADR render, report) is designed for a two-pass cycle:

**Pass 1 — Generate**
Claude produces the artifact. Comment rail is present, LocalStorage persistence is wired, copy-as-prompt button is at the bottom of the rail.

**Pass 2 — Review and revise**
1. Samer reads the artifact in browser, types slide-by-slide comments into the rail.
2. Samer clicks "Copy as prompt" — gets a formatted block like:
   ```
   ADR-006 — Slide-by-slide review
   Slide 01 (Cover): Wordmark missing
   Slide 02 (Context): Too verbose — cut to 3 bullets
   Slide 03 (Decision): Perfect
   …
   ```
3. Samer pastes this block back into Claude Code.

**When a comment block is pasted back**, Claude MUST:
- Parse each `Slide NN (Title): <comment>` line
- For each non-"—" comment, locate the corresponding slide/section and apply the edit
- Preserve ALL unmentioned slides verbatim (compound, don't replace — `feedback_compound_dont_replace.md`)
- Re-embed the updated comment rail with the same localStorage keys so prior comments persist
- Output the revised artifact to the same path (version-bump the filename per `artifact-versioning` skill)
- Confirm which slides changed and which stayed unchanged

**Rails must persist.** The comment rail is not decorative — it is the review interface. Every artifact version ships with it. Removing the rail on a revision is a regression.

## Round-trip back to vault

If the HTML artifact captures a decision or learning that belongs in the brain:
1. Author the decision/session-memo as `.md` in the vault per knowledge-schema (`class:`, FHIR if product, ADR-004 tags)
2. Link the HTML artifact from the .md as `artifact: <path or URL>`
3. Activity log entry mentions both
