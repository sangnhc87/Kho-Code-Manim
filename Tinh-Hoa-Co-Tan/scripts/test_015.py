from src.core import Board

# Đơn Binh Thắng Đơn Tượng
# Black King at d0. Black Elephant at c0.
# Red Pawn at c1. Red King at e9.
# Row 0: 2 empty (a, b), c0=Elephant (b), d0=King (k), 5 empty (e,f,g,h,i). So `2bk5`
# Row 1: 2 empty (a,b), c1=Pawn (P), 6 empty. So `2P6`
# Row 2..8: 9
# Row 9: 4 empty (a,b,c,d), e9=King (K), 4 empty. So `4K4`
fen = "2bk5/2P6/9/9/9/9/9/9/9/4K4 w"
try:
    b = Board.fen(fen)
    print("FEN is valid")
except Exception as e:
    print(f"FEN error: {e}")

# Try a sequence of moves
moves = [
    ('c1', 'c0'), # Red Pawn captures Elephant
]
for src, dst in moves:
    print(f"Playing {src}{dst}")
    b.play(src, dst)
    print(b.fen())
