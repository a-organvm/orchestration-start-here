---
name: fieldwork-intelligence-system
description: Fieldwork system — 4-layer process intelligence. MVP built 2026-03-31 (Layer 1). Spec v4.0 governs Layers 2-4.
type: project
---

## Fieldwork Intelligence System

**Spec:** `docs/superpowers/specs/2026-03-30-fieldwork-intelligence-system-design.md` (v4.0)
**Convergence recs:** `docs/superpowers/specs/2026-03-30-fieldwork-zettelkasten-convergence-recs.md`
**Implementation plan:** `.claude/plans/2026-03-30-fieldwork-mvp-seed-fix.md`

**Status:** Layer 1 MVP built and tested (2026-03-31). Layers 2-4 designed but unbuilt.

### What exists now (Layer 1 MVP)
- `contrib_engine/fieldwork.py` — 94 lines, 3 functions: `record()`, `load_fieldwork()`, `save_fieldwork()`
- `contrib_engine/schemas.py` — 4 enums (ObservationCategory, SpectrumLevel as IntEnum, StrategicTag, ObservationSource) + 2 models (FieldObservation, FieldworkIndex)
- CLI: `python -m contrib_engine fieldwork record` and `fieldwork show` (with --workspace, --category, --min-spectrum filters)
- Tests: 14 new tests in `tests/test_contrib_fieldwork.py`, 164 total suite passing
- Data: `data/fieldwork.yaml` (created on first write, append-only)
- `atom_id: str = ""` field present but unused — zero-cost Zettelkasten hook for Batch 4

### Key design decisions
- SpectrumLevel is IntEnum (AVOID=-2 through ABSORB=+2) — first IntEnum in codebase, justified by ordinal comparison needs
- `strategic` is `list[StrategicTag]` not single tag — observations can carry multiple strategic tags
- IDs: `fo-{workspace_short}-{MMDD}-{seq:03d}` — strips `contrib--` prefix, deterministic within session
- Dual scoring: `scored_by` field distinguishes "agent" (inline, fast) from "orchestrator" (phase transition, calibrated)

### What's next (unbuilt)
- **Layer 2:** `compile_dossier()`, per-workspace category verdicts, `data/dossiers/{workspace}.yaml`
- **Layer 3:** `synthesize()`, cross-repo pattern extraction, `data/fieldwork_synthesis.yaml`
- **Layer 4:** `detect_outputs()`, `produce_output()`, knowledge output pipeline, `data/knowledge_outputs.yaml`
- **Integration:** `record_from_review()` dual-write to outreach, `absorb_to_backflow()` for ABSORB spectrum, shatterpoint → CampaignAction routing
- **SIGNAL_REGISTRY.md:** Shared signal namespace — deferred, belongs in `praxis-perpetua/`

### Remaining vacuums (out-of-realm, not yet dispatched)
- TypeScript dead code: 572 lines in `src/` — archive or delete
- Workflow execution audit: 17 cron workflows never verified for actual execution

**Why:** Closes the self-targeting loop. Contributions generate intelligence → intelligence identifies next contributions.

**How to apply:** Layer 1 is operational — use `fieldwork record` during contribution sessions. Layer 2 (dossier compilation) is the next build target.
