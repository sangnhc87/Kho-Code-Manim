# Video 18 MASTER — Một mặt bị cấm

Bài toán về hộp chữ nhật `8 × 5 × 4`. Từ điểm P trên mặt trước đến Q trên mặt sau, **không được đi trên mặt trên**.

Phương án ngắn nhất khi không cấm mặt nào có độ dài `sqrt(65)` và đi qua nắp trên. Phương án này bị loại.

Đường ngắn nhất hợp lệ đi theo ba mặt `trước → đáy → sau`, có độ dài **`sqrt(137)`**. Hai điểm đổi mặt có hoành độ `34/11` và `54/11`.

## Cách sử dụng

Đặt mã Python vào `Manim-Typst/`, workflow vào `.github/workflows/`, sau đó kích hoạt GitHub Actions bằng `workflow_dispatch` hoặc commit hai tệp.

Pipeline thực hiện kiểm tra cú pháp, lời giảng, công thức Typst, hình học, bố cục, render thử 480p rồi xuất MP4 1080p ghép giọng đọc Edge TTS.

Chưa kiểm chứng render thật trong môi trường tạo tệp; **phải kiểm tra artifact video và nghe lời giảng** sau khi Actions hoàn thành.
