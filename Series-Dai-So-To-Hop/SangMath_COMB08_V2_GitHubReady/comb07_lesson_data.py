"""Verified lesson data for COMB07 V2: combinations without order."""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
from itertools import permutations, combinations
from math import comb, perm, factorial
from series_config import symbol

ROOT=Path(__file__).resolve().parent
CHAPTER_IDS=('intro','ordered','groups','general','symmetry','constraint','captain','practice')
CHAPTER_LABELS={'intro': '01 · CHỌN NHÓM KHÔNG VAI TRÒ', 'ordered': '02 · SÁU THỨ TỰ MỘT NHÓM', 'groups': '03 · LIỆT KÊ MƯỜI NHÓM', 'general': '04 · CÔNG THỨC TỔ HỢP', 'symmetry': '05 · ĐỐI XỨNG VÀ PASCAL', 'constraint': '06 · CHỌN NHÓM CÓ ĐIỀU KIỆN', 'captain': '07 · NHÓM VÀ ĐỘI TRƯỞNG', 'practice': '08 · LUYỆN TẬP VÀ TỔNG KẾT'}
FORMULAS={'ordered60': 'A^(5)_(3) = 5 times 4 times 3 = 60', 'factor6': '3! = 6', 'count10': 'C^(5)_(3) = frac(60,6) = 10', 'groups10': 'C^(5)_(3) = 10', 'relation': 'A^(n)_(k) = C^(n)_(k) times k!', 'general': 'C^(n)_(k) = frac(n!,k! times (n-k)!)', 'count5': 'C^(5)_(3) = frac(5!,3! times 2!) = 10', 'extreme': 'C^(n)_(0) = C^(n)_(n) = 1', 'one': 'C^(n)_(1) = n', 'symmetry': 'C^(n)_(k) = C^(n)_(n-k)', 'seven': 'C^(7)_(2) = C^(7)_(5) = 21', 'pascal': 'C^(n)_(k) = C^(n-1)_(k-1) + C^(n-1)_(k)', 'pascal20': 'C^(6)_(3) = C^(5)_(2) + C^(5)_(3) = 20', 'six20': 'C^(6)_(3) = 20', 'bad4': 'C^(4)_(1) = 4', 'valid16': 'C^(6)_(3) - C^(4)_(1) = 20 - 4 = 16', 'alternate16': 'C^(4)_(3) + 2 times C^(4)_(2) = 4 + 12 = 16', 'must10': 'C^(5)_(2) = 10', 'eight56': 'C^(8)_(3) = 56', 'captain168': 'C^(8)_(3) times 3 = 168', 'captainfirst': '8 times C^(7)_(2) = 168', 'pick15': 'C^(6)_(2) = 15', 'gender31': 'C^(7)_(3) - C^(4)_(3) = 31', 'gender18': 'C^(4)_(2) times C^(3)_(1) = 18', 'sum32': 'C^(5)_(0) + C^(5)_(1) + C^(5)_(2) + C^(5)_(3) + C^(5)_(4) + C^(5)_(5) = 32'}

@dataclass(frozen=True)
class Beat:
    section:str
    state:int
    heading:str
    lines:tuple[str,str,str]
    takeaway:str
    narration:str
    formula:str
    min_seconds:float

def load_beats():
    data=json.loads((ROOT/'comb07_beats.json').read_text(encoding='utf-8'))
    return tuple(Beat(x[0],int(x[1]),x[2],tuple(x[3:6]),x[6],x[7],x[8],float(x[9])) for x in data)

BEATS=load_beats()
PEOPLE5='ABCDE'
PEOPLE6='ABCDEF'

def groups(n,k):
    return tuple(combinations('ABCDEFGH'[:n],k))

def ordered_groups(n,k):
    return tuple(permutations('ABCDEFGH'[:n],k))

def restricted_teams():
    return tuple(team for team in combinations(PEOPLE6,3) if not {'A','B'}<=set(team))

def teams_with_captain():
    return tuple((team,leader) for team in combinations('ABCDEFGH',3) for leader in team)

def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(x.section for x in BEATS))==CHAPTER_IDS
    assert Counter(x.section for x in BEATS)=={s:6 for s in CHAPTER_IDS}
    assert all([x.state for x in BEATS if x.section==s]==list(range(6)) for s in CHAPTER_IDS)
    assert len({b.heading for b in BEATS})==48
    assert all(len(b.lines)==3 and all(b.lines) for b in BEATS)
    assert all(len(b.narration.split())>=38 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>900
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    for n in range(1,9):
        for k in range(n+1):
            assert len(groups(n,k))==comb(n,k)
            assert len(ordered_groups(n,k))==perm(n,k)
            assert perm(n,k)==factorial(k)*comb(n,k)
            assert comb(n,k)==comb(n,n-k)
    assert len(groups(5,3))==10
    assert len(ordered_groups(5,3))==60
    assert len(restricted_teams())==16
    assert len(teams_with_captain())==168
    assert len({t for t in combinations('ABCDEFG',3) if 'A' in t and 'B' not in t})==10
    return True

if __name__=='__main__':
    validate()
    print(f'COMB07 validated: beats={len(BEATS)}, base_duration={sum(b.min_seconds for b in BEATS)+5.2:.1f}s, narration_words={sum(len(b.narration.split()) for b in BEATS)}')
