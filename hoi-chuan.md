Bnj thiết kế bài khoảng cách min giauwx 2 hàm số, 2 đối tượng toán thực tế chương hàm số lớp 12, đa dạng mô hình hoá ~>=10 bài, mô hình thực tế, giải chi tiết thoả # MANIM TEACHING SPEC
## Bộ quy tắc chuẩn xây dựng bài giảng Toán THPT bằng Manim

**Thương hiệu bài giảng:** Thầy Nguyễn Văn Sang  
**Phạm vi áp dụng:** Toán THPT 10, 11, 12  
**Công nghệ chính:** Python + Manim Community + LaTeX/MathTex + Edge TTS + FFmpeg + Google Colab  
**Mục tiêu:** Sinh code Manim ổn định, đẹp, đồng nhất, có tính sư phạm cao và có thể chạy tự động trên Google Colab.

---

# 1. MỤC TIÊU CHUNG

Mọi bài giảng Manim phải đáp ứng đồng thời các yêu cầu sau:

1. Nội dung toán học chính xác.
2. Hình vẽ rõ ràng, đúng quy ước hình học.
3. Bố cục nhất quán giữa các bài.
4. Animation phục vụ việc giảng bài, không dùng hiệu ứng chỉ để trang trí.
5. Màu sắc có ý nghĩa cố định.
6. Công thức toán học dùng LaTeX thông qua `MathTex`.
7. Văn bản tiếng Việt dùng `Text`.
8. Hình 3D chỉ dùng khi thực sự cần thiết.
9. Ưu tiên khả năng render ổn định trên Google Colab.
10. Code phải có cấu trúc rõ ràng, dễ sửa và dễ tái sử dụng.
11. Audio phải đồng bộ hợp lý với animation.
12. Có thể xuất video hoàn chỉnh mà người dùng chỉ cần chạy một ô Colab duy nhất.

---

# 2. TRIẾT LÝ THIẾT KẾ

Mọi bài giảng phải tuân theo thứ tự ưu tiên sau:

```text
Đúng toán học
→ Dễ hiểu
→ Bố cục rõ ràng
→ Animation hợp lý
→ Hình ảnh đẹp
→ Render ổn định
→ Tối ưu tốc độ
```

Không được hy sinh tính dễ hiểu hoặc tính chính xác chỉ để tạo hiệu ứng đẹp.

---

# 3. NGUYÊN TẮC SINGLE-CELL COLAB

Mỗi bài giảng phải có thể được đóng gói thành một script Python hoàn chỉnh.

Người dùng chỉ cần:

```text
Copy toàn bộ script
→ Paste vào một ô Code duy nhất trên Google Colab
→ Run
→ Nhận video hoàn chỉnh
```

Tuy nhiên bên trong script có thể tự động tạo nhiều file tạm.

Khuyến nghị kiến trúc:

```text
Single-cell UX
Multi-file architecture
```

Ví dụ:

```text
Colab Cell
│
├── cài môi trường
├── tạo lesson.py
├── tạo lesson_data.py
├── tạo audio
├── render Manim
├── ghép audio
├── tạo subtitle
└── xuất video
```

Không nên viết một file `construct()` dài hàng nghìn dòng nếu có thể chia helper function.

---

# 4. PHIÊN BẢN VÀ MÔI TRƯỜNG

Ưu tiên pin version để đảm bảo khả năng render lặp lại.

Ví dụ:

```python
MANIM_VERSION = "0.21.0"
```

Cài đặt:

```bash
pip install "manim==0.21.0"
pip install edge-tts
pip install nest_asyncio
```

Cài thêm hệ thống cần thiết:

```bash
apt-get update
apt-get install -y \
    ffmpeg \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    fonts-dejavu-core \
    fonts-noto-core \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-science \
    dvisvgm
```

Không tự động nâng phiên bản Manim bằng:

```bash
pip install -U manim
```

trong production.

---

# 5. CẤU HÌNH HỆ THỐNG CHUẨN

Mỗi file phải có phần cấu hình đầu file.

