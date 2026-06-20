"""Tests for scripts.lib.progress project evaluation and reporting."""

from __future__ import annotations

import datetime

from scripts.lib import progress


def _write(path, text="x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _standard_code_repo(tmp_path):
    repo = tmp_path / "code-repo"
    repo.mkdir()
    _write(
        repo / "seed.yaml",
        "schema_version: '1.0'\norgan: ORGAN-IV\nrepo: code-repo\n",
    )
    _write(repo / "README.md", " ".join(["word"] * 550))
    _write(repo / ".gitignore", ".venv\n")
    _write(repo / "CHANGELOG.md", "# Changelog\n")
    _write(repo / "pyproject.toml", "[project]\nname = 'code-repo'\n")
    _write(repo / ".github" / "workflows" / "ci.yml", "name: CI\n")
    _write(repo / "src" / "app.py", "def run():\n    return 'ok'\n")
    _write(repo / "tests" / "test_app.py", "def test_ok():\n    assert True\n")
    return repo


def _standard_code_entry(**overrides):
    entry = {
        "name": "code-repo",
        "org": "organvm-iv-taxis",
        "tier": "standard",
        "documentation_status": "DEPLOYED",
        "ci_workflow": "ci.yml",
        "implementation_status": "PROTOTYPE",
        "promotion_status": "CANDIDATE",
        "deployment_url": "https://example.test/code-repo",
        "last_validated": (datetime.date.today() - datetime.timedelta(days=10)).isoformat(),
        "description": "A standard code repository",
    }
    entry.update(overrides)
    return entry


def test_detect_profile_uses_registry_and_filesystem_signals(tmp_path):
    docs_repo = tmp_path / "governance-docs"
    docs_repo.mkdir()
    _write(docs_repo / "README.md", "# Governance\n")

    code_repo = tmp_path / "governance-code"
    code_repo.mkdir()
    _write(code_repo / "src" / "policy.py", "POLICY = True\n")

    assert progress.detect_profile({"tier": "archive"}) is progress.Profile.ARCHIVED
    assert progress.detect_profile({"tier": "stub"}) is progress.Profile.STUB
    assert progress.detect_profile({"tier": "infrastructure"}) is progress.Profile.INFRASTRUCTURE
    assert (
        progress.detect_profile({"name": "governance-policy"}, docs_repo)
        is progress.Profile.GOVERNANCE
    )
    assert (
        progress.detect_profile({"name": "governance-policy"}, code_repo)
        is progress.Profile.CODE_FULL
    )
    assert (
        progress.detect_profile({"implementation_status": "DESIGN_ONLY"})
        is progress.Profile.DOCUMENTATION
    )


def test_detect_languages_skips_generated_and_dependency_directories(tmp_path):
    repo = tmp_path / "repo"
    _write(repo / "src" / "app.py", "print('ok')\n")
    _write(repo / "src" / "model.py", "VALUE = 1\n")
    _write(repo / "README.md", "# Repo\n")
    _write(repo / ".github" / "workflows" / "ci.yml", "name: CI\n")
    _write(repo / "node_modules" / "package" / "ignored.js", "ignored\n")
    _write(repo / ".venv" / "ignored.py", "ignored\n")

    languages = progress.detect_languages(repo)

    assert languages["Python"] == 2
    assert languages["Markdown"] == 1
    assert languages["YAML"] == 1
    assert "JavaScript" not in languages
    assert progress.primary_language(languages) == "Python"
    assert progress.primary_language({"Markdown": 3, "YAML": 1}) == "none"


def test_probe_scaffold_and_security_signals(tmp_path):
    repo = tmp_path / "repo"
    _write(repo / "README.md", "short readme\n")
    _write(repo / ".gitignore", ".venv\n")
    _write(repo / "LICENSE", "MIT\n")
    _write(repo / "CHANGELOG.md", "# Changelog\n")
    _write(repo / "SECURITY.md", "# Security\n")
    _write(repo / "pyproject.toml", "[project]\nname = 'repo'\n")
    _write(repo / ".env", "TOKEN=secret\n")

    scaffold = progress.probe_scaffold(repo)
    security = progress.probe_security(repo)

    assert scaffold.has_readme is True
    assert scaffold.has_gitignore is True
    assert scaffold.has_license is True
    assert scaffold.has_pkg_config is True
    assert scaffold.pkg_config_type == "pyproject.toml"
    assert scaffold.scaffold_score >= 5
    assert security.has_security_policy is True
    assert security.clean is False
    assert security.to_dict()["exposed_secrets"] == [".env"]


def test_evaluate_project_scores_code_repo_and_recommends_next_promotion(tmp_path):
    repo = _standard_code_repo(tmp_path)

    evaluated = progress.evaluate_project(_standard_code_entry(), "ORGAN-IV", repo)
    gates = {checkpoint.name: checkpoint for checkpoint in evaluated.checkpoints}

    assert evaluated.profile is progress.Profile.CODE_FULL
    assert evaluated.primary_lang == "Python"
    assert evaluated.score == 8
    assert evaluated.total == 10
    assert evaluated.pct == 80
    assert evaluated.promotion_ready is True
    assert evaluated.next_promotion == "PUBLIC_PROCESS"
    assert evaluated.blockers == [
        "GRAD: promotion_status=CANDIDATE (need GRADUATED)",
        "OMEGA: blocked by: GRAD; platinum_status=false",
    ]
    for gate_name in ("SEED", "SCAFFOLD", "CI", "TESTS", "DOCS", "PROTO", "CAND", "DEPLOY"):
        assert gates[gate_name].passed is True
        assert gates[gate_name].applicable is True
    assert gates["GRAD"].passed is False
    assert gates["OMEGA"].next_action == "Clear remaining gate failures first: GRAD"
    assert evaluated.to_dict()["promotion_ready"] is True


def test_evaluate_project_marks_documentation_gates_not_applicable(tmp_path):
    repo = tmp_path / "docs-repo"
    repo.mkdir()
    _write(repo / "README.md", " ".join(["docs"] * 700))
    _write(repo / ".gitignore", ".venv\n")
    _write(repo / "CHANGELOG.md", "# Changelog\n")

    evaluated = progress.evaluate_project(
        {
            "name": "docs-repo",
            "tier": "standard",
            "implementation_status": "DESIGN_ONLY",
            "documentation_status": "DEPLOYED",
            "promotion_status": "LOCAL",
        },
        "ORGAN-I",
        repo,
    )
    gates = {checkpoint.name: checkpoint for checkpoint in evaluated.checkpoints}

    assert evaluated.profile is progress.Profile.DOCUMENTATION
    assert gates["TESTS"].applicable is False
    assert gates["DEPLOY"].applicable is False
    assert gates["DOCS"].passed is True
    assert gates["PROTO"].passed is False
    assert "TESTS" not in evaluated.blockers[0]


def test_evaluate_all_resolves_workspace_paths_and_computes_summary(tmp_path):
    workspace = tmp_path / "workspace"
    repo = workspace / "organvm-iv-taxis" / "code-repo"
    repo.mkdir(parents=True)
    for item in _standard_code_repo(tmp_path).iterdir():
        target = repo / item.name
        if item.is_dir():
            target.mkdir(exist_ok=True)
            for child in item.rglob("*"):
                if child.is_file():
                    _write(target / child.relative_to(item), child.read_text())
        else:
            _write(target, item.read_text())

    registry = {
        "organs": {
            "ORGAN-IV": {"repositories": [_standard_code_entry()]},
            "ORGAN-I": {
                "repositories": [
                    {
                        "name": "remote-only",
                        "org": "organvm-i-theoria",
                        "tier": "stub",
                        "documentation_status": "",
                        "promotion_status": "LOCAL",
                    }
                ]
            },
        }
    }

    projects = progress.evaluate_all(registry, workspace)
    summary = progress.compute_system_summary(projects)
    test_stats = {gate.name: gate for gate in progress.compute_gate_stats(projects)}

    assert [project.repo for project in projects] == ["code-repo", "remote-only"]
    assert projects[0].primary_lang == "Python"
    assert projects[1].profile is progress.Profile.STUB
    assert summary.total_repos == 2
    assert summary.profile_counts["code-full"] == 1
    assert summary.profile_counts["stub"] == 1
    assert summary.language_counts == {"Python": 1}
    assert summary.promotion_ready_count == 1
    assert test_stats["TESTS"].total_passed == 1
    assert test_stats["TESTS"].total_na == 1


def test_snapshot_delta_tracks_improvements_regressions_added_and_removed():
    old_snapshot = {
        "timestamp": "2026-06-01T00:00:00",
        "summary": {"sys_pct": 50},
        "projects": [
            {
                "repo": "alpha",
                "organ": "ORGAN-IV",
                "score": 1,
                "total": 2,
                "pct": 50,
                "profile": "code-full",
                "checkpoints": [
                    {"name": "SEED", "passed": True, "applicable": True},
                    {"name": "CI", "passed": False, "applicable": True},
                ],
            },
            {
                "repo": "beta",
                "organ": "ORGAN-I",
                "score": 2,
                "total": 2,
                "pct": 100,
                "profile": "code-full",
                "checkpoints": [
                    {"name": "SEED", "passed": True, "applicable": True},
                    {"name": "TESTS", "passed": True, "applicable": True},
                ],
            },
            {"repo": "removed", "score": 1, "total": 1, "pct": 100, "checkpoints": []},
        ],
    }
    new_snapshot = {
        "timestamp": "2026-06-20T00:00:00",
        "summary": {"sys_pct": 60},
        "projects": [
            {
                "repo": "alpha",
                "organ": "ORGAN-IV",
                "score": 2,
                "total": 2,
                "pct": 100,
                "profile": "code-full",
                "checkpoints": [
                    {"name": "SEED", "passed": True, "applicable": True},
                    {"name": "CI", "passed": True, "applicable": True},
                ],
            },
            {
                "repo": "beta",
                "organ": "ORGAN-I",
                "score": 1,
                "total": 2,
                "pct": 50,
                "profile": "documentation",
                "checkpoints": [
                    {"name": "SEED", "passed": True, "applicable": True},
                    {"name": "TESTS", "passed": False, "applicable": True},
                ],
            },
            {"repo": "added", "score": 0, "total": 1, "pct": 0, "checkpoints": []},
        ],
    }

    delta = progress.compute_delta(old_snapshot, new_snapshot)

    assert delta.delta_sys_pct == 10
    assert delta.repos_added == ["added"]
    assert delta.repos_removed == ["removed"]
    assert [repo.repo for repo in delta.repos_improved] == ["alpha"]
    assert delta.repos_improved[0].gates_gained == ["CI"]
    assert [repo.repo for repo in delta.repos_regressed] == ["beta"]
    assert delta.repos_regressed[0].gates_lost == ["TESTS"]
    assert delta.repos_regressed[0].profile_changed is True
    assert delta.to_dict()["repos_improved"] == 1


def test_snapshot_persistence_and_exports_round_trip(tmp_path):
    repo = _standard_code_repo(tmp_path)
    evaluated = progress.evaluate_project(_standard_code_entry(), "ORGAN-IV", repo)
    summary = progress.compute_system_summary([evaluated])

    snapshot_path = progress.save_snapshot(
        [evaluated],
        summary,
        tmp_path / "snapshots",
        label="test",
    )
    loaded = progress.load_snapshot(snapshot_path)
    snapshots = progress.list_snapshots(tmp_path / "snapshots")

    assert loaded["label"] == "test"
    assert loaded["summary"]["total_repos"] == 1
    assert loaded["projects"][0]["repo"] == "code-repo"
    assert snapshots == [snapshot_path]
    assert "code-repo,ORGAN-IV,standard,code-full,8,10,80" in progress.export_csv([evaluated])
    assert "| code-repo | ORGAN-IV | code-full | 8/10 | 80%" in progress.export_markdown(
        [evaluated], summary
    )
    assert "code-repo" in progress.render_next_actions([evaluated], limit=2)
