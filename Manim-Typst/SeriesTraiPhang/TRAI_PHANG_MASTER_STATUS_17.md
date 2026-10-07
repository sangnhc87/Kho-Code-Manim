# SERIES TRẢI PHẲNG — MASTER

Chuẩn khóa:
- Lời thoại chỉ nói toán và dẫn dắt học sinh.
- Bố cục hai cột cố định.
- Text và MathTypst không chồng nhau.
- Mặt mở thật quanh đúng cạnh chung.
- Điểm nằm trên mặt phải đi theo chính mặt khi mở.
- Với bài tham số, kiểm tra cả công thức độ dài lẫn vị trí điểm đổi mặt.
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
- [x] 16 — Mái nhà lăng trụ tam giác.
- [x] 17 — Điểm đích chạy trên cạnh.
- [ ] 18 — Một mặt bị cấm.
- [ ] 19 — Hộp chữ nhật tham số, phương án tối ưu đổi kiểu.
- [ ] 20 — Capstone thuật toán đường ngắn nhất trên bề mặt.

## Video 17

Khối lập phương cạnh `4`.

- A cố định.
- P chạy trên `CC'`.
- `t=CP`, `0<=t<=4`.
- dải mặt: `ABCD -> BCC'B'`.

Kết quả:

`L(t)=sqrt((4+t)^2+16)`.

Điểm đổi mặt:

`BX=16/(4+t)`.

Đặc biệt:
- `t=0`: `X=C`, `L=4 sqrt(2)`;
- `t=2`: `BX=8/3`, `L=2 sqrt(13)`;
- `t=4`: `X` là trung điểm `BC`, `L=4 sqrt(5)`.

Dạng tổng quát cạnh `a`:

`L(t)=sqrt((a+t)^2+a^2)`;

`BX=a^2/(a+t)`.
