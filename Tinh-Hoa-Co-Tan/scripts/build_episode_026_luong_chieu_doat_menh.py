#!/usr/bin/env python3
"""Build episode 026: Lưỡng Chiếu Đoạt Mệnh (Xe Pháo Mã)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, e1. Elephants a2, c0.
    # Red: King e9, Chariot e2, Cannon e4, Knight h4, Pawn f2.
    fen = "2eak4/4a4/e3RP3/9/4C2N1/9/9/9/9/4K4 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "label": "PHÂN TÍCH", "headline": "Phân tích", "insight": "Kỳ lý", "narration": "Lưỡng Chiếu Đoạt Mệnh: Sự kết hợp hoàn hảo giữa đòn 'Lưỡng chiếu' (chiếu đôi) và sức mạnh áp đảo của Mã Ngọa Tào.",
        "duration": 7.0
    })
    
    # Lời giải: Xe ăn Sĩ, Lưỡng chiếu
    b.play('e2', 'e1')
    beats.append({
        "fen": "2eak4/4R4/e4P3/9/4C2N1/9/9/9/9/4K4 b",
        "moves": ["e2e1"],
        "label": "PHÂN TÍCH", "headline": "Phân tích", "insight": "Kỳ lý", "narration": "Xe 5 tiến 1! Thí Xe chém Sĩ trung tâm. Chớp nhoáng tạo ra thế 'Lưỡng chiếu' (Xe và Pháo cùng chiếu).",
        "duration": 7.0
    })
    
    # Đen chạy Tướng
    b.play('e0', 'f0')
    beats.append({
        "fen": "2ea1k3/4R4/e4P3/9/4C2N1/9/9/9/9/4K4 w",
        "moves": ["e0f0"],
        "label": "PHÂN TÍCH", "headline": "Phân tích", "insight": "Kỳ lý", "narration": "Bị chiếu đôi, Tướng Đen không thể ăn Xe, buộc phải xuất Tướng 5 bình 4 (e0-f0) chạy trốn.",
        "duration": 5.0
    })
    
    # Sát cục: Mã Ngọa Tào
    b.play('h4', 'g2')
    beats.append({
        "fen": "2ea1k3/4R4/e4PN2/9/4C4/9/9/9/9/4K4 b",
        "moves": ["h4g2"],
        "label": "PHÂN TÍCH", "headline": "Phân tích", "insight": "Kỳ lý", "narration": "Mã 2 thoái 3! Giáng đòn sấm sét chiếu Tướng. Tướng Đen không thể vào lại e0 (bị Xe khống chế), cũng không thể thượng lên f1 (bị Tốt cản). Đỏ thắng tuyệt đối!",
        "duration": 8.0
    })
    
    episode = {
        "id": "tap-0026",
        "title": "Tập 026: Lưỡng Chiếu Đoạt Mệnh",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0026.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
