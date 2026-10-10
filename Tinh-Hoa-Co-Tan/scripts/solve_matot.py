"""Exact retrograde calculation for K+N vs k+p (Pawn) capture-Pawn objective.
"""
from collections import deque
from src.core import Board, sq

R_KING = tuple((x,y) for x in range(3,6) for y in range(7,10))
B_KING = tuple((x,y) for x in range(3,6) for y in range(0,3))
# Black pawns across river: y in 4..9 (or 5..9)
PAWN_SQUARES = tuple((x,y) for y in range(3,10) for x in range(9))
SQUARES = tuple((x,y) for y in range(10) for x in range(9))

def fen_of(k, K, n, p, side):
    cells = {k: 'k', K: 'K', n: 'N', p: 'p'}
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
    k, K, n, p, turn = state
    bd = Board({k: 'k', K: 'K', n: 'N', p: 'p'}, 'red' if turn == 0 else 'black')
    for start, pc in tuple(bd.cells.items()):
        if (pc.isupper()) != (turn == 0): continue
        for dst in SQUARES:
            if dst in bd.cells and bd.cells[dst].isupper() == pc.isupper(): continue
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
                yield move, ('CAPTURE_P' if captured == 'p' else 'CAPTURE_N')
            else:
                updated = {'k': k, 'K': K, 'N': n, 'p': p}
                updated[pc] = dst
                yield move, (updated['k'], updated['K'], updated['N'], updated['p'], 1 - turn)

def solve():
    states = []
    for k in B_KING:
        for K in R_KING:
            for p in PAWN_SQUARES:
                if p in (k, K): continue
                for n in SQUARES:
                    if n in (k, K, p): continue
                    bd = Board({k: 'k', K: 'K', n: 'N', p: 'p'})
                    if bd.facing_generals(): continue
                    for turn in (0, 1):
                        if bd.in_check('black' if turn == 0 else 'red'): continue
                        states.append((k, K, n, p, turn))
    index = {s: i for i, s in enumerate(states)}
    parents = [[] for _ in states]
    degree = [0] * len(states)
    result = [0] * len(states)
    depth = [0] * len(states)
    q = deque()
    for i, s in enumerate(states):
        for mv, nxt in legal_moves(s):
            if nxt == 'CAPTURE_P':
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
    print('Solving K+N vs k+p...')
    ss, idx, res, d = solve()
    print('STATES:', len(ss), 'WDL:', dict(collections.Counter(res)), 'max depth:', max(d))
    starts = []
    for s in ss:
        if s[-1] != 0: continue
        i = idx[s]
        # Look for positions where depth is between 7 and 17 (3-8 moves each side)
        # and pawn is across river (y >= 5) or on river bank (y=4)
        k, K, n, p, turn = s
        if p[1] < 4: continue
        if res[i] != 1 or not (7 <= d[i] <= 19): continue
        opts = []
        for move, nxt in legal_moves(s):
            if nxt in idx: opts.append((move, res[idx[nxt]], d[idx[nxt]]))
            elif nxt == 'CAPTURE_P': opts.append((move, -1, 0))
            else: opts.append((move, 0, 0))
        wins = [o for o in opts if o[1] == -1]
        bad = [o for o in opts if o[1] == 0]
        if wins and bad:
            starts.append((s, d[i], min(wins, key=lambda x: x[2]), bad[0], len(wins)))
    print('CANDIDATES:', len(starts))
    # Sort candidates by depth descending
    starts.sort(key=lambda x: x[1], reverse=True)
    for x in starts[:15]:
        print(fen_of(*x[0]), 'depth:', x[1], 'best:', x[2], 'draw:', x[3], 'win-moves:', x[4])
