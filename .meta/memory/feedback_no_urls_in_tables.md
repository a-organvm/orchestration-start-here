---
name: no_bare_long_urls
description: Never output bare long URLs — use short markdown link text to prevent terminal line-wrap breakage
type: feedback
---

Never output raw long URLs. Terminal line wrapping splits them across lines, destroying the link regardless of format (tables, bullets, plain text).

**Why:** Terminal columns are ~80 chars. Any URL longer than remaining line space gets wrapped and becomes unclickable.

**How to apply:** Always use short markdown link text: `[comment](https://long-url...)` or `[draft](https://long-url...)`. The terminal renders the short text as clickable. Never paste a bare URL inline.
