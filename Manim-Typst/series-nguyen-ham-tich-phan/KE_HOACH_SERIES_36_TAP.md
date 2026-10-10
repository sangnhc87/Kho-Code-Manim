# KẾ HOẠCH SERIES 36 TẬP
## Nguyên Hàm – Tích Phân – Ứng Dụng Chuyên Sâu

> **Tác giả:** Thầy Nguyễn Văn Sang · **Mã series:** `INT01 → INT36` · **Chuyên đề gốc:** 12.3 (xem `plan.md` ở gốc repo)
> **Công nghệ:** Manim Community 0.19 + Typst (công thức) + Edge TTS `vi-VN-NamMinhNeural` + GitHub Actions + YouTube API
> **Nguồn dữ liệu máy đọc được:** [`series_plan.json`](series_plan.json) (tiêu đề YouTube, mức độ, phạm vi chương trình, trạng thái).

---

## 1. Định vị series

| Câu hỏi | Trả lời |
| :--- | :--- |
| Dành cho ai? | Học sinh lớp 12 ôn thi tốt nghiệp THPT; học sinh khá – giỏi muốn hiểu bản chất; giáo viên cần học liệu trực quan. |
| Khác SGK ở đâu? | Mỗi khái niệm đều có **hình ảnh động chứng minh vì sao đúng** (trường hướng, tổng Riemann, cắt lát thể tích) chứ không chỉ công thức. |
| Bám chương trình nào? | Toán 12 – GDPT 2018, Chương IV *Nguyên hàm và tích phân* (Nguyên hàm → Tích phân → Ứng dụng hình học). |
| Bám đề thi nào? | Cấu trúc thi tốt nghiệp từ 2025: **Phần I** trắc nghiệm 4 lựa chọn, **Phần II** Đúng/Sai, **Phần III** trả lời ngắn. Mỗi tập có ít nhất 1 câu theo dạng Phần II hoặc Phần III. |

### Phạm vi chương trình (gắn nhãn trong từng tập)

- 🟢 **core** – nằm trong chương trình bắt buộc, thi tốt nghiệp.
- 🟣 **extended** – mở rộng (đổi biến, từng phần, phân thức hữu tỉ, hàm ẩn): dành cho HSG, đánh giá năng lực, đại học. Video phải nói rõ ở phần mở đầu để học sinh không học lệch trọng tâm.

---

## 2. Khung chuẩn của MỘT tập (9 – 16 phút)

| Khối | Thời lượng | Nội dung bắt buộc |
| :--- | :---: | :--- |
| **Mở đầu (Hook)** | ≤ 1 phút | Một tình huống/câu hỏi then chốt, có hình động. Kết thúc bằng thẻ tiêu đề tập. |
| **Phần 1 – Bản chất** | 3 – 5 phút | Mô phỏng trực quan cơ chế → rút ra định nghĩa/công thức trọng tâm (đóng khung). |
| **Phần 2 – Ví dụ** | 3 – 4 phút | 1 bài cơ bản → 1 bài vận dụng (ưu tiên bài thực tế). Lời giải hiện từng dòng đúng nhịp lời giảng. |
| **Phần 3 – Đề thi mới & mẹo** | 2 – 3 phút | 1 câu Đúng/Sai 4 ý **hoặc** 1 câu trả lời ngắn; mẹo kiểm tra nhanh / bẫy hay gặp. |
| **Tổng kết (Outro)** | ≤ 1 phút | 3 ý cần nhớ, 3 bài tự luyện có đáp số, giới thiệu tập sau. |

**Quy tắc hiển thị:** không hiển thị số phân cảnh/nhãn debug; luôn có thanh tiến độ theo khối, tên phần đang học và footer **Thầy Nguyễn Văn Sang**; đồ thị dùng tọa độ thật (`Axes.c2p`), không vẽ "minh họa ước chừng".

**Quy tắc đồng bộ:** mỗi *nhịp* (beat) = 1 đoạn lời giảng + 1 hàm hoạt họa. Thời lượng nhịp = độ dài MP3 thật + 0,6 s; hoạt họa được co giãn theo thời lượng này nên hình luôn khớp lời.

