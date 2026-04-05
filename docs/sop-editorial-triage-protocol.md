# SOP-IV-ETP-001: Editorial Triage Protocol

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** Commerce domain (applicable to client engagements across organs)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Handling contested claims in client content without unilateral censorship: never remove without asking, never publish without flagging.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Content contains claims that could be contested | All content is factual, verifiable, or clearly opinion-framed |
| 2 | Content will be published or made client-facing | Content is internal-only and will not reach a public audience |
| 3 | The client authored or provided the content | Content is system-generated or third-party-licensed with existing review |
| 4 | The system operator is not the decision authority on content framing | The operator has explicit editorial authority over the content |
| 5 | Multiple disposition options exist (keep, reframe, remove) | Content is legally required to appear as-is (regulatory, contractual) |

If conditions 1-2 hold but 3-5 do not, the operator may apply editorial judgment directly.
If condition 1 fails (no contested claims), skip this protocol entirely — content passes through clean.

**Key principle:** The client decides how their content is presented on their professional site. The system's job is to surface what needs a decision, not to make the decision.

---

## 2. Protocol Phases

```
ATOMS WITH CONTESTED CLAIMS (identified during atomization)
    |
    +-- Phase 1: IDENTIFY        Mark atoms with contested claims as FLAGGED
    +-- Phase 2: CATEGORIZE       Classify by claim type and risk level
    +-- Phase 3: PRESENT          Generate Editorial Review Document with options
    +-- Phase 4: DECIDE           Client selects disposition per item
    +-- Phase 5: APPLY            Execute dispositions using client-approved language
```

### Phase 1: IDENTIFY

**Purpose:** During atomization (Xenograft Phase 4), mark atoms containing contested claims using the FLAGGED editorial state, distinct from CLEAN and UNVERIFIED.

**Invariant steps:**
1. During atom decomposition, evaluate each atom for contested claims:
   - Medical claims (health outcomes, treatments, diagnoses)
   - Scientific claims (mechanisms, causation, efficacy)
   - Statistical claims (percentages, studies cited without sources)
   - Legal claims (rights, obligations, regulatory assertions)
   - Financial claims (income projections, ROI, market assertions)
2. For each identified atom, set `editorial: FLAGGED` in the atom registry
3. Do NOT remove, modify, or editorialize the content at this stage
4. Do NOT make judgment calls about whether the claim is true or false
5. Generate `FLAGGED-ATOMS.md` listing all flagged atoms with their source locations

**Editorial states:**
- **CLEAN** — No contested claims detected; ready for publication
- **FLAGGED** — Contains claims requiring client review before publication
- **UNVERIFIED** — Insufficient context to determine; requires investigation

**Outputs:** Updated atom registry with editorial states, `FLAGGED-ATOMS.md`

**Ledger emission:** `editorial_flags_raised` with `{flagged_count, clean_count, unverified_count}`

### Phase 2: CATEGORIZE

**Purpose:** For each FLAGGED atom, classify the claim type and risk level to help the client make informed decisions.

**Invariant steps:**
1. For each FLAGGED atom, assign a claim type:
   - `medical` — Health outcomes, treatments, body mechanics, wellness protocols
   - `scientific` — Mechanisms, causation, natural phenomena, research claims
   - `statistical` — Numbers, percentages, study citations, population-level assertions
   - `legal` — Rights, obligations, certifications, regulatory compliance
   - `financial` — Income, ROI, market projections, pricing claims
2. For each FLAGGED atom, assign a risk level:
   - **LOW** — A reasonable interpretation exists; mainstream-adjacent; defensible with minor framing
   - **MEDIUM** — Contested in the field; credible practitioners disagree; requires careful framing
   - **HIGH** — Contradicts scientific or professional consensus; could expose client to liability or credibility damage
3. For MEDIUM and HIGH risk atoms, draft a brief rationale explaining why the flag was raised
4. Update the atom registry with `claim_type` and `risk_level` fields

**Categorization invariant:** Risk level assesses publication risk, not truth value. The system does not adjudicate whether a claim is true. It assesses whether the claim, if published as-is, could create problems for the client.

**Outputs:** Categorized flagged atoms with claim types and risk levels

**Ledger emission:** `editorial_categorized` with `{low_count, medium_count, high_count, by_claim_type}`

### Phase 3: PRESENT

**Purpose:** Generate the Editorial Review Document — a decision surface for the client, not a correction list.

**Invariant steps:**
1. Generate the Editorial Review Document with one entry per FLAGGED atom:
   ```
   ## FLAGGED ITEM: ATM-0547

   **Source:** [filename], Section [heading], Line [N]
   **Claim type:** scientific | **Risk level:** MEDIUM

   **Original content:**
   > "Water has memory and can be programmed with intention..."

   **Why this was flagged:**
   The concept of water memory is contested within mainstream science.
   Publishing as-is may invite scrutiny from evidence-based practitioners.

   **Options:**
   - [ ] KEEP — Publish as-is (client accepts framing risk)
   - [ ] REFRAME — Publish with modified language (suggested below)
   - [ ] REMOVE — Do not publish this content

   **Suggested reframe:**
   > "Some practitioners work with the concept that water responds to
   > intention — a perspective drawn from [client's framework name]..."
   ```
2. Group items by risk level: HIGH first, then MEDIUM, then LOW
3. Within each risk level, group by claim type
4. Include a summary table at the top:
   - Total flagged items by risk level and claim type
   - Estimated time to review (rough: 1-2 minutes per LOW, 3-5 per MEDIUM, 5-10 per HIGH)
