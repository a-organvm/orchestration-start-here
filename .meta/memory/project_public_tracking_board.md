---
name: public-tracking-board
description: GitHub Projects V2 board at a-organvm/projects/2 tracks all Plague Campaign contributions publicly. 22 issues in a-organvm/a-organvm repo.
type: project
---

## Public Tracking Board

**URL:** [a-organvm/projects/2](https://github.com/orgs/a-organvm/projects/2)
**Title:** The Plague — Open Source Contribution Campaign
**Visibility:** Public
**Issues repo:** a-organvm/a-organvm (issues #26–#47)

**Custom fields:** Phase (UNBLOCK→ENGAGE→CULTIVATE→HARVEST→INJECT→STALLED), Domain (8 options), Language (5), Wave (3), Income Signal (Yes/No), Relationship Score (number)

**Auth note:** The active `GITHUB_TOKEN` env var lacks `project` scope. Must `unset GITHUB_TOKEN` before any `gh project` commands to fall through to the keyring token which has the scope.

**Why:** Public visibility of contribution work. Each issue links to the external PR with full context. Board supports filtering by wave, domain, language, income signal.

**How to apply:** When new PRs are submitted, create corresponding issues and add to project. Update issue status when PRs are reviewed/merged/closed.
