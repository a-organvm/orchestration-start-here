# SOP-IV-SBM-001: Spiral Build Methodology

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Project phasing as a spiral — forward, return, forward at a higher level — with the invariant that client-facing work ships first, always.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Project has multiple deliverable types (content + infrastructure + systems) | Single-deliverable project (one artifact, one deadline) |
| 2 | Client or stakeholder is actively working during the build | Handoff engagement (deliver finished product, no interim interaction) |
| 3 | Some deliverables are blocked on decisions or dependencies not yet resolved | All requirements are fully specified upfront |
| 4 | The project spans more than one work session or sprint | Single-session task completable in one sitting |
| 5 | Visible progress matters to stakeholders between deliveries | Internal tooling where only final output is evaluated |

If conditions 1-2 hold but 3-5 do not, a linear build plan (waterfall) may suffice.
If condition 2 fails (no concurrent client activity), the return wave loses its enrichment signal — use a milestone-based plan instead.

---

## 2. Protocol Phases

```
PROJECT INITIATION
    │
    ├── ⟨alpha⟩ FOUNDATION    Resolve blockers, lay ground, establish infrastructure
    │
    ├── {there  FIRST PASS    Bones live — deliver something usable FIRST
    │
    ├──  back)  RETURN         Go back through first-pass deliverables with enrichment
    │
    ├──  again  SECOND PASS   Build infrastructure products: revenue, automation, independence
    │
    └── ⟨omega⟩ COMPLETION    System runs autonomously, client is sovereign
```

### The Critical Lesson

Maddie was already selling while they were building governance tooling. Client-facing work ships first, always. The infrastructure that makes it sustainable ships second. Reversing this order means the client has nothing to show while you build plumbing.

### Phase 1: FOUNDATION (alpha)

**Purpose:** Clear the path. Resolve every blocker that would stall the first pass. Establish the minimum infrastructure to begin delivering.

**Invariant steps:**
1. Inventory all known blockers:
   - Access and permissions (accounts, repos, API keys, domains)
   - Decisions pending from client/stakeholder
   - Technical prerequisites (hosting, CI, deployment pipeline)
   - Information gaps (missing content, unclear requirements)
2. Resolve blockers in dependency order — the blocker that gates the most downstream work resolves first
3. Set up the project board (invoke `SOP-IV-BGT-001` if using GitHub Projects)
4. Create the skeleton structure:
   - Repository/directory structure with placeholder files
   - Build and deploy pipeline (even if deploying a placeholder)
   - Communication channels and feedback mechanisms
5. Categorize all known work items using the wave classification (see below)
6. Exit criteria: no UNBLOCKED items remain that require Foundation-phase infrastructure

**Outputs:** Cleared blockers, project board, skeleton structure, wave-classified backlog

**Ledger emission:** `foundation_complete` with `{blockers_resolved, items_classified, skeleton_created}`

### Phase 2: FIRST PASS (there)

**Purpose:** Deliver something the client can show, sell, or use immediately. Structure visible. Placeholders for what is not done. Never hide incompleteness — display it as architecture.

**Invariant steps:**
1. Work only UNBLOCKED items from the wave-classified backlog
2. Prioritize by client visibility:
   - **Tier 1:** Things the client shows to others (website, pitch deck, portfolio)
   - **Tier 2:** Things the client uses daily (tools, dashboards, workflows)
   - **Tier 3:** Things the client needs to exist but does not interact with (infrastructure, CI)
3. For each deliverable:
   - Build the structure first (navigation, layout, sections, headings)
   - Fill primary content (hero sections, key pages, core functionality)
   - Leave secondary content as explicit placeholders:
     ```markdown
     <!-- PLACEHOLDER: Case study section — content pending from client (CLR-003) -->
     ```
   - Placeholders are architecture, not laziness. They show the client where everything goes.
4. Deploy/deliver after each coherent batch — do not wait for the full pass to complete
5. Collect client feedback on first-pass deliverables (this feedback drives the Return wave)
6. Exit criteria: all Tier 1 items are live with structure visible; client has something to show

**Outputs:** Live deliverables with visible structure, placeholder map, client feedback

**Ledger emission:** `first_pass_complete` with `{tier1_delivered, tier2_delivered, placeholders_remaining}`

### Phase 3: RETURN (back)

**Purpose:** Go back through first-pass deliverables with enrichment. Fill gaps, connect pieces, improve quality, add depth. This is not a second version — it is the completion of the first version at a higher resolution.

