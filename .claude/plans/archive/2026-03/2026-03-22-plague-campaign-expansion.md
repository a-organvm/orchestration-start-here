# The Plague Campaign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the contribution engine from a mechanical PR-shipping machine into a full campaign system with outreach tracking, backflow pipelines, campaign sequencing, and activated workspaces — turning 7 silent open PRs into living symbiotic relationships.

**Architecture:** Three new modules (campaign.py, outreach.py, backflow.py) added to the existing `contrib_engine/` package, all sharing Pydantic models in `schemas.py`. A standalone `__main__.py` entry point provides CLI access. Engine fixes (monitor parsing, CLI wiring) are applied first, then new modules, then data initialization, then workspace activation.

**Tech Stack:** Python 3.11+, Pydantic v2, PyYAML, `gh` CLI (subprocess), pytest

**Spec:** `docs/superpowers/specs/2026-03-22-plague-campaign-expansion-design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `contrib_engine/schemas.py` | MODIFY | Add 12 new models: CampaignPhase, CampaignAction, Campaign, OutreachChannel, OutreachDirection, OutreachEvent, TargetRelationship, OutreachIndex, BackflowType, BackflowStatus, BackflowItem, BackflowIndex |
| `contrib_engine/monitor.py` | MODIFY | Fix `_infer_target()` to handle both seed.yaml formats |
| `contrib_engine/cli.py` | MODIFY | Add `prefix` parameter to `register_contrib_commands()` |
| `contrib_engine/__main__.py` | CREATE | Standalone CLI entry point |
| `contrib_engine/campaign.py` | CREATE | Campaign sequencer: load/save/plan/next_actions/complete |
| `contrib_engine/outreach.py` | CREATE | Outreach tracker: load/save/log/check/show |
| `contrib_engine/backflow.py` | CREATE | Backflow pipeline: load/save/add/deposit/pending |
| `contrib_engine/outreach_protocol.md` | CREATE | Human engagement protocol document |
| `contrib_engine/data/campaign.yaml` | CREATE | Initial campaign state with 13 actions |
| `contrib_engine/data/outreach.yaml` | CREATE | Initial outreach state for 7 workspaces |
| `contrib_engine/data/backflow.yaml` | CREATE | Initial backflow items (pending) |
| `tests/test_contrib_monitor.py` | MODIFY | Add 3 tests for new seed.yaml parsing |
| `tests/test_contrib_campaign.py` | CREATE | 8 tests for campaign sequencer |
| `tests/test_contrib_outreach.py` | CREATE | 6 tests for outreach tracker |
| `tests/test_contrib_backflow.py` | CREATE | 6 tests for backflow pipeline |
| `tests/test_contrib_cli.py` | CREATE | 6 tests for CLI entry point |
| `tests/test_contrib_github_client.py` | CREATE | 3 tests for github_client mocks |
| `tests/test_contrib_scanner_sources.py` | CREATE | 8 tests for new scanner sources |
| `tests/test_contrib_integration.py` | CREATE | 2 cross-module integration tests |

---

## Task 1: Fix Monitor Seed.yaml Parsing

**Files:**
- Modify: `contrib_engine/monitor.py:56-63`
- Test: `tests/test_contrib_monitor.py`

- [ ] **Step 1: Write failing tests for new seed.yaml format**

Add to `tests/test_contrib_monitor.py`:

```python
class TestInferTargetDictFormat:
    def test_infers_from_dict_produces(self):
        """The 6 newer workspaces use dict format with consumers."""
        seed = {
            "produces": [
                {"type": "contribution", "description": "Skills", "consumers": ["anthropics/skills"]}
            ]
        }
        assert _infer_target(seed) == "anthropics/skills"

    def test_infers_from_mixed_produces(self):
        """Handle both string and dict formats in same produces list."""
        seed = {
            "produces": [
                "theory_extraction",
                {"type": "contribution", "consumers": ["dbt-labs/dbt-mcp"]},
            ]
        }
        assert _infer_target(seed) == "dbt-labs/dbt-mcp"

    def test_dict_without_consumers(self):
        """Dict format without consumers returns empty."""
        seed = {
            "produces": [
                {"type": "artifact", "description": "something"}
            ]
        }
        assert _infer_target(seed) == ""
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_monitor.py::TestInferTargetDictFormat -v`
Expected: 3 FAILED (all return "" because dict format not handled)

- [ ] **Step 3: Fix `_infer_target()` in monitor.py**

Replace `_infer_target` in `contrib_engine/monitor.py:56-63`:

```python
def _infer_target(seed: dict) -> str:
    """Infer target repo from seed.yaml produces edges.

    Handles two formats:
    1. String: "pr_to_{owner}_{repo}" -> "{owner}/{repo}"
    2. Dict: {"type": "contribution", "consumers": ["owner/repo"]} -> "owner/repo"
    """
    for edge in seed.get("produces", []):
        if isinstance(edge, str) and edge.startswith("pr_to_"):
            parts = edge.replace("pr_to_", "").split("_", 1)
            if len(parts) == 2:
                return f"{parts[0]}/{parts[1]}"
        elif isinstance(edge, dict):
            consumers = edge.get("consumers", [])
            if consumers and isinstance(consumers, list):
                # First consumer that looks like owner/repo
                for consumer in consumers:
                    if isinstance(consumer, str) and "/" in consumer:
                        return consumer
    return ""
```

- [ ] **Step 4: Run all monitor tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_monitor.py -v`
Expected: 12 passed (9 existing + 3 new)

- [ ] **Step 5: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/monitor.py tests/test_contrib_monitor.py
git commit -m "fix: monitor._infer_target() handles both seed.yaml formats

Supports string 'pr_to_{owner}_{repo}' (adenhq-hive) and dict
{type: contribution, consumers: [owner/repo]} (6 newer workspaces)."
```

---

## Task 2: Expand Schemas with New Models

**Files:**
- Modify: `contrib_engine/schemas.py`

- [ ] **Step 1: Add campaign models to schemas.py**

Append after the `ContributionStatusIndex` class:

```python
# --- Campaign models ---


class CampaignPhase(StrEnum):
    """Phase of a contribution campaign."""

    UNBLOCK = "unblock"
    ENGAGE = "engage"
    CULTIVATE = "cultivate"
    HARVEST = "harvest"
    INJECT = "inject"


class CampaignAction(BaseModel):
    """A single action in the campaign queue."""

    id: str
    workspace: str
    phase: CampaignPhase
    action: str
    priority: int = 0
    manual: bool = False
    automated: bool = False
    blocked_by: list[str] = Field(default_factory=list)
    completed: bool = False
    completed_at: str = ""

    model_config = {"extra": "allow"}


