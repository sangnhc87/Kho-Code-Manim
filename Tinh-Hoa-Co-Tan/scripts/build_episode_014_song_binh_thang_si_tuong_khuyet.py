import json
from pathlib import Path

def main():
    fen0 = "2b1k4/9/3P1P3/9/9/9/9/9/9/3K5 w"
    
    beats = []
    
    beats.append({
        "fen": fen0,
        "text": "Song Binh khéo thắng Sĩ Tượng khuyết: Hai Tốt kiểm soát 2 sườn, Tướng khống chế.",
        "duration": 6.0
    })
    
    fen1 = "2b1k4/3P5/5P3/9/9/9/9/9/9/3K5 b"
    beats.append({
        "fen": fen0,
        "moves": ["d2d1"],
        "text": "Đỏ đi Binh 6 tiến 1! Nước cờ áp sát cung thành, ép Tướng Đen.",
        "duration": 5.0
    })
    
    fen2 = "2b2k3/3P5/5P3/9/9/9/9/9/9/3K5 w"
    beats.append({
        "fen": fen1,
        "moves": ["e0f0"],
        "text": "Tướng Đen buộc phải dạt sang lộ 4 (f0).",
        "duration": 5.0
    })
    
    fen3 = "2bP1k3/9/5P3/9/9/9/9/9/9/3K5 b"
    beats.append({
        "fen": fen2,
        "moves": ["d1d0"],
        "text": "Đỏ tiếp tục Binh 6 tiến 1 xuống đáy. Tốt lụt khóa chặt đường về trung lộ của Tướng Đen.",
        "duration": 5.0
    })
    
    fen4 = "3P1k3/9/b4P3/9/9/9/9/9/9/3K5 w"
    beats.append({
        "fen": fen3,
        "moves": ["c0a2"],
        "text": "Tướng Đen hết nước đi, đành thoái Tượng (Tượng 3 thoái 1).",
        "duration": 5.0
    })
    
    fen5 = "3P1k3/5P3/b8/9/9/9/9/9/9/3K5 b"
    beats.append({
        "fen": fen4,
        "moves": ["f2f1"],
        "text": "Đỏ đi Binh 4 tiến 1. Tuyệt sát! Đỏ thắng.",
        "duration": 6.0
    })
    
    episode = {
        "title": "Tập 014: Song Binh Khéo Thắng Sĩ Tượng Khuyết",
        "fen": fen0,
        "beats": beats
    }
    
    out_dir = Path("episodes")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tap-0014.json"
    out_file.write_text(json.dumps(episode, ensure_ascii=False, indent=2))
    print(f"Wrote {out_file}")

if __name__ == '__main__':
    main()