```python
# ==========================================================
# SYSTEM CONFIG
# ==========================================================

TEN_THAY = "Thầy Nguyễn Văn Sang"

GIONG_DOC  = "vi-VN-NamMinhNeural"
TOC_DO_DOC = "-5%"

PREVIEW_WIDTH  = 854
PREVIEW_HEIGHT = 480
PREVIEW_FPS    = 15

STANDARD_WIDTH  = 1280
STANDARD_HEIGHT = 720
STANDARD_FPS    = 24

FINAL_WIDTH  = 1920
FINAL_HEIGHT = 1080
FINAL_FPS    = 30
```

---

# 6. CHẾ ĐỘ RENDER

Phải hỗ trợ ba chế độ.

## 6.1 Preview

Dùng khi đang chỉnh bài.

```text
854 × 480
15 FPS
```

## 6.2 Standard

Dùng để kiểm tra video gần hoàn chỉnh.

```text
1280 × 720
24 FPS
```

## 6.3 Final

Dùng để xuất bản.

```text
1920 × 1080
30 FPS
```

Không render 1080p trong tất cả các lần test.

---

# 7. HỆ THỐNG MÀU CHUẨN

```python
BG      = "#0B1120"
PANEL   = "#0E1D34"

INK     = "#EDF4FF"
MUTED   = "#7A9ABF"

BLUE    = "#38BDF8"
CYAN    = "#3ADEC8"
GOLD    = "#FFD700"
GREEN   = "#4ADE80"
RED     = "#FF6B6B"
ORANGE  = "#FB923C"
```

## Ý nghĩa màu bắt buộc

```text
INK
→ nội dung chính

MUTED
→ chú thích phụ
→ đường phụ
→ nét khuất
→ metadata

BLUE
→ đối tượng hình học chính
→ đồ thị chính

CYAN
→ đối tượng đang thay đổi
→ điểm chuyển động
→ vector chuyển động

GOLD
→ kết luận
→ đáp án
→ công thức trọng tâm

GREEN
→ giả thiết đúng
→ điều kiện hợp lệ
→ dữ kiện đã biết

RED
→ sai
→ loại
→ cảnh báo
→ miền không hợp lệ

ORANGE
→ biến trung gian
→ đại lượng đang phân tích
```

Không thay đổi ý nghĩa màu giữa các bài.

---

# 8. BACKGROUND VÀ PANEL

Background mặc định:

```python
config.background_color = BG
```

Panel dùng:

```python
RoundedRectangle(
    corner_radius=0.18,
    fill_color=PANEL,
    fill_opacity=0.88,
    stroke_color=MUTED,
    stroke_opacity=0.22,
    stroke_width=1.5,
)
```

Không dùng quá nhiều panel trên cùng một scene.

---

# 9. FONT VĂN BẢN TIẾNG VIỆT

Ưu tiên:

```text
DejaVu Sans
Noto Sans
```

Ví dụ:

```python
Text(
    "Ta xét hàm số sau",
    font="DejaVu Sans",
    color=INK,
)
```

Không dùng font lạ chưa chắc có trên Google Colab.

---

# 10. QUY TẮC TEXT VÀ MATHTEX

## 10.1 Text

Dùng `Text()` cho:

```text
câu văn tiếng Việt
tiêu đề
hướng dẫn
chú thích
metadata
footer
số trang
số câu
```

Ví dụ:

```python
Text("Bài 01/10 • Trang 2/3")
```

được phép.

## 10.2 MathTex

Dùng `MathTex()` cho:

```text
biến
biểu thức
hàm số
phương trình
tọa độ
vector
ký hiệu hình học
số mang ý nghĩa toán học
```

Ví dụ:

```python
MathTex(r"x^2 - 5x + 6 = 0")
```

Không dùng:

```python
Text("x^2 - 5x + 6 = 0")
```

---

# 11. LATEX TEMPLATE CHUẨN

```python
TMPL = TexTemplate()

TMPL.add_to_preamble(
    r"""
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{bm}
    \usepackage{xcolor}
    \usepackage{mathtools}
    """
)

def mtx(s, size=34, color=INK):
    return MathTex(
        s,
        font_size=size,
        color=color,
        tex_template=TMPL,
    )
```

