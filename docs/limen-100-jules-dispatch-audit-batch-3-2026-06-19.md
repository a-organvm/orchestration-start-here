# LIMEN-100: Jules Dispatch Audit, Batch 3

**Audit date:** 2026-06-19  
**Prior context:** Audited 2026-06-01 from Jules-ready batch  
**Repository:** `a-organvm/orchestration-start-here`  
**Task:** Audit GitHub orgs for open issues suitable for Jules dispatch

## Scope

Audited live GitHub issue state through the GitHub connector for the installed ORGANVM accounts:

- `organvm-i-theoria`
- `organvm-ii-poiesis`
- `organvm-iii-ergon`
- `organvm-iv-taxis`
- `organvm-v-logos`
- `organvm-vi-koinonia`
- `organvm-vii-kerygma`
- `meta-organvm`
- `a-organvm`

The connector installation for `organvm` exposed no repositories during this run. The user account `4444J99` was treated as out of scope because the task names GitHub orgs. Local `gh` was present but unusable because its token is invalid, and direct network access to `api.github.com` was blocked by the sandbox, so all live issue findings below come from the GitHub connector.

## Method

The connector does not support free-form `org:` issue search without an explicit repository scope, so the audit used repo-scoped searches over repositories visible from each org installation. Search terms emphasized the current activation corpus and dispatchable work:

- `ACTIVATION AUDIT`
- `EV Activation Audit`
- `ship-soon`
- `ship-now`
- `Acceptance`
- targeted full open-issue search for `a-organvm/orchestration-start-here`

Jules-ready means:

- the issue names one repo and one bounded change surface
- the work is code/docs/static-site editing, not account, billing, secret, deployment, or external-human work
- the issue body includes acceptance criteria, an activation path, or a PR candidate
- the expected verification can be done with local tests, markdown/render review, static checks, or CI
- the task should fit one isolated PR without cross-org write side effects

## Batch 3 Dispatch Queue

### Tier 1: Dispatch Now

| Rank | Issue | Why Jules-ready | Verification |
|---:|---|---|---|
| 1 | `a-organvm/orchestration-start-here#159` Document the promotion state machine with a Mermaid diagram | Documentation-only, clear source file (`governance-rules.json`), explicit acceptance criteria, estimated 20 minutes | README renders; state diagram covers all states/transitions |
| 2 | `a-organvm/orchestration-start-here#160` Add dependency graph visualization using Mermaid flowchart | Documentation-only, clear source file (`governance-rules.json`), explicit acceptance criteria, estimated 20 minutes | README renders; all allowed edges represented |
| 3 | `organvm-iii-ergon/specvla-ergon--avditor-mvndi#16` Activation audit ship-now hygiene | Small PR candidate: fix `metadataBase` fallback and add `.env.local.example` with variable names only | Typecheck/build if available; inspect OG URL fallback |
| 4 | `organvm-iii-ergon/organvm-iii-ergon.github.io#1` Static landing page content drift | One-file `index.html` update replacing dead repo-card links with current repo cards | Static HTML review; Pages auto-deploys from main |
| 5 | `organvm-vii-kerygma/.github#7` Org profile link/count drift | Pure README table/count update to post-transfer `a-organvm` links | Markdown review; no workflow changes |
| 6 | `organvm-iv-taxis/.github#6` Org profile link/count drift | Pure README table/count update; issue gives exact stale links and intended targets | Markdown review; no workflow changes |
| 7 | `organvm-ii-poiesis/.github#6` Profile README org-name and workflow table drift | Text-only fix: replace phantom org references and list `release.yml` | Markdown review |
| 8 | `meta-organvm/.github#9` Root README/homepage polish | Very small public-page fix: expand 2-line root README or correct homepage target | Markdown review |
| 9 | `organvm-vi-koinonia/.github#12` Keepalive status accuracy | One-line README accuracy fix; avoids enabling workflows or touching secrets | Markdown review |
| 10 | `organvm-i-theoria/hierarchia-mundi#1` Ship-now hygiene fix | Small docs/seed cleanup: dead links, counts, imports/install line; no deploy secrets | Python package smoke path from README if repo has tests |

### Tier 2: Dispatch After Human Confirms Scope

