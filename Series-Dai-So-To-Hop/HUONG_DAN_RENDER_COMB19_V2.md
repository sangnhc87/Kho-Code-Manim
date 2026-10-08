# Hướng dẫn render COMB19 V2 trên GitHub Actions

## 1. Gói dành cho repository cũ

Bản cập nhật này bổ sung COMB19 vào bộ COMB01–COMB18 và GEO01. **Không cần tạo repository mới**.
Giải nén ZIP, chép **toàn bộ nội dung**, bao gồm thư mục ẩn `.github`, vào gốc repository hiện có, commit và push.

## 2. Chạy workflow

1. Vào **Actions** trên GitHub.
2. Chọn **Render COMB19 V2 - Tap con va cong thuc 2 mu n**.
3. Chọn **Run workflow** với `quality=preview`, `voice=off`.
4. Sau khi kiểm tra khung hình trong Artifacts, mới chạy `voice=on` để kiểm tra lời giảng.
5. Cuối cùng chọn `quality=fullhd` (1920×1080, 30 FPS) để xuất bản.

Workflow dùng Python 3.11, Manim Community, Typst, FFmpeg và font Noto Sans. File Scene là
`episodes/comb19_subsets.py`, lớp `COMB19`.

## 3. Chạy thủ công trên máy có Manim/Typst

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb19_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb19_subsets.py COMB19
```

Nếu có truy cập dịch vụ Edge TTS, có thể chạy `--voice on`. TTS ngoài mạng có thể chậm hoặc thất bại tạm thời; hãy render không tiếng để duyệt hình trước.

## 4. File đầu ra và kiểm tra

- MP4: `media/videos/**/COMB19.mp4`.
- 8 ảnh theo chương, contact sheet, báo cáo: `qa_comb19_v2/`.
- Lời giảng: `narration_COMB19_v2.md`.
- Phụ đề: `subtitles_COMB19_v2.srt`.
- Manifest thời lượng: `voice/comb19_voice_manifest.json`.

Workflow tự kiểm tra có MP4, thời lượng tối thiểu 18 phút 20 giây, độ phân giải và luồng âm thanh khi `voice=on`.

**Lưu ý nghiệm thu:** thời lượng nền dự kiến 19:17 và 3525 từ thuyết minh chỉ là **dữ liệu thiết kế**, chưa có MP4 Manim được render thực tế trong môi trường biên soạn. Ảnh storyboard là minh họa bố cục, không thay thế kiểm tra video render.
