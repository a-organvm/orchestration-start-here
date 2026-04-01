# Handoff: 72h Reconciliation Refinement

**Origin session:** 2026-04-01 · `orchestration-start-here`
**Committed artifact:** `dc4ec5f` — `docs/reconciliation-72h.md`
**Script:** `scripts/reconcile-72h.py`

---

## State Delivered

469 operator prompts extracted from JSONL sessions (2026-03-29 to 2026-03-31), cross-referenced against 159 git commits across 6 workspaces. Report generated, committed, and redacted for credential references.

### Current Statistics
- 13.1% DELIVERED (53 — high-confidence 3+ keyword match)
- 26.2% PARTIAL (106 — 2-keyword match, likely real but cross-workspace)
- 59.4% HANGING (240 — no commit evidence, category inflated)
- 1.2% DEFERRED (5 — explicit future-reference)
- 0% HUMAN-ACTION

### Classification Breakdown
META 163, BUILD 143, AUDIT 44, PLAN 22, TRIAGE 13, RESEARCH 10, DECISION 9

---

## What Needs Doing

### 1. Reconciler Script Refinements (`scripts/reconcile-72h.py`)

**Add STEERING classification.** ~80 of the 240 HANGING prompts are routing signals: "proceed", "logic dictates order", "continue", "all of the above". These are not tasks — they're dispatch confirmations. The classifier needs a STEERING category with keywords: `proceed, continue, yes, logic, dictates, order, all of the above, hell yes, go, next`.

**Cross-workspace commit pooling.** Currently matches prompts primarily against same-workspace commits. A `workspace-root` prompt that produced a commit in `orchestration-start-here` shows as HANGING. The matcher should pool all commits and weight by keyword overlap, not workspace alignment.

**Prompt deduplication.** The same "Provide an overview..." prompt appears 15+ times across workspaces. Deduplicate by text hash before classification — count once, note repetition count.

**Noise pattern expansion.** Add: `^proceed$`, `^continue$`, `^yes$`, `^❯`, image-only prompts `^\[Image`.

### 2. Hanging Item Triage

The 240 HANGING items contain three real populations:

| Population | Estimated Count | Action |
|-----------|----------------|--------|
| Steering commands | ~80 | Reclassify as STEERING, no outcome needed |
| Philosophical/design intake | ~60 | These became absorbed into larger commits without keyword trace — mark as ABSORBED with note |
| Genuinely unresolved | ~100 | Cross-reference against IRF, intake_router history, and current task queues |

### 3. Statistical Growth Patterns

The prompts themselves describe their own growth trajectory. Key patterns visible in the data:

- **Prompt density by workspace:** `workspace-root` (128), `application-pipeline` (82), `meta-organvm` (118), `orchestration-start-here` (67), `a-organvm` (8) — the root workspace is the primary dispatch surface
- **Classification distribution suggests:** 40% of prompts are META/steering, 35% BUILD, 11% AUDIT — the system spends more time routing than building
- **Session-close prompts** ("Provide an overview...") account for ~15 DELIVERED matches to the same commit — the reconciler should normalize these as a single session-close event
- **Temporal clustering:** prompts arrive in bursts (13:xx, 15:xx, 20:xx, 00:xx-01:xx) aligned with session boundaries

### 4. Integration Points

- **Action Ledger:** The reconciliation should emit entries into `action_ledger/data/actions.yaml` — each reconciliation run is itself a system action with parameters (window, prompt_count, delivery_rate)
- **Intake Router:** HANGING items that are genuinely unresolved should be routed back through `intake_router` for dispatch
- **Fieldwork:** Patterns observed during reconciliation (e.g., "steering commands don't need outcomes") should be recorded as fieldwork observations

---

## Entry Points

```
# Re-run with current data
python3 scripts/reconcile-72h.py > docs/reconciliation-72h.md

# Review hanging items
grep "HANGING" docs/reconciliation-72h.md | wc -l

# Action ledger current state
python -m action_ledger show --origin emitted

# Intake router history
python -m intake_router history --limit 20
```

---

## Pickup Prompt

> Resume from `docs/handoff-72h-reconciliation.md`. The 72h reconciliation script at `scripts/reconcile-72h.py` needs four refinements: STEERING classification, cross-workspace commit pooling, prompt deduplication, and noise expansion. Then triage the 240 HANGING items into steering/absorbed/unresolved. The data's growth patterns are self-describing in the prompts — do not re-analyze what's recorded, refine the instrument that reads it.
