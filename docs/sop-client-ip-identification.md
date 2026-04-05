# SOP-IV-CIP-001: Client IP Identification

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** Commerce domain (applicable to client engagements across organs)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Recognizing and naming the client's original intellectual property from within their raw material.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Client has provided original material (not exclusively third-party content) | All material is licensed, quoted, or externally sourced |
| 2 | The material contains recurring named concepts, frameworks, or methodologies | Material is purely operational (instructions, specs, requirements) |
| 3 | Build output will present content under the client's name/brand | Output is white-label, anonymous, or system-branded |
| 4 | An atom registry exists for the material | Material has not been atomized (invoke Xenograft first) |
| 5 | The engagement includes content strategy, not only technical build | Engagement is pure implementation with no content layer |

If conditions 1-3 hold but 4 does not, invoke SOP-IV-XGR-001 (Xenograft Protocol) first.
If condition 2 fails (no named concepts), the protocol will complete quickly with an empty inventory — which is itself a finding worth reporting.

---

## 2. Protocol Phases

```
ATOM REGISTRY WITH PROVENANCE DATA (from Xenograft)
    |
    +-- Phase 1: FILTER          Select LOCAL-provenance atoms
    +-- Phase 2: SCAN            Identify named frameworks, methodologies, terminology
    +-- Phase 3: VERIFY          Confirm originality against external sources
    +-- Phase 4: INVENTORY       Produce the IP Inventory with full metadata
    +-- Phase 5: PROTECT         Recommend protection strategy per item
```

### Phase 1: FILTER

**Purpose:** Narrow the atom registry to atoms containing the client's original work, excluding external references and common knowledge.

**Invariant steps:**
1. From the atom registry, select all atoms where `provenance` indicates client authorship:
   - Client-authored documents (conversations, notes, recordings, drafts)
   - Client's original frameworks described in third-party interviews or profiles
   - Client's presentations, workshops, or teaching materials
2. Exclude atoms where provenance is:
   - External reference (cited books, articles, studies)
   - Common knowledge (widely-known facts, standard industry terms)
   - System-generated (metadata, structural markers, boilerplate)
3. Tag selected atoms with `ip_candidate: true` in the registry
4. Generate `IP-CANDIDATES.md` listing all candidate atoms with source references

**Filter invariant:** When in doubt about provenance, include the atom as a candidate. Phase 3 will verify. False positives are preferable to missed IP.

**Outputs:** Filtered atom set with `ip_candidate: true` tags

**Ledger emission:** `ip_candidates_filtered` with `{total_atoms, candidate_count, excluded_count}`

### Phase 2: SCAN

**Purpose:** Within the candidate atoms, identify specific intellectual property patterns.

**Invariant steps:**
1. Scan for **named frameworks**: capitalized terms or phrases used consistently across multiple atoms
   - Example: "Bio-Safety Pyramid", "Feel Good First", "EAU Framework"
   - Consistency test: the term appears in 3+ atoms with coherent meaning
2. Scan for **unique methodologies**: multi-step processes the client describes as their own
   - Example: "90-second cortisol reset", a specific sequenced protocol
   - Ownership test: the client presents it as their approach, not a citation
3. Scan for **original terminology**: terms the client coined or uses distinctively
   - Example: "Creature Selves" as a therapeutic concept
   - Distinctiveness test: the term is not standard vocabulary in the client's field
4. For each identified IP item, record:
   ```yaml
   - ip_id: IP-001
     name: "Bio-Safety Pyramid"
     type: named_framework
     description: "Hierarchical model for establishing biological safety..."
     source_atoms: [ATM-0234, ATM-0567, ATM-0891, ATM-1102]
     first_appearance: "File: coaching-session-12.md, Section: Core Model"
     frequency: 14   # Number of atoms referencing this concept
   ```
5. Cross-reference IP items with each other — some may be components of a larger system

**Outputs:** IP item list with source atom references and cross-references

**Ledger emission:** `ip_items_scanned` with `{framework_count, methodology_count, terminology_count}`

### Phase 3: VERIFY

**Purpose:** For each candidate IP item, confirm originality by searching external sources.

**Invariant steps:**
1. For each IP item, search external sources:
   - Web search for the exact term/phrase
   - Academic databases for the concept
   - Industry publications for the methodology
   - Competitor/peer content for similar frameworks
2. Classify originality:
   - **LOCAL** — The term/framework is the client's original creation. Not found elsewhere, or found only in content attributed to the client.
   - **SHARED** — The term exists elsewhere but the client's usage or adaptation is distinctive. Example: "Burnt Toast Theory" exists in popular culture; the client's specific application to their domain is their adaptation.
   - **COMMON** — The term/concept is widely used in the field. Not protectable. Example: "mindfulness" or "holistic wellness."
3. For SHARED items, document:
   - The external usage (who, where, when)
   - How the client's version differs
   - Whether the client's adaptation is sufficiently distinctive to claim
4. Update IP items with `originality` classification and verification notes

**Verification invariant:** Do not conflate popularity with non-originality. A client may have independently created something that later became popular. Check chronology, not just prevalence.

**Outputs:** Verified IP inventory with originality classifications

**Ledger emission:** `ip_verified` with `{local_count, shared_count, common_count}`

### Phase 4: INVENTORY

**Purpose:** Produce the formal IP Inventory — the deliverable document.

