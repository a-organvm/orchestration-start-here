# SOP-IV-XGR-001: The Xenograft Protocol

**Version:** 1.0
**Date:** 2026-04-03
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Etymology:** ξένος (xenos, foreign/alien) + γράφειν (graphein, to write/record)

> The process of receiving foreign material, sequencing its genome, proving exhaustive
> coverage, and organizing it for integration into the host system.

---

## 1. When This Protocol Applies

Six invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Material crosses a boundary | Generated internally, already in-schema |
| 2 | Material is unstructured | Arrives as structured data (JSON, YAML, API response) |
| 3 | Action is required | Archive-only (no downstream work) |
| 4 | Provenance matters | Anonymous, commodity data |
| 5 | Completeness must be provable | Sample-based analysis acceptable |
| 6 | Multiple perspectives validate | Single-model decomposition sufficient |

If conditions 1-3 hold but 4-6 do not, use the lightweight `intake_router` instead.
If condition 2 fails (structured data), use `document-audit-feature-extraction` directly.

---

## 2. Protocol Phases

```
ALIEN MATERIAL ARRIVES (any format, any source, any volume)
    │
    ├── Phase 1: ARCHIVE         Persist raw, split binary/text tracking
    ├── Phase 2: CONVERT         Normalize to Markdown
    ├── Phase 3: EXTRACT         Frontmatter + structural metadata
    ├── Phase 4: ATOMIZE         Decompose to idea-level, tag in-situ
    ├── Phase 5: VERIFY          Multi-model blind check, reconcile
    ├── Phase 6: COVERAGE        Prove exhaustive accounting
    └── Phase 7: STRIKE          Organize atoms into deployable work units
```

### Phase 1: ARCHIVE

**Purpose:** Create an immutable record of what arrived, before any transformation.

**Invariant steps:**
1. Create intake directory: `intake/{YYYY-MM-DD}-{source-slug}/raw/`
2. Copy all files verbatim into `raw/` — no renaming, no restructuring
3. Generate manifest: `raw/MANIFEST.md` listing every file with:
   - Filename, size, MIME type, SHA-256 hash
   - Source attribution (who provided, when, via what channel)
   - Binary/text classification
4. Commit manifest + raw files as a single atomic commit

**Outputs:** `MANIFEST.md`, immutable `raw/` directory

**Ledger emission:** `received_xenograft` with `{source, file_count, total_bytes}`

### Phase 2: CONVERT

**Purpose:** Normalize all material to a processable text format.

**Invariant steps:**
1. For each file in `raw/`:
   - PDF → Markdown (preserve headings, lists, tables)
   - DOCX/PPTX/XLSX → Markdown
   - HTML → Markdown (strip navigation chrome, preserve content structure)
   - Images → `![description](path)` reference + OCR text if applicable
   - Audio/Video → Transcript markdown (with timestamps if available)
   - Already Markdown/Text → Copy verbatim
2. Write converted files to `intake/{date}-{slug}/converted/`
3. Maintain 1:1 filename mapping: `raw/report.pdf` → `converted/report.md`
4. Log conversion failures in `converted/CONVERSION-ERRORS.md`

**Outputs:** `converted/` directory with Markdown-normalized corpus

**Failure mode:** If >20% of files fail conversion, HALT and escalate — the source
format may require a specialized converter before proceeding.

### Phase 3: EXTRACT

**Purpose:** Impose structural metadata on each converted document.

**Invariant steps:**
1. For each file in `converted/`, prepend YAML frontmatter:
   ```yaml
   ---
   source_file: {original filename from raw/}
   source_hash: {SHA-256 of raw file}
   content_type: {document|transcript|spreadsheet|image|presentation}
   author: {if attributable}
   date_created: {if determinable}
   date_ingested: {YYYY-MM-DD}
   word_count: {computed}
   section_count: {computed from headings}
   domain: {assigned per Domain Atom Definitions below}
   ---
   ```
2. Identify document structure: heading hierarchy, section boundaries, list items
3. Write extracted files to `intake/{date}-{slug}/extracted/`
4. Generate `extracted/STRUCTURE-MAP.md` — table of all documents with section counts,
   word counts, and preliminary domain assignment

