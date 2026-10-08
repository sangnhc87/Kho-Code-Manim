"""COMB10 V2 — hoán vị có phần tử giống nhau và ràng buộc.
Mọi kết quả minh hoạ được kiểm chứng bằng liệt kê hữu hạn độc lập.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from math import factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
CHAPTER_LABELS={'identity': '01 · KHI HAI VẬT KHÔNG PHÂN BIỆT', 'mama': '02 · MAMA: 24 HOÁN VỊ THÀNH SÁU', 'banana': '03 · BANANA: TỪ 720 XUỐNG 60', 'general': '04 · CÔNG THỨC HOÁN VỊ LẶP', 'block': '05 · CÁC CHỮ A PHẢI ĐỨNG LIỀN NHAU', 'gaps': '06 · BA CHỮ A KHÔNG ĐỨNG LIỀN NHAU', 'boundary': '07 · RÀNG BUỘC Ở VỊ TRÍ ĐẦU VÀ CUỐI', 'challenge': '08 · AABBC: TỔNG HỢP VÀ LUYỆN TẬP'}
FORMULAS={'fourfact': '4! = 24', 'aabc': 'frac(4!, 2!) = 12', 'mama': 'frac(4!, 2! times 2!) = 6', 'banana': 'frac(6!, 3! times 2!) = 60', 'all720': '6! = 720', 'factorial': '3! times 2! = 12', 'general': 'frac(n!, k_1! times k_2! times dots times k_r!)', 'condition': 'k_1 + k_2 + dots + k_r = n', 'block12': 'frac(4!, 2!) = 12', 'gaps4': 'C^(4)_(3) = 4', 'gaps12': 'frac(3!, 2!) times C^(4)_(3) = 12', 'startB': 'frac(5!, 3! times 2!) = 10', 'endA': 'frac(5!, 2! times 2!) = 30', 'overlap6': 'frac(4!, 2! times 2!) = 6', 'union34': '10 + 30 - 6 = 34', 'aabbc30': 'frac(5!, 2! times 2!) = 30', 'adjAA12': 'frac(4!, 2!) = 12', 'free18': '30 - 12 = 18', 'both12': '30 - 12 - 12 + 6 = 12', 'compare': '60 = 12 + 48'}
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

BEATS=tuple(Beat(a[0],int(a[1]),a[2],tuple(a[3:6]),a[6],a[7],a[8],float(a[9]))
    for a in json.loads((ROOT/'comb10_beats.json').read_text(encoding='utf-8')))

def unique_words(word:str):
    return tuple(sorted({''.join(p) for p in permutations(word)}))

def multiset_count(word:str):
    denominator=1
    for count in Counter(word).values():denominator*=factorial(count)
    return factorial(len(word))//denominator

def count_banana_no_adjacent():
    return sum('AA' not in word for word in unique_words('BANANA'))

def validate():
    assert len(BEATS)==48 and len(CHAPTER_LABELS)==8
    assert [x for x in dict.fromkeys(b.section for b in BEATS)]==list(CHAPTER_LABELS)
    assert Counter(b.section for b in BEATS)=={key:6 for key in CHAPTER_LABELS}
    assert all([b.state for b in BEATS if b.section==key]==list(range(6)) for key in CHAPTER_LABELS)
    assert all(len(b.narration.split())>=43 for b in BEATS)
    assert all(not b.formula or b.formula in FORMULAS for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>1030
    assert len(unique_words('AABC'))==12
    assert len(unique_words('MAMA'))==6
    assert len(unique_words('BANANA'))==60
    assert multiset_count('AABC')==12 and multiset_count('MAMA')==6
    assert multiset_count('BANANA')==60
    banana=unique_words('BANANA')
    assert sum('AAA' in w for w in banana)==12
    assert sum('AA' not in w for w in banana)==12
    assert sum('AAA' not in w for w in banana)==48
    assert sum(w.startswith('B') for w in banana)==10
    assert sum(w.endswith('A') for w in banana)==30
    assert sum(w.startswith('B') and w.endswith('A') for w in banana)==6
    assert sum(w.startswith('B') or w.endswith('A') for w in banana)==34
    items=unique_words('AABBC')
    assert len(items)==30
    assert sum('AA' in w for w in items)==12
    assert sum('AA' not in w for w in items)==18
    assert sum('BB' in w for w in items)==12
    assert sum('AA' in w and 'BB' in w for w in items)==6
    assert sum('AA' not in w and 'BB' not in w for w in items)==12
    return True

if __name__=='__main__':
    validate()
    print(f'COMB10 VALID beats={len(BEATS)} words={sum(len(x.narration.split()) for x in BEATS)} seconds_base={sum(b.min_seconds for b in BEATS)+5.2}')
