<!-- ORGANVM:AUTO:START -->
## Agent Context (auto-generated — do not edit)

This repo participates in the **ORGAN-IV (Orchestration)** swarm.

### Active Subscriptions
- Event: `repo.created` → Action: Update registry, assign seed.yaml template
- Event: `ci.passed` → Action: Check if repo qualifies for promotion
- Event: `essay.published` → Action: Trigger ORGAN-VII distribution workflow

### Production Responsibilities
- **Produce** `governance-rules` for all
- **Produce** `health-reports` for all
- **Produce** `promotion-decisions` for all

### External Dependencies
- **Consume** `registry-updates` from `any`
- **Consume** `essay-notifications` from `ORGAN-V`

### Governance Constraints
- Adhere to unidirectional flow: I→II→III
- Never commit secrets or credentials

*Last synced: 2026-02-24T12:41:28Z*
<!-- ORGANVM:AUTO:END -->
