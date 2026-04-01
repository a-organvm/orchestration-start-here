#!/usr/bin/env python3
"""Prompt-to-Outcome Reconciliation — 72h automated cross-reference.

Reads operator prompts from JSONL session files, reads git logs from all
workspaces, classifies each prompt, matches to outcomes, produces the
reconciliation report.

Run: python3 scripts/reconcile-72h.py > docs/reconciliation-72h.md
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────

WORKSPACES = {
    "orchestration-start-here": Path.home() / "Workspace/organvm-iv-taxis/orchestration-start-here",
    "meta-organvm": Path.home() / "Workspace/meta-organvm",
    "organvm-engine": Path.home() / "Workspace/meta-organvm/organvm-engine",
    "corpvs-testamentvm": Path.home() / "Workspace/meta-organvm/organvm-corpvs-testamentvm",
    "a-organvm": Path.home() / "Workspace/a-organvm",
    "application-pipeline": Path.home() / "Workspace/4444J99/application-pipeline",
}

SESSION_DIRS = {
    "orchestration-start-here": Path.home() / ".claude/projects/-Users-4jp-Workspace-organvm-iv-taxis-orchestration-start-here",
    "meta-organvm": Path.home() / ".claude/projects/-Users-4jp-Workspace-meta-organvm",
    "a-organvm": Path.home() / ".claude/projects/-Users-4jp-Workspace-a-organvm",
    "application-pipeline": Path.home() / ".claude/projects/-Users-4jp-Workspace-4444J99-application-pipeline",
    "workspace-root": Path.home() / ".claude/projects/-Users-4jp-Workspace",
}

CUTOFF = datetime(2026, 3, 29, 0, 0)

# ── Classification keywords ───────────────────────────────────────────

CLASSIFY_PATTERNS: dict[str, list[str]] = {
    "BUILD": ["build", "implement", "create", "write", "add", "wire", "fix", "feat", "embodiment", "function"],
    "PLAN": ["plan", "spec", "design", "approach", "strategy", "architecture", "propose"],
    "AUDIT": ["audit", "check", "verify", "sisyphus", "hall-monitor", "safe to close", "certain", "review"],
    "TRIAGE": ["triage", "sort", "compress", "prioritize", "reduce", "group", "rank"],
    "RESEARCH": ["explore", "investigate", "what is", "state of affairs", "provide", "overview", "analyze"],
    "DECISION": ["recommend", "which", "choose", "decision", "option", "accept", "select"],
    "META": ["token", "process", "workflow", "session", "prompt", "recording", "remember", "memory"],
}

NOISE_PATTERNS = [
    r"^\s*$",
    r"^\[Request interrupted",
    r"^<command-name>",
    r"^<local-command",
    r"^<task-notification>",
    r"^<user-prompt-submit-hook>",
    r"^\s*↵\s*$",
    r"^/model",
    r"^/clear",
    r"^/init",
]


# ── Data structures ───────────────────────────────────────────────────

@dataclass
class Prompt:
    timestamp: str
    workspace: str
    session_id: str
    text: str
    classification: str = ""
    summary: str = ""
    outcome: str = ""
    evidence: str = ""


@dataclass
class Commit:
    hash: str
    date: str
    message: str
    workspace: str


# ── Extract prompts from JSONL ────────────────────────────────────────

def extract_prompts() -> list[Prompt]:
    prompts: list[Prompt] = []

    for ws_name, ws_dir in SESSION_DIRS.items():
        if not ws_dir.exists():
            continue
        for jf in sorted(ws_dir.glob("*.jsonl")):
            mtime = datetime.fromtimestamp(jf.stat().st_mtime)
            if mtime < CUTOFF:
                continue

            session_id = jf.stem[:8]
            with open(jf) as fh:
                for line in fh:
                    try:
                        obj = json.loads(line.strip())
                        if obj.get("type") != "user" or obj.get("isMeta", False):
                            continue
                        msg = obj.get("message", {})
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            text = " ".join(
                                p.get("text", "") if isinstance(p, dict) else str(p)
                                for p in content
                            ).strip()
                        else:
                            text = str(content).strip()

                        if len(text) < 5:
                            continue

                        ts = obj.get("timestamp", "")[:19]
                        prompts.append(Prompt(
                            timestamp=ts,
                            workspace=ws_name,
                            session_id=session_id,
                            text=text,
                        ))
                    except Exception:
                        pass

    return sorted(prompts, key=lambda p: p.timestamp)


# ── Classify prompts ──────────────────────────────────────────────────

def is_noise(text: str) -> bool:
    for pat in NOISE_PATTERNS:
        if re.match(pat, text):
            return True
    return False


def classify(prompt: Prompt) -> str:
    if is_noise(prompt.text):
        return "NOISE"

    text_lower = prompt.text.lower()
    scores: dict[str, int] = {}
    for cat, keywords in CLASSIFY_PATTERNS.items():
        scores[cat] = sum(1 for kw in keywords if kw in text_lower)

    if max(scores.values(), default=0) == 0:
        return "META"  # default for unclassifiable non-noise

    return max(scores, key=lambda k: scores[k])


def summarize(text: str) -> str:
    """First meaningful line, truncated."""
    clean = text.replace("↵", "\n").strip()
    lines = [l.strip() for l in clean.split("\n") if l.strip() and not l.strip().startswith("<")]
    if not lines:
        return "(empty)"
    first = lines[0][:120]
    return first + ("..." if len(lines[0]) > 120 else "")


# ── Extract commits ───────────────────────────────────────────────────

def extract_commits() -> list[Commit]:
    commits: list[Commit] = []
    for ws_name, ws_dir in WORKSPACES.items():
        if not ws_dir.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--since=72 hours ago",
                 "--format=%h|%ad|%s", "--date=short"],
                capture_output=True, text=True, cwd=ws_dir, timeout=10,
            )
            for line in result.stdout.strip().split("\n"):
                if "|" not in line:
                    continue
                parts = line.split("|", 2)
                if len(parts) == 3:
                    commits.append(Commit(
                        hash=parts[0], date=parts[1],
                        message=parts[2], workspace=ws_name,
                    ))
        except Exception:
            pass

    return commits


# ── Match prompts to outcomes ─────────────────────────────────────────

def match_outcomes(prompts: list[Prompt], commits: list[Commit]) -> None:
    """For each prompt, try to find a matching commit or plan."""
    commit_messages_lower = [(c, c.message.lower()) for c in commits]

    for p in prompts:
        if p.classification == "NOISE":
            continue

        text_lower = p.text.lower()[:300]

        # Extract key words from the prompt (>4 chars, not common)
        stop_words = {"this", "that", "with", "from", "have", "will", "been",
                      "what", "when", "where", "which", "their", "there",
                      "about", "would", "could", "should", "these", "those",
                      "your", "they", "them", "than", "then", "into", "just",
                      "like", "make", "does", "also", "want", "need", "here"}
        words = set(re.findall(r"[a-z]{4,}", text_lower)) - stop_words

        # Find best matching commit
        best_score = 0
        best_commit = None
        for c, msg_lower in commit_messages_lower:
            score = sum(1 for w in words if w in msg_lower)
            if score > best_score:
                best_score = score
                best_commit = c

        if best_score >= 3:
            p.outcome = "DELIVERED"
            p.evidence = f"{best_commit.hash} ({best_commit.workspace}): {best_commit.message[:80]}"
        elif best_score >= 2:
            p.outcome = "PARTIAL"
            p.evidence = f"Possible: {best_commit.hash} ({best_commit.workspace}): {best_commit.message[:80]}"
        elif any(w in text_lower for w in ["billing", "enterprise", "copilot", "ghas"]):
            p.outcome = "HUMAN-ACTION"
            p.evidence = "Requires operator action (billing/infra)"
        elif any(w in text_lower for w in ["irf", "irf-", "future", "next session", "later"]):
            p.outcome = "DEFERRED"
            p.evidence = "Referenced as future work"
        else:
            p.outcome = "HANGING"
            p.evidence = ""


# ── Report generation ─────────────────────────────────────────────────

def generate_report(prompts: list[Prompt], commits: list[Commit]) -> str:
    lines: list[str] = []

    noise_count = sum(1 for p in prompts if p.classification == "NOISE")
    actionable = [p for p in prompts if p.classification != "NOISE"]

    lines.append("# Prompt-to-Outcome Reconciliation — 72 Hours")
    lines.append(f"\n**Generated:** {datetime.now().isoformat()[:19]}")
    lines.append(f"**Window:** 2026-03-29 to 2026-03-31")
    lines.append(f"**Total prompts:** {len(prompts)}")
    lines.append(f"**Noise filtered:** {noise_count}")
    lines.append(f"**Actionable:** {len(actionable)}")
    lines.append(f"**Commits available:** {len(commits)}")

    # ── Statistics ──
    outcomes = {}
    for p in actionable:
        outcomes[p.outcome] = outcomes.get(p.outcome, 0) + 1

    lines.append("\n## Statistics\n")
    lines.append("| Outcome | Count | % |")
    lines.append("|---------|-------|---|")
    for outcome in ["DELIVERED", "PARTIAL", "HANGING", "DEFERRED", "HUMAN-ACTION"]:
        count = outcomes.get(outcome, 0)
        pct = f"{count / len(actionable) * 100:.1f}" if actionable else "0"
        lines.append(f"| {outcome} | {count} | {pct}% |")

    # ── Classification breakdown ──
    classifications = {}
    for p in actionable:
        classifications[p.classification] = classifications.get(p.classification, 0) + 1

    lines.append("\n## Classification Breakdown\n")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for cls in sorted(classifications, key=lambda k: -classifications[k]):
        lines.append(f"| {cls} | {classifications[cls]} |")

    # ── By workspace ──
    ws_counts: dict[str, dict[str, int]] = {}
    for p in actionable:
        ws = p.workspace
        if ws not in ws_counts:
            ws_counts[ws] = {}
        ws_counts[ws][p.outcome] = ws_counts[ws].get(p.outcome, 0) + 1

    lines.append("\n## By Workspace\n")
    lines.append("| Workspace | Delivered | Partial | Hanging | Deferred | Human |")
    lines.append("|-----------|-----------|---------|---------|----------|-------|")
    for ws in sorted(ws_counts):
        d = ws_counts[ws]
        lines.append(f"| {ws} | {d.get('DELIVERED',0)} | {d.get('PARTIAL',0)} | {d.get('HANGING',0)} | {d.get('DEFERRED',0)} | {d.get('HUMAN-ACTION',0)} |")

    # ── Delivered ──
    delivered = [p for p in actionable if p.outcome == "DELIVERED"]
    lines.append(f"\n## Delivered ({len(delivered)})\n")
    lines.append("| Time | Workspace | Prompt Summary | Evidence |")
    lines.append("|------|-----------|----------------|----------|")
    for p in delivered[:80]:
        lines.append(f"| {p.timestamp[11:16]} | {p.workspace} | {p.summary} | {p.evidence} |")

    # ── Hanging ──
    hanging = [p for p in actionable if p.outcome == "HANGING"]
    lines.append(f"\n## Hanging ({len(hanging)})\n")
    lines.append("| Time | Workspace | Prompt Summary |")
    lines.append("|------|-----------|----------------|")
    for p in hanging:
        lines.append(f"| {p.timestamp[11:16]} | {p.workspace} | {p.summary} |")

    # ── Deferred ──
    deferred = [p for p in actionable if p.outcome == "DEFERRED"]
    lines.append(f"\n## Deferred ({len(deferred)})\n")
    lines.append("| Time | Workspace | Prompt Summary | Evidence |")
    lines.append("|------|-----------|----------------|----------|")
    for p in deferred:
        lines.append(f"| {p.timestamp[11:16]} | {p.workspace} | {p.summary} | {p.evidence} |")

    # ── Human Action ──
    human = [p for p in actionable if p.outcome == "HUMAN-ACTION"]
    lines.append(f"\n## Human Action Required ({len(human)})\n")
    for p in human:
        lines.append(f"- [{p.timestamp[11:16]}] {p.summary}")

    lines.append("\n---")
    lines.append("*Generated by scripts/reconcile-72h.py — keyword matching against git logs.*")
    lines.append("*Accuracy: DELIVERED is high-confidence (3+ keyword matches). HANGING may include*")
    lines.append("*prompts whose outcomes were captured by a different workspace's commit.*")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────

def main() -> None:
    print("Extracting prompts from JSONL...", file=sys.stderr)
    prompts = extract_prompts()
    print(f"  Found {len(prompts)} prompts", file=sys.stderr)

    print("Classifying...", file=sys.stderr)
    for p in prompts:
        p.classification = classify(p)
        p.summary = summarize(p.text)

    print("Extracting commits...", file=sys.stderr)
    commits = extract_commits()
    print(f"  Found {len(commits)} commits", file=sys.stderr)

    print("Matching outcomes...", file=sys.stderr)
    match_outcomes(prompts, commits)

    report = generate_report(prompts, commits)
    print(report)

    print("\nDone.", file=sys.stderr)


if __name__ == "__main__":
    main()
