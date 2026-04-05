# SOP-IV-ICA-001: Inflated Claims Audit

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any system with declared maturity states, test counts, or coverage claims)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Cross-references declared status claims (GRADUATED, PRODUCTION, test counts, coverage percentages) against observable evidence, grading each as VERIFIED, UNVERIFIABLE, or CONTRADICTED.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test |
|---|-----------|---------------|
| 1 | System uses a promotion state machine (LOCAL, CANDIDATE, GRADUATED, etc.) and repos have declared promotion states | No formal promotion states; all repos treated equally |
| 2 | Repositories or components claim specific test counts, coverage percentages, or feature completeness | No quantitative claims are made anywhere in documentation or metadata |
| 3 | A promotion review, system audit, or dissolution audit is underway | Routine development with no audit trigger |
| 4 | Discrepancy suspected between declared state and observable reality (e.g., GRADUATED repo with failing CI) | All repos recently verified through independent CI/CD pipeline |
| 5 | seed.yaml or registry.json entries have not been independently verified since initial declaration | All seed.yaml entries are generated from CI output, not manually declared |
| 6 | System has more than 10 repos — manual spot-checking is insufficient | Small system where every repo can be individually verified in minutes |

---

## 2. Protocol Phases

```
ENUMERATE ──> EVIDENCE ──> CHECK ──> GRADE ──> REPORT
     │            │           │         │         │
     │            │           │         │         └─ Inflated Claims Report
     │            │           │         └─ VERIFIED / UNVERIFIABLE / CONTRADICTED
     │            │           └─ Actual evidence collection
     │            └─ Evidence requirement definitions
     └─ Claim inventory
```

### Phase 1: ENUMERATE
**Purpose:** Collect every status or maturity claim across the system.
**Invariant steps:**
1. Extract promotion states from the registry (registry-v2.json or equivalent): for each repo, record the declared `promotion_status`.
2. Extract tier claims from seed.yaml files: `tier` (flagship, standard, infrastructure) and any `maturity` or `status` fields.
3. Search documentation (CLAUDE.md, README.md, AGENTS.md) for quantitative claims: test counts ("638 tests"), coverage percentages ("80% coverage"), feature completeness ("production-ready"), CI status claims ("all checks passing").
4. Search CI workflow files for threshold declarations: coverage minimums, required check lists, quality gate definitions.
5. For each claim, record: source file, claim text, claim type (promotion_state, test_count, coverage, feature_claim, ci_status), claimed value, and repo/component.
**Outputs:** Claims Inventory (repo, source, claim_type, claimed_value, claim_text).
**Ledger emission:** `ica_enumerate_complete` with `{total_claims, repos_with_claims, claim_types}`

### Phase 2: EVIDENCE
**Purpose:** Define the evidence required to verify each type of claim.
**Invariant steps:**
1. For each claim type, define the evidence standard:

   | Claim Type | Evidence Required |
   |------------|-------------------|
   | `GRADUATED` | Zero critical/blocking issues open; CI workflow exists and last run passed; documentation complete (README, CLAUDE.md, seed.yaml all present); no pending blockers in issue tracker |
   | `PRODUCTION` | Test suite exists with passing tests; coverage report exists meeting declared threshold; deployment pipeline functional; no security advisories open |
   | `test_count` (N) | N or more test functions discoverable in test files; test runner executes without import errors |
   | `coverage` (X%) | Coverage report generated within last 30 days showing X% or higher |
   | `feature_claim` ("X is implemented") | Code implementing X exists; at least one test exercises X; X is reachable from documented entry points |
   | `ci_status` ("passing") | Most recent CI run on default branch is green; no required checks are failing or skipped |

2. Record the evidence standard alongside each claim in the inventory.
**Outputs:** Evidence Standards Table (claim_type, evidence_required, verification_method).
**Ledger emission:** `ica_evidence_defined` with `{claim_types_defined}`

### Phase 3: CHECK
**Purpose:** Verify each claim against actual, observable evidence.
**Invariant steps:**
1. For promotion state claims:
   - Check issue tracker for open critical/blocking issues.
   - Locate CI workflow file; check most recent run status via `gh run list` or equivalent.
   - Verify documentation files exist and are non-empty.
   - Search for TODO/FIXME/HACK markers in code that indicate incomplete work.
2. For test count claims:
   - Count test functions: `grep -r "def test_\|it(\|test(\|describe(" tests/` or equivalent.
   - Run the test suite if safe to do so; record pass/fail/error counts.
   - Compare actual count against claimed count.
3. For coverage claims:
   - Check for existing coverage reports (htmlcov/, coverage.xml, .nyc_output/).
   - If no report exists, attempt to generate one: `pytest --cov` or `vitest --coverage`.
   - Compare actual percentage against claimed percentage.
4. For feature claims:
   - Search codebase for implementation of the claimed feature.
   - Check if tests exist that exercise the feature.
   - Verify the feature is reachable from documented entry points (CLI commands, API endpoints, imports).
5. For CI status claims:
   - Query the CI system for the most recent run on the default branch.
   - Check if all required checks passed (not just the most recent commit).
6. Record all evidence found (or not found) for each claim.
**Outputs:** Evidence Collection (claim, evidence_found, evidence_details, verification_date).
**Ledger emission:** `ica_check_complete` with `{claims_checked, evidence_found, evidence_missing}`

