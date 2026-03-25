---
name: Full context ingestion before contributing
description: Before contributing to any external repo, fully ingest their CONTRIBUTING.md, code style, conventions, recent PRs, and house rules. No drive-by PRs.
type: feedback
---

Contribution requires full context ingestion — when we go to someone's house, we follow the goddamn rules.

**Why:** A PR that violates the target repo's conventions signals "I didn't read your docs." It undermines the human's credibility and wastes reviewer time. The contribution engine's value proposition is competence — every PR must look like it was written by someone who belongs in that codebase.

**How to apply:**
- Before writing ANY code for an external contribution, read: CONTRIBUTING.md, README, CODE_OF_CONDUCT, recent merged PRs (for style), linter config, test patterns, commit message conventions
- Match their code style exactly — their indent width, their naming conventions, their test framework, their import ordering
- If they use conventional commits, use conventional commits. If they use Signed-off-by, sign off. If they require CLA, sign it first.
- Check their PR template — fill it out completely
- Look at how recent merged PRs were structured — that's the real style guide
- If the repo is small enough, read the whole thing. If large, read the modules you're touching + their test equivalents
- The contribution should be INDISTINGUISHABLE from an insider's work
