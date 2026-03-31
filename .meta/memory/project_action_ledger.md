---
name: project_action_ledger
description: Action Ledger — system-wide process recording infrastructure. Synthesizer paradigm applied to ideas. Plan approved 2026-03-31.
type: project
---

## Action Ledger

**Plan:** `.claude/plans/scalable-baking-conway.md`
**Status:** Phases 1-4 BUILT + COMMITTED + PUSHED (2026-03-31, commit add3902). Phase 5 (integration) remains.
**Location:** `orchestration-start-here/action_ledger/`

Records the process of doing — ideas as they move through parameter space, their composition into sequences, sequences into chains, chains into a project whole.

**Conceptual prior art:** Alchemical Synthesizer (ORGAN-II, `organvm-ii-poiesis/alchemical-synthesizer`). Module registry → parameter registry. Patch bay → route system. CHRONOS automation → parameter trajectories. Euclidean rhythms → cycle detection.

### What exists (Phases 1-4, 57 tests, 221 total suite)
- `schemas.py` (185 lines) — Action, Sequence, Chain, Route, ParamAxis, ParamRegistry, RouteKind, ROUTE_INVERSES
- `ledger.py` (367 lines) — record() atomic (append+sequence+registry), compose_chain(), close_session(), _compute_arc(), full YAML persistence
- `routes.py` (193 lines) — build_route_graph(), routes_from/to, find_producers/consumers, trace_lineage(), provenance_comment/yaml_header
- `cycles.py` (274 lines) — detect_verb_cycles(), detect_trajectory_cycles(), detect_intent_cycles(), detect_stalls(), detect_all_cycles()
- `cli.py` (441 lines) — record, show, sequence {show,close,intent}, chain {show,close-session}, routes {from,to,lineage}, cycles, params
- `__main__.py` (38 lines) — standalone CLI entry
- `data/` — actions.yaml, sequences.yaml, param_registry.yaml (seed data from CLI test)

### Git state (session close)
- **All committed+pushed** (add3902): schemas.py, ledger.py, routes.py, cycles.py, cli.py, __init__.py, __main__.py, test_action_ledger.py (57 tests), data files, seed.yaml, CLAUDE.md

### What remains
- **Phase 5 — Integration:** Wire contrib_engine to emit actions into the ledger (IRF-OSS-032)
- **Convergence:** Action ledger + dispatch ledger must converge (IRF-OSS-033, see project_temporal_convergence.md)
- **Design spec:** Write formal spec to `docs/superpowers/specs/2026-03-31-action-ledger-design.md` (IRF-OSS-034)

### Completed this session
- ✅ seed.yaml updated (action_ledger modules, test_count=221, produces action_ledger_data)
- ✅ CLAUDE.md updated (directory structure + action_ledger section)
- ✅ IRF items created (IRF-OSS-032 through IRF-OSS-035, pushed to meta-organvm)
- ✅ All code committed+pushed (local:remote=1:1)

**Why:** User repeats cycles across sessions without realizing until too late. This system makes cycles visible so they can be formalized into new systems. Recursive proof generalized.

**How to apply:** Phases 1-4 operational. Next: commit+push the uncommitted work, then Phase 5 integration.
