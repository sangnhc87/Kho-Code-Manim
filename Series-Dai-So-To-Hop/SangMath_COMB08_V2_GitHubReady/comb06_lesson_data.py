"""Single source of truth for COMB06: mathematics, narration, beats, timings."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from math import perm, factorial, comb
import json
from pathlib import Path
from series_config import symbol

ROOT=Path(__file__).resolve().parent
CHAPTER_IDS=('intro','slots','tree','general','restrict','digits','compare','practice')
CHAPTER_LABELS={
'intro':'01  BA GIẢI THƯỞNG',
'slots':'02  ĐIỀN BA VỊ TRÍ',
'tree':'03  CÂY LỰA CHỌN',
'general':'04  ĐỊNH NGHĨA CHỈNH HỢP',
'restrict':'05  PHÂN CÔNG CÓ ĐIỀU KIỆN',
'digits':'06  LẬP SỐ KHÔNG LẶP',
'compare':'07  PHÂN BIỆT PHÉP ĐẾM',
'practice':'08  LUYỆN TẬP VÀ KẾT LUẬN',
}

def a(n,k):return symbol('A',n,k)
def c(n,k):return symbol('C',n,k)

FORMULAS={
 'first6':'6',
 'firsttwo':'6 times 5 = 30',
 'award120':f'{a(6,3)} = 6 times 5 times 4 = 120',
 'sixroles':'3! = 6',
 'compare720':'P_6 = 6! = 720',
 'general':f'{a("n","k")}',
 'falling':f'{a("n","k")} = n times (n-1) times dots.c times (n-k+1)',
 'factorial':f'{a("n","k")} = frac(n!, (n-k)!)',
 'zero':f'{a("n",0)} = 1',
 'all':f'{a("n","n")} = n!',
 'restrict180':'6 times 6 times 5 = 180',
 'comp180':f'{a(7,3)} - {a(6,2)} = 210 - 30 = 180',
 'banA':'6 times 5 times 4 = 120',
 'mustA60':'2 times 6 times 5 = 60',
 'exclude120':f'{a(6,3)} = 120',
 'digit4':'4',
 'digit44':'4 times 4 = 16',
 'digit48':'4 times 4 times 3 = 48',
 'digitcomp':f'{a(5,3)} - {a(4,2)} = 60 - 12 = 48',
 'digit30':'4 times 3 + 2 times 3 times 3 = 30',
 'team20':f'{c(6,3)} = 20',
 'divide6':'120 = 20 times 3!',
 'relation':f'{a("n","k")} = {c("n","k")} times k!',
 'quiz20':f'{a(5,2)} = 5 times 4 = 20',
 'seven210':f'{a(7,3)} = 7 times 6 times 5 = 210',
}

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
    raw=json.loads((ROOT/'comb06_beats.json').read_text(encoding='utf-8'))
    return tuple(Beat(row[0],int(row[1]),row[2],tuple(row[3:6]),row[6],row[7],row[8],float(row[9])) for row in raw)

BEATS=load_beats()
PEOPLE6='ABCDEF'
PEOPLE7='ABCDEFG'
DIGITS='01234'


def ordered_awards(people=PEOPLE6,k=3):
    return tuple(permutations(people,k))


def restricted_awards(people=PEOPLE7,banned='A',k=3):
    return {p for p in permutations(people,k) if p[0]!=banned}


def named_participant_not_first(people=PEOPLE7,name='A',k=3):
    return {p for p in permutations(people,k) if name in p and p[0]!=name}


def valid_digit_numbers(digits=DIGITS):
    return {int(''.join(p)) for p in permutations(digits,3) if p[0]!='0'}


def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(b.section for b in BEATS))==CHAPTER_IDS
    assert Counter(b.section for b in BEATS)=={s:6 for s in CHAPTER_IDS}
    assert all([b.state for b in BEATS if b.section==s]==list(range(6)) for s in CHAPTER_IDS)
    assert len({b.heading for b in BEATS})==48
    assert all(len(b.lines)==3 and all(b.lines) for b in BEATS)
    assert all(len(b.narration.split())>=38 for b in BEATS)
    assert sum(len(b.narration.split()) for b in BEATS)>=2800
    assert sum(b.min_seconds for b in BEATS)>900
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    for n in range(1,9):
        for k in range(n+1):
            assert len(ordered_awards('ABCDEFGH'[:n],k))==perm(n,k)
            assert perm(n,k)==factorial(n)//factorial(n-k)
    assert len(ordered_awards())==120
    assert len(restricted_awards())==180
    assert len(named_participant_not_first())==60
    assert len({p for p in permutations(PEOPLE7,3) if p[0]=='A'})==30
    assert len({p for p in permutations(PEOPLE7,3) if 'A' not in p})==120
    assert len(valid_digit_numbers())==48
    assert len({x for x in valid_digit_numbers() if x%2==0})==30
    assert 60-12==48 and 12+18==30
    assert len(ordered_awards())==comb(6,3)*factorial(3)
    return True

if __name__=='__main__':
    validate()
    print(f'COMB06 validated: beats={len(BEATS)}, duration={sum(b.min_seconds for b in BEATS)+5.2:.1f}s, narrated_words={sum(len(b.narration.split()) for b in BEATS)}')
