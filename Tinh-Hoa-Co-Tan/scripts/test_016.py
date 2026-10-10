from src.core import Board

fen = "4k4/3a1a3/b3eP3/4P4/9/9/9/9/9/4K4 w"
b = Board.fen(fen)
print("Initial:", b.fen())
b.play('e3', 'e2')
print("After e3e2:", b.fen())
b.play('e0', 'f0')
print("After e0f0:", b.fen())
b.play('e2', 'e1')
print("After e2e1:", b.fen())
