#!/usr/bin/env python3
"""Build episode 019: Mã Tốt Khéo Thắng Sĩ Tượng Toàn
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at e0. Advisors at d0, e1. Elephants at g2, i2.
    # Red Pawn at e2. Red Knight at c5. Red King at f7.
    fen = "3ak4/4a4/4P1e1e/9/9/2N6/9/5K3/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Mã Tốt khéo thắng Sĩ Tượng Toàn: Dù Đen có đầy đủ phòng ngự, nhưng nếu đội hình vướng víu tự cản đường nhau, Mã Tốt vẫn có thể tạo nên kỳ tích.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tốt Đỏ đã cắm sâu ở e2 khóa chặt cửa sinh e1. Tướng Đỏ chiếm mặt f ghim chặt Tướng Đen. Song Tượng Đen ở xa hoàn toàn vô dụng.",
        "duration": 7.0
    })
    
    # Lời giải
    b.play('c5', 'b3')
    beats.append({
        "fen": fen,
        "moves": ["c5b3"],
        "text": "Mã 7 thoái 8! Nước đi lùi Mã lấy đà kinh điển. Đỏ đe dọa nhảy Mã Khẩu sát cục.",
        "duration": 5.0
    })
    
    # Đen đi Tượng
    b.play('i2', 'g0')
    beats.append({
        "fen": "3ak1e2/4a4/4P1e2/1N7/9/9/9/5K3/9/9 w",
        "moves": ["i2g0"],
        "text": "Tướng Đen không thể nhúc nhích. Sĩ cũng không có nước đi tốt. Đen đành đi Tượng (Tượng 9 thoái 7) chờ chết.",
        "duration": 6.0
    })
    
    b.play('b3', 'c1')
    beats.append({
        "fen": "3ak1e2/2N1a4/4P1e2/9/9/9/9/5K3/9/9 b",
        "moves": ["b3c1"],
        "text": "Mã 8 tiến 7! Đòn Mã Khẩu chí mạng hạ màn trận đấu. Sĩ Tượng Toàn cũng đành bất lực trước sự tinh diệu của Mã Tốt. Đỏ thắng!",
        "duration": 7.0
    })
    
    episode = {
        "title": "Tập 019: Mã Tốt Phá Sĩ Tượng Toàn",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0019.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
