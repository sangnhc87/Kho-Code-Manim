"""Exact retrograde calculation for K+R+A vs k+A+A, objective: capture a Black Advisor.
"""
import collections
from collections import deque
from itertools import combinations
from src.core import Board, sq

R_PALACE = tuple((x,y) for x in range(3,6) for y in range(7,10))
B_PALACE = tuple((x,y) for x in range(3,6) for y in range(0,3))
R_ADV = ((4,8),(3,7),(5,7),(3,9),(5,9))
B_ADV = ((4,1),(3,0),(5,0),(3,2),(5,2))
SQUARES = tuple((x,y) for y in range(10) for x in range(9))

def fen_of(K, R, A, k, advs, side):
    cells = {K: 'K', R: 'R', A: 'A', k: 'k'}
    for p in advs: cells[p] = 'a'
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
    K, R, A, k, advs, turn = state
    cells = {K: 'K', R: 'R', A: 'A', k: 'k'}
    for p in advs: cells[p] = 'a'
    side = 'red' if turn == 0 else 'black'
    bd = Board(cells, side)
    for start, p in tuple(bd.cells.items()):
        if (p.isupper()) != (turn == 0): continue
        for dst in SQUARES:
            if dst in bd.cells and bd.cells[dst].isupper() == p.isupper(): continue
            if not bd.attacks(start, dst): continue
            captured = bd.cells.get(dst)
            if captured and captured.upper() == 'K': continue
            bd.cells.pop(start)
            bd.cells[dst] = p
            invalid = bd.in_check(side)
            bd.cells.pop(dst)
            bd.cells[start] = p
            if captured: bd.cells[dst] = captured
            if invalid: continue
            move = sq(*start) + sq(*dst)
            if captured:
                yield move, ('CAPTURE_A' if captured == 'a' else 'CAPTURE_N')
                continue
            nK, nR, nA, nk, nadvs = K, R, A, k, advs
            if p == 'K': nK = dst
            elif p == 'R': nR = dst
            elif p == 'A': nA = dst
            elif p == 'k': nk = dst
            else: nadvs = tuple(sorted(dst if q == start else q for q in advs))
            yield move, (nK, nR, nA, nk, nadvs, 1 - turn)

def all_states():
    states = []
    for K in R_PALACE:
        for A in R_ADV:
            if A == K: continue
            for k in B_PALACE:
                for R in SQUARES:
                    if R in (K, A, k): continue
                    for advs in combinations(B_ADV, 2):
                        if any(p in (K, R, A, k) for p in advs): continue
                        cells = {K: 'K', R: 'R', A: 'A', k: 'k', advs[0]: 'a', advs[1]: 'a'}
                        for turn in (0, 1):
                            bd = Board(cells, 'red' if turn == 0 else 'black')
                            if bd.facing_generals(): break
                            if bd.in_check('black' if turn == 0 else 'red'): continue
                            states.append((K, R, A, k, advs, turn))
    return states

def solve():
    states = all_states()
    index = {s: i for i, s in enumerate(states)}
    parents = [[] for _ in states]
    degree = [0] * len(states)
    result = [0] * len(states)
    depth = [0] * len(states)
    q = deque()
    for i, s in enumerate(states):
        for mv, nxt in legal_moves(s):
            if nxt == 'CAPTURE_A':
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
    import time
    t0 = time.time()
    print('Solving K+R+A vs k+A+A...', flush=True)
    ss, idx, res, d = solve()
    print('STATES:', len(ss), 'WDL:', dict(collections.Counter(res)), 'max depth:', max(d), f'time {time.time()-t0:.0f}s', flush=True)
    rows = []
    for s in ss:
        if s[-1] != 0: continue
        i = idx[s]
        if res[i] != 1: continue
        opts = []
        for move, n in legal_moves(s):
            if n in idx: opts.append((move, res[idx[n]], d[idx[n]]))
            elif n == 'CAPTURE_A': opts.append((move, -1, 0))
            else: opts.append((move, 0, 0))
        wins = [o for o in opts if o[1] == -1]
        bad = [o for o in opts if o[1] != -1]
        if wins and bad:
            rows.append((d[i], s, min(wins, key=lambda x: x[2]), len(wins), bad[0]))
    rows.sort(key=lambda r: r[0])
    print('CANDIDATES:', len(rows))
    for dd, s, best, nw, bad in rows[:15]:
        print(fen_of(*s), 'depth:', dd, 'best:', best, 'win-moves:', nw, 'trap:', bad)
