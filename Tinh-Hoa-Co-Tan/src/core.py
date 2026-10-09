"""Small Xiangqi position validator. Coordinates: a0 top-left black side, i9 bottom-right red side."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path

RED = 'KABENRCP'  # uppercase red, lowercase black
VALID = set('KABENRCPkabenrcp') | set('Hh')
HORSE = 'NnHh'


def parse_square(square):
    if len(square) != 2 or square[0] not in 'abcdefghi' or square[1] not in '0123456789':
        raise ValueError(f'Invalid square {square!r}; expected a0..i9')
    return ord(square[0]) - 97, int(square[1])


def sq(x, y):
    return chr(97+x) + str(y)


def who(piece):
    return 'red' if piece.isupper() else 'black'


@dataclass
class Board:
    cells: dict
    turn: str = 'red'

    @classmethod
    def fen(cls, fen):
        parts = fen.strip().split()
        rows = parts[0].split('/')
        if len(rows) != 10:
            raise ValueError('Xiangqi FEN requires 10 ranks')
        cells = {}
        for y, row in enumerate(rows):
            x = 0
            for ch in row:
                if ch.isdigit():
                    x += int(ch)
                elif ch in VALID:
                    if x > 8: raise ValueError('Rank overflow')
                    cells[(x,y)] = ch
                    x += 1
                else:
                    raise ValueError(f'Unrecognized FEN piece: {ch}')
            if x != 9:
                raise ValueError(f'FEN rank {y} width {x}, expected 9')
        if sum(v == 'K' for v in cells.values()) != 1 or sum(v == 'k' for v in cells.values()) != 1:
            raise ValueError('Exactly one general per side required')
        turn = ('red' if len(parts) < 2 or parts[1] in ('w','r') else 'black' if parts[1] in ('b',) else None)
        if turn is None: raise ValueError('Side to move should be w or b')
        b = cls(cells, turn)
        for (x,y), p in cells.items():
            if p in 'KkAa' and not b.palace(x,y,who(p)):
                raise ValueError(f'General/advisor outside palace at {sq(x,y)}')
            if p in 'BbEe' and (y < 5 if p.isupper() else y > 4):
                raise ValueError('Elephant crossed the river')
        if b.facing_generals():
            raise ValueError('Illegal FEN: facing generals')
        return b

    def palace(self,x,y,side):
        return 3 <= x <= 5 and (7 <= y <= 9 if side == 'red' else 0 <= y <= 2)

    def facing_generals(self):
        red = next((p for p,v in self.cells.items() if v == 'K'),None)
        black = next((p for p,v in self.cells.items() if v == 'k'),None)
        if red is None or black is None: return False
        if red[0] != black[0]: return False
        return not any((red[0], y) in self.cells for y in range(min(red[1],black[1])+1,max(red[1],black[1])))

    def path_clear(self, src,dst):
        x,y = src; a,b = dst
        if x == a:
            return sum((x,j) in self.cells for j in range(min(y,b)+1,max(y,b)))
        if y == b:
            return sum((j,y) in self.cells for j in range(min(x,a)+1,max(x,a)))
        return None

    def attacks(self,src,dst):
        x,y=src; a,b=dst
        if src == dst or src not in self.cells: return False
        p=self.cells[src]; u=p.upper(); dx=a-x; dy=b-y
        side=who(p)
        if u=='K':
            return (abs(dx)+abs(dy)==1 and self.palace(a,b,side)) or (dx==0 and self.cells.get(dst)=='k' if p=='K' else dx==0 and self.cells.get(dst)=='K') and self.path_clear(src,dst)==0
        if u=='A': return abs(dx)==abs(dy)==1 and self.palace(a,b,side)
        if u in ('B','E'): return abs(dx)==2 and abs(dy)==2 and (b>=5 if side=='red' else b<=4) and (x+dx//2,y+dy//2) not in self.cells
        if u in ('N','H'):
            if sorted((abs(dx),abs(dy))) != [1,2]: return False
            leg = (x+(1 if dx>0 else -1),y) if abs(dx)==2 else (x,y+(1 if dy>0 else -1))
            return leg not in self.cells
        if u=='R': return self.path_clear(src,dst)==0
        if u=='C':
            blockers=self.path_clear(src,dst)
            return blockers is not None and blockers == (1 if dst in self.cells else 0)
        if u=='P':
            forward=-1 if side=='red' else 1
            crossed=(y<=4 if side=='red' else y>=5)
            return (dx==0 and dy==forward) or (crossed and abs(dx)==1 and dy==0)
        return False

    def in_check(self,side):
        king = next((pos for pos,p in self.cells.items() if p==('K' if side=='red' else 'k')),None)
        if king is None: return True
        if self.facing_generals(): return True
        return any(who(p)!=side and self.attacks(pos,king) for pos,p in self.cells.items())

    def play(self, src_name,dst_name):
        src,dst=parse_square(src_name),parse_square(dst_name)
        piece=self.cells.get(src)
        if not piece: raise ValueError(f'No piece at {src_name}')
        if who(piece)!=self.turn: raise ValueError(f'Wrong side on {src_name}: {self.turn} to play')
        captured=self.cells.get(dst)
        if captured and who(piece)==who(captured): raise ValueError('Cannot capture friendly piece')
        if captured and captured.upper()=='K': raise ValueError('Capturing general not allowed')
        if not self.attacks(src,dst): raise ValueError(f'Illegal move {src_name}{dst_name} ({piece})')
        self.cells[dst]=self.cells.pop(src)
        if self.in_check(self.turn):
            self.cells[src]=self.cells.pop(dst)
            if captured: self.cells[dst]=captured
            raise ValueError(f'Move {src_name}{dst_name} leaves general in check or facing')
        self.turn='black' if self.turn=='red' else 'red'
        return captured


def read_episode(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    validate_episode(data)
    return data


def validate_episode(data):
    for key in ('id','title','fen','beats'):
        if not data.get(key): raise ValueError(f'Missing episode field {key}')
    beats=data['beats']
    if not isinstance(beats,list) or len(beats)<2: raise ValueError('Need at least 2 beats')
    b=Board.fen(data['fen'])
    for idx,beat in enumerate(beats,1):
        # Chapters can return to the original position or start any legal branch.
        if 'fen' in beat:
            b=Board.fen(beat['fen'])
        for key in ('label','headline','narration','insight'):
            if not beat.get(key): raise ValueError(f'Beat {idx}: missing {key}')
        for move in beat.get('moves',[]):
            if len(move)!=4:
                raise ValueError(f'Beat {idx}: move must be coordinate string b7d8')
            b.play(move[:2],move[2:])
    return True
