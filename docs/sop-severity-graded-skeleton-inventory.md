# SOP-IV-SGS-001: Severity-Graded Skeleton Inventory

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Catalogue all structural problems in a system, grade each by reversibility and blast radius, document evidence, and produce a severity-ordered remediation queue.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A structural audit or cross-cut analysis has surfaced anomalies | No prior audit — raw exploration, not grading |
| 2 | The anomaly count exceeds trivial (>5 distinct issues) | 1-3 isolated issues that can be fixed ad hoc |
| 3 | Remediation resources are limited and must be prioritized | Unlimited time/budget — fix everything in parallel |
| 4 | Trust in the system's declared state is uncertain | System has been recently verified and is known-clean |
| 5 | A restructuring, dissolution, or migration decision depends on knowing what is broken | Routine maintenance with no structural decisions pending |

If conditions 1-2 hold but 3-5 do not, the SWEEP and GRADE phases are still valuable for documentation, but TRIAGE can be abbreviated.

---

## 2. Protocol Phases

```
ANOMALIES (from FHA, DCA, or direct observation)
    │
    ├── Phase 1: SWEEP        Systematic scan for anomalies across 5 categories
    ├── Phase 2: GRADE        Assign severity S1-S5 by reversibility and blast radius
    ├── Phase 3: EVIDENCE     Document what, where, why, and how-detected per skeleton
    ├── Phase 4: PRESENT      Generate severity-grouped table with remediation guidance
    └── Phase 5: TRIAGE       Prioritize and sequence the remediation queue
```

### Phase 1: SWEEP

**Purpose:** Systematically scan the system for anomalies across five defined categories, ensuring no class of problem is overlooked.

**Invariant steps:**
1. Scan for **structural contradictions**: declared state vs. actual state mismatches. Look for:
   - Config files that disagree with each other (.gitmodules vs. README, registry vs. disk)
   - Duplicate directories (byte-identical or near-identical content in two locations)
   - Invisible-to-git directories that contain irreplaceable content
   - State machines or governance rules reimplemented in incompatible ways
2. Scan for **dead weight**: artifacts that consume space, attention, or maintenance burden without providing value. Look for:
   - Scaffold-only directories (ceremony files exist but no real work was done)
   - Repos marked for dissolution that still exist
   - Corpora marked for deduplication that were never deduplicated
   - Frozen snapshots that are neither archived nor maintained
3. Scan for **inflated claims**: declared capabilities, metrics, or statuses that exceed observed evidence. Look for:
   - GRADUATED or PRODUCTION status with incomplete task backlogs
   - Test count claims that cannot be independently verified
   - Tier assignments (flagship, standard) not justified by actual maturity
   - Documentation claiming features that don't exist in code
4. Scan for **accumulation/drift**: gradual entropy from organic growth without cleanup. Look for:
   - Multi-namespace plan sprawl (plans in 5+ different directory conventions)
   - Cache directories for tools not used at that level
   - Session artifacts with no cleanup protocol
   - Virtual environments or dependency locks committed or left in-tree
   - Nesting amplification (.github/.github/, wrapper-within-wrapper)
5. Scan for **missing links**: gaps in expected structure or connectivity. Look for:
   - No shared dependency resolution across a multi-repo system
   - No single operational index for scattered SOPs/playbooks/protocols
   - Cross-boundary consumption without an import mechanism
   - Expected ceremony files absent in directories that need them
6. Record each finding as a raw skeleton entry: `{category, short_description, location}`

**Outputs:**
- Raw skeleton list grouped by category, with locations

**Ledger emission:** `emitted_skeletons_swept` with `{contradiction_count, dead_weight_count, inflated_count, drift_count, missing_count}`

### Phase 2: GRADE

**Purpose:** Assign each skeleton a severity grade S1-S5 based on two axes: how hard it is to fix (reversibility) and how much damage it causes if left unfixed (blast radius).

**Invariant steps:**
1. Apply the severity scale:

