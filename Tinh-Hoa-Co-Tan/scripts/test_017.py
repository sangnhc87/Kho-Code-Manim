from src.core import Board

fen = "4k4/4c4/3P1P3/9/9/9/9/9/9/3K5 w"
b = Board.fen(fen)
b.play('d2', 'd1')
print("After d2d1:", b.as_fen() if hasattr(b, 'as_fen') else "ok")
b.play('e1', 'e8')
b.play('f2', 'f1')
b.play('e8', 'e7')

print("Before final:")
try:
    b.play('d1', 'd0')
    print("d1d0 valid!")
    try:
        b.play('e0', 'e1')
        print("e0e1 valid - NOT MATE")
    except:
        pass
    try:
        b.play('e0', 'd0')
        print("e0d0 valid - NOT MATE")
    except:
        pass
    try:
        b.play('e0', 'f0')
        print("e0f0 valid - NOT MATE")
    except:
        pass
except Exception as e:
    print("Error:", e)

