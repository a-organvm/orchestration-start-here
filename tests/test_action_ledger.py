"""Tests for the action ledger — Phase 1: record button."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from action_ledger.schemas import (
    Action,
    ActionIndex,
    ParamAxis,
    ParamRegistry,
    Produced,
    Route,
    RouteKind,
    Sequence,
    SequenceIndex,
)
from action_ledger.ledger import (
    close_sequence,
    load_actions,
    load_param_registry,
    load_sequences,
    record,
    save_actions,
    save_param_registry,
    save_sequences,
    set_sequence_intent,
)


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestAction:
    def test_minimal_action(self):
        a = Action(id="act-S42-0331-001", timestamp="2026-03-31T14:00:00",
                    session="S42", verb="explored", target="fieldwork")
        assert a.id == "act-S42-0331-001"
        assert a.params == {}
        assert a.produced == []
        assert a.routes == []

    def test_action_with_open_params(self):
        a = Action(id="act-S42-0331-001", timestamp="2026-03-31T14:00:00",
                    session="S42", verb="designed", target="action-ledger",
                    params={"abstraction": 0.7, "maturity": 0.3, "domain": "orchestration"})
        assert a.params["abstraction"] == 0.7
        assert a.params["domain"] == "orchestration"

    def test_action_with_routes(self):
        a = Action(id="act-S42-0331-001", timestamp="2026-03-31T14:00:00",
                    session="S42", verb="explored", target="fieldwork",
                    routes=[Route(kind=RouteKind.CONSUMED, target="fieldwork.py")])
        assert len(a.routes) == 1
        assert a.routes[0].effective_amount() == 1.0

    def test_route_defaults(self):
        r_contradict = Route(kind=RouteKind.CONTRADICTS, target="x")
        assert r_contradict.effective_amount() == -1.0

        r_informed = Route(kind=RouteKind.INFORMED_BY, target="y")
        assert r_informed.effective_amount() == 0.6

        r_custom = Route(kind=RouteKind.CONSUMED, target="z", amount=0.3)
        assert r_custom.effective_amount() == 0.3


class TestParamRegistry:
    def test_register_new_axis(self):
        reg = ParamRegistry()
        reg.register("abstraction", 0.7, "2026-03-31T14:00:00")
        assert "abstraction" in reg.axes
        assert reg.axes["abstraction"].frequency == 1
        assert reg.axes["abstraction"].first_seen == "2026-03-31"

    def test_register_increments_frequency(self):
        reg = ParamRegistry()
        reg.register("abstraction", 0.7, "2026-03-31T14:00:00")
        reg.register("abstraction", 0.5, "2026-03-31T15:00:00")
        assert reg.axes["abstraction"].frequency == 2

    def test_register_expands_range(self):
        reg = ParamRegistry()
        reg.register("urgency", 0.5, "2026-03-31T14:00:00")
        reg.register("urgency", 1.5, "2026-03-31T15:00:00")
        assert reg.axes["urgency"].range[1] == 1.5

    def test_register_multiple_axes(self):
        reg = ParamRegistry()
        reg.register("abstraction", 0.7, "2026-03-31T14:00:00")
        reg.register("maturity", 0.3, "2026-03-31T14:00:00")
        reg.register("urgency", 1.0, "2026-03-31T14:00:00")
        assert len(reg.axes) == 3


class TestSequenceIndex:
    def test_active_for_session(self):
        idx = SequenceIndex(sequences=[
            Sequence(id="seq-S42-001", session="S42", closed=True),
            Sequence(id="seq-S42-002", session="S42", closed=False),
        ])
        active = idx.active_for_session("S42")
        assert active is not None
        assert active.id == "seq-S42-002"

    def test_active_for_session_none(self):
        idx = SequenceIndex(sequences=[
            Sequence(id="seq-S42-001", session="S42", closed=True),
        ])
        assert idx.active_for_session("S42") is None

    def test_active_for_session_wrong_session(self):
        idx = SequenceIndex(sequences=[
            Sequence(id="seq-S42-001", session="S42", closed=False),
        ])
        assert idx.active_for_session("S43") is None


# ---------------------------------------------------------------------------
# Ledger tests
# ---------------------------------------------------------------------------


class TestRecord:
    def test_basic_record(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        action = record(
            actions, sequences, registry,
            session="S42", verb="explored", target="fieldwork",
        )

        assert action.id.startswith("act-S42-")
        assert action.verb == "explored"
        assert action.target == "fieldwork"
        assert len(actions.actions) == 1

    def test_record_auto_creates_sequence(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        action = record(
            actions, sequences, registry,
            session="S42", verb="explored", target="fieldwork",
        )

        assert len(sequences.sequences) == 1
        seq = sequences.sequences[0]
        assert seq.session == "S42"
        assert action.id in seq.action_ids
        assert action.sequence_id == seq.id

    def test_record_slots_into_existing_sequence(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        a1 = record(actions, sequences, registry,
                     session="S42", verb="explored", target="fieldwork")
        a2 = record(actions, sequences, registry,
                     session="S42", verb="designed", target="schemas")

        assert len(sequences.sequences) == 1
        assert a1.sequence_id == a2.sequence_id
        assert len(sequences.sequences[0].action_ids) == 2

    def test_record_registers_params(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork",
               params={"abstraction": 0.7, "maturity": 0.3})

        assert "abstraction" in registry.axes
        assert "maturity" in registry.axes
        assert registry.axes["abstraction"].frequency == 1

    def test_record_builds_automation_lanes(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork",
               params={"abstraction": 0.7})
        record(actions, sequences, registry,
               session="S42", verb="designed", target="schemas",
               params={"abstraction": 0.5})
        record(actions, sequences, registry,
               session="S42", verb="built", target="ledger",
               params={"abstraction": 0.3})

        seq = sequences.sequences[0]
        assert "abstraction" in seq.automation
        assert seq.automation["abstraction"] == [0.7, 0.5, 0.3]

    def test_record_with_string_params_skips_automation(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork",
               params={"domain": "orchestration", "abstraction": 0.7})

        seq = sequences.sequences[0]
        assert "abstraction" in seq.automation
        assert "domain" not in seq.automation

    def test_record_with_routes(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        action = record(
            actions, sequences, registry,
            session="S42", verb="explored", target="fieldwork",
            routes=[{"kind": "consumed", "target": "fieldwork.py"}],
        )

        assert len(action.routes) == 1
        assert action.routes[0].kind == RouteKind.CONSUMED
        assert action.routes[0].target == "fieldwork.py"

    def test_record_with_produced(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        action = record(
            actions, sequences, registry,
            session="S42", verb="designed", target="action-ledger",
            produced=[{"type": "insight", "ref": "spectrum model is reusable"}],
        )

        assert len(action.produced) == 1
        assert action.produced[0].type == "insight"

    def test_separate_sessions_get_separate_sequences(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        a1 = record(actions, sequences, registry,
                     session="S42", verb="explored", target="a")
        a2 = record(actions, sequences, registry,
                     session="S43", verb="explored", target="b")

        assert len(sequences.sequences) == 2
        assert a1.sequence_id != a2.sequence_id


class TestCloseSequence:
    def test_close(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork")

        seq = close_sequence(sequences, "S42", outcome="patterns reusable")
        assert seq is not None
        assert seq.closed is True
        assert seq.outcome == "patterns reusable"

    def test_close_creates_new_on_next_record(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork")
        close_sequence(sequences, "S42")
        record(actions, sequences, registry,
               session="S42", verb="built", target="ledger")

        assert len(sequences.sequences) == 2

    def test_close_no_active(self):
        sequences = SequenceIndex()
        assert close_sequence(sequences, "S42") is None


class TestSetSequenceIntent:
    def test_set_intent(self):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork")
        seq = set_sequence_intent(sequences, "S42", "determine reusability")

        assert seq is not None
        assert seq.intent == "determine reusability"


# ---------------------------------------------------------------------------
# Persistence tests
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_actions_round_trip(self, tmp_path: Path):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork",
               params={"abstraction": 0.7},
               routes=[{"kind": "consumed", "target": "fieldwork.py"}],
               produced=[{"type": "insight", "ref": "reusable"}])

        path = tmp_path / "actions.yaml"
        save_actions(actions, path)

        loaded = load_actions(path)
        assert len(loaded.actions) == 1
        a = loaded.actions[0]
        assert a.verb == "explored"
        assert a.params["abstraction"] == 0.7
        assert len(a.routes) == 1
        assert a.routes[0].kind == RouteKind.CONSUMED
        assert len(a.produced) == 1

    def test_sequences_round_trip(self, tmp_path: Path):
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="a",
               params={"abstraction": 0.7})
        record(actions, sequences, registry,
               session="S42", verb="designed", target="b",
               params={"abstraction": 0.5})

        path = tmp_path / "sequences.yaml"
        save_sequences(sequences, path)

        loaded = load_sequences(path)
        assert len(loaded.sequences) == 1
        seq = loaded.sequences[0]
        assert len(seq.action_ids) == 2
        assert seq.automation["abstraction"] == [0.7, 0.5]

    def test_param_registry_round_trip(self, tmp_path: Path):
        registry = ParamRegistry()
        registry.register("abstraction", 0.7, "2026-03-31T14:00:00")
        registry.register("maturity", 0.3, "2026-03-31T14:00:00")
        registry.register("abstraction", 0.5, "2026-03-31T15:00:00")

        path = tmp_path / "param_registry.yaml"
        save_param_registry(registry, path)

        loaded = load_param_registry(path)
        assert len(loaded.axes) == 2
        assert loaded.axes["abstraction"].frequency == 2
        assert loaded.axes["maturity"].frequency == 1

    def test_load_nonexistent_returns_empty(self, tmp_path: Path):
        assert len(load_actions(tmp_path / "nope.yaml").actions) == 0
        assert len(load_sequences(tmp_path / "nope.yaml").sequences) == 0
        assert len(load_param_registry(tmp_path / "nope.yaml").axes) == 0

    def test_yaml_structure(self, tmp_path: Path):
        """Verify the YAML output is human-readable and structured."""
        actions = ActionIndex()
        sequences = SequenceIndex()
        registry = ParamRegistry()

        record(actions, sequences, registry,
               session="S42", verb="explored", target="fieldwork",
               params={"abstraction": 0.7, "maturity": 0.3})

        path = tmp_path / "actions.yaml"
        save_actions(actions, path)

        raw = yaml.safe_load(path.read_text())
        assert "actions" in raw
        assert raw["actions"][0]["verb"] == "explored"
        assert raw["actions"][0]["params"]["abstraction"] == 0.7
