#!/usr/bin/env python3
"""Build episode 010: Mã Thắng Đơn Tượng (Bí tử)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black Elephant at c0, Black King at d1.
    # Red Knight at a2, Red King at e7.
    fen = "2e6/3k5/N8/9/9/9/9/4K4/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Mã thắng Đơn Tượng: Một thế cờ tàn tuyệt đẹp. Khác với Sĩ, Tượng bay chéo rất rộng, nhưng lại có điểm yếu là 'mắt Tượng'.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đỏ ở e7 đang khống chế cột trung tâm. Vấn đề là làm sao để bắt Tượng hoặc dồn Đen vào thế bí tử.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('a2', 'c3')
    beats.append({
        "fen": fen,
        "moves": ["a2c3"],
        "text": "Đỏ đi Mã 9 tiến 7! Chiếu Tướng.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "2e6/3k5/9/2N6/9/9/9/4K4/9/9 b",
        "text": "Mã Đỏ chiếu Tướng, buộc Tướng Đen phải di chuyển.",
        "duration": 5.0
    })
    
    b.play('d1', 'd0')
    beats.append({
        "fen": "2e6/3k5/9/2N6/9/9/9/4K4/9/9 b",
        "moves": ["d1d0"],
        "text": "Đen đành thoái Tướng xuống d0 (Tướng 4 thoái 1).",
        "duration": 5.0
    })
    
    b.play('c3', 'b1')
    beats.append({
        "fen": "2ek5/9/9/2N6/9/9/9/4K4/9/9 w",
        "moves": ["c3b1"],
        "text": "Mã 7 thoái 8! Lại tiếp tục chiếu Tướng, đồng thời khéo léo chui vào 'mắt Tượng'.",
        "duration": 6.0
    })
    
    b.play('d0', 'd1')
    beats.append({
        "fen": "2ek5/1N7/9/9/9/9/9/4K4/9/9 b",
        "moves": ["d0d1"],
        "text": "Tướng Đen buộc phải trèo lên d1 (Tướng 4 tiến 1) để tránh bị ăn mất.",
        "duration": 5.0
    })
    
    b.play('e7', 'e8')
    beats.append({
        "fen": "2e6/1N1k5/9/9/9/9/9/4K4/9/9 w",
        "moves": ["e7e8"],
        "text": "Tướng 5 thoái 1! Lại một nước chờ tinh diệu của Tướng Đỏ.",
        "duration": 5.0
    })
    
    beats.append({
        "fen": "2e6/1N1k5/9/9/9/9/9/9/4K4/9 b",
        "text": "Lúc này Tượng Đen bị Mã chặn mắt ở b1, và bị chính Tướng Đen chặn mắt ở d1 nên không thể nhúc nhích.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": "2e6/1N1k5/9/9/9/9/9/9/4K4/9 b",
        "text": "Tướng Đen bị Mã Đỏ khống chế hai điểm d0 và d2, trung lộ bị Tướng Đỏ ghim. Đen hết nước đi (Bí tử). Đỏ thắng!",
        "duration": 7.0
    })
    
    episode = {
        "title": "Tập 0010: Mã Thắng Đơn Tượng (Bí Tử)",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0010.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
