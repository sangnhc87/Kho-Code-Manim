#!/usr/bin/env python3
"""Build episode 020: Xe Tốt Khéo Thắng Song Sĩ (Tuyệt Sát Ép Góc)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at d0. Advisors at f0, e1.
    # Red Pawn at e2. Red Chariot at f4. Red King at e7.
    fen = "3k1a3/4a4/4P4/9/5R3/9/9/4K4/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Xe Tốt khéo thắng Song Sĩ: Một thế cờ vô cùng mẫu mực. Đỏ có Tốt nhập tâm (e2) và Tướng chiếm trung (e7) khóa chặt không gian của Tướng Đen.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đen bị ép lệch sang cột d. Xe Đỏ đang phục sẵn ở f4 chuẩn bị ra đòn quyết định.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('f4', 'd4')
    beats.append({
        "fen": "3k1a3/4a4/4P4/9/3R5/9/9/4K4/9/9 b",
        "moves": ["f4d4"],
        "text": "Xe 4 bình 6! Đâm Xe chiếu Tướng. Nước đi chí mạng ép Đen vào thế bí.",
        "duration": 5.0
    })
    
    # Đen buộc phải lên Sĩ cản
    b.play('e1', 'd2')
    beats.append({
        "fen": "3k1a3/9/3aP4/9/3R5/9/9/4K4/9/9 w",
        "moves": ["e1d2"],
        "text": "Tướng Đen không thể vào e0 do Tướng Đỏ ghim, cũng không thể lên d1 do Xe Đỏ kiểm soát. Đen buộc phải bung Sĩ (Sĩ 5 tiến 6) để cản chiếu.",
        "duration": 7.0
    })
    
    b.play('d4', 'd2')
    beats.append({
        "fen": "3k1a3/9/3RP4/9/9/9/9/4K4/9/9 b",
        "moves": ["d4d2"],
        "text": "Xe 6 tiến 2! Xe dũng mãnh ăn thẳng Sĩ Đen. Tướng Đen không thể ăn Xe vì đã có Tốt e2 bảo vệ (đòn Xe mượn chân Tốt). Sát cục tuyệt đẹp!",
        "duration": 7.0
    })
    
    episode = {
        "title": "Tập 020: Xe Tốt Phá Song Sĩ",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0020.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