Mọi helper toán nên đi qua `mtx()` nếu có thể.

---

# 12. QUY CHUẨN CÔNG THỨC

## Phân số

Ưu tiên:

```latex
\frac{a}{b}
```

hoặc:

```latex
\dfrac{a}{b}
```

Không viết:

```text
a/b
```

nếu biểu thức cần trình bày toán học rõ ràng.

## Vector

```latex
\vec{v}
\overrightarrow{AB}
```

## Chỉ số

```latex
x_1
x_2
x_{1,2}
```

## Giới hạn

```latex
\Delta t \to 0
```

## Công thức kết luận

Ưu tiên:

```latex
\boxed{...}
```

Ví dụ:

```python
mtx(
    r"\boxed{h'(t)=\frac{v}{\pi R^2}}",
    color=GOLD,
)
```

---

# 13. LAYOUT CHUẨN

Mỗi scene phải nằm trong safe area.

Không đặt nội dung sát mép frame.

Khuyến nghị:

```text
Top safe area    ≈ 0.35
Bottom safe area ≈ 0.35
Left safe area   ≈ 0.35
Right safe area  ≈ 0.35
```

---

# 14. LAYOUT HAI CỘT

Dùng mặc định cho bài có hình + công thức.

```text
┌──────────────────────────────────────┐
│              TIÊU ĐỀ                 │
├────────────────┬─────────────────────┤
│                │                     │
│     HÌNH       │       TOÁN          │
│     45%        │       55%           │
│                │                     │
├────────────────┴─────────────────────┤
│ Thầy Nguyễn Văn Sang • Trang ...     │
└──────────────────────────────────────┘
```

Không để hình chạy sang cột toán.

Không để công thức đè lên hình.

---

# 15. LAYOUT ĐẠI SỐ

Nếu không có hình minh họa:

```text
centered content
```

Không để toàn bộ nội dung lệch một phía vô lý.

---

# 16. TITLE

Title luôn ở vị trí thống nhất.

Ví dụ:

```python
title = Text(
    "Ứng dụng đạo hàm",
    font="DejaVu Sans",
    font_size=34,
    color=INK,
)
```

Nên đặt:

```python
title.to_edge(UP, buff=0.25)
```

Không đổi vị trí title giữa các scene.

---

# 17. FOOTER

Mỗi scene phải có footer.

Ví dụ:

```text
Thầy Nguyễn Văn Sang • Bài 01/10 • Trang 2/5
```

Màu:

```python
MUTED
```

Font nhỏ hơn nội dung chính.

Không dùng GOLD hoặc BLUE cho footer.

---

# 18. CẤU TRÚC SƯ PHẠM

Mỗi bài nên theo cấu trúc:

```text
0. Câu hỏi kích hoạt
1. Mô hình hóa
2. Phân tích
3. Tính toán
4. Kết luận
5. Nhận xét
```

---

# 19. CÂU HỎI KÍCH HOẠT

Nếu phù hợp, mở đầu bằng một câu hỏi.

Ví dụ:

```text
Nếu nước chảy vào đều thì mực nước có dâng đều không?
```

Không mở đầu bằng công thức dài nếu chưa có ngữ cảnh.

---

# 20. MÔ HÌNH HÓA

Phải xác định:

```text
đại lượng đã biết
đại lượng cần tìm
biến phụ thuộc
biến độc lập
quan hệ giữa các đại lượng
```

Hình minh họa nên xuất hiện cùng lúc với việc giới thiệu biến.

---

# 21. PHÂN TÍCH

Không đưa công thức cuối ngay lập tức.

Phải cho học sinh thấy:

```text
vì sao dùng công thức
công thức đến từ đâu
biến nào phụ thuộc biến nào
```

---

# 22. TÍNH TOÁN

Các bước biến đổi phải xuất hiện tuần tự.

Ưu tiên:

```python
TransformMatchingTex()
```

Ví dụ:

```python
eq1 = MathTex(r"x^2-5x+6=0")
eq2 = MathTex(r"(x-2)(x-3)=0")

self.play(
    TransformMatchingTex(eq1, eq2)
)
```

---