### Phase 4: GRADE
**Purpose:** Assign a grade to each claim based on evidence.
**Invariant steps:**
1. For each claim, apply the grading rubric:
   - **VERIFIED** — Evidence exists and confirms the claim. The claimed value matches or exceeds the observed value.
   - **UNVERIFIABLE** — Evidence does not exist to confirm or deny the claim. No test suite to count, no CI to check, no coverage report to read. The claim may be true but cannot be independently confirmed.
   - **CONTRADICTED** — Evidence exists and contradicts the claim. Test count is lower than claimed, CI is failing, coverage is below threshold, GRADUATED repo has critical open issues.
2. For CONTRADICTED claims, compute the gap: claimed value minus actual value (e.g., "claimed 638 tests, found 412" or "claimed GRADUATED, found 17 critical issues open").
3. For UNVERIFIABLE claims, note what infrastructure is missing (no test suite, no CI, no coverage tooling).
4. Compute aggregate statistics: verified rate, unverifiable rate, contradiction rate.
**Outputs:** Graded Claims Table (claim, grade, gap_description, missing_infrastructure).
**Ledger emission:** `ica_grade_complete` with `{verified, unverifiable, contradicted}`

### Phase 5: REPORT
**Purpose:** Produce the final Inflated Claims Report with actionable recommendations.
**Invariant steps:**
1. Compile the **Inflated Claims Report** table: Repo | Claim | Source | Claimed Value | Actual Value | Grade | Gap Description.
2. Sort by severity: CONTRADICTED first (sorted by gap magnitude), then UNVERIFIABLE, then VERIFIED.
3. For each CONTRADICTED claim, recommend one of:
   - **CORRECT** — Update the claim to match reality (demote status, fix test count, update coverage number).
   - **REMEDIATE** — Fix the underlying issue to make the claim true (fix failing tests, close critical issues, add missing infrastructure).
4. For each UNVERIFIABLE claim, recommend:
   - **INSTRUMENT** — Add the missing infrastructure (CI pipeline, test suite, coverage tooling) so the claim becomes verifiable.
5. Compute the **Inflation Index**: contradicted_count / total_claims. Systems with inflation index > 0.2 have systemic honesty debt.
6. Produce a summary: total claims, grade distribution, inflation index, top-3 most inflated repos.
**Outputs:** Inflated Claims Report, Inflation Index, Remediation Recommendations.
**Ledger emission:** `inflated_claims_audited` with `{claims_checked, verified, unverifiable, contradicted}`

---

## 3. Outputs

| Output | Phase | Format | Description |
|--------|-------|--------|-------------|
| Claims Inventory | ENUMERATE | Table | Every status/maturity claim with source and claimed value |
| Evidence Standards Table | EVIDENCE | Table | What evidence is required for each claim type |
| Evidence Collection | CHECK | Table | Actual evidence found (or not found) for each claim |
| Graded Claims Table | GRADE | Table | Each claim graded as VERIFIED, UNVERIFIABLE, or CONTRADICTED |
| Inflated Claims Report | REPORT | Report | Final report with grades, gaps, remediation recommendations, and inflation index |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Test suite exists but cannot be executed (missing dependencies, broken imports) | CHECK phase encounters import errors or environment failures | Record as UNVERIFIABLE with note "test infrastructure broken"; recommend environment fix before re-audit |
| CI system is unreachable or credentials are insufficient | CHECK phase cannot query CI run status | Fall back to local evidence: `.github/workflows/` file existence, git log for CI-related commits; grade CI claims as UNVERIFIABLE |
| Claims are implicit rather than explicit — no file says "GRADUATED" but the registry does | ENUMERATE phase finds fewer claims than expected | Expand search to registry entries, seed.yaml fields, and GitHub repo descriptions; treat registry state as an implicit claim |
| Repo has been archived or deleted since claim was made | CHECK phase finds no repo at expected path | Grade all claims for that repo as UNVERIFIABLE; recommend registry cleanup |
| Audit itself produces false contradictions — test count differs due to parametrized tests or test discovery differences | GRADE phase flags contradictions that seem marginal | For test counts within 10% of claimed value, grade as VERIFIED with note; only flag CONTRADICTED for >10% deviation |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| Promotion Readiness Checklist | ICA is the verification counterpart to promotion readiness | Promotion checklist declares requirements; ICA verifies they are met post-promotion |
| SOP-IV-CBR-001 (Cross-Boundary Reference Mapping) | Undeclared cross-boundary dependencies can inflate maturity claims | CBR undeclared_count feeds ICA as an additional claim to check (implicit claim: "all dependencies are declared") |
| SOP-IV-PAR-001 (Plan Archaeology) | Plans marked COMPLETED are claims that can be audited | PAR ORPHAN output (plans with no implementation evidence) feeds ICA as contradicted feature claims |
| SOP-IV-RCC-001 (Registry Caching Chain Analysis) | Stale caches can cause registry claims to diverge from canonical state | RCC staleness findings feed ICA as evidence that registry-based claims may be outdated |
| Governance Rules (Article VI) | Promotion state machine defines valid states | ICA EVIDENCE phase uses Article VI definitions to determine what evidence each state requires |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** ORGAN-II (Poiesis) — 32 repos with 7 GRADUATED; generative art repos are likely to have feature claims that are difficult to verify programmatically, stress-testing the evidence framework
