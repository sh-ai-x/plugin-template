#!/usr/bin/env bash
set -euo pipefail

# Install __PLUGIN_NAME__ for Google Antigravity (agy).
#
#   bin/install-agy.sh --global
#   bin/install-agy.sh /path/to/workspace
#   bin/install-agy.sh --check
#
# Global mode creates symlinks in both known agy plugin roots. Workspace mode writes
# .agents/plugins.json and .agents/skills.json while preserving unrelated entries.

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="__PLUGIN_NAME__"
GLOBAL_ROOT="${HOME}/.gemini/config/plugins/${PLUGIN_NAME}"
CLI_ROOT="${HOME}/.gemini/antigravity-cli/plugins/${PLUGIN_NAME}"

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

usage() {
  sed -n '2,11p' "$0" | sed 's/^# \?//'
}

CHECK=0
GLOBAL=0
DRY_RUN=0
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK=1; shift ;;
    --global) GLOBAL=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) die "unknown option: $1" ;;
    *) [[ -z "$TARGET" ]] || die "unexpected argument: $1"; TARGET="$1"; shift ;;
  esac
done

if [[ "$CHECK" == "1" ]]; then
  [[ -f "${PLUGIN_ROOT}/plugin.json" ]] || die "missing plugin.json"
  [[ -d "${PLUGIN_ROOT}/skills" ]] || die "missing skills directory"
  printf 'OK: %s is structured for agy\n' "$PLUGIN_NAME"
  [[ -L "$GLOBAL_ROOT" || -d "$GLOBAL_ROOT" ]] && printf 'global: installed\n' || printf 'global: not installed\n'
  exit 0
fi

if [[ "$GLOBAL" == "1" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] link %s -> %s\n' "$GLOBAL_ROOT" "$PLUGIN_ROOT"
    printf '[dry-run] link %s -> %s\n' "$CLI_ROOT" "$PLUGIN_ROOT"
    exit 0
  fi
  mkdir -p "$(dirname "$GLOBAL_ROOT")" "$(dirname "$CLI_ROOT")"
  ln -sfn "$PLUGIN_ROOT" "$GLOBAL_ROOT"
  ln -sfn "$PLUGIN_ROOT" "$CLI_ROOT"
  printf 'installed %s globally for agy\n' "$PLUGIN_NAME"
  exit 0
fi

if [[ -n "$TARGET" ]]; then
  TARGET="$(cd "$TARGET" && pwd)"
  AGENTS_DIR="${TARGET}/.agents"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] register %s in %s\n' "$PLUGIN_ROOT" "$AGENTS_DIR"
    exit 0
  fi
  mkdir -p "$AGENTS_DIR"
  AGENTS_DIR="$AGENTS_DIR" PLUGIN_ROOT="$PLUGIN_ROOT" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["AGENTS_DIR"])
plugin_root = os.environ["PLUGIN_ROOT"]

def upsert(path: Path, value: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"entries": []}
    entries = data.setdefault("entries", [])
    if not any(entry.get("path") == value for entry in entries):
        entries.append({"path": value})
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

upsert(root / "plugins.json", plugin_root)
upsert(root / "skills.json", str(Path(plugin_root) / "skills"))
PY
  printf 'configured %s for agy in %s\n' "$PLUGIN_NAME" "$TARGET"
  exit 0
fi

usage
exit 1