# 23. KẾT LUẬN

Kết luận phải:

```text
ngắn
rõ
đóng khung
dùng GOLD
```

Ví dụ:

```python
answer = MathTex(
    r"\boxed{x=2\text{ hoặc }x=3}",
    color=GOLD,
)
```

---

# 24. NHẬN XÉT SƯ PHẠM

Nếu phù hợp, thêm:

```text
mẹo
ý nghĩa hình học
ý nghĩa vật lý
ý nghĩa thực tế
cảnh báo sai lầm
```

Không thêm nhận xét chỉ để kéo dài video.

---

# 25. QUY TẮC ANIMATION

Animation phải có ý nghĩa sư phạm.

Mapping mặc định:

```text
Text mới              → FadeIn
Công thức mới         → Write
Đường/hình mới        → Create
Biến đổi công thức    → TransformMatchingTex
Thay object           → ReplacementTransform
Nhấn mạnh             → Indicate / Circumscribe
Ẩn object             → FadeOut
Điểm chuyển động      → ValueTracker
Hình động liên tục    → always_redraw
```

---

# 26. HIỆU ỨNG NÊN HẠN CHẾ

Không lạm dụng:

```python
Flash()
Wiggle()
SpinInFromNothing()
GrowFromCenter()
```

Chỉ dùng khi có mục đích rõ ràng.

Một bài giảng tốt thường chỉ cần:

```text
Fade
Create
Write
Transform
Highlight
```

---

# 27. TIMING CHUẨN

```python
ANIM_FAST   = 0.4
ANIM_NORMAL = 0.8
ANIM_SLOW   = 1.4
```

Không dùng animation toán học quan trọng ngắn hơn khoảng:

```text
0.7 giây
```

trừ khi rất đơn giản.

Không làm hàng loạt animation 0.1–0.2 giây.

---

# 28. GIỮ NGƯỜI HỌC THEO KỊP

Sau một công thức quan trọng:

```python
self.wait(0.3)
```

hoặc lâu hơn nếu cần.

Không xuất hiện 4–5 dòng công thức liên tiếp trong chưa đầy một giây.

---

# 29. HÌNH HỌC 2D

Nét thấy:

```python
Line(
    ...,
    stroke_width=3,
)
```

Nét phụ:

```python
stroke_width=2
```

---

# 30. NÉT KHUẤT VÀ ĐƯỜNG PHỤ

Phải dùng:

```python
DashedLine(
    ...,
    dash_length=0.08,
)
```

hoặc khoảng:

```text
0.08 – 0.12
```

Màu:

```python
MUTED
```

hoặc giảm opacity.

---

# 31. ĐIỂM HÌNH HỌC

```python
POINT_RADIUS = 0.055
```

Ví dụ:

```python
Dot(
    point,
    radius=POINT_RADIUS,
    color=BLUE,
)
```

---

# 32. NHÃN ĐIỂM

Dùng:

```python
MathTex("A")
```

Không dùng:

```python
Text("A")
```

nếu `A` là ký hiệu hình học.

Ví dụ:

```python
label_A.next_to(dot_A, UR, buff=0.08)
```

---

# 33. TRÁNH CHỒNG NHÃN

Mọi nhãn phải:

```text
không đè đường
không đè điểm
không đè công thức
không chạm mép frame
```

Nếu có thể, đặt label bằng:

```python
next_to()
```

thay vì tọa độ tuyệt đối.

---

# 34. GÓC VUÔNG

Ưu tiên:

```python
RightAngle()
```

Nếu không phù hợp, vẽ hai đoạn nhỏ.

---

# 35. KÍCH THƯỚC

Dùng:

```python
DoubleArrow()
```

hoặc line + label.

Ví dụ:

```text
R
H
h(t)
x
```

Nhãn phải lệch khỏi đường kích thước.

---

# 36. ĐỒ THỊ

Dùng:

```python
Axes()
```

và:

```python
plot()
```

Đồ thị chính:

```python
BLUE
```

Điểm đang xét:

```python
CYAN
```

Tiệm cận:

```python
MUTED
```

Điểm loại:

```python
RED
```

---

# 37. VALUE TRACKER

