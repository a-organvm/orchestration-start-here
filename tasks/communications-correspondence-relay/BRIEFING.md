# Briefing: Communications & Correspondence — The Relay Protocol

**Session:** S51 | **Date:** 2026-04-01
**Archetype:** RELAY-CIRCUIT
**Plan source:** `.claude/plans/2026-04-01-communications-correspondence-relay-protocol.md`

---

## Vacuum

Four communication subsystems. No shared lifecycle. No state machine. No cross-channel dispatch.

| Fragment | What it does | What it doesn't |
|----------|-------------|-----------------|
| Mail triage | Inbound sweep → classify → route | No outbound. No cross-channel. No response tracking. |
| Handoff docs | Inter-session context relay | Ad-hoc format. No provenance. No verification. |
| PR discipline | GitHub correspondence etiquette | Behavioral only. Not connected to lifecycle. |
| Outbound | **Nothing. The vacuum.** | No process. No tracking. No state. |

## Ideal State

One SOP. Six phases. One state machine. All channels.

```
SWEEP → CLASSIFY → COMPOSE → RELAY → DISPATCH → VERIFY
  ↓         ↓          ↓         ↓         ↓          ↓
RECEIVED → TRIAGED → COMPOSED → RELAYED → DISPATCHED → CONFIRMED → CLOSED
```

## Campaign Dependencies

| What | State | Door |
|------|-------|------|
| Action ledger | Built | Ready to consume correspondence verbs |
| Intake router | Built | Needs CORRESPONDENCE domain (K2) |
| Mail triage pattern | Exists | Becomes Phase 1-2 (plasticity, not preservation) |
| Handoff pattern | Exists in 3 docs | Becomes Phase 4 (formalized, not ad-hoc) |
| Contrib engine monitor | Built | PR correspondence already flows — SOP governs the human layer |

## Deliverables

| Key | Artifact | Door |
|-----|----------|------|
| K1 | `docs/sop-communications-correspondence.md` | CREATE |
| K2 | `intake_router/router.py` CORRESPONDENCE domain | EDIT |
| K3-K5 | `action_ledger/data/{actions,sequences,chains}.yaml` | APPEND |
