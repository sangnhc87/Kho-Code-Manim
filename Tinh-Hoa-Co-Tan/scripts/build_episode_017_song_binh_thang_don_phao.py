import json
from pathlib import Path

def main():
    fen0 = "4k4/4c4/3P1P3/9/9/9/9/9/9/3K5 w"
    
    beats = []
    
    beats.append({
        "fen": fen0,
        "text": "Song Binh đánh Đơn Pháo: Pháo không có ngòi thì không thể tấn công. Đỏ chỉ cần dùng Song Binh kẹp chặt Cửu cung và phối hợp cùng mặt Tướng là giành chiến thắng.",
        "duration": 7.0,
        "label": "MỞ ĐẦU",
        "headline": "Pháo vô ngòi",
        "narration": "Song Binh đánh Đơn Pháo: Pháo không có ngòi thì vô hại. Đỏ sẽ dùng Song Binh và mặt Tướng để khóa chặt ván cờ.",
        "insight": "Ý chính",
        "moves": []
    })
    
    beats.append({
        "moves": ["d2d1"],
        "text": "Đỏ đi Binh 6 tiến 1! Áp sát Pháo Đen, bắt đầu siết vòng vây.",
        "duration": 5.0,
        "label": "NƯỚC 1",
        "headline": "Tiến Binh",
        "narration": "Đỏ đi Binh 6 tiến 1! Áp sát Pháo Đen, siết vòng vây.",
        "insight": "Tiến Binh",
    })
    
    beats.append({
        "moves": ["e1e8"],
        "text": "Pháo Đen vô tác dụng, đành phải thoái sâu về sân nhà (Pháo 5 thoái 7) để tìm cơ hội.",
        "duration": 5.5,
        "label": "NƯỚC 2",
        "headline": "Thoái Pháo",
        "narration": "Pháo Đen vô tác dụng, đành phải thoái sâu về sân nhà.",
        "insight": "Thoái Pháo",
    })
    
    beats.append({
        "moves": ["f2f1"],
        "text": "Đỏ không vội vàng, đi tiếp Binh 4 tiến 1. Đưa nốt Binh còn lại xuống kẹp cổ. Tướng Đen giờ đây đã hết đường nhúc nhích.",
        "duration": 6.5,
        "label": "NƯỚC 3",
        "headline": "Kẹp Cổ",
        "narration": "Đỏ bình tĩnh đi Binh 4 tiến 1 kẹp cổ. Tướng Đen giờ đây đã hết đường nhúc nhích.",
        "insight": "Kẹp cổ",
    })
    
    beats.append({
        "moves": ["e8e7"],
        "text": "Vì Tướng Đen bị kẹp cứng, Đen buộc phải đi Pháo (Pháo 5 tiến 1), chờ đợi đòn kết liễu.",
        "duration": 5.0,
        "label": "NƯỚC 4",
        "headline": "Tuyệt vọng",
        "narration": "Vì Tướng Đen bị kẹp cứng, Đen đành phải đi Pháo, chờ đòn kết liễu.",
        "insight": "Hết nước",
    })
    
    beats.append({
        "moves": ["d1d0"],
        "text": "Đỏ đâm Binh 6 tiến 1 chiếu tuyệt sát! Tướng Đen không thể ăn Tốt vì bị mặt Tướng Đỏ (ở lộ 4) bảo vệ. Đỏ thắng!",
        "duration": 7.0,
        "label": "KẾT THÚC",
        "headline": "Tuyệt sát",
        "narration": "Đỏ đâm Binh chiếu tuyệt sát! Tướng Đen bị mặt Tướng Đỏ ghim chặt. Đỏ thắng!",
        "insight": "Tuyệt sát",
    })
    
    episode = {
        "id": "tap-0017",
        "title": "Tập 017: Song Binh Phá Đơn Pháo",
        "subtitle": "Bài Tập Cờ Tàn",
        "category": "Tàn Binh",
        "goal_text": "Tuyệt sát! Đỏ thắng",
        "analysis_status": "draft",
        "fen": fen0,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0017.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
