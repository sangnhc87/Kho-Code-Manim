"""Exact retrograde calculation for K+N vs k+b (Elephant) capture-Elephant objective.
"""
from collections import deque
from src.core import Board, sq

ELEPHANT = ((2,0), (6,0), (0,2), (4,2), (8,2), (2,4), (6,4))
R_KING = tuple((x,y) for x in range(3,6) for y in range(7,10))
B_KING = tuple((x,y) for x in range(3,6) for y in range(0,3))
SQUARES = tuple((x,y) for y in range(10) for x in range(9))

def fen_of(k, K, n, b, side):
    cells = {k: 'k', K: 'K', n: 'N', b: 'b'}
    ranks = []
    for y in range(10):
        run = 0; rank = ''
        for x in range(9):
            piece = cells.get((x,y))
            if piece:
                if run: rank += str(run); run = 0
                rank += piece
            else: run += 1
        if run: rank += str(run)
        ranks.append(rank)
    return '/'.join(ranks) + ' ' + ('w' if side == 0 else 'b')

def legal_moves(state):
    k, K, n, el, turn = state
    bd = Board({k: 'k', K: 'K', n: 'N', el: 'b'}, 'red' if turn == 0 else 'black')
    for start, p in tuple(bd.cells.items()):
        if (p.isupper()) != (turn == 0): continue
        for dst in SQUARES:
            if dst in bd.cells and bd.cells[dst].isupper() == p.isupper(): continue
            if not bd.attacks(start, dst): continue
            prev = bd.cells.pop(start)
            captured = bd.cells.get(dst)
            if captured and captured.upper() == 'K':
                bd.cells[start] = prev; continue
            bd.cells[dst] = prev
            invalid = bd.in_check(bd.turn)
            bd.cells.pop(dst)
            bd.cells[start] = prev
            if captured: bd.cells[dst] = captured
            if invalid: continue
            move = sq(*start) + sq(*dst)
            if captured:
                yield move, ('CAPTURE_B' if captured == 'b' else 'CAPTURE_N')
            else:
                updated = {'k': k, 'K': K, 'N': n, 'b': el}
                updated[p] = dst
                yield move, (updated['k'], updated['K'], updated['N'], updated['b'], 1 - turn)

def solve():
    states = []
    for k in B_KING:
        for K in R_KING:
            for el in ELEPHANT:
                for n in SQUARES:
                    if n in (k, K, el): continue
                    bd = Board({k: 'k', K: 'K', n: 'N', el: 'b'})
                    if bd.facing_generals(): continue
                    for turn in (0, 1):
                        if bd.in_check('black' if turn == 0 else 'red'): continue
                        states.append((k, K, n, el, turn))
    index = {s: i for i, s in enumerate(states)}
    parents = [[] for _ in states]
    degree = [0] * len(states)
    result = [0] * len(states)
    depth = [0] * len(states)
    q = deque()
    for i, s in enumerate(states):
        for mv, nxt in legal_moves(s):
            if nxt == 'CAPTURE_B':
                result[i] = 1; depth[i] = 1
            elif nxt == 'CAPTURE_N':
                degree[i] += 1
            elif nxt in index:
                j = index[nxt]; parents[j].append(i); degree[i] += 1
        if result[i] == 1: q.append(i)
        elif degree[i] == 0:
            result[i] = -1; q.append(i)
    while q:
        i = q.popleft()
        for p in parents[i]:
            if result[p]: continue
            if result[i] == -1:
                result[p] = 1; depth[p] = depth[i] + 1; q.append(p)
            else:
                degree[p] -= 1
                depth[p] = max(depth[p], depth[i] + 1)
                if degree[p] == 0:
                    result[p] = -1; q.append(p)
    return states, index, result, depth

if __name__ == '__main__':
    import collections
    print('Solving K+N vs k+b...')
    ss, idx, res, d = solve()
    print('STATES:', len(ss), 'WDL:', dict(collections.Counter(res)), 'max depth:', max(d))
    starts = []
    for s in ss:
        if s[-1] != 0: continue
        i = idx[s]
        if res[i] != 1 or not (7 <= d[i] <= 21): continue
        opts = []
        for move, n in legal_moves(s):
            if n in idx: opts.append((move, res[idx[n]], d[idx[n]]))
            elif n == 'CAPTURE_B': opts.append((move, -1, 0))
            else: opts.append((move, 0, 0))
        wins = [o for o in opts if o[1] == -1]
        bad = [o for o in opts if o[1] == 0]
        if wins and bad:
            starts.append((s, d[i], min(wins, key=lambda x: x[2]), bad[0], len(wins)))
    print('CANDIDATES:', len(starts))
    for x in starts[:10]:
        print(fen_of(*x[0]), 'depth:', x[1], 'best:', x[2], 'draw:', x[3], 'win-moves:', x[4])
