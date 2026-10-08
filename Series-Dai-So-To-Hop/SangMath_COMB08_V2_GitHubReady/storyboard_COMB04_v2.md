# Storyboard COMB04 V2 — Khi nào thứ tự quan trọng?

## Mục tiêu đầu ra

Học sinh nêu được điều kiện có/không xét thứ tự; giải thích AB khác BA trong bài phân công trưởng–phó nhưng là một nhóm trong bài chọn đội; biết từ danh sách có thứ tự gom lại những trường hợp biểu thị cùng một nhóm; tránh chia nhầm khi không có tính đồng đều.

## Tám chương

| Chương | Nhịp | Hình động chủ đạo | Toán học / đáp số |
|---|---|---|---|
| 01. Hai câu hỏi | 01–06 | 4 học sinh, hai bộ nhãn: đội và trưởng/phó | Định nghĩa một kết quả |
| 02. Phân công | 07–12 | Mở 4×3 bảng các cặp AB, AC..., tô cặp đảo | 4×3=12 |
| 03. Chọn đội | 13–18 | Ghép từng cặp AB–BA, tạo sáu lớp tương đương | 12÷2=6 |
| 04. Hoán đổi | 19–24 | Đổi thẻ qua hai ô giữ nguyên vai trò; đổi trong khung đội | Kết quả đổi hay không? |
| 05. Chọn ba trong năm | 25–30 | Sáu hoán vị ABC thu về một nhóm; 10 nhóm | 60÷3!=10 |
| 06. Sáu học sinh | 31–36 | 30 phân công so với bảng 15 nhóm | 30÷2=15 |
| 07. Đội trưởng | 37–42 | Tách đội trưởng và thành viên thường; đếm hai cách | 8×21=56×3=168 |
| 08. Ôn tập | 43–48 | Ba câu quiz + sơ đồ quyết định | 6, 20, 10; dẫn sang video 05 |

## Kỹ thuật hình động

- Hình bên trái chiếm 45%, lời giải bên phải 55%, font Noto Sans, công thức Typst.
- Mỗi nhịp có hình trạng thái riêng và chuyển động trọng tâm (`Indicate` hoặc `Swap`), rồi lần lượt lộ ba ý giải thích và kết luận. Không đặt toàn bộ chứng minh ở màn hình ngay từ đầu.
- Màu cyan: đối tượng/nhóm được xét; vàng: kết quả, vai trò; tím: hoán đổi/gom; xanh lá: nhóm hợp lệ.
- Nguồn sự thật là `comb04_beats.json` và `comb04_lesson_data.py`. Video dùng đúng thuyết minh đó để tạo TTS/SRT.
- Không giả sử mọi bài có chữ “chọn” đều không xét thứ tự; không xem hai thành viên không có vai trò là hai kết quả chỉ vì đổi chỗ trên hình.

**Kết quả kiểm thử:** do GitHub Actions chạy lại. **Yêu cầu nghiệm thu:** xem MP4 và contact sheet rồi mới công bố.
