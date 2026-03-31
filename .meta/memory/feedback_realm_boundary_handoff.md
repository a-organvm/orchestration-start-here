---
name: realm-boundary-handoff
description: When vacuums span multiple stacks/concerns, separate in-realm from out-of-realm and provide structured handoff prompts.
type: feedback
---

When session work spans multiple realms (e.g., Python contrib_engine + TypeScript dead code + CI/ops audit), separate them cleanly:

1. Identify which items are "in-realm" (same stack, same directory context)
2. Identify which are "out-of-realm" (different stack, different concern)
3. Execute in-realm items in the current session
4. Provide structured **handoff relay prompts** for out-of-realm items — complete task descriptions the user can paste into a separate session

**Why:** User said "if within same realm, otherwise hand-off relay prompt provide below and ill sort it proper" (2026-03-31). The user manages multiple parallel sessions and prefers to route work themselves rather than have one session attempt everything.

**How to apply:** At session start, when presented with a work queue spanning multiple realms, assess realm boundaries immediately. Ask only about in-realm scope. Include handoff prompts as deliverables alongside code.