**Outputs:** `extracted/` directory, `STRUCTURE-MAP.md`

### Phase 4: ATOMIZE

**Purpose:** Decompose each document to its smallest actionable units, tagged in-situ.

**Invariant process:**
1. Read each document in `extracted/`
2. Identify atoms — the smallest unit of meaning that could independently motivate action
3. Mark each atom in-situ using the tagging convention:
   ```
   <!-- ATOM:{domain}:{type}:{sequential-id} -->
   The actual content that constitutes this atom.
   <!-- /ATOM -->
   ```
4. Write atomized files to `intake/{date}-{slug}/atomized/`
5. Generate `atomized/ATOM-REGISTRY.yaml`:
   ```yaml
   atoms:
     - id: ATM-001
       domain: client
       type: requirement
       source_file: converted/brief.md
       source_section: "§3.2 Technical Requirements"
       source_line: 47
       summary: "System must support 10K concurrent users"
       confidence: 0.95
   ```

**Variant: Domain Atom Definitions**

The atom types are domain-specific. The protocol ships with these built-in domains;
new domains can be registered by adding a section here.

#### Client Engagement Atoms (ORGAN-III)
| Type | Definition | Example |
|------|-----------|---------|
| `requirement` | Something the system must do or be | "Must support SSO" |
| `constraint` | A limitation on how requirements can be met | "Budget: $50K" |
| `preference` | Desired but not mandatory | "Prefer React over Vue" |
| `decision` | A choice already made by the client | "Logo is final" |
| `voice` | Brand voice, tone, or style indicator | "Playful but professional" |
| `asset` | Existing content or media to incorporate | "Use hero image from Drive" |
| `dependency` | External system or timeline dependency | "Stripe integration required" |
| `question` | Unresolved ambiguity requiring client input | "Which payment tiers?" |

#### Research Corpus Atoms (ORGAN-I)
| Type | Definition | Example |
|------|-----------|---------|
| `claim` | A factual assertion made by the source | "Recursive systems self-heal" |
| `finding` | An empirical result or observation | "Latency reduced 40% with caching" |
| `method` | A technique or approach described | "Used Monte Carlo simulation" |
| `framework` | A conceptual model or taxonomy | "The 4-quadrant governance model" |
| `citation` | A reference to external work | "See Meadows (2008), p. 147" |
| `contradiction` | A claim that conflicts with another source | "Contradicts Smith (2019)" |
| `open_question` | An explicitly stated research gap | "No studies address X" |

#### Creative Brief Atoms (ORGAN-II)
| Type | Definition | Example |
|------|-----------|---------|
| `aesthetic` | Visual or sensory constraint | "Dark palette, no pastels" |
| `technical` | Implementation technology requirement | "WebGL, 60fps minimum" |
| `reference` | Existing work cited as inspiration | "Like Refik Anadol's data sculptures" |
| `narrative` | Story or conceptual framing | "Journey from chaos to order" |
| `deliverable` | Concrete output expected | "3 variations, 4K resolution" |
| `constraint` | Budget, timeline, or platform limit | "Must run on mobile Safari" |

#### Editorial Atoms (ORGAN-V)
| Type | Definition | Example |
|------|-----------|---------|
| `argument` | A claim being advanced with evidence | "Automation amplifies, not replaces" |
| `evidence` | Data or source supporting an argument | "BLS data shows 12% growth" |
| `counterpoint` | Anticipated objection or opposing view | "Critics argue this is naive" |
| `narrative_thread` | A storyline or thematic arc | "The automation paradox" |
| `source_quote` | Direct quotation to be attributed | "'We shape our tools...' — McLuhan" |
| `structural_note` | Placement or ordering guidance | "This section before the case study" |

#### System Documentation Atoms (ORGAN-IV)
| Type | Definition | Example |
|------|-----------|---------|
| `procedure` | A step-by-step process | "To deploy: run X then Y" |
| `decision` | An architectural or governance decision | "Chose PostgreSQL over MongoDB" |
| `constraint` | A system invariant or rule | "No back-edges I←III" |
| `dependency` | An inter-component requirement | "Session requires Redis" |
| `tribal_knowledge` | Undocumented but critical information | "Must restart after config change" |
| `debt` | Known technical debt or workaround | "Hardcoded path in line 47" |

