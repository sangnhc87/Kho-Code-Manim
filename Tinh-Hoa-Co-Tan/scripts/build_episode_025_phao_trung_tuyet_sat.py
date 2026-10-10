#!/usr/bin/env python3
"""Build episode 025: Pháo Trùng Tuyệt Sát (Song Pháo)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, f0. Elephants a2, i2.
    fen = "3aka3/1N7/e2RC3e/5CN2/9/9/9/9/9/4K4 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Pháo Trùng Tuyệt Sát: Một sát cục hoàn mỹ kết hợp sức mạnh của Song Pháo và sự yểm trợ tinh tế của Song Mã.",
        "duration": 7.0
    })
    
    # Lời giải: Xe ăn Sĩ
    b.play('d2', 'd0')
    beats.append({
        "fen": "3Rka3/1N7/e3C3e/5CN2/9/9/9/9/9/4K4 b",
        "moves": ["d2d0"],
        "text": "Xe 4 tiến 2! Chém gãy Sĩ góc chiếu Tướng. Xe được Mã b1 bảo vệ nên Tướng Đen không thể ăn, buộc phải thượng lên lầu 2.",
        "duration": 7.0
    })
    
    # Đen chạy Tướng
    b.play('e0', 'e1')
    beats.append({
        "fen": "3R1a3/1N2k4/e3C3e/5CN2/9/9/9/9/9/4K4 w",
        "moves": ["e0e1"],
        "text": "Tướng 5 tiến 1 (e0-e1).",
        "duration": 4.0
    })
    
    # Sát cục: Pháo Trùng
    b.play('f3', 'e3')
    beats.append({
        "fen": "3R1a3/1N2k4/e3C3e/4C1N2/9/9/9/9/9/4K4 b",
        "moves": ["f3e3"],
        "text": "Pháo 4 bình 5! Thiết lập thế 'Pháo Trùng' sát cục. Tướng Đen không thể ăn Pháo e2 vì Mã g3 đã phục sẵn bảo vệ. Đỏ thắng tuyệt đối!",
        "duration": 8.0
    })
    
    episode = {
        "id": "tap-0025",
        "title": "Tập 025: Pháo Trùng Tuyệt Sát",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0025.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