Dùng khi có đại lượng thay đổi liên tục.

Ví dụ:

```python
tracker = ValueTracker(0)
```

Không dùng `ValueTracker` nếu object chỉ đổi một lần.

---

# 38. ALWAYS_REDRAW

Chỉ dùng khi object thực sự phụ thuộc liên tục vào tracker.

Ví dụ:

```python
point = always_redraw(
    lambda: Dot(
        axes.c2p(
            tracker.get_value(),
            f(tracker.get_value()),
        ),
        color=CYAN,
    )
)
```

Không tạo quá nhiều `always_redraw()` cùng lúc.

---

# 39. PERFORMANCE RULE

Nếu object chỉ cần thay đổi một lần:

```python
Transform()
```

tốt hơn `always_redraw()`.

Nếu có thể dùng 2D thì không dùng 3D.

Nếu có thể dùng object tĩnh thì không dùng updater.

---

# 40. HÌNH 3D — NGUYÊN TẮC CHUNG

Không mặc định dùng `ThreeDScene`.

Mọi hình không gian phải được phân loại:

```text
A. 2D projection
B. pseudo-3D
C. real 3D
```

---

# 41. MỨC A — 2D PROJECTION

Ưu tiên cho:

```text
hình hộp
hình chóp
lăng trụ
tứ diện
hình trụ
hình nón
```

nếu bài không cần quay không gian.

Dùng:

```text
Line
DashedLine
Polygon
Ellipse
```

---

# 42. MỨC B — PSEUDO-3D

Dùng phối cảnh 2D để tạo cảm giác không gian.

Ví dụ hình trụ:

```text
ellipse trên
ellipse dưới
hai cạnh bên
mặt nước ellipse
```

Cách này ưu tiên cho:

```text
bài mực nước
related rates
thể tích
mặt cắt
```

---

# 43. MỨC C — REAL 3D

Chỉ dùng `ThreeDScene` khi cần:

```text
vector không gian
mặt phẳng
giao tuyến
rotation để hiểu cấu trúc
surface
tọa độ Oxyz
```

---

# 44. CAMERA 3D

Khởi tạo:

```python
self.set_camera_orientation(
    phi=65 * DEGREES,
    theta=-45 * DEGREES,
)
```

Không quay camera liên tục chỉ để cho đẹp.

Một scene thường chỉ cần tối đa:

```text
1–2 camera transitions quan trọng
```

---

# 45. CAMERA MOVEMENT

Ví dụ:

```python
self.move_camera(
    phi=70 * DEGREES,
    theta=-25 * DEGREES,
    run_time=2,
)
```

Camera motion phải giúp học sinh hiểu một cấu trúc mới.

---

# 46. SURFACE 3D

Surface phải:

```text
giảm opacity
không che điểm quan trọng
không che trục
không che giao tuyến
```

Ưu tiên opacity vừa phải.

---

# 47. MÔ HÌNH CHẤT LỎNG

Nếu có nước/chất lỏng:

```text
fill_opacity khoảng 0.25–0.45
```

Màu:

```python
CYAN
```

Không tô quá đậm làm mất đường phụ.

---

# 48. AUDIO PIPELINE

Dùng:

```text
edge-tts
```

Voice mặc định:

```text
vi-VN-NamMinhNeural
```

Rate:

```text
-5%
```

---

# 49. PHIÊN ÂM TOÁN CHO VOICE

Không gửi trực tiếp công thức LaTeX cho TTS.

Phải viết lời đọc tự nhiên.

Ví dụ:

```text
V'(t)
→ V phẩy theo t

πR²
→ pi nhân R bình phương

v/(πR²)
→ v chia cho pi nhân R bình phương
```

---

# 50. AUDIO CACHE

Tên file audio phải dựa trên hash của:

```text
text
voice
rate
pitch
engine
```

Khuyến nghị dùng:

```text
SHA-256
```

Ví dụ payload:

```python
{
    "text": text,
    "voice": voice,
    "rate": rate,
    "pitch": pitch,
    "engine": "edge-tts",
}
```

---

# 51. AUDIO FORMAT

Edge TTS có thể lưu:

