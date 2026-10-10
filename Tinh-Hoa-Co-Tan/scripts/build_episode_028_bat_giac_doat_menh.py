#!/usr/bin/env python3
"""Build episode 028: Bát Giác Đoạt Mệnh (Mã Bát Giác)
"""

import json
from pathlib import Path
from src.core import Board

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, f0.
    # Red: King e9, Chariot 1 a3, Chariot 2 h1, Knight h3, Pawn g2.
    fen = "3akaR2/9/6P2/R6N1/9/9/9/9/9/3K5 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "label": "PHÂN TÍCH",
        "headline": "Bát Giác Mã",
        "narration": "Bát Giác Đoạt Mệnh: Một ván cờ tàn mẫu mực thể hiện sức mạnh của đòn Bát Giác Mã (Mã đứng ở góc chéo cung Tướng) kết hợp cùng Xe và Tốt áp sát.",
        "insight": "Tuyệt kỹ Bát Giác Mã",
        "duration": 7.0
    })
    
    # Move 1: Mã 2 tấn 4
    b.play('h3', 'f2')
    beats.append({
        "fen": "3akaR2/9/5NP2/R8/9/9/9/9/9/3K5 b",
        "moves": ["h3f2"],
        "label": "BƯỚC 1",
        "headline": "Mã 2 tấn 4",
        "narration": "Mã 2 tấn 4 chiếu Tướng! Lập tức hình thành thế Bát Giác Mã kiểm soát chặt huyệt đạo d1. Tướng Đen không thể nhúc nhích sang hai bên, buộc phải thượng lên e1.",
        "insight": "Khóa chặt góc cung",
        "duration": 6.0
    })
    
    # Black King moves
    b.play('e0', 'e1')
    beats.append({
        "fen": "3a1aR2/4k4/5NP2/R8/9/9/9/9/9/3K5 w",
        "moves": ["e0e1"],
        "label": "BƯỚC 1",
        "headline": "Tướng 5 tiến 1",
        "narration": "Tướng Đen tiến 1 tạm thời né đòn.",
        "insight": "Chạy Tướng",
        "duration": 4.0
    })
    
    # Move 2: Xe 9 bình 5
    b.play('a3', 'e3')
    beats.append({
        "fen": "3a1aR2/4k4/5NP2/4R4/9/9/9/9/9/3K5 b",
        "moves": ["a3e3"],
        "label": "BƯỚC 2",
        "headline": "Xe 9 bình 5",
        "narration": "Xe 9 bình 5 vỗ mặt! Tướng Đen bị Mã khóa chết cửa d1, không thể thoái lui vì vướng Mã, đành ngậm ngùi lệch sang lộ 6 (f1).",
        "insight": "Dồn ép liên hoàn",
        "duration": 7.0
    })
    
    # Black King moves
    b.play('e1', 'f1')
    beats.append({
        "fen": "3a1aR2/5k3/5NP2/4R4/9/9/9/9/9/3K5 w",
        "moves": ["e1f1"],
        "label": "BƯỚC 2",
        "headline": "Tướng 5 bình 4",
        "narration": "Bị dồn vào đường cùng, Tướng Đen buộc phải lệch sang cột f.",
        "insight": "Tướng vào góc chết",
        "duration": 4.0
    })
    
    # Move 3: Binh 3 tấn 1
    b.play('g2', 'g1')
    beats.append({
        "fen": "3a1aR2/5kP2/5N3/4R4/9/9/9/9/9/3K5 b",
        "moves": ["g2g1"],
        "label": "BƯỚC 3",
        "headline": "Binh 3 tấn 1",
        "narration": "Binh 3 tấn 1! Nước chốt hạ không tưởng. Tốt lết xuống một bước kề sát cổ Tướng Đen, lại được Xe yểm trợ phía sau. Tướng Đen đã hết đường lui. Sát cục vô cùng đẹp mắt!",
        "insight": "Tuyệt Sát",
        "duration": 8.0
    })
    
    episode = {
        "id": "tap-0028",
        "title": "Tập 028: Bát Giác Đoạt Mệnh",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0028.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