class Campaign(BaseModel):
    """The full campaign state."""

    name: str = "The Plague"
    started: str = ""
    targets: list[str] = Field(default_factory=list)
    actions: list[CampaignAction] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    def next_actions(self, limit: int = 5) -> list[CampaignAction]:
        """Return top-priority unblocked incomplete actions."""
        completed_ids = {a.id for a in self.actions if a.completed}
        available = []
        for a in self.actions:
            if a.completed:
                continue
            # An action is unblocked if all blocked_by IDs are completed
            # or not found (defensive — treat missing as resolved)
            blocked = any(
                bid not in completed_ids
                for bid in a.blocked_by
                if any(x.id == bid for x in self.actions)
            )
            if not blocked:
                available.append(a)
        return sorted(available, key=lambda a: a.priority)[:limit]

    def phase_summary(self) -> dict[str, int]:
        """Count incomplete actions per phase."""
        summary: dict[str, int] = {}
        for a in self.actions:
            if not a.completed:
                summary[a.phase] = summary.get(a.phase, 0) + 1
        return summary


# --- Outreach models ---


class OutreachChannel(StrEnum):
    """Communication channel for outreach."""

    GITHUB_ISSUE = "github_issue"
    GITHUB_PR = "github_pr"
    DISCORD = "discord"
    SLACK = "slack"
    EMAIL = "email"
    TWITTER = "twitter"


class OutreachDirection(StrEnum):
    """Direction of an outreach interaction."""

    OUTBOUND = "outbound"
    INBOUND = "inbound"
    MUTUAL = "mutual"


class OutreachEvent(BaseModel):
    """A single outreach interaction."""

    channel: OutreachChannel
    date: str
    direction: OutreachDirection
    summary: str
    url: str = ""

    model_config = {"extra": "allow"}


class TargetRelationship(BaseModel):
    """Relationship state with a single external target."""

    workspace: str
    target: str
    maintainers: list[str] = Field(default_factory=list)
    community_channels: list[dict] = Field(default_factory=list)
    outreach_events: list[OutreachEvent] = Field(default_factory=list)
    issue_claimed: bool = False
    issue_assigned: bool = False
    cla_signed: bool = False
    first_human_contact: str = ""
    relationship_score: int = 0

    model_config = {"extra": "allow"}


class OutreachIndex(BaseModel):
    """All outreach relationships."""

    generated: str = ""
    relationships: list[TargetRelationship] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    def get_relationship(self, workspace: str) -> TargetRelationship | None:
        for r in self.relationships:
            if r.workspace == workspace:
                return r
        return None


# --- Backflow models ---


class BackflowType(StrEnum):
    """Type of knowledge flowing back into ORGANVM."""

    THEORY = "theory"
    GENERATIVE = "generative"
    CODE = "code"
    NARRATIVE = "narrative"
    COMMUNITY = "community"
    DISTRIBUTION = "distribution"


class BackflowStatus(StrEnum):
    """Status of a backflow item."""

    PENDING = "pending"
    EXTRACTED = "extracted"
    DEPOSITED = "deposited"
    PUBLISHED = "published"


class BackflowItem(BaseModel):
    """A single backflow item to deposit into an ORGANVM organ."""

    workspace: str
    organ: str
    backflow_type: BackflowType
    title: str
    description: str
    status: BackflowStatus = BackflowStatus.PENDING
    artifact_path: str = ""
    deposited_at: str = ""

    model_config = {"extra": "allow"}


class BackflowIndex(BaseModel):
    """All backflow items across all contributions."""

    generated: str = ""
    items: list[BackflowItem] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    def pending_by_organ(self) -> dict[str, list[BackflowItem]]:
        """Group pending items by target organ."""
        result: dict[str, list[BackflowItem]] = {}
        for item in self.items:
            if item.status == BackflowStatus.PENDING:
                result.setdefault(item.organ, []).append(item)
        return result
```

- [ ] **Step 2: Verify all imports work**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -c "from contrib_engine.schemas import Campaign, CampaignAction, CampaignPhase, OutreachIndex, TargetRelationship, OutreachEvent, OutreachChannel, OutreachDirection, BackflowIndex, BackflowItem, BackflowType, BackflowStatus; print('All 12 new models import OK')"`
Expected: `All 12 new models import OK`

- [ ] **Step 3: Run existing tests to verify no regressions**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/ -v`
Expected: All 25+ existing tests still pass

- [ ] **Step 4: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/schemas.py
git commit -m "feat: add campaign, outreach, backflow Pydantic models to schemas

12 new models: CampaignPhase, CampaignAction, Campaign,
OutreachChannel, OutreachDirection, OutreachEvent, TargetRelationship,
OutreachIndex, BackflowType, BackflowStatus, BackflowItem, BackflowIndex.
All follow existing model_config extra=allow + Field(default_factory) patterns."
```

---

## Task 3: Refactor CLI and Create Entry Point

**Files:**
- Modify: `contrib_engine/cli.py`
- Create: `contrib_engine/__main__.py`
- Test: `tests/test_contrib_cli.py`

- [ ] **Step 1: Write failing test for CLI entry point**

Create `tests/test_contrib_cli.py`:

```python
"""Tests for the CLI entry point."""

import subprocess
import sys


class TestCliEntryPoint:
    def test_help_runs(self):
        """python -m contrib_engine --help should exit 0."""
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "--help"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode == 0
        assert "scan" in result.stdout
        assert "campaign" in result.stdout

    def test_scan_subcommand_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "scan", "--help"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode == 0
        assert "--no-github" in result.stdout

    def test_invalid_subcommand(self):
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "nonexistent"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode != 0

    def test_campaign_subcommand_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "campaign", "--help"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode == 0
        assert "show" in result.stdout or "campaign" in result.stdout.lower()

    def test_outreach_subcommand_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "outreach", "--help"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode == 0

    def test_backflow_subcommand_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "contrib_engine", "backflow", "--help"],
            capture_output=True, text=True,
            cwd="/Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here",
        )
        assert result.returncode == 0


class TestPrefixParameter:
    def test_register_with_prefix(self):
        """When prefix is set, commands get prefixed names."""
        import argparse
        from contrib_engine.cli import register_contrib_commands

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        register_contrib_commands(subparsers, prefix="contrib-")
        # Should have contrib-scan, not scan
        args = parser.parse_args(["contrib-scan", "--no-github"])
        assert hasattr(args, "func")

    def test_register_without_prefix(self):
        """When prefix is empty, commands have clean names."""
        import argparse
        from contrib_engine.cli import register_contrib_commands

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        register_contrib_commands(subparsers, prefix="")
        args = parser.parse_args(["scan", "--no-github"])
        assert hasattr(args, "func")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_cli.py -v`
Expected: FAIL (no `__main__.py`, no `prefix` parameter)

- [ ] **Step 3: Refactor cli.py to accept prefix parameter**

In `contrib_engine/cli.py`, change the function signature and all `add_parser` calls:

