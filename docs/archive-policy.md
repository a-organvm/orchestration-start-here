# Automated Archive Policy

> **Governance**: Article VI (Promotion State Machine)
> **Scope**: All repositories across the eight-organ system
> **Version**: 1.0

---

## Purpose

Repositories that are no longer actively maintained consume governance attention, CI minutes, and cognitive overhead. This policy defines automated criteria for identifying archive candidates, a warning period for human review, and a reversible archive process.

---

## Archive Criteria

A repository becomes an **archive candidate** when ALL three conditions are met:

| # | Condition | Threshold | Rationale |
|---|---|---|---|
| 1 | **No commits** | >180 days (6 months) | Extended inactivity signals abandonment or completion |
| 2 | **Status = LOCAL** | >12 months at LOCAL | Repos that never progressed past LOCAL were likely experiments |
| 3 | **Zero dependents** | No other repo declares a `consumes` edge to this repo | Archiving a repo with dependents would break the dependency graph |

All three conditions must be true simultaneously. A repo with no commits but active dependents is **not** an archive candidate — it is load-bearing infrastructure that needs maintenance, not archival.

---

## Monthly Audit

The `organ-audit.py` script generates archive candidates as part of its monthly run. The audit:

1. Queries `registry-v2.json` for all repos with `promotion_status: LOCAL`
2. Checks last commit date via git log or GitHub API
3. Checks the dependency graph for inbound `consumes` edges
4. Outputs a list of repos meeting all three criteria

The audit output is appended to the monthly audit report and posted as a GitHub issue in `orchestration-start-here` with the label `archive-candidate`.

---

## Warning Period

Archive candidates enter a **30-day warning period** before any action is taken.

### During the Warning Period

1. The archive-candidate issue is created with:
   - Repository name and organ
   - Last commit date
   - Current promotion status
   - Dependency graph excerpt (confirming zero dependents)
   - Explicit deadline: "Will be archived on YYYY-MM-DD unless action is taken"

2. The repo owner (or organ lead) may prevent archival by:
   - Making a meaningful commit (not an empty commit or whitespace change)
   - Promoting the repo to CANDIDATE or higher
   - Adding `archive_exempt: true` to the repo's `seed.yaml`
   - Commenting on the issue with a justification for keeping the repo active

3. If no action is taken within 30 days, the repo proceeds to archival.

---

## Archive Process

When the warning period expires without intervention:

### Step 1: Update Registry

Set `promotion_status: ARCHIVED` in `registry-v2.json`:

```json
{
  "name": "repo-name",
  "organ": "ORGAN-X",
  "promotion_status": "ARCHIVED",
  "archived_date": "2026-MM-DD",
  "archived_reason": "automated-policy: no commits >180d, LOCAL >12mo, zero dependents"
}
```

### Step 2: Archive on GitHub

Archive the repository on GitHub via the API or UI. This makes the repo read-only but preserves all history, issues, and artifacts.

```bash
gh repo archive <org>/<repo> --yes
```

### Step 3: Update Dependents

Verify that no `consumes` edges reference the archived repo. (The audit should have already confirmed this, but verify as a safety check.)

### Step 4: Close the Archive-Candidate Issue

Close the issue with a comment confirming archival, including the date and registry commit hash.

### Step 5: Update seed.yaml

Add `promotion_status: ARCHIVED` and `archived_date` to the repo's `seed.yaml`. This is a final commit before the repo becomes read-only:

```yaml
promotion_status: ARCHIVED
archived_date: "2026-MM-DD"
```

---

## Reversal Process

Archival is reversible. Unarchiving a repo requires:

1. **Unarchive on GitHub**: `gh repo unarchive <org>/<repo> --yes`
2. **Reset promotion status**: Set `promotion_status: LOCAL` in both `registry-v2.json` and `seed.yaml`
3. **Re-enter the promotion pipeline**: The repo must progress through `LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED` like any new repo. There is no shortcut back to the repo's pre-archive status.
4. **Create a tracking issue**: Document why the repo was unarchived and what work is planned

This deliberate friction ensures that unarchiving is intentional and that the repo receives active maintenance going forward.

---

## Exceptions

### archive_exempt Flag

Repos may be marked exempt from automated archival by adding the following to their `seed.yaml`:

```yaml
archive_exempt: true
archive_exempt_reason: "Long-term reference material, accessed seasonally"
```

The `archive_exempt_reason` field is required. Valid reasons include:

- Long-term reference material with seasonal access patterns
- Dependency of a system that checks for its existence (e.g., org profile repos)
- Intentionally stable — no changes expected but repo must remain accessible
- Pending external dependency (e.g., waiting for upstream API availability)

Invalid reasons (will be flagged in audit):

- "Might need it someday" (too vague)
- "Haven't decided yet" (indecision is not exemption)
- No reason provided (the field is required)

### Manual Override

The system administrator may override the automated policy for any repo by commenting on the archive-candidate issue with `OVERRIDE: <reason>`. This extends the warning period by 90 days and requires a follow-up decision.

---

## Governance Integration

This policy implements a specific path in the Article VI promotion state machine:

```
LOCAL (>12 months) + no commits (>180 days) + zero dependents
    → ARCHIVE CANDIDATE (30-day warning)
        → ARCHIVED (read-only on GitHub)
            → LOCAL (if unarchived, must re-promote)
```

The key governance principle: **archival is administrative, not punitive.** Archived repos retain their full history and can be restored. The purpose is to reduce active governance surface area, not to delete work.

---

## References

- [governance-rules.json](../../governance-rules.json) — Article VI (Promotion State Machine)
- [tier-based-testing-matrix.md](tier-based-testing-matrix.md) — Testing requirements by tier
- [seed-schema/](seed-schema/) — seed.yaml schema including `archive_exempt` field
- [ci-templates.md](ci-templates.md) — CI workflow templates
