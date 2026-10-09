import json
from pathlib import Path

history_file = Path('youtube_uploaded_history.json')
data = json.loads(history_file.read_text())

if "thong_ke_04" not in data:
    data["thong_ke_04"] = {
        "title": "STAT04: Tứ Phân Vị Q1, Q2, Q3 | Chia Nhỏ Dữ Liệu - Thầy Nguyễn Văn Sang",
        "video_id": "XGJrRJCbfKE",
        "url": "https://youtu.be/XGJrRJCbfKE",
        "file": "media/videos/scene/1080p30/STAT04.mp4",
        "uploaded_at": "2026-10-09 10:29:27"
    }

history_file.write_text(json.dumps(data, indent=2) + '\n')
