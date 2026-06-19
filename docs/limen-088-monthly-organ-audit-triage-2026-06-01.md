# LIMEN-088: Monthly Organ Audit — 2026-06-01 Manual Triage

**Triage date:** 2026-06-19
**Repository:** `a-organvm/orchestration-start-here`
**Source issue:** [#165](https://github.com/a-organvm/orchestration-start-here/issues/165) — "Monthly Organ Audit — 2026-06-01" (auto-generated, labels `audit`, `monthly`)
**Task:** Monthly Organ Audit — 2026-06-01 manual triage

## What issue #165 is

Issue #165 is filed automatically by the `monthly-organ-audit.yml` workflow
(`.github/workflows/monthly-organ-audit.yml`), which runs on the 1st of each month
(`cron: 0 2 1 * *`). Each run:

1. Runs `scripts/organ-audit.py --registry registry.json --governance governance-rules.json --output audit-report.md`
2. Runs `scripts/calculate-metrics.py --registry registry.json --output metrics.json`
3. Opens an issue titled `Monthly Organ Audit — <date>` containing the report + a
   per-organ metrics table, labeled `audit` and `monthly`.
4. Stamps `registry.json` with `last_audit` / `audit_history`.

"Manual triage" of this issue means reviewing the audit findings, dispositioning the
alerts, and acting on anything the automated pass cannot resolve on its own.

> **Access note.** This triage was performed from the local checkout. Live GitHub
> access (`gh`, the GitHub connector, and `WebFetch`) was unavailable in the execution
> environment, so the issue body itself could not be re-read online. The findings below
> are grounded entirely in committed repository files — the audit workflow, the two
> audit scripts, `registry.json`, `governance-rules.json`, and the committed
> `audit-report.md` — which is sufficient to triage the audit and is in fact where the
> most important finding lives.

## Headline finding — the automated audit is reading a retired registry

**Severity: HIGH (silent false all-clear).**

`registry.json` in this repository was **retired on 2026-02-18**. It is now a redirect
stub with no `organs` key:

```json
{
  "_redirect": "This file has been retired. Use registry-v2.json from organvm-corpvs-testamentvm.",
  "_source": "https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/registry-v2.json",
  "_retired": "2026-02-18",
  "_reason": "Registry consolidation — single source of truth in organvm-corpvs-testamentvm/registry-v2.json"
}
```

Both audit scripts still take `registry.json` as their source of truth, and both read
`registry.get("organs", {})`. Against the stub, in standalone mode (no `organvm-engine`
installed), they do **not** error — they silently produce empty/zeroed output:

- `scripts/calculate-metrics.py` iterates the eight organ IDs, hits
  `if not organ: continue` for every one, and returns `total_repos: 0`,
  `operational_organs: 0`, `completion: 0.0`, `organs: {}`.
- `scripts/organ-audit.py` produces an empty `## Organ Status` section,
  `Organs operational: 0/7`, no warnings, and the message
  `No critical alerts or warnings.`

**Consequence:** any 2026-06-01 monthly audit that ran the standalone path reported a
green "all clear" describing **zero** repos and **zero** operational organs — a false
all-clear that masks the real system instead of auditing it. (If `organvm-engine` is
installed in CI, behavior depends on whether `_engine_load_registry` follows the
`_source` redirect; the local/standalone path, which the workflow falls back to, is
definitively broken.)

This is the primary item to action from the 2026-06-01 audit.

## Last-good audit snapshot (committed `audit-report.md`)

The committed `audit-report.md` predates the stub and reflects the last run that saw a
real registry. It is the most recent *meaningful* organ snapshot available locally:

| Organ | Status | Repos (documented) | With deps |
|-------|--------|--------------------|-----------|
| ORGAN-I  | SILVER SPRINT COMPLETE | 18 (17) | 7/18 |
| ORGAN-II | SILVER SPRINT COMPLETE | 22 (14) | 11/22 |
| ORGAN-III| SILVER SPRINT COMPLETE | 21 (20) | 4/21 |
| ORGAN-IV | SILVER SPRINT COMPLETE | 9 (5)   | 4/9  |
| ORGAN-V  | SILVER SPRINT COMPLETE | 2 (1)   | 1/2  |
| ORGAN-VI | SILVER SPRINT COMPLETE | 3 (0)   | 0/3  |
| ORGAN-VII| SILVER SPRINT COMPLETE | 4 (0)   | 0/4  |

- **Circular dependencies:** none detected
- **Direction violations:** none (governance `articles.II.allowed_dependencies`)
- **Total repos:** 79 · **Documented:** 57 · **Organs operational:** 7/7 · **Dependency violations:** 0
- **Warnings (1):** ORGAN-II — 1 repo not fully documented: `artist-toolkits-templates`

### Staleness cross-check

The live system variables surfaced in `CLAUDE.md` (Ontologia, last updated
2026-04-14) report **89 active repos / 145 total / 10 operational organs**, against the
audit snapshot's **79 repos / 7 organs**. The gap is consistent with the registry having
been retired: the in-repo audit corpus stopped tracking the system once the single
source of truth moved to `organvm-corpvs-testamentvm/registry-v2.json`.

## Triage dispositions

| # | Finding | Severity | Disposition |
|--:|---------|----------|-------------|
| 1 | Audit pipeline reads retired `registry.json` stub → silent all-zeros report | HIGH | **Remediate** — repoint scripts/workflow at the canonical registry; add a non-empty guard (see Recommendations). Tracked by this triage. |
| 2 | `audit-report.md` / metrics are stale vs. live Ontologia counts (79 vs 89 repos, 7 vs 10 organs) | MEDIUM | **Consequence of #1.** Resolves once #1 is fixed and a real audit re-runs. |
| 3 | ORGAN-II `artist-toolkits-templates` not fully documented | LOW | **Carry forward.** Documentation-only follow-up; cannot be confirmed fixed until the audit reads live data again. Re-verify after #1. |
| 4 | No structural integrity failures in last-good snapshot (0 cycles, 0 direction violations) | — | **No action.** Clean as of last real audit; re-confirm after #1. |

## Recommendations (remediation for finding #1)

1. **Point the audit at the canonical registry.** Update
   `.github/workflows/monthly-organ-audit.yml`, `scripts/organ-audit.py`, and
   `scripts/calculate-metrics.py` to read `registry-v2.json` from
   `meta-organvm/organvm-corpvs-testamentvm` (fetch it in CI, or follow the `_source`
   URL in the stub), instead of the retired local `registry.json`.
2. **Fail loud on an empty registry.** Add a guard in both scripts: if
   `registry.get("organs")` is empty/absent, exit non-zero with a clear error rather
   than emitting a zeroed "all clear." This converts the silent false-pass into a
   visible CI failure the next time the source goes missing.
3. **Stop stamping the retired file.** The workflow's final step writes `last_audit` /
   `audit_history` back into `registry.json`; once the source is repointed, either drop
   that step or redirect it to wherever the canonical audit history should live.
4. **Re-run after the fix** and re-triage findings #2 and #3 against real data.

## Completion

The 2026-06-01 monthly audit has been triaged. The actionable outcome is finding #1:
the monthly-organ-audit pipeline is auditing a registry that was retired on 2026-02-18
and therefore reports a false all-clear. Findings #2 and #3 are downstream of #1 and
should be re-verified once the audit source is repointed at
`organvm-corpvs-testamentvm/registry-v2.json`. No structural integrity violations were
present in the last real snapshot.
