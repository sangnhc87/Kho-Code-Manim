"""Emit teacher narration and storyboard from single lesson source."""
from __future__ import annotations
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat03.lesson import BEATS, CHAPTERS, N, MEAN, MEDIAN, MODES, validate

def main():
    validate()
    lines=['# THONG-KE-03 — Lời giảng tiếng Việt',
           '', '**Tên bài:** Số trung bình – Trung vị – Mốt',
           '', '**Dữ liệu chính:** 40 điểm giả lập dùng từ STAT01.',
           '', '**Dữ liệu thứ hai:** chín thời lượng luyện tập giả lập (không phải điểm).',
           '', '> Đề nghị duyệt tốc độ đọc TTS và bảng phụ đề trước khi xuất bản.', '']
    story=['# THONG-KE-03 — Storyboard đầy đủ 32 nhịp',
           '', 'Bố cục: mô hình toán bên trái, lập luận/công thức bên phải.',
           'Cảnh ngoại lệ dùng ValueTracker; những phần khác biến đổi từng trạng thái.',
           'Tám chương, mỗi chương bốn nhịp. Thời lượng nền 800 giây = 13:20.', '']
    for i,b in enumerate(BEATS):
        if b.step==1:
            lines.extend([f'## Chương {b.chapter:02d} — {CHAPTERS[b.chapter-1]}',''])
            story.extend([f'## Chương {b.chapter:02d} — {CHAPTERS[b.chapter-1]}',''])
        lines.extend([f'### Nhịp {i+1:02d} — {b.title}','',f'**Ý chính:** {b.thesis}','',b.voice,''])
        story.extend([f'### Nhịp {i+1:02d} ({b.duration:.0f} giây) — {b.title}',
                      f'- **Thông điệp trên màn hình:** {b.thesis}',
                      f'- **Lời giảng:** {b.voice}',
                      f'- **Hình động:** Chương {b.chapter} — trạng thái {b.step} của mô hình dữ liệu; '+
                      ('kéo ngoại lệ và cập nhật trung bình trực tiếp.' if b.chapter==5 and b.step==2 else 'hiện lập luận sau quan sát.'), ''])
    (ROOT/'LOI_GIANG_STAT03.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (ROOT/'STORYBOARD_STAT03.md').write_text('\n'.join(story)+'\n',encoding='utf-8')
    print('Generated STAT03 docs: 32 narrations, 8 chapters',len(' '.join(b.voice for b in BEATS).split()),'words')
if __name__=='__main__':main()
