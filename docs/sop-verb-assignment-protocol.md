# SOP-IV-VAP-001: Verb Assignment Protocol

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Compress each structural unit to a single verb that captures its essential action — then use verb collisions to detect redundancy and verb gaps to detect missing capability.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | System contains multiple units (repos, modules, teams, directories) that overlap in purpose | Each unit has a unique, well-defined purpose already documented |
| 2 | A restructuring, merger, or dissolution decision requires knowing what each unit *does* vs. what it *is called* | Naming is sufficient — names already encode function accurately |
| 3 | The unit count is large enough that verbal overlap is plausible (>8 units) | Small system (<8 units) where overlap is visible by inspection |
| 4 | Units were created by different people/sessions over time, risking organic overlap | All units were designed in a single session with intentional differentiation |

If conditions 1-2 hold but 3-4 do not, the protocol still works but the COLLIDE phase may yield few results.

---

## 2. Protocol Phases

```
UNIT LIST (repos, modules, teams, directories)
    │
    ├── Phase 1: ENUMERATE    List all units to be verb-assigned
    ├── Phase 2: DISTILL      Read each unit's content and compress to one verb
    ├── Phase 3: COLLIDE      Detect verb collisions — same verb assigned to multiple units
    ├── Phase 4: GAP          Detect verb gaps — needed verbs that no unit owns
    ├── Phase 5: MAP          Produce the verb map table
    └── Phase 6: RECONCILE    For each collision, recommend merge, differentiate, or dissolve
```

### Phase 1: ENUMERATE

**Purpose:** Produce the complete list of units that will receive verb assignments. The list must be exhaustive — any unit omitted is a unit whose redundancy goes undetected.

**Invariant steps:**
1. Source the unit list from one of:
   - FHA structural classes table (for directory-level verb assignment)
   - Registry or seed.yaml inventory (for repo-level verb assignment)
   - Org chart or team roster (for team-level verb assignment)
   - Module or package index (for code-level verb assignment)
2. For each unit, record: name, size metric (lines of code, file count, or team headcount), and any existing description/purpose statement
3. Include units marked for dissolution or archival — their verbs matter for understanding what will be lost
4. Include phantom/untracked units — they may own verbs that nothing else covers
5. Do not filter by status or tier — every unit participates regardless of maturity

**Outputs:**
- Unit list: `{unit_name, size_metric, existing_description, status}`
- Total unit count

**Ledger emission:** `emitted_units_enumerated` with `{unit_count, include_dissolved, include_phantom}`

### Phase 2: DISTILL

**Purpose:** For each unit, read its actual content and purpose, then compress to a single verb. The verb must describe what the unit *does*, not what it *is*.

**Invariant steps:**
1. For each unit, read:
   - README or primary documentation
   - seed.yaml (produces/consumes edges, tier, description)
   - CLAUDE.md or equivalent agent instructions
   - Source code structure (top-level modules, entry points)
   - If available, the unit's changelog (what has it actually delivered?)
2. Ask: **"If this unit could only perform one action, what would that action be?"**
3. Assign a single verb in infinitive form. Proven verbs from the ORGAN-IV dissection:
   - `coordinate` (orchestration-start-here — orchestrates via registry, governance, scripts)
   - `orchestrate` (tool-interaction-design — the conductor package, session management)
   - `agent` (agentic-titan — the multi-agent framework itself)
   - `smith` (agent--claude-smith — forges/crafts Claude agent instances)
   - `teach` (a-i--skills — skill collection, a reference library)
   - `connect` (universal-node-network — node-to-node routing)
   - `scan` (reverse-engine-recursive-run — system scanning/verification)
   - `contribute` (contrib workspaces — upstream open-source contribution)
   - `score` (vox--architectura-gubernatio — voice governance scoring)
   - `publish` (vox--publica — public-facing output)
4. If a unit resists compression to one verb, it may be doing too many things — record this as a note
5. If a unit's verb is the same as its parent or sibling, record this as a preliminary collision signal
6. A unit that cannot be assigned any verb is a **verbless unit** — likely dead weight or a container with no intrinsic action

**Outputs:**
- Verb assignment per unit: `{unit_name, verb, confidence, notes}`
- Verbless unit list (units that resist assignment)
- Multi-verb unit list (units that needed >1 verb)