**Quy tắc toán học:** mọi kết quả trong video được kiểm bằng SymPy trong `intXX/lesson.py` (`validate()` chạy trong CI trước khi render).

---

## 3. Lộ trình 36 tập

### PHẦN A – NGUYÊN HÀM: BẢN CHẤT VÀ KỸ THUẬT (INT01 – INT10)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **INT01** 🟢 | Đi ngược đạo hàm: bản chất nguyên hàm · họ nguyên hàm & hằng số C | Nền tảng | Trường hướng của f(x)=2x; con trượt C tịnh tiến họ parabol; khoảng cách hằng giữa 2 nguyên hàm; xe chạy theo v(t) | Đúng/Sai 4 ý về F của 6x²−2x; trả lời ngắn F qua điểm A |
| **INT02** 🟢 | Tính chất nguyên hàm & hàm lũy thừa · quy tắc tuyến tính, bẫy tích – thương | Nền tảng | Ghép hai họ nguyên hàm; phản ví dụ ∫(f·g) ≠ ∫f·∫g bằng đạo hàm kiểm tra | Trắc nghiệm chọn khẳng định đúng |
| **INT03** 🟢 | Nguyên hàm của 1/x và hàm số mũ · ln\|x\| trên từng khoảng | Nền tảng | Hai nhánh của ln\|x\| trượt độc lập; eˣ là "điểm bất động" của đạo hàm | Đúng/Sai về hằng số trên hai khoảng rời nhau |
| **INT04** 🟢 | Nguyên hàm hàm lượng giác · bảng cơ bản & hạ bậc | Thông hiểu | Sóng sin/cos lệch pha – đạo hàm là phép quay ¼ chu kỳ | ∫sin²x dx bằng hạ bậc |
| **INT05** 🟢 | Nguyên hàm của f(ax+b) · vì sao phải chia cho a | Thông hiểu | Co giãn đồ thị theo phương ngang làm độ dốc nhân a | Bẫy quên hệ số 1/a |
| **INT06** 🟢 | Nguyên hàm có điều kiện & hàm từng khúc · tìm C, nối liên tục | Vận dụng 7+ | Hai mảnh đồ thị được "hàn" tại điểm nối | Câu Đúng/Sai 4 ý (dạng hay ra) |
| **INT07** 🟣 | Nguyên hàm phân thức hữu tỉ · chia đa thức & tách phân thức | Vận dụng 8+ | Phân tích hệ số bất định bằng hoạt họa ghép mảnh | ∫ (ax+b)/(x²−k²) dx |
| **INT08** 🟣 | Phương pháp đổi biến số · nhận diện u và du | Vận dụng 8+ | "Kính lúp" đổi trục x → u, vi phân du | ∫ 2x·eˣ² dx, ∫ sin x·cos³x dx |
| **INT09** 🟣 | Phương pháp từng phần · sơ đồ đường chéo | Vận dụng 8+ | Bảng đạo hàm – nguyên hàm chạy chéo có dấu ± | ∫ x²eˣ dx bằng sơ đồ |
| **INT10** 🟢 | Từ tốc độ thay đổi đến đại lượng · tổng ôn phần A | Vận dụng 8+ | Dân số, nhiệt độ, chi phí biên phục hồi từ tốc độ | Trả lời ngắn có đơn vị thực tế |

