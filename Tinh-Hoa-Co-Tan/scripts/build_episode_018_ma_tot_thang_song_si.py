#!/usr/bin/env python3
"""Build episode 018: Mã Tốt Khéo Thắng Song Sĩ (Mã Khẩu Sát Cục)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at e0. Advisors at d0, e1.
    # Red Pawn at e2. Red Knight at c5. Red King at f7.
    fen = "3ak4/4a4/4P4/9/9/2N6/9/5K3/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Mã Tốt khéo thắng Song Sĩ: Một thế cờ vô cùng sắc sảo. Tốt Đỏ đã nhập tâm (e2) khóa chặt yết hầu e1, Tướng Đỏ chiếm mặt ghim cột f.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đen hoàn toàn hết đường nhúc nhích. Đỏ chỉ cần đưa Mã vào vị trí tung đòn 'Mã Khẩu' là sát cục.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('c5', 'b3')
    beats.append({
        "fen": fen,
        "moves": ["c5b3"],
        "text": "Mã 7 thoái 8! Lùi Mã chuẩn bị mượn đường nhào tới c1.",
        "duration": 5.0
    })
    
    # Đen buộc phải đi Sĩ vì Tướng không thể đi
    b.play('e1', 'f0')
    beats.append({
        "fen": "3ak4/4a4/4P4/1N7/9/9/9/5K3/9/9 b",
        "moves": ["e1f0"],
        "text": "Tướng Đen không thể nhúc nhích. Sĩ Đen buộc phải thoái về (Sĩ 5 thoái 4). Dù lên Sĩ d2 hay f2 kết quả cũng không đổi.",
        "duration": 7.0
    })
    
    b.play('b3', 'c1')
    beats.append({
        "fen": "3aka3/9/4P4/1N7/9/9/9/5K3/9/9 w",
        "moves": ["b3c1"],
        "text": "Mã 8 tiến 7! Đòn Mã Khẩu chí mạng. Tướng Đen bị kẹp giữa Tốt, Mã và Tướng Đỏ, không thể chống đỡ. Đỏ thắng tuyệt đẹp!",
        "duration": 6.0
    })
    
    episode = {
        "title": "Tập 018: Mã Tốt Khéo Thắng Song Sĩ",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0018.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
