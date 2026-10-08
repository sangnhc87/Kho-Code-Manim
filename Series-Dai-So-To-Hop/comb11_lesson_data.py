"""COMB11: Hoán vị vòng tròn, bài tập điều kiện, vòng hạt và bao hàm-loại trừ."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import permutations
from math import factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
CHAPTER_LABELS = {'rotation': '01 · PHÉP QUAY VÀ CÁCH XẾP VÒNG TRÒN', 'anchor': '02 · CỐ ĐỊNH MỘT NGƯỜI', 'reflection': '03 · PHÂN BIỆT QUAY VÀ LẬT GƯƠNG', 'adjacent': '04 · HAI NGƯỜI NGỒI CẠNH NHAU', 'apart': '05 · HAI NGƯỜI KHÔNG NGỒI CẠNH', 'alternate': '06 · XẾP NAM NỮ XEN KẼ', 'couples': '07 · BA CẶP VỢ CHỒNG, KHÔNG CẶP NÀO KỀ NHAU', 'challenge': '08 · VẬN DỤNG VÀ KIỂM TRA ĐIỀU KIỆN'}
FORMULAS = {'line24': '4! = 24', 'orbit4': 'frac(4!,4) = 6', 'circle4': 'frac(4!,4) = 3! = 6', 'threefact': '3! = 6', 'compare4': '4! = 24 quad 3! = 6', 'threecircle': '(3-1)! = 2', 'line720': '6! = 720', 'fixA': '5!', 'fix120': '5! = 120', 'general': '(n-1)!', 'quotient': 'frac(n!,n) = (n-1)!', 'chairs': '6! = 720', 'mirror': '120 != 60', 'necklace': '120 / 2 = 60', 'mirror60': 'frac(120,2) = 60', 'models': '720 quad 120 quad 60', 'symmetry': '"cẩn trọng với phần tử trùng"', 'quiz': '"đọc điều kiện trước"', 'pair': 'A B', 'block5': '(5-1)! = 4!', 'twoorders': '2! times 4!', 'adj48': '2 times 4! = 48', 'anchor48': '2 times 4! = 48', 'blockrule': '"gộp khối rồi hoán đổi bên trong"', 'complement': '120-48', 'sub72': '120-48=72', 'threepositions': '5-2=3', 'direct72': '3 times 4! = 72', 'wrap': '"vòng khép kín"', 'seven480': '6! - 2 times 5! = 480', 'men': 'M_1 quad M_2 quad M_3', 'men2': '(3-1)! = 2', 'girls': '3! = 6', 'twelve': '2 times 6=12', 'orientation': '"không nhân hai vì chọn điểm đầu"', 'alternategeneral': '(m-1)! times m!', 'couples': 'E_1, E_2, E_3', 'all120': '5! =120', 'one48': '2 times 4! = 48', 'two24': '2^2 times 3! = 24', 'three16': '2^3 times 2! = 16', 'final32': '120-3 times 48+3 times 24-16=32', 'opposite': '"A đối diện B"', 'opp24': '4! =24', 'triple': '4! times 3!', 'triple144': '4! times 3! =144', 'decision': '"quay / phản xạ / điều kiện"', 'summary': '120 quad 48 quad 72 quad 32'}
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
BEATS=tuple(Beat(r[0],int(r[1]),r[2],tuple(r[3:6]),r[6],r[7],r[8],float(r[9])) for r in json.loads((ROOT/'comb11_beats.json').read_text(encoding='utf-8')))

def circular_representatives(n:int):
    """All oriented arrangements of n distinct people modulo rotation."""
    if n<3:raise ValueError('n must be >= 3')
    return tuple((0,)+p for p in permutations(range(1,n)))

def neighbors(cycle,a,b):
    ia=cycle.index(a); ib=cycle.index(b); n=len(cycle)
    return (ia-ib)%n in (1,n-1)

def alternating(cycle,m=3):
    return all((cycle[i]<m)!=(cycle[(i+1)%len(cycle)]<m) for i in range(len(cycle)))

def opposite(cycle,a,b):
    n=len(cycle)
    return n%2==0 and (cycle.index(a)-cycle.index(b))%n==n//2

def no_couple_adjacent(cycle):
    return all(not neighbors(cycle,i,i+3) for i in range(3))

def validate():
    from collections import Counter
    assert len(BEATS)==48
    assert Counter(x.section for x in BEATS)=={key:6 for key in CHAPTER_LABELS}
    assert all(x.formula in FORMULAS for x in BEATS)
    assert all(len(b.narration.split())>=43 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>1000
    six=circular_representatives(6)
    assert len(six)==120
    assert sum(neighbors(c,0,1) for c in six)==48
    assert sum(not neighbors(c,0,1) for c in six)==72
    assert sum(alternating(c) for c in six)==12
    assert sum(opposite(c,0,1) for c in six)==24
    assert sum(no_couple_adjacent(c) for c in six)==32
    assert len(circular_representatives(4))==6
    assert len(circular_representatives(7))==720
    seven=circular_representatives(7)
    # A,B,C occupy a block: in the induced circular sequence each consecutive triple counts.
    assert sum(any(set((c[i],c[(i+1)%7],c[(i+2)%7]))=={0,1,2} for i in range(7)) for c in seven)==144
    assert 120-3*48+3*24-16 ==32
    assert factorial(6)//6==120
    return True

if __name__=='__main__':
    validate()
    print(f'COMB11 VALID beats={len(BEATS)} words={sum(len(x.narration.split()) for x in BEATS)} seconds={sum(x.min_seconds for x in BEATS)}')
