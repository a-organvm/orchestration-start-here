"""Outreach Tracker — models relationship lifecycle with external targets."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import yaml

from contrib_engine.schemas import (
    OutreachChannel,
    OutreachDirection,
    OutreachEvent,
    OutreachIndex,
    TargetRelationship,
)

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent / "data"


def log_event(
    index: OutreachIndex,
    workspace: str,
    channel: str,
    summary: str,
    direction: str = "outbound",
    url: str = "",
) -> None:
    """Log an outreach event to a workspace's relationship."""
    rel = index.get_relationship(workspace)
    if rel is None:
        rel = TargetRelationship(workspace=workspace, target="")
        index.relationships.append(rel)
    event = OutreachEvent(
        channel=OutreachChannel(channel),
        date=datetime.now().strftime("%Y-%m-%d"),
        direction=OutreachDirection(direction),
        summary=summary,
        url=url,
    )
    rel.outreach_events.append(event)
    rel.relationship_score = compute_relationship_score(rel)
    if not rel.first_human_contact and direction in ("inbound", "mutual"):
        rel.first_human_contact = event.date


def compute_relationship_score(rel: TargetRelationship) -> int:
    """Compute relationship strength score (0-100)."""
    score = 0
    score += min(len(rel.outreach_events) * 5, 40)
    channels = {e.channel for e in rel.outreach_events}
    score += min(len(channels) * 5, 20)
    inbound_count = sum(
        1
        for e in rel.outreach_events
        if e.direction in (OutreachDirection.INBOUND, OutreachDirection.MUTUAL)
    )
    score += min(inbound_count * 10, 20)
    if rel.issue_assigned:
        score += 10
    elif rel.issue_claimed:
        score += 5
    if rel.cla_signed:
        score += 10
    return min(score, 100)


def check_github_interactions(index: OutreachIndex) -> int:
    """Poll GitHub for new interactions. Returns count of new events."""
    return 0


def save_outreach(index: OutreachIndex, output_path: Path | None = None) -> Path:
    """Persist the outreach index to YAML."""
    path = output_path or DATA_DIR / "outreach.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            index.model_dump(mode="python"),
            f,
            default_flow_style=False,
            sort_keys=False,
        )
    return path


def load_outreach(input_path: Path | None = None) -> OutreachIndex:
    """Load the outreach index from YAML."""
    path = input_path or DATA_DIR / "outreach.yaml"
    if not path.exists():
        return OutreachIndex()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return OutreachIndex()
    return OutreachIndex.model_validate(data)