| Issue | Hold reason | Jules-sized slice |
|---|---|---|
| `organvm-v-logos/.github#15` Root `workflows/` duplicate | Issue offers either move to `workflow-templates/` or delete; choose one before dispatch | Move to `workflow-templates/` and add `.properties.json`, or delete duplicate root dir |
| `meta-organvm/organvm-scrutator#2` False-active daily scan and directory warnings | Repo verdict is PARK, but two concrete code fixes are safe | Add zero-plan guard to workflow, or add `is_file()` guard in scanner |
| `organvm-vii-kerygma/organvm-vii-kerygma--superproject#2` Missing READMEs | Work touches submodule/member repo expectations; verify repo layout before assigning | Add README files for `kerygma-pipeline` and `kerygma-profiles` only if present in checkout |
| `organvm-ii-poiesis/organvm-ii-poiesis--superproject#2` Missing README for `performance-sdk` | Same submodule/member uncertainty | Add `performance-sdk/README.md` only if the directory exists in the repo checkout |
| `a-organvm/a-i--skills#23` Activation ship-soon | Release/package artifact work may require publishing credentials; docs-only slice is safe | Add explicit install/use docs tied to `v1.2.0`; do not publish |
| `a-organvm/agent--claude-smith#27` Activation ship-soon | Package/release automation may require npm permissions | Confirm package metadata and add smoke-test usage docs; defer publish |
| `a-organvm/agentic-titan#93` Activation ship-soon | Publishing/container decision needed | Draft release artifact plan and smoke-check docs; defer actual publish |
| `a-organvm/petasum-super-petasum#145` Activation ship-soon | Runtime/package path is not bounded enough yet | First dispatch should only inventory manifests and propose release path |

### Tier 3: Do Not Dispatch To Jules

| Issue | Reason |
|---|---|
| `organvm-iii-ergon/content-engine--asset-amplifier#22` | Requires Cloudflare/Stripe/API secrets and redeploy work |
| `meta-organvm/persona-fleet#3` | Financial/live-trading context and identity files; even the mechanical `ethers` fix sits inside a sensitive repo |
| Superproject `kill`, `skip`, or decommission issues across `organvm-iii-ergon`, `organvm-iv-taxis`, `organvm-v-logos`, `organvm-vi-koinonia`, and `meta-organvm` | Mostly archive/delete/account-state actions or historical curation, not autonomous code PRs |
| `organvm-ii-poiesis/organvm-ii-poiesis--superproject#5` | PARK; PR candidate is explicitly not sufficient because dangling submodule pins also need repair |
| `organvm-vii-kerygma/organvm-vii-kerygma--superproject#6` | PARK pending org-vs-`a-organvm` consolidation decision |
| Human/community/revenue issues such as `organvm-v-logos/.github#4`, `#5`, `#6`, `#7` | Require human outreach, experiments, external validation, or recurring judgment |

## Suggested Batch 3 Packs

### Pack 3A: Low-Risk Diagrams And Public Profile Hygiene

Dispatch together or sequentially:

1. `a-organvm/orchestration-start-here#159`
2. `a-organvm/orchestration-start-here#160`
3. `organvm-iv-taxis/.github#6`
4. `organvm-vii-kerygma/.github#7`
5. `organvm-ii-poiesis/.github#6`

These are all text/Markdown changes. They have low blast radius and clear visual verification.

### Pack 3B: Static Pages And Runtime Discoverability

Dispatch after Pack 3A:

1. `organvm-iii-ergon/specvla-ergon--avditor-mvndi#16`
2. `organvm-iii-ergon/organvm-iii-ergon.github.io#1`
3. `meta-organvm/.github#9`
4. `organvm-vi-koinonia/.github#12`
5. `organvm-i-theoria/hierarchia-mundi#1`

These are still bounded, but some need repo-specific build or package smoke checks.

### Pack 3C: Scoped Follow-Up Only

Do not dispatch until a human chooses the exact slice:

1. `meta-organvm/organvm-scrutator#2`
2. `organvm-v-logos/.github#15`
3. `a-organvm/a-i--skills#23`
4. `a-organvm/agent--claude-smith#27`
5. `a-organvm/agentic-titan#93`

## Jules Prompt Template

Use this template for Tier 1 tasks:

```text
You are working in REPO_FULL_NAME on ISSUE_URL.

Goal:
- Implement only the issue's bounded PR candidate / acceptance criteria.

Constraints:
- Do not touch secrets, deployment settings, billing, repository settings, or workflow enablement.
- Keep the PR limited to the named files unless the issue acceptance criteria requires otherwise.
- Preserve existing style and avoid unrelated cleanup.

Verification:
- Run the repo's relevant local checks if available.
- For Markdown/Mermaid/static HTML, confirm the syntax renders or is structurally valid.
- In the PR summary, include changed files, verification run, and any remaining manual follow-up.
```

## Completion Notes

The strongest immediate Jules candidates are `a-organvm/orchestration-start-here#159` and `#160`; they are small, local to this repository, and have explicit acceptance criteria. The broader Batch 3 audit found many activation-audit issues, but most are not Jules-ready because they are either decommission/archive decisions, deployment/secret work, or human/community execution.
