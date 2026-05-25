---
name: scrips-voice
description: The editorial and visual reference for every non-product Scrips surface — TOPIC, ADRs, briefs, decks (investor/board/sales), Confluence pages, blog posts, marketing copy, brand documents. Codifies voice, banned/preferred language, paragraph patterns, callout system, typography, color usage, and logo rules. Owns how Scrips writes and looks anywhere it is not the product. Signal DS owns product UI; this skill owns everything else. Use when drafting, reviewing, or editing any Scrips-branded artifact that is not product UI.
---

# scrips-voice — Editorial and Visual Reference for Non-Product Surfaces

**One-sentence boundary:** *Signal owns how the product looks. scrips-voice owns how everything else does.*

This skill is the canonical reference for any Scrips artifact that is not product UI. Read it before drafting, editing, or reviewing TOPIC, ADRs, briefs, investor decks, board decks, sales decks, Confluence pages, blog posts, marketing copy, brand documents, or any externally facing Scrips surface.

When you cannot decide a phrasing, structure, or visual choice — this skill is the answer. When the answer isn't here, propose an addition; do not freelance.

---

## 1. Voice — how Scrips writes

### Cardinal rules

1. **Terse over expansive.** Cut every word that doesn't carry weight. A clear sentence beats a clear paragraph.
2. **Evidence over assertion.** Numbers, named clinics, FHIR resources, ADR references. Never "we believe" — show the basis.
3. **Geometry over abstraction.** Two shapes. Three letters. Three definitions. Four personas. The reader remembers structure, not adjectives.
4. **Memorable line per section.** Every section ends on a takeaway the reader can recite back 24 hours later. Not a summary — a sentence.
5. **One idea per paragraph.** Three to five sentences. Then break.
6. **Lead with the diagram, support with prose.** Visual carries the idea. Prose explains the visual. Not the other way around.

### Use these patterns (locked from TOPIC + canon)

- **"X is the disease, Y is the treatment."** ("Fragmentation is the disease. Interoperability is the treatment.")
- **"X prevents. Y delivers. Z sustains."** (Content / Care / Coverage)
- **"Not A. Not B. C."** ("Not Infrastructure. Infostructure.")
- **"Two shapes. Three letters."** (Geometric mnemonic structure.)
- **"This is not a feature. It is the [structural thing]."** ("The patient app is not a feature. It is the switching cost.")
- **"This is a decision, not a suggestion."** (For priority sequences.)
- **"This is the cost of operating, not a competitive moat."** (For regulatory compliance like NABIDH/Malaffi.)
- **The anaesthesiologist metaphor (preserve verbatim, never paraphrase):** *"Nobody calls them a co-pilot. Nobody calls them a companion. They are the ambient intelligence of the room — present always, visible only when the moment requires it."*

### Tone modes by audience

| Audience | Mode | Example |
|---|---|---|
| Clinical partner | Precise, FHIR-aware, no emoji, no marketing | "Encounter (FHIR R4) with Observation references and CarePlan updates." |
| Patient | Clear, no jargon, supportive, never condescending | "Your activity has been lower for 8 days. A 15-minute walk would help today." |
| Investor | Numbers, structural moats, evidence | "NABIDH and Malaffi compliance: a 2-year head-start any competitor must close before seeing their first patient." |
| Internal team | Terse, decisive, no hedging | "EHR maturation first. Form studio second. Patient app pilot third. This sequence is locked." |
| External hire | Operational, navigable, no founder-speak | "Every feature is classified through the TOPIC schema before sprint assignment." |

---

## 2. Banned language — never use in any Scrips artifact

### Hard bans (delete on sight)