```python
def register_contrib_commands(
    subparsers: argparse._SubParsersAction,
    prefix: str = "",
) -> None:
    """Register contrib subcommands.

    Args:
        subparsers: Subparsers action from parent ArgumentParser.
        prefix: Command name prefix. Empty for standalone, "contrib-" for embedded.
    """

    scan_parser = subparsers.add_parser(
        f"{prefix}scan",
        help="Scan for open-source contribution targets",
        description="Read application pipeline signals and GitHub data to find targets.",
    )
```

Apply the `f"{prefix}"` pattern to all 5 existing `add_parser` calls: `scan`, `list`, `approve`, `status`, `monitor`.

- [ ] **Step 4: Create `contrib_engine/__main__.py`**

```python
"""Standalone CLI entry point for the contribution engine.

Usage:
    python -m contrib_engine scan [--no-github]
    python -m contrib_engine list [--status STATUS] [--min-score N]
    python -m contrib_engine approve TARGET [--skip-fork] [--skip-remote] [--skip-registry]
    python -m contrib_engine status
    python -m contrib_engine monitor
    python -m contrib_engine campaign {show,next,complete,plan}
    python -m contrib_engine outreach {show,log,check}
    python -m contrib_engine backflow {show,pending,add,deposit}
"""

from __future__ import annotations

import argparse
import sys

from contrib_engine.cli import register_contrib_commands


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="contrib_engine",
        description="ORGANVM Contribution Engine — The Plague Campaign",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Register existing commands with no prefix (standalone mode)
    register_contrib_commands(subparsers, prefix="")

    # Register new campaign commands
    _register_campaign_commands(subparsers)
    _register_outreach_commands(subparsers)
    _register_backflow_commands(subparsers)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)


def _register_campaign_commands(subparsers: argparse._SubParsersAction) -> None:
    campaign = subparsers.add_parser("campaign", help="Campaign sequencer")
    campaign_sub = campaign.add_subparsers(dest="campaign_command")

    show = campaign_sub.add_parser("show", help="Show campaign state + next actions")
    show.set_defaults(func=_cmd_campaign_show)

    nxt = campaign_sub.add_parser("next", help="Show single next action")
    nxt.set_defaults(func=_cmd_campaign_next)

    complete = campaign_sub.add_parser("complete", help="Mark action complete")
    complete.add_argument("action_id", help="Action ID to complete")
    complete.set_defaults(func=_cmd_campaign_complete)

    plan = campaign_sub.add_parser("plan", help="Generate action queue from workspace state")
    plan.set_defaults(func=_cmd_campaign_plan)

    campaign.set_defaults(func=lambda args: campaign.print_help())


def _register_outreach_commands(subparsers: argparse._SubParsersAction) -> None:
    outreach = subparsers.add_parser("outreach", help="Outreach tracker")
    outreach_sub = outreach.add_subparsers(dest="outreach_command")

    show = outreach_sub.add_parser("show", help="Show relationships")
    show.add_argument("workspace", nargs="?", help="Filter by workspace")
    show.set_defaults(func=_cmd_outreach_show)

    log = outreach_sub.add_parser("log", help="Log an outreach event")
    log.add_argument("workspace", help="Workspace name")
    log.add_argument("channel", help="Channel (github_issue, discord, email, ...)")
    log.add_argument("summary", help="Event summary")
    log.set_defaults(func=_cmd_outreach_log)

    check = outreach_sub.add_parser("check", help="Poll GitHub for new interactions")
    check.set_defaults(func=_cmd_outreach_check)

    outreach.set_defaults(func=lambda args: outreach.print_help())


def _register_backflow_commands(subparsers: argparse._SubParsersAction) -> None:
    backflow = subparsers.add_parser("backflow", help="Backflow pipeline")
    backflow_sub = backflow.add_subparsers(dest="backflow_command")

    show = backflow_sub.add_parser("show", help="Show backflow items by organ")
    show.set_defaults(func=_cmd_backflow_show)

    pending = backflow_sub.add_parser("pending", help="Show pending extractions")
    pending.set_defaults(func=_cmd_backflow_pending)

    add = backflow_sub.add_parser("add", help="Add a backflow item")
    add.add_argument("workspace", help="Workspace name")
    add.add_argument("organ", help="Target organ (I, II, III, V, VI, VII)")
    add.add_argument("backflow_type", help="Type (theory, generative, code, narrative, community, distribution)")
    add.add_argument("title", help="Item title")
    add.set_defaults(func=_cmd_backflow_add)

    deposit = backflow_sub.add_parser("deposit", help="Mark item as deposited")
    deposit.add_argument("index", type=int, help="Item index (0-based)")
    deposit.set_defaults(func=_cmd_backflow_deposit)

    backflow.set_defaults(func=lambda args: backflow.print_help())


# --- Command implementations (delegate to modules) ---


def _cmd_campaign_show(args: argparse.Namespace) -> None:
    from contrib_engine.campaign import load_campaign
    campaign = load_campaign()
    print(f"Campaign: {campaign.name} (started {campaign.started})")
    print(f"Targets: {len(campaign.targets)}")
    summary = campaign.phase_summary()
    for phase, count in summary.items():
        print(f"  {phase}: {count} pending")
    print(f"\nNext actions:")
    for a in campaign.next_actions():
        manual = " [MANUAL]" if a.manual else ""
        print(f"  [{a.priority}] {a.id}: {a.action}{manual}")


def _cmd_campaign_next(args: argparse.Namespace) -> None:
    from contrib_engine.campaign import load_campaign
    campaign = load_campaign()
    actions = campaign.next_actions(limit=1)
    if not actions:
        print("No pending actions. Campaign complete!")
        return
    a = actions[0]
    manual = " [MANUAL — requires human action]" if a.manual else ""
    print(f"{a.id}: {a.action}{manual}")
    print(f"  Workspace: {a.workspace}")
    print(f"  Phase: {a.phase}")
    print(f"  Priority: {a.priority}")


def _cmd_campaign_complete(args: argparse.Namespace) -> None:
    from contrib_engine.campaign import complete_action, load_campaign, save_campaign
    campaign = load_campaign()
    if complete_action(campaign, args.action_id):
        save_campaign(campaign)
        print(f"Completed: {args.action_id}")
    else:
        print(f"Action not found: {args.action_id}")
        sys.exit(1)


def _cmd_campaign_plan(args: argparse.Namespace) -> None:
    from contrib_engine.campaign import generate_campaign, save_campaign
    campaign = generate_campaign()
    save_campaign(campaign)
    print(f"Generated campaign with {len(campaign.actions)} actions")


def _cmd_outreach_show(args: argparse.Namespace) -> None:
    from contrib_engine.outreach import load_outreach
    index = load_outreach()
    for r in index.relationships:
        if args.workspace and r.workspace != args.workspace:
            continue
        score = r.relationship_score
        events = len(r.outreach_events)
        print(f"{r.workspace}: {r.target} (score: {score}, events: {events})")
        if args.workspace:
            for e in r.outreach_events:
                print(f"  [{e.date}] {e.channel} ({e.direction}): {e.summary}")


def _cmd_outreach_log(args: argparse.Namespace) -> None:
    from contrib_engine.outreach import load_outreach, log_event, save_outreach
    index = load_outreach()
    log_event(index, args.workspace, args.channel, args.summary)
    save_outreach(index)
    print(f"Logged: {args.channel} event for {args.workspace}")


def _cmd_outreach_check(args: argparse.Namespace) -> None:
    from contrib_engine.outreach import check_github_interactions, load_outreach, save_outreach
    index = load_outreach()
    changes = check_github_interactions(index)
    save_outreach(index)
    print(f"Checked {len(index.relationships)} relationships, {changes} new interactions")


def _cmd_backflow_show(args: argparse.Namespace) -> None:
    from contrib_engine.backflow import load_backflow
    index = load_backflow()
    by_organ: dict[str, list] = {}
    for item in index.items:
        by_organ.setdefault(item.organ, []).append(item)
    for organ, items in sorted(by_organ.items()):
        print(f"\nORGAN-{organ}:")
        for item in items:
            print(f"  [{item.status}] {item.workspace}: {item.title} ({item.backflow_type})")


def _cmd_backflow_pending(args: argparse.Namespace) -> None:
    from contrib_engine.backflow import load_backflow
    index = load_backflow()
    pending = index.pending_by_organ()
    if not pending:
        print("No pending backflow items.")
        return
    for organ, items in sorted(pending.items()):
        print(f"\nORGAN-{organ}: {len(items)} pending")
        for item in items:
            print(f"  {item.workspace}: {item.title}")


def _cmd_backflow_add(args: argparse.Namespace) -> None:
    from contrib_engine.backflow import add_item, load_backflow, save_backflow
    index = load_backflow()
    add_item(index, args.workspace, args.organ, args.backflow_type, args.title)
    save_backflow(index)
    print(f"Added backflow item: {args.title} -> ORGAN-{args.organ}")


def _cmd_backflow_deposit(args: argparse.Namespace) -> None:
    from contrib_engine.backflow import deposit_item, load_backflow, save_backflow
    index = load_backflow()
    if deposit_item(index, args.index):
        save_backflow(index)
        print(f"Deposited item {args.index}")
    else:
        print(f"Item index {args.index} not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run CLI tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_cli.py -v`
