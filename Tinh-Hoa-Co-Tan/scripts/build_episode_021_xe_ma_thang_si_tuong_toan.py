#!/usr/bin/env python3
"""Build episode 021: Xe Mã Tốt Phá Sĩ Tượng Toàn (Tuyệt sát dẫn dụ)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, e1, Elephants a2, c0.
    # Red: Pawn d1, Knight b3, Chariot i2, King f7.
    fen = "2eak4/3Pae3/e7R/1N7/9/9/9/5K3/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Xe Mã Tốt phá Sĩ Tượng Toàn: Một thế cờ tàn thực dụng đỉnh cao. Đen thủ kín bưng với Sĩ Tượng Toàn. Làm sao Đỏ phá vỡ?",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Đỏ có Tốt d1 yểm trợ trung lộ, Tướng f7 khống chế cánh phải. Điểm cốt lõi là dùng Xe để 'dẫn dụ' Sĩ Đen tự bóp nghẹt Tướng.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('i2', 'i0')
    beats.append({
        "fen": "2eak3R/3Pae3/e8/1N7/9/9/9/5K3/9/9 b",
        "moves": ["i2i0"],
        "text": "Xe 9 tiến 2! Chiếu Tướng. Tướng Đen không thể nhúc nhích vì vướng Sĩ, buộc Đen phải thoái Sĩ về cản chiếu.",
        "duration": 6.0
    })
    
    # Đen buộc phải thoái Sĩ
    b.play('e1', 'f0')
    beats.append({
        "fen": "2eakaa2R/3P4/e8/1N7/9/9/9/5K3/9/9 w",
        "moves": ["e1f0"],
        "text": "Đen buộc Sĩ 5 thoái 4. Nhưng đây chính là bẫy! Sĩ Đen lùi về f0 đã tự nhốt Tướng của mình, tạo điều kiện cho Mã ra tay.",
        "duration": 7.0
    })
    
    # Sát cục
    b.play('b3', 'd2')
    beats.append({
        "fen": "2eakaa2R/3P4/e2N5/9/9/9/9/5K3/9/9 b",
        "moves": ["b3d2"],
        "text": "Mã 8 tiến 7! Đòn kết liễu hoàn hảo. Tướng Đen bị kẹt cứng giữa 2 Sĩ nhà, đường lên e1 thì bị Tốt Đỏ d1 chốt chặt. Đỏ thắng tàn cuộc mãn nhãn!",
        "duration": 8.0
    })
    
    episode = {
        "title": "Tập 021: Xe Mã Tốt Phá Cờ Thế",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0021.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
