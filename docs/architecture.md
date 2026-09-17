# Template architecture

This repository treats a plugin template as a compatibility boundary, not as a copy of one host's
private configuration.

## Canonical package

The package root owns the portable identity and reusable implementation:

- `plugin.json`: portable Agent Plugins manifest and the AGY identity surface
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`: short host-facing pointers into shared project docs
- `skills/<name>/SKILL.md`: workflow instructions and their local references/scripts
- `mcp.json`: portable MCP configuration
- `hooks/`: common lifecycle configuration and deterministic scripts
- `worktrees/`: documentation and optional helpers; no implicit destructive cleanup
- `mcp/`, `rules/`, `workflows/`, `agents/`, `scripts/`: shared extension and operating surfaces

The host adapters are deliberately thin:

| Host | Adapter | Reason |
|---|---|---|
| Claude Code | `.claude-plugin/plugin.json` | Claude manifest, namespace, and marketplace metadata |
| Codex | `.codex-plugin/plugin.json` | Compatibility metadata for the Codex plugin loader |
| Codex/ChatGPT | `extensions.com.openai` in `plugin.json` | Portable OpenAI presentation and hook wiring |
| Antigravity (`agy`) | root `plugin.json`, `.agents/plugins.json`, `.agents/skills.json` | Registration remains owned by the consuming workspace; the template does not add a host-specific installer |

## Namespace choice

The generated plugin name is normalized once and copied to every manifest. Skill directories never
carry a host prefix. Claude Code adds the plugin name when presenting a skill, while Codex and agy
discover the same skill directory through their own loaders. This avoids three divergent copies of a
workflow and keeps migrations mechanical.

## Hook choice

The hook event schema is shared where possible. Commands resolve the installed root using
`CLAUDE_PLUGIN_ROOT` with a `PLUGIN_ROOT` fallback, because Claude Code and Codex expose different
primary names. Scripts are common; matchers and event coverage may be split into adapter files when
host behavior diverges.

Hooks are opt-in at the behavior level: the initial hook files are no-op examples, and new hooks
should be added only after defining whether they are fail-open or fail-closed. A hook must not write
into the installed cache or depend on a sibling checkout.

## MCP choice

The template keeps both portable `mcp.json` and Claude-compatible `.mcp.json`. A server that is truly
portable should be represented in both with the corresponding schema. Secrets are always environment
references. If a server is only usable on one host, keep it in that host's adapter documentation and
do not claim it is cross-agent.

## Worktree choice

Worktree creation belongs to the host or the consuming repository. The plugin only observes the
current `cwd`, ships self-contained scripts, and documents `.worktreeinclude`. This avoids coupling a
plugin cache path to a particular machine and prevents automatic cleanup from deleting user work.

## Versioning and updates

Template versions are immutable directories such as `templates/v1` and `templates/v2`. A new template
version is added rather than mutating an old directory in place. Generated plugin versions use semver
and are written to all host manifests together.

Runtime updates differ by host:

- Claude Code updates the marketplace and then the installed plugin; explicit manifest versions are
  cache keys.
- Codex installs from a local marketplace and uses a cachebuster suffix for local iteration before
  reinstalling.
- agy registration points at the source root and shared `skills/` tree; update means pulling the source
  and refreshing the host's registration when required.
