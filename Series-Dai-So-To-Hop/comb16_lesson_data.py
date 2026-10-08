"""COMB16: splitting labeled/unlabeled teams and assigning group roles."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from math import comb, factorial
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
CHAPTERS=json.loads((ROOT/'comb16_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS={x[0]:x[1] for x in CHAPTERS}
FORMULAS=json.loads((ROOT/'comb16_formulas.json').read_text(encoding='utf-8'))
DATA=json.loads((ROOT/'comb16_beats.json').read_text(encoding='utf-8'))
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
BEATS=tuple(Beat(x['section'],x['state'],x['heading'],tuple(x['lines']),
                 x['takeaway'],x['narration'],x['formula'],x['min_seconds']) for x in DATA)

def partitions_of_size(people,parts):
    """Enumerate unordered partitions respecting the exact multiset of sizes."""
    people=tuple(people)
    sizes=tuple(parts)
    assert sum(sizes)==len(people)
    def rec(remaining,slots):
        if not slots:
            if not remaining:yield ()
            return
        s=slots[0]
        for subset in combinations(remaining,s):
            rest=tuple(x for x in remaining if x not in subset)
            for tail in rec(rest,slots[1:]):
                # canonical sorting removes permutations of equal-sized groups
                pack=(tuple(subset),)+tail
                if tuple(sorted((size,g) for size,g in zip(sizes,pack)))!=tuple((size,g) for size,g in zip(sizes,pack)):
                    continue
                yield pack
    return tuple(rec(people,sizes))

def three_triplets():
    """Generate the 280 partitions into unordered triples by anchoring smallest remaining label."""
    persons=tuple('ABCDEFGHI')
    output=[]
    for b in combinations(persons[1:],2):
        g1=('A',)+b
        leftover=tuple(x for x in persons if x not in g1)
        first=leftover[0]
        for extra in combinations(leftover[1:],2):
            g2=(first,)+extra
            g3=tuple(x for x in leftover if x not in g2)
            output.append((g1,g2,g3))
    assert len(output)==280
    return tuple(output)

def math_counts():
    pairs6=partitions_of_size('ABCDEF',(2,2,2))
    pairs8=partitions_of_size('ABCDEFGH',(2,2,2,2))
    equal4=partitions_of_size('ABCDEFGH',(4,4))
    three=three_triplets()
    same4=sum(any('A' in g and 'B' in g for g in p) for p in equal4)
    different4=len(equal4)-same4
    same3=sum(any('A' in g and 'B' in g for g in p) for p in three)
    other3=len(three)-same3
    return dict(labeled_3_5=comb(8,3),labeled_4_4=comb(8,4),unlabeled_4_4=len(equal4),
                unlabeled_3_5=comb(8,3),labeled_triplets=comb(9,3)*comb(6,3),
                unlabeled_triplets=len(three),pairs_six=len(pairs6),pairs_eight=len(pairs8),
                choose_six_pair=comb(9,6)*len(pairs6),leader_3_5=comb(8,3)*3,
                three_leaders=len(three)*27,same_four=same4,different_four=different4,
                same_triplets=same3,different_triplets=other3,capstone=other3*27)

def validate():
    assert len(BEATS)==48 and len(CHAPTERS)==8 and len(FORMULAS)==48
    assert Counter(b.section for b in BEATS)=={c[0]:6 for c in CHAPTERS}
    assert [b.state for b in BEATS]==list(range(6))*8
    assert all(b.formula in FORMULAS and len(b.lines)==3 for b in BEATS)
    assert all(len(b.narration.split())>=45 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>=1150
    expected=dict(labeled_3_5=56,labeled_4_4=70,unlabeled_4_4=35,unlabeled_3_5=56,
                  labeled_triplets=1680,unlabeled_triplets=280,pairs_six=15,pairs_eight=105,
                  choose_six_pair=1260,leader_3_5=168,three_leaders=7560,
                  same_four=15,different_four=20,same_triplets=70,different_triplets=210,capstone=5670)
    assert math_counts()==expected,(math_counts(),expected)
    return True
if __name__=='__main__':
    validate()
    print('COMB16_VALID 48 beats, 8 chapters, counts:',math_counts())
