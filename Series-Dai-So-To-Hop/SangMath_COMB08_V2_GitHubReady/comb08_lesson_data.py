"""COMB08: mathematically checked culmination of Season 1."""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
from itertools import combinations,permutations
from math import comb,perm,factorial
ROOT=Path(__file__).resolve().parent
CHAPTER_IDS=tuple({'compare': '01 · BA TÌNH HUỐNG, BA PHÉP ĐẾM', 'diagnose': '02 · CÂY QUYẾT ĐỊNH CHỌN PHƯƠNG PHÁP', 'roles': '03 · CÙNG SÁU HỌC SINH, HAI CÁCH CHỌN', 'captain': '04 · CHỌN ĐỘI VÀ PHÂN CÔNG ĐỘI TRƯỞNG', 'forbidden': '05 · PHÂN CÔNG CÓ ĐIỀU KIỆN CẤM', 'gender': '06 · CHỌN NHÓM NAM NỮ CÓ RÀNG BUỘC', 'digits': '07 · LẬP SỐ VÀ CHIA TRƯỜNG HỢP', 'capstone': '08 · BÀI TOÁN TỔNG HỢP NÂNG CAO'})
CHAPTER_LABELS={'compare': '01 · BA TÌNH HUỐNG, BA PHÉP ĐẾM', 'diagnose': '02 · CÂY QUYẾT ĐỊNH CHỌN PHƯƠNG PHÁP', 'roles': '03 · CÙNG SÁU HỌC SINH, HAI CÁCH CHỌN', 'captain': '04 · CHỌN ĐỘI VÀ PHÂN CÔNG ĐỘI TRƯỞNG', 'forbidden': '05 · PHÂN CÔNG CÓ ĐIỀU KIỆN CẤM', 'gender': '06 · CHỌN NHÓM NAM NỮ CÓ RÀNG BUỘC', 'digits': '07 · LẬP SỐ VÀ CHIA TRƯỜNG HỢP', 'capstone': '08 · BÀI TOÁN TỔNG HỢP NÂNG CAO'}
FORMULAS={'factorial720': 'P_6 = 6! = 720', 'arrange30': 'A^(6)_(2) = 6 times 5 = 30', 'choose15': 'C^(6)_(2) = frac(6 times 5,2!) = 15', 'relation': 'A^(n)_(k) = C^(n)_(k) times k!', 'fullperm': 'P_n = n!', 'genericarr': 'A^(n)_(k) = frac(n!,(n-k)!)', 'genericchoose': 'C^(n)_(k) = frac(n!,k! times (n-k)!)', 'check30': 'A^(6)_(2) = 2! times C^(6)_(2) = 30', 'captain56': 'C^(8)_(3) = 56', 'captain168': 'C^(8)_(3) times 3 = 168', 'captain21': 'C^(7)_(2) = 21', 'captainfirst': '8 times C^(7)_(2) = 168', 'captainrelation': '3 times C^(8)_(3) = A^(8)_(1) times C^(7)_(2)', 'forbid210': 'A^(7)_(3) = 7 times 6 times 5 = 210', 'forbid30': 'A^(6)_(2) = 30', 'forbid180': '6 times 6 times 5 = 180', 'forbidalt': '210 - 30 = 180', 'genderall': 'C^(7)_(3) = 35', 'gendernone': 'C^(4)_(3) = 4', 'gender31': 'C^(7)_(3)-C^(4)_(3) = 31', 'gender18': 'C^(4)_(2) times C^(3)_(1) = 18', 'gendercheck': 'C^(4)_(2) times C^(3)_(1)+C^(4)_(1) times C^(3)_(2)+C^(3)_(3) = 31', 'digit48': '4 times 4 times 3 = 48', 'digit0': '4 times 3 = 12', 'digit24': '2 times 3 times 3 = 18', 'digit30': '12 + 18 = 30', 'digitother': '48 - 30 = 18', 'capall': 'C^(8)_(3) times 3 = 168', 'capbad': 'C^(6)_(3) times 3 = 60', 'capbadA': 'C^(7)_(2) = 21', 'cap87': '168 - 60 - 21 = 87', 'cap42': 'C^(7)_(2) times 2 = 42', 'cap45': 'C^(6)_(2) times 3 = 45', 'capboth': '42 + 45 = 87', 'capleaderB': 'C^(7)_(2) = 21', 'capleaderother': '6 times (C^(7)_(2) - C^(5)_(2)) = 66', 'capthird': '21 + 66 = 87'}
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
BEATS=tuple(Beat(x[0],int(x[1]),x[2],tuple(x[3:6]),x[6],x[7],x[8],float(x[9]))
   for x in json.loads((ROOT/'comb08_beats.json').read_text(encoding='utf-8')))

def all_captain_teams():
    return tuple((team,lead) for team in combinations('ABCDEFGH',3) for lead in team)

def advanced_teams():
    return tuple((team,lead) for team,lead in all_captain_teams()
                 if ('A' in team or 'B' in team) and lead!='A')

def even_numbers():
    return tuple(100*a+10*b+c for a,b,c in permutations(range(5),3)
                 if a!=0 and c%2==0)

def constrained_roles():
    return tuple(q for q in permutations('ABCDEFG',3) if q[0]!='A')

def gender_teams():
    return tuple(q for q in combinations(range(7),3) if any(j>=4 for j in q))

def validate():
    assert len(BEATS)==48
    assert tuple(dict.fromkeys(x.section for x in BEATS))==CHAPTER_IDS
    assert Counter(x.section for x in BEATS)=={x:6 for x in CHAPTER_IDS}
    assert all([b.state for b in BEATS if b.section==sec]==list(range(6)) for sec in CHAPTER_IDS)
    assert len({b.heading for b in BEATS})==48
    assert all(b.formula in FORMULAS or not b.formula for b in BEATS)
    assert all(len(b.narration.split())>=45 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>=960
    assert factorial(6)==720 and perm(6,2)==30 and comb(6,2)==15
    assert comb(8,3)*3==8*comb(7,2)==168
    assert len(constrained_roles())==180
    assert len(gender_teams())==31
    assert sum(sum(j<4 for j in q)==2 for q in gender_teams())==18
    assert len(even_numbers())==30 and len(set(even_numbers()))==30
    assert len(advanced_teams())==87
    assert len(set(advanced_teams()))==87
    assert all('A' in t or 'B' in t for t,_ in advanced_teams())
    assert all(lead!='A' for _,lead in advanced_teams())
    assert 168-60-21==42+45==87
    return True
if __name__=='__main__':
    validate()
    print('COMB08_OK',len(BEATS),sum(x.min_seconds for x in BEATS)+5.2,sum(len(x.narration.split()) for x in BEATS))