Expected: Some pass (help, prefix), some fail (campaign/outreach/backflow modules not yet created). That's expected — they depend on Tasks 4-6.

- [ ] **Step 6: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/cli.py contrib_engine/__main__.py tests/test_contrib_cli.py
git commit -m "feat: standalone CLI entry point + prefix parameter for cli.py

python -m contrib_engine {scan,list,approve,status,monitor,campaign,outreach,backflow}
cli.py accepts prefix parameter for dual-mode registration."
```

---

## Task 4: Build Campaign Sequencer

**Files:**
- Create: `contrib_engine/campaign.py`
- Test: `tests/test_contrib_campaign.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_contrib_campaign.py`:

```python
"""Tests for the campaign sequencer."""

from datetime import datetime
from pathlib import Path

import yaml

from contrib_engine.schemas import Campaign, CampaignAction, CampaignPhase


class TestNextActions:
    def test_returns_lowest_priority_first(self):
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="low", workspace="w", phase=CampaignPhase.ENGAGE, action="low", priority=3),
                CampaignAction(id="high", workspace="w", phase=CampaignPhase.UNBLOCK, action="high", priority=0),
                CampaignAction(id="mid", workspace="w", phase=CampaignPhase.ENGAGE, action="mid", priority=1),
            ],
        )
        result = campaign.next_actions(limit=2)
        assert [a.id for a in result] == ["high", "mid"]

    def test_excludes_completed(self):
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="done", workspace="w", phase=CampaignPhase.UNBLOCK, action="done", completed=True),
                CampaignAction(id="todo", workspace="w", phase=CampaignPhase.ENGAGE, action="todo", priority=1),
            ],
        )
        result = campaign.next_actions()
        assert [a.id for a in result] == ["todo"]

    def test_respects_blocked_by(self):
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="first", workspace="w", phase=CampaignPhase.UNBLOCK, action="first", priority=0),
                CampaignAction(id="second", workspace="w", phase=CampaignPhase.UNBLOCK, action="second", priority=0, blocked_by=["first"]),
            ],
        )
        result = campaign.next_actions()
        assert [a.id for a in result] == ["first"]

    def test_unblocks_when_dependency_completed(self):
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="first", workspace="w", phase=CampaignPhase.UNBLOCK, action="first", completed=True),
                CampaignAction(id="second", workspace="w", phase=CampaignPhase.UNBLOCK, action="second", blocked_by=["first"]),
            ],
        )
        result = campaign.next_actions()
        assert [a.id for a in result] == ["second"]

    def test_missing_blocked_by_treated_as_unblocked(self):
        """If blocked_by references an ID not in the actions list, treat as unblocked."""
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="orphan", workspace="w", phase=CampaignPhase.ENGAGE, action="orphan", blocked_by=["nonexistent"]),
            ],
        )
        result = campaign.next_actions()
        assert [a.id for a in result] == ["orphan"]

    def test_empty_campaign(self):
        campaign = Campaign(started="2026-03-22")
        assert campaign.next_actions() == []


class TestPhaseSummary:
    def test_counts_incomplete_by_phase(self):
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="a", workspace="w", phase=CampaignPhase.UNBLOCK, action="a"),
                CampaignAction(id="b", workspace="w", phase=CampaignPhase.UNBLOCK, action="b", completed=True),
                CampaignAction(id="c", workspace="w", phase=CampaignPhase.ENGAGE, action="c"),
            ],
        )
        summary = campaign.phase_summary()
        assert summary["unblock"] == 1
        assert summary["engage"] == 1
        assert "cultivate" not in summary


