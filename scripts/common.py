"""공용 유틸: 프런트매터·마크다운 절·장부 파싱."""
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"
EPISODES = ROOT / "episodes"
TRACKER = ROOT / "tracker"
BUILD = ROOT / "build"

# 설정 파일명. 기존 설정집 시트명이 다르면 여기만 바꾼다.
FILES = {
    "01": "01_개요.md",
    "02": "02_전체구성.md",
    "03": "03_세계관.md",
    "04": "04_인물.md",
    "05": "05_관계·세력.md",
    "06": "06_스킬.md",
    "07": "07_시스템창·방송.md",
    "08": "08_복선장부.md",
    "09": "09_연표.md",
    "10": "10_문체규칙.md",
    "state": "current_state.md",
}

LEN_MIN, LEN_MAX = 5000, 5500


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def ep_path(n: int) -> Path:
    return EPISODES / f"ep{n:03d}.md"


def split_frontmatter(text: str):
    """(frontmatter dict, body) — YAML 의존 없이 'key: value' / [a, b] 만 파싱."""
    fm, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        for ln in m.group(1).splitlines():
            km = re.match(r"^\s*([^:：]+)[:：]\s*(.*)$", ln)
            if not km:
                continue
            k, v = km.group(1).strip(), km.group(2).strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
            fm[k] = v
        body = m.group(2)
    return fm, body


def body_text(text: str) -> str:
    """프런트매터와 첫 제목 줄(# ...)을 뺀 본문."""
    _, body = split_frontmatter(text)
    lines = body.lstrip("\n").splitlines()
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def count_chars(s: str):
    with_space = len(s.replace("\n", ""))
    no_space = len(re.sub(r"\s+", "", s))
    return with_space, no_space


def section(text: str, heading: str) -> str:
    """heading 을 포함하는 첫 '#..' 헤더부터 같은/상위 레벨 다음 헤더 전까지."""
    out, level = [], None
    for ln in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lv = len(m.group(1))
            if level is not None and lv <= level:
                break
            if level is None and heading.strip() in m.group(2).strip():
                level = lv
                out.append(ln)
                continue
        if level is not None:
            out.append(ln)
    return "\n".join(out).strip()


def headers(text: str, level: int = 2):
    return [m.group(1).strip() for m in re.finditer(rf"^{'#'*level}\s+(.+?)\s*$", text, re.M)]


def parse_kv_block(text: str) -> dict:
    d = {}
    for ln in text.splitlines():
        m = re.match(r"^\s*-?\s*([^:：#]+)[:：]\s*(.*)$", ln)
        if m:
            d[m.group(1).strip()] = m.group(2).strip()
    return d


def split_list(s: str):
    if not s:
        return []
    s = re.sub(r"【.*?】", "", s)
    return [x.strip() for x in re.split(r"[,、，/]", s) if x.strip() and x.strip() not in ("-", "없음", "—")]


def ep_in_cell(cell: str, ep: int) -> bool:
    """'15' / '30~35' / '30-35' / '12, 40' 같은 셀에 ep 가 포함되는가."""
    for a, b in re.findall(r"(\d+)\s*[~\-–]\s*(\d+)", cell):
        if int(a) <= ep <= int(b):
            return True
    stripped = re.sub(r"\d+\s*[~\-–]\s*\d+", "", cell)
    return any(int(x) == ep for x in re.findall(r"\d+", stripped))


# 08_복선장부 열 인덱스 (열 순서 고정)
F_ID, F_CLUE, F_PLANT, F_SHOWN, F_RANGE, F_KNOWERS, F_COND, F_PAYOFF, F_STATUS = range(9)


def foreshadow_rows():
    """(header_line, [(cells, raw_line), ...])"""
    text = read(SETTING / FILES["08"])
    header, rows = None, []
    for ln in text.splitlines():
        if ln.startswith("| ID"):
            header = ln
            continue
        if re.match(r"^\|\s*F-\d+", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            rows.append((cells, ln))
    return header, rows
