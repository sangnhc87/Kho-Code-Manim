# Manim trên GitHub Codespaces — Thầy Nguyễn Văn Sang

Bộ này có hai video hoàn chỉnh: tâm tỉ cự Oxyz (15 bài có lời giải) và tốc độ nước dâng (12 mô hình 3D, dùng diện tích mặt thoáng). Mã hình và lời giảng giữ nguyên từ bản Colab đã gửi; bổ sung cách chạy Codespaces.

## Lần đầu trên Codespace đang dùng

1. Mở Terminal trong Codespaces. Làm việc trong thư mục dự án dưới `/workspaces`.
2. Kéo file `manim_codespaces.zip` vào Explorer bên trái để upload.
3. Chạy:

```bash
python3 -m zipfile -e manim_codespaces.zip .
cd manim_codespaces
bash setup_codespaces.sh
```

Bộ cài tạo môi trường Python tại `~/.local/share/manim-teaching-019/venv` (hoặc dưới `XDG_DATA_HOME` nếu đã đặt), ngoài repo, dùng chung cho cả hai video, cài Manim 0.19.0, FFmpeg, LaTeX, phông tiếng Việt và giọng đọc Edge TTS. Log cài đặt nằm ở `~/.local/share/manim-teaching-019/logs/setup.log`; đường dẫn thực tế được in khi chạy. Cuối quá trình, bộ cài tự render một đoạn thử nhỏ để kiểm tra chữ Việt, công thức, hình 3D và MP4; không mở xem đoạn thử.

Lần sau mở lại **cùng Codespace**, không cần cài lại. Nếu chạy lại bộ cài khi môi trường còn đủ, nó kiểm tra rồi thoát. Nếu rebuild container hoặc tạo Codespace mới thì chạy lại lệnh cài; môi trường hệ thống có thể đã mất. Repo chỉ chứa mã và hướng dẫn. Môi trường Python nằm ngoài repo, còn video, audio, log render và cache nằm trong `/tmp/manim-video-output`. Dữ liệu này là tạm: tải video trước khi xóa/rebuild Codespace; không dùng thư mục tạm làm nơi lưu lâu dài.

## Những lần render sau

Mở Terminal tại thư mục `manim_codespaces` rồi chạy **một** trong hai lệnh:

```bash
bash render.sh oxyz
```

```bash
bash render.sh nuoc
```

Cả hai lệnh mặc định xuất **1080p, 30 fps**. Không nhúng video vào trang, không mở trình phát, không tự tải. Terminal chỉ in các mốc chính và một dòng sau mỗi chương; log chi tiết được ghi ra file. Chỉ cho một render của bộ này chạy cùng lúc để tránh vô tình chạy trùng hoặc ghi chồng video.

Chọn bản xem thử hoặc một bài để thử trước:

```bash
bash render.sh oxyz preview B01
bash render.sh nuoc preview B08
```

Chọn 720p/24 fps:

```bash
bash render.sh nuoc standard
```

Tham số thứ ba có thể là `B01,B02` để chỉ dựng các bài đó. Bỏ tham số này và dùng Terminal không có biến `MANIM_LESSONS` tùy chỉnh để dựng đủ. Không cần sửa phần nội dung trong file `.py`.

## Tải video về máy

Chờ Terminal báo **HOÀN TẤT**. Thêm thư mục tạm vào Explorer bằng lệnh sau; thao tác này không đưa file vào Git:

```bash
code --add /tmp/manim-video-output
```

Trong Explorer, mở thư mục vừa thêm rồi tìm:

- `/tmp/manim-video-output/Oxyz_Tam_Ti_Cu/oxyz_tam_ti_cu_hay_la_kho.mp4`
- `/tmp/manim-video-output/Nuoc_Dang_3D_Mat_Thoang/toc_do_nuoc_dang_3d_dien_tich_mat_thoang.mp4`

Chuột phải đúng file MP4 → **Download…**. Có thể tải phụ đề SRT/VTT, mục lục TXT và ZIP mã nguồn trong cùng thư mục. Không cần mở MP4 trong trình soạn thảo, không cần mở port hoặc tạo web server.

