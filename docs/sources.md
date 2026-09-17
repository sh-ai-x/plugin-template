# Source references

The v1 layout was derived from these primary references, checked on 2026-09-17:

- [OpenAI plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [OpenAI skills](https://developers.openai.com/plugins/concepts/skills)
- [OpenAI package your plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [OpenAI Codex Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
- [Claude Code create plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)

The Antigravity (`agy`) adapter follows the existing compatible plugin pattern in the local
`obsidian_organize` worktree: a root `plugin.json`, `.agents/plugins.json`, `.agents/skills.json`,
and explicit global/workspace installation modes. agy's local integration is kept as an adapter because
it does not share Claude Code or Codex's marketplace contract.