#### Legal/Compliance Atoms
| Type | Definition | Example |
|------|-----------|---------|
| `claim` | A factual assertion in a legal context | "Defendant was present on March 5" |
| `obligation` | A contractual or regulatory requirement | "Must retain records for 7 years" |
| `right` | An entitlement or permission | "Licensee may sublicense" |
| `precedent` | Reference to prior ruling or standard | "Per GDPR Article 17" |
| `contradiction` | Conflicting statements across documents | "Exhibit A says $50K, Exhibit B says $75K" |
| `timeline_event` | A date-anchored fact | "Contract signed 2025-01-15" |

### Phase 5: VERIFY

**Purpose:** Validate decomposition quality through independent multi-model assessment.

**Invariant process:**
1. Select 2+ verification agents from `fleet.yaml` (prefer agents with `audit` or
   `research` work types; NEVER use the same agent that performed Phase 4)
2. For each verifier, provide:
   - The original `extracted/` document (NOT the atomized version)
   - The domain atom type definitions
   - Instruction: "Independently identify all atoms in this document"
3. Each verifier produces their own `ATOM-REGISTRY-{agent}.yaml`
4. Reconcile all registries:
   - **Agreement** (≥2 models found same atom): HIGH confidence → keep
   - **Partial** (1 model found, others missed): REVIEW — re-examine source
   - **Conflict** (models disagree on type/boundary): ARBITRATE — human decides
   - **Novel** (verifier found atom original missed): ADD with verification note
5. Produce `VERIFICATION-REPORT.md`:
   ```
   Total atoms (primary):    87
   Total atoms (verifier A): 91
   Total atoms (verifier B): 84
   Agreement rate:            89%
   Added from verification:   6
   Conflicts requiring human: 3
   Final atom count:          93
   ```

**Fleet dispatch pattern:**
```yaml
dispatch:
  primary: claude          # Strategic decomposition
  verifiers:
    - codex                # Structural precision
    - gemini               # Volume/coverage breadth
  reconciliation: claude   # Arbitration requires strategic judgment
```

**Failure mode:** If agreement rate < 70%, the domain atom definitions may be
under-specified. Refine definitions and re-run Phase 4 before continuing.

### Phase 6: COVERAGE

**Purpose:** Prove that every unit of source material has been accounted for.

**Invariant process:**
1. For each document in `extracted/`:
   - Compute total sections (from heading hierarchy)
   - Compute total paragraphs (non-empty blocks)
   - Compute total word count
2. For each atom in the reconciled `ATOM-REGISTRY.yaml`:
   - Record source file, section, and line range
3. Generate `COVERAGE-PROOF.md`:
   ```
   Document: brief.md
   Sections: 14/14 covered (100%)
   Paragraphs: 47/52 covered (90.4%)
   Uncovered paragraphs:
     - §2.1 ¶3: "Thank you for choosing..." (boilerplate, intentionally excluded)
     - §4.2 ¶1-2: "Appendix references..." (reference-only, no actionable content)
     - §6.1 ¶4-5: "Terms and conditions..." (legal boilerplate)
   Word coverage: 4,812/5,100 (94.4%)
   Exclusion justifications: 5/5 documented
   ```
4. Every uncovered section/paragraph MUST have an explicit exclusion justification.
   The valid exclusion reasons are:
   - `boilerplate` — standard language with no domain-specific content
   - `duplicate` — content repeated from another section (cite which)
   - `metadata` — headers, footers, page numbers, TOC entries
   - `reference_only` — points to external content without adding claims
5. If exclusion justifications < 100% of uncovered content: HALT and atomize the gaps

**Proof threshold:** Coverage ≥ 90% of non-boilerplate content. Below this, Phase 4
must be re-entered with tighter attention.

**Ledger emission:** `coverage_proved` with `{document_count, atom_count, coverage_pct}`

### Phase 7: STRIKE

**Purpose:** Organize verified atoms into deployable work units.

**Invariant process:**
1. Group atoms by actionability:
   - **Immediate** — can be acted on now with no dependencies
   - **Blocked** — requires external input (questions, decisions, access)
   - **Deferred** — useful but not time-sensitive
