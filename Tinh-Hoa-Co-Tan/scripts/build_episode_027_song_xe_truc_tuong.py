#!/usr/bin/env python3
"""Build episode 027: Song Xe Trục Tướng (Double Chariot Chasing King)
"""

import json
from pathlib import Path
from src.core import Board

def main():
    # Initial FEN:
    # Black: King d0, Advisor f0.
    # Red: King f7, Chariot 1 f2, Chariot 2 a3, Pawn e3, Knight b2.
    fen = "3k1a3/9/1N3R3/R3P4/9/9/9/5K3/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "label": "PHÂN TÍCH",
        "headline": "Sát cục Song Xe",
        "narration": "Song Xe Trục Tướng: Sự phối hợp nhịp nhàng của hai cỗ Xe tạo thành một chiếc bẫy hình học hoàn hảo, dồn Tướng đối phương vào tử lộ.",
        "insight": "Tuyệt kỹ dồn Tướng",
        "duration": 7.0
    })
    
    # Move 1: Xe 1 bình 4
    b.play('a3', 'd3')
    beats.append({
        "fen": "3k1a3/9/1N3R3/3RP4/9/9/9/5K3/9/9 b",
        "moves": ["a3d3"],
        "label": "BƯỚC 1",
        "headline": "Xe 1 bình 4",
        "narration": "Xe 1 bình 4 chiếu Tướng! Mã bảo vệ mắt d1 nên Tướng không thể tiến lên, buộc phải di chuyển sang lộ 5.",
        "insight": "Khóa chặt lộ d1",
        "duration": 6.0
    })
    
    # Black King moves
    b.play('d0', 'e0')
    beats.append({
        "fen": "4ka3/9/1N3R3/3RP4/9/9/9/5K3/9/9 w",
        "moves": ["d0e0"],
        "label": "BƯỚC 1",
        "headline": "Tướng 4 bình 5",
        "narration": "Tướng Đen buộc phải vào trung cung an toàn.",
        "insight": "Chạy Tướng",
        "duration": 4.0
    })
    
    # Move 2: Xe 6 tiến 2 (f2-f0)
    b.play('f2', 'f0')
    beats.append({
        "fen": "4kR3/9/1N7/3RP4/9/9/9/5K3/9/9 b",
        "moves": ["f2f0"],
        "label": "BƯỚC 2",
        "headline": "Xe 6 tiến 2",
        "narration": "Xe 6 tiến 2, hung hãn chém Sĩ chiếu Tướng! Lúc này lộ 4 đã bị Xe kia phong tỏa, Tướng Đen hết đường lui, đành phải thượng lầu.",
        "insight": "Chém Sĩ phá vây",
        "duration": 7.0
    })
    
    # Black King moves
    b.play('e0', 'e1')
    beats.append({
        "fen": "5R3/4k4/1N7/3RP4/9/9/9/5K3/9/9 w",
        "moves": ["e0e1"],
        "label": "BƯỚC 2",
        "headline": "Tướng 5 tiến 1",
        "narration": "Tướng Đen thượng lên hàng 2, tưởng chừng đã thoát được sự truy kích.",
        "insight": "Thượng Tướng",
        "duration": 4.0
    })
    
    # Move 3: Xe 4 tiến 2 (d3-d1)
    b.play('d3', 'd1')
    beats.append({
        "fen": "5R3/3Rk4/1N7/4P4/9/9/9/5K3/9/9 b",
        "moves": ["d3d1"],
        "label": "BƯỚC 3",
        "headline": "Xe 4 tiến 2",
        "narration": "Xe 4 tiến 2! Đòn sát thủ lạnh lùng. Xe chiếu ngang, Tướng không thể xuống, cũng không thể chạy sang hai bên do bị Xe còn lại và Tốt kiểm soát. Đỏ thắng tuyệt đối!",
        "insight": "Tuyệt Sát",
        "duration": 8.0
    })
    
    episode = {
        "id": "tap-0027",
        "title": "Tập 027: Song Xe Trục Tướng",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0027.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
