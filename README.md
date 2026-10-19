# NOVEL_P2_ORION — 280화 웹소설 제작 저장소

Claude Code + Git 기반. 설정집은 모듈화된 마크다운, 규칙은 CLAUDE.md, 회차 생성은 슬래시 명령, 정합성은 스크립트와 pre-commit 훅이 지킨다.

## 처음 한 번
Windows(PowerShell):
```powershell
cd <저장소 폴더>
git init
.\scripts\install_hooks.ps1
python scripts\extract_context.py --ep 1     # 동작 확인
```
macOS/Linux/Git Bash:
```bash
git init
bash scripts/install_hooks.sh
# setting/ 의 【확정 필요】 를 기존 설정집으로 채운다 (01·03·04·06·08·10 우선)
# CLAUDE.md 2장 표를 10_문체규칙.md 와 맞춘다
git add -A && git commit -m "setting: 초기 설정집 등록"
```

## 매 회차 루프
| 단계 | 명령 | 결과 |
|---|---|---|
| 1. 브리프 작성 | `tracker/progress.md` 「다음 회차 브리프」를 사람이 채운다 | 목표·장애물·심을/회수할 복선·바꾸지 말 사실 |
| 2. 집필 | `/write-episode N` | `episodes/epNNN.md` (초고) + 갱신 제안 블록 |
| 3. 검토 | 사람이 읽는다. 필요하면 `/review-episode N 수정` | 문제 표 + 수정본 |
| 4. 승인·커밋 | 갱신 제안을 승인하고 `/commit-episode N` | progress·current_state·08 갱신 + 1커밋 |
| 체크포인트 | 50·120·200·250화에 `/resummarize-state N` | current_state 재작성 |

## 수동 스크립트
```bash
python scripts/extract_context.py --ep 15          # 집필 컨텍스트 묶음 → build/context_ep015.md
python scripts/check_length.py episodes/ep015.md   # 본문 글자 수 (공백 포함 5,000~5,500)
python scripts/lint_episode.py episodes/ep015.md   # 프런트매터·복선 ID·인물·분량·progress 연동 검사
```

## 규칙 요약
- 설정의 정본은 `setting/`. 원고가 설정을 바꾸지 않는다. 바꾸려면 설정 먼저 고치고 커밋.
- 회차 파일은 `tracker/progress.md` + `setting/current_state.md` 와 같은 커밋 (훅이 차단).
- 전체 설정집을 한 번에 읽히지 않는다. 브리프가 지정한 조각만.
- 사람 검토 단계를 빼지 않는다.

## 폴더
```
CLAUDE.md                 항상 적용되는 규칙
setting/00_INDEX.md       모듈 지도 — 언제 어느 파일을 읽는가
setting/01~10_*.md        설정 모듈 (기존 번호 체계 유지)
setting/current_state.md  현재 회차까지의 확정 상태 (매 회차 필수)
episodes/epNNN.md         회차 원고 (프런트매터 + 본문)
tracker/progress.md       진행표 + 다음 회차 브리프 + 재요약 로그
scripts/                  extract_context / check_length / lint_episode / hooks
.claude/skills/           /write-episode /review-episode /commit-episode /resummarize-state
build/                    자동 생성 컨텍스트 (커밋 안 함)
```
