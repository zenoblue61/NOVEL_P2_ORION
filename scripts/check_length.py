#!/usr/bin/env python3
"""회차 본문 글자 수 측정.

사용: python scripts/check_length.py episodes/ep001.md [episodes/ep002.md ...] [--min 5000] [--max 5500]
프런트매터(--- ... ---)와 첫 제목 줄(# ...)을 제외한 본문만 센다.
공백 포함(줄바꿈 제외) / 공백 제외 둘 다 출력. 기준은 공백 포함.
범위 밖이면 종료 코드 1.
"""
import argparse
import sys
from pathlib import Path

from common import LEN_MAX, LEN_MIN, body_text, count_chars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--min", type=int, default=LEN_MIN)
    ap.add_argument("--max", type=int, default=LEN_MAX)
    a = ap.parse_args()
    bad = 0
    for f in a.files:
        p = Path(f)
        if not p.exists():
            print(f"{f}: 파일 없음")
            bad += 1
            continue
        ws, ns = count_chars(body_text(p.read_text(encoding="utf-8")))
        ok = a.min <= ws <= a.max
        mark = "OK " if ok else ("부족" if ws < a.min else "초과")
        diff = "" if ok else f" ({ws - a.min:+,}자 vs 하한 / {ws - a.max:+,}자 vs 상한)"
        print(f"{mark} {p.name}: 공백 포함 {ws:,}자 / 공백 제외 {ns:,}자  [기준 {a.min:,}~{a.max:,}]{diff}")
        bad += 0 if ok else 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