```text
.mp3
```

Không giả định output gốc là WAV.

Nếu cần WAV:

```bash
ffmpeg -i input.mp3 output.wav
```

---

# 52. AUDIO DURATION

Dùng:

```text
ffprobe
```

để lấy duration.

Không ước lượng bằng số ký tự.

---

# 53. AUDIO–ANIMATION SYNC

Không ép animation luôn dài đúng bằng audio.

Nguyên tắc:

```text
segment_duration
=
max(
    audio_duration,
    minimum_visual_duration
)
```

Nếu audio dài:

```text
animation chạy trước
→ giữ hình thêm
```

Nếu animation cần lâu:

```text
không tăng tốc quá mức chỉ để khớp audio
```

---

# 54. CẤU TRÚC SEGMENT

Khuyến nghị:

```python
{
    "voice": "...",
    "math": "...",
    "visual_action": "...",
    "highlight": "...",
    "min_visual_time": 2.0,
}
```

---

# 55. SUBTITLE

Mỗi video nên tự động sinh:

```text
.srt
.vtt
```

Dựa trên:

```text
text
start_time
duration
```

---

# 56. PHỤ ĐỀ

Subtitle phải:

```text
ngắn
đúng câu
không hiển thị nguyên LaTeX
```

Dùng cách đọc tự nhiên.

---

# 57. FOOTER THƯƠNG HIỆU

Bắt buộc có:

```text
Thầy Nguyễn Văn Sang
```

Màu:

```python
MUTED
```

Không quá nổi.

---

# 58. PROGRESS

Hiển thị:

```text
Bài 01/10 • Trang 2/5
```

hoặc format tương tự.

Không để progress chiếm không gian nội dung.

---

# 59. CODE STRUCTURE

File Python phải có cấu trúc:

```text
1. Imports
2. System config
3. Colors
4. TexTemplate
5. Helper functions
6. Lesson data
7. Scene classes
8. Audio helpers
9. Render helpers
10. Export
```

---

# 60. HELPER FUNCTIONS

Nên có:

```python
def mtx(...):
    ...

def make_title(...):
    ...

def make_footer(...):
    ...

def make_panel(...):
    ...

def label_point(...):
    ...

def create_audio(...):
    ...

def probe_duration(...):
    ...
```

---

# 61. KHÔNG NHÉT TOÀN BỘ VÀO CONSTRUCT

Sai:

```python
class Lesson(Scene):
    def construct(self):
        # 1500 dòng
```

Đúng hơn:

```python
class Lesson(Scene):

    def show_intro(self):
        ...

    def show_model(self):
        ...

    def show_solution(self):
        ...

    def show_answer(self):
        ...

    def construct(self):
        self.show_intro()
        self.show_model()
        self.show_solution()
        self.show_answer()
```

---

# 62. DATA-DRIVEN LESSON

Ưu tiên tách dữ liệu:

```python
LESSON = {
    "title": "...",
    "slides": [
        ...
    ]
}
```

Không hard-code nội dung ở quá nhiều nơi.

---

# 63. SINGLE SOURCE OF TRUTH

Nếu có thể, dữ liệu bài học nên nằm trong:

```text
lesson.yaml
lesson.json
```

hoặc một dict Python duy nhất.

Từ dữ liệu này sinh:

```text
Manim
TTS
subtitle
SCORM
```

---

# 64. COLAB ENVIRONMENT CACHE

Không giả định:

```text
/content/env_ok.txt
```

tồn tại vĩnh viễn.

Nó chỉ tồn tại trong runtime hiện tại.

Nếu cần cache lâu dài:

```text
Google Drive
```

Ví dụ:

```text
/content/drive/MyDrive/manim_cache/
```

---

# 65. ASSET CACHE

Nên cache:

```text
audio
font
image
svg
render asset
```

Không cache file tạm không cần thiết.

---

# 66. FAIL-SAFE

Mỗi bước quan trọng phải kiểm tra.

Ví dụ:

```python
assert audio_path.exists()
assert video_path.exists()
```

Nếu command thất bại:

```text
dừng
in lỗi rõ ràng
```