| Grade | Name | Reversibility | Blast Radius | Definition |
|-------|------|---------------|--------------|------------|
| **S1** | Structural contradictions | Hard to fix — requires systemic change | High — undermines trust in all declared state | Two sources of truth disagree; the system contradicts itself |
| **S2** | Dead weight | Easy to fix — delete or archive | Medium — wastes attention and inflates counts | Artifacts that exist but provide no value; removal is safe |
| **S3** | Inflated claims | Dangerous — requires admitting overstatement | High — erodes trust in status/metrics | The system claims more than it delivers; trust is at stake |
| **S4** | Accumulation/drift | Gradual — requires sustained attention | Low per item, high in aggregate | Entropy from growth without cleanup; each item is minor but the sum degrades legibility |
| **S5** | Missing links | Medium — requires design, not just cleanup | Medium — gaps limit system capability | Something expected is absent; filling the gap may require new architecture |

2. For each skeleton from Phase 1, assign a severity grade
3. If a skeleton spans two categories (e.g., a duplicate directory that is also dead weight), assign the higher severity
4. Record the grade alongside each skeleton entry

**Outputs:**
- Graded skeleton list: `{id, grade, category, short_description, location}`

**Ledger emission:** `emitted_skeletons_graded` with `{s1_count, s2_count, s3_count, s4_count, s5_count}`

### Phase 3: EVIDENCE

**Purpose:** For each skeleton, document sufficient evidence that a reader who was not present for the audit can independently verify the finding.

**Invariant steps:**
1. For each skeleton, document:
   - **What it is**: one-sentence description of the problem
   - **Where it is**: exact file paths, directory names, config entries
   - **What makes it a problem**: the specific harm — confusion, data loss risk, trust erosion, wasted resources
   - **How it was detected**: which phase of which SOP surfaced it (FHA Phase 2, DCA lens 6, direct observation, etc.)
   - **Evidence artifacts**: the specific files, counts, dates, or diffs that prove the finding
2. Use the naming convention from DISSECTION: `S{grade}.{sequence}` (e.g., S1.1, S1.2, S2.1)
3. Assign bold-formatted titles that are scannable: `**S1.1 — agentkit = contrib--coinbase-agentkit (byte-identical duplicate)**`
4. For inflated claims (S3), include both the claim and the counter-evidence side by side

**Outputs:**
- Evidence-documented skeleton entries, each with ID, title, description, location, harm, detection method, and evidence

**Ledger emission:** `emitted_skeletons_evidenced` with `{total_documented, evidence_artifacts_cited}`

### Phase 4: PRESENT

**Purpose:** Generate the severity table — the primary output artifact that decision-makers will use.

**Invariant steps:**
1. Group skeletons by severity grade (S1 first, S5 last)
2. Within each grade, order by blast radius (highest first)
3. For each skeleton, include:
   - ID and title
   - One-paragraph evidence summary (full evidence in Phase 3 is the appendix)
   - Recommended remediation: specific action (delete, merge, archive, document, redesign)
   - Estimated effort: trivial (minutes), small (hours), medium (days), large (sprint+)
4. Produce a summary count table:

| Grade | Count | Effort Range |
|-------|------:|-------------|
| S1 — Structural contradictions | N | medium-large |
| S2 — Dead weight | N | trivial-small |
| S3 — Inflated claims | N | medium |
| S4 — Accumulation/drift | N | small-medium |
| S5 — Missing links | N | medium-large |

5. Calculate total skeleton count and the ratio of easy-fix (S2, S4) to hard-fix (S1, S3, S5) items

**Outputs:**
- Severity table with remediation guidance
- Summary count table
- Appendix: full evidence from Phase 3

**Ledger emission:** `emitted_skeleton_inventory_presented` with `{total_skeletons, easy_fix_count, hard_fix_count}`

### Phase 5: TRIAGE

**Purpose:** Sequence the remediation queue — what to fix first, second, and what to defer.

