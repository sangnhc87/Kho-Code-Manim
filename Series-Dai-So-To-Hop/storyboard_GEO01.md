# Storyboard Manim–Typst — GEO01 (độc lập)

| Cảnh | Trái: trực quan hóa | Phải: đề bài và lập luận | Typst / Tương tác |
|---|---|---|---|
| 01. Đặt vấn đề | Tam giác ABC trên tọa độ; nhấn vùng tô màu | Nguyên đề bài và yêu cầu tính T | Chữ VN Pango |
| 02. Quỹ tích | Đường tím y=x−1/2; M chạy trên đường thẳng | x=m, y=m−1/2 | `geo_line` |
| 03. Phóng đại gần C | Hình tam giác cắt phóng to đồng dạng; đoạn xanh nằm trong | Hiểu đầu đoạn thuộc hai cạnh | Dùng phép co giãn đều (không méo) |
| 04. Tìm hai biên | Đánh dấu giao với BC rồi AC | BC: x+3y=5; AC: x+y=3 | `geo_bounds` |
| 05. Hệ bất phương trình | Hiện tam giác nguyên tỉ lệ, nhận 3 miền | x−y+3>0; x+3y−5>0; 3−x−y>0 | `geo_three` |
| 06. Thay tham số | Khoảng xanh highlight | 7/2>0; 4m−13/2>0; 7/2−2m>0 | `geo_bounds` |
| 07. Kết luận | Hai đầu biên vàng, khoảng trong xanh | a=13/8, b=7/4, T=20 | `geo_final` |
| 08. Tổng quát | Tam giác có định hướng | s=sgn([AB,AC]); 3 tích có hướng cùng dấu | `geo_general` |
| 09. Trường hợp biên | Chấm xanh/đỏ/vàng minh họa | >0 miền trong; ≥0 miền đóng | `geo_boundary` |
| 10. Tọa độ tỉ cự | Vùng trong tam giác | αA+βB+γC, α+β+γ=1, tất cả dương | `geo_bary` |
| 11. Tổng kết | Quay lại tam giác ban đầu | Ba bước giải tổng quát | `geo_final` |

## Tiêu chuẩn nghiệm thu

- Hình A(0,3), B(−1,2), C(2,1) và giao điểm phải **đúng tỉ lệ tọa độ**.
- Chỉ zoom đồng dạng, không kéo dãn khác tỉ lệ x/y.
- Miền trong là bất phương trình **nghiêm**; miền gồm biên dùng bất phương trình không nghiêm.
- Tích có hướng phải dùng `sgn(D)` để xử lý tam giác thuận/ngược.
- Hai biên đúng `13/8`, `7/4`; T=20; không lấy dấu bằng.
- Typst biên dịch thành ảnh nền trong suốt; không dùng MathTex của LaTeX.
- Không đè chữ sang hình; tối đa 6 dòng giải thích/bảng phải.
- Chạy pytest/unittest và render preview, quan sát 8 khung hình rồi mới xuất Full HD.
