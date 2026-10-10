#!/usr/bin/env python3
"""Build episode 029: Tiểu Xe Đoạt Mệnh (Phế Xe Thắng Cục)
"""

import json
from pathlib import Path
from src.core import Board

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, f0, Elephants a2, c0. Pawn e2.
    # Red: King e9, Chariot 1 e4, Chariot 2 h0.
    # Red Knights: b3, g2.
    # Red Pawns: c2, f2.
    fen = "2eaka1R1/9/e1P1pPN2/1N7/4R4/9/9/9/9/4K4 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "label": "PHÂN TÍCH",
        "headline": "Tiểu Xe Đoạt Mệnh",
        "narration": "Một tuyệt tác cờ tàn phế Xe để dồn Tướng vào đường cùng. Hãy chú ý sức mạnh của các Tốt (Tiểu Xe) khi đã sang sông và áp sát Cửu cung.",
        "insight": "Phế Xe tạo thế",
        "duration": 7.0
    })
    
    # Move 1: Xe 2 bình 4
    b.play('h0', 'f0')
    beats.append({
        "moves": ["h0f0"],
        "label": "BƯỚC 1",
        "headline": "Xe 2 bình 4",
        "narration": "Xe 2 bình 4 chém Sĩ chiếu Tướng! Nước đi dũng mãnh nhờ có Mã bảo vệ. Tướng Đen không thể ăn Xe, đành phải thượng lên lầu 2.",
        "insight": "Dồn Tướng",
        "duration": 6.0
    })
    
    # Black King moves
    b.play('e0', 'e1')
    beats.append({
        "moves": ["e0e1"],
        "label": "BƯỚC 1",
        "headline": "Tướng 5 tiến 1",
        "narration": "Tướng Đen thượng lên e1 tạm lánh.",
        "insight": "Chạy Tướng",
        "duration": 4.0
    })
    
    # Move 2: Xe 5 tiến 2
    b.play('e4', 'e2')
    beats.append({
        "moves": ["e4e2"],
        "label": "BƯỚC 2",
        "headline": "Xe 5 tiến 2",
        "narration": "Xe 5 tiến 2 tiêu diệt Tốt cản đường và tiếp tục chiếu! Chớp nhoáng tạo ra sức ép nghẹt thở. Tướng Đen bị khóa chặt hai cánh, đành phải né sang lộ 4 (d1).",
        "insight": "Phá Tốt đoạt đường",
        "duration": 7.0
    })
    
    # Black King moves
    b.play('e1', 'd1')
    beats.append({
        "moves": ["e1d1"],
        "label": "BƯỚC 2",
        "headline": "Tướng 5 bình 6",
        "narration": "Tướng Đen né sang d1, hy vọng thoát khỏi tầm ngắm.",
        "insight": "Vào góc hẹp",
        "duration": 4.0
    })
    
    # Move 3: Binh 7 bình 6
    b.play('c2', 'd2')
    beats.append({
        "moves": ["c2d2"],
        "label": "BƯỚC 3",
        "headline": "Binh 7 bình 6",
        "narration": "Binh 7 bình 6! Đòn kết liễu hoàn hảo. Tốt đóng vai trò như một Tiểu Xe đâm ngang cổ Tướng. Tướng Đen bị Mã khóa chặt cửa c1, Xe giữ cửa e1, hoàn toàn hết đường sống. Đỏ thắng!",
        "insight": "Tuyệt Sát",
        "duration": 8.0
    })
    
    episode = {
        "id": "tap-0029",
        "title": "Tập 029: Tiểu Xe Đoạt Mệnh",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0029.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