Không tiếp tục ghép file hỏng.

---

# 67. SCORM — NGUYÊN TẮC

SCORM là tầng đóng gói LMS.

Không trộn logic SCORM vào Scene Manim.

Pipeline:

```text
Manim
→ MP4

TTS
→ MP3

Subtitle
→ VTT

sau đó

MP4 + VTT + HTML + imsmanifest.xml
→ SCORM ZIP
```

---

# 68. SCORM STRUCTURE

Ví dụ:

```text
lesson_scorm/
│
├── imsmanifest.xml
├── index.html
├── lesson.mp4
├── lesson.vtt
├── poster.webp
├── scorm.js
└── assets/
```

---

# 69. TYPST

Typst có thể được dùng làm:

```text
tài liệu PDF
worksheet
handout
bài tập
tóm tắt lý thuyết
```

Nhưng chuẩn Manim của hệ thống này vẫn là:

```text
Python + MathTex + LaTeX
```

Không bắt buộc chuyển MathTex sang MathTypst.

---

# 70. QUY TẮC CẤM

AI không được:

```text
1. Dùng Text cho công thức toán.
2. Đưa quá nhiều màu vào cùng một công thức.
3. Dùng camera 3D chỉ để trang trí.
4. Dùng ThreeDScene nếu 2D đủ rõ.
5. Tạo quá nhiều always_redraw.
6. Hard-code hàng chục tọa độ rời rạc.
7. Đặt text sát mép frame.
8. Để label chồng đường.
9. Để footer chồng nội dung.
10. Render Final mỗi lần test.
11. Dùng font chưa được đảm bảo có trên Colab.
12. Dùng animation ngẫu nhiên.
13. Biến đổi công thức bằng FadeOut/FadeIn nếu có thể dùng TransformMatchingTex.
14. Làm animation quá nhanh để học sinh không theo kịp.
15. Thay đổi ý nghĩa màu giữa các bài.
```

---

# 71. KIỂM TRA TRƯỚC KHI RENDER

AI phải kiểm tra logic:

```text
[ ] import đầy đủ
[ ] syntax hợp lệ
[ ] MathTex hợp lệ
[ ] font tồn tại
[ ] màu đúng spec
[ ] title không tràn
[ ] footer không chồng
[ ] hình nằm trong safe area
[ ] label không đè đường
[ ] công thức không tràn frame
[ ] animation có run_time hợp lý
[ ] ThreeDScene chỉ dùng khi cần
[ ] audio file tồn tại
[ ] ffprobe đọc được duration
```

---

# 72. KIỂM TRA SAU RENDER

Sau khi render:

```text
[ ] video mở được
[ ] audio nghe được
[ ] audio không lệch nghiêm trọng
[ ] không mất font
[ ] không có công thức bị cắt
[ ] không có object ngoài frame
[ ] màu dễ nhìn
[ ] không có frame đứng bất thường
[ ] subtitle hợp lệ
```

---

# 73. QUALITY GATE

Video chỉ được coi là hoàn thành khi đạt:

```text
Math correctness
Pedagogy clarity
Visual clarity
Audio clarity
Layout safety
Rendering stability
Brand consistency
```

---

# 74. CÁCH AI PHẢI SUY NGHĨ TRƯỚC KHI VIẾT CODE

Trước khi sinh code, AI phải nội bộ xác định:

```text
1. Scene nào cần thiết?
2. Mỗi scene dạy một ý gì?
3. Hình nào cần xuất hiện?
4. Công thức nào cần TransformMatchingTex?
5. Object nào thực sự cần ValueTracker?
6. Có cần 3D thật không?
7. Audio dài khoảng bao lâu?
8. Layout nào phù hợp?
9. Điểm nào cần highlight?
10. Có nguy cơ chồng object hay không?
```

Sau đó mới viết code.

---

# 75. FORMAT ĐẦU RA AI

Khi được yêu cầu tạo một bài giảng Manim hoàn chỉnh, AI phải ưu tiên trả:

```text
1 script hoàn chỉnh
```

có thể copy trực tiếp vào Google Colab.

Không trả pseudo-code nếu người dùng yêu cầu code hoàn chỉnh.

