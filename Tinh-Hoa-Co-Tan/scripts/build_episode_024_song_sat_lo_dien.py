#!/usr/bin/env python3
"""Build episode 024: Mã Ngọa Tào + Xe (Tuyệt Sát Lộ Diện)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, d2, Elephants a2, c0.
    # Red: King e7, Chariot e3, Knight c4, Pawn g1.
    fen = "2eak4/6P2/e2a5/4R4/2N6/9/9/4K4/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Xe Mã Tuyệt Sát: Một đòn phối hợp kinh điển giữa Mã Ngọa Tào và Xe, với sự yểm trợ thầm lặng của Tốt.",
        "duration": 6.0
    })
    
    # Lời giải: Mã Ngọa Tào
    b.play('c4', 'd2')
    beats.append({
        "fen": "2eak4/6P2/e2N5/4R4/9/9/9/4K4/9/9 b",
        "moves": ["c4d2"],
        "text": "Mã 3 tiến 4! Khéo léo ăn Sĩ d2 và tung đòn 'Ngọa Tào' chiếu Tướng. Sĩ d0 đã bít đường sang trái, Tướng Đen buộc phải xuất tướng sang phải.",
        "duration": 7.0
    })
    
    # Đen chạy Tướng
    b.play('e0', 'f0')
    beats.append({
        "fen": "2ea1k3/6P2/e2N5/4R4/9/9/9/4K4/9/9 w",
        "moves": ["e0f0"],
        "text": "Tướng 5 bình 4 (e0-f0) chạy trốn.",
        "duration": 5.0
    })
    
    # Sát cục: Xe chiếu
    b.play('e3', 'f3')
    beats.append({
        "fen": "2ea1k3/6P2/e2N5/5R3/9/9/9/4K4/9/9 b",
        "moves": ["e3f3"],
        "text": "Xe 5 bình 4! Chiếu sát cục! Tướng Đen không thể vào lại e0 vì Mã Ngọa Tào trấn giữ, không thể thượng lên f1 vì Tốt Đỏ g1 đã phục kích sẵn. Đỏ thắng tuyệt đối!",
        "duration": 8.0
    })
    
    episode = {
        "title": "Tập 024: Mã Ngọa Tào Tuyệt Sát",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0024.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
