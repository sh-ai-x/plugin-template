# GEMINI.md — shared project pointer

This is the Antigravity-facing entry point. Use the same source of truth as Claude Code and Codex:

- Contract and operating rules: `rules/index.md` (includes `iron-laws.md` and `guidelines.md`)
- Skills and workflows: `skills/README.md` and `workflows/README.md`
- Hooks and MCP: `hooks/index.md` and `mcp/README.md`
- Worktrees: `worktrees/README.md`
- Codebase map: `docs/CODEBASE-MAP.md`

The `.agents/` files register the root plugin and its shared skills; they are not a duplicate skill
implementation.
