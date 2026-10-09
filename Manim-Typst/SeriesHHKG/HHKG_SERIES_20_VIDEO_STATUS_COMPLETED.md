# HHKG CHUYÊN SÂU — ROADMAP 20 VIDEO — HOÀN THÀNH

## Chặng A — Nền tảng cấu hình và khoảng cách
- [x] 01. Một cấu hình — nhiều đại lượng
- [x] 02. Khoảng cách trong không gian I
- [x] 03. Khoảng cách giữa hai đường chéo nhau

## Chặng B — Góc trong không gian
- [x] 04. Góc trong không gian
- [x] 05. Góc nhị diện chuyên sâu
- [x] 06. Góc nhị diện nâng cao và bài ngược

## Chặng C — Thể tích và tỷ số thể tích
- [x] 07. Thể tích & tỷ số thể tích I
- [x] 08. Tỷ số thể tích nâng cao
- [x] 09. Thể tích từ khoảng cách và góc

## Chặng D — Thiết diện
- [x] 10. Thiết diện I — dựng đúng giao tuyến
- [x] 11. Thiết diện II — diện tích và tỷ số
- [x] 12. Thiết diện III — bài khó, điểm động, cực trị

## Chặng E — Khối tròn và mô hình hình học 3D
- [x] 13. Nón — trụ — cầu — chóp cụt chuyên sâu
- [x] 14. Mô hình thực tế 3D

## Chặng F — Điểm động, cực trị và Oxyz
- [x] 15. Điểm động & cực trị HHKG
- [x] 16. Oxyz như ngôn ngữ thứ hai

## Chặng G — Tổng hợp luyện thi phân hóa cao
- [x] 17. Đúng/Sai HHKG
- [x] 18. Trả lời ngắn HHKG
- [x] 19. Những cấu hình lạ nhưng lời giải đẹp
- [x] 20. Capstone — bản đồ phương pháp HHKG THPT

## Trạng thái
- **20/20 video đã hoàn thành phần source + workflow render.**
- Video 20 đóng vai trò bản đồ ra quyết định: khoảng cách, góc, thiết diện, thể tích, điểm động/cực trị, Oxyz/trải phẳng.

## Chuẩn xuyên suốt
- Manim Community + Typst/MathTypst.
- `inter`, `perp`, `parallel`, `frac(...)`, `hat(...)`.
- Không `sect`, `intersect`, `angle`, không slash fraction trong MathTypst.
- Typst preflight toàn bộ biểu thức tĩnh trước render.
- Hình 3D chuẩn thấy/khuất; đường phụ nét đứt màu nhấn.
- Cung góc trên hình được dựng từ hai tia hình học thật bằng `angle_arc_3d`.
- TTS NamMinh, master audio ghép một lần bằng ffmpeg.
- Mỗi bài theo mạch: đề → chẩn đoán cấu hình → dựng phụ/mặt cắt → chứng minh quan hệ → tính → kiểm tra.
