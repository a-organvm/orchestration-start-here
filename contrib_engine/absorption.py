"""Absorption Protocol — detect expansive questions from external conversations.

Scans inbound comments across tracked relationships for questions that:
1. Contain assumptions we don't share (assumption divergence)
2. Point at unnamed patterns in our architecture
3. Reveal independent convergence with our design choices

Flagged items enter the formalization pipeline: detect → assess → formalize → deposit.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from contrib_engine.github_client import _run_gh
from contrib_engine.schemas import (
    AbsorptionItem,
    AbsorptionIndex,
    AbsorptionStatus,
    AbsorptionTrigger,
    BackflowItem,
    BackflowStatus,
    BackflowType,
)

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"

# --- Detection heuristics ---

EXPANSION_PATTERNS: list[tuple[str, AbsorptionTrigger, str]] = [
    # (regex, trigger type, evidence template)
    (
        r"how do you (?:handle|deal with|manage|approach)",
        AbsorptionTrigger.UNNAMED_PATTERN,
        "Asks about handling strategy — may point at unnamed pattern",
    ),
    (
        r"what happens (?:when|if)",
        AbsorptionTrigger.UNNAMED_PATTERN,
        "Probes edge case / failure mode — may expose undocumented behavior",
    ),
    (
        r"we (?:ended up|built|did|use|have|went with|opted for|chose)",
        AbsorptionTrigger.INDEPENDENT_CONVERGENCE,
        "Describes their own implementation — potential convergence signal",
    ),
    (
        r"(?:does|would) .+ (?:win|override|take precedence|beat)",
        AbsorptionTrigger.ASSUMPTION_DIVERGENCE,
        "Assumes conflict resolution hierarchy — we may resolve differently",
    ),
    (
        r"isn't that (?:just|basically|essentially)",
        AbsorptionTrigger.ASSUMPTION_DIVERGENCE,
        "Equates our approach with a known pattern — we may differ",
    ),
    (
        r"(?:most|other|typical) (?:\w+ )?(?:systems|frameworks|tools|approaches)",
        AbsorptionTrigger.ASSUMPTION_DIVERGENCE,
        "References conventional approach — our divergence may be the insight",
    ),
    (
        r"(?:the (?:hard|tricky|interesting) part|the real challenge)",
        AbsorptionTrigger.UNNAMED_PATTERN,
        "Identifies a hard subproblem — may point at a pattern worth naming",
    ),
    (
        r"(?:instead of|rather than|as opposed to)",
        AbsorptionTrigger.ASSUMPTION_DIVERGENCE,
        "Contrasts approaches — divergence point worth examining",
    ),
]

REDUCTION_PATTERNS: list[str] = [
    r"what version",
    r"can you add",
    r"this (?:doesn't work|is broken|fails)",
    r"when will",
    r"is there a (?:plan|timeline|eta)",
    r"how do i install",
    r"what (?:license|language)",
]

# Minimum quality thresholds for questioner
MIN_COMMENT_LENGTH = 80  # Short comments rarely contain deep questions


def detect_triggers(text: str) -> list[tuple[AbsorptionTrigger, str]]:
    """Run expansion heuristics against a comment body.

    Returns list of (trigger_type, evidence) for all matches.
    Returns empty list if text matches reduction patterns or is too short.
    """
    if len(text) < MIN_COMMENT_LENGTH:
        return []

    # Check reduction patterns first — early exit
    for pattern in REDUCTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return []

    triggers = []
    for pattern, trigger_type, evidence in EXPANSION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            triggers.append((trigger_type, evidence))

    return triggers


def fetch_inbound_comments(
    owner: str,
    repo: str,
    issue_number: int,
    since: str = "",
    our_username: str = "4444J99",
) -> list[dict[str, Any]]:
    """Fetch comments on an issue/PR from external users (not us).

    Args:
        owner: Repo owner.
        repo: Repo name.
        issue_number: Issue or PR number.
        since: ISO date string — only return comments after this date.
        our_username: Our GitHub username to exclude.

    Returns:
        List of {user, body, created_at, url} dicts.
    """
    result = _run_gh([
        "api", f"repos/{owner}/{repo}/issues/{issue_number}/comments",
        "-q", f'[.[] | select(.user.login != "{our_username}") '
              f'| {{user: .user.login, body: .body, '
              f'created_at: .created_at, '
              f'url: .html_url}}]',
    ], timeout=15)

    if not isinstance(result, list):
        return []

    if since:
        result = [c for c in result if c.get("created_at", "") > since]

    return result


def scan_conversations(
    conversations: list[dict[str, Any]] | None = None,
    since: str = "",
) -> list[AbsorptionItem]:
    """Scan tracked conversations for expansion-worthy questions.

    Args:
        conversations: List of {owner, repo, issue_number} dicts.
            If None, reads from outreach.yaml to find all tracked issues/PRs.
        since: Only scan comments after this ISO date.

    Returns:
        List of newly detected AbsorptionItems.
    """
    if conversations is None:
        conversations = _load_tracked_conversations()

    existing = load_absorption()
    existing_urls = {item.source_url for item in existing.items}

    detected: list[AbsorptionItem] = []

    for conv in conversations:
        owner = conv["owner"]
        repo = conv["repo"]
        issue_number = conv["issue_number"]
        workspace = conv.get("workspace", f"contrib--{owner}-{repo}")

        comments = fetch_inbound_comments(owner, repo, issue_number, since=since)

        for comment in comments:
            url = comment.get("url", "")
            if url in existing_urls:
                continue  # Already tracked

            triggers = detect_triggers(comment.get("body", ""))
            if not triggers:
                continue

            item = AbsorptionItem(
                id=f"abs-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(detected)}",
                workspace=workspace,
                source_url=url,
                questioner=comment.get("user", ""),
                question_text=comment.get("body", "")[:500],
                detected_at=datetime.now().isoformat(),
                triggers=[t for t, _ in triggers],
                trigger_evidence="; ".join(e for _, e in triggers),
                status=AbsorptionStatus.DETECTED,
            )
            detected.append(item)
            logger.info(
                "Detected absorption candidate from @%s: %d triggers — %s",
                item.questioner,
                len(triggers),
                item.trigger_evidence,
            )

    return detected


def _load_tracked_conversations() -> list[dict[str, Any]]:
    """Load tracked conversations from outreach.yaml.

    Extracts GitHub issue/PR URLs from outreach events and returns
    them as {owner, repo, issue_number, workspace} dicts.
    """
    outreach_path = DATA_DIR / "outreach.yaml"
    if not outreach_path.exists():
        return []

    with open(outreach_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or not isinstance(data, dict):
        return []

    conversations = []
    seen = set()

    for rel in data.get("relationships", []):
        target = rel.get("target", "")
        workspace = rel.get("workspace", "")
        if not target or "/" not in target:
            continue

        owner, repo = target.split("/", 1)

        for event in rel.get("outreach_events", []):
            url = event.get("url", "")
            # Extract issue/PR numbers from URLs
            for pattern in [
                rf"github\.com/{re.escape(owner)}/{re.escape(repo)}/(?:pull|issues)/(\d+)",
            ]:
                match = re.search(pattern, url)
                if match:
                    issue_number = int(match.group(1))
                    key = (owner, repo, issue_number)
                    if key not in seen:
                        seen.add(key)
                        conversations.append({
                            "owner": owner,
                            "repo": repo,
                            "issue_number": issue_number,
                            "workspace": workspace,
                        })

    # Also include explicitly tracked conversations
    for conv in load_tracked_conversations_config():
        key = (conv["owner"], conv["repo"], conv["issue_number"])
        if key not in seen:
            seen.add(key)
            conversations.append(conv)

    return conversations


def run_absorption_scan(since: str = "") -> AbsorptionIndex:
    """Run a full absorption scan across all tracked conversations.

    Args:
        since: Only scan comments after this ISO date.

    Returns:
        Updated AbsorptionIndex with newly detected items appended.
    """
    index = load_absorption()
    new_items = scan_conversations(since=since)

    if new_items:
        index.items.extend(new_items)
        save_absorption(index)
        logger.info("Absorption scan: %d new items detected", len(new_items))
    else:
        logger.info("Absorption scan: no new items detected")

    return index


def save_absorption(index: AbsorptionIndex, output_path: Path | None = None) -> Path:
    """Save absorption state to YAML."""
    path = output_path or DATA_DIR / "absorption.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            index.model_dump(mode="json"),
            f,
            default_flow_style=False,
            sort_keys=False,
        )
    return path


def load_absorption(input_path: Path | None = None) -> AbsorptionIndex:
    """Load absorption state from YAML."""
    path = input_path or DATA_DIR / "absorption.yaml"
    if not path.exists():
        return AbsorptionIndex()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return AbsorptionIndex()
    return AbsorptionIndex.model_validate(data)


# --- Tracked conversations (beyond outreach URLs) ---

TRACKED_CONVERSATIONS_PATH = DATA_DIR / "tracked_conversations.yaml"


def load_tracked_conversations_config() -> list[dict[str, Any]]:
    """Load explicitly tracked conversations (issues, discussions, etc.)."""
    if not TRACKED_CONVERSATIONS_PATH.exists():
        return []
    with open(TRACKED_CONVERSATIONS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else []


def save_tracked_conversations_config(conversations: list[dict[str, Any]]) -> None:
    """Save tracked conversations config."""
    TRACKED_CONVERSATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKED_CONVERSATIONS_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(conversations, f, default_flow_style=False, sort_keys=False)


def add_tracked_conversation(
    owner: str, repo: str, issue_number: int, workspace: str = "", label: str = "",
) -> None:
    """Add a conversation to the tracked list."""
    conversations = load_tracked_conversations_config()
    key = f"{owner}/{repo}#{issue_number}"
    for c in conversations:
        if f"{c['owner']}/{c['repo']}#{c['issue_number']}" == key:
            return  # Already tracked
    conversations.append({
        "owner": owner,
        "repo": repo,
        "issue_number": issue_number,
        "workspace": workspace or f"{owner}-{repo}",
        "label": label,
    })
    save_tracked_conversations_config(conversations)
    logger.info("Now tracking conversation: %s", key)


# --- Formalization ---

ORGAN_MAP: dict[str, str] = {
    "theory": "I",
    "formal": "I",
    "pattern": "I",
    "mathematical": "I",
    "generative": "II",
    "diagram": "II",
    "visual": "II",
    "code": "III",
    "implementation": "III",
    "narrative": "V",
    "essay": "V",
    "community": "VI",
    "distribution": "VII",
}


def infer_organ(item: AbsorptionItem) -> str:
    """Infer target organ from triggers and question content.

    Theory/pattern questions → ORGAN-I
    Implementation questions → ORGAN-III
    Most absorption items are theory-level → default to I.
    """
    text = (item.question_text + " " + item.trigger_evidence).lower()
    for keyword, organ in ORGAN_MAP.items():
        if keyword in text:
            return organ
    # Default: unnamed patterns and assumption divergence are theory-level
    return "I"


def generate_formalization_prompt(item: AbsorptionItem) -> str:
    """Generate a structured prompt for formalizing an absorbed question.

    Returns a prompt that can be passed to an LLM agent to produce
    the theory note artifact.
    """
    triggers_str = ", ".join(t.value for t in item.triggers)
    organ = infer_organ(item)

    return f"""## Absorption Protocol — Formalization Task