class TestCompleteAction:
    def test_complete_marks_done(self):
        from contrib_engine.campaign import complete_action

        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(id="test", workspace="w", phase=CampaignPhase.UNBLOCK, action="test"),
            ],
        )
        assert complete_action(campaign, "test")
        assert campaign.actions[0].completed
        assert campaign.actions[0].completed_at != ""

    def test_complete_nonexistent_returns_false(self):
        from contrib_engine.campaign import complete_action

        campaign = Campaign(started="2026-03-22")
        assert not complete_action(campaign, "nonexistent")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_campaign.py -v`
Expected: FAIL (campaign module not found)

- [ ] **Step 3: Create `contrib_engine/campaign.py`**

```python
"""Campaign Sequencer — prescriptive action queue for the Plague campaign.

Reads workspace states, PR states, and outreach data to produce a
priority-ordered queue of actions across all 7 contribution targets.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import yaml

from contrib_engine.schemas import Campaign, CampaignAction, CampaignPhase

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"


def complete_action(campaign: Campaign, action_id: str) -> bool:
    """Mark a campaign action as completed."""
    for action in campaign.actions:
        if action.id == action_id:
            action.completed = True
            action.completed_at = datetime.now().isoformat()
            return True
    return False


def generate_campaign() -> Campaign:
    """Generate a campaign from current workspace states.

    Reads contrib--* workspaces and their seed.yaml files to build
    the initial action queue. For now, loads from the existing
    campaign.yaml if it exists, or returns an empty campaign.
    """
    existing = load_campaign()
    if existing.actions:
        return existing
    return Campaign(started=datetime.now().strftime("%Y-%m-%d"))


def save_campaign(campaign: Campaign, output_path: Path | None = None) -> Path:
    """Save campaign state to YAML."""
    path = output_path or DATA_DIR / "campaign.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            campaign.model_dump(mode="python"),
            f,
            default_flow_style=False,
            sort_keys=False,
        )
    return path


def load_campaign(input_path: Path | None = None) -> Campaign:
    """Load campaign state from YAML."""
    path = input_path or DATA_DIR / "campaign.yaml"
    if not path.exists():
        return Campaign()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return Campaign()
    return Campaign.model_validate(data)
```

- [ ] **Step 4: Run campaign tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_campaign.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/campaign.py tests/test_contrib_campaign.py
git commit -m "feat: campaign sequencer with priority ordering and blocked_by resolution"
```

---

## Task 5: Build Outreach Tracker

**Files:**
- Create: `contrib_engine/outreach.py`
- Test: `tests/test_contrib_outreach.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_contrib_outreach.py`:

```python
"""Tests for the outreach tracker."""

from pathlib import Path

import yaml

from contrib_engine.schemas import (
    OutreachChannel,
    OutreachDirection,
    OutreachEvent,
    OutreachIndex,
    TargetRelationship,
)


class TestLogEvent:
    def test_logs_event_to_existing_relationship(self):
        from contrib_engine.outreach import log_event

        index = OutreachIndex(
            generated="2026-03-22",
            relationships=[
                TargetRelationship(workspace="contrib--adenhq-hive", target="adenhq/hive"),
            ],
        )
        log_event(index, "contrib--adenhq-hive", "github_pr", "Submitted PR #6707")
        assert len(index.relationships[0].outreach_events) == 1
        assert index.relationships[0].outreach_events[0].channel == OutreachChannel.GITHUB_PR

    def test_logs_event_creates_relationship_if_missing(self):
        from contrib_engine.outreach import log_event

        index = OutreachIndex(generated="2026-03-22")
        log_event(index, "contrib--new", "discord", "Joined community")
        assert len(index.relationships) == 1
        assert index.relationships[0].workspace == "contrib--new"

    def test_multiple_events(self):
        from contrib_engine.outreach import log_event

        index = OutreachIndex(
            generated="2026-03-22",
            relationships=[
                TargetRelationship(workspace="w", target="t"),
            ],
        )
        log_event(index, "w", "github_pr", "PR submitted")
        log_event(index, "w", "discord", "Joined server")
        assert len(index.relationships[0].outreach_events) == 2


class TestRelationshipScore:
    def test_score_increases_with_events(self):
        from contrib_engine.outreach import compute_relationship_score

        rel = TargetRelationship(
            workspace="w", target="t",
            outreach_events=[
                OutreachEvent(channel=OutreachChannel.GITHUB_PR, date="2026-03-22", direction=OutreachDirection.OUTBOUND, summary="PR"),
                OutreachEvent(channel=OutreachChannel.DISCORD, date="2026-03-22", direction=OutreachDirection.OUTBOUND, summary="Joined"),
            ],
        )
        score = compute_relationship_score(rel)
        assert score > 0

    def test_score_zero_with_no_events(self):
        from contrib_engine.outreach import compute_relationship_score

        rel = TargetRelationship(workspace="w", target="t")
        assert compute_relationship_score(rel) == 0


class TestPersistence:
    def test_save_and_load_roundtrip(self, tmp_path):
        from contrib_engine.outreach import load_outreach, save_outreach

        index = OutreachIndex(
            generated="2026-03-22",
            relationships=[
                TargetRelationship(workspace="w", target="t", issue_claimed=True),
            ],
        )
        path = save_outreach(index, tmp_path / "outreach.yaml")
        loaded = load_outreach(path)
        assert len(loaded.relationships) == 1
        assert loaded.relationships[0].issue_claimed is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_outreach.py -v`
Expected: FAIL

- [ ] **Step 3: Create `contrib_engine/outreach.py`**

```python
"""Outreach Tracker — models relationship lifecycle with external targets.