---

# 76. QUY TẮC ĐỒNG NHẤT TOÀN BỘ SERIES

Tất cả video trong cùng series phải giữ nguyên:

```text
palette
font
footer
title position
stroke width
animation semantics
camera convention
MathTex style
audio voice
audio rate
```

Không tự ý thiết kế lại style cho từng bài.

---

# 77. NGUYÊN TẮC TỐI GIẢN

Một scene chỉ nên chứa những thứ phục vụ một ý chính.

Nếu một scene quá nhiều:

```text
text
formula
diagram
table
highlight
arrow
```

hãy tách thành scene hoặc stage nhỏ hơn.

---

# 78. NGUYÊN TẮC VISUAL HIERARCHY

Mỗi frame phải cho người xem biết ngay:

```text
đâu là nội dung chính
đâu là dữ kiện
đâu là kết luận
```

Kích thước gợi ý:

```text
Title       30–38
Main text   26–32
Math        30–42
Footer      18–22
```

Tùy resolution có thể điều chỉnh.

---

# 79. NGUYÊN TẮC “KHÔNG TRANG TRÍ THỪA”

Không thêm:

```text
hạt sáng
particle
gradient phức tạp
camera shake
animation xoay
logo chuyển động liên tục
```

nếu không phục vụ bài học.

---

# 80. NGUYÊN TẮC KẾT LUẬN CUỐI CÙNG

Mọi bài giảng phải hướng tới tiêu chuẩn:

```text
CHÍNH XÁC
RÕ RÀNG
NHẸ
ỔN ĐỊNH
NHẤT QUÁN
DỄ HIỂU
DỄ TÁI SỬ DỤNG
```

Không tối ưu cho việc “trông nhiều hiệu ứng”.

Tối ưu cho:

```text
học sinh nhìn
→ hiểu
→ theo kịp
→ nhớ được
```

---

# MASTER DIRECTIVE FOR AI

Khi nhận tài liệu này, AI phải hiểu rằng đây là **đặc tả bắt buộc**, không phải gợi ý.

AI phải:

```text
- Tuân thủ palette.
- Tuân thủ layout.
- Dùng MathTex cho toán.
- Dùng Text cho tiếng Việt.
- Ưu tiên 2D hoặc pseudo-3D.
- Chỉ dùng real 3D khi cần.
- Dùng animation có mục đích.
- Dùng TransformMatchingTex cho biến đổi toán.
- Tránh object tràn frame.
- Tránh label chồng nhau.
- Giữ footer và thương hiệu.
- Tối ưu cho Google Colab.
- Pin dependency.
- Cache audio.
- Đo duration bằng ffprobe.
- Xuất video hoàn chỉnh.
- Kiểm tra lỗi trước khi kết thúc.
```

Nếu có nhiều cách triển khai, AI phải ưu tiên theo thứ tự:

```text
ổn định
→ dễ hiểu
→ dễ bảo trì
→ đẹp
→ phức tạp
```

Nếu một hiệu ứng đẹp nhưng có nguy cơ gây lỗi render, hãy chọn phương án đơn giản và ổn định hơn.

---

# TÓM TẮT STACK CHUẨN

```text
Nội dung toán
        ↓
Python lesson data
        ↓
Manim Community
        ↓
MathTex + LaTeX
        ↓
2D / pseudo-3D / selective 3D
        ↓
Edge TTS
        ↓
FFmpeg
        ↓
MP4 + SRT/VTT
        ↓
SCORM nếu cần
```

---

# CHUẨN THƯƠNG HIỆU CUỐI

```text
Thương hiệu:
Thầy Nguyễn Văn Sang

Phong cách:
Premium Dark Educational

Định hướng:
Modern
Clean
Mathematical
Professional
Non-distracting

Màu nền:
Deep Navy

Màu trọng tâm:
Sky Blue / Cyan / Gold

Mục tiêu cuối:
Một hệ thống video bài giảng Toán THPT có hình ảnh, animation và cách trình bày đồng nhất như một sản phẩm giáo dục chuyên nghiệp.
```

---

**END OF MANIM TEACHING SPEC**