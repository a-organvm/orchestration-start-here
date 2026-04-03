# Open-Close Patterns: Top-Level Directory Analysis

## Week of March 27 - April 3, 2026

---

## Hierarchy Map

```
/Users/4jp/Workspace/
├── (root/unspecified)      ← 96 commands, 46 AI sessions
├── organvm-iv-taxis        ← 76 commands, 46 AI sessions
│   ├── orchestration-start-here
│   └── vox--architectura-gubernatio
├── 4444J99                 ← 66 commands, 54 AI sessions
│   ├── application-pipeline
│   ├── domus-semper-palingenesis
│   └── portfolio
├── meta-organvm             ← 47 commands, 32 AI sessions
│   ├── aerarium--res-publica
│   └── post-flood
├── organvm-iii-ergon        ← 22 commands, 13 AI sessions
│   ├── commerce--meta
│   ├── content-engine--asset-amplifier
│   └── sovereign-systems--elevate-align
├── a-organvm               ← 12 commands, 10 AI sessions
└── organvm-i-theoria       ← 10 commands, 7 AI sessions
    └── conversation-corpus-engine
```

---

## Top-Level Open Patterns

### By Directory (AI tool invocations = session opens)

| Directory | Opens | Primary Tools | Pattern |
|-----------|-------|---------------|---------|
| **4444J99** | 54 | Claude(18), Gemini(12), OpenClaw(10) | Multi-tool experimental |
| **root** | 46 | Claude(15), Gemini(12), Codex(8) | Quick lookups, global ops |
| **organvm-iv-taxis** | 46 | Claude(26), OpenCode(8), Gemini(7) | Deep orchestration work |
| **meta-organvm** | 32 | Claude(17), Gemini(7), Ollama(3) | System architecture |
| **organvm-iii-ergon** | 13 | Claude(7), OpenCode(2), OpenClaw(2) | Content engineering |
| **a-organvm** | 10 | Gemini(3), Codex(3), Claude(3) | Equal distribution |
| **organvm-i-theoria** | 7 | Claude(5), OpenCode(1), Goose(1) | Theory/corpuses |

---

## Session Flow Patterns

### Typical Entry Sequence

```
1. cd into workspace
2. cd into specific organ or project  
3. invoke AI tool (claude/codex/gemini/opencode)
4. work session...
5. (exit AI tool - not captured in shell history)
```

### Close Pattern: cd ..

The pattern shows `cd ..` IS used to exit directories:
- March 31: Multiple `cd ..` chains observed
- Pattern: `cd '..'` → `cd '..'` → `cd 'organvm-iv-taxis'`

**However:** No explicit session termination markers in shell history.

---

## Tool Selection by Context

| Directory | Preferred Tool | Secondary | Usage Pattern |
|-----------|---------------|-----------|----------------|
| organvm-iv-taxis | Claude (57%) | OpenCode (17%) | Orchestration, architecture |
| 4444J99 | Claude (33%) | Gemini (22%) | Mixed experimental |
| meta-organvm | Claude (53%) | Gemini (22%) | System design |
| organvm-iii-ergon | Claude (54%) | OpenCode (15%) | Content pipeline |
| a-organvm | Equal | - | Exploration |

---

## Observed Patterns

### 1. Multi-Tool Chaining
```
gemini → codex → opencode
```
Same task flows through multiple AI tools for different aspects.

### 2. Deep Session Pattern
```
cd organvm-iv-taxis
claude [work for 30+ min]
cd ..
cd meta-organvm  
claude [continue]
```

### 3. Quick Lookup Pattern
```
cd ~/Workspace/any-project
gemini [single query]
exit
```

### 4. Orchestration Handoff
```
opencode [invoke]
[AIs collaborate]
exit
codex [continue in same dir]
```

---

## Gap: Session Close Markers

**Missing from data:**
- Explicit session end indicators (AI tools don't write to shell history on exit)
- No "closing" event captured
- Only `cd ..` as proxy for session navigation change

**Recommendation:** 
- Add explicit session markers to shell prompt or wrapper scripts
- Capture AI tool exit codes to log session completion
- Track time-in-directory for session duration estimates

---

## Stats Summary

- Total AI sessions opened: 210
- Total `cd ..` traversals: ~20 (proxy for close/navigate away)
- Open:Close ratio: ~10:1 (sessions don't cleanly close, just navigate away)
- Most active: 4444J99 (54 opens) tied with root (46 opens)
- Heaviest tool: Claude Code (26-57% depending on directory)

---

*Generated: 2026-04-03*
*Source: Warp SQLite command history*
