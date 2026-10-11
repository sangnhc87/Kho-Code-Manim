# KẾ HOẠCH SERIES 30 TẬP
## Xác Suất Chuyên Sâu – Từ Cổ Điển Đến Có Điều Kiện, Toàn Phần Và Bayes

> **Tác giả:** Thầy Nguyễn Văn Sang · **Mã series:** `XS01 → XS30`
> **Công nghệ:** Manim Community 0.19 + Typst (100 % công thức) + Edge TTS `vi-VN-NamMinhNeural` + GitHub Actions + YouTube API — dùng lại bộ máy đã chạy ổn định của series INT (36 tập).
> **Nguồn dữ liệu máy đọc được:** [`series_plan.json`](series_plan.json).
> **Series nền đi kèm:** Đại số tổ hợp `COMB01–COMB25` (đếm). Series này **không dạy lại phép đếm**, mà dẫn link tới đúng tập COMB khi cần.

---

## 1. Định vị series

| Câu hỏi | Trả lời |
| :--- | :--- |
| Dành cho ai? | Học sinh 10 – 11 – 12 học theo chương trình; học sinh lớp 12 ôn thi tốt nghiệp; giáo viên cần học liệu trực quan. |
| Bám chương trình nào? | GDPT 2018, xuyên ba lớp: **Toán 10** (xác suất theo định nghĩa cổ điển), **Toán 11** (các quy tắc tính xác suất: hợp, giao, độc lập, công thức cộng, công thức nhân), **Toán 12** (xác suất có điều kiện, công thức xác suất toàn phần, công thức Bayes). |
| Bám đề thi nào? | Cấu trúc thi tốt nghiệp từ 2025: **Phần I** trắc nghiệm, **Phần II** Đúng/Sai 4 ý, **Phần III** trả lời ngắn. Xác suất có điều kiện, toàn phần và Bayes là dạng trọng tâm của đề mới, rất hợp với câu Đúng/Sai nhiều ý và trả lời ngắn. |
| Khác SGK ở đâu? | Mỗi xác suất đều **nhìn thấy được**: lưới không gian mẫu, sơ đồ cây có trọng số, biểu đồ Venn theo diện tích, hình vuông đơn vị và bảng hai chiều. Mô phỏng hàng nghìn lần thử cho thấy tần suất hội tụ về đúng con số vừa tính. |
| Kiểm chứng toán học | Mọi xác suất trong video được kiểm **hai lần** trong `xsXX/lesson.py`: phân số chính xác (`fractions`/SymPy) **và** liệt kê vét cạn không gian mẫu (`itertools`) khi có thể. CI dừng nếu hai cách lệch nhau. |

### Phạm vi chương trình (gắn nhãn trong từng tập)

- 🟢 **core**: nằm trong chương trình bắt buộc, có thể ra thi tốt nghiệp.
- 🟣 **extended**: mở rộng (phép thử lặp Bernoulli, công thức cộng 3 biến cố, Monty Hall, bài toán ngày sinh). Dành cho học sinh giỏi, đánh giá năng lực, đại học. Video nói rõ ở phần mở đầu để học sinh không học lệch trọng tâm.

---

## 2. Khung chuẩn của MỘT tập (7 – 12 phút)

Giữ đúng khung đã kiểm nghiệm ở series INT:

| Khối | Thời lượng | Nội dung bắt buộc |
| :--- | :---: | :--- |
| **Mở đầu (Hook)** | ≤ 1 phút | Một trò chơi hoặc nghịch lý nhỏ, có hình động. Kết thúc bằng thẻ tiêu đề. |
| **Phần 1 – Bản chất** | 3 – 4 phút | Mô hình trực quan (lưới, cây, Venn, hình vuông đơn vị) rồi rút ra công thức đóng khung. |
| **Phần 2 – Ví dụ** | 3 – 4 phút | Từ bài cơ bản đến bài vận dụng thực tế, lời giải hiện từng dòng đúng nhịp lời giảng. |
| **Phần 3 – Đề thi mới** | 2 – 3 phút | 1 câu Đúng/Sai 4 ý **hoặc** 1 câu trả lời ngắn (phiếu 4 ô), kèm bẫy hay gặp. |
| **Tổng kết** | ≤ 1 phút | 3 ý cần nhớ, 3 bài tự luyện có đáp số, giới thiệu tập sau. |

