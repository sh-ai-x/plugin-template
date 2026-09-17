# Hooks

See [`index.md`](index.md) for the shared hook contract.

`hooks/hooks.json` is intentionally shared by Claude Code and Codex. The event schema is common,
while the hook environment is adapted by the host:

- Claude Code provides `CLAUDE_PLUGIN_ROOT`.
- Codex provides `PLUGIN_ROOT` and also exposes `CLAUDE_PLUGIN_ROOT` for compatibility.

The command uses `${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT}}`, so hook scripts stay in one location.
Keep hook behavior deterministic. Use `fail_closed` only for rules that must block on uncertainty,
and keep network calls or expensive model decisions out of command hooks.

If a host needs a different matcher or lifecycle event, add an adapter file under `hooks/adapters/`
and keep the executable logic in `hooks/scripts/`.