**Invariant steps:**
1. **S1 first**: structural contradictions undermine all other work. If the system contradicts itself, no other fix is trustworthy until S1 items are resolved.
2. **S3 second**: inflated claims erode trust. Fixing them may mean demoting status, reducing claimed metrics, or acknowledging incomplete work. This is uncomfortable but necessary before any restructuring.
3. **S2 next**: dead weight is the easiest win — deletion or archival clears noise and makes the system legible. High morale impact: visible cleanup.
4. **S4 then**: accumulation/drift requires sustained attention but each item is small. Batch similar items (all cache cleanups together, all plan consolidations together).
5. **S5 last**: missing links often require design decisions that depend on the system being clean (S1-S4 resolved) before the right design becomes clear.
6. Within each grade, sequence by: (a) items that block other items first, (b) quick wins before slow burns, (c) items in actively-maintained directories before stale ones.
7. Produce the triage queue: ordered list with `{id, grade, title, remediation, estimated_effort, dependencies, recommended_sprint}`

**Outputs:**
- Triage queue (ordered remediation list)
- Dependency graph between skeletons (if fixing X requires fixing Y first)

**Ledger emission:** `emitted_skeleton_inventory_completed` with `{s1_count, s2_count, s3_count, s4_count, s5_count, total}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| SWEEP | Raw skeleton list by category | Grouped list |
| GRADE | Graded skeleton list with severity | Structured list |
| EVIDENCE | Evidence-documented entries with IDs | Narrative per skeleton |
| PRESENT | Severity table, summary counts, appendix | Markdown tables + narrative |
| TRIAGE | Ordered remediation queue with dependencies | Ordered list |

The combined output constitutes the **Skeleton Inventory** — the definitive catalogue of what is wrong with the system, graded and sequenced for action.

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| SWEEP misses a category (e.g., no scan for inflated claims) | Post-hoc discovery of an S3 issue not in the inventory | Re-run SWEEP for the missed category; append to inventory with a note on when it was discovered |
| Grade assignment inconsistent (similar issues get different grades) | Review shows S2 and S4 items that should be the same grade | Establish explicit decision criteria and re-grade all borderline cases; document the criteria used |
| Evidence insufficient (reader cannot independently verify) | External reviewer asks "how do you know this?" and the entry cannot answer | Re-run EVIDENCE for the specific skeleton; add file paths, counts, or diffs until independently verifiable |
| Inflated claims (S3) disputed by author | Author argues the claim was valid at time of writing | Distinguish "was valid, now stale" (reclassify as S4 drift) from "was never valid" (remains S3) |
| TRIAGE sequence contested | Stakeholders disagree on priority order | Use the two-axis framework (reversibility × blast radius) as objective tiebreaker; document the disagreement |
| Too many skeletons to act on (>30) | Remediation queue exceeds available capacity | Group by directory and tackle one directory at a time; mark deferred items with a revisit date |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship |
|-----|-------------|
| SOP-IV-FHA-001 (Flattened Hierarchy Audit) | FHA and DCA produce the raw anomalies that SGS grades. Without a prior audit, SWEEP operates blind. |
| SOP-IV-DCA-001 (Domain Cross-Cut Analysis) | DCA's collision and void lists feed directly into SGS Phase 1. Collisions often become S1 or S4; voids become S5. |
| SOP-IV-VAP-001 (Verb Assignment Protocol) | VAP's collision detection (two units with the same verb) produces S1 or S2 candidates for SGS. |
| SOP-IV-XGR-001 (Xenograft Protocol) | Xenograft ingestion can produce skeletons (incomplete conversion, missing atoms). SGS can be run post-xenograft to verify ingestion quality. |
| Promotion & State Transitions (system SOP) | S3 findings (inflated claims) may require demoting repos from GRADUATED to CANDIDATE or PRODUCTION to GRADUATED. SGS feeds promotion review. |
| Stranger Test Protocol (system SOP) | Both assess system legibility, but Stranger Test evaluates from a newcomer's perspective while SGS grades from a structural auditor's perspective. |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** `~/Workspace/organvm-iii-ergon/` (ORGAN-III superproject, ~26 repos, the commercial organ — testing whether the severity scale and categories generalize to a product-focused system where inflated claims carry different weight)
