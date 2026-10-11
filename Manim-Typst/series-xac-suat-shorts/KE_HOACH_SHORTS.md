# KẾ HOẠCH SERIES SHORTS · XÁC SUẤT 3 PHÚT
## 200 thử thách xác suất: từ Mở đầu đến đề Học sinh giỏi

> **Tác giả:** Thầy Nguyễn Văn Sang · **Mã:** `XSS001 → XSS200` · **Định dạng:** YouTube Shorts dọc 1080×1920, tối đa 3 phút.
> **Danh sách đầy đủ 200 Shorts:** [`DANH_SACH_SHORTS.md`](DANH_SACH_SHORTS.md) · **Dữ liệu máy đọc:** [`shorts_plan.json`](shorts_plan.json) · **Nguồn và kiểm chứng:** [`shorts_plan.py`](shorts_plan.py).
> **Series dài đi kèm:** Xác suất chuyên sâu `XS01 – XS30` ([kế hoạch](../series-xac-suat/KE_HOACH_SERIES_30_TAP.md)). Mỗi Short dẫn về đúng một tập dài.

---

## 1. Ý tưởng

Mỗi Short là **một câu đố xác suất trọn vẹn**: đề bài trong 5 giây đầu, người xem đoán, rồi hình động giải thích vì sao đáp án đúng, và kết bằng một con số đóng khung. Độ khó tăng dần qua 6 mức, nên xem theo thứ tự cũng thành một lộ trình học. Xem ngẫu nhiên từng clip vẫn hiểu được.

| Mức | Tên | Shorts | Số lượng | Thời lượng | Nội dung |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **L1** | Mở đầu | 001 – 015 | 15 | 30 – 60 s | Đồng xu, xúc xắc, lá bài: không gian mẫu, định nghĩa cổ điển, biến cố đối |
| **L2** | Cơ bản | 016 – 035 | 20 | 45 – 75 s | Hai xúc xắc, chọn bi, xếp hàng, tổ hợp trong tử và mẫu |
| **L3** | Thông hiểu | 036 – 060 | 25 | 60 – 90 s | Cược de Méré, công thức cộng, độc lập, mạch nối tiếp và song song, "ít nhất" |
| **L4** | Vận dụng | 061 – 085 | 25 | 75 – 120 s | Xác suất có điều kiện, bảng hai chiều, toàn phần, Bayes, xét nghiệm, lọc thư rác |
| **L5** | Khó | 086 – 105 | 20 | 90 – 150 s | Monty Hall, ngày sinh, thư bỏ nhầm phong bì (1/e), "con trai sinh thứ Ba", chuyển bi nhiều bước |
| **L6** | Rất khó | 106 – 120 | 15 | 120 – 180 s | Xác suất hình học (Buffon, bẻ que), con bạc phá sản, kiểm phiếu, Pólya, 6/π² |
| | **Nhánh 2** | | | | **Xác suất có điều kiện, sơ đồ cây, câu chặn điểm, đề học sinh giỏi** |
| **L7** | Sơ đồ cây | 121 – 140 | 20 | 60 – 120 s | Cây từ 2 tầng đến cây dừng sớm, cây vô hạn, cây thay đổi theo nhánh, đi ngẫu nhiên (kiến trên lập phương), deuce |
| **L8** | Có điều kiện | 141 – 160 | 20 | 60 – 120 s | Thu hẹp không gian mẫu, đảo điều kiện, "ít nhất một át" và "át bích", đôi một độc lập, hai nhân chứng |
| **L9** | Toàn phần – Bayes | 161 – 175 | 15 | 75 – 150 s | Nhân chứng taxi, đoán mò, dự báo, tín hiệu nhiễu, câu hỏi nhạy cảm, cập nhật niềm tin nhiều bước |
| **L10** | Chặn điểm 8-9-10 | 176 – 190 | 15 | 90 – 170 s | Dạng câu khó nhất đề tốt nghiệp: tổ hợp trong xác suất, xếp chỗ, đa giác đều, Bayes kiểu trả lời ngắn |
| **L11** | Học sinh giỏi | 191 – 200 | 10 | 120 – 180 s | Gối của Lewis Carroll, nghịch lý Simpson, bi cuối cùng, cầu thang, bài toán thư ký, Monty Hall 100 cửa |

