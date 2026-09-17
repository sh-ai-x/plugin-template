#!/usr/bin/env python3
"""Generate a new multi-agent plugin from a versioned template."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


TOKEN_PATTERN = re.compile(r"__([A-Z0-9_]+)__")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value or not NAME_PATTERN.fullmatch(value):
        raise ValueError("plugin name must contain lowercase letters, numbers, and hyphens")
    if len(value) > 64:
        raise ValueError("plugin name must be 64 characters or fewer")
    return value


def display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def github_slug(repository: str, name: str) -> str:
    parsed = urlparse(repository)
    if parsed.hostname in {"github.com", "www.github.com"}:
        path = parsed.path.strip("/")
        if path.endswith(".git"):
            path = path[:-4]
        if path.count("/") == 1:
            return path
    return f"example/{name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new Claude Code + Codex + agy plugin from a versioned template."
    )
    parser.add_argument("template_version", help="Template directory name, for example v1")
    parser.add_argument("plugin_name", help="New plugin name; normalized to lowercase kebab-case")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Parent directory for the generated plugin (default: current directory)",
    )
    parser.add_argument(
        "--plugin-version",
        default="0.1.0",
        help="Initial plugin semantic version (default: 0.1.0)",
    )
    parser.add_argument("--description", default=None, help="Plugin description")
    parser.add_argument("--display-name", default=None, help="Human-readable plugin name")
    parser.add_argument("--author-name", default="Plugin Author", help="Author display name")
    parser.add_argument(
        "--author-url", default="https://github.com/example", help="Author profile URL"
    )
    parser.add_argument(
        "--repository",
        default=None,
        help="Repository URL; defaults to https://github.com/example/<plugin-name>",
    )
    parser.add_argument("--homepage", default=None, help="Plugin homepage URL")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the destination without writing files"
    )
    return parser.parse_args()


def copy_template(source: Path, destination: Path, replacements: dict[str, str]) -> None:
    for source_path in sorted(source.rglob("*")):
        relative = source_path.relative_to(source)
        if relative.name == "template.json":
            continue
        target_path = destination / relative
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        raw = source_path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            target_path.write_bytes(raw)
            continue
        for token, replacement in replacements.items():
            text = text.replace(token, replacement)
        unresolved = sorted(set(TOKEN_PATTERN.findall(text)))
        if unresolved:
            raise ValueError(
                f"unresolved template tokens in {relative}: "
                + ", ".join(f"__{token}__" for token in unresolved)
            )
        target_path.write_text(text, encoding="utf-8")
        if source_path.stat().st_mode & 0o111:
            target_path.chmod(target_path.stat().st_mode | 0o111)


def validate_generated(destination: Path, plugin_name: str, plugin_version: str) -> None:
    for manifest_path in (
        destination / "plugin.json",
        destination / ".claude-plugin" / "plugin.json",
        destination / ".codex-plugin" / "plugin.json",
    ):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if data.get("name") != plugin_name:
            raise ValueError(f"manifest name mismatch: {manifest_path}")
        if data.get("version") != plugin_version:
            raise ValueError(f"manifest version mismatch: {manifest_path}")
    for required in (
        destination / "skills" / "example-workflow" / "SKILL.md",
        destination / "hooks" / "hooks.json",
        destination / ".mcp.json",
        destination / "mcp.json",
        destination / ".agents" / "plugins.json",
        destination / ".agents" / "skills.json",
    ):
        if not required.exists():
            raise ValueError(f"generated template is missing {required.relative_to(destination)}")


def main() -> int:
    args = parse_args()
    try:
        plugin_name = normalize_name(args.plugin_name)
        if not SEMVER_PATTERN.fullmatch(args.plugin_version):
            raise ValueError("--plugin-version must be a semantic version such as 0.1.0")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    template_root = repo_root / "templates" / args.template_version
    if not template_root.is_dir():
        available = sorted(path.name for path in (repo_root / "templates").iterdir() if path.is_dir())
        print(
            f"error: unknown template version {args.template_version!r}; "
            f"available: {', '.join(available) or '(none)'}",
            file=sys.stderr,
        )
        return 2

    repository = args.repository or f"https://github.com/example/{plugin_name}"
    homepage = args.homepage or repository
    destination = args.output.expanduser().resolve() / plugin_name
    if destination.exists():
        print(f"error: destination already exists: {destination}", file=sys.stderr)
        return 2
    if args.dry_run:
        print(destination)
        return 0

    values = {
        "__PLUGIN_NAME__": plugin_name,
        "__PLUGIN_VERSION__": args.plugin_version,
        "__PLUGIN_DISPLAY_NAME__": args.display_name or display_name(plugin_name),
        "__PLUGIN_DESCRIPTION__": args.description
        or "A cross-agent plugin built from the Claude Code + Codex template.",
        "__AUTHOR_NAME__": args.author_name,
        "__AUTHOR_URL__": args.author_url,
        "__REPOSITORY__": repository,
        "__HOMEPAGE__": homepage,
        "__MARKETPLACE_NAME__": f"{plugin_name}-marketplace",
        "__GITHUB_REPO__": github_slug(repository, plugin_name),
        "__YEAR__": str(datetime.now(timezone.utc).year),
    }

    try:
        copy_template(template_root, destination, values)
        validate_generated(destination, plugin_name, args.plugin_version)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if destination.exists():
            shutil.rmtree(destination)
        print(f"error: generation failed: {exc}", file=sys.stderr)
        return 1

    print(f"created {destination}")
    print(f"template: {args.template_version}")
    print(f"plugin: {plugin_name}@{args.plugin_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
