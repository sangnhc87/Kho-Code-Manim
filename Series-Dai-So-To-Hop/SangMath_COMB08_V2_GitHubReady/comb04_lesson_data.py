"""COMB04 V2: exact counting models + 48 synchronized teaching beats."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import permutations, combinations
from math import factorial, comb, perm
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
PEOPLE4 = tuple('ABCD')
PEOPLE5 = tuple('ABCDE')
PEOPLE6 = tuple('ABCDEF')
ORDERED4 = tuple(''.join(t) for t in permutations(PEOPLE4, 2))
UNORDERED4 = tuple(''.join(t) for t in combinations(PEOPLE4, 2))
UNORDERED5_3 = tuple(''.join(t) for t in combinations(PEOPLE5, 3))
UNORDERED6_2 = tuple(''.join(t) for t in combinations(PEOPLE6, 2))
ORDERS_ABC = tuple(''.join(t) for t in permutations('ABC'))

FORMULAS = {
    'ordered12': '4 times 3 = 12',
    'team6': 'frac(4 times 3, 2) = 6',
    'halfrelation': '12 = 2 times 6',
    'sixty': '5 times 4 times 3 = 60',
    'sixorders': '3! = 3 times 2 times 1 = 6',
    'ten': 'frac(60, 3!) = 10',
    'factorial': 'k! = k times (k-1) times dots.c times 1',
    'thirty': '6 times 5 = 30',
    'fifteen': 'frac(6 times 5, 2) = 15',
    'captain168': '8 times 21 = 56 times 3 = 168',
    'team56': 'frac(8 times 7 times 6, 3!) = 56',
    'twenty': '5 times 4 = 20',
}
CHAPTER_IDS = ('intro','ordered','unordered','swap','choose3','choose6','captain','practice')
CHAPTER_LABELS = {
    'intro':'01  HAI CÂU HỎI KHÁC NHAU',
    'ordered':'02  PHÂN CÔNG CÓ THỨ TỰ',
    'unordered':'03  CHỌN NHÓM KHÔNG THỨ TỰ',
    'swap':'04  THÍ NGHIỆM HOÁN ĐỔI',
    'choose3':'05  MỞ RỘNG CHỌN BA TRONG NĂM',
    'choose6':'06  HAI CÁCH ĐẾM TRÊN SÁU NGƯỜI',
    'captain':'07  BÀI TOÁN ĐỘI TRƯỞNG',
    'practice':'08  CỦNG CỐ VÀ CHUYỂN GIAO',
}
@dataclass(frozen=True)
class Beat:
    section:str
    state:int
    heading:str
    lines:tuple[str,...]
    takeaway:str
    narration:str
    formula:str
    min_seconds:float


def load_beats():
    raw=json.loads((ROOT/'comb04_beats.json').read_text(encoding='utf-8'))
    return tuple(Beat(a[0],a[1],a[2],tuple(a[3:6]),a[6],a[7],a[8],float(a[9])) for a in raw)

BEATS=load_beats()


def group_ordered_pairs(people=PEOPLE4):
    """Each unordered pair has exactly two distinct oriented representatives."""
    return {''.join(c):(''.join(c), ''.join(reversed(c))) for c in combinations(people,2)}


def team_with_captain(people='ABCDEFGH'):
    """Brute-force all distinct (three-person roster, designated captain) objects."""
    return {(tuple(group), captain) for group in combinations(people,3) for captain in group}


def team_with_captain_by_captain(people='ABCDEFGH'):
    """Independent enumeration: designate captain before two equal-role teammates."""
    return {(tuple(sorted((cap,)+tail)),cap)
            for cap in people
            for tail in combinations([p for p in people if p != cap],2)}


def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(b.section for b in BEATS))==CHAPTER_IDS
    assert Counter(b.section for b in BEATS)==dict.fromkeys(CHAPTER_IDS,6)
    assert all([b.state for b in BEATS if b.section==section]==list(range(6)) for section in CHAPTER_IDS)
    assert all(len(b.lines)==3 and all(b.lines) for b in BEATS)
    assert all(len(b.narration.split())>=30 for b in BEATS)
    assert all(16<=b.min_seconds<=27 for b in BEATS)
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>780
    assert len(ORDERED4)==12 and len(UNORDERED4)==6
    assert all(len(x)==2 for x in group_ordered_pairs().values())
    assert set(x for group in group_ordered_pairs().values() for x in group)==set(ORDERED4)
    assert len(UNORDERED5_3)==10 and factorial(3)*len(UNORDERED5_3)==perm(5,3)==60
    assert len(ORDERS_ABC)==6
    assert len(UNORDERED6_2)==15 and perm(6,2)==30
    assert len(team_with_captain())==168
    assert team_with_captain()==team_with_captain_by_captain()
    assert comb(8,3)*3==8*comb(7,2)==168
    assert len(set(b.heading for b in BEATS))==48
    return True

if __name__=='__main__':
    validate()
    print(f'COMB04 LESSON VALIDATED: beats={len(BEATS)}, min_seconds={sum(b.min_seconds for b in BEATS):.1f}, words={sum(len(b.narration.split()) for b in BEATS)}')