2. For each Immediate group, compose a **strike**:
   ```yaml
   strike:
     id: STR-001
     name: "Technical requirements implementation"
     atoms: [ATM-003, ATM-007, ATM-012, ATM-015]
     target_organ: III
     target_repo: spiral-path-web
     work_type: implementation
     dispatch_to: codex    # Per fleet.yaml routing
     estimated_complexity: medium
     dependencies: []
   ```
3. For Blocked atoms, generate **clarification requests**:
   ```yaml
   clarification:
     id: CLR-001
     atoms: [ATM-022, ATM-023]
     question: "Which payment tiers should the system support?"
     addressed_to: "client"
     blocking: [STR-003, STR-004]
   ```
4. Write `STRIKE-PLAN.md` summarizing all strikes, their dispatch targets,
   and the critical path
5. Feed strikes into `intake_router` for operational dispatch

**Integration with existing infrastructure:**
- Strikes become `intake_router` intakes → action ledger entries
- Clarification requests become GitHub issues with `blocked` + `question` labels
- Deferred atoms are logged as IRF items for future sessions

**Ledger emission:** `strike_planned` with `{strike_count, blocked_count, deferred_count}`

---

## 3. Directory Structure

Each Xenograft engagement creates this tree:

```
intake/{YYYY-MM-DD}-{source-slug}/
├── raw/                    # Phase 1: Immutable originals
│   ├── MANIFEST.md         # File inventory with hashes
│   └── {original files}
├── converted/              # Phase 2: Markdown-normalized
│   ├── CONVERSION-ERRORS.md
│   └── {converted files}
├── extracted/              # Phase 3: Frontmatter + structure
│   ├── STRUCTURE-MAP.md
│   └── {extracted files}
├── atomized/               # Phase 4: In-situ tagged
│   ├── ATOM-REGISTRY.yaml  # Primary decomposition
│   └── {atomized files}
├── verified/               # Phase 5: Multi-model reconciled
│   ├── ATOM-REGISTRY-{agent}.yaml  # Per-verifier
│   ├── ATOM-REGISTRY-reconciled.yaml
│   ├── VERIFICATION-REPORT.md
│   └── {final atomized files}
├── coverage/               # Phase 6: Exhaustiveness proof
│   └── COVERAGE-PROOF.md
├── strikes/                # Phase 7: Deployable work units
│   ├── STRIKE-PLAN.md
│   ├── STR-001.yaml
│   └── CLR-001.yaml
└── XGR-META.yaml           # Protocol metadata
```

`XGR-META.yaml` tracks protocol execution state:
```yaml
protocol: SOP-IV-XGR-001
version: "1.0"
source: {name, date, channel, file_count}
phases_completed: [1, 2, 3]
current_phase: 4
primary_agent: claude
verifiers: [codex, gemini]
domain: client
atom_count: null        # Set after Phase 4
coverage_pct: null      # Set after Phase 6
strike_count: null      # Set after Phase 7
```

---

## 4. Where Intake Directories Live

The intake directory location depends on the engagement scope:

| Scope | Location | Example |
|-------|----------|---------|
| Per-repo (client engagement) | `{repo}/intake/` | `spiral-path-web/intake/2026-04-01-maddie/` |
| Per-organ (research corpus) | `{organ-dir}/intake/` | `organvm-i-theoria/intake/2026-05-01-complexity/` |
| System-wide (cross-organ) | `alchemia-ingestvm/intake/` | `alchemia-ingestvm/intake/2026-06-01-acquisition/` |
| Unsorted (triage pending) | `~/Workspace/intake/` | Already exists as staging area |

`alchemia-ingestvm/` is the canonical system-wide staging area for Xenograft
engagements that span multiple organs or whose target organ is not yet determined.

---

## 5. Integration Map