### PHẦN B – TÍCH PHÂN (INT11 – INT20)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **INT11** 🟢 | Diện tích dưới đường cong & tổng Riemann | Nền tảng | Hình chữ nhật mảnh dần, sai số co về 0 | Ước lượng quãng đường từ bảng vận tốc |
| **INT12** 🟢 | Định nghĩa tích phân & Newton–Leibniz · F(b)−F(a), diện tích có dấu | Nền tảng | Diện tích tô màu = độ chênh độ cao của F | Tích phân không phụ thuộc chọn C |
| **INT13** 🟢 | Tính chất của tích phân · tuyến tính, cộng khoảng, đổi cận | Thông hiểu | Cắt – ghép miền diện tích | Đúng/Sai về tính chất |
| **INT14** 🟢 | Tích phân chứa trị tuyệt đối & hàm từng khúc | Vận dụng 7+ | Lật phần âm lên trên trục | ∫₀³\|x²−3x+2\|dx |
| **INT15** 🟢 | Tích phân, độ dời và quãng đường · v(t), a(t) | Vận dụng 8+ | Xe đổi chiều: độ dời ≠ quãng đường | Trả lời ngắn quãng đường phanh |
| **INT16** 🟣 | Tích phân đổi biến số · đổi biến phải đổi cận | Vận dụng 8+ | Miền lấy tích phân co giãn theo u | Bẫy giữ nguyên cận cũ |
| **INT17** 🟣 | Tích phân từng phần · chọn u – dv | Vận dụng 8+ | Diện tích hình chữ nhật uv tách làm hai | ∫₀¹ x eˣ dx |
| **INT18** 🟣 | Tích phân hàm ẩn & tính đối xứng · chẵn – lẻ, f(a+b−x) | Vận dụng cao 9+ | Gập đối xứng miền diện tích | ∫ f(x) biết f(x)+f(−x)=g(x) |
| **INT19** 🟣 | Hàm ẩn từ phương trình vi phân đơn giản | Vận dụng cao 9+ | Trường hướng tổng quát, nghiệm qua điểm | f'(x)=x·f²(x), f(1)=… |
| **INT20** 🟢 | Tổng ôn tích phân theo 3 dạng câu hỏi | Tổng hợp | Bảng tổng hợp động | Mini-đề 10 câu |

### PHẦN C – ỨNG DỤNG HÌNH HỌC (INT21 – INT28)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **INT21** 🟢 | Diện tích hình phẳng giới hạn bởi đồ thị và Ox · ∫\|f\| | Thông hiểu | Diện tích dương/âm tách màu | Bẫy quên trị tuyệt đối |
| **INT22** 🟢 | Diện tích giữa hai đường cong · giao điểm & chia khoảng | Vận dụng 7+ | Dải mỏng "trên trừ dưới" quét ngang | Parabol và đường thẳng |
| **INT23** 🟢 | Diện tích hình ghép & bài toán tham số · tối ưu | Vận dụng cao 9+ | Kéo tham số m, diện tích thay đổi trực tiếp | Tìm m để hai phần diện tích bằng nhau |
| **INT24** 🟢 | Đọc diện tích từ đồ thị f' · so sánh f(a), f(b) | Vận dụng cao 9+ | Diện tích = độ biến thiên của f | Sắp thứ tự f(0), f(2), f(5) |
| **INT25** 🟢 | Thể tích vật thể theo thiết diện S(x) | Thông hiểu | Cắt lát 3D – xếp chồng | Thiết diện tam giác đều |
| **INT26** 🟢 | Thể tích khối tròn xoay quanh Ox · phương pháp đĩa | Thông hiểu | Quay miền phẳng 360° trong 3D | V = π∫f² dx |
| **INT27** 🟢 | Khối tròn xoay giữa hai đường · vành khăn | Vận dụng 8+ | Đĩa khoét lỗ | Bẫy π∫(f−g)² |
| **INT28** 🟢 | Chứng minh thể tích nón, cầu, chỏm cầu | Vận dụng 8+ | Quay tam giác, nửa đường tròn | Dựng lại công thức bằng tích phân |

### PHẦN D – ỨNG DỤNG THỰC TẾ & MÔ HÌNH HÓA (INT29 – INT33)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **INT29** 🟢 | Bài toán chuyển động thực tế · phanh xe, hai xe gặp nhau | Vận dụng 8+ | Hai xe trên trục đường + đồ thị v(t) đồng bộ | Trả lời ngắn: thời điểm gặp nhau |
| **INT30** 🟢 | Thiết kế: cổng parabol, logo, mảnh vườn | Vận dụng 8+ | Chọn hệ trục phù hợp trên ảnh thực | Chi phí trồng hoa theo diện tích |
| **INT31** 🟢 | Bồn chứa, bể nước và lưu lượng | Vận dụng 8+ | Mực nước dâng theo lưu lượng thay đổi | Thời gian đầy bể |
| **INT32** 🟢 | Tích phân trong kinh tế và sinh học | Vận dụng 8+ | Chi phí biên → tổng chi phí | Lợi nhuận tăng thêm khi sản xuất thêm |
| **INT33** 🟢 | Mô hình hóa từ dữ liệu thực | Vận dụng cao 9+ | Từ bảng số → hàm → tích phân | Câu trả lời ngắn nhiều bước |

