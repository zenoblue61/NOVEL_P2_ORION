#!/usr/bin/env python3
"""회차 파일 정합성 검사. 커밋 전 pre-commit 훅이 호출한다.

사용: python scripts/lint_episode.py episodes/ep015.md [--no-length] [--strict]

오류(종료 1):
  - 프런트매터 누락 / 필수 키 누락 / 회차 번호와 파일명 불일치
  - 심은복선·회수복선 ID가 08_복선장부에 없음
  - 본문 분량 범위 밖 (--no-length 로 끌 수 있음)
  - 상태가 '확정'인데 progress.md 진행표에 행이 없음
경고(기본은 통과, --strict 면 오류):
  - 등장인물이 04_인물.md 헤더에 없음
  - 말미유형이 직전 2화와 같음 (연속 3화)
"""
import argparse
import re
import sys
from pathlib import Path

from common import (FILES, LEN_MAX, LEN_MIN, SETTING, TRACKER, F_ID, body_text,
                    count_chars, foreshadow_rows, headers, read, split_frontmatter)

REQUIRED = ["회차", "제목", "등장인물", "심은복선", "회수복선", "말미유형", "다음시작점", "상태"]


def progress_rows():
    rows = {}
    for ln in read(TRACKER / "progress.md").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|(.*)\|\s*$", ln)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            rows[int(m.group(1))] = cells
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--no-length", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    p = Path(a.file)
    errors, warns = [], []
    text = read(p)
    if not text:
        print(f"[오류] {p}: 파일 없음 또는 비어 있음")
        sys.exit(1)

    fm, _ = split_frontmatter(text)
    if not fm:
        errors.append("프런트매터(--- ... ---)가 없다. episodes/_TEMPLATE.md 형식을 따를 것.")
    for k in REQUIRED:
        if k not in fm:
            errors.append(f"프런트매터 키 누락: {k}")

    m = re.match(r"ep(\d{3})\.md$", p.name)
    if m and str(fm.get("회차", "")).strip() != str(int(m.group(1))):
        errors.append(f"프런트매터 회차({fm.get('회차')}) ≠ 파일명 회차({int(m.group(1))})")

    # 복선 ID
    _, rows = foreshadow_rows()
    ids = {c[F_ID] for c, _ in rows if c}
    for key in ("심은복선", "회수복선"):
        v = fm.get(key, [])
        v = v if isinstance(v, list) else [x.strip() for x in str(v).split(",") if x.strip()]
        for fid in v:
            if fid and fid not in ids:
                errors.append(f"{key} ID {fid} 가 08_복선장부에 없다.")

    # 등장인물
    heads = set(headers(read(SETTING / FILES["04"]), 2))
    chars = fm.get("등장인물", [])
    chars = chars if isinstance(chars, list) else [x.strip() for x in str(chars).split(",") if x.strip()]
    for c in chars:
        if c not in heads:
            warns.append(f"등장인물 '{c}' 가 04_인물.md 의 ## 헤더에 없다.")

    # 분량
    if not a.no_length:
        ws, _ = count_chars(body_text(text))
        if not (LEN_MIN <= ws <= LEN_MAX):
            errors.append(f"본문 {ws:,}자 — 기준 {LEN_MIN:,}~{LEN_MAX:,} 범위 밖.")

    # progress 연동 / 말미 유형 연속
    prows = progress_rows()
    ep = int(fm["회차"]) if str(fm.get("회차", "")).isdigit() else None
    if ep is not None:
        if fm.get("상태") == "확정" and ep not in prows:
            errors.append(f"상태가 확정인데 progress.md 진행표에 {ep}화 행이 없다.")
        ending = fm.get("말미유형", "")
        prev = [prows[n] for n in (ep - 1, ep - 2) if n in prows]
        # 진행표 열: 제목|구간|시간·장소|핵심 변화|심은 복선|회수 복선|말미 유형|다음 시작점|상태 → 말미 유형 index 6
        prev_endings = [r[6] for r in prev if len(r) > 6]
        if ending and len(prev_endings) == 2 and all(e == ending for e in prev_endings):
            warns.append(f"말미 유형 '{ending}' 이 직전 2화와 같다 (연속 3화).")

    for e in errors:
        print(f"[오류] {p.name}: {e}")
    for w in warns:
        print(f"[경고] {p.name}: {w}")
    if not errors and not warns:
        print(f"OK {p.name}")
    sys.exit(1 if errors or (a.strict and warns) else 0)


if __name__ == "__main__":
    main()
