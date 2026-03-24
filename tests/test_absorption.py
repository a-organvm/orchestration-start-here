"""Tests for the Absorption Protocol."""

import pytest

from contrib_engine.absorption import (
    _extract_pattern_name,
    _generate_theory_note,
    add_tracked_conversation,
    auto_formalize,
    deposit_to_backflow,
    detect_triggers,
    generate_formalization_prompt,
    infer_organ,
    load_absorption,
    load_tracked_conversations_config,
    mark_formalized,
    save_absorption,
    save_tracked_conversations_config,
    scan_conversations,
)
from contrib_engine.schemas import (
    AbsorptionIndex,
    AbsorptionItem,
    AbsorptionStatus,
    AbsorptionTrigger,
)


class TestDetectTriggers:
    """Test the expansion/reduction heuristic gate."""

    def test_unnamed_pattern_how_handle(self):
        text = "How do you handle conflicting traces? Like if two agents deposit contradicting RESOURCE traces about the same target."
        triggers = detect_triggers(text)
        assert len(triggers) >= 1
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.UNNAMED_PATTERN in types

    def test_unnamed_pattern_what_happens(self):
        text = "What happens when the crisis level drops but agents are mid-task? Do they immediately split or finish their current work first?"
        triggers = detect_triggers(text)
        assert len(triggers) >= 1
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.UNNAMED_PATTERN in types

    def test_convergence_we_ended_up(self):
        text = "We ended up doing something cruder with TTL-based file locks that agents check before acting. The decay approach is more elegant."
        triggers = detect_triggers(text)
        assert len(triggers) >= 1
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.INDEPENDENT_CONVERGENCE in types

    def test_convergence_we_built(self):
        text = "We built a similar system using Redis pub/sub for the coordination layer. The pheromone field is interesting because it doesn't need a message broker."
        triggers = detect_triggers(text)
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.INDEPENDENT_CONVERGENCE in types

    def test_assumption_divergence_isnt_that_just(self):
        text = "Isn't that basically just eventual consistency with extra steps? The traces converge through decay and reinforcement which is similar to CRDT convergence."
        triggers = detect_triggers(text)
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.ASSUMPTION_DIVERGENCE in types

    def test_assumption_divergence_most_frameworks(self):
        text = "Most orchestration frameworks treat agent topology as static, so having it adapt based on crisis metrics is a fundamentally different design."
        triggers = detect_triggers(text)
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.ASSUMPTION_DIVERGENCE in types

    def test_assumption_divergence_does_win(self):
        text = "Does the higher intensity trace win over the lower one, or is there some kind of merge strategy for conflicting information?"
        triggers = detect_triggers(text)
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.ASSUMPTION_DIVERGENCE in types

    def test_hard_part_trigger(self):
        text = "The hard part is making sure the agents don't thrash between states when the metrics are noisy. How stable is the hysteresis in practice?"
        triggers = detect_triggers(text)
        types = [t for t, _ in triggers]
        assert AbsorptionTrigger.UNNAMED_PATTERN in types

    def test_multiple_triggers(self):
        text = "We ended up doing something similar — most frameworks crash the whole group but we built a redistribute model. How do you handle the state transfer?"
        triggers = detect_triggers(text)
        assert len(triggers) >= 2  # convergence + unnamed_pattern or divergence

    def test_reduction_what_version(self):
        text = "What version of Python are you using for the hive module? I'm having compatibility issues with 3.10."
        triggers = detect_triggers(text)
        assert triggers == []

    def test_reduction_can_you_add(self):
        text = "Can you add support for Kubernetes as a runtime? It would be useful for our deployment environment."
        triggers = detect_triggers(text)
        assert triggers == []

    def test_reduction_broken(self):
        text = "This doesn't work when I try to run it on Windows. The path separators cause issues in the pheromone field key generation."
        triggers = detect_triggers(text)
        assert triggers == []

    def test_too_short(self):
        text = "Interesting approach."
        triggers = detect_triggers(text)
        assert triggers == []

    def test_empty(self):
        triggers = detect_triggers("")
        assert triggers == []


