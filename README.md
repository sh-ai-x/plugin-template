# Claude Code + Codex Plugin Template

Claude Code와 Codex에서 함께 사용할 수 있는 플러그인을 만들기 위한 버전 관리형 템플릿 저장소입니다.

이 저장소는 공통 `hooks`, `skills`, `worktrees`, `MCP`, 워크플로우, namespace 규칙과 각 호스트의 설치·업데이트 방식을 조합해 새 플러그인 프로젝트를 생성하는 것을 목표로 합니다.

템플릿은 버전별 디렉터리로 관리하고, 단일 설치 스크립트에서 버전 이름을 선택해 새 플러그인을 생성합니다.

## Status

초기 저장소를 준비하는 단계입니다. 템플릿 버전과 생성 스크립트는 초기 push 이후 추가됩니다.

## Design goals

- Claude Code와 Codex의 공통 컴포넌트는 한 번만 정의
- 호스트별 manifest와 호환성 차이는 명시적인 adapter로 분리
- 템플릿 버전은 서로 독립된 디렉터리로 보존
- 설치·업데이트는 재현 가능한 단일 명령으로 실행
- worktree와 MCP 설정은 비밀정보를 커밋하지 않는 구조로 제공

## Planned layout

```text
templates/
  v1/
scripts/
docs/
```

## License

License will be added with the first template release.
