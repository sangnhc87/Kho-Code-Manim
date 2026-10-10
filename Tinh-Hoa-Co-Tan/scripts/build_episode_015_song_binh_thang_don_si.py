import json
from pathlib import Path

def main():
    fen0 = "3ak4/5P3/9/4P4/9/9/9/9/9/3K5 w"
    
    beats = []
    
    beats.append({
        "fen": fen0,
        "text": "Song Binh khéo thắng Đơn Sĩ: Lợi dụng mặt Tướng ghim chặt đối phương.",
        "duration": 6.0,
        "label": "MỞ ĐẦU",
        "headline": "Thử thách",
        "narration": "Song Binh khéo thắng Đơn Sĩ: Lợi dụng mặt Tướng ghim chặt đối phương.",
        "insight": "Ý chính",
        "moves": []
    })
    
    fen1 = "3ak4/5P3/4P4/9/9/9/9/9/9/3K5 b"
    beats.append({
        "fen": fen0,
        "moves": ["e3e2"],
        "text": "Đỏ đi Binh 5 tiến 1. Áp sát cung thành, chuẩn bị đâm thẳng vào trung lộ.",
        "duration": 5.0,
        "label": "NƯỚC 1",
        "headline": "Tiến Binh",
        "narration": "Đỏ đi Binh 5 tiến 1. Áp sát cung thành.",
        "insight": "Tiến Binh",
    })
    
    fen2 = "4k4/4aP3/4P4/9/9/9/9/9/9/3K5 w"
    beats.append({
        "fen": fen1,
        "moves": ["d0e1"],
        "text": "Đen lên Sĩ (Sĩ 4 tiến 5) để che chắn và ngăn Tốt Đỏ đâm xuống.",
        "duration": 5.0,
        "label": "NƯỚC 2",
        "headline": "Lên Sĩ",
        "narration": "Đen lên Sĩ để che chắn trung lộ.",
        "insight": "Lên Sĩ",
    })
    
    fen3 = "4k4/4PP3/9/9/9/9/9/9/9/3K5 b"
    beats.append({
        "fen": fen2,
        "moves": ["e2e1"],
        "text": "Tuy nhiên, Đỏ táo bạo đi Binh 5 tiến 1! Đâm thẳng Tốt ăn Sĩ chiếu Tướng. Tuyệt sát! Tướng Đen không thể sang d0 vì lộ mặt Tướng Đỏ, sang f0 bị Tốt kẹp, ăn lên e1 thì bị Tốt f1 bảo vệ. Đỏ thắng!",
        "duration": 7.0,
        "label": "KẾT THÚC",
        "headline": "Tuyệt sát",
        "narration": "Đỏ táo bạo đâm Tốt ăn Sĩ chiếu Tướng. Tuyệt sát! Đỏ thắng!",
        "insight": "Tuyệt sát",
    })
    
    episode = {
        "id": "tap-0015",
        "title": "Tập 015: Song Binh Thắng Đơn Sĩ",
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