Tracks human engagement: Discord joins, issue claims, email threads,
PR comments, community participation.
"""

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

    # Events (0-40): 5 points per event, capped
    score += min(len(rel.outreach_events) * 5, 40)

    # Channel diversity (0-20): 5 points per unique channel
    channels = {e.channel for e in rel.outreach_events}
    score += min(len(channels) * 5, 20)

    # Inbound signals (0-20): 10 points per inbound/mutual event
    inbound_count = sum(
        1 for e in rel.outreach_events
        if e.direction in (OutreachDirection.INBOUND, OutreachDirection.MUTUAL)
    )
    score += min(inbound_count * 10, 20)

    # Assignment (0-10)
    if rel.issue_assigned:
        score += 10
    elif rel.issue_claimed:
        score += 5

    # CLA (0-10)
    if rel.cla_signed:
        score += 10

    return min(score, 100)


def check_github_interactions(index: OutreachIndex) -> int:
    """Poll GitHub for new interactions on tracked PRs. Returns count of new events."""
    # Placeholder — full implementation requires PR polling per workspace
    return 0


def save_outreach(index: OutreachIndex, output_path: Path | None = None) -> Path:
    """Save outreach index to YAML."""
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
    """Load outreach index from YAML."""
    path = input_path or DATA_DIR / "outreach.yaml"
    if not path.exists():
        return OutreachIndex()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return OutreachIndex()
    return OutreachIndex.model_validate(data)
```

- [ ] **Step 4: Run outreach tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_outreach.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/outreach.py tests/test_contrib_outreach.py
git commit -m "feat: outreach tracker with event logging, scoring, persistence"
```

---

## Task 6: Build Backflow Pipeline

**Files:**
- Create: `contrib_engine/backflow.py`
- Test: `tests/test_contrib_backflow.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_contrib_backflow.py`:

```python
"""Tests for the backflow pipeline."""

from contrib_engine.schemas import BackflowIndex, BackflowItem, BackflowStatus, BackflowType


class TestAddItem:
    def test_adds_item(self):
        from contrib_engine.backflow import add_item

        index = BackflowIndex(generated="2026-03-22")
        add_item(index, "contrib--adenhq-hive", "I", "theory", "Forward-only lifecycle pattern")
        assert len(index.items) == 1
        assert index.items[0].organ == "I"
        assert index.items[0].backflow_type == BackflowType.THEORY

    def test_adds_multiple_items(self):
        from contrib_engine.backflow import add_item

        index = BackflowIndex(generated="2026-03-22")
        add_item(index, "w", "I", "theory", "Pattern A")
        add_item(index, "w", "II", "generative", "Diagram B")
        add_item(index, "w", "V", "narrative", "Essay C")
        assert len(index.items) == 3


class TestDepositItem:
    def test_deposits_item(self):
        from contrib_engine.backflow import deposit_item

        index = BackflowIndex(
            generated="2026-03-22",
            items=[
                BackflowItem(workspace="w", organ="I", backflow_type=BackflowType.THEORY, title="T", description="D"),
            ],
        )
        assert deposit_item(index, 0)
        assert index.items[0].status == BackflowStatus.DEPOSITED
        assert index.items[0].deposited_at != ""

    def test_deposit_invalid_index(self):
        from contrib_engine.backflow import deposit_item

        index = BackflowIndex(generated="2026-03-22")
        assert not deposit_item(index, 0)


class TestPendingByOrgan:
    def test_groups_pending(self):
        index = BackflowIndex(
            generated="2026-03-22",
            items=[
                BackflowItem(workspace="w", organ="I", backflow_type=BackflowType.THEORY, title="A", description=""),
                BackflowItem(workspace="w", organ="I", backflow_type=BackflowType.CODE, title="B", description=""),
                BackflowItem(workspace="w", organ="V", backflow_type=BackflowType.NARRATIVE, title="C", description=""),
                BackflowItem(workspace="w", organ="I", backflow_type=BackflowType.THEORY, title="D", description="", status=BackflowStatus.DEPOSITED),
            ],
        )
        pending = index.pending_by_organ()
        assert len(pending["I"]) == 2
        assert len(pending["V"]) == 1
        assert "deposited" not in str(pending)

    def test_empty_returns_empty(self):
        index = BackflowIndex(generated="2026-03-22")
        assert index.pending_by_organ() == {}


class TestPersistence:
    def test_save_and_load_roundtrip(self, tmp_path):
        from contrib_engine.backflow import load_backflow, save_backflow

        index = BackflowIndex(
            generated="2026-03-22",
            items=[
                BackflowItem(workspace="w", organ="I", backflow_type=BackflowType.THEORY, title="T", description="D"),
            ],
        )
        path = save_backflow(index, tmp_path / "backflow.yaml")
        loaded = load_backflow(path)
        assert len(loaded.items) == 1
        assert loaded.items[0].backflow_type == BackflowType.THEORY
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_backflow.py -v`
Expected: FAIL

- [ ] **Step 3: Create `contrib_engine/backflow.py`**

```python
"""Backflow Pipeline — tracks knowledge flowing back into ORGANVM organs.

Each external contribution produces backflow items: theory for ORGAN-I,
visualizations for ORGAN-II, code patterns for ORGAN-III, narratives
for ORGAN-V, community for ORGAN-VI, distribution for ORGAN-VII.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import yaml

from contrib_engine.schemas import (
    BackflowIndex,
    BackflowItem,
    BackflowStatus,
    BackflowType,
)

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"


def add_item(
    index: BackflowIndex,
    workspace: str,
    organ: str,
    backflow_type: str,
    title: str,
    description: str = "",
) -> None:
    """Add a pending backflow item."""
    item = BackflowItem(
        workspace=workspace,
        organ=organ,
        backflow_type=BackflowType(backflow_type),
        title=title,
        description=description,
    )
    index.items.append(item)


def deposit_item(index: BackflowIndex, item_index: int) -> bool:
    """Mark a backflow item as deposited into its target organ."""
    if item_index < 0 or item_index >= len(index.items):
        return False
    index.items[item_index].status = BackflowStatus.DEPOSITED
    index.items[item_index].deposited_at = datetime.now().isoformat()
    return True


def save_backflow(index: BackflowIndex, output_path: Path | None = None) -> Path:
    """Save backflow index to YAML."""
    path = output_path or DATA_DIR / "backflow.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            index.model_dump(mode="python"),
            f,
            default_flow_style=False,
            sort_keys=False,
        )
    return path


def load_backflow(input_path: Path | None = None) -> BackflowIndex:
    """Load backflow index from YAML."""
    path = input_path or DATA_DIR / "backflow.yaml"
    if not path.exists():
        return BackflowIndex()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return BackflowIndex()
    return BackflowIndex.model_validate(data)
```

- [ ] **Step 4: Run backflow tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_backflow.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/backflow.py tests/test_contrib_backflow.py
git commit -m "feat: backflow pipeline with organ routing and deposit tracking"
```

---

## Task 7: Full Test Suite Verification + CLI Integration

**Files:**
- All test files
- `tests/test_contrib_cli.py` (re-run after modules exist)

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_*.py -v --tb=short`
Expected: All tests pass (25 existing + 20+ new)

- [ ] **Step 2: Run CLI help to verify all subcommands**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m contrib_engine --help`
Expected: Lists scan, list, approve, status, monitor, campaign, outreach, backflow

- [ ] **Step 3: Run CLI integration smoke test**

Run:
```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
python3 -m contrib_engine campaign show 2>&1
python3 -m contrib_engine outreach show 2>&1
python3 -m contrib_engine backflow pending 2>&1
```
Expected: No crashes (empty data is OK)

- [ ] **Step 4: Commit any fixes needed**

---

## Task 8: Generate Initial Campaign Data

**Files:**
- Create: `contrib_engine/data/campaign.yaml`
- Create: `contrib_engine/data/outreach.yaml`
- Create: `contrib_engine/data/backflow.yaml`
- Create: `contrib_engine/outreach_protocol.md`

- [ ] **Step 1: Write campaign.yaml**

Write `contrib_engine/data/campaign.yaml` with the 13 actions from the spec (Section 5 — the full flat YAML structure with UNBLOCK and ENGAGE phases).

- [ ] **Step 2: Write outreach.yaml**

Generate initial outreach state from the 7 workspaces and their PR data:

```yaml
generated: "2026-03-22"
relationships:
  - workspace: contrib--adenhq-hive
    target: adenhq/hive
    maintainers: [vincent-jiang]
    community_channels:
      - type: discord
        url: ""
        joined: false
    outreach_events:
      - channel: github_pr
        date: "2026-03-21"
        direction: outbound
        summary: "Submitted PR #6707 — design versioning system"
        url: "https://github.com/adenhq/hive/pull/6707"
    issue_claimed: false
    issue_assigned: false
  - workspace: contrib--anthropic-skills
    target: anthropics/skills
    outreach_events:
      - channel: github_pr
        date: "2026-03-21"
        direction: outbound
        summary: "Submitted PR #723 — testing-patterns skill"
        url: "https://github.com/anthropics/skills/pull/723"
  # ... (repeat for all 7)
```

