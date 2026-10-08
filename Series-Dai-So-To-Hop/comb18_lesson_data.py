"""Mathematical source of truth for COMB18 (no Manim dependency)."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CHAPTERS = json.loads((ROOT/'comb18_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS = dict(CHAPTERS)
FORMULAS = json.loads((ROOT/'comb18_formulas.json').read_text(encoding='utf-8'))
DATA = json.loads((ROOT/'comb18_beats.json').read_text(encoding='utf-8'))

@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str, str, str]
    takeaway: str
    narration: str
    formula: str
    min_seconds: float

BEATS = tuple(Beat(r['section'], r['state'], r['heading'], tuple(r['lines']),
                   r['takeaway'], r['narration'], r['formula'],r['min_seconds']) for r in DATA)


def triangle(n):
    """Build rows by parent additions, not math.comb."""
    rows = [(1,)]
    for _ in range(n):
        old=rows[-1]
        rows.append((1,)+tuple(old[i-1]+old[i] for i in range(1,len(old)))+(1,))
    return tuple(rows)


def select_two_cases(n,k):
    """Independent enumeration: cases with and without distinguished element zero."""
    groups=list(combinations(range(n),k))
    yes=sum(0 in group for group in groups)
    return yes, len(groups)-yes


def hockey_stick(k,n):
    return sum(triangle(r)[r][k] for r in range(k,n+1))


def alternating_sum(n):
    return sum((-1)**k*x for k,x in enumerate(triangle(n)[n]))


def odd_cells(n):
    return {(r,k) for r,row in enumerate(triangle(n)) for k,x in enumerate(row) if x%2}


def vandermonde_splits():
    return tuple(comb(5,i)*comb(3,3-i) for i in range(4))


def validate():
    assert len(BEATS)==48
    assert len(CHAPTERS)==8 and len(FORMULAS)==48
    assert [b.state for b in BEATS] == list(range(6))*8
    assert [sum(b.section==section for b in BEATS) for section,_ in CHAPTERS]==[6]*8
    assert all(b.formula in FORMULAS and len(b.lines)==3 for b in BEATS)
    assert all(len(b.narration.split())>=38 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)+5.2>=1100
    assert triangle(6)[6]==(1,6,15,20,15,6,1)
    assert triangle(8)[8][3]==56
    assert all(triangle(n)[n]==tuple(comb(n,k) for k in range(n+1)) for n in range(14))
    assert select_two_cases(6,3)==(10,10)
    assert hockey_stick(2,5)==20
    assert hockey_stick(3,7)==70
    assert all(alternating_sum(n)==0 for n in range(1,15))
    assert alternating_sum(0)==1
    assert len(odd_cells(8).intersection({(8,k) for k in range(9)}))==2
    assert all((7,k) in odd_cells(8) for k in range(8))
    assert vandermonde_splits()==(1,15,30,10)
    assert sum(vandermonde_splits())==56
    return True

if __name__=='__main__':
    validate()
    print('COMB18_VALID 8 chapters, 48 beats, Pascal recurrence and Vandermonde=56')
