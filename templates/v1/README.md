# __PLUGIN_DISPLAY_NAME__

`__PLUGIN_NAME__` is a versioned cross-agent plugin scaffold for Claude Code, Codex, and Google
Antigravity (`agy`). It was generated from the `v1` template of the
[plugin-template](https://github.com/sh-ai-x/plugin-template) repository.

## Structure

```text
__PLUGIN_NAME__/
├── plugin.json                 # Portable Agent Plugins manifest and AGY identity
├── .claude-plugin/
│   ├── plugin.json             # Claude Code manifest
│   └── marketplace.json        # Single-plugin Claude marketplace
├── .codex-plugin/plugin.json   # Codex compatibility overlay
├── .agents/                    # AGY workspace registration examples
├── skills/                     # Shared workflows; one SKILL.md per skill
├── hooks/                     # Shared lifecycle config and scripts
├── mcp.json                    # Portable MCP schema
├── .mcp.json                   # Claude-compatible MCP schema
├── worktrees/                  # Worktree policy and integration notes
├── bin/install-agy.sh          # Optional AGY global/workspace installer
└── LICENSE                     # MIT
```

The root `plugin.json`, `skills/`, and `mcp.json` are the portable source of truth. Host manifests
only add metadata or compatibility wiring. Do not duplicate skill instructions between hosts.

## Namespace rule

Use `__PLUGIN_NAME__` as the only canonical plugin identifier. Keep skill directories short and
host-neutral, such as `skills/example-workflow/`.

| Host | Discovery/invocation shape |
|---|---|
| Claude Code | Plugin components are presented with the plugin namespace, for example `/__PLUGIN_NAME__:example-workflow`. |
| Codex | The plugin identity is `__PLUGIN_NAME__`; skills are discovered from `skills/<skill-name>/SKILL.md`. |
| Antigravity (`agy`) | The root manifest and `.agents/` entries point to the same `skills/` tree. |

Avoid embedding `claude-`, `codex-`, or `agy-` in skill names. Add host-specific behavior only in
adapter manifests, hook matchers, or installation scripts.

## Add a workflow

1. Copy `skills/example-workflow/` to a stable kebab-case name.
2. Rewrite its `SKILL.md` description around the user goal and trigger conditions.
3. Put deterministic code in `scripts/` inside that skill or in a shared `scripts/` directory.
4. Keep references and templates beside the skill so installed caches remain self-contained.
5. Test the skill in a new conversation after installation or update.

## Add MCP

Add a named server to both `mcp.json` and `.mcp.json` when the server is intended for both portable
Codex and Claude Code loading. Keep credentials as environment references, for example
`${SERVICE_API_KEY}`, and never commit secret values. Use `mcp.json` transport types accepted by the
portable Agent Plugins schema; use Claude's `.mcp.json` shape for Claude-specific configuration.

## Hooks

`hooks/hooks.json` is shared. The bundled scripts are no-op examples so a freshly generated plugin
does not block work. Replace them with small deterministic checks as the plugin contract becomes
clear. Use `${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT}}` to resolve bundled scripts on both Claude Code and
Codex.

## Install and update

### Claude Code

For a local development session:

```bash
claude --plugin-dir "$(pwd)"
```

For a GitHub marketplace:

```bash
claude plugin marketplace add __GITHUB_REPO__
claude plugin install __PLUGIN_NAME__@__MARKETPLACE_NAME__ --scope user
claude plugin update __PLUGIN_NAME__ --scope user
```

Update the marketplace before updating the plugin when the catalog itself changed:

```bash
claude plugin marketplace update __MARKETPLACE_NAME__
```

Claude Code caches marketplace plugins. If `version` is explicit, bump it for users to receive an
update; otherwise a Git source can use its commit SHA as the version. The generated template uses an
explicit semantic version so releases are deliberate.

### Codex

Use the repository's local marketplace during development, then reinstall after a manifest or skill
change:

```bash
codex plugin marketplace add .
codex plugin add __PLUGIN_NAME__@__MARKETPLACE_NAME__
```

For routine local iteration, update the Codex cachebuster suffix while preserving the semantic base
version, then reinstall the plugin from the marketplace. Start a new thread after reinstalling so
new skills and MCP tools are loaded.

### Antigravity (`agy`)

Use the included adapter when the `agy` CLI is available:

```bash
bin/install-agy.sh --global
bin/install-agy.sh --check
```

For one workspace only:

```bash
bin/install-agy.sh /path/to/workspace
```

Global mode uses symlinks, so pulling a new commit updates the linked source. Workspace mode updates
the `.agents/` registration while preserving unrelated entries.

## Worktrees

Keep plugin files self-contained because Claude marketplace installs are cached copies and Codex
managed worktrees are separate Git checkouts. Do not reference `../` paths or write persistent state
into the installed plugin directory. See `worktrees/README.md` and `.worktreeinclude`.

## Development checklist

- Keep `plugin.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json` on the same plugin
  name and version.
- Validate JSON after editing manifests.
- Test `claude --plugin-dir .` before publishing.
- Review and trust Codex plugin hooks before enabling them.
- Test the AGY adapter with `--dry-run` before a global install.
- Bump the plugin semantic version for distributed changes.