**Source:** {item.source_url}
**Questioner:** @{item.questioner}
**Workspace:** {item.workspace}
**Triggers:** {triggers_str}
**Evidence:** {item.trigger_evidence}
**Target Organ:** {organ}

### The Question

{item.question_text}

### Your Task

This question triggered the Absorption Protocol because it {_explain_triggers(item.triggers)}.

Write a theory note (markdown) that:

1. **Names the pattern** the question exposed — give it a clear, reusable name
2. **States formal properties** — what are the invariants, guarantees, or constraints?
3. **Distinguishes from similar patterns** — what is this NOT? (table format)
4. **Identifies biological/mathematical analogues** if applicable
5. **Notes independent convergence** if the questioner described their own implementation
6. **Places in relationship to sibling patterns** in the ORGANVM theory corpus

### Output Format

Save the theory note to:
`organvm-{_organ_name(organ)}/my-knowledge-base/intake/canonical/contributions/<pattern-name-kebab>.md`

Then return the pattern name and artifact path for backflow registration.
"""


def _explain_triggers(triggers: list[AbsorptionTrigger]) -> str:
    """Human-readable explanation of why triggers fired."""
    parts = []
    if AbsorptionTrigger.ASSUMPTION_DIVERGENCE in triggers:
        parts.append("contains an assumption we don't share")
    if AbsorptionTrigger.UNNAMED_PATTERN in triggers:
        parts.append("points at something we haven't named")
    if AbsorptionTrigger.INDEPENDENT_CONVERGENCE in triggers:
        parts.append("reveals independent convergence with our design")
    return ", ".join(parts) if parts else "matched expansion heuristics"


def _organ_name(organ: str) -> str:
    """Map organ number to directory name component."""
    names = {
        "I": "i-theoria",
        "II": "ii-poiesis",
        "III": "iii-ergon",
        "IV": "iv-taxis",
        "V": "v-logos",
        "VI": "vi-koinonia",
        "VII": "vii-kerygma",
    }
    return names.get(organ, "i-theoria")


def mark_formalized(
    index: AbsorptionIndex,
    item_id: str,
    pattern_name: str,
    organ: str = "",
) -> AbsorptionItem | None:
    """Mark an absorption item as formalized.

    Args:
        index: The absorption index.
        item_id: ID of the item to mark.
        pattern_name: Name of the pattern that was formalized.
        organ: Target organ (inferred if empty).

    Returns:
        The updated item, or None if not found.
    """
    for item in index.items:
        if item.id == item_id:
            item.status = AbsorptionStatus.FORMALIZED
            item.pattern_name = pattern_name
            item.organ = organ or infer_organ(item)
            return item
    return None


def deposit_to_backflow(
    item: AbsorptionItem,
    artifact_path: str,
) -> BackflowItem:
    """Create a backflow item from a formalized absorption item.

    Args:
        item: The formalized absorption item.
        artifact_path: Path to the theory note artifact.

    Returns:
        The created BackflowItem (caller must add to BackflowIndex and save).
    """
    if item.status != AbsorptionStatus.FORMALIZED:
        raise ValueError(f"Item {item.id} is not formalized (status: {item.status})")

    backflow = BackflowItem(
        workspace=item.workspace,
        organ=item.organ or infer_organ(item),
        backflow_type=BackflowType.THEORY,
        title=item.pattern_name,
        description=f"Absorbed from @{item.questioner}'s question: {item.question_text[:100]}",
        status=BackflowStatus.DEPOSITED,
        artifact_path=artifact_path,
        deposited_at=datetime.now().strftime("%Y-%m-%d"),
    )

    # Update absorption item
    item.status = AbsorptionStatus.DEPOSITED
    item.backflow_ref = f"backflow:{item.organ}:{item.pattern_name}"

    return backflow
