# SOP: Communications & Correspondence — Relay Protocol

**Version:** 1.0
**Date:** 2026-04-02
**Session:** S51 (executed S52)
**Archetype:** RELAY-CIRCUIT

---

## Overview

This SOP unifies all communication subsystems under one lifecycle. It governs inbound correspondence (mail triage), inter-session handoffs, outbound correspondence, and cross-channel dispatch.

**Scope:** All channels — email, GitHub, LinkedIn, iMessage, Slack, postal.
**Trigger modes:** Recurring (daily triage), on-demand (ad-hoc correspondence), event-driven (handoff relay).

---

## The Lifecycle

```
INJECT → CREATE → OPERATE → VERIFY → PRECIPITATE → STOP
```

| Phase | What Happens | Trigger |
|-------|--------------|---------|
| **INJECT** | Raw correspondence enters the system | New email, handoff prompt, manual draft |
| **CREATE** | Classification and initial routing | Domain detection, priority assignment |
| **OPERATE** | Composition, handoff, dispatch | Content creation, verification |
| **VERIFY** | Confirmation tracking, closure | Receipt, response, timeout |
| **PRECIPITATE** | Receipt deposit, next portal seeding | Session close |
| **STOP** | Agent stops, operator decides continuation | Hard stop |

---

## State Machine

```
RECEIVED → TRIAGED → COMPOSED → DISPATCHED → CONFIRMED → CLOSED
```

| State | Description | Next State |
|-------|-------------|-------------|
| **RECEIVED** | Inbound correspondence logged | TRIAGED |
| **TRIAGED** | Classified by domain, priority, channel | COMPOSED (if reply needed) or DISPATCHED (if just logging) |
| **COMPOSED** | Draft created, protocol validated | DISPATCHED |
| **DISPATCHED** | Sent via appropriate channel | CONFIRMED |
| **CONFIRMED** | Response received or timeout passed | CLOSED |
| **CLOSED** | Archived, no further action | — |

---

## Phase Details

### Phase 1: INJECT (Received)

**Entry:** Any new correspondence enters the system.

**Actions:**
- Log to action_ledger with `verb: received`
- Extract sender, subject, channel, timestamp
- Route to appropriate handling path

**Output:** `act-SXX-XXXX-001` in action_ledger

---

### Phase 2: CREATE (Triaged)

**Entry:** Correspondence requires classification.

**Actions:**
- Apply IntakeDomain (CORRESPONDENCE, PIPELINE, etc.)
- Assign priority (P0-P4)
- Determine response required (yes/no/monitor)
- Log verb: `triaged`

**Output:** `act-SXX-XXXX-002` in action_ledger

---

### Phase 3: OPERATE (Composed)

**Entry:** Response required.

**Actions:**
- Compose draft following Outreach Protocol (P-I through P-VII)
- Validate against existing correspondence history
- Apply channel-specific tone (email vs GitHub vs LinkedIn)
- Log verb: `composed`

**Output:** Draft in appropriate location (Drafts folder, pipeline drafts, etc.)

---

### Phase 4: OPERATE (Relayed/Handoff)

**Entry:** Inter-session context needs transfer.

**Actions:**
- Format CONTEXT/TASK/DISCIPLINE/PROVENANCE blocks
- Verify receiving location is accessible
- Log verb: `relayed`

**Output:** Handoff document at target location

---

### Phase 5: OPERATE (Dispatched)

**Entry:** Correspondence ready to send.

**Actions:**
- Send via channel-specific method
- Log verb: `dispatched`
- Record destination, timestamp

**Output:** `act-SXX-XXXX-00X` in action_ledger

---

### Phase 6: VERIFY (Confirmed/Closed)

**Entry:** Sent, awaiting response or timeout.

**Actions:**
- Monitor for response (24h for email, 48h for LinkedIn)
- On response: log verb: `confirmed`, update state
- On timeout: log verb: `closed`, archive

**Output:** `act-SXX-XXXX-00X` in action_ledger

---

### Phase ε: PRECIPITATE

**Entry:** Session complete.

**Actions:**
- Write RECEIPT.md with forward deposit
- Seed next portal's BRIEFING.md if predictable
- Commit all artifacts
- Push to origin

**Output:** RECEIPT.md in portal directory

---

### Phase STOP

**Entry:** Agent stops.

**Actions:**
- Do NOT delete portal directory
- Do NOT continue to next task
- Operator reads RECEIPT and decides continuation

**Output:** Session closed

---

## Channel-Specific Guidance

### Email
- Tone: Professional, concise, action-oriented
- Protocol: P-I through P-VII mandatory
- State transitions logged to action_ledger

### GitHub
- Tone: Technical, reference-linked, brief
- State: Issues, PRs, discussions tracked separately
- Dispatched = comment submitted or PR created

### LinkedIn
- Tone: Professional, value-first, no pitch
- State: Connection requests, messages, inMails tracked
- Dispatched = connection made or message sent

### iMessage/Slack
- Tone: Casual, synchronous-appropriate
- State: Quick messages, not archived long-term
- Dispatched = message sent

### Postal
- Tone: Formal, physical address required
- State: Physical mail tracked separately
- Dispatched = shipped

---

## Integration Points

### Intake Router
- `IntakeDomain.CORRESPONDENCE` routes to this SOP
- Keywords: correspondence, email, outbound, inbound, reply, draft, follow-up, message, contact

### Action Ledger
- All state transitions logged with verbs: received, triaged, composed, dispatched, confirmed, closed
- Sequence: seq-S51-001 (relay circuit)
- Chain: chain-S51-001 (phase chain)

### Handoff Pattern
- Existing CONTEXT/TASK format preserved
- Becomes Phase 4 (relayed) in this SOP
- Provenance chain verified

---

## Out of Scope

- Real-time chat (iMessage, SMS) — state logged but not full SOP
- Billing disputes — routes to BILLING domain
- Pipeline applications — routes to PIPELINE domain
- Emergency correspondence — P0 priority, skip to DISPATCHED

---

## Related Documents

- `docs/mail-triage-2026-04-01.md` — Phase 1-2 detail
- `docs/handoff-*.md` — Phase 4 format
- `intake_router/router.py` — CORRESPONDENCE domain
- `action_ledger/data/actions.yaml` — State transitions

---

**End of SOP**