# Hooks index

`hooks/hooks.json` is the shared lifecycle configuration for Claude Code and Codex. The command
paths resolve from the installed plugin root and call the scripts in `hooks/scripts/`.

Rules for hook changes:

1. Keep hooks deterministic and fast.
2. Document whether a hook is fail-open or fail-closed.
3. Do not write persistent state into the installed plugin cache.
4. Use host-specific matchers only in the manifest or hook configuration when event behavior differs.

Review and trust bundled hooks before enabling them in Codex.
