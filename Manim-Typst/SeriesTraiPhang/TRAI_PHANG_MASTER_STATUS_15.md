# SERIES TRẢI PHẲNG — MASTER

Chuẩn khóa:
- Lời thoại chỉ nói toán và dẫn dắt học sinh.
- Bố cục hai cột cố định.
- Text và MathTypst không chồng nhau.
- Không dùng hiệu ứng trang trí thừa.
- Mặt cong khai triển được phải giữ nguyên độ dài trên bề mặt.
- Với vật thể ghép, phải giữ đúng điểm chuyển giữa các loại mặt.
- Narration lint + Typst preflight + geometry preflight + layout preflight + smoke render.

## Tiến độ 20 video

- [x] 01 — Lập phương, đi qua 2 mặt.
- [x] 02 — Lập phương, đi qua đúng 4 mặt.
- [x] 03 — Hộp chữ nhật, đi qua đúng 5 mặt.
- [x] 04 — Lập phương, đi qua đủ 6 mặt.
- [x] 05 — Lăng trụ tam giác đều.
- [x] 06 — Lăng trụ lục giác đều, so sánh hai hướng.
- [x] 07 — Tứ diện đều, đi qua cạnh đối.
- [x] 08 — Chóp tứ giác đều, cánh quạt mặt bên.
- [x] 09 — Chóp tam giác không đều, chọn đúng dải mặt.
- [x] 10 — Chóp cụt vuông, dải hình thang.
- [x] 11 — Hình trụ, đường xoắn thành đường thẳng.
- [x] 12 — Hình trụ, đường đi quấn k vòng.
- [x] 13 — Hình nón, trải thành hình quạt và đổi góc.
- [x] 14 — Hình nón cụt, vành quạt và kiểm tra tính hợp lệ.
- [x] 15 — Silo trụ + nón, ghép hai phép khai triển.
- [ ] 16 — Mái nhà lăng trụ tam giác.
- [ ] 17 — Điểm đích chạy trên cạnh.
- [ ] 18 — Một mặt bị cấm.
- [ ] 19 — Hộp chữ nhật tham số.
- [ ] 20 — Capstone thuật toán đường ngắn nhất trên bề mặt.

## Video 15

Silo:
- thân trụ `r=3`, `h=4`;
- mái nón `r=3`, `h=4`, `l=5`.

Điểm chuyển mặt:
- `M` cố định trên vòng nối.

Phần trụ:
- góc A->M: `2 pi/3`;
- độ lệch ngang: `2 pi`;
- `L_tru=2 sqrt(pi^2+4)`.

Phần nón:
- góc vật lý M->B: `5 pi/6`;
- góc trên hình quạt: `pi/2`;
- `SM=5`, `SB=5/2`;
- `L_non=5 sqrt(5)/2`.

Kết quả:

`L_min=2 sqrt(pi^2+4)+5 sqrt(5)/2`.

Điểm dạy học chính:
**một đường đi qua vật thể ghép có thể cần nhiều loại bản khai triển; nếu điểm chuyển mặt cố định, tối ưu từng phần rồi cộng.**
