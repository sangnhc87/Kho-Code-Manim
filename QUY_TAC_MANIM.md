# BỘ QUY TẮC CHUẨN XÂY DỰNG BÀI GIẢNG MANIM
> **Thương hiệu bài giảng: Thầy Nguyễn Văn Sang**  
> Áp dụng cho toàn bộ các bài giảng Toán THPT (Toán 10, 11, 12) sản xuất bằng Manim Community và AI Voiceover.

---

## I. NGUYÊN TẮC "1 Ô COLAB DUY NHẤT" (ALL-IN-ONE SINGLE CELL)

> **Yêu cầu sống còn**: Mỗi bài giảng là một tệp Python hoàn chỉnh, khép kín 100%. Người dùng chỉ cần copy toàn bộ nội dung tệp, dán vào **đúng 1 ô Code duy nhất trên Google Colab** và bấm Run là tự động ra video bài giảng hoàn chỉnh, không cần thao tác thêm bất cứ lệnh phụ nào.

### Quy trình 5 bước tự động tích hợp trong script:
1. **Bước 1 — Tự động cài đặt môi trường trọn gói**:
   - Nhận diện môi trường Colab (`if Path("/content").exists():`).
   - Tự động chạy `apt-get` cài đặt đầy đủ: `ffmpeg`, `pkg-config`, `libcairo2-dev`, `libpango1.0-dev`, font tiếng Việt `fonts-dejavu-core`, `fonts-noto-core`, hệ thống $\LaTeX$ `texlive-latex-base`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-science`, `dvisvgm`.
   - Tự động chạy `pip install`: `manim==0.19.0`, `edge-tts`, `nest_asyncio`.
   - Có cơ chế tạo file đánh dấu `env_ok.txt` để khi chạy lại không mất thời gian cài lại từ đầu.
2. **Bước 2 — Định nghĩa dữ liệu bài giảng & Tự động tạo Audio**:
   - Khởi tạo mảng dữ liệu `LESSONS` hoặc `SLIDES` chứa toàn bộ câu hỏi, mô hình, lời dẫn và công thức.
   - Gọi `edge-tts` sinh lời thoại với giọng `vi-VN-NamMinhNeural` tốc độ `-5%`.
   - Cache audio bằng mã băm MD5 và dùng `ffprobe` đo đạc thời lượng chính xác tuyệt đối từng câu.
3. **Bước 3 — Tạo mã nguồn Manim & Render hoạt họa**:
   - Tự động tạo và thực thi file kịch bản Manim Scene.
   - Render ở độ phân giải và FPS định sẵn bằng Cairo renderer (nhanh, chuẩn xác, không crash).
4. **Bước 4 — Ghép nối Audio và Video hoàn chỉnh**:
   - Sử dụng `ffmpeg` ghép video đồ họa từ Manim với toàn bộ file audio thuyết minh tiếng Việt đã chuẩn bị.
5. **Bước 5 — Trình chiếu & Cung cấp liên kết tải xuống**:
   - Tự động nén zip (nếu nhiều video) hoặc xuất video thành phẩm.
   - Hiển thị video trực tiếp trên output của Colab hoặc gọi `files.download()` khi hoàn tất.

---

## II. CẤU HÌNH HỆ THỐNG & NHẬN DIỆN THƯƠNG HIỆU (BẮT BUỘC)

Tất cả các file script Manim trong kho code phải khai báo chuẩn bộ thông số định danh ở đầu file:

```python
# ======================================================================
# CẤU HÌNH HỆ THỐNG & BẢN QUYỀN NỘI DUNG
# ======================================================================
TEN_THAY    = "Thầy Nguyễn Văn Sang"
GIONG_DOC   = "vi-VN-NamMinhNeural"
TOC_DO_DOC  = "-5%"

# Cấu hình video chuẩn
RESOLUTION  = "1280,720"   # Mặc định 720p tối ưu thời gian render, 1080p khi xuất bản HD
FPS         = 24           # 24 fps (chuẩn mượt cho bài giảng), 15 fps khi test nháp
```

### Yêu cầu hiển thị nhận diện (Header/Footer):
1. **Footer**: Luôn có dòng chữ nhận diện thương hiệu `Thầy Nguyễn Văn Sang` nằm góc dưới cùng (hoặc căn giữa dưới), font trang nhã, màu muted (`#7A9ABF`).
2. **Số trang / Tiến độ**: Luôn hiển thị vị trí bài học (ví dụ: `Bài 01/10 • Trang 2/3`).

