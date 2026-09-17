# Codebase map

| Path | Purpose |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | Host entry points into shared project guidance |
| `plugin.json` | Portable plugin identity and OpenAI presentation |
| `.claude-plugin/` | Claude Code manifest and marketplace metadata |
| `.codex-plugin/` | Codex manifest overlay |
| `.agents/` | Antigravity-compatible root and skill registrations |
| `skills/` | Self-contained workflow skills |
| `hooks/` | Shared lifecycle configuration and scripts |
| `mcp/`, `mcp.json`, `.mcp.json` | MCP policy and host configurations |
| `worktrees/` | Worktree policy |
| `rules/`, `iron-laws/`, `guidelines/` | Operating contract |
| `workflows/`, `agents/`, `scripts/` | Optional runbooks, agents, and shared helpers |
| `docs/` | Maps and scope notes |

The source of truth is the generated plugin root. Installed hosts may cache or copy it, so paths must
remain valid after installation.
