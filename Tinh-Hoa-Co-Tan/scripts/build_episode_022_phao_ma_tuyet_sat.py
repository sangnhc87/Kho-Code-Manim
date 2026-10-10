#!/usr/bin/env python3
"""Build episode 022: Pháo Mã Tuyệt Sát (Phế Xe, Lồng Pháo, Cản Tượng)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, f0, Elephants a2, c0.
    # Red: King e7, Knight d4, Cannon e4, Chariot f1, Pawns d1, f2.
    fen = "2eaka3/3P1R3/e4P3/9/3NC4/9/9/4K4/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Pháo Mã tuyệt sát: Một ván cờ tàn thực dụng ở đẳng cấp rất cao. Đen có đủ Sĩ Tượng Toàn phòng thủ kiên cố. Đỏ phải phối hợp cả 5 quân để phá vỡ.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Tướng Đỏ chiếm trung, Pháo e4 nhòm ngó. Tốt d1 và f2 tuy nhỏ bé nhưng đóng vai trò huyệt đạo cực kỳ quan trọng trong sát cục này.",
        "duration": 7.0
    })
    
    # Lời giải: Phế Xe
    b.play('f1', 'f0')
    beats.append({
        "fen": "2eakR3/3P5/e4P3/9/3NC4/9/9/4K4/9/9 b",
        "moves": ["f1f0"],
        "text": "Xe 4 tiến 1! Đòn phế Xe chấn động! Đỏ hiến Xe ăn thẳng vào Sĩ Đen để ép Tướng Đen phải xuất cung (lệch sang cột f).",
        "duration": 7.0
    })
    
    # Đen ăn Xe
    b.play('e0', 'f0')
    beats.append({
        "fen": "2ea1k3/3P5/e4P3/9/3NC4/9/9/4K4/9/9 w",
        "moves": ["e0f0"],
        "text": "Tướng 5 bình 4 ăn Xe. Đen không còn lựa chọn nào khác vì Sĩ Tượng không thể cứu viện.",
        "duration": 6.0
    })
    
    # Sát cục: Mã Hậu Pháo
    b.play('d4', 'e2')
    beats.append({
        "fen": "2ea1k3/3P5/e3NP3/9/4C4/9/9/4K4/9/9 b",
        "moves": ["d4e2"],
        "text": "Mã 6 tiến 5! Tuyệt sát Mã Hậu Pháo! Tướng Đen không thể vào e0 vì bị Pháo chiếu, không thể lên f1 vì Tốt f2 chặn.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": "2ea1k3/3P5/e3NP3/9/4C4/9/9/4K4/9/9 b",
        "text": "Đặc biệt, Tượng Đen ở c0 không thể ăn Mã e2 vì đã bị Tốt Đỏ d1 'cản mắt'. Một sự phối hợp hoàn hảo không tì vết. Đỏ thắng!",
        "duration": 8.0
    })
    
    episode = {
        "title": "Tập 022: Pháo Mã Tuyệt Sát",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0022.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
