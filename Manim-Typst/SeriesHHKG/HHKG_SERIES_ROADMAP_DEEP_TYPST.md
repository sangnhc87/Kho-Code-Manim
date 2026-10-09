# HHKG CHUYÊN SÂU — MANIM + TYPST

## Chuẩn chung của toàn series

- Mỗi video mục tiêu **10–15 phút**, các video tổng hợp có thể 15–18 phút.
- Hình 3D phải có quy tắc thống nhất: cạnh thấy nét liền, cạnh khuất nét đứt trung tính, đường phụ/hình chiếu nét đứt màu nhấn, mặt phẳng tô trong suốt nhẹ.
- Giữ góc camera dạy học cố định trong một cấu hình nếu việc quay camera làm thay đổi trạng thái thấy/khuất.
- Nội dung toán dùng `MathTypst`; tiếng Việt dùng `Text`.
- Phân số dùng `frac(...)`, giao dùng `inter`, góc phẳng dùng `hat(...)`; không dùng `sect`, `intersect`, `angle`, không dùng slash fraction trong biểu thức toán.
- Mỗi workflow có **Typst math preflight** và tự compile toàn bộ biểu thức Typst tĩnh trước khi render.
- Mỗi bài theo mạch: **đề bài → nhìn cấu hình → dựng đường/mặt phụ → chứng minh lựa chọn → tính toán → chốt mẫu nhận dạng**.
- Ưu tiên bài có nhiều cách nhìn, bài đảo ngược, điểm động, bất biến, cực trị và mô hình thực tế.

## Chặng A — Nền tảng cấu hình và khoảng cách

### 01. Một cấu hình — nhiều đại lượng
Góc đường–mặt, góc nhị diện, thể tích, khoảng cách điểm–mặt, thiết diện song song, tỷ số thể tích.

### 02. Khoảng cách trong không gian I
Điểm–mặt, đường–mặt song song, mặt phẳng phụ, đổi khoảng cách thành thể tích, khoảng cách bất biến theo điểm động.

### 03. Khoảng cách giữa hai đường chéo nhau
Đường vuông góc chung, mặt phẳng song song chứa một đường, hình lập phương, tứ diện đều, tứ diện vuông, điểm động.

## Chặng B — Góc trong không gian

### 04. Góc trong không gian
Hai đường, đường–mặt, hai mặt, hình chiếu, đường chéo nhau, góc biến thiên theo điểm động.

### 05. Góc nhị diện chuyên sâu
Định nghĩa qua mặt cắt vuông góc cạnh chung, chóp vuông, chóp đều, tứ diện đều, hình lập phương, tham số chiều cao, mô hình mặt dốc.

### 06. Góc nhị diện nâng cao và bài ngược
Nhiều cạnh chung khó thấy, lăng trụ xiên, chóp có đáy tam giác, góc nhị diện cho trước để tìm chiều cao/cạnh, so sánh hai góc nhị diện, điểm động làm góc đạt cực trị.

## Chặng C — Thể tích và tỷ số thể tích

### 07. Thể tích & tỷ số thể tích I
Cùng đáy, cùng chiều cao, đổi đỉnh, đổi đáy, tỷ số theo chiều cao, chóp cụt, đồng dạng.

### 08. Tỷ số thể tích nâng cao
Phân chia tứ diện, điểm trên cạnh theo tham số, định lý thể tích kiểu Menelaus/Ceva ở mức phổ thông, các bài không cần tính thể tích tuyệt đối.

### 09. Thể tích từ khoảng cách và góc
Kết nối thể tích với khoảng cách điểm–mặt, diện tích hình chiếu, góc đường–mặt, góc nhị diện; bài ngược tìm khoảng cách/góc từ thể tích.

## Chặng D — Thiết diện

### 10. Thiết diện I — dựng đúng giao tuyến
Mặt phẳng qua ba điểm, qua đường và điểm, song song đường/mặt; quy trình tìm giao tuyến có kiểm soát.

### 11. Thiết diện II — diện tích và tỷ số
Thiết diện của chóp, lăng trụ, hình hộp; hình thang, hình bình hành, tam giác; đồng dạng và tỷ số diện tích.

### 12. Thiết diện III — bài khó, điểm động, cực trị
Mặt phẳng cắt phụ thuộc tham số, thiết diện biến dạng, diện tích lớn nhất/nhỏ nhất, thiết diện qua trung điểm hoặc trọng tâm.

## Chặng E — Khối tròn và mô hình hình học 3D

### 13. Nón — trụ — cầu — chóp cụt
Thiết diện qua trục, mặt cầu nội/ngoại tiếp, khoảng cách tới trục, góc sinh–đáy, thể tích và diện tích.

### 14. Mô hình thực tế 3D
Mái nhà, bồn chứa, silo, ram dốc, tấm pin mặt trời, camera, drone, vùng an toàn, đóng gói và tối ưu vật liệu.

## Chặng F — Điểm động, cực trị và Oxyz

### 15. Điểm động & cực trị HHKG
Khoảng cách nhỏ nhất, góc lớn nhất/nhỏ nhất, thể tích lớn nhất, vị trí đặc biệt; dùng bình phương khoảng cách và tham số hóa hợp lý.

### 16. Oxyz như ngôn ngữ thứ hai
Dùng tọa độ để kiểm chứng hoặc rút gọn cấu hình khó; vector pháp tuyến, khoảng cách, góc, mặt phẳng; luôn đối chiếu lại ý nghĩa hình học.

## Chặng G — Tổng hợp luyện thi phân hóa cao

### 17. Đúng/Sai HHKG
Một cấu hình chung với 4 mệnh đề: góc, khoảng cách, thể tích, thiết diện; tập trung vào lỗi suy luận hình học.

### 18. Trả lời ngắn HHKG
Các bài mô hình hóa 3D, góc nhị diện, khoảng cách chéo nhau, tỷ số thể tích, thiết diện; lời giải gọn nhưng phải dựng đúng cấu hình.

### 19. Những cấu hình lạ nhưng lời giải đẹp
Tứ diện trực tâm, tứ diện đều, hình hộp có đường chéo đặc biệt, bất biến, đối xứng, phép chiếu; các bài khó nhìn nhưng lời giải ngắn.

### 20. Capstone — bản đồ phương pháp HHKG THPT
Một video 15–18 phút tổng hợp toàn bộ chiến lược: nhìn cạnh chung, chọn mặt cắt, chọn hình chiếu, đổi khoảng cách thành thể tích, đổi hai đường chéo nhau thành điểm–mặt, dùng đồng dạng và Oxyz khi cần.
