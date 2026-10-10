#!/usr/bin/env python3
"""Build episode 012: Song Binh Khéo Thắng Song Sĩ (Tốt Nhập Tâm)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at e0. Advisors at d0, f0.
    # Red Pawns at d2, f1. Red King at d7.
    fen = "3aka3/5P3/3P5/9/9/9/9/3K5/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Song Binh khéo thắng Song Sĩ: Thế cờ 'Hai Tốt kẹp cổ' vô cùng kinh điển. Đỏ dùng Tướng khống chế trục dọc và hai Tốt áp sát Cửu cung.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đỏ ở d7 đang ghim chặt cột dọc d. Sĩ Đen d0 không thể ăn Tốt d2 vì bị ghim, trong khi Tướng Đen e0 không có đường lui.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('d2', 'd1')
    beats.append({
        "fen": fen,
        "moves": ["d2d1"],
        "text": "Đỏ đi Binh 6 tiến 1! Nước đi điềm tĩnh tạo thành thế kìm kẹp.",
        "duration": 5.0
    })
    
    b.play('d0', 'e1')
    beats.append({
        "fen": "4ka3/3PaP3/9/9/9/9/9/3K5/9/9 b",
        "moves": ["d0e1"],
        "text": "Tướng Đen không thể sang e1 do Tốt f1 khống chế, đành phải lên Sĩ (Sĩ 6 tiến 5).",
        "duration": 5.0
    })
    
    b.play('d1', 'd0')
    beats.append({
        "fen": "3Pka3/4aP3/9/9/9/9/9/3K5/9/9 w",
        "moves": ["d1d0"],
        "text": "Binh 6 tiến 1! Tốt lọt xuống đáy chiếu Tướng.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "3Pka3/4aP3/9/9/9/9/9/3K5/9/9 b",
        "text": "Tướng Đen không thể ăn Tốt d0 vì có mặt Tướng Đỏ bảo kê. Không thể nhúc nhích. Đỏ thắng tuyệt đẹp!",
        "duration": 7.0
    })
    
    episode = {
        "title": "Tập 012: Song Binh Khéo Thắng Song Sĩ",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0012.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
