"""Translate our top-origin display notation to Pikafish's bottom-origin UCI."""
from src.core import parse_square, sq


def flip_move(move):
    if len(move) != 4:
        raise ValueError('Expected a four-character coordinate move')
    src, dst = parse_square(move[:2]), parse_square(move[2:])
    return sq(src[0], 9-src[1]) + sq(dst[0], 9-dst[1])


def board_fen(board):
    rows = []
    for y in range(10):
        row, blanks = '', 0
        for x in range(9):
            piece = board.cells.get((x, y))
            if piece:
                if blanks:
                    row += str(blanks)
                    blanks = 0
                row += piece
            else:
                blanks += 1
        if blanks:
            row += str(blanks)
        rows.append(row)
    return '/'.join(rows) + (' w' if board.turn == 'red' else ' b') + ' - - 0 1'
