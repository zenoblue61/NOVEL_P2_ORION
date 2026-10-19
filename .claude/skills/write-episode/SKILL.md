---
name: write-episode
description: 회차 N을 집필한다. 컨텍스트 자동 수집 → 브리프 확인 → 초고 → 분량·정합성 검사 → 갱신 제안. 사용 /write-episode 15
---
회차 번호: $ARGUMENTS (비어 있으면 tracker/progress.md 브리프의 「회차」를 쓴다.)

1. `python scripts/extract_context.py --ep N` 을 실행하고 `build/context_epNNN.md` 를 읽는다. 다른 설정 파일은 열지 않는다. 스크립트가 실패하면 CLAUDE.md 1장의 수동 프로토콜을 따른다.
2. 「수집 경고」를 확인한다. 브리프 회차가 다르거나 브리프가 비어 있으면 **멈추고** 사용자에게 브리프 갱신을 요청한다 (질문 하나). 직전 회차 파일이 없으면 미확인 범위를 밝히고 진행한다.
3. 브리프의 목표·장애물·선택·변화·심을 복선·회수할 복선·바꾸지 말 사실·말미 유형을 내부 기준으로 삼는다. 준비표는 출력하지 않는다.
4. `episodes/_TEMPLATE.md` 형식으로 `episodes/epNNN.md` 를 쓴다. 프런트매터 상태: 초고. 제목 줄 형식: `# 제N화. 제목`.
5. `python scripts/check_length.py episodes/epNNN.md` 실행. 범위 밖이면 장면 단위로 가감하고 재측정한다. 측정값만 보고한다.
6. `python scripts/lint_episode.py episodes/epNNN.md` 실행. 오류는 고친다.
7. 응답 끝에 CLAUDE.md 5장의 「갱신 제안」 블록을 붙인다. **progress.md / current_state.md / 08_복선장부.md 는 아직 수정하지 않는다.** 사용자 승인 후 /commit-episode 가 반영한다.

출력: 회차 파일 경로, 측정 글자 수, 갱신 제안 블록. 본문을 채팅에 다시 붙여 넣지 않는다 (파일로 읽게 한다).
