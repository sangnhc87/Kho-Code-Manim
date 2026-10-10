from src.core import Board
fen = "2b1k4/9/3P1P3/9/9/9/9/9/9/5K3 w"
b = Board.fen(fen)
b.play('d2', 'd1')
print("d2d1 played")
b.play('c0', 'a2')
print("c0a2 played")
b.play('f2', 'f1')
print("f2f1 played")
b.play('a2', 'c4')
print("a2c4 played")
b.play('f1', 'e1')
print("f1e1 played (Check!)")

# Verify King cannot move
try:
    b.play('e0', 'd0')
    print("e0d0 valid!")
except Exception as e:
    print("e0d0 error:", e)

try:
    b.play('e0', 'f0')
    print("e0f0 valid!")
except Exception as e:
    print("e0f0 error:", e)
    
try:
    b.play('e0', 'e1')
    print("e0e1 valid!")
except Exception as e:
    print("e0e1 error:", e)
