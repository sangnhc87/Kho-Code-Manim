#!/usr/bin/env python3
"""Build episode 008: Pháo Song Sĩ phá Song Sĩ
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at d0, Advisors at f0, f2. (e1 is empty!)
    # Red King at e7. Red Advisor at d7, e8.
    # Red Cannon at b8.
    # Wait, e8 is an Advisor. So Rank 8: 1C2A4 (b8=C, e8=A)
    # Rank 7: 3AK4 (d7=A, e7=K)
    fen = "3k1a3/9/5a3/9/9/9/9/3AK4/1C2A4/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Pháo Song Sĩ phá Song Sĩ: Một thế cờ tàn nghệ thuật. Tướng đỏ chiếm trung lộ, ép Sĩ đen phải phân tán.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Lúc này Sĩ đen đã lệch (một con ở f2, một con ở f0), trung lộ (cột e) hoàn toàn trống trải.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đỏ ở e7 khống chế toàn bộ cột trung tâm, khiến Tướng Đen không thể bình ra.",
        "duration": 5.0
    })
    
    # Lời giải
    beats.append({
        "fen": fen,
        "moves": ["b8d8"],
        "text": "Đỏ đi Pháo 8 bình 6! Lợi dụng Sĩ Đỏ làm ngòi, giáng đòn sát cục tuyệt đẹp.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": "3k1a3/9/5a3/9/9/9/9/3AK4/3CA4/9 b",
        "text": "Tướng Đen bị kẹt cứng, Sĩ Đen không thể che đỡ. Đỏ thắng tuyệt đối!",
        "duration": 5.0
    })
    
    episode = {
        "title": "Tập 0008: Pháo Song Sĩ Phá Song Sĩ",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0008.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