```
                                    ┌──────────────────────┐
                                    │   ALIEN MATERIAL     │
                                    │   (any source)       │
                                    └──────────┬───────────┘
                                               │
                                    ┌──────────▼───────────┐
                                    │  XENOGRAFT PROTOCOL  │
                                    │  (Phases 1-7)        │
                                    └──────────┬───────────┘
                                               │
                        ┌──────────────────────┼──────────────────────┐
                        │                      │                      │
             ┌──────────▼──────────┐ ┌────────▼─────────┐ ┌─────────▼──────────┐
             │   STRIKES           │ │  CLARIFICATIONS   │ │  DEFERRED ATOMS    │
             │   (work units)      │ │  (questions)      │ │  (future work)     │
             └──────────┬──────────┘ └────────┬─────────┘ └─────────┬──────────┘
                        │                      │                      │
             ┌──────────▼──────────┐ ┌────────▼─────────┐ ┌─────────▼──────────┐
             │   intake_router     │ │  GitHub Issues    │ │  IRF Registry      │
             │   → action_ledger   │ │  (blocked label)  │ │  (CND/IRF items)   │
             │   → fleet dispatch  │ │                   │ │                    │
             └─────────────────────┘ └──────────────────┘ └────────────────────┘
```

---

## 6. Multi-Model Verification Specification

The verification phase is what distinguishes this protocol from single-pass ingestion.
One model's decomposition is opinion. Three models converging is evidence.

### Verifier Selection Rules

1. Primary decomposer and verifiers MUST be different agents
2. At least 2 verifiers are required; 3 recommended for high-stakes engagements
3. Verifiers should have complementary strengths:
   - Structural precision (Codex: catches boundary errors, missing atoms)
   - Coverage breadth (Gemini: casts wide net, high recall)
   - Semantic depth (Claude: catches nuance, contextual meaning)
4. For legal/compliance domains, require ≥3 verifiers and human arbitration for all conflicts

### Blind Check Protocol

Verifiers receive:
- The extracted documents (Phase 3 output)
- The domain atom type definitions (from §2 Phase 4 Variant)
- A neutral instruction prompt (no priming toward expected atom count)

Verifiers do NOT receive:
- The primary decomposition
- The primary atom count
- Any hints about expected coverage

This prevents anchoring bias. Each verifier produces an independent registry.

### Reconciliation Algorithm

```
for each atom A in primary_registry:
    matches = find_matching_atoms(A, verifier_registries)
    if len(matches) >= 2:
        A.confidence = HIGH
    elif len(matches) == 1:
        A.confidence = REVIEW
    else:
        A.confidence = LOW  # Only primary found it

for each atom V in verifier_registries NOT matched to primary:
    if confirmed_by >= 1 other verifier:
        add_to_registry(V, confidence=HIGH, source="verification")
    else:
        add_to_registry(V, confidence=REVIEW, source="verification-single")

for each atom with conflicting type assignments:
    flag_for_human_arbitration()
```

Matching criteria: same source document, overlapping line range (±5 lines),
semantically equivalent summary (human judgment or embedding similarity > 0.85).

---

## 7. Domain Registration

To add a new domain, append to the Domain Atom Definitions table in Phase 4
and register here:

| Domain ID | Organ | Registered | Atom Types |
|-----------|-------|------------|------------|
| `client` | III | 2026-04-03 | 8 types |
| `research` | I | 2026-04-03 | 7 types |
| `creative` | II | 2026-04-03 | 6 types |
| `editorial` | V | 2026-04-03 | 6 types |
| `system` | IV | 2026-04-03 | 6 types |
| `legal` | — | 2026-04-03 | 6 types |

New domains should define 5-10 atom types. Fewer indicates the domain may be a
subset of an existing one. More indicates the domain should be split.

---

## 8. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| `transcript-ingestion-protocol` | Downstream consumer | Phase 2 can produce transcripts that this SOP ingests |
| `document-audit-feature-extraction` | Parallel / alternative | Use for structured docs; Xenograft for unstructured |
| `research-to-implementation-pipeline` | Downstream consumer | Xenograft Phase 7 strikes feed into Gold Path |
| `styx-pipeline-traversal` | Orthogonal | Styx traverses organs; Xenograft ingests into them |
| `cross-agent-handoff` | Used during Phase 5 | Verification dispatch uses handoff envelopes |
| `session-self-critique` | Applied within phases | Each phase exit is a self-critique checkpoint |

---

