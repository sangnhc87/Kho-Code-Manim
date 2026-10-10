import json
from pathlib import Path

def main():
    fen0 = "3aka3/9/3PPP3/9/9/9/9/9/9/4K4 w"
    
    beats = []
    
    beats.append({
        "fen": fen0,
        "text": "Tam Binh phá Song Sĩ: Trong cờ tàn, 3 Tốt nếu đã áp sát Cửu cung thì sức mạnh vô cùng khủng khiếp. Hãy xem cách Đỏ dùng đòn Bức Tử để giành chiến thắng.",
        "duration": 7.0,
        "label": "MỞ ĐẦU",
        "headline": "Áp sát",
        "narration": "Ba Tốt đã áp sát Cửu cung, tạo thế công cực mạnh. Hãy xem cách Đỏ giăng bẫy Bức Tử.",
        "insight": "Ý chính",
        "moves": []
    })
    
    beats.append({
        "moves": ["e2e1"],
        "text": "Đỏ táo bạo đi Binh 5 tiến 1! Đâm thẳng Tốt nhập tâm chiếu Tướng, phế Binh để phá vỡ cấu trúc phòng ngự.",
        "duration": 5.5,
        "label": "NƯỚC 1",
        "headline": "Phế Binh",
        "narration": "Đỏ táo bạo đi Binh 5 tiến 1 chiếu Tướng. Phế Tốt nhập tâm để phá vỡ cấu trúc phòng ngự.",
        "insight": "Phế Binh",
    })
    
    beats.append({
        "moves": ["d0e1"],
        "text": "Đen không thể vào Tướng, đành phải đi Sĩ 4 tiến 5 (ăn Tốt). Nhưng đây chính là cái bẫy chết người!",
        "duration": 5.5,
        "label": "NƯỚC 2",
        "headline": "Sập bẫy",
        "narration": "Đen buộc phải ăn Sĩ lên. Nhưng đây chính là lúc cái bẫy sập xuống!",
        "insight": "Ăn Tốt",
    })
    
    beats.append({
        "moves": ["d2d1"],
        "text": "Đỏ đi Binh 6 tiến 1! Khóa chặt ngả đường cuối cùng của Tướng Đen. Một nước đi kết liễu hoàn hảo.",
        "duration": 5.5,
        "label": "NƯỚC 3",
        "headline": "Khóa chặt",
        "narration": "Đỏ đi Binh 6 tiến 1 khóa chặt ngả đường cuối cùng. Đen hoàn toàn rơi vào thế bí tử.",
        "insight": "Khóa chặt",
    })
    
    beats.append({
        "moves": [],
        "text": "Tuyệt sát bằng luật Hết nước đi (Bức Tử)! Tướng Đen bị kẹp chết. Sĩ trung tâm bị ghim mặt Tướng không thể nhúc nhích. Sĩ biên vướng đồng đội. Đỏ thắng!",
        "duration": 8.0,
        "label": "KẾT THÚC",
        "headline": "Bức Tử",
        "narration": "Bức tử! Tướng Đen hết đường. Sĩ trung tâm bị ghim. Đen không còn nước đi hợp lệ nên bị xử thua. Đỏ thắng!",
        "insight": "Bức tử",
    })
    
    episode = {
        "id": "tap-020",
        "title": "Tập 020: Tam Binh Bức Tử Song Sĩ",
        "subtitle": "Bài Tập Cờ Tàn",
        "category": "Tàn Binh",
        "goal_text": "Bức tử! Đỏ thắng",
        "analysis_status": "draft",
        "fen": fen0,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-020.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
