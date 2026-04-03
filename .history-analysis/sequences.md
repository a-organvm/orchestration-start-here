# Sequence Patterns: Prompt History Analysis

## Week of March 27 - April 3, 2026

---

## 1. Tool Switching Sequences

### Observed Transitions (AI tool → AI tool)

| Transition | Count | Interpretation |
|------------|-------|----------------|
| claude → gemini | 11 | Claude does deep work, uses Gemini for quick lookups |
| gemini → claude | 11 | Gemini exploration, Claude implementation |
| codex → gemini | 10 | Codex to Gemini for context/gap-filling |
| claude → codex | 9 | Claude starts, Codex continues same task |
| codex → opencode | 8 | Codex passes to OpenCode for orchestration |
| opencode → claude | 7 | OpenCode invokes Claude |
| gemini → opencode | 7 | Gemini exploration, OpenCode orchestration |
| gemini → codex | 6 | Gemini to Codex for code generation |

### Key Pattern: Multi-Tool Orchestration

```
Gemini (explore) → Claude (implement) → Codex (refine) → OpenCode (coordinate)
```

Each tool serves a different function in the workflow.

---

## 2. Directory Navigation Sequences

### Top Directory Transitions

| From → To | Count |
|-----------|-------|
| organvm-iv-taxis → root | 21 |
| organvm-iv-taxis → 4444J99 | 14 |
| root → organvm-iv-taxis | 14 |
| root → 4444J99 | 12 |
| 4444J99 → organvm-iv-taxis | 12 |
| meta-organvm → root | 9 |
| 4444J99 → meta-organvm | 8 |
| 4444J99 → root | 6 |
| meta-organvm → organvm-iv-taxis | 6 |
| root → meta-organvm | 6 |

### Hub Pattern

```
organvm-iv-taxis ←→ root ←→ 4444J99
                         ↓
                    meta-organvm
```

- **root** acts as the central hub/multiplier
- **organvm-iv-taxis** and **4444J99** are most interconnected
- Heavy traffic between orchestration and personal workspace

---

## 3. Session Handoff Patterns

### Evidence

- **59 sessions** (55%) contain "Pasted text" content
- This indicates handoff between AI tools or continuation from previous work

### Handoff Flow

```
[Claude Session A END]
  └── "[Pasted text #N +X lines]" ← Work output

[Claude Session B BEGIN]  
  └── "[Pasted text #N +X lines]" ← Continuation

[New AI Tool Session]
  └── Picks up where previous left off
```

---

## 4. Prompt Intention Patterns (Session Start)

| Intent | Count | Example |
|--------|-------|---------|
| **other** | 69 | Unclassified / unique prompts |
| **continue** | 23 | "keep going", "next", "resume" |
| **review** | 6 | "audit", "check", "analyze" |
| **create** | 6 | "implement", "build", "make" |
| **plan** | 2 | "roadmap", "strategy" |
| **explain** | 2 | "how does", "what is" |

### Insight

- **21%** of sessions are explicit continuations
- Many sessions start with unique context not fitting standard categories

---

## 5. Session Duration Patterns

| Duration | Sessions | Description |
|----------|----------|-------------|
| **instant** (<1m) | 26 | Quick lookups, `/resume`, `/model` switches |
| **<15m** | 17 | Short task bursts |
| **15m-1h** | 19 | Focused work bursts |
| **1h-4h** | 21 | Deep work sessions |
| **4h-8h** | 11 | Extended sessions |
| **8h+** | 14 | Overnight/continuous sessions |

### Insight

- ~24% are instant/very short (quick tool switches)
- ~38% are deep work (1h+)
- ~13% are overnight/continuous (8h+)

---

## 6. Combined Sequence Example (March 31 - Peak Day)

```
14:00 [root] gemini                    # Exploration
14:15 [root] codex                    # Continue with Codex  
14:20 [organvm-iv-taxis] opencode     # Orchestration invoke
14:25 [organvm-iv-taxis] claude       # Deep implementation
   ... (17 prompts, 2.5 hours) ...
17:00 [organvm-iv-taxis] opencode     # Check coordination
17:10 [organvm-iv-taxis] cd ..       
17:11 [root] cd organvm-iv-taxis      # Navigation
17:12 [organvm-iv-taxis] claude       # Continue
```

---

## Summary: Core Sequence Patterns

### Pattern A: Exploration → Implementation → Refinement
```
gemini → codex → opencode → claude
```

### Pattern B: Deep Work Sessions
```
cd <dir> → claude → ... [hours] ... → cd .. → cd <next-dir>
```

### Pattern C: Multi-Tool Handoff
```
[Claude END] "[Pasted text]" → [Claude BEGIN] "[Pasted text]" → [Codex]
```

### Pattern D: Orchestration Control
```
opencode → claude → claude → opencode
```

---

*Source: Warp SQLite + Claude Code history.jsonl*
*Generated: 2026-04-03*