- [ ] **Step 3: Write backflow.yaml**

Generate pending backflow items for each workspace — at minimum 1 per organ:

```yaml
generated: "2026-03-22"
items:
  - workspace: contrib--adenhq-hive
    organ: "I"
    backflow_type: theory
    title: "Forward-only lifecycle state machine as universal governance pattern"
    description: "Extracted from fusion of ORGANVM promotion FSM + Hive QueenPhaseState"
    status: pending
  - workspace: contrib--adenhq-hive
    organ: "II"
    backflow_type: generative
    title: "State transition comparison diagrams"
    description: "Mermaid diagrams comparing ORGANVM vs Hive lifecycle models"
    status: pending
  # ... (entries for all 7 workspaces x relevant organs)
```

- [ ] **Step 4: Write outreach_protocol.md**

Write `contrib_engine/outreach_protocol.md` from spec Section 6 — the full Pre-PR, Active PR, Post-Merge, Post-Rejection protocol.

- [ ] **Step 5: Verify data loads**

Run:
```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
python3 -m contrib_engine campaign show
python3 -m contrib_engine outreach show
python3 -m contrib_engine backflow pending
```
Expected: All three display data correctly

- [ ] **Step 6: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/data/ contrib_engine/outreach_protocol.md
git commit -m "feat: initialize campaign data — 13 actions, 7 relationships, backflow items

The Plague campaign is live with UNBLOCK and ENGAGE phase actions
across all 7 contribution targets."
```

---

## Task 9: Scanner Source Expansion

**Files:**
- Modify: `contrib_engine/scanner.py`
- Modify: `contrib_engine/github_client.py` (add `list_user_forks()`)
- Test: `tests/test_contrib_scanner_sources.py`
- Test: `tests/test_contrib_github_client.py`

- [ ] **Step 1: Write failing tests for new scanner sources**

Create `tests/test_contrib_scanner_sources.py`:

```python
"""Tests for expanded scanner data sources."""

from unittest.mock import patch
from pathlib import Path

import yaml

from contrib_engine.scanner import (
    _extract_star_signals,
    _extract_fork_signals,
    _extract_pr_history,
    _extract_dependency_signals,
)
from contrib_engine.schemas import ContributionTarget


class TestStarSignals:
    def test_extracts_stargazers(self):
        with patch("contrib_engine.scanner.who_starred_my_repos") as mock:
            mock.return_value = [{"login": "user1", "repo": "4444J99/hive"}]
            result = _extract_star_signals()
            assert len(result) == 1
            assert result[0]["login"] == "user1"

    def test_empty_on_no_stars(self):
        with patch("contrib_engine.scanner.who_starred_my_repos") as mock:
            mock.return_value = []
            result = _extract_star_signals()
            assert result == []


class TestForkSignals:
    def test_extracts_forks(self):
        with patch("contrib_engine.scanner.list_user_forks") as mock:
            mock.return_value = [
                {"name": "hive", "parent": {"owner": "adenhq", "name": "hive"}},
                {"name": "langgraph", "parent": {"owner": "langchain-ai", "name": "langgraph"}},
            ]
            result = _extract_fork_signals()
            assert len(result) == 2
            assert result[0]["github"] == "adenhq/hive"

    def test_empty_on_no_forks(self):
        with patch("contrib_engine.scanner.list_user_forks") as mock:
            mock.return_value = []
            result = _extract_fork_signals()
            assert result == []


class TestPRHistory:
    def test_extracts_from_journals(self, tmp_path):
        journal_dir = tmp_path / "contrib--test" / "journal"
        journal_dir.mkdir(parents=True)
        (journal_dir / "session.md").write_text("- **PR:** PR #123\n- **Repo:** owner/repo")
        result = _extract_pr_history(tmp_path)
        assert len(result) == 1
        assert result[0]["workspace"] == "contrib--test"
        assert 123 in result[0]["pr_numbers"]

    def test_empty_on_no_journals(self, tmp_path):
        result = _extract_pr_history(tmp_path)
        assert result == []


class TestDependencySignals:
    def test_extracts_from_pyproject(self, tmp_path):
        proj = tmp_path / "repo"
        proj.mkdir()
        toml = proj / "pyproject.toml"
        toml.write_text('[project]\nname = "test"\ndependencies = [\n    "pydantic>=2.0",\n    "fastapi",\n]\n')
        result = _extract_dependency_signals(tmp_path)
        assert len(result) == 2
        packages = [r["package"] for r in result]
        assert "pydantic" in packages
        assert "fastapi" in packages

    def test_empty_on_no_projects(self, tmp_path):
        result = _extract_dependency_signals(tmp_path)
        assert result == []
```

Create `tests/test_contrib_github_client.py`:

```python
"""Tests for github_client with mocks."""

from unittest.mock import patch

from contrib_engine.github_client import who_starred_my_repos, get_repo_info, search_issues


class TestWhoStarredMyRepos:
    def test_returns_list(self):
        with patch("contrib_engine.github_client._run_gh") as mock:
            mock.return_value = [{"login": "user1", "repo": "4444J99/hive"}]
            result = who_starred_my_repos()
            assert isinstance(result, list)

    def test_returns_empty_on_timeout(self):
        with patch("contrib_engine.github_client._run_gh") as mock:
            mock.return_value = None
            result = who_starred_my_repos()
            assert result == []


class TestSearchIssues:
    def test_returns_empty_on_no_results(self):
        with patch("contrib_engine.github_client._run_gh") as mock:
            mock.return_value = []
            result = search_issues("owner", "repo", ["keyword"])
            assert result == []
```

- [ ] **Step 2: Add new scanner functions to `scanner.py`**

Add `list_user_forks()` to `contrib_engine/github_client.py` (keeps all `_run_gh` calls centralized):

```python
def list_user_forks(username: str = "4444J99") -> list[dict]:
    """List forks owned by username with parent info."""
    result = _run_gh([
        "repo", "list", username,
        "--json", "name,isFork,parent",
        "--limit", "50",
    ])
    if isinstance(result, list):
        return [r for r in result if r.get("isFork")]
    return []
```

Then add new source functions to `contrib_engine/scanner.py`:

```python
from contrib_engine.github_client import who_starred_my_repos, list_user_forks


def _extract_star_signals() -> list[dict]:
    """Extract inbound signals from users who starred our repos."""
    stars = who_starred_my_repos()
    return [{"login": s.get("login", ""), "repo": s.get("repo", "")} for s in stars]


def _extract_fork_signals(username: str = "4444J99") -> list[dict]:
    """Extract outbound signals from repos we've forked."""
    forks = list_user_forks(username)
    result = []
    for fork in forks:
        parent = fork.get("parent", {})
        if parent:
            owner = parent.get("owner", "")
            name = parent.get("name", "")
            if owner and name:
                result.append({"name": fork["name"], "github": f"{owner}/{name}"})
    return result


