"""Produce complete narration and 32-beat storyboard from canonical lesson metadata."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat04.lesson import BEATS,CHAPTERS,Q1,Q2,Q3,IQR,validate
validate()

narration=['# THONG-KE-04 – TỨ PHÂN VỊ Q1, Q2, Q3','',
           'Dữ liệu: 40 điểm giả lập của STAT01–03. Quy ước SGK: lấy trung vị của hai nửa; nếu n lẻ, loại trung vị chung trước khi chia.','',
           'Lời giảng được căn theo 32 nhịp trong `stat04/lesson.py`. Khi bật TTS, mỗi nhịp có một tệp âm thanh độc lập.','']
board=['# Storyboard STAT04 – 32 nhịp / 8 chương','',
       '## Tư tưởng sư phạm','',
       'Sắp xếp → Chia đôi → Tìm trung vị mỗi nửa → Kiểm chứng bằng tích lũy → Vận dụng. Các đáp số xuất hiện theo từng nhịp, không tiết lộ trước.','',
       'Mô hình: tối 1920×1080, hai cột; đồ họa dữ liệu bên trái, suy luận + Typst bên phải. Những biểu đồ lớn ưu tiên cột trái.','']
for chapter in range(1,9):
    b=BEATS[(chapter-1)*4:chapter*4]
    narration.append(f'## Chương {chapter:02d} – {CHAPTERS[chapter-1]}')
    board.append(f'## Chương {chapter:02d} – {CHAPTERS[chapter-1]}')
    for k,beat in enumerate(b,1):
        narration.extend(['',f'### Nhịp {k} — {beat.title}','',beat.voice,''])
        board.extend(['',f'### {chapter:02d}.{k} – {beat.title}',
              f'- Kết luận xuất hiện: **{beat.thesis}**',
              f'- Thời lượng nền: **{beat.duration:.0f} giây**; TTS có thể kéo dài.',
              f'- Lời giảng: {beat.voice}',
              '- Hình: cập nhật đối tượng dữ liệu/nhấn mạnh vị trí hoặc điều kiện mới tương ứng với nhịp.',''])
(ROOT/'LOI_GIANG_STAT04.md').write_text('\n'.join(narration)+'\n',encoding='utf-8')
(ROOT/'STORYBOARD_STAT04.md').write_text('\n'.join(board)+'\n',encoding='utf-8')

readme='''# SangMath – Thống kê trực quan 10–12

Bộ nguồn bao gồm **STAT01–STAT04**. Mã nguồn tách dữ liệu/luận giải khỏi Manim để dễ kiểm thử và tái sử dụng.

## Các video
- STAT01: Dữ liệu biết nói – 40 điểm kiểm tra giả lập.
- STAT02: Các biểu đồ thống kê.
- STAT03: Số trung bình, trung vị và mốt.
- **STAT04: Tứ phân vị Q1, Q2, Q3; mẫu chẵn/lẻ; tần số tích lũy; ngoại lệ; IQR.**

## Dữ liệu STAT04
40 điểm kiểm tra *giả lập* giống ba tập trước, N=40, Q1=6, Q2=7, Q3=8, IQR=2.
Xác định bằng trung vị hai nửa: vị trí 10–11, 20–21, 30–31.

Với n lẻ, bỏ trung vị toàn mẫu trước khi chia thành hai nửa. Đây là quy ước sách giáo khoa phổ thông; phần mềm thống kê có thể sử dụng thuật toán tứ phân vị khác.

## Render
Xem `HUONG_DAN_RENDER_STAT04.md`. Chạy `python -m unittest discover -s tests -v` để kiểm tra toán học.

Cảnh chính: `stat04/scene.py` – class `STAT04`. 32 nhịp, 832 giây nền (13:52). Khi bật TTS dùng `edge-tts` và thời lượng cập nhật theo âm thanh thực tế.

Dự án chưa xác nhận render Manim/Typst tại môi trường soạn. **Bản preview từ GitHub phải được duyệt hình, âm thanh và tốc độ** trước khi sử dụng trong lớp.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
series='''# Series Thống kê trực quan – SANGMATH

Dự kiến 18 tập, theo ba khối phổ thông 10–12 và một phần mở rộng.

- STAT01 – Dữ liệu thống kê và bảng tần số: code.
- STAT02 – Các loại biểu đồ: code.
- STAT03 – Trung bình, trung vị, mốt: code.
- STAT04 – Tứ phân vị Q1,Q2,Q3: code.
- STAT05 – Khoảng biến thiên, IQR, biểu đồ hộp: tiếp theo.
- STAT06 – Phương sai, độ lệch chuẩn: dự kiến.
- STAT07–STAT14 – Mẫu số liệu ghép nhóm và vận dụng: dự kiến.
- STAT15–STAT18 – Đọc hiểu biểu đồ, nghịch lý Simpson, tương quan, lấy mẫu: mở rộng.

Cả bốn tập hiện là **mã nguồn GitHub Ready**, chưa phải MP4 Manim được nghiệm thu.
'''
(ROOT/'README_THONG_KE_SERIES.md').write_text(series,encoding='utf-8')
guide='''# HƯỚNG DẪN GITHUB ACTIONS – STAT04

## Cập nhật repository cũ
Nếu đã có STAT01–03, dùng ZIP patch STAT04. Giải nén và chép nội dung vào gốc repository `sangmath-thong-ke`, giữ nguyên cấu trúc `stat01/`, `stat02/`, `stat03/`, `stat04/` và `.github/workflows/`.

Nếu chưa có các tập trước, dùng ZIP trọn bộ STAT01–STAT04. Commit và push lên nhánh chính.

## Chạy render
1. Mở **Actions** → **Render STAT04 - Tu phan vi Q1 Q2 Q3 - Manim Typst** → **Run workflow**.
2. Chọn `quality=preview`, `voice=off` để kiểm tra hình, công thức và mốc thời gian.
3. Tải artifact. Xem 8 ảnh chụp chương và MP4; sửa nếu thấy chữ đè, hiển thị sai dấu, chuyển động quá nhanh/chậm.
4. Chạy lại `voice=on` để có giọng đọc tiếng Việt (cần mạng, edge-tts có thể từ chối hoặc đổi chính sách). Khi lỗi TTS, workflow báo lỗi, **không tự tạo video giả có tiếng**.
5. Sau khi duyệt, chạy `quality=fullhd` xuất 1920×1080, 30 fps.

## Chạy trong máy Linux đã cài Manim / Typst
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_stat04_typst.py
python scripts/prepare_stat04.py --voice off
manim -ql -r 854,480 --fps 24 stat04/scene.py STAT04
VIDEO=$(find media/videos -type f -name STAT04.mp4 | head -n 1)
python scripts/qa_stat04.py --video "$VIDEO" --quality preview --voice off
```

## Kiểm tra kỹ thuật
- `scripts/prepare_stat04.py` tạo `stat04/runtime_plan.json` và `STAT04_vi.srt` khớp 32 nhịp.
- Thời lượng thiết kế **832 giây (13 phút 52 giây)** khi `voice=off`; với TTS có thể kéo dài.
- `scripts/qa_stat04.py` dùng FFprobe kiểm tra độ phân giải, thời lượng, luồng âm thanh nếu bật TTS, sau đó trích 8 ảnh vào `artifacts/stat04_qa/`.
- Kiểm tra kỹ thuật KHÔNG đồng nghĩa video đã đạt chất lượng trình bày và sư phạm.

## Quy ước tứ phân vị
- n chẵn: Q1 và Q3 là trung vị hai nửa có n/2 giá trị.
- n lẻ: loại Q2 trước khi lấy trung vị hai nửa còn lại.
- Trường hợp bộ điểm giả lập: Q1=6, Q2=7, Q3=8. Vị trí tương ứng: 10–11, 20–21, 30–31.
- Khi nhiều quan sát trùng nhau, tránh khẳng định cứng rằng chính xác 25% số quan sát nhỏ hơn Q1.
'''
(ROOT/'HUONG_DAN_RENDER_STAT04.md').write_text(guide,encoding='utf-8')
manifest={'episode':'STAT04','scene':'STAT04','chapters':8,'beats':len(BEATS),
          'silent_target_seconds':sum(b.duration for b in BEATS),
          'q1':Q1,'q2':Q2,'q3':Q3,'iqr':IQR,
          'narration_words':sum(len(b.voice.split()) for b in BEATS),
          'typst_formulas':8,'status':'CODE_TESTED_NOT_RENDERED'}
(ROOT/'STAT04_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(manifest)