**Invariant steps:**
1. Review all feedback collected during First Pass
2. Review all AFTER-DECISIONS items — decisions that have been made since First Pass started:
   - Reclassify resolved decisions as UNBLOCKED
   - Identify newly blocked items (new questions surfaced during First Pass)
3. For each first-pass deliverable:
   - Fill placeholders with actual content
   - Improve quality: better copy, tighter design, edge case handling
   - Connect pieces: cross-references, navigation, internal links
   - Add depth: secondary pages, supporting content, documentation
4. Process AFTER-BUILD-PROGRESS items that are now unblocked by First Pass infrastructure
5. Run the board audit (`SOP-IV-BGT-001` Phase 6) to detect drift accumulated during the build
6. Exit criteria: all Tier 1 and Tier 2 items are complete (no placeholders); feedback incorporated

**Outputs:** Enriched deliverables, resolved placeholders, processed feedback

**Ledger emission:** `return_complete` with `{placeholders_filled, feedback_items_addressed, quality_improvements}`

### Phase 4: SECOND PASS (again)

**Purpose:** Build the infrastructure that makes the system self-sustaining. Revenue systems, automation, independence tooling. The client should be able to operate without the builder after this phase.

**Invariant steps:**
1. Work items that were AFTER-BUILD-PROGRESS — infrastructure that depended on First Pass being live:
   - Revenue/payment systems (the client needs something to sell before you build the payment flow)
   - Automation (the client needs manual processes before you automate them)
   - Analytics and monitoring (the client needs traffic before dashboards are meaningful)
   - Documentation and training (the client needs the system before you document it)
2. For each infrastructure deliverable:
   - Build with the client's actual usage patterns as input (observed during First Pass and Return)
   - Prioritize automation of the most painful manual processes first
   - Test with real data, not synthetic fixtures
3. Begin knowledge transfer: document processes, record walkthroughs, create runbooks
4. Run redundancy detection (`SOP-IV-BGT-001` Phase 7) to clean up board accumulated during build
5. Exit criteria: client can perform all critical operations independently; revenue infrastructure live

**Outputs:** Infrastructure deliverables, automation scripts, documentation, knowledge transfer materials

**Ledger emission:** `second_pass_complete` with `{infrastructure_delivered, processes_automated, knowledge_transferred}`

### Phase 5: COMPLETION (omega)

**Purpose:** The system runs autonomously. The client is sovereign. Handoff is complete.

**Invariant steps:**
1. Final audit: run all governance checks:
   - Board audit (`SOP-IV-BGT-001` Phase 6)
   - Authority audit (`SOP-IV-SAD-001` Phase 6)
   - Redundancy detection and cleanup
2. Close all open items:
   - DEFERRED items logged as IRF entries for future work
   - Remaining AFTER-DECISIONS items documented as open questions with recommended defaults
   - All WIP items either completed or explicitly deferred with rationale
3. Produce handoff package:
   - System architecture overview
   - Runbook for recurring operations
   - Contact/escalation paths
   - Maintenance schedule (what needs periodic attention)
4. Transition board to maintenance mode:
   - Close the project board or archive completed views
   - Create a maintenance board if ongoing support is expected
5. Exit criteria: client operates independently; no critical items remain in WIP; handoff accepted

**Outputs:** Handoff package, clean board, maintenance plan, sovereign client

**Ledger emission:** `completion_achieved` with `{items_closed, items_deferred, handoff_accepted}`

---

## 3. Wave Classification

Every work item entering the backlog receives a wave classification that determines when it is actionable:

| Classification | Definition | Queued For |
|----------------|------------|------------|
| **UNBLOCKED** | Can be acted on now with no external dependencies | Current wave (First Pass or Return) |
| **AFTER-DECISIONS** | Blocked on client/stakeholder input — a question must be answered first | Return wave (by which time decisions are expected) |
| **AFTER-BUILD-PROGRESS** | Depends on infrastructure from the current wave being live | Second Pass (infrastructure that requires First Pass to exist) |
| **DEFERRED** | Useful but not time-critical — no wave assignment | Logged as IRF item for future sessions |

Wave classification is assigned during FOUNDATION and re-evaluated at each phase transition. Items can be reclassified as blockers resolve:
- AFTER-DECISIONS item where the decision was made → reclassify to UNBLOCKED
- AFTER-BUILD-PROGRESS item where the dependency shipped → reclassify to UNBLOCKED
- UNBLOCKED item that surfaced a new dependency → reclassify to AFTER-DECISIONS or AFTER-BUILD-PROGRESS