## 9. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Conversion rate < 80% | Phase 2 error count | Install domain-specific converter, re-run Phase 2 |
| Agreement rate < 70% | Phase 5 verification | Refine atom definitions, re-run Phase 4 with tighter spec |
| Coverage < 90% | Phase 6 proof | Re-enter Phase 4 for uncovered sections |
| Strike dispatch fails | Phase 7 fleet routing | Fall back to manual dispatch, log fleet gap |
| Source material changes mid-protocol | Phase 1 hash mismatch | Archive current state, restart from Phase 1 with delta |

---

## 10. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Invocable by:** Any organ
- **Versioning:** SemVer. Breaking changes (new required phases, changed atom tag format)
  increment major. New domains or optional features increment minor.
- **Review cadence:** After every 5th Xenograft engagement, review atom definitions
  for adequacy and reconciliation thresholds for calibration.

---

## Appendix: Sovereign Systems Instance

First full-scale deployment of the Xenograft Protocol. Documented here as the reference
instance for future engagements.

### Engagement Summary

- **Source:** Sovereign Systems client engagement (ORGAN-III)
- **Corpus:** 127 files, ~360,000 words
- **Atom yield:** 1,821 atoms decomposed
- **Domain:** Client engagement (extended schema)

### 17-Field Atom Schema

The generic 7-field atom schema (§2 Phase 4) was extended to 17 fields to capture the
full dimensionality of a large client engagement:

| # | Field | Description |
|---|-------|-------------|
| 1 | `id` | Unique atom identifier (ATM-NNNN) |
| 2 | `domain` | Routing domain (client, system, editorial, etc.) |
| 3 | `type` | Domain-specific atom type (requirement, decision, etc.) |
| 4 | `source_file` | Origin file in converted/ |
| 5 | `source_section` | Section heading within source |
| 6 | `source_line` | Line number in source |
| 7 | `summary` | Human-readable atom description |
| 8 | `confidence` | Verification confidence (HIGH/REVIEW/LOW) |
| 9 | `provenance` | Who authored/provided this content and when |
| 10 | `nature` | Content nature: directive, observation, artifact, question |
| 11 | `tier` | Signal classification: SIGNAL, CONTEXT, or NOISE |
| 12 | `pillar` | Strategic pillar the atom contributes to |
| 13 | `editorial` | Editorial judgment: publish, internal-only, discard |
| 14 | `build_state` | Implementation state: unbuilt, in-progress, complete, blocked |
| 15 | `nodes` | Connected nodes in the dependency/reference graph |
| 16 | `actionability` | Immediate, blocked, or deferred |
| 17 | `strike_id` | Assigned strike (STR-NNNN) after Phase 7, null before |

### SIGNAL / CONTEXT / NOISE Tiering

A three-tier classification applied during atomization (Phase 4) to separate
actionable content from supporting material and discardable filler:

| Tier | Count | Pct | Definition |
|------|-------|-----|------------|
| **SIGNAL** | 1,153 | 63.4% | Directly actionable — motivates a strike, a decision, or a deliverable |
| **CONTEXT** | 557 | 30.6% | Supporting material — informs but does not independently motivate action |
| **NOISE** | 111 | 6.1% | Boilerplate, duplicates, metadata — excluded from strike planning |

This tiering replaced the binary "covered / excluded" model from Phase 6. CONTEXT atoms
are retained in the registry for traceability but do not generate strikes. NOISE atoms
are documented with exclusion justifications per the Phase 6 invariant.

### Three-Way Verification Configuration

The multi-model verification (Phase 5) was configured as follows:

```yaml
dispatch:
  primary: claude              # Strategic decomposition — full 127-file corpus
  verifiers:
    - gemini                   # Coverage breadth — high recall, catches missed atoms
    - claude-blind             # Same model, zero shared context — tests prompt stability
  reconciliation: claude       # Arbitration on conflicts
```

**claude-blind** denotes a separate Claude session with no access to the primary
decomposition, atom counts, or intermediate notes. This tests whether the protocol's
atom definitions are sufficiently precise to produce convergent results from the same
model architecture without shared state — a stronger test than cross-model agreement
alone.

Agreement rate: 91% (above the 70% threshold). 34 atoms added from verification.
12 conflicts resolved via human arbitration.
