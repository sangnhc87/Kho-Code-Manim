# Trải Nghiệm ManimGX-Typst Trên GitHub Actions

> **Bài toán:** Tối ưu hóa sản xuất hai kiểu mũ (Toán 10 - Hệ bất phương trình bậc nhất hai ẩn & Quy hoạch tuyến tính).  
> **Thương hiệu:** Thầy Nguyễn Văn Sang  
> **Công nghệ:** ManimGX (Rust + wgpu/lavapipe + Native Typst typesetting) chạy 100% trên GitHub Actions.

---

## 1. Phân Tích Toán Học Chi Tiết (Câu 2)

### Đề bài:
Một phân xưởng sản xuất hai kiểu mũ:
- Thời gian làm $1$ mũ kiểu I gấp $2$ lần kiểu II.
- Nếu chỉ sản xuất kiểu II thì trong $1$ giờ làm được $60$ chiếc.
- Phân xưởng làm việc $8$ tiếng mỗi ngày.
- Thị trường tiêu thụ tối đa: $200$ chiếc mũ kiểu I và $240$ chiếc mũ kiểu II mỗi ngày.
- Tiền lãi: $1$ chiếc kiểu I lãi $24$ nghìn đồng, kiểu II lãi $15$ nghìn đồng.
- Gọi $x, y$ là số mũ kiểu I và II cần sản xuất.

### Lập luận:
1. **Năng suất và thời gian:**
   - $1$ giờ làm $60$ mũ II $\implies$ thời gian làm $1$ mũ II là $\dfrac{1}{60}$ giờ.
   - Thời gian làm $1$ mũ I gấp đôi kiểu II $\implies \dfrac{2}{60} = \dfrac{1}{30}$ giờ.
   - Tổng thời gian làm $x$ mũ I và $y$ mũ II:
     $$t = \frac{2x}{60} + \frac{y}{60} = \frac{2x + y}{60} \text{ (giờ)}$$
   - Phát biểu a) ghi $\dfrac{2x - y}{60}$ $\implies$ **SAI (S)**.

2. **Hệ bất phương trình ràng buộc:**
   - Điều kiện không âm: $x \ge 0, y \ge 0$.
   - Giới hạn thị trường: $x \le 200, y \le 240$.
   - Quỹ thời gian $8$ giờ/ngày: $\dfrac{2x + y}{60} \le 8 \iff 2x + y \le 480$.
   - Hệ điều kiện:
     $$\begin{cases} 0 \le x \le 200 \\ 0 \le y \le 240 \\ 2x + y \le 480 \end{cases}$$
   - Phát biểu b) $\implies$ **ĐÚNG (Đ)**.

3. **Miền nghiệm hình học (Ngũ giác lồi $OABCD$):**
   - $O(0, 0)$
   - $A(200, 0)$
   - $B(200, 80)$ (giao của $x = 200$ và $2x + y = 480$)
   - $C(120, 240)$ (giao của $y = 240$ và $2x + y = 480$)
   - $D(0, 240)$

4. **Hàm tiền lãi và giá trị cực đại:**
   - Hàm mục tiêu: $F(x, y) = 24x + 15y$ (nghìn đồng)
   - $F(O) = 0$
   - $F(A) = 24(200) + 15(0) = 4.800$ nghìn đ ($4.800.000$ đ)
   - $F(B) = 24(200) + 15(80) = 6.000$ nghìn đ ($6.000.000$ đ)
   - $F(C) = 24(120) + 15(240) = 2.880 + 3.600 = 6.480$ nghìn đ ($6.480.000$ đ) $\implies$ **LỚN NHẤT (MAX)**
   - $F(D) = 24(0) + 15(240) = 3.600$ nghìn đ ($3.600.000$ đ)
   - Phát biểu c) $\implies$ **ĐÚNG (Đ)**.
   - Phát biểu d) $\implies$ **ĐÚNG (Đ)**.

**Đáp án chuẩn: a) S — b) Đ — c) Đ — d) Đ**

---

## 2. Vì Sao Dùng ManimGX-Typst Trên GitHub Actions?

- **Không nóng máy, không tốn RAM/CPU máy cá nhân:** GitHub runner (Ubuntu 16GB RAM) đảm nhận toàn bộ quá trình render và xuất file MP4.
- **Tốc độ vượt trội:** ManimGX xây dựng trên Rust + wgpu rendering, tích hợp Typst biên dịch toán học tức thì, không cần cài bộ $\LaTeX$ cồng kềnh (tiết kiệm hàng GB và vài phút build).
- **Tự động lưu trữ Artifacts:** Video MP4 thành phẩm 1080p và ảnh Storyboard (bản xem trước từng phân cảnh) được upload tự động lên tab **Actions** của repository để tải về bất kỳ lúc nào.
