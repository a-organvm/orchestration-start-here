# Tier-Based Testing Matrix

> **Governance**: Article I (Registry as Source of Truth), Article VI (Promotion State Machine)
> **Scope**: All repositories across the eight-organ system
> **Version**: 1.0

---

## Overview

Every repository in the ORGANVM system has a **tier** declared in its `seed.yaml`: flagship, standard, infrastructure, or stub. The tier determines the minimum testing requirements for CI, promotion, and governance compliance.

This document expands the testing guidance from [ci-templates.md](ci-templates.md) into a standalone reference matrix.

---

## Testing Matrix

| Requirement | Flagship | Standard | Infrastructure | Stub |
|---|---|---|---|---|
| **Unit tests** | Required | Required | Optional | Not required |
| **Contract tests** | Required | Optional | Required | Required |
| **Integration tests** | Required | Not required | Not required | Not required |
| **CI matrix** (multi-version) | Required (2+ versions) | Single version | Single version | Not required |
| **Coverage tracking** | Required (>=80%) | Required (tracked) | Optional | Not required |
| **Coverage threshold** | >=80% statements | No minimum | No minimum | N/A |
| **Security scanning** | Required (CodeQL or equivalent) | Not required | Not required | Not required |
| **Lint/format** | Required | Required | Optional | Not required |
| **Type checking** | Required (strict) | Required | Optional | Not required |
| **Smoke tests** | Required | Optional | Required | Not required |
| **Schema validation** | Required | Required | Required | Required |

---

## Tier Definitions

### Flagship

Flagship repos are the system's load-bearing walls. They have the highest testing requirements because failures cascade across the system.

**Examples**: `orchestration-start-here`, `agentic-titan`

**Testing requirements**:
- Full unit test suite with >=80% statement coverage
- Contract tests validating all declared `produces`/`consumes` edges
- Integration tests covering cross-component interactions
- CI runs on a version matrix (e.g., Python 3.11 + 3.12, or Node 20 + 22)
- Security scanning via CodeQL or equivalent static analysis
- Lint, format, and type checking enforced in CI (ruff + mypy for Python, tsc --noEmit for TypeScript)

### Standard

Standard repos are the majority of the system. They require solid fundamentals but not the full flagship treatment.

**Examples**: `agent--claude-smith`, `a-i--skills`, `petasum-super-petasum`

**Testing requirements**:
- Unit tests covering core functionality
- Single CI version (latest stable)
- Coverage tracked but no minimum threshold enforced
- Contract tests optional but recommended for repos with `produces`/`consumes` edges
- Lint and type checking enforced

### Infrastructure

Infrastructure repos provide shared tooling, CI templates, org profiles, and community health files. Their primary risk is breaking other repos' workflows, so contract validation is critical even though they may have minimal application code.

**Examples**: `.github` (org profile), CI workflow templates

**Testing requirements**:
- Contract validation: all YAML/JSON schemas parse correctly
- Smoke tests: workflows and templates render without errors
- Coverage optional (infrastructure repos often have more config than code)
- Schema validation required

### Stub

Stub repos are placeholders, early-stage experiments, or archived projects being held for future use. They must meet only the minimum governance requirements.

**Examples**: `universal-node-network` (minimal/early stage)

**Testing requirements**:
- `seed.yaml` parses and validates against the schema
- `README.md` exists
- No code tests required

---

## Contract Tests in ORGANVM

A "contract test" in ORGANVM has a specific meaning that differs from the general software engineering concept. ORGANVM contract tests verify three things:

### 1. seed.yaml Validates

The repository's `seed.yaml` must:
- Parse as valid YAML
- Conform to the seed schema (see [seed-schema/](seed-schema/))
- Declare a valid `organ` value matching its GitHub organization
- Declare a valid `tier` matching its testing obligations
- Declare a valid `promotion_status` from the state machine

### 2. Dependency Graph Has No Back-Edges

The `produces` and `consumes` edges declared in `seed.yaml` must respect Article II's unidirectional dependency flow:

```
ORGAN-I -> ORGAN-II -> ORGAN-III
             (no back-edges)
ORGAN-IV orchestrates all
ORGAN-V observes (read-many, write-one)
ORGAN-VII consumes only
```

The `validate-deps.py` script in this repo enforces this constraint. Any `consumes` edge that flows backward (e.g., ORGAN-I consuming from ORGAN-III) is a contract violation.

### 3. Registry Entry Exists

Every repo with a `seed.yaml` must have a corresponding entry in `registry-v2.json` (or `registry.json` for legacy repos). The registry entry must match the `seed.yaml` on critical fields: organ, tier, and promotion_status.

---

## Promotion Gates

Testing requirements interact with the promotion state machine. Each promotion transition has a testing gate:

| Transition | Testing Gate |
|---|---|
| LOCAL -> CANDIDATE | seed.yaml validates, README exists |
| CANDIDATE -> PUBLIC_PROCESS | All tier-required tests pass in CI, contract tests pass |
| PUBLIC_PROCESS -> GRADUATED | Full tier requirements met for 30+ days, no regression |
| Any -> ARCHIVED | No testing gate (archival is administrative) |

A repo cannot be promoted if it does not meet the testing requirements for its tier at the target status level.

---

## Implementation

### CI Template Selection

Use the CI templates from [ci-templates.md](ci-templates.md) based on tier:

| Tier | Template |
|---|---|
| Flagship | `ci-full.yml` (matrix, coverage, security) |
| Standard | `ci-standard.yml` (single version, lint, test) |
| Infrastructure | `ci-minimal.yml` (schema validation, smoke) |
| Stub | `ci-stub.yml` (seed.yaml validation only) |

### Adding Tests to an Existing Repo

1. Check the repo's tier in `seed.yaml`
2. Compare current test coverage against this matrix
3. Add missing test categories in priority order: contract tests first, then unit tests, then integration
4. Update CI workflow to match the tier's template

---

## References

- [ci-templates.md](ci-templates.md) — CI workflow templates and configuration
- [governance-rules.json](../../governance-rules.json) — Articles I, II, VI
- [seed-schema/](seed-schema/) — seed.yaml schema definition
- [adr/sdlc-to-organ-mapping.md](adr/sdlc-to-organ-mapping.md) — SDLC phases mapped to organs