- **AI-native, AI-first, AI-powered, AI-enabled** — AI is *how* we build, not *what* we are. Use "clinical operating system with embedded intelligence" or specify the capability (Orb NBA, Orb JITAI, Orb Coding Edits).
- **Disrupting healthcare** — we are building what is missing.
- **Pivot** — we focused.
- **Digital health startup** — we are an infrastructure company.
- **Synergy, leverage, ecosystem** (when used as filler), **revolutionize, game-changing, unleash, empower** — VC-speak. Replace with the specific outcome.
- **Solution** (when used to mean "the product") — name the thing.
- **Best-in-class, world-class, cutting-edge** — show, don't claim.
- **Robust, scalable, seamless** — empty signifiers. Replace with the measurable property.
- **Just** (as filler — "just click here") — delete.
- **Very, really, simply, basically, actually** — adverb sludge. Delete.
- **Holistic** (unless referring to the Care domain layer specifically defined in TOPIC) — vague.
- **Co-pilot, companion** (for Orb or any AI feature) — explicit canon prohibition. Use "ambient intelligence" or name the capability.

### Soft bans (use sparingly, prefer alternatives)

- **Solution** → product, system, capability, workflow
- **Engage / engagement** → name what they do (book, message, monitor, decide)
- **Innovative** → describe the specific innovation
- **User** → person, patient, practitioner, practice, payer (the five Ps from TOPIC)
- **Customer** → practice, payer, longevity clinic — be specific
- **Patient journey** → encounter cascade, care continuum, or specific moments
- **Seamless** → frictionless if literal; otherwise delete
- **Empower** → enable + name the action

### Banned health and market claims (verify before use)

- **"40% diabetes prevalence in UAE"** — false. UAE diabetes prevalence is ~12-15% per IDF. Use "40%+ of UAE adults carry cardiometabolic risk markers" — true and stronger.
- **"HAAD"** — outdated. Rebranded to **DoH Abu Dhabi** in 2018. Use "Department of Health Abu Dhabi (DoH)" or "DoH" on second mention.
- **"DHPO is a policy office"** — false. **DHPO = Dubai Health Post Office** — the e-claims clearinghouse / EDI gateway operated by DHA.
- **"Epic competitor"** — never. Scrips is not building Epic. We build what Epic will not build for boutique and prevention clinics.
- **Specific microservice counts, transaction volumes, clinic counts, revenue numbers** — verify against live source before publishing. Numbers in marketing copy are claims, not decoration.

---

## 3. Visual system — non-product surfaces

This is the editorial visual language. Product UI is governed by Signal DS at `signal-ds.vercel.app`. The two share tokens but apply them differently.

### Typography stack

```css
--serif: 'Instrument Serif', Georgia, serif;
--sans:  'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
```

- **Instrument Serif** — display, h1, h2, h3, pull quotes, italic accents
- **DM Sans** — body, captions, labels, UI chrome, all sans-serif content
- Body weight: **300** (light) for prose, **500** (medium) for labels and emphasis
- Never bold — emphasis is via italics, color, or size, not weight

### Color tokens (locked, identical to Signal DS)

| Token | Hex | Use on non-product surfaces |
|---|---|---|
| Blue | `#0076F8` | Primary editorial accent. Section labels. Links. The "Scrips" mark color: `#0082CA` (slightly different — the wordmark uses this) |
| Green | `#41AE55` | Positive callouts (note). "Resolved," "shipped," "live" status pills |
| Amber | `#E5A000` | Warning callouts. "In progress," "at risk," "borderline" |
| Red | `#CD3232` | Stop callouts. "Blocked," "rejected," "critical" |
| Ink | `#0D0D0D` | Display text (h1, h2, h3) |
| Text | `#3A3A3C` | Body prose |
| Muted | `#6C6C70` | Secondary prose, body in callouts |
| Subtle | `#AEAEB2` | Captions, metadata, dim labels |
| Rule | `#E5E5EA` | Borders, dividers |
| BG | `#F7F9FA` | Section backgrounds (alt) |

**Rejected colors (never use on Scrips surfaces):** Purple, Teal, Dark Indigo, Salmon. These failed clinical suitability review for Signal DS and the same prohibition applies to brand surfaces.

### Callout system (use these four — no others)

