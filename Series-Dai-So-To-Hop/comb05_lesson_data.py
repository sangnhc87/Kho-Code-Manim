"""COMB05 V2 — exact permutation models, 48 complete Vietnamese lecture beats."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import permutations, combinations
from math import factorial, comb
from pathlib import Path
import json
from series_config import symbol

ROOT=Path(__file__).resolve().parent
CHAPTER_IDS=('intro','slots','grid','factorial','block','complement','advanced','practice')
CHAPTER_LABELS={
 'intro':'01  TỪ BÀI TOÁN ĐẾN KHÁI NIỆM',
 'slots':'02  QUY TẮC NHÂN TỪ CÁC VỊ TRÍ',
 'grid':'03  NHÌN THẤY TẤT CẢ 24 HOÁN VỊ',
 'factorial':'04  ĐỊNH NGHĨA VÀ GIAI THỪA',
 'block':'05  KỸ THUẬT GỘP KHỐI',
 'complement':'06  KHÔNG KỀ: HAI CÁCH GIẢI',
 'advanced':'07  MỞ RỘNG ĐIỀU KIỆN',
 'practice':'08  LUYỆN TẬP VÀ TỔNG KẾT',
}
FORMULAS={
 'four':'4','fourthree':'4 times 3 = 12',
 'fourthreetwo':'4 times 3 times 2 = 24','twentyfour':'P_4 = 4! = 24',
 'six':'3! = 6','fourtimesix':'4 times 3! = 24',
 'general':'P_n = n! = n times (n-1) times dots.c times 1',
 'five':'P_5 = 5! = 120','zero':'0! = 1',
 'recurrence':'P_n = n times P_(n-1)',
 'block24':'4! = 24','two':'2! = 2',
 'adjacent48':'4! times 2! = 48', 'small4':'2! times 2! = 4',
 'apart72':'5! - 2 times 4! = 72', 'threebase':'3! = 6',
 'gaps':f'{symbol("C",4,2)} = 6',
 'gaps72':f'3! times {symbol("C",4,2)} times 2! = 72',
 'before60':'frac(5!, 2) = 60','ends48':'2! times 4! = 48',
 'apart480':'6! - 2 times 5! = 480',
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
    raw=json.loads((ROOT/'comb05_beats.json').read_text(encoding='utf-8'))
    return tuple(Beat(r[0],r[1],r[2],tuple(r[3:6]),r[6],r[7],r[8],float(r[9])) for r in raw)

BEATS=load_beats()
BOOKS=tuple('ABCD')
FOUR_ORDERS=tuple(''.join(q) for q in permutations(BOOKS))
STUDENTS5=tuple('ABCDE')
STUDENTS6=tuple('ABCDEF')


def adjacent(seq,a='A',b='B'):
    return abs(seq.index(a)-seq.index(b))==1


def before(seq,a='A',b='B'):
    return seq.index(a)<seq.index(b)


def gap_count_5():
    """Independent constructive enumeration: permute CDE, insert A/B in distinct gaps."""
    results=set()
    for base in permutations('CDE'):
        for gap_a,gap_b in permutations(range(4),2):
            gap_to_letter={gap_a:'A',gap_b:'B'}
            out=[]
            for idx in range(4):
                if idx in gap_to_letter:out.append(gap_to_letter[idx])
                if idx<3:out.append(base[idx])
            results.add(''.join(out))
    return results


def count_adjacent(people='ABCDE'):
    return {''.join(seq) for seq in permutations(people) if adjacent(seq)}


def count_nonadjacent(people='ABCDE'):
    return {''.join(seq) for seq in permutations(people) if not adjacent(seq)}


def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(b.section for b in BEATS))==CHAPTER_IDS
    assert Counter(b.section for b in BEATS)=={s:6 for s in CHAPTER_IDS}
    assert all([b.state for b in BEATS if b.section==section]==list(range(6)) for section in CHAPTER_IDS)
    assert all(len(b.lines)==3 and all(b.lines) for b in BEATS)
    assert all(len(b.narration.split())>=35 for b in BEATS)
    assert all(18<=b.min_seconds<=24 for b in BEATS)
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>=840
    assert len(set(b.heading for b in BEATS))==48
    assert len(FOUR_ORDERS)==24 and len(set(FOUR_ORDERS))==24
    assert all(len(set(x))==4 and set(x)==set(BOOKS) for x in FOUR_ORDERS)
    assert len(count_adjacent())==48 and len(count_nonadjacent())==72
    assert len(gap_count_5())==72 and gap_count_5()==count_nonadjacent()
    all5={''.join(x) for x in permutations(STUDENTS5)}
    assert count_adjacent() | count_nonadjacent() == all5
    assert not (count_adjacent() & count_nonadjacent())
    assert sum(before(s) for s in permutations(STUDENTS5))==60
    assert sum(s[0] in 'AB' and s[-1] in 'AB' for s in permutations(STUDENTS6))==48
    assert len(count_nonadjacent(STUDENTS6))==480
    assert factorial(0)==1 and factorial(4)==24 and factorial(5)==120
    return True

if __name__=='__main__':
    validate()
    print(f'COMB05 LESSON VALIDATED beats={len(BEATS)} baseline={sum(b.min_seconds for b in BEATS):.1f}s words={sum(len(b.narration.split()) for b in BEATS)}')
