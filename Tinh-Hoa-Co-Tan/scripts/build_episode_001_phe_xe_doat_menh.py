#!/usr/bin/env python3
"""Build episode 001: Phế Xe Đoạt Mệnh (Tuyệt Học Cờ Tàn)
"""

import json
from pathlib import Path
from src.core import Board

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, f0. Chariot d1. Cannon e2. Knight f2.
    # Red: Chariot 1 h0, Chariot 2 f3, Knight h4, Cannon 1 a1, Cannon 2 e6, Pawn e4, King e9.
    fen = "3aka1R1/C2r5/4cn3/5R3/4P2N1/9/4C4/9/9/4K4 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "label": "PHÂN TÍCH",
        "headline": "Phế Xe Đoạt Mệnh",
        "narration": "Chào mừng các bạn đến với Tinh Hoa Cờ Tàn. Hôm nay chúng ta sẽ chiêm ngưỡng một tuyệt kỹ thực dụng: Phế Xe đoạt mệnh. Trong thế cờ vô cùng căng thẳng, Đỏ tung ra chuỗi 3 nước sát thủ liên hoàn, ép Tướng Đen vào tử lộ.",
        "insight": "Tuyệt sát liên hoàn",
        "duration": 9.0
    })
    
    # Move 1: Xe 2 bình 4
    b.play('h0', 'f0')
    beats.append({
        "moves": ["h0f0"],
        "label": "BƯỚC 1",
        "headline": "Xe 2 bình 4",
        "narration": "Đỏ khai đòn sấm sét: Xe 2 bình 4 chém thẳng Sĩ chiếu Tướng! Phế Xe không thương tiếc. Tướng Đen không thể sang lộ 6 vì bị Pháo nhòm ngó, buộc phải ăn Xe.",
        "insight": "Phế Xe mở đường",
        "duration": 8.0
    })
    
    # Black King moves
    b.play('e0', 'f0')
    beats.append({
        "moves": ["e0f0"],
        "label": "BƯỚC 1",
        "headline": "Tướng 5 bình 4",
        "narration": "Đen buộc phải dùng Tướng ăn Xe.",
        "insight": "Sập bẫy",
        "duration": 3.0
    })
    
    # Move 2: Mã 2 tiến 3
    b.play('h4', 'g2')
    beats.append({
        "moves": ["h4g2"],
        "label": "BƯỚC 2",
        "headline": "Mã 2 tiến 3",
        "narration": "Mã Đỏ lập tức nhảy Ngọa Tào chiếu Tướng! Đường lui sang lộ 6 vẫn bị Pháo khóa chặt, Tướng Đen hết cách đành lùi lại vị trí cũ.",
        "insight": "Mã Ngọa Tào",
        "duration": 7.0
    })
    
    # Black King moves
    b.play('f0', 'e0')
    beats.append({
        "moves": ["f0e0"],
        "label": "BƯỚC 2",
        "headline": "Tướng 4 bình 5",
        "narration": "Tướng Đen lùi về cung, tưởng chừng đã an toàn.",
        "insight": "Lùi bước",
        "duration": 3.0
    })
    
    # Move 3: Xe 4 bình 5
    b.play('f3', 'e3')
    beats.append({
        "moves": ["f3e3"],
        "label": "BƯỚC 3",
        "headline": "Xe 4 bình 5",
        "narration": "Nhưng không! Xe Đỏ bình vào trung lộ, mượn ngòi Tốt để Pháo gánh bảo vệ. Mã Ngọa Tào kiểm soát nốt cửa thoát. Tướng Đen bị kẹp chết giữa Cửu cung. Tuyệt sát vinh quang!",
        "insight": "Song sát vô phương",
        "duration": 9.0
    })
    
    episode = {
        "id": "tap-0001",
        "title": "Tập 001: Phế Xe Đoạt Mệnh",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0001.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
