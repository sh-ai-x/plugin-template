# Iron laws

These invariants keep the generated plugin portable:

1. One canonical plugin name and semantic version appear in every host manifest.
2. One shared skill tree is used by every host; do not fork instructions by host.
3. Hooks are deterministic, scoped to the plugin root, and explicit about failure behavior.
4. Skills, hooks, MCP servers, and scripts do not depend on sibling checkouts.
5. Secrets and machine-local state never enter the generated package.
6. Worktree behavior observes the current working directory and never performs implicit destructive cleanup.
7. A template version is an immutable compatibility contract; add `templates/v2/` for breaking changes.
8. Installation and update instructions match the host's actual cache and namespace behavior.
