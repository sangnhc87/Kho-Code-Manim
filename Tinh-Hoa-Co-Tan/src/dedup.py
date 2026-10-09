"""Xiangqi position canonicalization and deduplication.
Eliminates duplicates due to horizontal symmetry (left-right mirror) and transposition.
"""
from src.core import Board, sq, parse_square

FILES = 'abcdefghi'


def mirror_square(square_name):
    """Mirror square across central column (file e / index 4): x' = 8 - x, y' = y."""
    x, y = parse_square(square_name)
    return sq(8 - x, y)


def mirror_fen(fen):
    """Reflect entire FEN across central vertical axis (x -> 8-x)."""
    parts = fen.strip().split()
    ranks = parts[0].split('/')
    mirrored_ranks = []
    for rank in ranks:
        # Expand rank to full 9 characters
        expanded = []
        for ch in rank:
            if ch.isdigit():
                expanded.extend(['.'] * int(ch))
            else:
                expanded.append(ch)
        # Reverse horizontally
        rev = expanded[::-1]
        # Compress back to FEN run-length format
        compact = []
        blanks = 0
        for ch in rev:
            if ch == '.':
                blanks += 1
            else:
                if blanks > 0:
                    compact.append(str(blanks))
                    blanks = 0
                compact.append(ch)
        if blanks > 0:
            compact.append(str(blanks))
        mirrored_ranks.append(''.join(compact))
    
    turn = parts[1] if len(parts) > 1 else 'w'
    return '/'.join(mirrored_ranks) + ' ' + turn


def canonical_fen(fen):
    """Return the lexicographically minimal representation between the position and its mirror.
    This guarantees that symmetric positions (e.g. left vs right wing) are treated as identical.
    """
    m_fen = mirror_fen(fen)
    return min(fen.strip(), m_fen.strip())


def material_signature(fen):
    """Return normalized material key for taxonomy categorization, e.g. 'RED_KN_vs_BLK_kb'."""
    board_part = fen.strip().split()[0]
    red_pieces = []
    black_pieces = []
    for ch in board_part:
        if ch.isalpha():
            if ch.isupper():
                red_pieces.append(ch)
            else:
                black_pieces.append(ch)
    red_key = ''.join(sorted(red_pieces))
    black_key = ''.join(sorted(black_pieces))
    return f'RED_{red_key}_vs_BLK_{black_key}'
