#!/usr/bin/env python3
"""Build episode 009: Mã Thắng Đơn Sĩ (Bí tử)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Red King at d7, Knight at g0.
    # Black King at d1, Advisor at d2.
    fen = "6N2/3k5/3a5/9/9/9/9/3K5/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Mã thắng Đơn Sĩ: Một thế cờ tàn điền hình. Mã không thể chiếu bí, nhưng có thể dồn Tướng địch vào thế bí tử (hết nước đi).",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đen ở d1 không thể sang e1 vì Mã Đỏ ở g0 đang nhòm ngó. Sĩ Đen ở d2 cũng bị Tướng Đỏ ghim không thể nhúc nhích.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Đỏ chỉ cần đi một nước chờ để ép Đen tự chui vào góc chết.",
        "duration": 5.0
    })
    
    # Lời giải
    b.play('d7', 'd8')
    beats.append({
        "fen": fen,
        "moves": ["d7d8"],
        "text": "Tướng 6 tiến 1! Nước đi chờ đợi xuất sắc.",
        "duration": 5.0
    })
    
    b.play('d1', 'd0')
    beats.append({
        "fen": "6N2/3k5/3a5/9/9/9/9/9/3K5/9 b",
        "moves": ["d1d0"],
        "text": "Đen hết cách, buộc phải thoái Tướng xuống d0 (Tướng 4 thoái 1).",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "3k2N2/9/3a5/9/9/9/9/9/3K5/9 w",
        "moves": ["g0f2"],
        "text": "Mã 3 tiến 4! Giáng đòn quyết định.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "3k5/9/3a1N3/9/9/9/9/9/3K5/9 b",
        "text": "Mã Đỏ khống chế cả d1 và e0. Sĩ Đen d2 bị ghim. Tướng Đen hết nước đi (Bí tử). Đỏ thắng!",
        "duration": 6.0
    })
    
    episode = {
        "title": "Tập 0009: Mã Thắng Đơn Sĩ (Bí Tử)",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0009.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