**Quy tắc hiển thị:** 100 % công thức và con số dựng bằng Typst (`self.M`, `self.TM`, `readout`). Không gõ toán dạng chữ thường. Có thanh tiến độ, tên phần đang học, footer **Thầy Nguyễn Văn Sang**.

**Quy tắc mô phỏng:** mọi mô phỏng dùng hạt giống ngẫu nhiên cố định (`seed`), nên video render lại vẫn ra đúng một kết quả.

---

## 3. Bộ hình trực quan riêng của series (`common/prob.py`)

| Khối hình | Dùng cho |
| :--- | :--- |
| **Lưới không gian mẫu** (6×6 cho hai xúc xắc, 2ⁿ cho đồng xu) | Đếm n(Ω), tô biến cố, “zoom” vào B khi tính P(A\|B). |
| **Sơ đồ cây có trọng số** | Mọc từng nhánh, ghi xác suất trên cạnh, nhân dọc nhánh, cộng các lá; lật ngược cây cho Bayes. |
| **Venn theo diện tích** | Hợp, giao, xung khắc, công thức cộng; diện tích tỉ lệ đúng với xác suất. |
| **Hình vuông đơn vị** | Độc lập (lưới tích), xác suất toàn phần (dải dọc), Bayes (tỉ lệ diện tích trong cột dương tính). |
| **Bảng hai chiều** | Dữ liệu khảo sát và xét nghiệm, đọc P(A\|B) theo hàng hoặc cột. |
| **Bình bi, bộ thẻ, xúc xắc, đồng xu** | Rút có hoàn lại / không hoàn lại, hoạt họa từng lần rút. |
| **Bộ đếm Monte Carlo** | Thanh tần suất hội tụ về xác suất lý thuyết (luật số lớn trực quan). |

---

## 4. Lộ trình 30 tập

### PHẦN A – NGÔN NGỮ CỦA NGẪU NHIÊN (XS01 – XS06) · Toán 10

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **XS01** 🟢 | Phép thử và không gian mẫu · Ω và n(Ω) | Nền tảng | Tung xúc xắc, đồng xu; lưới 6×6 hiện từng ô | Đúng/Sai về n(Ω) của phép thử nhiều bước |
| **XS02** 🟢 | Biến cố và biến cố đối · từ lời nói sang tập hợp | Nền tảng | Tô màu tập con trên lưới; Ā là phần còn lại | Viết A bằng liệt kê, tính n(A) |
| **XS03** 🟢 | Sơ đồ cây và bảng · liệt kê phép thử nhiều bước | Nền tảng | Cây mọc nhánh từng tầng; bảng hai chiều | Gia đình 3 con, đề thi 3 câu |
| **XS04** 🟢 | Định nghĩa cổ điển của xác suất · điều kiện đồng khả năng | Thông hiểu | Mỗi ô lưới cùng "khối lượng"; phản ví dụ của d'Alembert | Bẫy "sấp–sấp, ngửa–ngửa, một sấp một ngửa" |
| **XS05** 🟢 | Tần suất và xác suất · từ thí nghiệm đến lý thuyết | Thông hiểu | Monte Carlo 10 000 lần tung, đường tần suất hội tụ | So sánh xác suất thực nghiệm và lý thuyết |
| **XS06** 🟢 | Xác suất của biến cố đối · bài toán "ít nhất một" | Vận dụng 7+ | Đảo màu lưới: đếm phần bù nhanh hơn | P(ít nhất một con 6 khi tung 4 lần) |

