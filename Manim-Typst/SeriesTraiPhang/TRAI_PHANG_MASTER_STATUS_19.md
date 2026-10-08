# SERIES TRẢI PHẲNG — MASTER — TIẾN ĐỘ 18/20

## Đã soạn mã và workflow

- [x] 01 — Lập phương, qua 2 mặt
- [x] 02 — Lập phương, qua 4 mặt
- [x] 03 — Hộp chữ nhật, qua 5 mặt
- [x] 04 — Lập phương, qua 6 mặt
- [x] 05 — Lăng trụ tam giác đều
- [x] 06 — Lăng trụ lục giác đều
- [x] 07 — Tứ diện đều
- [x] 08 — Chóp tứ giác đều
- [x] 09 — Chóp tam giác không đều
- [x] 10 — Chóp cụt vuông
- [x] 11 — Hình trụ, đường xoắn
- [x] 12 — Hình trụ, quấn k vòng
- [x] 13 — Hình nón, hình quạt
- [x] 14 — Hình nón cụt, vành quạt
- [x] 15 — Silo trụ + nón
- [x] 16 — Mái nhà lăng trụ tam giác
- [x] 17 — Điểm đích chạy trên cạnh
- [x] 18 — Một mặt bị cấm
- [x] 19 — Hộp chữ nhật tham số, phương án đổi kiểu
- [ ] 20 — Capstone tìm đường ngắn nhất trên bề mặt

**Lưu ý:** Dấu tích thể hiện đã soạn mã, kịch bản và workflow; không có nghĩa video 1080p đã được render và duyệt hình/nghe.

## Video 18

- Hộp `8 × 5 × 4`.
- P trên mặt trước `(2,0,3)`, Q trên mặt sau `(6,5,3)`.
- Mặt trên `z=4` bị cấm.
- Đường ngắn nhất không cấm: `sqrt(65)` qua mặt trên.
- Đường ngắn nhất hợp lệ: `sqrt(137)` qua đáy.
- Hai điểm đổi mặt: `x_X=34/11`, `x_Y=54/11`.
- So sánh toàn bộ 7 dải mặt hợp lệ, có kiểm tra cạnh cắt, thứ tự và biến dạng cứng.
- Lời thoại tiếng Việt, bố cục hai cột, MathTypst, Edge TTS, video 1080p qua GitHub Actions.


## Video 19

Hình hộp `4 × 6 × t`, `2≤t≤10`, A và G là hai đỉnh đối diện.

- Qua trái và nắp: `L_I=sqrt((t+4)^2+36)`;
- Qua trước và phải: `L_II=sqrt(t^2+100)`;
- Qua đáy và sau: `L_III=sqrt((t+6)^2+16)`.

`L_III^2-L_I^2=4t>0`, nên III bị loại.

`L_I^2-L_II^2=8(t-6)`.

- `2≤t<6`: I tối ưu.
- `t=6`: I và II cùng tối ưu, `L_min=2sqrt(34)`.
- `6<t≤10`: II tối ưu.

Ý chính: tối ưu theo tham số có thể đổi kiểu phương án.
