"""COMB09: ordered selections with repetition, 48 independently auditable lesson beats."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import product, permutations
from math import comb, perm
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CHAPTER_LABELS = {'repeat': '01 · CÓ LẶP KHÁC GÌ KHÔNG LẶP?', 'strings': '02 · DÃY CÓ THỨ TỰ VÀ N MŨ K', 'pin': '03 · MÃ PIN VÀ CHỮ SỐ ĐẦU 0', 'norepeat': '04 · KHI KHÔNG ĐƯỢC LẶP', 'multiset': '05 · CÙNG LẶP, NHƯNG KHÔNG XÉT THỨ TỰ', 'atleast': '06 · ÍT NHẤT MỘT CHỮ A', 'exact': '07 · ĐÚNG HAI CHỮ A', 'adjacency': '08 · KHÔNG CÓ HAI CHỮ A LIỀN NHAU'}
FORMULAS = {'nine': '3 times 3 = 9', 'threepower': '3^3 = 27', 'general': 'n^k', 'fourpower': '3^4 = 81', 'pin10': '10^4 = 10 000', 'prefixzero': '0 0 7 3', 'norepeat': '10 times 9 times 8 times 7 = 5 040', 'number': '9 times 9 times 8 times 7 = 4 536', 'length3': '3 times 2 times 1 = 6', 'multiset10': 'C^(5)_(3) = 10', 'compare2710': '27 != 10', 'complement': '3^4 - 2^4 = 65', 'noa': '2^4 = 16', 'positions': 'C^(4)_(2) = 6', 'otherchoices': '2^2 = 4', 'exact24': 'C^(4)_(2) times 2^2 = 24', 'Fbase': 'F_0 = 1 quad F_1 = 3', 'Frec': 'F_n = 2 F_(n-1) + 2 F_(n-2)', 'Fnum': 'F_2 = 8 quad F_3 = 22 quad F_4 = 60', 'F60': '2 times 22 + 2 times 8 = 60', 'quiz': '3^3 - 2^3 = 19'}
@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str,str,str]
    takeaway: str
    narration: str
    formula: str
    min_seconds: float
BEATS = tuple(Beat(a[0],int(a[1]),a[2],tuple(a[3:6]),a[6],a[7],a[8],float(a[9]))
              for a in json.loads((ROOT/'comb09_beats.json').read_text(encoding='utf-8')))

def words(n, alphabet='ABC'):
    return tuple(''.join(x) for x in product(alphabet, repeat=n))

def nonadjacent(n):
    return tuple(w for w in words(n) if 'AA' not in w)

def multiset_choices():
    return set(''.join(sorted(x)) for x in product('ABC',repeat=3))

def four_digit_numbers_no_repeat():
    return tuple(1000*a+100*b+10*c+d for a,b,c,d in permutations(range(10),4) if a!=0)

def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(b.section for b in BEATS))==tuple(CHAPTER_LABELS)
    assert Counter(b.section for b in BEATS)=={x:6 for x in CHAPTER_LABELS}
    assert all([b.state for b in BEATS if b.section==sec]==list(range(6)) for sec in CHAPTER_LABELS)
    assert all(len(b.narration.split())>=43 for b in BEATS)
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>=960
    assert len(words(2))==9 and len(words(3))==27
    assert len(words(4))==81
    assert len(set(product(range(10),repeat=4)))==10000
    assert len(set(permutations(range(10),4)))==5040
    assert len(four_digit_numbers_no_repeat())==4536
    assert len(multiset_choices())==10 and comb(5,3)==10
    assert len([w for w in words(4) if 'A' in w])==65
    assert len([w for w in words(4) if w.count('A')==2])==24
    assert [len(nonadjacent(n)) for n in range(5)]==[1,3,8,22,60]
    assert all('AA' not in w for w in nonadjacent(4))
    return True
if __name__=='__main__':
    validate()
    print('COMB09_OK',len(BEATS),'duration',sum(b.min_seconds for b in BEATS)+5.2,'words',sum(len(b.narration.split()) for b in BEATS))
