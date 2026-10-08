"""COMB03: one authoritative data source for scenes, narration and QA."""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str, ...]
    takeaway: str
    narration: str
    formula: str = ""
    min_seconds: float = 17.1

CHAPTER_IDS = ("intro", "growth", "omega", "exacttwo", "noadjacent", "proof", "expansion", "practice")
CHAPTER_LABELS = {
    "intro": "01  BÀI TOÁN MỞ ĐẦU",
    "growth": "02  CÂY PHÁT TRIỂN TỪNG TẦNG",
    "omega": "03  KHÔNG GIAN MẪU",
    "exacttwo": "04  BIẾN CỐ ĐÚNG HAI LẦN NGỬA",
    "noadjacent": "05  ĐIỀU KIỆN KHÔNG LIÊN TIẾP",
    "proof": "06  ĐẾM ĐỦ VÀ KHÔNG TRÙNG",
    "expansion": "07  MỞ RỘNG BỐN LẦN GIEO",
    "practice": "08  LUYỆN TẬP VÀ TỔNG KẾT",
}

# Encode N=heads (ngua), S=tails (sap).
OMEGA_3 = tuple(''.join(a) for a in product('NS', repeat=3))
EXACTLY_TWO_N = tuple(x for x in OMEGA_3 if x.count('N') == 2)
NO_ADJACENT_N = tuple(x for x in OMEGA_3 if 'NN' not in x)
BAD_ADJACENT_N = tuple(x for x in OMEGA_3 if 'NN' in x)
OMEGA_4 = tuple(''.join(a) for a in product('NS', repeat=4))
NO_ADJACENT_4 = tuple(x for x in OMEGA_4 if 'NN' not in x)
TREE_PREFIXES = {k: tuple(''.join(a) for a in product('NS', repeat=k)) for k in (1,2,3)}
BRANCH_DEGREES = (2,1,3)

FORMULAS = {
    'two': '2 times 2 = 4',
    'eight': '2 times 2 times 2 = 8',
    'omega': '|Omega| = 2^3 = 8',
    'three': '3',
    'probthree': 'P(A) = frac(3, 8)',
    'five': '8 - 3 = 5',
    'probfive': 'P(B) = frac(5, 8)',
    'unique': '2^3 = 8',
    'six': '2 + 1 + 3 = 6',
    'eight4': '5 + 3 = 8',
    'fib': 'f_n = f_(n-1) + f_(n-2)',
    'four': '2^4 = 16',
}


def load_beats():
    data=json.loads((ROOT/'comb03_beats.json').read_text(encoding='utf-8'))
    return tuple(Beat(entry[0], entry[1], entry[2], tuple(entry[3:6]),
                      entry[6],entry[7],entry[8],float(entry[9])) for entry in data)

BEATS=load_beats()


def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(b.section for b in BEATS))==CHAPTER_IDS
    assert Counter(b.section for b in BEATS)==dict.fromkeys(CHAPTER_IDS,6)
    for section in CHAPTER_IDS:
        chapter=[b for b in BEATS if b.section==section]
        assert [b.state for b in chapter]==list(range(6))
    for b in BEATS:
        assert all(b.lines) and len(b.lines)==3
        assert len(b.narration.split())>=27,(b.section,b.state)
        assert 16<=b.min_seconds<=28
        assert not b.formula or b.formula in FORMULAS
    assert len(OMEGA_3)==8 and len(set(OMEGA_3))==8
    assert set(EXACTLY_TWO_N)=={'NNS','NSN','SNN'}
    assert set(NO_ADJACENT_N)=={'NSN','NSS','SNS','SSN','SSS'}
    assert set(BAD_ADJACENT_N)=={'NNN','NNS','SNN'}
    assert len(NO_ADJACENT_4)==8
    assert len(NO_ADJACENT_N)+len(BAD_ADJACENT_N)==8
    assert sum(BRANCH_DEGREES)==6
    assert sum(b.min_seconds for b in BEATS)>=780
    return True

if __name__=='__main__':
    validate()
    print('COMB03_LESSON_DATA_OK',len(BEATS), 'minimum_seconds',round(sum(b.min_seconds for b in BEATS)))