**Ledger emission:** `emitted_verbs_distilled` with `{unit_count, unique_verbs, verbless_count, multi_verb_count}`

### Phase 3: COLLIDE

**Purpose:** Detect verb collisions — two or more units assigned the same verb. Each collision is a redundancy signal that demands investigation.

**Invariant steps:**
1. Group units by assigned verb
2. For each verb with >1 unit, create a collision entry:
   - **Verb**: the shared verb
   - **Units**: list of units assigned this verb
   - **Differentiation test**: read the two (or more) units side by side and ask: "Is there a meaningful difference in *how* they perform this verb, or are they genuinely redundant?"
3. Classify each collision:
   - **True redundancy**: units do the same thing, one should absorb the other
   - **False collision / homonym**: units share a verb but operate in different domains or at different scales (e.g., `validate` at repo level vs. `validate` at system level)
   - **Partial overlap**: units share a verb but each also does something the other doesn't — merger or clear boundary-drawing required
4. For true redundancies, identify which unit is larger, more mature, or more actively maintained — this is the candidate absorber
5. Record collision severity: true redundancy = high, partial overlap = medium, false collision = low

**Outputs:**
- Collision list: `{verb, units[], classification, severity}`
- True redundancy pairs with recommended absorber

**Ledger emission:** `emitted_verb_collisions_detected` with `{collision_count, true_redundancy_count, partial_overlap_count}`

### Phase 4: GAP

**Purpose:** Detect verb gaps — actions the system needs to perform but that no unit currently owns.

**Invariant steps:**
1. Define the **expected verb set** for the system's domain. For an orchestration organ, expected verbs might include:
   - `coordinate`, `orchestrate`, `govern`, `validate`, `route`, `monitor`, `agent`, `smith`, `teach`, `score`, `publish`, `document`, `test`
2. Compare the expected verb set to the assigned verb set from Phase 2
3. For each expected verb not present in any unit's assignment, create a gap entry:
   - **Missing verb**: the action no unit performs
   - **Consequence**: what capability the system lacks because no unit owns this verb
   - **Candidate fillers**: existing units that could expand to cover this verb, or a recommendation for a new unit
4. For each assigned verb not in the expected set, verify it is genuinely needed — it may be a niche verb that signals overspecialization, or it may be a novel capability the expected set didn't anticipate
5. Record gap severity: high (system cannot function properly without it), medium (reduces effectiveness), low (nice-to-have)

**Outputs:**
- Gap list: `{missing_verb, consequence, candidate_fillers, severity}`
- Unexpected verb list (assigned verbs not in expected set)

**Ledger emission:** `emitted_verb_gaps_detected` with `{gap_count, unexpected_verb_count}`

### Phase 5: MAP

**Purpose:** Produce the verb map — the primary output artifact that makes the system's action landscape visible at a glance.

**Invariant steps:**
1. Create the verb map table with one row per unit:

| Unit | Verb | Size | Collision | Notes |
|------|------|-----:|:---------:|-------|
| orchestration-start-here | coordinate | 11,857 | — | registry, governance, scripts |
| tool-interaction-design | orchestrate | 40,693 | — | conductor package, sessions |
| agentic-titan | agent | 119,260 | — | multi-agent framework |
| ... | ... | ... | ... | ... |

2. Mark collision cells: if a unit's verb collides with another unit, mark it with the collision classification
3. Append verbless units at the bottom with an empty verb cell
4. Append the gap list below the table
5. Include a verb frequency summary: each verb, how many units own it, total size covered

**Outputs:**
- Verb map table
- Verb frequency summary
- Verbless unit list
- Gap list

**Ledger emission:** `emitted_verb_map_produced` with `{unit_count, unique_verbs, table_rows}`

### Phase 6: RECONCILE

**Purpose:** For each collision, recommend a specific structural action. For each gap, recommend a specific filler.

**Invariant steps:**
1. For each **true redundancy collision**:
   - Recommend **merge**: one unit absorbs the other. The larger/more-mature unit absorbs. The absorbed unit's unique content migrates, then the absorbed unit is dissolved or archived.
   - Specify what content migrates and what is discarded.
2. For each **partial overlap collision**:
   - Recommend **differentiate**: draw an explicit boundary. Rename one unit, split shared responsibilities, or add a domain qualifier to the verb (e.g., `validate-deps` vs. `validate-skills`).
   - Specify the boundary line.
