# HƯỚNG DẪN RENDER VÀ NGHIỆM THU – INT01

## Chủ đề bài học
**Đi ngược đạo hàm – Bản chất của nguyên hàm.** Đối tượng lớp 12. 8 chương/32 phân đoạn. Thời lượng nền **14 phút 24 giây** khi không có tiếng; giọng đọc có thể làm dài hơn.

## Cập nhật repository

Đây là bài đầu tiên của series mới. Giải nén `SangMath_NguyenHam_TichPhan_INT01_GitHubReady.zip` và đưa **nội dung bên trong** vào gốc repository mới trên GitHub, không đặt nguyên ZIP hoặc tạo một thư mục bọc bên ngoài. Phải có `.github/workflows/render-int01.yml`.

## Render trên GitHub Actions

1. Vào **Actions → Render INT01 - Ban chat nguyen ham → Run workflow**.
2. Chọn `quality=preview`, `voice=off` để kiểm thử hình trước. Workflow chạy `unittest`, compile Typst thành SVG, smoke-render bằng Manim thật, render MP4, chạy ffprobe, xuất 8 ảnh QA.
3. Download **Artifacts**. Kiểm tra đủ 8 chương: họ parabol thật sự là phép tịnh tiến lên xuống, tiếp tuyến **song song tại cùng hoành độ**, không bị sai điểm đặt, đồ thị đúng tỉ lệ, công thức Typst không bị tràn, không có chữ đè hình.
4. Chọn `voice=on`, giữ preview, nghe giọng **nam tiếng Việt** `vi-VN-NamMinhNeural` từ đầu đến cuối; đối chiếu phụ đề. Nếu TTS lỗi thì workflow phải thất bại, không được xuất MP4 im lặng.
5. Sau khi preview đạt, chạy `quality=fullhd`, `voice=on` để xuất **1920×1080, 30 FPS**.

## Chuẩn video

- Hai cột cố định: đồ thị bên trái, diễn giải và Typst bên phải.
- Footer chính xác **Thầy Nguyễn Văn Sang**.
- Không hiện từ "nhịp", số phân đoạn, `Scene`, `Manim–Typst`, label debug hoặc tên công nghệ trong video.
- Bài tập cuối **chỉ hiện hàm kết quả sau khi đã hướng dẫn lập luận**.
- Các kết luận về hiệu nguyên hàm là hằng số được áp dụng **trên một khoảng**.

## Các phép tính chuẩn

- `d/dx(x²+C)=2x` với mọi hằng số C.
- Với `F₁=x²−1` và `F₂=x²+2`, hiệu bằng `3` với mọi x.
- `F(1)=3`, `F(x)=x²+C` ⇒ `C=2`, `F(x)=x²+2`.
- `v(t)=2t+1`, `s(0)=2` ⇒ `s(t)=t²+t+2`.
- `G′(x)=3x²`, `G(1)=5` ⇒ `G(x)=x³+4`.

## Lệnh cục bộ Linux

```bash
python -m pip install -r requirements.txt
python scripts/prepare_int01.py --voice off
python -m unittest discover -s tests -v
python scripts/build_int01_typst.py
manim -ql -r 426,240 --fps 8 int01/scene.py INT01_SMOKE
manim -ql -r 854,480 --fps 24 int01/scene.py INT01
VIDEO=$(find media/videos -type f -name INT01.mp4 | head -n 1)
python scripts/qa_int01.py --video "$VIDEO" --quality preview --voice off
```

## Ranh giới nghiệm thu

Môi trường tạo gói **không có Manim, Typst, không cài qua mạng được**, nên các kiểm tra hiện tại mới là cú pháp, dữ liệu, toán học, tệp và ảnh storyboard. **Chưa xác minh bằng render thật.** GitHub Actions được thiết kế để thực hiện smoke-render và render MP4 thực tế, sau đó thầy cần duyệt trực quan và nghe thử trước khi đưa vào dạy học.
