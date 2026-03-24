# The Absorption Protocol

When external questions arrive — GitHub comments, PR reviews, Discord messages, conversations — they are not tests to pass. They are probes that illuminate regions of the architecture invisible from inside.

The contribution engine has an outbound flow: contribute → learn → deposit. This protocol is the **inbound** complement: receive question → detect expansion → formalize → deposit → answer with depth.

## The Gate

Not every question deserves formalization. The protocol fires only when:

1. **The question contains an assumption we don't share.** Matt assumed state transfer requires a merge step. We don't merge — we use stigmergy. His assumption exposed our divergence as an innovation.
2. **The question points at something unnamed.** "How do you handle conflicting traces?" pointed at reader-side resolution — a pattern that was implemented but had no name or formalization.
3. **Independent convergence is visible.** Matt's TTL-based file locks are a cruder version of the same principle. Two systems arriving at the same shape = structural attractor worth naming.

If none of these fire, answer the question normally. If any fire, the protocol activates.

## The Flow

```
RECEIVE — external question arrives
    │
    ▼
ASSESS — expansive or reductive?
    │
    ├── Reductive (tests boundaries, seeks limits, probes for weakness)
    │   └── Answer precisely, don't over-share. No formalization needed.
    │
    └── Expansive (contains assumption we don't share, points at unnamed pattern,
        shows independent convergence)
        │
        ▼
    FORMALIZE — before answering, write the theory note
        │  • Name the pattern
        │  • State formal properties
        │  • Identify what this is NOT (distinguish from similar patterns)
        │  • Note the biological/mathematical analogue
        │  • Note the independent convergence if present
        │  • Place in relationship to sibling patterns
        │
        ▼
    DEPOSIT — route to the appropriate organ via backflow pipeline
        │  • ORGAN-I: formal patterns, mathematical properties
        │  • ORGAN-II: diagrams, visual representations
        │  • ORGAN-V: essay potential, narrative framing
        │
        ▼
    ANSWER — respond to the original question, now informed by formalization
        │  The answer is deeper because we formalized first.
        │  The questioner sees the depth and asks deeper.
        │  Positive feedback loop.
        │
        ▼
    CREDIT — the questioner's contribution is logged
           • Outreach: relationship score increases
           • Backflow: source attribution to the questioner
           • The question itself is the knowledge source
```

## Detection Heuristics

Questions that typically trigger the protocol:

- **"How do you handle X?"** where X is something we handle differently from convention → assumption divergence
- **"What happens when Y?"** where Y is a failure mode we designed around → unnamed pattern exposure
- **"We did Z instead"** where Z is an independent implementation of the same principle → convergence signal
- **"Does A win over B?"** where our answer is "neither — C decides" → resolution strategy worth naming

Questions that typically DON'T trigger:

- "What version of X do you use?" → factual, no expansion
- "Can you add feature Y?" → request, not probe
- "This doesn't work because Z" → bug report, handle normally
- "Why not just use X?" → may be reductive (dismissing complexity) unless X reveals a real alternative

## The Inversion

The contribution engine's thesis is that outbound contributions generate inbound knowledge. The absorption protocol is the dual: **inbound questions generate inbound knowledge.** The conversation itself is the contribution — the external party contributes a question, we contribute a formalization, both parties leave with more than they started with.

This makes the contribution engine bidirectional at the conversational level, not just at the code level.

## Implementation

Currently: ad hoc recognition by the operator (human or agent).

Future: the `monitor.py` module already polls PR comments. Extend it to run the ASSESS gate on every new inbound comment across all tracked relationships. Flag comments that match the detection heuristics for formalization review.

Detection could be keyword-based initially:
- "how do you handle" + topic not in existing theory notes
- "we ended up doing" + different implementation (convergence signal)
- "what happens when" + failure/edge case not documented
- Questioner has >50 followers or maintains >10-star repos (signal quality proxy)
