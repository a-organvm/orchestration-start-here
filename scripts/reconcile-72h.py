#!/usr/bin/env python3
"""Prompt-to-outcome reconciliation for the March 29-31, 2026 window.

Reads operator prompts from Claude JSONL session files, cross-references them
against commit activity across the tracked workspaces, and emits a markdown
report. The report distinguishes:

- `STEERING`: dispatch confirmations / routing signals
- `ABSORBED`: conceptual intake likely folded into nearby work without direct
  commit-message keyword trace
- `UNRESOLVED`: prompts that still need explicit follow-on work

Run:
    python3 scripts/reconcile-72h.py > docs/reconciliation-72h.md
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from intake_router.router import classify as classify_intake
    from intake_router.router import route as route_intake
except Exception:
    classify_intake = None
    route_intake = None


WINDOW_START = datetime(2026, 3, 29, 0, 0).astimezone()
WINDOW_END = datetime(2026, 4, 1, 0, 0).astimezone()
WINDOW_LABEL = "2026-03-29 to 2026-03-31"

WORKSPACES = {
    "orchestration-start-here": Path.home()
    / "Workspace/organvm-iv-taxis/orchestration-start-here",
    "meta-organvm": Path.home() / "Workspace/meta-organvm",
    "organvm-engine": Path.home() / "Workspace/meta-organvm/organvm-engine",
    "corpvs-testamentvm": Path.home()
    / "Workspace/meta-organvm/organvm-corpvs-testamentvm",
    "a-organvm": Path.home() / "Workspace/a-organvm",
    "application-pipeline": Path.home() / "Workspace/4444J99/application-pipeline",
}

SESSION_DIRS = {
    "orchestration-start-here": Path.home()
    / ".claude/projects/-Users-4jp-Workspace-organvm-iv-taxis-orchestration-start-here",
    "meta-organvm": Path.home() / ".claude/projects/-Users-4jp-Workspace-meta-organvm",
    "a-organvm": Path.home() / ".claude/projects/-Users-4jp-Workspace-a-organvm",
    "application-pipeline": Path.home()
    / ".claude/projects/-Users-4jp-Workspace-4444J99-application-pipeline",
    "workspace-root": Path.home() / ".claude/projects/-Users-4jp-Workspace",
}

CLASSIFY_PATTERNS: dict[str, tuple[str, ...]] = {
    "BUILD": (
        "build",
        "implement",
        "create",
        "write",
        "add",
        "wire",
        "fix",
        "feat",
        "embodiment",
        "function",
    ),
    "PLAN": ("plan", "spec", "design", "approach", "strategy", "architecture", "propose"),
    "AUDIT": (
        "audit",
        "check",
        "verify",
        "sisyphus",
        "hall-monitor",
        "safe to close",
        "certain",
        "review",
    ),
    "TRIAGE": ("triage", "sort", "compress", "prioritize", "reduce", "group", "rank"),
    "RESEARCH": (
        "explore",
        "investigate",
        "what is",
        "state of affairs",
        "provide",
        "overview",
        "analyze",
    ),
    "DECISION": ("recommend", "which", "choose", "decision", "option", "accept", "select"),
    "META": ("token", "process", "workflow", "session", "prompt", "recording", "remember", "memory"),
}

NOISE_PATTERNS = (
    re.compile(r"^\s*$", re.IGNORECASE),
    re.compile(r"^\[request interrupted", re.IGNORECASE),
    re.compile(r"^<command-name>", re.IGNORECASE),
    re.compile(r"^<local-command", re.IGNORECASE),
    re.compile(r"^<task-notification>", re.IGNORECASE),
    re.compile(r"^<user-prompt-submit-hook>", re.IGNORECASE),
    re.compile(r"^\s*↵\s*$", re.IGNORECASE),
    re.compile(r"^/model", re.IGNORECASE),
    re.compile(r"^/clear", re.IGNORECASE),
    re.compile(r"^/init", re.IGNORECASE),
    re.compile(r"^proceed$", re.IGNORECASE),
    re.compile(r"^continue$", re.IGNORECASE),
    re.compile(r"^yes$", re.IGNORECASE),
    re.compile(r"^❯", re.IGNORECASE),
    re.compile(r"^\[image", re.IGNORECASE),
)

STEERING_PATTERNS = (
    re.compile(r"^proceed with all(?:,?\s+logic dictat(?:es|eth) order)?[;.!]*$", re.IGNORECASE),
    re.compile(r"^all of the above[;.!]*$", re.IGNORECASE),
    re.compile(r"^hell yes[;.!]*$", re.IGNORECASE),
    re.compile(r"^subagent driven proceed[;.!]*$", re.IGNORECASE),
    re.compile(r"^what'?s logically next\b.*$", re.IGNORECASE),
    re.compile(r"^return[;.!]*$", re.IGNORECASE),
    re.compile(r"^(?:close|receive|handoff|intake|review|return|new)(?:--[a-z0-9-]+)+$", re.IGNORECASE),
)

ABSORBABLE_CLASSIFICATIONS = {"META", "PLAN", "RESEARCH", "AUDIT", "DECISION"}
ABSORBED_PHRASES = (
    "provide an overview",
    "all that was",
    "all that is",
    "all that needs to be",
    "what's logically next",
    "what is happening",
    "why is this happening",
    "the shape",
    "the reason i am",
    "i want to codify",
    "law dictates order",
    "logic dictates order",
    "physics of the universe",
    "soul persists",
    "safe to close",
)
ABSORBED_TERMS = (
    "overview",
    "session",
    "context",
    "shape",
    "system",
    "signal",
    "pattern",
    "portal",
    "formalize",
    "codify",
    "universe",
    "physics",
    "memory",
    "handoff",
)

STOP_WORDS = {
    "this",
    "that",
    "with",
    "from",
    "have",
    "will",
    "been",
    "what",
    "when",
    "where",
    "which",
    "their",
    "there",
    "about",
    "would",
    "could",
    "should",
    "these",
    "those",
    "your",
    "they",
    "them",
    "than",
    "then",
    "into",
    "just",
    "like",
    "make",
    "does",
    "also",
    "want",
    "need",
    "here",
    "because",
    "been",
}

SECRET_VALUE_PATTERNS = (
    (re.compile(r"(?im)^\s*[a-z]{4}(?: [a-z]{4}){3}\s*$"), "[REDACTED_APP_PASSWORD]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{10,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\bsk-[A-Za-z0-9]{10,}\b"), "[REDACTED_API_KEY]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
)
SECRET_LABEL_PATTERNS = (
    re.compile(r"(?i)(app password|password|secret|token|api key)\s*:\s*[^\n]+"),
    re.compile(r"(?i)(1password ref)\s*:\s*[^\n]+"),
)


@dataclass
class Prompt:
    timestamp: str
    dt: datetime
    workspace: str
    session_id: str
    text: str
    normalized_text: str
    text_hash: str
    repetitions: int = 1
    classification: str = ""
    summary: str = ""
    outcome: str = ""
    evidence: str = ""
    route_hint: str = ""
    keyword_overlap: int = 0


@dataclass
class Commit:
    hash: str
    timestamp: str
    dt: datetime
    message: str
    workspace: str
    message_lower: str


def parse_datetime(raw: str) -> datetime | None:
    """Parse ISO timestamps from Claude JSONL and git logs into local aware datetimes."""
    if not raw:
        return None

    candidates = [raw.strip(), raw.strip()[:19]]
    for candidate in candidates:
        try:
            dt = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt.tzinfo is None:
            return dt.replace(tzinfo=WINDOW_START.tzinfo)
        return dt.astimezone(WINDOW_START.tzinfo)
    return None


def in_window(dt: datetime | None) -> bool:
    return dt is not None and WINDOW_START <= dt < WINDOW_END


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def redact_text(text: str) -> str:
    redacted = text
    for pattern, replacement in SECRET_VALUE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    for pattern in SECRET_LABEL_PATTERNS:
        redacted = pattern.sub(lambda m: m.group(0).split(":", 1)[0] + ": [REDACTED]", redacted)
    return redacted


def extract_prompt_text(obj: dict[str, object]) -> str:
    msg = obj.get("message", {})
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content", "")
    if isinstance(content, list):
        return " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        ).strip()
    return str(content).strip()


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.lower().encode("utf-8")).hexdigest()[:16]


def extract_prompts() -> list[Prompt]:
    prompts: list[Prompt] = []

    for workspace, session_dir in SESSION_DIRS.items():
        if not session_dir.exists():
            continue
        for jsonl_file in sorted(session_dir.glob("*.jsonl")):
            session_id = jsonl_file.stem[:8]
            with open(jsonl_file, encoding="utf-8") as handle:
                for line in handle:
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("type") != "user" or obj.get("isMeta", False):
                        continue
                    dt = parse_datetime(str(obj.get("timestamp", "")))
                    if not in_window(dt):
                        continue
                    raw_text = extract_prompt_text(obj)
                    if len(raw_text) < 5:
                        continue
                    normalized = normalize_text(raw_text)
                    prompts.append(
                        Prompt(
                            timestamp=dt.isoformat(timespec="seconds"),
                            dt=dt,
                            workspace=workspace,
                            session_id=session_id,
                            text=raw_text,
                            normalized_text=normalized,
                            text_hash=prompt_hash(normalized),
                        )
                    )

    return sorted(prompts, key=lambda prompt: prompt.dt)


def deduplicate_prompts(prompts: list[Prompt]) -> tuple[list[Prompt], int]:
    unique: list[Prompt] = []
    seen: dict[str, Prompt] = {}
    duplicates = 0

    for prompt in prompts:
        first = seen.get(prompt.text_hash)
        if first is None:
            seen[prompt.text_hash] = prompt
            unique.append(prompt)
            continue
        first.repetitions += 1
        duplicates += 1

    return unique, duplicates


def is_noise(text: str) -> bool:
    return any(pattern.match(text.strip()) for pattern in NOISE_PATTERNS)


def is_steering(text: str) -> bool:
    normalized = normalize_text(text)
    return any(pattern.match(normalized) for pattern in STEERING_PATTERNS)


def classify(prompt: Prompt) -> str:
    text = prompt.normalized_text
    text_lower = text.lower()

    if is_noise(text):
        return "NOISE"
    if is_steering(text):
        return "STEERING"

    scores = {
        category: sum(1 for keyword in keywords if keyword in text_lower)
        for category, keywords in CLASSIFY_PATTERNS.items()
    }
    if max(scores.values(), default=0) == 0:
        return "META"
    return max(scores, key=lambda category: scores[category])


def summarize(text: str, repetitions: int = 1) -> str:
    clean = redact_text(text.replace("↵", "\n")).strip()
    lines = [
        line.strip()
        for line in clean.splitlines()
        if line.strip() and not line.strip().startswith("<")
    ]
    if not lines:
        summary = "(empty)"
    else:
        first = lines[0][:120]
        summary = first + ("..." if len(lines[0]) > 120 else "")
    if repetitions > 1:
        summary = f"{summary} (x{repetitions})"
    return summary


def extract_commits() -> list[Commit]:
    commits: list[Commit] = []

    for workspace, repo_dir in WORKSPACES.items():
        if not repo_dir.exists():
            continue
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={WINDOW_START.isoformat()}",
                f"--until={WINDOW_END.isoformat()}",
                "--format=%h|%aI|%s",
            ],
            capture_output=True,
            text=True,
            cwd=repo_dir,
            timeout=10,
            check=False,
        )
        for line in result.stdout.splitlines():
            if "|" not in line:
                continue
            commit_hash, raw_timestamp, message = line.split("|", 2)
            dt = parse_datetime(raw_timestamp)
            if not in_window(dt):
                continue
            commits.append(
                Commit(
                    hash=commit_hash,
                    timestamp=dt.isoformat(timespec="seconds"),
                    dt=dt,
                    message=message,
                    workspace=workspace,
                    message_lower=message.lower(),
                )
            )

    return sorted(commits, key=lambda commit: commit.dt)


def meaningful_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9-]{3,}", text.lower())) - STOP_WORDS


def commit_match_score(prompt: Prompt, commit: Commit, words: set[str]) -> tuple[float, int]:
    overlap = sum(1 for word in words if word in commit.message_lower)
    if overlap == 0:
        return 0.0, 0

    delta = commit.dt - prompt.dt
    delta_hours = abs(delta.total_seconds()) / 3600
    time_bonus = 0.0
    if timedelta() <= delta <= timedelta(hours=6):
        time_bonus = 0.75
    elif timedelta() <= delta <= timedelta(hours=24):
        time_bonus = 0.35
    elif delta_hours <= 48:
        time_bonus = 0.1

    return overlap + time_bonus, overlap


def nearby_commit_count(prompt: Prompt, commits: list[Commit], hours: int = 8) -> int:
    horizon = prompt.dt + timedelta(hours=hours)
    return sum(1 for commit in commits if prompt.dt <= commit.dt <= horizon)


def is_absorbable(prompt: Prompt, active_commit_window: int) -> bool:
    if prompt.classification not in ABSORBABLE_CLASSIFICATIONS:
        return False
    if active_commit_window == 0:
        return False

    text_lower = prompt.normalized_text.lower()
    if any(phrase in text_lower for phrase in ABSORBED_PHRASES):
        return True

    abstract_hits = sum(1 for term in ABSORBED_TERMS if term in text_lower)
    return abstract_hits >= 1 and len(meaningful_words(text_lower)) >= 8


def build_route_hint(prompt: Prompt) -> str:
    if classify_intake is None or route_intake is None:
        return ""
    try:
        intake = classify_intake(prompt.normalized_text)
        dispatch = route_intake(intake)
    except Exception:
        return ""

    workspace = Path(dispatch.workspace).name if dispatch.workspace else "operator-decision"
    if intake.domain.value == "unknown":
        return f"unknown -> {dispatch.agent}"
    return f"{intake.domain.value} -> {workspace} ({dispatch.agent})"


def match_outcomes(prompts: list[Prompt], commits: list[Commit]) -> None:
    for prompt in prompts:
        if prompt.classification == "NOISE":
            continue

        if prompt.classification == "STEERING":
            prompt.outcome = "STEERING"
            prompt.evidence = "Routing confirmation or dispatch command"
            continue

        text_lower = prompt.normalized_text.lower()
        words = meaningful_words(text_lower)

        best_score = 0.0
        best_overlap = 0
        best_commit: Commit | None = None
        for commit in commits:
            score, overlap = commit_match_score(prompt, commit, words)
            if score > best_score:
                best_score = score
                best_overlap = overlap
                best_commit = commit

        prompt.keyword_overlap = best_overlap

        if best_overlap >= 3 and best_commit is not None:
            prompt.outcome = "DELIVERED"
            prompt.evidence = (
                f"{best_commit.hash} ({best_commit.workspace}): {best_commit.message[:90]}"
            )
            continue

        if best_overlap >= 2 and best_commit is not None:
            prompt.outcome = "PARTIAL"
            prompt.evidence = (
                f"Possible: {best_commit.hash} ({best_commit.workspace}): "
                f"{best_commit.message[:90]}"
            )
            continue

        if any(term in text_lower for term in ("billing", "enterprise", "copilot", "ghas")):
            prompt.outcome = "HUMAN-ACTION"
            prompt.evidence = "Requires operator action (billing / infrastructure)"
            continue

        if any(term in text_lower for term in ("irf", "irf-", "future", "next session", "later")):
            prompt.outcome = "DEFERRED"
            prompt.evidence = "Explicit future reference"
            continue

        active_commit_window = nearby_commit_count(prompt, commits)
        if is_absorbable(prompt, active_commit_window):
            prompt.outcome = "ABSORBED"
            prompt.evidence = (
                "Conceptual intake without direct keyword trace; "
                f"{active_commit_window} commits landed within 8h"
            )
            continue

        prompt.outcome = "UNRESOLVED"
        prompt.route_hint = build_route_hint(prompt)
        if prompt.route_hint:
            prompt.evidence = f"Route hint: {prompt.route_hint}"


def counts_by(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def generate_report(raw_prompt_count: int, duplicate_count: int, prompts: list[Prompt], commits: list[Commit]) -> str:
    lines: list[str] = []

    noise_count = sum(1 for prompt in prompts if prompt.classification == "NOISE")
    actionable = [prompt for prompt in prompts if prompt.classification != "NOISE"]

    lines.append("# Prompt-to-Outcome Reconciliation — 72 Hours")
    lines.append(f"\n**Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"**Window:** {WINDOW_LABEL}")
    lines.append(f"**Raw prompts in window:** {raw_prompt_count}")
    lines.append(f"**Duplicates collapsed:** {duplicate_count}")
    lines.append(f"**Unique prompts:** {len(prompts)}")
    lines.append(f"**Noise filtered:** {noise_count}")
    lines.append(f"**Actionable:** {len(actionable)}")
    lines.append(f"**Commits available:** {len(commits)}")

    outcomes = counts_by([prompt.outcome for prompt in actionable])
    lines.append("\n## Statistics\n")
    lines.append("| Outcome | Count | % |")
    lines.append("|---------|-------|---|")
    for outcome in (
        "DELIVERED",
        "PARTIAL",
        "STEERING",
        "ABSORBED",
        "UNRESOLVED",
        "DEFERRED",
        "HUMAN-ACTION",
    ):
        count = outcomes.get(outcome, 0)
        pct = f"{(count / len(actionable) * 100):.1f}" if actionable else "0.0"
        lines.append(f"| {outcome} | {count} | {pct}% |")

    lines.append("\n## Triage of Former Hanging Work\n")
    lines.append("| Bucket | Count | Meaning |")
    lines.append("|--------|-------|---------|")
    lines.append(f"| STEERING | {outcomes.get('STEERING', 0)} | Routing / confirmation prompts that do not imply a deliverable |")
    lines.append(f"| ABSORBED | {outcomes.get('ABSORBED', 0)} | Conceptual intake likely folded into nearby work without direct commit-message trace |")
    lines.append(f"| UNRESOLVED | {outcomes.get('UNRESOLVED', 0)} | Still needs explicit follow-on action |")

    classifications = counts_by([prompt.classification for prompt in actionable])
    lines.append("\n## Classification Breakdown\n")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for classification in sorted(classifications, key=lambda key: (-classifications[key], key)):
        lines.append(f"| {classification} | {classifications[classification]} |")

    by_workspace: dict[str, dict[str, int]] = {}
    for prompt in actionable:
        workspace_counts = by_workspace.setdefault(prompt.workspace, {})
        workspace_counts[prompt.outcome] = workspace_counts.get(prompt.outcome, 0) + 1

    lines.append("\n## By Workspace\n")
    lines.append("| Workspace | Delivered | Partial | Steering | Absorbed | Unresolved | Deferred | Human |")
    lines.append("|-----------|-----------|---------|----------|----------|------------|----------|-------|")
    for workspace in sorted(by_workspace):
        counts = by_workspace[workspace]
        lines.append(
            f"| {workspace} | {counts.get('DELIVERED', 0)} | {counts.get('PARTIAL', 0)} | "
            f"{counts.get('STEERING', 0)} | {counts.get('ABSORBED', 0)} | "
            f"{counts.get('UNRESOLVED', 0)} | {counts.get('DEFERRED', 0)} | "
            f"{counts.get('HUMAN-ACTION', 0)} |"
        )

    sections = (
        ("Delivered", "DELIVERED", "| Time | Workspace | Prompt Summary | Evidence |"),
        ("Partial", "PARTIAL", "| Time | Workspace | Prompt Summary | Evidence |"),
        ("Steering", "STEERING", "| Time | Workspace | Prompt Summary | Evidence |"),
        ("Absorbed", "ABSORBED", "| Time | Workspace | Prompt Summary | Evidence |"),
        ("Unresolved", "UNRESOLVED", "| Time | Workspace | Prompt Summary | Route / Evidence |"),
        ("Deferred", "DEFERRED", "| Time | Workspace | Prompt Summary | Evidence |"),
    )

    for title, outcome, header in sections:
        items = [prompt for prompt in actionable if prompt.outcome == outcome]
        lines.append(f"\n## {title} ({len(items)})\n")
        lines.append(header)
        lines.append("|------|-----------|----------------|------------------|")
        for prompt in items:
            detail = prompt.evidence or prompt.route_hint or ""
            lines.append(
                f"| {prompt.timestamp[11:16]} | {prompt.workspace} | {prompt.summary} | {detail} |"
            )

    human = [prompt for prompt in actionable if prompt.outcome == "HUMAN-ACTION"]
    lines.append(f"\n## Human Action Required ({len(human)})\n")
    for prompt in human:
        lines.append(f"- [{prompt.timestamp[11:16]}] {prompt.summary}")

    lines.append("\n---")
    lines.append("*Generated by `scripts/reconcile-72h.py` using prompt timestamps, deduplicated prompt hashes, and pooled commit matching across all tracked workspaces.*")
    lines.append("*Report summaries are redacted for credential-like material.*")
    return "\n".join(lines)


def main() -> None:
    raw_prompts = extract_prompts()
    prompts, duplicate_count = deduplicate_prompts(raw_prompts)

    for prompt in prompts:
        prompt.classification = classify(prompt)
        prompt.summary = summarize(prompt.text, prompt.repetitions)

    commits = extract_commits()
    match_outcomes(prompts, commits)
    print(generate_report(len(raw_prompts), duplicate_count, prompts, commits))


if __name__ == "__main__":
    main()
