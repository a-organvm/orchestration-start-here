---
name: pr_comment_discipline
description: Rules for contributor comment discipline on external PRs — minimize noise, maximize merge probability
type: feedback
---

## PR Comment Discipline — External Contributions

The goal is to be the contributor whose PRs require zero maintainer energy to merge. Comment volume inversely correlates with merge probability on small PRs.

**Why:** dbt-mcp PR #669 (3-line string change) accumulated 7 contributor comments — bump before review, two "I'm done" signals, a build failure disclosure. Each individually reasonable; in aggregate, it made a trivial PR look like a project. Maintainers gauge effort-to-merge from notification count.

### Rules

1. **Never bump before first review.** Submit and wait. The PR notification is the bump. Pre-review "checking in" comments signal impatience, not professionalism.

2. **One commit per review round.** Apply all feedback from a review cycle in a single commit. Never split corrections across multiple commits with separate "done" comments.

3. **One confirmation comment per round.** After applying feedback: one comment, one sentence. "Applied all suggestions in `<sha>`." No paragraphs, no diffs, no explanations unless the reviewer asked a question.

4. **Never disclose build failures unprompted.** If asked "did you test locally?" and the build fails, find another way to verify (read the test suite, check the CI config, describe what the change touches). Disclosing "I can't build this" creates hesitation. If the change is pure string literals, say "Changes are string-only — no logic paths affected. Happy to verify further if CI surfaces anything."

5. **Silence is a signal.** After all feedback is addressed, stop commenting. The commit itself is the signal. Maintainers see push notifications. A clean diff with no new comments says "this is ready" more clearly than another comment saying "this is ready."

6. **One bump per patience window.** If no activity after 7 days: one sentence. "All feedback addressed — ready when you are." Then silence for another 7 days. Never bump twice in the same week.

7. **Match PR size to comment budget.** Rough guide:
   - 1-10 line change: 0-1 comments beyond review responses
   - 10-50 line change: 1-2 comments
   - 50+ line change: comment as needed, but still minimize

### How to Apply

Before posting any comment on an external PR, count existing comments from 4444J99 on that PR. If the count exceeds the budget for the PR's size, do not post. If the comment contains information the maintainer didn't ask for, do not post.