5. Frame the document as choices, not corrections:
   - Opening: "Here is content where the framing matters. How do you want to present these?"
   - NOT: "Here are errors in your content that need fixing."

**Presentation invariant:** Every FLAGGED atom must appear in the Editorial Review Document. No atom is silently removed or silently passed through.

**Outputs:** Editorial Review Document (Markdown)

**Ledger emission:** `editorial_review_generated` with `{total_items, document_path}`

### Phase 4: DECIDE

**Purpose:** Record the client's disposition for each flagged item, with date and rationale.

**Invariant steps:**
1. Send the Editorial Review Document to the client
2. For each item, the client selects one disposition:
   - **KEEP** — Publish as-is. The client acknowledges the framing.
   - **REFRAME** — Publish with modified language. The client approves the specific reframe.
   - **REMOVE** — Do not publish this content.
3. Record each decision:
   ```yaml
   - atom_id: ATM-0547
     disposition: REFRAME
     decided_by: "Maddie"
     decided_date: 2026-04-02
     rationale: "Use the 'some practitioners' framing"
     approved_text: "Some practitioners work with the concept that..."
   ```
4. For REFRAME dispositions, the approved text must come from the client or be explicitly approved by the client. The system may suggest language, but the client owns the final wording.
5. If the client does not respond to specific items, those items remain FLAGGED and MUST NOT be published

**Outputs:** Decision log for editorial items

**Ledger emission:** `editorial_decisions_logged` with `{keep_count, reframe_count, remove_count, pending_count}`

### Phase 5: APPLY

**Purpose:** Execute the client's editorial dispositions across the content.

**Invariant steps:**
1. For each KEEP disposition:
   - Set `editorial: CLEAN` in the atom registry
   - No content changes
2. For each REFRAME disposition:
   - Replace the original content with the client-approved text
   - Set `editorial: CLEAN` in the atom registry
   - Record the original text in `editorial_history` for traceability
3. For each REMOVE disposition:
   - Set `editorial: REMOVED` in the atom registry
   - Set `build_state: N/A` and `actionability: N/A`
   - Do not delete the atom from the registry (traceability)
   - Remove from any associated issues or strikes
4. Verify: no atom with `editorial: FLAGGED` remains in content destined for publication
5. Update the project board: issues containing REMOVED atoms are re-scoped; issues containing REFRAMED atoms get updated content

**Outputs:** Updated atom registry, updated content, updated project board

**Ledger emission:** `editorial_applied` with `{kept, reframed, removed, publication_ready_count}`

---

## 3. Outputs

| Phase | Primary Output | Format | Audience |
|-------|---------------|--------|----------|
| IDENTIFY | Flagged atom list | YAML, Markdown | Internal |
| CATEGORIZE | Categorized flags with risk levels | YAML | Internal |
| PRESENT | Editorial Review Document | Markdown | Client |
| DECIDE | Decision log | YAML | Internal + Client |
| APPLY | Updated atom registry, updated content | YAML, Markdown | Internal |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Flagging rate > 30% of atoms | Phase 1 count | Review flagging criteria; may be over-sensitive. Recalibrate by domain. |
| Flagging rate = 0% on content with known contested material | Phase 1 count | Review flagging criteria; may be under-sensitive. Add domain-specific claim patterns. |
| Client does not respond to editorial review | Phase 4 stalls | Escalate with summary: "N items require your input before publication. Here are the 3 highest-risk." |
| Client requests wholesale KEEP on HIGH-risk items | Phase 4 disposition | Record the decision. Add a note to the atom: "Client-approved as-is on [date]." Do not override. |
| Reframe language disputed | Phase 4/5 iteration | Client provides their own language. System records it. The client owns the words. |
| New contested claims discovered after Phase 5 | Post-publication review | Re-enter Phase 1 for the new content. The protocol is re-entrant. |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-XGR-001 (Xenograft Protocol) | Upstream producer | Xenograft Phase 4 (ATOMIZE) triggers editorial flagging |
| SOP-IV-CPP-001 (Content-to-Product Pipeline) | Parent pipeline | This protocol is invoked during CPP Phase 2 (PROCESS) |
| SOP-IV-CIP-001 (Client IP Identification) | Parallel | IP items may also be FLAGGED if they contain contested claims |
| SOP-IV-MPR-001 (Multi-Perspective Reporting) | Downstream consumer | Client Report must reflect editorial dispositions |
| `document-audit-feature-extraction` | Alternative path | Use for structured documents with known-clean content |
| `session-self-critique` | Applied within phases | Each phase exit is a self-critique checkpoint |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Primary domain:** ORGAN-III (Ergon) client engagements, ORGAN-V (Logos) editorial content
- **Invocable by:** Any organ publishing client-provided content
- **Versioning:** SemVer. New claim types or risk levels increment minor. Changes to the disposition model increment major.
- **Review cadence:** After every 5th engagement, review flagging patterns for calibration. Are HIGH-risk items being consistently KEPT? (May indicate over-flagging.) Are unflagged items causing post-publication issues? (May indicate under-flagging.)
- **Sovereign Systems instance:** 104 FLAGGED atoms out of 1,821 total (5.7%). Claim types: water memory, biophotonics, frequency healing, statistical claims without sources. Client response: mixture of KEEP, REFRAME, and REMOVE — validating that the three-option model works.
