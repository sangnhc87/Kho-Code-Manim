#!/usr/bin/env python3
"""Build episode 011: Đơn Binh Khéo Thắng Đơn Sĩ (Tốt Lấn Cung)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at d1, Advisor at d2.
    # Red Pawn at e2, Red King at d7.
    fen = "9/3k5/3aP4/9/9/9/9/3K5/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Đơn Binh khéo thắng Đơn Sĩ: Một thế cờ tàn cơ bản trong loạt bài Tàn Binh. Một Tốt bình thường hòa một Sĩ, nhưng ở hình cờ này Đỏ có thủ đoạn đặc biệt.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tốt Đỏ đã lấn sâu vào Cửu cung (e2). Tướng Đỏ (d7) đang ghim chặt Sĩ Đen (d2) khiến Sĩ không thể nhúc nhích.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('d7', 'd8')
    beats.append({
        "fen": fen,
        "moves": ["d7d8"],
        "text": "Đỏ đi Tướng 6 tiến 1! Đòn chờ kinh điển.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "9/3k5/3aP4/9/9/9/9/9/3K5/9 b",
        "text": "Tướng Đen không thể sang e1 do Tốt Đỏ kiểm soát, Sĩ Đen lại bị ghim. Đen buộc phải thoái Tướng.",
        "duration": 5.0
    })
    
    b.play('d1', 'd0')
    beats.append({
        "fen": "9/3k5/3aP4/9/9/9/9/9/3K5/9 b",
        "moves": ["d1d0"],
        "text": "Tướng Đen thoái xuống d0 (Tướng 4 thoái 1).",
        "duration": 5.0
    })
    
    b.play('e2', 'e1')
    beats.append({
        "fen": "3k5/9/3aP4/9/9/9/9/9/3K5/9 w",
        "moves": ["e2e1"],
        "text": "Binh 5 tiến 1! Tốt lấn cung áp sát.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "3k5/4P4/3a5/9/9/9/9/9/3K5/9 b",
        "text": "Tốt Đỏ khống chế cả e0 và d1. Sĩ Đen d2 muốn ăn Tốt e1 nhưng không dám vì lộ mặt Tướng. Đen hết nước đi (Bí tử). Đỏ thắng!",
        "duration": 7.0
    })
    
    episode = {
        "title": "Tập 0011: Đơn Binh Khéo Thắng Đơn Sĩ (Tốt Lấn Cung)",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-011.json" # using tap-011.json
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
