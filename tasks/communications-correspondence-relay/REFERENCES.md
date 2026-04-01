# Keys — Doors Requiring Opening

Only the files that need to be read, modified, or created. Nothing else.

---

## Doors to Open (files to modify or create)

| Key | Door | Operation | Why |
|-----|------|-----------|-----|
| K1 | `docs/sop-communications-correspondence.md` | **CREATE** | The SOP. Does not exist. This is the primary artifact. |
| K2 | `intake_router/router.py` lines 25-34, 83-132, 134-166 | **EDIT** | Add CORRESPONDENCE to `IntakeDomain` enum, `DOMAIN_KEYWORDS`, `ROUTING_TABLE` |
| K3 | `action_ledger/data/actions.yaml` | **APPEND** | 3 actions for S51 event |
| K4 | `action_ledger/data/sequences.yaml` | **APPEND** | 1 sequence for S51 |
| K5 | `action_ledger/data/chains.yaml` | **APPEND** | 1 chain for S51 |

---

## Context Stream — Minimum Data to Proceed

Read these before touching anything. This is the complete picture required for matter-disturbance.

### The Shape (what the SOP looks like)

| File | What it gives you | Read depth |
|------|-------------------|------------|
| `docs/sop-war-master-protocol.md` | SOP structural template — authority, purpose, laws, phases, injection pattern | Full |
| `docs/mail-triage-2026-04-01.md` | Phase 1-2 prior art — formal sort table, P0/P1/P2/Noise classification, handler assignment, ledger state footer | Full |
| `docs/handoff-72h-reconciliation.md` | Phase 4 prior art — handoff format, "What Needs Doing" sections, integration points | Full |

### The Wiring (how artifacts connect to code)

| File | What it gives you | Read depth |
|------|-------------------|------------|
| `action_ledger/schemas.py` lines 15-30, 57-97 | `ActionOrigin`, `RouteKind`, `Route`, `Action` — the data types for ledger entries | Targeted |
| `intake_router/router.py` lines 25-34, 83-166 | `IntakeDomain` enum, `DOMAIN_KEYWORDS` dict, `ROUTING_TABLE` dict — the three extension points | Targeted |

### The Tension (what must NOT be broken)

| Constraint | Source | Consequence of violation |
|------------|--------|--------------------------|
| Mail-triage format must survive as Phase 1-2 | `docs/mail-triage-2026-04-01.md` | Future triage events depend on this structure |
| Handoff CONTEXT/TASK block format must survive as Phase 4 | `docs/handoff-*.md` | Existing handoff relay prompts would break |
| Action ledger append-only | `action_ledger/ledger.py` | Never overwrite existing YAML entries |
| Intake router enum order | `intake_router/router.py` | UNKNOWN must remain last |
| 240 tests must still pass | `tests/` | `python -m pytest tests/ -q` |

---

## Channels (for SOP content, not for this task)

The SOP must document these channels. You do not need API access to write the SOP — you need to know the channel landscape exists:

```
Email (Gmail API/MCP) · GitHub (gh CLI/MCP) · iMessage (manual)
LinkedIn (manual) · Slack (API) · USPS (Informed Delivery)
```
