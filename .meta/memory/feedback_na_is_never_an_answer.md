---
name: na-is-never-an-answer
description: N/A is never an answer. Every N/A, "unknown", zero, or placeholder in system output represents a vacuum that must be researched, planned, and logged. No exceptions.
type: feedback
---

N/A is never an answer. It is a symptom. Every instance of "n/a", "unknown", "TBD", "0/N", or placeholder text in any system output — CLAUDE.md, dashboards, metrics, context files — is a vacuum where something should exist.

**Why:** The system describes itself to itself. When it reports "n/a", it is admitting ignorance about its own state. This is unacceptable. Either the data exists and the rendering is broken (fix the renderer), or the data doesn't exist and the infrastructure is missing (build it), or the metric doesn't map to reality (redefine or remove it). In all three cases, the correct response is action — never acceptance.

**How to apply:** On every session start and close, scan auto-generated context for N/A, unknown, zero, and placeholder values. For each one: (1) research the root cause, (2) write a plan if the fix is non-trivial, (3) log an IRF item. The default posture is that every N/A is a P1 until proven otherwise. Do not report N/A vacuums back to the user as findings — fix them or file them. The system simply knows.