---

## III. QUY TẮC CÔNG THỨC TOÁN HỌC & LATEX (BẮT BUỘC 100%)

> **Nguyên tắc vàng**: Tuyệt đối **KHÔNG** sử dụng `Text()` để gõ số, biến số, biểu thức hoặc công thức toán học (ví dụ: cấm `Text("x = 5")` hay `Text("S = pi*R^2")`). Mọi yếu tố toán học đều phải qua bộ dịch **$\LaTeX$** bằng `MathTex()`.

### 1. Phân định rõ ràng `Text` vs `MathTex`:
- **`Text()`**: Chỉ dùng cho câu văn giải thích, lời dẫn tiếng Việt thuần túy. Luôn chỉ định `font="DejaVu Sans"` (hoặc `Noto Sans`) để tránh lỗi dấu tiếng Việt.
- **`MathTex()`**: Dùng cho **toàn bộ** số, chữ cái đại diện cho biến ($x, y, z, t, a, b, c$), tham số, vectơ, hình học ($A, B, C, S$), hàm số, phương trình, hệ thức.

### 2. Thiết lập TexTemplate chuẩn:
Mọi file đều phải có template nạp đầy đủ gói toán học:
```python
TMPL = TexTemplate()
TMPL.add_to_preamble(r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{xcolor}\usepackage{bm}")

def mtx(s, size=30, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TMPL)
```

### 3. Quy chuẩn trình bày công thức:
- **Công thức trọng tâm / Kết luận**: Luôn đóng khung bằng `\boxed{}`:
  ```python
  mtx(r"\boxed{ v_{\text{dâng}} = h'(t) = \frac{v}{\pi R^2} }", color=GOLD)
  ```
- **Ký hiệu chỉ số / vector**: Viết đúng cú pháp chuẩn: `\vec{v}`, `\overrightarrow{AB}`, `x_{1,2}`, `\Delta t \to 0`.
- **Phân số**: Luôn dùng `\frac{...}{...}` hoặc `\dfrac{...}{...}` để nét phân số thanh thoát, rõ ràng.

---

## IV. CHUẨN MỰC NỘI DUNG SƯ PHẠM (CHUẨN - CHI TIẾT - DỄ HIỂU)

Mỗi bài toán phải được phân tách thành một kịch bản sư phạm 3 bước rõ ràng:

### Bước 1: Mô hình hóa & Đặt vấn đề trực quan
- Nêu đề bài ngắn gọn, làm nổi bật đại lượng đã cho và đại lượng cần tìm.
- Cột bên trái hiển thị mô hình hình học / đồ thị động minh họa cho bài toán.

### Bước 2: Phân tích & Lập luận toán học từng bước
- Không đưa ra công thức đột ngột; phải dẫn dắt lý do vì sao dùng công thức đó.
- Các bước biến đổi đại số / vi phân / tích phân phải xuất hiện tuần tự theo nhịp đọc của lời giảng.
- Đối với các bài toán thực tế (Related Rates, Cực trị, Tiệm cận): nêu rõ ý nghĩa vật lý/kinh tế của từng biến số.

### Bước 3: Đóng khung kết luận & Nhận xét sư phạm
- Kết luận đáp số rõ ràng trong khung nổi bật.
- Kèm theo nhận xét / mẹo giải nhanh hoặc ý nghĩa thực tế (ví dụ: *nước dâng nhanh hay chậm dần*, *chi phí tiến dần đến mức sàn nào*...).

---

## V. QUY CHUẨN ĐỒ HỌA HÌNH HỌC (2D, 3D, NÉT ĐỨT, NÉT LIỀN)

### 1. Quy ước nét vẽ chuẩn SGK hình học:
- **Nét thấy (Visible line)**: Dùng `Line`, `Polygon`, `Arc` với nét liền, độ dày `stroke_width=3`.
- **Nét khuất / Đường gióng / Đường phụ (Hidden/Auxiliary line)**:
  - Bắt buộc dùng `DashedLine()` với `dash_length=0.08` đến `0.12`.
  - Màu sắc đường phụ nên nhạt hơn (`MUTED` hoặc opacity thấp hơn) để không lấn át hình chính.