### PHẦN B – XÁC SUẤT CỔ ĐIỂN VỚI PHÉP ĐẾM (XS07 – XS13) · Toán 10

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **XS07** 🟢 | Chọn đồ vật · tổ hợp trong tử và mẫu | Thông hiểu | Bình bi, rút cùng lúc k viên | Chọn 3 bi có đủ hai màu |
| **XS08** 🟢 | Xếp chỗ và lập số · hoán vị, chỉnh hợp | Vận dụng 7+ | Hàng ghế, ô chữ số lần lượt được lấp | Hai bạn ngồi cạnh nhau; số chẵn có chữ số khác nhau |
| **XS09** 🟢 | Hai xúc xắc, ba đồng xu · bảng tổng và tích | Thông hiểu | Lưới 6×6 tô theo tổng, đường chéo cùng tổng | Tổng chia hết cho 3; tích là số chẵn |
| **XS10** 🟢 | Chia nhóm, rút thăm, phân công | Vận dụng 8+ | Thẻ tên bay vào từng nhóm | Hai bạn thân cùng nhóm |
| **XS11** 🟢 | "Ít nhất", "nhiều nhất", "đúng k" · chia trường hợp hay dùng phần bù | Vận dụng 8+ | Cây quyết định chọn cách đếm | Đề có ít nhất 2 câu khó |
| **XS12** 🟢 | Thứ tự có quan trọng? · đếm tử và mẫu cùng một cách | Vận dụng 8+ | Hai cách đếm song song ra cùng xác suất | Rút lần lượt so với rút cùng lúc |
| **XS13** 🟣 | Trực giác đánh lừa · bài toán ngày sinh, tổng ôn A–B | Vận dụng cao 9+ | Đường cong xác suất trùng ngày sinh theo số người | 23 người: hơn 50 % trùng ngày sinh |

### PHẦN C – CÁC QUY TẮC TÍNH XÁC SUẤT (XS14 – XS19) · Toán 11

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **XS14** 🟢 | Biến cố hợp, giao, xung khắc | Nền tảng | Venn động: hai vùng trượt lại gần, chồng lên, tách rời | Đúng/Sai phân biệt A ∪ B và A ∩ B |
| **XS15** 🟢 | Công thức cộng xác suất · P(A ∪ B) = P(A) + P(B) − P(AB) | Thông hiểu | Diện tích Venn: phần giao bị đếm hai lần | Lớp học thích Toán hoặc thích Anh |
| **XS16** 🟢 | Biến cố độc lập · trực giác và định nghĩa | Thông hiểu | Hình vuông đơn vị chia lưới tích: P(AB) = P(A)·P(B) | Hai xạ thủ bắn độc lập |
| **XS17** 🟢 | Công thức nhân cho biến cố độc lập · hệ nối tiếp, song song | Vận dụng 8+ | Sơ đồ mạch điện, dòng chảy qua công tắc | Độ tin cậy của hệ thống máy |
| **XS18** 🟣 | Phép thử lặp · đúng k lần thành công | Vận dụng 8+ | Cây n tầng, đếm các đường có k nhánh "thành công" | Đoán mò 10 câu trắc nghiệm |
| **XS19** 🟢 | Tổng ôn Phần C · phối hợp cộng và nhân | Vận dụng 8+ | Bảng chọn công thức theo từ khóa | Đúng/Sai 4 ý tổng hợp |

### PHẦN D – XÁC SUẤT CÓ ĐIỀU KIỆN, TOÀN PHẦN, BAYES (XS20 – XS27) · Toán 12 ⭐ trọng tâm

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **XS20** 🟢 | Xác suất có điều kiện · thu hẹp không gian mẫu | Thông hiểu | Lưới 6×6 "zoom" vào B; Ω mới chỉ còn các ô của B | P(tổng bằng 8 \| có một con 3) |
| **XS21** 🟢 | Đọc xác suất có điều kiện từ bảng hai chiều | Thông hiểu | Bảng khảo sát: tô theo hàng và theo cột | P(A\|B) ≠ P(B\|A) trên cùng một bảng |
| **XS22** 🟢 | Công thức nhân xác suất · P(AB) = P(A)·P(B\|A) | Vận dụng 7+ | Bình bi rút không hoàn lại, cây có trọng số | Rút 2 bi liên tiếp cùng màu |
| **XS23** 🟢 | Độc lập nhìn qua điều kiện · độc lập khác xung khắc | Vận dụng 8+ | Venn đặt cạnh hình vuông đơn vị: hai khái niệm tách bạch | Bẫy "xung khắc nên độc lập" |
| **XS24** 🟢 | Công thức xác suất toàn phần · chia nhỏ theo nguyên nhân | Vận dụng 8+ | Hình vuông đơn vị chia dải dọc, cộng các lá của cây | Hai phân xưởng, tỉ lệ phế phẩm chung |
| **XS25** 🟢 | Công thức Bayes · lật ngược sơ đồ cây | Vận dụng 8+ | Lật cây; trong cột "dương tính", tỉ lệ diện tích của "có bệnh" | Xét nghiệm dương tính giả |
| **XS26** 🟢 | Toàn phần và Bayes với nhiều giả thuyết · bài toán nhiều bước | Vận dụng cao 9+ | Ba nhánh nguyên nhân; bi chuyển hộp | Chuyển 1 bi từ hộp I sang hộp II rồi rút |
| **XS27** 🟣 | Bayes trong đời sống · Monty Hall, lọc thư rác, xét nghiệm hai lần | Vận dụng cao 9+ | Mô phỏng 1000 ván Monty Hall; cập nhật niềm tin sau mỗi lần xét nghiệm | Đổi cửa được 2/3 |

