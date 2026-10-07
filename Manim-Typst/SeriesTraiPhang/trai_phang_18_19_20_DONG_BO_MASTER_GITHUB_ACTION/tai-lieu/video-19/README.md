# Trải Phẳng 19 MASTER — Hộp chữ nhật có tham số

**Bài toán:** hộp chữ nhật `4 × 6 × t`, với `2 ≤ t ≤ 10`; đường đi trên mặt ngoài từ A đến đỉnh đối diện G.

Ba bản trải: `(t+4)×6`, `10×t`, `(t+6)×4`.

Chiều cao chuyển phương án: **t = 6**.

`L_min(t)=sqrt((t+4)^2+36)` với `2≤t≤6`.

`L_min(t)=sqrt(t^2+100)` với `6≤t≤10`.

Tại t=6: `L_min=2sqrt(34)` và tồn tại nhiều đường đi khác nhau cùng tối ưu.

## Cách chạy GitHub Actions

Đưa file Python vào `Manim-Typst/`. Đưa workflow vào `.github/workflows/`, commit và chọn Run workflow. Các bước bao gồm kiểm tra Python, lời giảng, cú pháp MathTypst, tiền kiểm hình học, tiền kiểm bố cục, smoke render 480p, render 1080p, tạo audio Edge TTS và ghép audio một lần.

**Lưu ý:** Cấu trúc một cột hình học 3D và một cột công thức cố định, không đọc thuật ngữ kỹ thuật trong lời thoại. Đây là gói source/workflow; chưa khẳng định render thành công khi chưa chạy GitHub Actions.