- **Ký hiệu góc vuông**: Dùng `RightAngle()` hoặc vẽ 2 đoạn thẳng vuông góc nhỏ góc $90^\circ$.
- **Độ dài & Tọa độ**: Các mũi tên chỉ kích thước `DoubleArrow()`, nhãn kích thước $R, H, h(t), x$ đặt lệch nhẹ khỏi đường nét để không bị đè chữ.

### 2. Mô hình hóa hình học (Ưu tiên mô hình mặt cắt trực quan):
- Để tránh lỗi treo GPU/Colab với `ThreeDScene`, các khối 3D (nón, trụ, cầu, chóp) được mô hình hóa bằng **mặt cắt 2D xuyên trục** kết hợp với hình elip phối cảnh (`Ellipse`) thể hiện mặt thoáng / đáy tròn.
- Mực nước / chất lỏng / miền diện tích tô màu trong suốt với `fill_opacity=0.25 - 0.45` để vẫn nhìn thấy trục tọa độ và đường phụ phía sau.

---

## VI. HỆ THỐNG MÀU SẮC (PREMIUM DARK PALETTE) & HIỆU ỨNG

### 1. Bảng màu chuẩn:
```python
BG     = "#0b1120"   # Xanh đen vũ trụ sâu thẳm (Deep Slate/Navy)
PANEL  = "#0e1d34"   # Khung chứa nội dung / bảng tóm tắt
INK    = "#EDF4FF"   # Chữ trắng ngà chống mỏi mắt (Primary Text)
MUTED  = "#7A9ABF"   # Chú thích phụ, đường gióng mờ
BLUE   = "#38BDF8"   # Nét vẽ hình học, đồ thị chính (Sky Blue)
CYAN   = "#3ADEC8"   # Điểm di động, vector, nước dâng
GOLD   = "#FFD700"   # Kết quả đóng khung, công thức mấu chốt, đáp án
GREEN  = "#4ADE80"   # Điều kiện nghiệm đúng, dữ kiện đã biết
RED    = "#FF6B6B"   # Điểm giới hạn, miền loại, cảnh báo sai lầm
ORANGE = "#FB923C"   # Nhấn mạnh biến trung gian
```

### 2. Hiệu ứng chuyển động (Motion & Animation):
- **Xuất hiện**: Dùng `FadeIn(mob, shift=UP*0.2)` hoặc `Write()` cho công thức. Tránh hiện ra đột ngột.
- **Biến đổi**: Khi chuyển vế đổi dấu hoặc thế phương trình, dùng `TransformMatchingTex()` hoặc `ReplacementTransform()` để học sinh theo dõi được dòng suy nghĩ.
- **Nhấn mạnh trọng tâm**: Dùng `Indicate(mob, color=GOLD)` hoặc `Circumscribe(mob, color=CYAN)` khi giọng đọc nhắc đến đại lượng đó.
- **Đồ thị / Mực nước**: Dùng `ValueTracker` kết hợp `always_redraw()` để mô phỏng mực nước dâng thật, tiếp tuyến trượt trên đường cong thật.

---

## VII. ĐỒNG BỘ GIỌNG ĐỌC AI (`edge-tts`) & AUDIO PIPELINE

1. **Phiên âm toán học cho lời đọc (`voice`)**:
   - Viết lời thoại tự nhiên theo cách giáo viên đọc trên lớp:
     - $V'(t) \to$ *"Đạo hàm của thể tích V theo thời gian"* hoặc *"V phẩy"*
     - $\pi R^2 \to$ *"Pi nhân R bình phương"*
     - $\frac{v}{\pi R^2} \to$ *"v chia cho Pi nhân R bình phương"*
     - $\Delta \to$ *"đen-ta"*, $\alpha \to$ *"an-pha"*
2. **Cơ chế Hash Audio Cache**:
   - Dùng hash MD5 chuỗi văn bản lời thoại + tên giọng + tốc độ để đặt tên file `audio_cache/{hash}.wav`.
   - Kiểm tra dung lượng và tính hợp lệ qua `ffprobe`. Không tạo lại audio nếu đã có sẵn.
3. **Khớp hình và tiếng (Syncing)**:
   - Dùng `probe_dur(audio_file)` lấy thời gian chính xác từng phần.
   - Hoạt họa trong Manim điều phối tốc độ sao cho animation kết thúc vừa vặn hoặc `self.wait(max(0.1, duration - anim_time))`, tạo trải nghiệm xem mượt mà như video bài giảng chuyên nghiệp.
