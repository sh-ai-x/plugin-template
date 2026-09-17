#!/usr/bin/env bash
set -euo pipefail

# Read the event so the hook remains safe for both runtimes. Keep diagnostics on stderr.
event_json="$(cat || true)"
if [[ "${PLUGIN_TEMPLATE_DEBUG:-0}" == "1" ]]; then
  printf '%s\n' "__PLUGIN_NAME__: SessionStart received" >&2
  printf '%s\n' "$event_json" >&2
fi
