import json
from pathlib import Path

history_file = Path('youtube_uploaded_history.json')
data = json.loads(history_file.read_text())

if "thong_ke_05" not in data:
    data["thong_ke_05"] = {
        "title": "STAT05: Khoảng Biến Thiên, IQR & Biểu Đồ Hộp | Đo Độ Phân Tán Dữ Liệu - Thầy Nguyễn Văn Sang",
        "video_id": "dIsNe8bP-8Y",
        "url": "https://youtu.be/dIsNe8bP-8Y",
        "file": "media/videos/scene/1080p30/STAT05.mp4",
        "uploaded_at": "2026-10-09 10:26:28"
    }

history_file.write_text(json.dumps(data, indent=2) + '\n')