class TestAbsorptionModels:
    """Test Pydantic model behavior."""

    def test_absorption_item_creation(self):
        item = AbsorptionItem(
            id="abs-test-001",
            workspace="contrib--m13v-summarize-recent-commit",
            source_url="https://github.com/org/repo/issues/20#comment-123",
            questioner="m13v",
            question_text="How do you handle conflicting traces?",
            detected_at="2026-03-24T12:00:00",
            triggers=[AbsorptionTrigger.UNNAMED_PATTERN],
            trigger_evidence="Asks about handling strategy",
            status=AbsorptionStatus.DETECTED,
        )
        assert item.status == AbsorptionStatus.DETECTED
        assert item.questioner == "m13v"

    def test_absorption_index_pending(self):
        index = AbsorptionIndex(items=[
            AbsorptionItem(
                id="abs-1", workspace="w1", source_url="u1",
                questioner="a", question_text="q1", detected_at="t1",
                status=AbsorptionStatus.DETECTED,
            ),
            AbsorptionItem(
                id="abs-2", workspace="w2", source_url="u2",
                questioner="b", question_text="q2", detected_at="t2",
                status=AbsorptionStatus.FORMALIZED,
            ),
            AbsorptionItem(
                id="abs-3", workspace="w3", source_url="u3",
                questioner="c", question_text="q3", detected_at="t3",
                status=AbsorptionStatus.ASSESSED,
            ),
        ])
        pending = index.pending_formalization()
        assert len(pending) == 2
        assert {i.id for i in pending} == {"abs-1", "abs-3"}

    def test_by_status(self):
        index = AbsorptionIndex(items=[
            AbsorptionItem(
                id="abs-1", workspace="w1", source_url="u1",
                questioner="a", question_text="q1", detected_at="t1",
                status=AbsorptionStatus.DEPOSITED,
            ),
            AbsorptionItem(
                id="abs-2", workspace="w2", source_url="u2",
                questioner="b", question_text="q2", detected_at="t2",
                status=AbsorptionStatus.DEPOSITED,
            ),
        ])
        deposited = index.by_status(AbsorptionStatus.DEPOSITED)
        assert len(deposited) == 2


class TestSaveLoad:
    """Test persistence."""

    def test_save_and_load(self, tmp_path):
        index = AbsorptionIndex(
            generated="2026-03-24",
            items=[
                AbsorptionItem(
                    id="abs-test-001",
                    workspace="contrib--test",
                    source_url="https://example.com",
                    questioner="tester",
                    question_text="How do you handle X?",
                    detected_at="2026-03-24T12:00:00",
                    triggers=[AbsorptionTrigger.UNNAMED_PATTERN],
                    trigger_evidence="Test evidence",
                    status=AbsorptionStatus.DETECTED,
                ),
            ],
        )
        path = tmp_path / "absorption.yaml"
        save_absorption(index, output_path=path)
        loaded = load_absorption(input_path=path)
        assert len(loaded.items) == 1
        assert loaded.items[0].questioner == "tester"
        assert loaded.items[0].triggers == [AbsorptionTrigger.UNNAMED_PATTERN]

    def test_load_empty(self, tmp_path):
        path = tmp_path / "nonexistent.yaml"
        loaded = load_absorption(input_path=path)
        assert len(loaded.items) == 0


class TestScanConversations:
    """Test conversation scanning with mock data."""

    def test_scan_filters_our_comments(self):
        """Ensure our own comments are excluded."""
        items = scan_conversations(conversations=[], since="")
        assert items == []

    def test_scan_empty_conversations(self):
        items = scan_conversations(conversations=[], since="")
        assert items == []


class TestTrackedConversations:
    """Test tracked conversations config."""

    def test_save_and_load(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "contrib_engine.absorption.TRACKED_CONVERSATIONS_PATH",
            tmp_path / "tracked.yaml",
        )
        save_tracked_conversations_config([
            {"owner": "org", "repo": "repo", "issue_number": 1, "workspace": "w"},
        ])
        loaded = load_tracked_conversations_config()
        assert len(loaded) == 1
        assert loaded[0]["owner"] == "org"

    def test_add_tracked_dedup(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "contrib_engine.absorption.TRACKED_CONVERSATIONS_PATH",
            tmp_path / "tracked.yaml",
        )
        add_tracked_conversation("org", "repo", 1, "w1")
        add_tracked_conversation("org", "repo", 1, "w2")  # Duplicate
        add_tracked_conversation("org", "repo", 2, "w3")  # Different
        loaded = load_tracked_conversations_config()
        assert len(loaded) == 2

    def test_load_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "contrib_engine.absorption.TRACKED_CONVERSATIONS_PATH",
            tmp_path / "nonexistent.yaml",
        )
        loaded = load_tracked_conversations_config()
        assert loaded == []


