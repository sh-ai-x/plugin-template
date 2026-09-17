# Worktree policy

Worktrees belong to the consuming Git repository, not to the installed plugin cache. The plugin may
provide scripts and hooks that observe a worktree, but it must not assume a fixed checkout path.

- Use relative paths or the host-provided plugin root for bundled files.
- Put persistent plugin state under the host data directory, never inside the installed cache.
- Do not copy secrets through `.worktreeinclude`.
- Keep branch creation and removal explicit; do not delete worktrees from a lifecycle hook without a
  user-visible policy.

Claude Code and Codex can both run isolated worktree sessions, but their orchestration and checkout
locations differ. Treat `cwd` from hook input as the current project root and use Git commands only
after checking that the target is a repository.
