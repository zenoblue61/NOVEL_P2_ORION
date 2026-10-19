#!/usr/bin/env python3
"""회차 N 집필에 필요한 설정 조각만 모아 build/context_epNNN.md 로 만든다.

사용:
  python scripts/extract_context.py --ep 15
  python scripts/extract_context.py --ep 15 --chars 한도윤,서리안 --files "06_스킬#초인화 단계표,07_시스템창·방송" --prev 2

기본값은 tracker/progress.md 「## 다음 회차 브리프」의 「등장 인물」「추가 설정 파일」「심을 복선」「회수할 복선」을 쓴다.
수집 항목: current_state 전체 / 브리프 / 직전 N화 전문 / 해당 복선 행 / 등장 인물 블록 / 지정 설정 절.
"""
import argparse
import sys

from common import (BUILD, EPISODES, FILES, SETTING, TRACKER, F_PAYOFF, F_PLANT,
                    F_STATUS, F_ID, ep_in_cell, ep_path, foreshadow_rows, headers,
                    parse_kv_block, read, section, split_list)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--chars", default=None, help="쉼표 구분 인물명 (기본: 브리프)")
    ap.add_argument("--files", default=None, help="쉼표 구분 '06_스킬#절' (기본: 브리프)")
    ap.add_argument("--prev", type=int, default=2, help="직전 몇 화 전문을 포함할지")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    ep = a.ep
    warn = []

    # 1) 브리프
    progress = read(TRACKER / "progress.md")
    brief_blk = section(progress, "다음 회차 브리프")
    brief = parse_kv_block(brief_blk)
    if not brief_blk:
        warn.append("progress.md 에 「## 다음 회차 브리프」 블록이 없다.")
    bep = brief.get("회차", "")
    if bep.isdigit() and int(bep) != ep:
        warn.append(f"브리프 회차({bep}) ≠ 요청 회차({ep}). 브리프를 먼저 갱신하라.")

    chars = split_list(a.chars) if a.chars is not None else split_list(brief.get("등장 인물", ""))
    files = split_list(a.files) if a.files is not None else split_list(brief.get("추가 설정 파일", ""))
    plant_ids = split_list(brief.get("심을 복선", ""))
    payoff_ids = split_list(brief.get("회수할 복선", ""))

    parts = [f"# 회차 {ep} 집필 컨텍스트 (자동 수집 — 읽기 전용)\n",
             "> 이 파일은 build/ 에 있으며 커밋하지 않는다. 설정의 정본은 setting/ 이다.\n"]

    # 2) current_state
    parts += ["\n---\n## [필수] setting/current_state.md\n", read(SETTING / FILES["state"]) or "(비어 있음)"]

    # 3) 브리프
    parts += ["\n---\n## [필수] 이번 회차 브리프 (tracker/progress.md)\n", brief_blk or "(없음)"]

    # 4) 직전 회차 전문
    for n in range(max(1, ep - a.prev), ep):
        p = ep_path(n)
        if p.exists():
            parts += [f"\n---\n## [필수] 직전 회차 전문: {p.name}\n", read(p)]
        else:
            warn.append(f"{p.name} 이 없다. 연속성 검증 불가 — 미확인으로 둔다.")

    # 5) 복선 행
    header, rows = foreshadow_rows()
    picked = []
    for cells, raw in rows:
        if len(cells) < 9:
            warn.append(f"08_복선장부 행 열 수 부족: {cells[0] if cells else raw}")
            continue
        fid, status = cells[F_ID], cells[F_STATUS]
        hit = (status == "진행"
               or (status == "예정" and ep_in_cell(cells[F_PLANT], ep))
               or (status in ("제시됨", "진행") and ep_in_cell(cells[F_PAYOFF], ep))
               or fid in plant_ids or fid in payoff_ids)
        if hit:
            picked.append(raw)
    known_ids = {c[F_ID] for c, _ in rows if len(c) > F_ID}
    for fid in plant_ids + payoff_ids:
        if fid not in known_ids:
            warn.append(f"브리프의 복선 ID {fid} 가 08_복선장부에 없다.")
    parts += ["\n---\n## [필수] 이번 회차 관련 복선 (setting/08_복선장부.md)\n"]
    parts += [header + "\n|---|---|---|---|---|---|---|---|---|\n" + "\n".join(picked)] if picked else ["(해당 없음)"]
    parts += ["\n브리프 지정 — 심을 복선: " + (", ".join(plant_ids) or "없음")
              + " / 회수할 복선: " + (", ".join(payoff_ids) or "없음")]

    # 6) 인물 블록
    chars_text = read(SETTING / FILES["04"])
    char_heads = headers(chars_text, 2)
    parts += ["\n---\n## [필수] 등장 인물 블록 (setting/04_인물.md)\n"]
    if not chars:
        warn.append("브리프에 「등장 인물」이 없다. 인물 블록을 수집하지 못했다.")
    for c in chars:
        blk = section(chars_text, c)
        if blk:
            parts.append(blk + "\n")
        else:
            warn.append(f"04_인물.md 에 '{c}' 블록이 없다. (존재하는 헤더: {', '.join(char_heads[:12])}…)")

    # 7) 지정 설정 절
    if files:
        parts += ["\n---\n## [선택] 브리프가 지정한 설정 절\n"]
    for spec in files:
        fname, _, sec = spec.partition("#")
        key = fname.strip()[:2]
        path = SETTING / FILES.get(key, fname.strip() if fname.strip().endswith(".md") else fname.strip() + ".md")
        text = read(path)
        if not text:
            warn.append(f"설정 파일 {path.name} 을 찾지 못했다.")
            continue
        blk = section(text, sec.strip()) if sec.strip() else text
        if not blk:
            warn.append(f"{path.name} 에 '{sec}' 절이 없다. (헤더: {', '.join(headers(text, 2)[:10])})")
            continue
        parts += [f"### {path.name}" + (f" — {sec.strip()}" if sec.strip() else ""), blk, ""]

    # 8) 경고
    parts += ["\n---\n## 수집 경고\n", "\n".join(f"- {w}" for w in warn) if warn else "- 없음"]

    BUILD.mkdir(exist_ok=True)
    out = BUILD / (a.out or f"context_ep{ep:03d}.md")
    text = "\n".join(parts)
    out.write_text(text, encoding="utf-8")
    print(f"{out.relative_to(BUILD.parent)}  ({len(text):,}자)")
    for w in warn:
        print(f"[경고] {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
