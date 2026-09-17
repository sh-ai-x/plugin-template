# Claude Code + Codex + Antigravity Plugin Template

Claude Code, Codex, and Google Antigravity (`agy`)에서 함께 사용할 플러그인을 만들기 위한
버전 관리형 템플릿 저장소입니다. 공통 `hooks`, `skills`, workflows, worktrees, MCP, rules와
namespace를 한 번 정의하고, 호스트별 manifest만 얇은 adapter로 둡니다.

첫 초기화 커밋은 [GitHub의 `main` 브랜치](https://github.com/sh-ai-x/plugin-template)에
push되어 있습니다.

## Quick start

```bash
python3 scripts/install-template.py v1 my-plugin
cd my-plugin
```

버전 이름을 첫 번째 인자로 지정합니다. 새 템플릿은 `templates/v2/`처럼 별도 디렉터리로
추가하며 기존 템플릿은 수정하지 않습니다.

```bash
python3 scripts/install-template.py --help
python3 scripts/install-template.py v1 my-plugin \
  --plugin-version 0.1.0 \
  --author-name "My Team" \
  --repository https://github.com/my-org/my-plugin
```

스크립트는 이름을 lowercase kebab-case로 정규화하고, 대상 디렉터리가 이미 있으면 중단하며,
세 호스트 manifest의 plugin name/version이 일치하는지 검사합니다.

## Generated layout

```text
my-plugin/
├── CLAUDE.md / AGENTS.md       # Claude/Codex 공통 instructions pointer
├── GEMINI.md                   # Antigravity instructions pointer
├── plugin.json                 # Portable Agent Plugins manifest
├── .claude-plugin/
│   ├── plugin.json             # Claude Code manifest
│   └── marketplace.json        # Claude marketplace entry
├── .codex-plugin/plugin.json   # Codex compatibility overlay
├── .agents/                    # AGY registration examples
├── skills/                     # Shared workflow skills
├── hooks/                      # Shared lifecycle config and scripts
├── worktrees/                  # Worktree policy
├── mcp/                        # MCP policy and server notes
├── rules/                      # Shared operating rules
├── workflows/                  # Workflow runbooks
├── agents/                     # Optional agent definitions
├── scripts/                    # Deterministic project helpers
├── iron-laws/ / guidelines/    # Invariants and working guidelines
├── docs/                       # Codebase map and scope notes
├── mcp.json                    # Portable MCP configuration
├── .mcp.json                   # Claude-compatible MCP configuration
└── .worktreeinclude            # Files copied into managed worktrees
```

공통 구현은 root의 `skills/`, `hooks/`, `mcp.json`에 두고, 호스트별 차이는 adapter manifest에서만
처리합니다. `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`는 세션 진입점에서 공통 문서로 안내하는 짧은
pointer이며, 실제 skill instructions는 `skills/<name>/SKILL.md` 안에 둡니다.

## Host compatibility

| Concern | Claude Code | Codex | Antigravity (`agy`) |
|---|---|---|---|
| Identity | `.claude-plugin/plugin.json` | root `plugin.json` + `.codex-plugin/plugin.json` | root `plugin.json` + `.agents/` |
| Skills | root `skills/<name>/SKILL.md` | same | same via `.agents/skills.json` |
| Hooks | `hooks/hooks.json` | same default path; review/trust before enable | adapter/optional |
| MCP | `.mcp.json` | portable `mcp.json` | host-specific registration if needed |
| Namespace | `/plugin:skill` style | plugin manifest + skill directory | plugin/skill paths |
| Install | `claude plugin marketplace add/install` | local marketplace + `codex plugin add` | Host discovery/registration using `.agents/` |
| Update | marketplace update, then plugin update | cachebuster + reinstall; new thread | pull source or re-register workspace |

`agy` support is intentionally an adapter: its registration format is not the Claude/Codex marketplace
contract. The template supplies `.agents/plugins.json` and `.agents/skills.json` examples that point at
the same root and `skills/` tree. It does not generate a host-specific installer; registration remains
owned by the consuming workspace and its AGY tooling.

## Design decisions and sources

- [Architecture and compatibility decisions](docs/architecture.md)
- [Host install/update instructions](templates/v1/README.md)
- [Official source references](docs/sources.md)

The v1 template follows the official guidance that skills are self-contained `SKILL.md` directories,
MCP is optional, hooks are lifecycle configuration, and plugin packages should keep portable files at
the root. Claude Code and Codex both cache or copy installed plugins, so generated files do not rely on
paths outside the plugin root. The generator is the only installer: choose a template version, then give
it the new plugin name.

## Verify

```bash
python3 -m pytest -q
TEST_ROOT=$(mktemp -d)
python3 scripts/install-template.py v1 example-plugin --output "$TEST_ROOT"
python3 -m json.tool "$TEST_ROOT/example-plugin/plugin.json" >/dev/null
```

## License

MIT
