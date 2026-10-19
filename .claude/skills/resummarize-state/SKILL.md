---
name: resummarize-state
description: 체크포인트(50·120·200·250화)에서 current_state.md를 원문 대조로 재작성해 컨텍스트 비대화를 막는다. 사용 /resummarize-state 120
---
체크포인트 회차: $ARGUMENTS.

1. 읽을 것: `setting/current_state.md` 전체, `tracker/progress.md` 의 직전 체크포인트 이후 진행표 행 전부, `setting/08_복선장부.md` 전체, `setting/09_연표.md` 의 해당 구간, `setting/02_전체구성.md`.
   원문 대조가 필요한 항목(인물 상태·정보 보유의 근거)은 해당 회차 `episodes/` 파일의 그 장면만 확인한다. 전 회차를 다시 읽지 않는다.
2. `current_state.md` 를 **재작성**한다.
   - 지금도 유효한 사실만 남긴다. 해소된 갈등·끝난 의무·회수된 복선 관련 상태는 삭제한다.
   - 각 항목에 근거 회차를 붙인다. 근거를 못 찾은 항목은 삭제하지 말고 「미확인(이전 state 승계)」로 표시한다.
   - 「인물별 정보 보유」는 현재 시점의 비대칭만 남긴다 (모두가 알게 된 사실은 삭제).
   - 분량 목표: 재작성 전보다 짧게. 길어졌다면 요약이 아니라 병합이다 — 다시 줄인다.
3. 재작성 전후 차이를 표로 낸다: 삭제한 항목 | 이유(해소 회차) / 수정한 항목 | 근거 회차 / 미확인 항목.
4. `tracker/progress.md` 「재요약 로그」에 행 추가. 「구간 체크포인트」의 재요약 완료 열 갱신.
5. `git add setting/current_state.md tracker/progress.md` → `git commit -m "state: N화까지 재요약"`.
6. 02_전체구성.md 의 남은 구간이 현실과 어긋나면 「검토 필요」로 보고만 한다. 임의 수정하지 않는다.
