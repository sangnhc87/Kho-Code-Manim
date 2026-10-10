#!/usr/bin/env python3
"""Build episode 013: Song Binh Khéo Thắng Song Tượng (Hai Tốt Kẹp Cổ)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black King at e0. Elephants at c0, a2.
    # Red Pawns at e2 (Tốt nhập tâm), f1 (Tốt kẹp). Red King at d7.
    fen = "2e1k4/5P3/e3P4/9/9/9/9/3K5/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Song Binh khéo thắng Song Tượng: Tượng bay chéo rất rộng nhưng không thể bảo vệ Tướng khỏi những đòn đâm trực diện của Tốt.",
        "duration": 6.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Đỏ đã thiết lập sẵn Tốt nhập tâm ở e2, kết hợp với Tướng ghim chặt cột d. Mọi nẻo đường thoát của Tướng Đen đều bị bịt kín.",
        "duration": 6.0
    })
    
    # Lời giải
    b.play('e2', 'e1')
    beats.append({
        "fen": fen,
        "moves": ["e2e1"],
        "text": "Binh 5 tiến 1! Đâm thẳng Tốt nhập tâm xuống chiếu Tướng. Sát khí bừng bừng!",
        "duration": 6.0
    })
    
    beats.append({
        "fen": "2e1k4/4PP3/e8/9/9/9/9/3K5/9/9 b",
        "text": "Tướng Đen không thể ăn Tốt e1 (do Tốt f1 bảo vệ), cũng không thể sang d0 (do Tướng Đỏ ghim). Đen chỉ còn một đường duy nhất.",
        "duration": 6.0
    })
    
    b.play('e0', 'f0')
    beats.append({
        "fen": "2e1k4/4PP3/e8/9/9/9/9/3K5/9/9 b",
        "moves": ["e0f0"],
        "text": "Tướng 5 bình 4. Đen buộc phải lách sang f0 để lánh nạn.",
        "duration": 5.0
    })
    
    b.play('f1', 'f0')
    beats.append({
        "fen": "2e2k3/4PP3/e8/9/9/9/9/3K5/9/9 w",
        "moves": ["f1f0"],
        "text": "Binh 4 tiến 1! Đâm Tốt hạ gục Tướng Đen. Sát cục liên hoàn, Song Tượng hoàn toàn bất lực. Đỏ thắng!",
        "duration": 6.0
    })
    
    episode = {
        "title": "Tập 013: Song Binh Khéo Thắng Song Tượng",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0013.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
