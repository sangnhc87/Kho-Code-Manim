import sys
from src.core import Board

def get_legal_moves(board):
    moves = []
    # Try all pieces
    for src in list(board.pieces.keys()):
        if board.who(board.pieces[src]) == board.turn:
            for file in 'abcdefghi':
                for rank in '0123456789':
                    dst = file + rank
                    if src != dst:
                        if board.attacks(src, dst):
                            captured = board.pieces.get(dst)
                            if captured and board.who(captured) == board.turn:
                                continue
                            try:
                                b_copy = Board.fen(board.fen())
                                b_copy.play(src, dst)
                                moves.append((src, dst))
                            except ValueError:
                                pass
    return moves

def is_mate(board):
    return len(get_legal_moves(board)) == 0

def find_forced_mate(fen, max_depth, is_red_turn):
    board = Board.fen(fen)
    if is_mate(board):
        return [] if is_red_turn else ["MATE"]
        
    if max_depth == 0:
        return None
        
    legal_moves = get_legal_moves(board)
    
    if is_red_turn:
        # Red wants ANY move to lead to a forced mate
        for src, dst in legal_moves:
            b_copy = Board.fen(board.fen())
            b_copy.play(src, dst)
            path = find_forced_mate(b_copy.fen(), max_depth - 1, False)
            if path is not None:
                return [(src, dst)] + path
        return None
    else:
        # Black wants to PREVENT mate. So ALL Black moves must lead to mate.
        longest_path = None
        for src, dst in legal_moves:
            b_copy = Board.fen(board.fen())
            b_copy.play(src, dst)
            path = find_forced_mate(b_copy.fen(), max_depth - 1, True)
            if path is None:
                return None # Black found an escape!
            if longest_path is None or len(path) > len(longest_path):
                longest_path = [(src, dst)] + path
        return longest_path if longest_path is not None else []

# "Tam Binh Tuyệt Sát Song Sĩ"
# fen = "3aka3/9/3PPP3/9/9/9/9/9/9/4K4 w"
fen = "3aka3/9/3PPP3/9/9/9/9/9/9/4K4 w"
path = find_forced_mate(fen, 3, True)
print("Path for Tam Binh Song Si:", path)

