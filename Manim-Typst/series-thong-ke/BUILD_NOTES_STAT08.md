# BUILD NOTES – STAT08

- Kế thừa STAT01–07, không tự ý sửa code cũ.
- `stat08/lesson.py`: tất cả số liệu và lời giảng, không phụ thuộc Manim.
- `stat08/scene.py`: 8 mô hình (32 trạng thái), dùng font Noto Sans và các SVG do Typst sinh.
- `scripts/build_stat08_typst.py`: biên dịch và xác minh 8 SVG thật, thất bại nếu thiếu.
- `scripts/check_stat08_states.py`: kiểm tra 32 hình và lời giải với API mock, **không phải render thật**.
- `STAT08_vi.srt`: phụ đề được tạo theo timeline gốc và sinh lại khi bật TTS.
- `.github/workflows/render-stat08.yml`: buộc chạy kiểm thử và smoke-render mọi trạng thái trước render chính, `ffprobe` xác minh độ dài, độ phân giải và âm thanh.
- Preview là storyboard thiết kế bằng Pillow, không phải ảnh Manim.
- Không gọi bài toán nội suy theo mật độ lớp không đều là công thức chuẩn bắt buộc SGK.
