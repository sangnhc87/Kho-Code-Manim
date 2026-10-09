"""Exact retrograde solver for King + Pawn vs King (K+P vs k).
Objective: Checkmate or Stalemate under ordinary legal moves.
"""
from collections import deque
from src.core import Board, sq

R_PALACE = tuple((x, y) for x in range(3, 6) for y in range(7, 10))
B_PALACE = tuple((x, y) for x in range(3, 6) for y in range(0, 3))
SQUARES = tuple((x, y) for y in range(10) for x in range(9))


def fen_of(k, K, p, side):
    cells = {k: 'k', K: 'K', p: 'P'}
    ranks = []
    for y in range(10):
        run = 0
        rank = ''
        for x in range(9):
            piece = cells.get((x, y))
            if piece:
                if run:
                    rank += str(run)
                    run = 0
                rank += piece
            else:
                run += 1
        if run:
            rank += str(run)
        ranks.append(rank)
    return '/'.join(ranks) + ' ' + ('w' if side == 0 else 'b')


def legal_moves(state):
    k, K, p, turn = state
    side = 'red' if turn == 0 else 'black'
    b = Board({k: 'k', K: 'K', p: 'P'}, side)
    for start, piece in tuple(b.cells.items()):
        if (piece.isupper()) != (turn == 0):
            continue
        for dst in SQUARES:
            if dst in b.cells and b.cells[dst].isupper() == piece.isupper():
                continue
            if not b.attacks(start, dst):
                continue
            captured = b.cells.get(dst)
            if captured and captured.upper() == 'K':
                continue
            b.cells.pop(start)
            b.cells[dst] = piece
            invalid = b.in_check(side)
            b.cells.pop(dst)
            b.cells[start] = piece
            if captured:
                b.cells[dst] = captured
            if invalid:
                continue

            move = sq(*start) + sq(*dst)
            if captured:
                yield move, 'DRAW_CAPTURED'
            else:
                nk, nK, np = k, K, p
                if piece == 'k':
                    nk = dst
                elif piece == 'K':
                    nK = dst
                elif piece == 'P':
                    np = dst
                yield move, (nk, nK, np, 1 - turn)


def solve():
    states = []
    for k in B_PALACE:
        for K in R_PALACE:
            for p in SQUARES:
                if p in (k, K):
                    continue
                for turn in (0, 1):
                    b = Board({k: 'k', K: 'K', p: 'P'}, 'red' if turn == 0 else 'black')
                    if b.facing_generals():
                        continue
                    if b.in_check('black' if turn == 0 else 'red'):
                        continue
                    states.append((k, K, p, turn))

    index = {s: i for i, s in enumerate(states)}
    parents = [[] for _ in states]
    degree = [0] * len(states)
    result = [0] * len(states)
    depth = [0] * len(states)
    best_move = {}

    q = deque()
    for i, s in enumerate(states):
        moves = list(legal_moves(s))
        degree[i] = len(moves)
        if s[3] == 1 and degree[i] == 0:
            result[i] = 1
            depth[i] = 0
            q.append(i)
        elif s[3] == 0 and degree[i] == 0:
            result[i] = -1
            depth[i] = 0
            q.append(i)
        else:
            for mv, nxt in moves:
                if nxt != 'DRAW_CAPTURED' and nxt in index:
                    parents[index[nxt]].append((i, mv))

    while q:
        j = q.popleft()
        r_j = result[j]
        d_j = depth[j]
        for i, mv in parents[j]:
            if result[i] != 0:
                continue
            turn_i = states[i][3]
            if turn_i == 0 and r_j == 1:
                result[i] = 1
                depth[i] = d_j + 1
                best_move[i] = mv
                q.append(i)
            elif turn_i == 1 and r_j == 1:
                degree[i] -= 1
                if degree[i] == 0:
                    result[i] = 1
                    depth[i] = d_j + 1
                    q.append(i)

    return states, index, result, depth, best_move
