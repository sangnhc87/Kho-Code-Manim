#!/usr/bin/env python3
"""Build episode 023: Phế Xe Xuyên Tâm (Xe Mã Pháo Tốt phối hợp)
"""

import json
from pathlib import Path
from src.core import Board, sq

def main():
    # Initial FEN:
    # Black: King e0, Advisors d0, e1, Elephants a2, c0.
    # Red: King f7, Chariot e3, Knight c2, Cannon d2, Pawn d1.
    fen = "2eak4/3Pa4/e1N6/3CR4/9/9/9/5K3/9/9 w"
    
    b = Board.fen(fen)
    
    beats = []
    
    # Phân tích
    beats.append({
        "fen": fen,
        "text": "Xe Mã Pháo Xuyên Tâm: Một sát cục kinh điển đòn 'Phế Xe' phá vỡ hàng thủ Sĩ Tượng Toàn kiên cố của Đen.",
        "duration": 7.0
    })
    
    beats.append({
        "fen": fen,
        "text": "Đỏ có Xe nhòm ngó trung lộ, Mã c2 sẵn sàng tiếp ứng. Tướng Đỏ f7 và Pháo d2 đóng vai trò then chốt bịt kín mọi đường lùi của Tướng Đen.",
        "duration": 7.0
    })
    
    # Lời giải: Phế Xe
    b.play('e3', 'e1')
    beats.append({
        "fen": "2eak4/3PR4/e1N6/3C5/9/9/9/5K3/9/9 b",
        "moves": ["e3e1"],
        "text": "Xe 5 tiến 2! Đòn hiến Xe sấm sét cắm thẳng vào tim (Xuyên Tâm). Đen không thể dùng Tướng ăn Xe vì Mã c2 bảo vệ, cũng không thể chạy Tướng sang f0 vì Tướng Đỏ f7 ghim chặt.",
        "duration": 8.0
    })
    
    # Đen buộc phải dùng Sĩ ăn Xe
    b.play('d0', 'e1')
    beats.append({
        "fen": "2e1k4/3Pa4/e1N6/3C5/9/9/9/5K3/9/9 w",
        "moves": ["d0e1"],
        "text": "Tướng Đen hết đường thoái, buộc phải dùng Sĩ 4 thối 5 (d0-e1) ăn Xe để giải sát.",
        "duration": 6.0
    })
    
    # Sát cục: Mã Hậu Pháo (tùy biến)
    b.play('c2', 'e1')
    beats.append({
        "fen": "2e1k4/3PN4/e8/3C5/9/9/9/5K3/9/9 b",
        "moves": ["c2e1"],
        "text": "Mã 3 tiến 5! Ăn lại Sĩ và chiếu Tướng. Đen hoàn toàn tuyệt vọng: Tướng không thể ra d0 vì Pháo d3 (mượn ngòi Tốt d1) nã đạn, không thể ăn Mã e1 vì Tốt d1 bảo kê.",
        "duration": 8.0
    })
    
    beats.append({
        "fen": "2e1k4/3PN4/e8/3C5/9/9/9/5K3/9/9 b",
        "text": "Năm quân Đỏ phối hợp nhịp nhàng như một cỗ máy, không thừa không thiếu một chi tiết nào. Đỏ thắng sát cuộc!",
        "duration": 7.0
    })
    
    episode = {
        "id": "tap-0023",
        "title": "Tập 023: Tuyệt Sát Phế Xe Xuyên Tâm",
        "fen": fen,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0023.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