## Tải xong thì dọn dữ liệu tạm

Sau khi đã tải MP4 và kiểm tra file trên máy cá nhân, chạy:

```bash
bash cleanup_outputs.sh
```

Lệnh này xóa video, phụ đề, âm thanh, cache và log render của **cả hai bài**, chỉ trong thư mục kết quả của bộ này. Nó không xóa repo hay môi trường Python. Nếu muốn dùng lại cache, chưa chạy lệnh dọn. Không tự xóa ngay sau render vì chương trình không xác nhận được việc tải xuống đã thành công.

## Cache và chạy lại

Chạy lại cùng lệnh sẽ dùng các câu đọc và chương đã hoàn tất còn trong thư mục `/tmp/manim-video-output`. Thay nội dung hoặc chất lượng sẽ tạo một phiên render khác. Nếu bị ngắt giữa một chương, chương đó phải làm lại; không mất các chương đã hoàn tất và cache còn hợp lệ.

Không có JavaScript giữ phiên. Nếu Codespace bị dừng/tự hết thời gian chờ, tiến trình render dừng; mở lại rồi chạy lệnh để dùng cache. Đóng tab không phải cam kết tiến trình sẽ chạy mãi. Khi video đã tải xong, có thể dừng Codespace trong giao diện GitHub.

## Tốc độ

Codespaces không tự động nhanh hơn Colab. Tốc độ phụ thuộc CPU được cấp và độ phức tạp hình; thêm lõi không bảo đảm tốc độ tăng theo tỉ lệ vì nhiều đoạn Manim xử lý tuần tự. Bộ này chưa tự đổi cấu hình máy hoặc mức sử dụng của tài khoản.

Kiểm tra số CPU trong Terminal:

```bash
nproc
lscpu
```

1080p/30 fps đẹp hơn nhưng render lâu hơn 720p/24 fps. Việc này chạy trên máy cloud; trình duyệt chỉ hiển thị Terminal. Không cam kết máy cá nhân mát 100%.

## Kiểm tra và xử lý lỗi

```bash
"${XDG_DATA_HOME:-$HOME/.local/share}/manim-teaching-019/venv/bin/python" check_environment.py
"${XDG_DATA_HOME:-$HOME/.local/share}/manim-teaching-019/venv/bin/python" oxyz_tam_ti_cu_hay_la_kho.py --check
"${XDG_DATA_HOME:-$HOME/.local/share}/manim-teaching-019/venv/bin/python" toc_do_nuoc_dang_3d_dien_tich_mat_thoang.py --check
```

Nếu báo thiếu môi trường, chạy lại `bash setup_codespaces.sh`. Nếu giọng đọc bị lỗi mạng/dịch vụ, chạy lại lệnh render; các câu đã tạo vẫn có cache. Edge TTS cần Internet khi tạo giọng lần đầu, và bộ cài cần Internet tải thư viện.

Hai file `.py` vẫn chạy được trên Colab theo hướng dẫn ở đầu file. Khi chạy trực tiếp trên Codespaces, dùng Python trong môi trường riêng ở trên hoặc `render.sh`, không dùng Python hệ thống chưa có thư viện. Chốt mặc định chỉ cho phép cloud, tránh vô tình dựng video trên Mac cá nhân.

Kiểm tra trước khi bàn giao: cú pháp Python/shell, kiểm chứng toán, nội dung/Scene không đổi, nhận diện Codespaces, đường dẫn kết quả, phần hướng dẫn tải và nhánh cài dùng lại. Chưa chạy bộ cài hoặc render trọn video trong Codespace riêng của người dùng.

## Tài liệu chính thức

- Nhận diện môi trường: https://docs.github.com/en/codespaces/developing-in-a-codespace/default-environment-variables-for-your-codespace
- Dữ liệu sau rebuild: https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace
- Tải file từ Explorer: https://docs.github.com/en/codespaces/troubleshooting/github-codespaces-logs
- Đổi loại máy: https://docs.github.com/en/codespaces/customizing-your-codespace/changing-the-machine-type-for-your-codespace