| Type | Color | Trigger | Example label |
|---|---|---|---|
| `insight` | Blue | A non-obvious framing or definition | "What this means" |
| `note` | Green | Confirmation, reinforcement, success | "Confirmed approach" |
| `warn` | Amber | Caution, decision required, tradeoff | "Handle with care" |
| `stop` | Red | Hard rule, prohibition, consequence | "Do not do this" |

**Rule:** never use emoji icons. Use a single character glyph or no glyph. Glyph candidates from TOPIC v1.0: `[ ]` (insight), `o` (note), `!` (warn), `^` (stop) — but these are inscrutable; **prefer a one-word label only**, no glyph.

### Hierarchy — heading sizes

```
.h1: clamp(44px, 7vw, 80px) — Hero only, once per document
.h2: clamp(30px, 4.5vw, 52px) — Section heading
.h3: 24px — Sub-section heading
.lead: 18px, weight 300 — Section opener paragraph
.body: 16px, weight 300 — Default prose
.lbl: 11px, uppercase, letter-spaced .12em, blue — Section eyebrow label
.pull: 20px Instrument Serif italic, blue left border 2px — Pull quote
.cap: 11px uppercase letter-spaced — Caption
```

### Layout primitives

- **Wrap width:** `max-width: 700px` for prose. Reference content (tables, lists) can extend wider.
- **Section padding:** `88px 0` standard. `144px 0 88px` for hero.
- **Section dividers:** `1px solid var(--rule)` between sections. No section is borderless.
- **Section backgrounds:** alternate white / `var(--bg)` (#F7F9FA). Never colored backgrounds for sections.
- **Cards:** `border-radius: 12-14px`, `1px solid var(--rule)`, `padding: 26-36px` depending on density.
- **Pull quotes:** left border `2px solid var(--blue)`, padding-left 24px, italic, max-width 500px. Use sparingly — they lose force at scale.

### Banner pattern (use for the one declarative line per document)

```html
<div class="banner">
  <div class="banner-text">
    Built for clinicians, patients,<br/>and <em>the science between them.</em>
  </div>
</div>
```

- Full-width band with top + bottom rule.
- Instrument Serif, clamp(21px, 3.5vw, 34px).
- One blue italic phrase per banner — the memorable line.
- One banner per document. Never two — they cancel each other.

---

## 4. Logo usage

### Wordmark (primary)

- **Source:** `~/scrips-repos/signal-portal/scrips-logo-blue.svg`
- **Color:** `#0082CA` (NOT `#0076F8` — the wordmark blue is a slightly different blue from the editorial accent blue. Both are correct in their context.)
- **Minimum size:** 80px wide
- **Clear space:** equal to the height of the "S" on all sides
- **Use on:** Hero of any Scrips-branded document, deck title slides, footer of long docs, investor materials cover
- **Do not:** rotate, recolor (except white-on-dark for `scrips-logo-white.svg`), distort, add glow/shadow

### Mnemonic mark (secondary — the TOPIC geometric mark)

The two-tile inline SVG used in TOPIC v1.0 hero — funnel triangle + loop circle — paired with three letter tiles (P / I / C) is the secondary mark for documents that explain the TOPIC framework specifically. Reuse the inline SVG pattern from TOPIC v1.0 lines 305–320. Do not rebuild from scratch — copy the pattern.

### Favicon

For Vercel-hosted Scrips documents, use `~/scrips-repos/signal-portal/scrips-logo-blue.svg` cropped to a 1:1 square or use the icon-only crop. The Storybook default purple favicon at `scrips-react/storybook-static/favicon.svg` is **not** a Scrips icon — do not use it.

---

## 5. Document structure — the Scrips long-form pattern

Every long-form Scrips document (TOPIC, ADRs over 200 lines, investor decks rendered as documents, board memos) follows this skeleton:

1. **Nav bar** — fixed, blurred white, 52px tall. Contains: wordmark or document name + version chip, anchor links to major sections.
2. **Hero** — h1, italic serif tagline, 2–4 hero stats (the memorable numbers), wordmark. One full viewport.
3. **Section — Introduction / About** — what this document is, who it serves, how to use it, what it connects to. Always grey background.
4. **Section — Problem / Why** — the diagnosis. The "X is the disease" framing.
5. **Section — Market / Context** — UAE-specific, regulatory context, NABIDH/Malaffi if relevant.
6. **Section — Model / Approach** — TaaS/PaaS, business model, or strategic frame.
7. **Section — Product / What** — what exists, what is building, what is planned.
8. **Section — Brand / Vocabulary / Definitions** — naming, etymology, glossary if short.
9. **Section — Frameworks** — the geometry (TOPIC), the design system (Signal), the operating model.
10. **Section — People** — personas, stakeholders, journeys.
11. **Section — Principles** — the I principles for TOPIC, or the equivalent for other docs.
12. **Section — Domains / Modules** — the three Cs, or the module breakdown.
13. **Section — Method** — six-step design method or the equivalent operating protocol.
14. **Section — Glossary** — alphabetized, every term a non-healthcare reader might not recognize.
15. **Footer** — wordmark, version, date, "Private and confidential" line.

Not every document needs all 15. Most TOPIC-class documents use 8–12. Order matters — sections build on each other.

---

## 6. Attention-span optimization (memorability budget)

A senior reader's attention budget for a long-form Scrips document is **20–30 minutes for first read**, with second-pass scanning. Documents over 1,200 lines are unread documents. Optimize for memorability, not completeness.

### Length targets

| Document type | Lines (single-file JSX) | First-read time |
|---|---|---|
| ADR | 100–250 | 5–10 min |
| Brief | 80–150 | 3–5 min |
| Operating manual (TOPIC-class) | **800–1,000** | **20–30 min** |
| Investor deck (rendered as doc) | 500–800 | 15–20 min |
| Glossary-only reference | unlimited (scrollable) | scan-only |

### Memorability rules

1. **One memorable line per section** — set as a pull quote or banner. The reader must be able to recite it back unprompted.
2. **Reference content visually distinct from narrative** — glossary, product list, persona cards = scannable cards or tables. Narrative = short paragraphs. The reader's eye must know which mode they're in within one glance.
3. **Pull quotes carry the heuristics** — the no-list, the conflict order, the priority sequence. Not buried in paragraphs.
4. **Cut everything that doesn't serve memorability** — decorative prose, hedging, narrative throat-clearing. Out.
5. **Section sized for one viewport** — each section's core idea fits in roughly one viewport on a 13" laptop. Reference content can scroll but is visually marked.
6. **The geometry recurs visually** — funnel and loop shapes appear as visual rhythm throughout, not just in the Geometry section.

### Maintainability rules

1. **Data extracted from prose into objects/arrays at the top of the JSX file.** Editing a persona, adding a worked rejection, or fixing a stat is a 1-line change, not a hunt-through-prose.
2. **CSS as a `const css` template string at the top** (matching TOPIC v1.0 pattern). Inline `style={{...}}` only for one-off positional overrides.
3. **Components decomposed in-file** for repeated patterns (PersonaCard, JourneyMoment, Callout, Banner). No external imports — single-file JSX is the deployment unit.
4. **Comments are sparse.** Only when WHY is non-obvious.

---

## 7. Hard rules (do not violate)

1. **No personal context about Samer or any team member in any company-facing document.** ADHD, energy, focus state, personal preferences — these are conversation context, never artifact content. Every Scrips artifact must read as institutional, not founder-personal.
2. **No invented data.** Every number, clinic name, claim, or statistic is verifiable. If you cannot cite it, do not write it.
3. **No invented entities.** People, organizations, projects mentioned in any Scrips document must exist in the brain (`08-people/`, `04-references/organizations/`, `13-projects/`). Use the canonical slug. Never fabricate to fill a sentence.
4. **No competing taxonomy.** TOPIC's domain language (Content / Care / Coverage), persona language (Superhealther / Kindahealther / The User / Power User), shape language (Funnel / Loop), and intelligence capability language (NBA / JITAI / Coding Edits) is locked. Do not rename, alias, or rephrase across documents.
5. **No marketing voice in operational documents.** Operational docs (TOPIC, ADRs, briefs) describe the system. Marketing voice belongs in marketing surfaces only.
6. **No emoji in any Scrips artifact unless explicitly requested.** Including in Slack drafts that will be sent under the Scrips name.
7. **The anaesthesiologist metaphor is preserved verbatim.** Never paraphrase it. Use it sparingly — once per document maximum.

---

## 8. Patterns that produce attention loss (avoid)

- **Front-loading the doc with a long "About this document" prose block** before the reader has any reason to care. Open with the strongest stat or framing, then explain.
- **Numbered lists longer than 6 items** without visual chunking — eyes glaze.
- **Tables with more than 4 columns** unless reference-mode (glossary, product matrix). Narrative tables stay narrow.
- **Pull quotes adjacent to other pull quotes.** They cancel each other's weight. Space them by at least one paragraph block.
- **Banners stacked.** One per document.
- **Section openers that recap the previous section.** Each section starts fresh. The reader knows where they are.
- **Footnote-heavy prose.** If a footnote is load-bearing, promote it. If it isn't, delete it.

---

## 9. Pre-flight checklist (run before publishing any Scrips artifact)

Before any Scrips document, deck, or external surface is published or shared, verify:

- [ ] Voice — every sentence cuttable? Every adverb earned? Every paragraph one idea?
- [ ] Banned words — searched and removed? (AI-native, leverage, synergy, etc.)
- [ ] Banned facts — DHPO, HAAD, 40% diabetes — replaced with corrected forms?
- [ ] Numbers — every number verified against live source?
- [ ] Names — every person, organization, project resolved to a brain slug?
- [ ] Personal context — zero references to Samer's ADHD, energy, focus state, personal preferences?
- [ ] Pull quotes — one memorable line per section? Banner once?
- [ ] Length — within target for document class?
- [ ] Maintainability — data extracted from prose? Editable in 1 line?
- [ ] Logo — wordmark `#0082CA` from `signal-portal/scrips-logo-blue.svg`? Favicon set?
- [ ] Color — only Blue/Green/Amber/Red? No purple/teal/indigo/salmon?
- [ ] Heading hierarchy — one h1, sequential h2/h3, no skipped levels?
- [ ] Mobile — `@media(max-width:720px)` reflows tested?
- [ ] Footer — version, date, "Private and confidential"?

---

## 10. Skill outputs by request type

| User asks | This skill returns |
|---|---|
| "Draft an investor email" | Voice-compliant copy + banned-word check + footer signature |
| "Review this deck" | Punch list: voice violations, banned words/facts, structural drift, missing memorable lines |
| "Make this section memorable" | Pull-quote candidate + banner candidate + 2–3 sharper phrasings |
| "Is this on-brand?" | Pre-flight checklist run, line-by-line |
| "Rebuild this in Scrips voice" | Rewrite preserving facts, restructuring per voice rules |
| "What's the right word for X?" | Preferred term + the rejected alternatives + the rationale |

---

## 11. Reference files

| File | Where | Purpose |
|---|---|---|
| TOPIC v1.0 | `~/Downloads/topic-final (1).jsx` | Reference implementation of voice + visual system |
| Signal DS | `signal-ds.vercel.app` | Product UI tokens (shared) and the Ten Commandments (locked) |
| Master decision log — April 25, 2026 | Brain `00-inbox/2026-04-25-session-master-capture-april-25-2026-full-topic-and-signal-d.md` | Locked language discipline |
| Naming philosophy | Brain `00-inbox/2026-04-25-topic-signal-naming-philosophy-and-relationship.md` | "Two is navigable. Three is a glossary." |
| Domain taxonomy | Brain `00-inbox/2026-04-25-domain-taxonomy-locked-content-care-coverage.md` | Content / Care / Coverage definitions |
| Wordmark SVG | `~/scrips-repos/signal-portal/scrips-logo-blue.svg` | The Scrips wordmark, `#0082CA` |
| Wordmark white | `~/scrips-repos/signal-portal/scrips-logo-white.svg` | For dark backgrounds |
| TOPIC mnemonic mark | TOPIC v1.0 lines 305–320 | The funnel + loop + P/I/C tile pattern, inline SVG |

---

## 12. Keynote / Presentation — language rules

Presentations carry amplified risk: a single banned phrase in a keynote reaches dozens of people simultaneously and becomes a reputational anchor. Apply all general bans from Section 2, plus the keynote-specific rules below.

### Hard-banned phrases in keynote context

These phrases are banned everywhere but require explicit flagging for slides, speaker notes, and spoken delivery:

| Phrase | Why banned | Canonical replacement |
|---|---|---|
| **"AI-native"** (as self-descriptor) | Signals technology identity over clinical outcome; invites "so what?" in investor rooms | "a company that redesigned around AI execution" |
| **"AI-native operating system"** | Positions Scrips as a tech product, not a clinical infrastructure play | "The clinical operating system for cardiometabolic care" |
| **"AI-first"** | Same signal problem as AI-native; raises competition framing | "built with embedded intelligence" |
| **"digital health startup"** | Commodity category; undermines infrastructure positioning | "clinical infrastructure company" or just "Scrips" |
| **"AI clinic"** (as product label) | Confused noun; implies a physical space or a chatbot | "cardiometabolic care" or "clinical infrastructure" |
| **"co-pilot" / "copilot"** | Explicit prohibition from canon (see Section 2 + anaesthesiologist metaphor) | "ambient intelligence" or name the specific capability (Orb NBA, Orb JITAI) |

### Canonical replacements table (keynote-ready)

| Banned in a deck | Use instead |
|---|---|
| "AI-native operating system" | "The clinical operating system for cardiometabolic care" |
| "AI-native company" | "a company that redesigned around AI execution" |
| "AI-first" | "built with embedded intelligence" |
| "AI clinic" | "cardiometabolic care" or "clinical infrastructure" |
| "co-pilot for clinicians" | "ambient intelligence — present always, visible only when the moment requires it" |
| "digital health startup" | "clinical infrastructure company" |

### Headline audit rule

Every deck headline (h1 and first-line callouts) must be checked against this section and Section 2 before the deck ships. If a headline contains any banned phrase, rewrite it using the replacement above before delivery.

### Cross-reference

See also: `~/.claude/skills/presentation-delivery.md` — narrative spine, claim framing table, canonical one-liners.

---

## 13. Inter-skill coordination

| Skill | Relationship |
|---|---|
| `signal` (design system) | Owns product UI. scrips-voice owns everything else. Tokens are shared. |
| `scrips-product` | Provides strategic positioning (compound thesis, settled debates, target segments). scrips-voice translates them into voice-compliant copy. |
| `scrips-engineering` | Provides architectural facts (FHIR resources, ADR references, microservice details). scrips-voice translates them into reader-appropriate language. |
| `scrips-chief-of-staff` | Receives finished artifacts for distribution. Does not modify voice. |
| Any drafting skill (`brief`, `synth`, `ship`) | Reads scrips-voice patterns before drafting external-facing output. |

---

## 14. Maintenance protocol

This skill evolves. After every artifact draft:

1. If a new banned word emerged from review, add to Section 2.
2. If a new pattern was approved, add to Section 1.
3. If a new layout primitive was used, add to Section 3.
4. Record significant additions in a brain memo with `class: vocabulary` per the knowledge schema.

This skill is the source of truth. If a published artifact contradicts it, the artifact is wrong, not the skill.