### PHẦN E – TỔNG ÔN & LUYỆN ĐỀ (XS28 – XS30)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **XS28** 🟢 | Bẫy sai kinh điển trong xác suất · kiểm tra bằng liệt kê và mô phỏng | Tổng hợp | "Phòng khám lỗi sai": không đồng khả năng, đếm lệch thứ tự, nhầm P(A\|B) với P(B\|A), nhầm độc lập với xung khắc, quên phần bù | Mỗi bẫy kèm một cách tự kiểm tra |
| **XS29** 🟢 | Luyện đề theo cấu trúc thi tốt nghiệp · phần xác suất | Tổng hợp | Đồng hồ đếm giờ, phiếu trả lời 4 ô | Trắc nghiệm, Đúng/Sai và trả lời ngắn, trọng tâm có điều kiện và Bayes |
| **XS30** 🟢 | Bản đồ tư duy · từ cổ điển đến Bayes, chiến lược 8+ / 9+ | Tổng hợp | Bản đồ mở dần: đếm, cổ điển, quy tắc, có điều kiện | Lộ trình tự học sau series |

---

## 5. Mạch kiến thức xuyên suốt

```text
Phép thử ─► Ω ─► biến cố ─► P(A) = n(A)/n(Ω)                       (lớp 10)
                                │
                                ├─► hợp, giao ─► công thức cộng       (lớp 11)
                                └─► độc lập ─► công thức nhân
                                                   │
         P(A|B) = P(AB)/P(B) ◄──────────────────────┘                 (lớp 12)
                │
                ├─► P(AB) = P(B)·P(A|B)        (công thức nhân tổng quát)
                ├─► P(A) = Σ P(Bᵢ)·P(A|Bᵢ)     (toàn phần)
                └─► P(Bᵢ|A) = P(Bᵢ)·P(A|Bᵢ)/P(A)   (Bayes)
```

Một ý tưởng nối cả series: **xác suất = phần của một tổng thể**. Điều kiện chỉ là **đổi tổng thể** (thu hẹp Ω); toàn phần là **chia tổng thể thành từng phần**; Bayes là **hỏi ngược** một phần đến từ đâu.

---

## 6. Chuẩn đặt tên & xuất bản

- **Thư mục:** `Manim-Typst/series-xac-suat/` · mỗi tập `xsXX/lesson.py` + `xsXX/scene.py`.
- **Tiêu đề YouTube:** `XSxx: <Tên tập> | <Dạng/kỹ thuật> - Thầy Nguyễn Văn Sang` (≤ 95 ký tự, lấy từ `series_plan.json`).
- **Mô tả YouTube:** sinh tự động, có mốc chương, mục tiêu bài, bài tự luyện, link tập COMB liên quan.
- **Phụ đề:** `XSxx_vi.srt` tải lên cùng video.
- **Playlist:** “Xác Suất Chuyên Sâu: Cổ Điển → Có Điều Kiện → Bayes | Thầy Nguyễn Văn Sang”.
- **Workflow:** `.github/workflows/render-xs.yml` (giống `render-int.yml`: `episode`, `quality`, `voice`, `upload`, `privacy`).

## 7. Quy trình sản xuất một tập

Giống hệt series INT: `lesson.py` (lời giảng + kiểm phân số + liệt kê vét cạn) → `build_typst` → `prepare_voice` → smoke → preview + QA + duyệt ảnh từng nhịp → commit → Actions render Full HD và đăng YouTube. Trong lúc CI render tập trước, dựng ngay tập sau.

## 8. Tiến độ

| Trạng thái | Tập |
| :--- | :--- |
| ⚪ Kế hoạch | XS01 – XS30 |

Lịch đề xuất: 2–3 tập/ngày dựng song song CI. Thứ tự ưu tiên: **Phần D trước** (lớp 12 ôn thi), sau đó A → B → C → E. Hoặc làm tuần tự XS01 → XS30 nếu muốn series liền mạch từ lớp 10.