3. For each **false collision**:
   - Recommend **accept**: the collision is a homonym, not a redundancy. Document the distinction so future audits don't re-flag it.
4. For each **verb gap**:
   - If an existing unit can expand: recommend which unit and what the expansion looks like.
   - If no existing unit fits: recommend creating a new unit with a seed.yaml declaring the missing verb as its primary action.
5. For each **verbless unit**:
   - Recommend **dissolve** (absorb useful content into a verb-owning unit) or **delete** (if no useful content exists).
6. Produce the reconciliation ledger: `{action, source_unit, target_unit, verb_before, verb_after, rationale}`

**Outputs:**
- Reconciliation ledger (action per collision, gap, and verbless unit)
- Disposition summary: merge N, differentiate N, accept N, expand N, create N, dissolve N

**Ledger emission:** `emitted_verb_map_assigned` with `{unit_count, unique_verbs, collisions, gaps}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| ENUMERATE | Unit list with size and status | Structured list |
| DISTILL | Verb assignment per unit with confidence | Structured list |
| COLLIDE | Collision list with classification and severity | Grouped list |
| GAP | Gap list with consequences and candidates | Structured list |
| MAP | Verb map table, frequency summary, verbless/gap appendices | Markdown tables |
| RECONCILE | Reconciliation ledger with dispositions | Action list |

The combined output constitutes the **Verb Map** — a compression of the system to its essential actions, with collision and gap analysis driving structural recommendations.

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Verb too abstract (e.g., "manage" assigned to 5 units) | COLLIDE finds 5+ units sharing one verb, all classified as false collisions | The verb is too high-level. Re-run DISTILL for those units with a more specific vocabulary. Ask "manage *what*?" to get the real verb. |
| Verb too specific (every unit gets a unique verb, no collisions) | COLLIDE finds zero collisions in a system known to have overlap | The verbs are too narrow. Lift the abstraction level: instead of "validate-yaml" and "validate-json," use "validate." |
| Unit resists single-verb compression | DISTILL notes >3 multi-verb units | The unit is doing too many things. This is itself a finding — feed it to SGS as an S4 (accumulation) or S1 (structural) skeleton. |
| Expected verb set is wrong for the domain | GAP finds 5+ missing verbs that upon reflection aren't actually needed | Revise the expected verb set. Use the assigned verb set as the ground truth and only flag gaps that represent genuine missing capability. |
| Reconciliation recommendations rejected | Stakeholders disagree with merge/dissolve recommendations | The verb map is evidence, not authority. Present the collision data and let the decision-maker choose. Document the decision and rationale. |
| Cultural resistance to "dissolve" | Units have authors who resist dissolution of their work | Frame dissolution as *absorption* — the content lives on inside a stronger unit. The verb survives; the container changes. |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship |
|-----|-------------|
| SOP-IV-FHA-001 (Flattened Hierarchy Audit) | FHA's directory list and structural classes are the primary input to ENUMERATE. |
| SOP-IV-DCA-001 (Domain Cross-Cut Analysis) | DCA's concentration analysis reveals which units carry the most cross-cutting weight — these are the units that most need precise verb assignment. |
| SOP-IV-SGS-001 (Severity-Graded Skeleton Inventory) | VAP's collisions produce S1 (structural contradiction) or S2 (dead weight) candidates for SGS. Verbless units are S2 candidates. |
| SOP-IV-XGR-001 (Xenograft Protocol) | After ingesting alien material, VAP can be applied to the new units to verify they don't collide with existing system verbs. |
| Repo Onboarding & Habitat Creation (system SOP) | When creating a new repo, VAP's gap analysis identifies which missing verb the new repo should own. The verb becomes part of the seed.yaml contract. |
| Ontological Renamer (skill) | VAP detects when names don't match verbs (a unit called "governance-framework" whose verb is actually "document"). The Ontological Renamer skill can then propose name changes. |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** `~/Workspace/organvm-i-theoria/` (ORGAN-I superproject, ~20 repos, the theoretical organ — testing whether verb assignment works in a domain where actions are more abstract: "theorize," "model," "prove," "compute" — and whether the collision/gap framework holds when verbs are inherently overlapping)
