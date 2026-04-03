# Session Boundaries: Derived from Prompt Content

## Week of March 27 - April 3, 2026

---

## Data Source

**Claude Code `history.jsonl`**: 1,086 prompts across 108 sessions

Each session has:
- **BEGIN**: First prompt in session (session start indicator)
- **END**: Last prompt in session (session close indicator)  
- **Duration**: Calculated from timestamps
- **Directory**: Derived from `project` field

---

## Session Stats

| Metric | Value |
|--------|-------|
| Total Sessions | 108 |
| Total Prompts | 1,086 |
| Avg Prompts/Session | 10.1 |
| Avg Session Duration | 493m (~8h) |
| Longest Session | 4,751m (~79h) |

---

## Sessions by Directory

### organvm-iv-taxis

**Sessions**: 35 | **Prompts**: 286 | **Total Time**: 13633m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 14:00 | 18:40 | 4600m | 31 |
| 14:18 | 18:05 | 4547m | 18 |
| 09:42 | 09:42 | 0m | 2 |
| 09:45 | 09:45 | 0m | 2 |
| 04:16 | 19:33 | 916m | 22 |
| 18:42 | 22:03 | 201m | 14 |
| 21:02 | 00:39 | 217m | 13 |
| 22:05 | 01:09 | 184m | 6 |

*... and 27 more sessions*

### 4444J99

**Sessions**: 21 | **Prompts**: 220 | **Total Time**: 11397m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 11:01 | 17:56 | 415m | 31 |
| 14:18 | 21:29 | 4751m | 34 |
| 17:46 | 18:04 | 18m | 5 |
| 19:15 | 22:03 | 4488m | 66 |
| 09:24 | 09:24 | 0m | 1 |
| 09:46 | 09:46 | 0m | 1 |
| 07:35 | 09:53 | 138m | 18 |
| 09:55 | 14:58 | 303m | 2 |

*... and 13 more sessions*

### meta-organvm

**Sessions**: 17 | **Prompts**: 249 | **Total Time**: 2017m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 09:44 | 09:44 | 1m | 2 |
| 12:00 | 14:21 | 141m | 7 |
| 12:12 | 17:28 | 316m | 65 |
| 15:00 | 21:10 | 370m | 61 |
| 16:02 | 16:02 | 0m | 1 |
| 18:58 | 20:39 | 101m | 13 |
| 19:37 | 20:26 | 49m | 8 |
| 20:23 | 20:39 | 17m | 6 |

*... and 9 more sessions*

### other

**Sessions**: 14 | **Prompts**: 128 | **Total Time**: 11372m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 14:44 | 05:36 | 3772m | 6 |
| 20:07 | 11:56 | 3829m | 35 |
| 23:19 | 12:07 | 3648m | 59 |
| 23:26 | 23:26 | 0m | 1 |
| 23:38 | 23:38 | 0m | 1 |
| 08:48 | 08:48 | 0m | 1 |
| 08:55 | 08:55 | 0m | 1 |
| 09:02 | 09:02 | 0m | 1 |

*... and 6 more sessions*

### organvm-iii-ergon

**Sessions**: 9 | **Prompts**: 108 | **Total Time**: 8555m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 10:39 | 09:29 | 4251m | 46 |
| 10:42 | 09:36 | 4254m | 49 |
| 11:10 | 11:10 | 0m | 1 |
| 10:01 | 10:01 | 0m | 1 |
| 10:01 | 10:01 | 0m | 1 |
| 08:08 | 08:08 | 0m | 1 |
| 08:08 | 08:08 | 0m | 2 |
| 00:20 | 01:10 | 50m | 6 |

*... and 1 more sessions*

### organvm-i-theoria

**Sessions**: 7 | **Prompts**: 51 | **Total Time**: 4534m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 23:23 | 17:57 | 3993m | 20 |
| 09:23 | 09:23 | 0m | 3 |
| 18:01 | 21:37 | 216m | 4 |
| 21:51 | 21:51 | 0m | 2 |
| 00:36 | 03:58 | 203m | 18 |
| 03:46 | 03:46 | 0m | 1 |
| 08:49 | 10:51 | 122m | 3 |

### a-organvm

**Sessions**: 5 | **Prompts**: 44 | **Total Time**: 1761m

| Begin | End | Duration | Prompts |
|-------|-----|----------|--------|
| 11:27 | 16:44 | 316m | 7 |
| 11:40 | 11:43 | 3m | 3 |
| 13:30 | 12:24 | 1374m | 29 |
| 12:37 | 13:35 | 58m | 3 |
| 13:35 | 13:45 | 9m | 2 |

---

## Key Patterns in Session Boundaries

### BEGIN Indicators (First Prompt in Session)

Common patterns marking session START:
- `/resume` - Continuing previous session
- `/model` - Switching models
- Direct task prompts ("what's next", "review X", "implement Y")
- `/init` - New session initialization

### END Indicators (Last Prompt in Session)

Common patterns marking session CLOSE:
- `[Pasted text]` - Receiving handover content
- `/clear` - Explicit session clear
- Task completion ("proceed", "done")
- Review/audit prompts

### Session Continuity

- Sessions span multiple days (duration shows "start → end" crossing midnight)
- `/resume` used to continue previous sessions
- Handoff pattern: `[Pasted text]` at END → new session BEGIN picks up

---

## Session Flow Example

```
[Session A] BEGIN: "what's next for the roadmap"
            ... 30 prompts ...
            END: "[Pasted text #6 +15 lines]"

[Session B] BEGIN: "[Pasted text #6 +15 lines]"  ← Continues from A
            ... 45 prompts ...
            END: "proceed with implementation"
```

This shows the handoff pattern visible in the data.

---

*Source: Claude Code `~/.claude/history.jsonl`*
*Generated: 2026-04-03*
