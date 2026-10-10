#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    fen0 = "4k4/9/3PnP3/9/9/9/9/9/9/4K4 w"
    
    beats = []
    
    beats.append({
        "fen": fen0,
        "text": "Song Binh khéo thắng Đơn Mã: Lợi dụng thế Tướng lộ diện (Tướng đối Tướng) để ghim chết Mã Đen, tạo điều kiện cho Song Binh áp sát.",
        "duration": 6.0,
        "label": "MỞ ĐẦU",
        "headline": "Ghim Mã",
        "narration": "Song Binh khéo thắng Đơn Mã: Lợi dụng thế Tướng đối Tướng để ghim chết Mã Đen, tạo điều kiện cho Song Binh áp sát.",
        "insight": "Ghim Mã",
        "moves": []
    })
    
    fen1 = "4k4/3P5/4nP3/9/9/9/9/9/9/4K4 b"
    beats.append({
        "fen": fen0,
        "moves": ["d2d1"],
        "text": "Đỏ đi Binh 6 tiến 1! Áp sát cung thành. Mã Đen lúc này bị ghim chặt không thể di chuyển vì sẽ lộ mặt Tướng.",
        "duration": 5.0,
        "label": "NƯỚC 1",
        "headline": "Tiến Binh",
        "narration": "Đỏ đi Binh 6 tiến 1! Áp sát cung thành. Mã Đen lúc này bị ghim chặt.",
        "insight": "Mã bị ghim",
    })
    
    fen2 = "5k3/3P5/4nP3/9/9/9/9/9/9/4K4 w"
    beats.append({
        "fen": fen1,
        "moves": ["e0f0"],
        "text": "Đen buộc phải Tướng 5 bình 4 (sang f0) vì Mã không thể đi, các lộ khác đều bị Binh kiểm soát.",
        "duration": 5.0,
        "label": "NƯỚC 2",
        "headline": "Dạt Tướng",
        "narration": "Đen buộc phải Tướng 5 bình 4 vì Mã không thể đi.",
        "insight": "Tướng chạy",
    })
    
    fen3 = "5k3/3P1P3/4n4/9/9/9/9/9/9/4K4 b"
    beats.append({
        "fen": fen2,
        "moves": ["f2f1"],
        "text": "Đỏ tiếp tục Binh 4 tiến 1! Cả hai Binh áp sát hàng đáy, Tướng Đen hết đường lui.",
        "duration": 5.0,
        "label": "NƯỚC 3",
        "headline": "Kẹp Cổ",
        "narration": "Đỏ tiếp tục Binh 4 tiến 1! Cả hai Binh áp sát hàng đáy.",
        "insight": "Ép góc",
    })
    
    fen4 = "5k3/4nP3/9/9/9/9/9/9/9/4K4 w"
    beats.append({
        "fen": fen3,
        "moves": ["e2d1"],
        "text": "Vì Tướng đã dạt sang f0 nên Mã Đen được giải phóng khỏi thế ghim, ăn ngay Binh đỏ ở d1.",
        "duration": 5.0,
        "label": "NƯỚC 4",
        "headline": "Mã thoát",
        "narration": "Mã Đen được giải phóng khỏi thế ghim, ăn ngay Binh đỏ ở d1.",
        "insight": "Mã ăn Binh",
    })
    
    fen5 = "5k3/4nP3/9/9/9/9/9/9/9/5K3 b"
    beats.append({
        "fen": fen4,
        "moves": ["e9f9"],
        "text": "Đỏ Tướng 5 bình 4 (sang f9). Kiểm soát không cho Tướng Đen vào lại trung lộ. Đen lại bị nhốt!",
        "duration": 5.0,
        "label": "NƯỚC 5",
        "headline": "Bình Tướng",
        "narration": "Đỏ Tướng 5 bình 4. Kiểm soát không cho Tướng Đen vào lại trung lộ.",
        "insight": "Bình Tướng",
    })
    
    fen6 = "5k3/5P3/3n4/9/9/9/9/9/9/5K3 w"
    beats.append({
        "fen": fen5,
        "moves": ["d1d2"],
        "text": "Mã Đen thoái về (Mã 6 thoái 7) hòng tìm đường cứu Tướng.",
        "duration": 5.0,
        "label": "NƯỚC 6",
        "headline": "Thoái Mã",
        "narration": "Mã Đen thoái về hòng tìm đường cứu Tướng.",
        "insight": "Thoái Mã",
    })
    
    fen7 = "5k3/9/3n2P3/9/9/9/9/9/9/5K3 b"
    beats.append({
        "fen": fen6,
        "moves": ["f1f2"],
        "text": "Đỏ lách nhẹ Binh 4 bình 3 (Binh ăn Mã hoặc bắt chết). Sát cục tuyệt đỉnh!",
        "duration": 6.0,
        "label": "KẾT THÚC",
        "headline": "Tuyệt sát",
        "narration": "Đỏ lách Binh tuyệt sát! Đỏ thắng.",
        "insight": "Tuyệt sát",
    })
    
    episode = {
        "id": "tap-0015",
        "title": "Tập 015: Song Binh Khéo Thắng Đơn Mã",
        "subtitle": "Bài Tập Cờ Tàn",
        "category": "Tàn Binh",
        "goal_text": "Tuyệt sát! Đỏ thắng",
        "analysis_status": "draft",
        "fen": fen0,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0015.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