---

## 4. The "Bones First" Principle

The spiral method's core insight: never hide incompleteness. Display it as architecture.

**What "bones first" looks like:**
- A website with all pages created, navigation working, hero sections filled, and body sections marked `[Content pending — interview scheduled 04/10]`
- A dashboard with all panels laid out, two panels with live data, three panels showing "Data source: pending Stripe integration (Second Pass)"
- A document with all headings in place, executive summary written, appendices marked as placeholders with expected completion dates

**Why it works:**
1. The client sees the full scope of what is being built, not just what is done
2. Placeholders are commitments — they promise something will go there
3. Feedback on structure comes early, when it is cheap to change
4. The client can begin using/showing the partial deliverable immediately
5. Nothing is hidden — the project state is the architecture itself

**What "bones first" is NOT:**
- Shipping broken functionality ("it crashes but the button is there")
- Vaporware demos ("this is what it will look like")
- Feature flags hiding unfinished work from the user

---

## 5. Outputs

| Phase | Output | Type | Purpose |
|-------|--------|------|---------|
| FOUNDATION | Cleared blockers, skeleton, classified backlog | Infrastructure | Enables First Pass to begin immediately |
| FIRST PASS | Live deliverables with visible structure | Client-facing | Client can show/sell/use |
| RETURN | Enriched deliverables, resolved placeholders | Client-facing | First version at full resolution |
| SECOND PASS | Infrastructure, automation, documentation | Operational | System becomes self-sustaining |
| COMPLETION | Handoff package, sovereign client | Terminal | Builder exits; client operates |

---

## 6. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| First Pass ships infrastructure instead of client-facing work | Tier 1 items still in backlog after First Pass | Ruthlessly deprioritize infrastructure; ship visible work first |
| Return wave has no enrichment signal (no client feedback) | Feedback collection step produced zero items | Proactively solicit feedback; if client is unresponsive, use best judgment and document assumptions |
| AFTER-DECISIONS items never unblock (client does not decide) | Items sit in AFTER-DECISIONS across two waves | Escalate with recommended defaults; proceed with defaults if no response |
| Second Pass builds automation for processes that changed during Return | Automation does not match actual workflow | Build automation from observed Return-wave behavior, not First Pass assumptions |
| Scope creep inflates each wave beyond capacity | Wave completion dates slip; DEFERRED count grows | Apply fixed-time-variable-scope: the wave deadline is fixed, scope adjusts to fit |
| Bones-first placeholders are never filled | Placeholder count does not decrease across waves | Track placeholder count as a health metric; unfilled placeholders in Return are a critical finding |

---

## 7. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| `SOP-IV-BGT-001` (Board Governance Toolkit) | Operational substrate | Board phases map to spiral waves; board audit runs at each phase transition |
| `SOP-IV-SAD-001` (Single-Authority Data Model) | Governing principle | Board is canonical for work item state throughout the spiral |
| `SOP-IV-XGR-001` (Xenograft Protocol) | Upstream supplier | Xenograft ingests client material during FOUNDATION; strikes feed the First Pass backlog |
| `fixed-time-variable-scope` | Constraint model | Each wave is a fixed-time container; scope adjusts within it |
| `score-rehearse-perform` | Complementary | Score-rehearse-perform governs individual deliverables; spiral governs the project arc |
| `session-self-critique` | Applied at phase transitions | Each phase exit is a self-critique checkpoint: did we ship the right things in the right order? |

---

## 8. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Invocable by:** Any organ running a multi-deliverable, multi-phase project
- **Core invariant:** Client-facing work ships first. Infrastructure ships second. This ordering is not negotiable. If you find yourself building plumbing while the client has nothing to show, you have violated the protocol.
- **Versioning:** SemVer. Changes to the wave structure or phase ordering increment major. New wave classifications or phase exit criteria increment minor.
- **Review cadence:** After every engagement that uses this methodology, conduct a retrospective: Did the wave ordering hold? Where did we deviate? What should the next version codify?
- **Adaptation guide:**
  - **Solo projects (no client):** Replace "client" with "user" or "audience." The principle still holds: the thing people see ships before the thing that makes it sustainable.
  - **Open source:** First Pass = working MVP with README. Return = tests, docs, CI. Second Pass = packaging, distribution, community infrastructure.
  - **Internal tools:** First Pass = the tool works for the primary use case. Return = edge cases, error handling, polish. Second Pass = monitoring, alerting, runbooks.