🟣 Từ L5 – L6 có nhiều bài **vượt chương trình phổ thông**. Video ghi rõ "thử thách mở rộng" để học sinh không học lệch trọng tâm.

---

## 2. Kịch bản chuẩn của một Short

| Đoạn | Thời gian | Trên màn hình | Lời đọc |
| :--- | :---: | :--- | :--- |
| **Móc câu** | 0 – 5 s | Mức độ (L1–L6) + số thứ tự, đề bài một dòng lớn, hình vật thể (xúc xắc, bi, cửa…) | Đọc nhanh câu hỏi, kết bằng "bạn đoán bao nhiêu?" |
| **Đoán** | 5 – 10 s | Đồng hồ đếm ngược 5 giây; với bài nghịch lý thì có 2–3 lựa chọn để đoán | "Dừng video, chốt đáp án của bạn!" |
| **Giải** | 10 s – cuối −15 s | Hình trực quan chạy theo từng bước: lưới, cây, Venn, hình vuông đơn vị, mô phỏng | 2 – 4 bước ngắn, mỗi bước một câu |
| **Đáp án** | 10 s | Con số đóng khung lớn, kèm dòng kiểm chứng (liệt kê, mô phỏng) | Đọc đáp án, nhấn vào chỗ hay sai |
| **Kết** | 5 s | "Bài đầy đủ: XSxx" + câu hỏi tương tự để bình luận | "Bình luận đáp án câu tiếp theo nhé!" |

Short dài hơn (L5–L6) có thêm **mô phỏng Monte Carlo** cho thấy kết quả lạ là thật: 1 000 ván Monty Hall, 10 000 lần thả kim Buffon.

---

## 3. Bố cục màn hình dọc 1080×1920

```text
┌───────────────────────────┐  ← 0
│ L4 · VẬN DỤNG    #071     │  dải tiêu đề (mức độ + số thứ tự)
│ Đề bài (Typst, 2–3 dòng)  │
├───────────────────────────┤  ← ~520 px
│                           │
│   SÂN KHẤU HÌNH ĐỘNG      │  lưới / cây / Venn / bình bi / mô phỏng
│                           │
├───────────────────────────┤  ← ~1250 px
│ Lời giải từng dòng (Typst)│
│ ╔═══════════════╗         │
│ ║ ĐÁP ÁN  1/6   ║         │
├───────────────────────────┤  ← ~1600 px
│ (vùng an toàn: nút, chữ   │  không đặt nội dung quan trọng
│  của YouTube đè lên)       │  ở 320 px dưới cùng và 140 px mép phải
└───────────────────────────┘  ← 1920
```

- **100 % công thức dựng bằng Typst** (`TM`, `M`, `readout` như series INT), không gõ toán dạng chữ thường.
- **Phụ đề cứng** (chữ chạy theo lời) ở phần đầu sân khấu, vì nhiều người xem Shorts tắt tiếng.
- Mô phỏng dùng **seed cố định**, nên render lại vẫn ra đúng một kết quả.

---

## 4. Bộ máy sản xuất: theo dữ liệu, không viết tay từng clip

120 Shorts không thể viết tay 120 cảnh riêng. Thay vào đó:

