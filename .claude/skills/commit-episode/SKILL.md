---
name: commit-episode
description: 승인된 갱신 제안을 progress.md·current_state.md·08_복선장부.md에 반영하고 회차 파일과 함께 한 커밋으로 묶는다. 사용 /commit-episode 15
---
회차 번호: $ARGUMENTS. 사용자가 「갱신 제안」을 승인한 뒤에만 실행한다. 승인 문구가 대화에 없으면 멈추고 확인한다.

1. `episodes/epNNN.md` 프런트매터를 읽는다. 상태를 「확정」으로 바꾼다.
2. `tracker/progress.md`
   - 「회차 진행표」에 행을 추가한다: `| N | 제목 | 구간 | 시간·장소 | 핵심 변화 | 심은 복선 | 회수 복선 | 말미 유형 | 다음 시작점 | 확정 |`
   - 「다음 회차 브리프」의 「회차」를 N+1 로 올리고 나머지 값은 비운다. 사용자가 다음 브리프 내용을 이미 줬으면 채운다. 키 이름은 바꾸지 않는다.
   - 구간 경계면 「구간 체크포인트」 상태를 갱신한다.
3. `setting/current_state.md`
   - 「기준 회차」를 N 으로. 승인된 변경(위치·부상·자원·초인화 단계·관계·정보 보유·미해결 갈등)을 반영하고 각 항목에 근거 회차 N 을 붙인다.
   - 「다음 회차 시작점」을 프런트매터의 다음시작점으로 바꾼다.
   - 승인되지 않은 사실은 쓰지 않는다.
4. `setting/08_복선장부.md`
   - 심은 복선: 상태 예정→제시됨, 「제시된 회차」에 N 기입.
   - 회수한 복선: 상태 →회수됨. 진전만 있으면 →진행.
   - 열 순서를 바꾸지 않는다.
5. 09_연표에 행 하나를 추가한다 (작중 시각·장소·경과 시간).
6. `python scripts/lint_episode.py episodes/epNNN.md` 통과 확인.
7. `git add episodes/epNNN.md tracker/progress.md setting/current_state.md setting/08_복선장부.md setting/09_연표.md` → `git commit -m "ep NNN: 제목"`. 훅이 차단하면 원인을 고치고 다시 커밋한다. SKIP_NOVEL_HOOK 을 쓰지 않는다.
8. 50·120·200·250화면 /resummarize-state 를 안내한다 (자동 실행하지 않는다).

출력: 커밋 해시, 반영한 변경 요약 3~5줄, 다음 회차 번호. 푸시는 하지 않는다.