def _extract_pr_history(organ_iv_dir: Path | None = None) -> list[dict]:
    """Extract target repos from existing contrib workspace journals."""
    base = organ_iv_dir or Path.home() / "Workspace" / "organvm-iv-taxis"
    result = []
    if not base.exists():
        return result
    import re
    pr_pattern = re.compile(r"\*\*PR:\*\*\s*PR\s*#(\d+)")
    for d in base.iterdir():
        if not d.is_dir() or not d.name.startswith("contrib--"):
            continue
        journal_dir = d / "journal"
        if not journal_dir.exists():
            continue
        for md in journal_dir.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            matches = pr_pattern.findall(text)
            if matches:
                result.append({"workspace": d.name, "pr_numbers": [int(m) for m in matches]})
    return result


def _extract_dependency_signals(workspace_dir: Path | None = None) -> list[dict]:
    """Extract external package dependencies from pyproject.toml files.

    Uses tomllib (Python 3.11+) for correct TOML parsing.
    Skips .venv, node_modules, .git directories.
    """
    import tomllib

    base = workspace_dir or Path.home() / "Workspace"
    result = []
    skip_dirs = {".venv", "node_modules", ".git", "__pycache__", ".tox"}
    for toml_path in base.rglob("pyproject.toml"):
        # Skip virtual environments and build directories
        if any(part in skip_dirs for part in toml_path.parts):
            continue
        try:
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
            deps = data.get("project", {}).get("dependencies", [])
            for dep in deps:
                # Extract package name (before any version specifier)
                import re
                match = re.match(r"([a-zA-Z0-9_-]+)", dep)
                if match:
                    result.append({"package": match.group(1), "source": str(toml_path)})
        except Exception:
            continue
    return result
```

- [ ] **Step 3: Run scanner source tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_scanner_sources.py tests/test_contrib_github_client.py -v`
Expected: 8 + 3 = 11 passed

- [ ] **Step 4: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add contrib_engine/scanner.py contrib_engine/github_client.py tests/test_contrib_scanner_sources.py tests/test_contrib_github_client.py
git commit -m "feat: expand scanner with 4 new sources — stars, forks, deps, PR history

list_user_forks() added to github_client.py (keeps _run_gh encapsulated).
Dependency scanner uses tomllib for correct multi-line TOML parsing."
```

---

## Task 10: Cross-Module Integration Tests

**Files:**
- Create: `tests/test_contrib_integration.py`

- [ ] **Step 1: Write integration tests**

Create `tests/test_contrib_integration.py`:

```python
"""Cross-module integration tests."""

from contrib_engine.schemas import (
    Campaign,
    CampaignAction,
    CampaignPhase,
    OutreachIndex,
    TargetRelationship,
    BackflowIndex,
    BackflowItem,
    BackflowType,
)


class TestCampaignMonitorIntegration:
    def test_campaign_next_action_reflects_pr_state(self):
        """Campaign actions should be ordered by workspace PR state."""
        campaign = Campaign(
            started="2026-03-22",
            targets=["contrib--a", "contrib--b"],
            actions=[
                CampaignAction(
                    id="a-unblock", workspace="contrib--a",
                    phase=CampaignPhase.UNBLOCK, action="Fix CLA", priority=0,
                ),
                CampaignAction(
                    id="b-engage", workspace="contrib--b",
                    phase=CampaignPhase.ENGAGE, action="Bump PR", priority=2,
                ),
            ],
        )
        # Unblock should come before engage
        next_actions = campaign.next_actions()
        assert next_actions[0].id == "a-unblock"


class TestCampaignOutreachInteraction:
    def test_outreach_events_inform_campaign_state(self):
        """Outreach events and campaign actions operate on the same workspaces."""
        campaign = Campaign(
            started="2026-03-22",
            actions=[
                CampaignAction(
                    id="join-discord", workspace="contrib--adenhq-hive",
                    phase=CampaignPhase.ENGAGE, action="Join Discord",
                ),
            ],
        )
        outreach = OutreachIndex(
            relationships=[
                TargetRelationship(workspace="contrib--adenhq-hive", target="adenhq/hive"),
            ],
        )
        # Both reference the same workspace
        assert campaign.actions[0].workspace == outreach.relationships[0].workspace
        # After completing the campaign action, outreach should have the event
        # (this is application-level logic, but the data models align)
```

- [ ] **Step 2: Run integration tests**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_integration.py -v`
Expected: 2 passed

- [ ] **Step 3: Run complete test suite**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/test_contrib_*.py -v --tb=short`
Expected: 67+ tests passed

- [ ] **Step 4: Commit**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git add tests/test_contrib_integration.py
git commit -m "test: cross-module integration tests for campaign + outreach"
```

---

## Task 11: Final Verification + Feature Commit

- [ ] **Step 1: Run full test suite one final time**

Run: `cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here && python3 -m pytest tests/ -v --tb=short`
Expected: All tests pass, 0 failures

- [ ] **Step 2: Verify CLI end-to-end**

Run:
```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
python3 -m contrib_engine campaign show
python3 -m contrib_engine campaign next
python3 -m contrib_engine outreach show
python3 -m contrib_engine backflow pending
python3 -m contrib_engine scan --no-github
```
Expected: All commands produce sensible output

- [ ] **Step 3: Verify monitor now parses all 7 workspaces**

Run:
```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
python3 -c "
from contrib_engine.monitor import discover_contributions
contribs = discover_contributions()
for c in contribs:
    print(f'{c.workspace}: {c.target}')
assert all(c.target for c in contribs), 'All workspaces should have targets!'
print(f'All {len(contribs)} workspaces parse correctly.')
"
```
Expected: All 7 workspaces show targets (no empty strings)

- [ ] **Step 4: Git status and final commit if needed**

```bash
cd /Users/4jp/Workspace/organvm-iv-taxis/orchestration-start-here
git status
```

---

## Summary

| Task | Component | Tests Added | Files |
|------|-----------|-------------|-------|
| 1 | Monitor fix | +3 | 2 modified |
| 2 | Schema expansion | 0 (tested via modules) | 1 modified |
| 3 | CLI + entry point | +8 (6 CLI + 2 prefix) | 2 modified, 2 created |
| 4 | Campaign sequencer | +8 | 2 created |
| 5 | Outreach tracker | +6 | 2 created |
| 6 | Backflow pipeline | +6 | 2 created |
| 7 | Full verification | 0 | 0 |
| 8 | Data initialization | 0 | 4 created |
| 9 | Scanner expansion | +11 | 1 modified, 2 created |
| 10 | Integration tests | +2 | 1 created |
| 11 | Final verification | 0 | 0 |
| **Total** | | **+44** (25 existing + 44 = 69) | 9 created, 4 modified |
