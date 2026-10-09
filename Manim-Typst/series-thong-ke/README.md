# SangMath – Series Thống kê trực quan 10–11–12

Bộ nguồn có **STAT01–STAT05**. Các tập sử dụng chung dữ liệu tổng hợp 40 điểm kiểm tra giả lập, với mỗi tập đi sâu một chủ đề. Code toán học (pure Python) được tách khỏi Manim để test độc lập.

- STAT01 – Dữ liệu biết nói: bảng tần số và biểu đồ.
- STAT02 – Các loại biểu đồ và cách tránh hình gây hiểu lầm.
- STAT03 – Số trung bình, trung vị, mốt và ngoại lệ.
- STAT04 – Tứ phân vị Q1, Q2, Q3 của dữ liệu không ghép nhóm.
- **STAT05 – Khoảng biến thiên, khoảng tứ phân vị, biểu đồ hộp và ngoại lệ theo Tukey.**

## Video 05

- 32 nhịp / tám chương / 864 giây thời lượng nền, cộng thời gian TTS nếu cần.
- Dữ liệu gốc: `stat01/lesson.py`; thuật toán tứ phân vị lấy từ `stat04/lesson.py`.
- Các phân phối mới là dữ liệu **giả lập độc lập**, có chú giải trong lời giảng.
- Quy ước tứ phân vị: trung vị của hai nửa; cỡ mẫu lẻ không dùng quan sát chính giữa trong cả hai nửa.
- Quy ước râu Tukey: quan sát hợp lệ xa nhất, không phải tọa độ ngưỡng 1,5×IQR.
- Giữ nguyên mã và workflow của STAT01–STAT04.

**Mã Manim:** `stat05/scene.py` (Scene `STAT05`, `STAT05_SMOKE`).

**Nguồn dữ liệu:** `stat05/lesson.py`.

**Kiểm thử:** `python -m unittest discover -s tests -v`.

**Hướng dẫn render:** [`HUONG_DAN_RENDER_STAT05.md`](HUONG_DAN_RENDER_STAT05.md).

**Lời thuyết minh:** [`LOI_GIANG_STAT05.md`](LOI_GIANG_STAT05.md).

**Storyboard:** [`STORYBOARD_STAT05.md`](STORYBOARD_STAT05.md).

MP4 phải được render/nghiệm thu trên GitHub Actions. Chưa thể đảm bảo không có lỗi trên runner chỉ từ kiểm thử Python.