### PHẦN E – TỔNG ÔN & LUYỆN ĐỀ (INT34 – INT36)

| Mã | Tên tập · Dạng/kỹ thuật | Mức | Trực quan Manim chủ đạo | Bài toán "đinh" / dạng đề mới |
| :--- | :--- | :---: | :--- | :--- |
| **INT34** 🟢 | Những bẫy sai kinh điển & kiểm tra bằng máy tính | Tổng hợp | "Phòng khám lỗi sai" – từng lỗi một | Kiểm tra nguyên hàm bằng d/dx |
| **INT35** 🟢 | Luyện đề theo cấu trúc thi tốt nghiệp | Tổng hợp | Đồng hồ đếm giờ + lời giải nhanh | 12 TN – 4 Đ/S – 6 TLN phần tích phân |
| **INT36** 🟢 | Bản đồ tư duy toàn chương · chiến lược 8+/9+ | Tổng hợp | Bản đồ tư duy mở dần | Lộ trình tự học sau series |

---

## 4. Chuẩn đặt tên & xuất bản

- **Tiêu đề YouTube:** `INTxx: <Tên tập> | <Dạng/kỹ thuật> - Thầy Nguyễn Văn Sang` (tối đa 95 ký tự; lấy từ `series_plan.json`).
- **Mô tả YouTube:** sinh tự động từ `intXX/runtime_plan.json`, **có mốc chương (00:00 …)** để YouTube hiện chapter, kèm mục tiêu bài và bài tự luyện.
- **Phụ đề:** `INTxx_vi.srt` (căn theo ranh giới câu do Edge TTS trả về), được tải lên YouTube cùng video.
- **Playlist:** “Nguyên Hàm - Tích Phân - Ứng Dụng Chuyên Sâu | Thầy Nguyễn Văn Sang”.

## 5. Quy trình sản xuất một tập (CI)

```text
intXX/lesson.py  (lời giảng + kiểm SymPy)
      │
      ├─ scripts/build_typst.py   → assets/intXX_formulas/*.svg (Typst thật, lỗi là dừng)
      ├─ scripts/prepare_voice.py → MP3 từng nhịp + runtime_plan.json + INTxx_vi.srt
      ├─ manim … INTxx_SMOKE      → render kỹ thuật toàn bộ nhịp, độ phân giải thấp
      ├─ manim … INTxx            → preview 854×480 hoặc Full HD 1920×1080
      ├─ scripts/qa_video.py      → kiểm tra luồng hình/tiếng, thời lượng, ảnh từng phần
      └─ upload_to_youtube.py     → video + mô tả có chapter + phụ đề + playlist
```

Thứ tự chạy workflow cho mỗi tập: `preview / voice=off` (duyệt hình) → `preview / voice=on` (duyệt tiếng) → `fullhd / voice=on / upload=true` (xuất bản).

## 6. Tiến độ

| Trạng thái | Tập |
| :--- | :--- |
| ✅ Đã xuất bản | INT01 (youtu.be/MLP1NJgcDmQ) · INT02 (youtu.be/Q27qaS8mqqE) |
| 🎬 Đã dựng đầy đủ, đang xuất bản | INT03 |
| ⚪ Kế hoạch | INT04 – INT36 |

### Khối dùng chung đã có (`common/blocks.py`)

Thẻ tiêu đề · thẻ mục tiêu · câu Đúng/Sai 4 ý · phiếu trả lời ngắn · đồ thị kiểm tra "độ dốc F = chiều cao f" ·
3 ý cần nhớ · bài tập tự luyện có đáp số · thẻ tập sau. Mỗi tập mới chỉ cần viết phần hoạt họa riêng.

Lịch đề xuất: 2 tập/tuần → hoàn thành 36 tập trong khoảng 18 tuần; ưu tiên Phần A và B trước kỳ thi học kỳ II.
