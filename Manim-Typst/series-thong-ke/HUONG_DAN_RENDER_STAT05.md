# Render STAT05 – Khoảng biến thiên, khoảng tứ phân vị, biểu đồ hộp

## Thêm vào repository `sangmath-thong-ke`

**Cách A:** tải ZIP trọn bộ STAT01–STAT05, giải nén, chép **nội dung bên trong** vào gốc repository và commit/push.

**Cách B:** nếu đã có STAT01–STAT04, dùng ZIP *patch STAT05*; giải nén và chép các tệp vào đúng thư mục gốc repository.

Giữ nguyên đường dẫn `.github/workflows/render-stat05.yml`. Không tạo thư mục lồng thêm khi upload lên GitHub.

## Chạy GitHub Actions

1. Vào **Actions → Render STAT05 - Khoang bien thien - IQR - Boxplot**.
2. Bấm **Run workflow**; chọn `quality=preview`, `voice=off` để thử hình trước.
3. Pipeline lần lượt: cài phụ thuộc → chạy kiểm thử tất cả 5 tập → **biên dịch tám SVG Typst** → chuẩn bị 32 nhịp → **render-smoke đủ 32 trạng thái** ở 426×240 → render bài hoàn chỉnh → FFprobe kiểm tra thời lượng/độ phân giải → trích tám ảnh QA.
4. Tải **Artifacts → STAT05-preview-voice-off**, mở MP4 và kiểm tra tám ảnh, các công thức, dấu tiếng Việt, số liệu.
5. Nếu đạt, chạy `voice=on` để tạo giọng đọc `vi-VN-HoaiMyNeural`. Nếu mạng/TTS lỗi, workflow sẽ **báo đỏ**, không phát hành video giả có tiếng. Cuối cùng dùng `quality=fullhd` để xuất 1920×1080/30fps.

**Thời lượng gốc:** 32 nhịp × 27 giây = 864 giây (14:24). Khi bật giọng đọc, chương trình sẽ kéo dài nhịp cần thiết theo độ dài âm thanh. `.srt` là phụ đề tiếng Việt khớp thời lượng các nhịp; không phải căn từng âm tiết.

## Lệnh kiểm thử và render trực tiếp (Ubuntu)

```bash
python -m unittest discover -s tests -v
python scripts/build_stat05_typst.py
python scripts/prepare_stat05.py --voice off
manim -ql -r 426,240 --fps 8 stat05/scene.py STAT05_SMOKE
manim -ql -r 854,480 --fps 24 stat05/scene.py STAT05
# Sau khi xem thử:
manim -qh -r 1920,1080 --fps 30 stat05/scene.py STAT05
```

## Chuẩn toán học và cách đọc hộp

- Bộ gốc 40 điểm giả lập: min=4, Q1=6, Q2=7, Q3=8, max=10. R=6, IQR=2.
- Ngưỡng Tukey: 3 và 11. Bộ gốc không có ngoại lệ; hai râu từ 4 đến 10.
- Thí nghiệm đổi **một điểm 10 thành 30**: R=26, IQR vẫn 2; một điểm ngoại lệ là 30. Râu **vẫn là 4 đến 10** vì một điểm 10 khác còn lại.
- Hai mẫu minh họa khác có trung vị 5,5 nhưng IQR 4 và 8.
- Bài luyện tập: 11 điểm `2,4,4,5,5,6,7,8,8,9,20`; R=18, IQR=4, ngoại lệ=20, râu Tukey từ 2 đến 9.
- **Không nhầm:** biểu đồ hộp năm mốc kéo râu đến cực trị; boxplot Tukey phân biệt điểm ngoại lệ và đặt râu tại quan sát còn lại xa nhất nằm trong hàng rào.

## Khi build lỗi

| Bước đỏ | Hướng xử lý |
|---|---|
| Install packages | Kiểm tra phiên bản Python và log cài Cairo/Pango/Manim. |
| Unit tests | Dữ liệu không đồng bộ; kiểm tra thay đổi trong `stat01/lesson.py` hoặc `stat04/lesson.py`. |
| Compile STAT05 Typst | Mở log báo file `.typ` lỗi; tám công thức luôn được tạo/biên dịch lại, không nuốt lỗi. |
| Smoke-render STAT05_SMOKE | Xem traceback sẽ chỉ ra cảnh hình hoặc SVG không dựng được. Smoke kiểm tra **đủ 32 trạng thái**, không chỉ tập đầu. |
| Render Full HD | Gửi traceback cuối và tên scene; lỗi chất lượng hình có thể không được test tự động phát hiện. |
| QA duration | So thời lượng dự kiến trong `stat05/runtime_plan.json` và video thực. |
| TTS | `edge-tts` cần mạng Internet, thời lượng dịch vụ có thể thay đổi. |

**Giới hạn của bộ giao:** Môi trường soạn hiện tại chưa có Manim/Typst và không thể tải qua Internet để render MP4 thật. Kiểm thử Python/toán học và cú pháp workflow **không thay cho nghiệm thu thực tế**. Quy trình smoke của GitHub giúp tìm lỗi dựng hình sớm, song vẫn phải duyệt ảnh/âm thanh/chữ trong MP4.
