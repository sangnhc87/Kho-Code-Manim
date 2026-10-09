# SangMath THONG-KE-08 – Hướng dẫn render và rà lỗi

**Bài:** Số trung bình và mốt của mẫu số liệu ghép nhóm (lớp 11).

## Cập nhật repository

- Nếu GitHub đã có STAT01–STAT07, dùng `SangMath_ThongKe_STAT08_Patch_GitHubReady.zip`. Giải nén tại thư mục gốc repo, giữ cấu trúc `.github/workflows`, `stat08`, `scripts`, `tests`, `typst`, `preview`.
- Nếu muốn một repository mới đủ 8 tập, dùng `SangMath_ThongKe_STAT01_STAT08_GitHubReady.zip`.
- Không mở ZIP để commit chính tệp ZIP; cần tải các tệp bên trong lên repo, bao gồm **thư mục ẩn `.github`**.

## Chạy GitHub Actions

**Actions → Render STAT08 - Trung binh va Mot mau ghep nhom → Run workflow**.

1. Chọn `quality: preview`, `voice: off` để kiểm tra trước.
2. Workflow thực thi theo thứ tự: cài hệ thống → kiểm thử Python → kiểm tra 32 trạng thái Manim bằng mock → **biên dịch thật 8 công thức Typst** → chuẩn bị 32 nhịp → **smoke-render thật 32 trạng thái** → render bài → `ffprobe` xác minh MP4 → xuất 8 ảnh QA.
3. Tải MP4 và các ảnh từ **Artifacts**. Duyệt công thức, nhịp giảng và việc lớp mốt được tô vàng.
4. Chạy `voice: on` để kiểm tra giọng đọc tiếng Việt; workflow sẽ báo lỗi nếu TTS không tạo được âm thanh.
5. Khi bản preview đạt, chuyển `quality: fullhd` xuất 1920×1080 / 30fps.

## Tự kiểm thử trong môi trường có công cụ

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/check_stat08_states.py
python scripts/build_stat08_typst.py
python scripts/prepare_stat08.py --voice off
manim -ql -r 426,240 --fps 8 stat08/scene.py STAT08_SMOKE
manim -ql -r 854,480 --fps 24 stat08/scene.py STAT08
```

## Kiến thức cần duyệt kỹ

- Dữ liệu gốc: trung bình **7,1**, mốt **7**.
- Bảng nhóm `[4;6), [6;8), [8;10), [10;12)` có `6,18,14,2`, trung bình ghép nhóm **7,6**, lớp mốt `[6;8)`, mốt **nội suy 7,5**.
- Bảng thay ranh giới `[4;6), [6;7), [7;9), [9;11)` có `6,8,18,8`, trung bình ghép nhóm **7,65**, mật độ `3,8,9,4`. Nội suy theo mật độ **7,333...** chỉ là **mở rộng**, không đồng nhất với quy tắc SGK cho lớp đều.
- Bài luyện `5,7,6,2`, trung bình ghép nhóm **5,5**, mốt nội suy **5,333...**.

## Lưu ý về mức độ kiểm thử

Các bài thử Python và mock không phải bằng chứng Manim/Typst đã render thành công. Chỉ khi bước **Compile Typst + Smoke render** trên GitHub thực sự xanh và ảnh QA đúng hình học, công thức, chữ tiếng Việt, mới có thể nghiệm thu bản video. Thời lượng hình nền thiết kế 16:00, chế độ `voice:on` có thể dài hơn tùy tốc độ đọc.