1. **`shorts_plan.py`** (đã có) giữ đề, đáp án, kiểu hình, tập liên kết, kèm phép kiểm chứng cho từng Short.
2. **`xss/xssNNN.py`** (mỗi Short ~30 – 60 dòng dữ liệu) chứa lời đọc từng nhịp, công thức Typst từng bước và tham số hình (ví dụ `grid(highlight=lambda a, b: a + b == 7)`).
3. **`engine/`** chứa các khối hình tái sử dụng cho khung dọc:

   | Khối | Dùng cho |
   | :--- | :--- |
   | `coin`, `die`, `cards`, `urn` | Vật thể: tung, gieo, rút, rút không hoàn lại |
   | `grid` | Lưới không gian mẫu (6×6, 6×6×6 theo lát), tô biến cố, "zoom" khi có điều kiện |
   | `tree` | Sơ đồ cây có trọng số, nhân dọc nhánh, lật ngược cho Bayes |
   | `venn` | Venn theo diện tích |
   | `square` | Hình vuông đơn vị: độc lập, toàn phần, Bayes, bài hẹn gặp |
   | `table` | Bảng hai chiều |
   | `circuit` | Mạch nối tiếp và song song |
   | `curve` | Đường cong theo n (ngày sinh, 1/e) |
   | `geo` | Đa giác đều, đường tròn, que bẻ đôi |
   | `sim` | Bộ đếm Monte Carlo có seed, thanh tần suất hội tụ |

4. **Khung chung `ShortScene`** lo phần lặp lại: dải mức độ, đồng hồ đoán, khung đáp án, thẻ kết, phụ đề cứng, vùng an toàn.

Mỗi Short chỉ cần thêm dữ liệu, nên một lượt có thể dựng **10 Shorts**.

---

## 5. Quy trình và lịch đăng

```text
shorts_plan.py (đề + đáp án đã kiểm chứng)
   └─ xss/xssNNN.py (lời đọc + bước giải + tham số hình)
        ├─ build_typst      → SVG công thức
        ├─ prepare_voice    → MP3 + SRT (Edge TTS vi-VN-NamMinhNeural)
        ├─ manim ShortScene → 1080×1920, ≤ 180 s
        ├─ qa_short         → kiểm khung dọc, độ dài ≤ 180 s, có tiếng, vùng an toàn
        └─ upload           → YouTube Shorts (#Shorts), ghi youtube_uploaded_history.json
```

- **Workflow** `render-xss.yml` dùng lại mô hình của Cờ tàn:
  - chạy tay theo lô: `episodes=XSS001-XSS010`;
  - **tự động theo lịch 2 lượt/ngày** (sáng và tối), mỗi lượt đăng Short kế tiếp chưa có trong lịch sử, có cơ chế đăng bù.
- **Tiêu đề:** `Xác suất #071 · Dương tính có chắc bệnh? – bạn giải được không? #Shorts` (≤ 100 ký tự, đã kiểm trong `shorts_plan.py`).
- **Mô tả:** đề bài, đáp án ẩn sau dòng "↓ đáp án ↓", link tập dài XSxx, hashtag `#Shorts #XacSuat #Toan10 #Toan11 #Toan12 #OnThiTotNghiep`.
- **Playlist:** “Xác Suất 3 Phút – 120 Thử Thách | Thầy Nguyễn Văn Sang”.

**Nhịp sản xuất đề xuất:** dựng 10 Shorts/lượt và đẩy lên kho chờ đăng. Đăng 2 Shorts/ngày, nên 120 Shorts phủ khoảng 2 tháng. Có thể đăng 3/ngày nếu muốn nhanh hơn.

---

## 6. Tiến độ

| Bước | Trạng thái |
| :--- | :--- |
| Kế hoạch 120 Shorts, đáp án đã kiểm chứng | ✅ Xong (`python shorts_plan.py` → `XSS_PLAN_OK`) |
| Bộ máy dọc `engine/` + `ShortScene` + workflow `render-xss.yml` | ⚪ Tiếp theo |
| Lô 1: XSS001 – XSS010 (L1) | ⚪ |
| Lô 2 – 12: XSS011 – XSS120 | ⚪ |