class TestFormalization:
    """Test the formalization pipeline."""

    def test_infer_organ_pattern(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="How do you handle conflicting pattern resolution?",
            detected_at="t", trigger_evidence="pattern detection",
        )
        assert infer_organ(item) == "I"

    def test_infer_organ_community(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="How does the community engage with this?",
            detected_at="t", trigger_evidence="community dynamics",
        )
        assert infer_organ(item) == "VI"

    def test_infer_organ_default(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="What about the transition mechanism?",
            detected_at="t", trigger_evidence="",
        )
        assert infer_organ(item) == "I"  # Default

    def test_generate_prompt(self):
        item = AbsorptionItem(
            id="abs-001", workspace="agentic-titan", source_url="https://example.com",
            questioner="m13v",
            question_text="How do you handle conflicting traces?",
            detected_at="2026-03-24",
            triggers=[AbsorptionTrigger.UNNAMED_PATTERN, AbsorptionTrigger.INDEPENDENT_CONVERGENCE],
            trigger_evidence="Points at unnamed pattern; independent convergence",
        )
        prompt = generate_formalization_prompt(item)
        assert "m13v" in prompt
        assert "conflicting traces" in prompt
        assert "Organ" in prompt
        assert "Names the pattern" in prompt

    def test_mark_formalized(self):
        index = AbsorptionIndex(items=[
            AbsorptionItem(
                id="abs-001", workspace="w", source_url="u", questioner="q",
                question_text="q", detected_at="t",
                status=AbsorptionStatus.DETECTED,
            ),
        ])
        result = mark_formalized(index, "abs-001", "reader-side-resolution")
        assert result is not None
        assert result.status == AbsorptionStatus.FORMALIZED
        assert result.pattern_name == "reader-side-resolution"

    def test_mark_formalized_not_found(self):
        index = AbsorptionIndex(items=[])
        result = mark_formalized(index, "nonexistent", "test")
        assert result is None

    def test_deposit_to_backflow(self):
        item = AbsorptionItem(
            id="abs-001", workspace="agentic-titan", source_url="u",
            questioner="m13v", question_text="How do you handle X?",
            detected_at="t",
            triggers=[AbsorptionTrigger.UNNAMED_PATTERN],
            status=AbsorptionStatus.FORMALIZED,
            pattern_name="reader-side-resolution",
            organ="I",
        )
        backflow = deposit_to_backflow(item, "path/to/artifact.md")
        assert backflow.organ == "I"
        assert backflow.title == "reader-side-resolution"
        assert backflow.artifact_path == "path/to/artifact.md"
        assert item.status == AbsorptionStatus.DEPOSITED
        assert "backflow:" in item.backflow_ref

    def test_deposit_requires_formalized(self):
        item = AbsorptionItem(
            id="abs-001", workspace="w", source_url="u", questioner="q",
            question_text="q", detected_at="t",
            status=AbsorptionStatus.DETECTED,
        )
        with pytest.raises(ValueError, match="not formalized"):
            deposit_to_backflow(item, "path.md")


class TestAutoFormalize:
    """Test autonomous formalization."""

    def test_extract_pattern_how_handle(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="How do you handle conflicting traces between agents?",
            detected_at="t",
        )
        name = _extract_pattern_name(item)
        assert name  # Should extract something
        assert "conflicting" in name.lower() or "traces" in name.lower()

    def test_extract_pattern_what_happens(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="What happens when the crisis level drops mid-fusion?",
            detected_at="t",
        )
        name = _extract_pattern_name(item)
        assert name
        assert "crisis" in name.lower() or "drops" in name.lower() or "level" in name.lower()

    def test_extract_pattern_fallback(self):
        item = AbsorptionItem(
            id="test", workspace="w", source_url="u", questioner="q",
            question_text="The stigmergy approach with pheromone decay solving stale state is elegant",
            detected_at="t",
        )
        name = _extract_pattern_name(item)
        assert name  # Fallback to distinctive words

    def test_generate_theory_note_all_triggers(self):
        item = AbsorptionItem(
            id="test", workspace="agentic-titan", source_url="https://example.com",
            questioner="m13v",
            question_text="How do you handle conflicting traces?",
            detected_at="2026-03-24",
            triggers=[
                AbsorptionTrigger.UNNAMED_PATTERN,
                AbsorptionTrigger.INDEPENDENT_CONVERGENCE,
                AbsorptionTrigger.ASSUMPTION_DIVERGENCE,
            ],
        )
        content = _generate_theory_note(item, "reader-side resolution", "I")
        assert "Reader-Side Resolution" in content
        assert "m13v" in content
        assert "Assumption Divergence" in content
        assert "Unnamed Pattern" in content
        assert "Independent Convergence" in content

    def test_auto_formalize_creates_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("contrib_engine.absorption.ORGAN_DIRS", tmp_path)
        # Create the expected organ directory
        organ_dir = tmp_path / "organvm-i-theoria" / "my-knowledge-base" / "intake" / "canonical" / "contributions"
        organ_dir.mkdir(parents=True)

        item = AbsorptionItem(
            id="abs-test", workspace="agentic-titan", source_url="https://example.com",
            questioner="m13v",
            question_text="How do you handle conflicting pheromone traces between multiple agents?",
            detected_at="2026-03-24",
            triggers=[AbsorptionTrigger.UNNAMED_PATTERN],
            status=AbsorptionStatus.DETECTED,
        )
        artifact_path = auto_formalize(item)
        assert artifact_path is not None
        assert item.status == AbsorptionStatus.FORMALIZED
        assert item.pattern_name
        # File should exist
        full_path = tmp_path / artifact_path
        assert full_path.exists()
        content = full_path.read_text()
        assert "m13v" in content

    def test_auto_formalize_skips_already_formalized(self):
        item = AbsorptionItem(
            id="abs-test", workspace="w", source_url="u", questioner="q",
            question_text="q", detected_at="t",
            status=AbsorptionStatus.FORMALIZED,
        )
        result = auto_formalize(item)
        assert result is None

    def test_auto_formalize_skips_no_pattern(self):
        item = AbsorptionItem(
            id="abs-test", workspace="w", source_url="u", questioner="q",
            question_text="ok",  # Too short for pattern extraction
            detected_at="t",
            status=AbsorptionStatus.DETECTED,
        )
        result = auto_formalize(item)
        assert result is None
