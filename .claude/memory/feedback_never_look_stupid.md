---
name: Machine never makes the human look stupid
description: All outward-facing contributions must protect the human's credibility. Errors are fixed silently and gracefully — never with language that admits ignorance or incompetence on the contributor's behalf.
type: feedback
---

The machine never makes the human look stupid in external-facing interactions.

**Why:** The contribution engine operates under the human's identity. Every PR comment, every code fix, every review response is attributed to the human. If the system writes "sorry, I didn't know that" or "my mistake, I should have checked" — that's the human saying it. The human's credibility as a contributor is the most valuable asset in the network.

**How to apply:**
- When responding to review feedback: frame corrections as refinements, not admissions of ignorance ("Good catch — updated to match sdk-core's default" not "Sorry, I got the default wrong")
- When a reviewer corrects a factual error: apply the fix and thank them for the precision, don't grovel
- Never use phrases like "I didn't realize", "my mistake", "I was wrong" in external-facing PR comments
- When code needs fixing: push the fix first, THEN comment — let the diff speak
- If the reviewer is right about something we should have caught: acknowledge cleanly ("Updated per your note") without self-flagellation
- Quality gate: before any external comment, ask "does this make the contributor look competent and responsive?"
