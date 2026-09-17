from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install-template.py"


def run_generator(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--output", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_generates_v1_plugin_with_consistent_manifests(tmp_path: Path) -> None:
    result = run_generator(tmp_path, "v1", "Example Plugin", "--plugin-version", "1.2.3")
    assert result.returncode == 0, result.stderr

    destination = tmp_path / "example-plugin"
    assert (destination / "skills/example-workflow/SKILL.md").is_file()
    for relative in (
        "CLAUDE.md",
        "AGENTS.md",
        "GEMINI.md",
        "hooks/index.md",
        "worktrees/README.md",
        "mcp/README.md",
        "rules/index.md",
        "workflows/README.md",
        "agents/README.md",
        "scripts/README.md",
        "iron-laws/index.md",
        "guidelines/index.md",
        "docs/CODEBASE-MAP.md",
    ):
        assert (destination / relative).is_file()
    assert not (destination / "bin").exists()

    for relative in (
        "plugin.json",
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ):
        manifest = json.loads((destination / relative).read_text(encoding="utf-8"))
        assert manifest["name"] == "example-plugin"
        assert manifest["version"] == "1.2.3"


def test_rejects_existing_destination(tmp_path: Path) -> None:
    destination = tmp_path / "example-plugin"
    destination.mkdir()
    result = run_generator(tmp_path, "v1", "example-plugin")
    assert result.returncode == 2
    assert "already exists" in result.stderr


def test_lists_unknown_template_version(tmp_path: Path) -> None:
    result = run_generator(tmp_path, "v9", "example-plugin")
    assert result.returncode == 2
    assert "unknown template version" in result.stderr