**Invariant steps:**
1. Compile the IP Inventory table:

   | # | Name | Type | Description | Source Atoms | Originality | Frequency | Protection |
   |---|------|------|-------------|-------------|-------------|-----------|------------|
   | IP-001 | Bio-Safety Pyramid | Named Framework | Hierarchical model for... | ATM-0234 +3 | LOCAL | 14 | Trademark candidate |
   | IP-002 | Feel Good First | Philosophy | Guiding principle that... | ATM-0102 +7 | LOCAL | 22 | Document + trademark |
   | IP-003 | Burnt Toast Theory | Methodology | Reframing technique... | ATM-0445 +2 | SHARED | 8 | Document adaptation |

2. For each item, write a brief narrative:
   - What it is, in the client's own language (drawn from atoms)
   - Where it appears in their content
   - How it relates to other IP items (if part of a larger system)
3. Identify the IP ecosystem:
   - Are multiple items part of a unified system? (e.g., Feel Good First is the philosophy, Bio-Safety Pyramid is the model, EAU is the framework)
   - Map the relationships between items
4. Produce a visual or textual map of the IP ecosystem if relationships exist

**Outputs:** IP Inventory document (Markdown), IP ecosystem map

**Ledger emission:** `ip_inventory_produced` with `{total_items, local_count, shared_count, ecosystem_clusters}`

### Phase 5: PROTECT

**Purpose:** Recommend protection strategies for each IP item based on its type and originality.

**Invariant steps:**
1. For each IP item, recommend a protection strategy:

   | IP Type | Originality | Recommendation |
   |---------|-------------|----------------|
   | Named Framework | LOCAL | Trademark consideration for the name; copyright for the written framework description |
   | Named Framework | SHARED | Document the client's specific adaptation; note prior art |
   | Unique Methodology | LOCAL | Copyright for the written process; trade secret for proprietary implementation details |
   | Unique Methodology | SHARED | Document differentiation from existing methods |
   | Original Terminology | LOCAL | Trademark consideration if used commercially; copyright for definitions |
   | Original Terminology | SHARED | Document the client's distinctive usage context |
   | Any | COMMON | Document-only — record that the client uses this term but it is not protectable IP |

2. For trademark candidates, note:
   - Is the name currently in use in commerce?
   - Is the name distinctive (not descriptive or generic)?
   - Recommended classes for registration (if applicable)
3. For copyright candidates, note:
   - What specific expression is protectable (not the idea, the expression)
   - Where the definitive written version exists
4. For trade secret candidates, note:
   - What should NOT be published (the proprietary implementation)
   - What can be published (the public-facing description)
5. Include a disclaimer: this is a content analysis, not legal advice. Recommend consulting an IP attorney for formal protection.

**Protection invariant:** Never recommend protection for COMMON items. Over-claiming dilutes the client's actual IP position.

**Outputs:** Protection recommendation per IP item, disclaimer

**Ledger emission:** `ip_protection_recommended` with `{trademark_candidates, copyright_candidates, trade_secret_candidates, document_only}`

---

## 3. Outputs

| Phase | Primary Output | Format | Audience |
|-------|---------------|--------|----------|
| FILTER | Candidate atom set | YAML | Internal |
| SCAN | IP item list with source references | YAML, Markdown | Internal |
| VERIFY | Verified IP inventory with originality | YAML, Markdown | Internal |
| INVENTORY | IP Inventory document, ecosystem map | Markdown | Client |
| PROTECT | Protection recommendations | Markdown | Client |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Zero IP items found | Phase 2 scan returns empty | Report the finding. Some engagements genuinely have no original IP. This is valuable information. |
| All items classify as COMMON | Phase 3 verification | Review with client — they may have a distinctive adaptation not captured in the atoms. Conduct a focused interview. |
| Client disputes originality classification | Phase 4 review | Record the client's position. If they claim LOCAL and evidence says SHARED, document both perspectives. The client makes the final call on how to present it. |
| External search finds identical framework | Phase 3 verification | Check chronology. If the client published first, they may have priority. If unclear, classify as SHARED and note the dispute. |
| IP items span multiple engagements | Phase 4 inventory | Cross-reference with previous engagement inventories. An IP item may grow across engagements. |
| Atom registry lacks provenance data | Phase 1 filter | Cannot reliably filter. Re-enter Xenograft Phase 4 with provenance tagging enabled. |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-XGR-001 (Xenograft Protocol) | Upstream producer | Atom registry with provenance data is the input |
| SOP-IV-CPP-001 (Content-to-Product Pipeline) | Parent pipeline | IP identification is invoked during CPP Phase 3 (ROUTE) |
| SOP-IV-ETP-001 (Editorial Triage Protocol) | Parallel | IP items containing contested claims are also FLAGGED |
| SOP-IV-MPR-001 (Multi-Perspective Reporting) | Downstream consumer | Client Report includes IP inventory highlights |
| `open-source-licensing-and-ip` | Related governance | For system-generated IP; this SOP is for client-generated IP |
| `source-evaluation-and-bibliography` | Related process | Bibliography work informs Phase 3 originality verification |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Primary domain:** ORGAN-III (Ergon) client engagements
- **Invocable by:** Any organ working with client-provided content containing potential IP
- **Versioning:** SemVer. New IP types or originality classifications increment minor. Changes to the protection model increment major.
- **Review cadence:** After every 3rd engagement, review IP detection patterns. Are named frameworks being missed? Are COMMON items being over-flagged as LOCAL?
- **Sovereign Systems instance:** 6 IP items identified — Bio-Safety Pyramid, Feel Good First, Burnt Toast Theory, 90-second cortisol reset, Creature Selves, EAU (Elevate, Align, Unlock) framework. All classified LOCAL. This is the reference instance.
