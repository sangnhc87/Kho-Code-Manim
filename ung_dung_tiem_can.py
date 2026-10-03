import sys
import subprocess
from pathlib import Path

def run_command(command):
    subprocess.run(command, check=True)

print("BƯỚC 1/4: Cài thư viện và phông chữ...")

run_command(["apt-get", "update", "-qq"])
run_command([
    "apt-get", "install", "-y", "-qq",
    "ffmpeg",
    "pkg-config",
    "libcairo2-dev",
    "libpango1.0-dev",
    "fonts-dejavu-core",
    "fonts-noto-core",
    "texlive",
    "texlive-latex-extra",
    "texlive-fonts-extra",
    "texlive-latex-recommended",
    "texlive-science",
    "tipa"
])

run_command([
    sys.executable, "-m", "pip", "install", "-q",
    "manim==0.19.0",
    "edge-tts>=7.0.0,<8",
    "ipywidgets"
])

WORK = Path("/content/ung_dung_tiem_can")
WORK.mkdir(parents=True, exist_ok=True)
SCRIPT = WORK / "ung_dung_tiem_can.py"

SOURCE = r'''
from manim import *
import asyncio
import edge_tts
import json
import math
import subprocess
import sys
import textwrap
import numpy as np
from pathlib import Path

# ================================================================
# CẤU HÌNH
# ================================================================

try:
    BASE = Path(__file__).resolve().parent
except NameError:
    BASE = Path.cwd()
AUDIO_DIR = BASE / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = BASE / "timing.json"

VOICE = "vi-VN-NamMinhNeural"
VOICE_RATE = "-8%"
TARGET_SECONDS = 600.0

ENTER_TIME = 0.60
AFTER_AUDIO_TIME = 0.30
EXIT_TIME = 0.30

FONT = "DejaVu Sans"
BG = "#101828"
FG = "#F8FAFC"
MUTED = "#CBD5E1"
ACCENT = "#38BDF8"
GREEN = "#34D399"
YELLOW = "#FBBF24"
PINK = "#F9A8D4"

config.background_color = BG

SLIDES = [
    {
        "title": "BÀI TOÁN THỰC TẾ VỀ ĐƯỜNG TIỆM CẬN",
        "lines": [
            "TOÁN 12 • Ứng dụng thực tiễn của tiệm cận",
            "Mục tiêu 1. Hiểu ý nghĩa của tiệm cận ngang: trạng thái bão hòa.",
            "Mục tiêu 2. Phân tích chi phí trung bình và nồng độ dung dịch.",
            "Mục tiêu 3. Giải bài toán ngược tìm tham số $A, B$ từ thực tế.",
            "Mục tiêu 4. Ứng dụng tiệm cận xiên trong tối ưu hóa chi phí.",
            "Trọng tâm: Đọc hiểu mô hình và giới hạn khi thời gian $t \to +\infty$."
        ],
        "narration": (
            "Chào các em. Trong bài học trước, chúng ta đã biết cách tìm "
            "đường tiệm cận. Hôm nay, chúng ta sẽ xem các đường tiệm cận "
            "này mang ý nghĩa gì trong thực tế. Các mô hình bão hòa, sự "
            "thay đổi nồng độ, chi phí sản xuất, tất cả đều có thể được "
            "mô tả bằng giới hạn khi một đại lượng tiến ra vô cực. Các bài "
            "toán này rất hay gặp trong đề thi hiện nay. Chúng ta cùng "
            "khám phá nhé!"
        )
    },
    {
        "title": "1. MÔ HÌNH BÃO HÒA (LEARNING CURVE)",
        "lines": [
            "Số từ vựng tiếng Anh học được sau $t$ tháng:",
            "$N(t) = \frac{2000t}{t + 15}$.",
            "Khi $t = 0$ (bắt đầu): $N(0) = 0$ từ.",
            "Khi $t = 15$: $N(15) = \frac{2000 \cdot 15}{30} = 1000$ từ.",
            "Hỏi sau nhiều năm, số từ tối đa đạt được là bao nhiêu?",
            "Toán học: Tính $\lim_{t \to +\infty} N(t)$.",
            "$\lim_{t \to +\infty} N(t) = 2000$. Tiệm cận ngang: $N = 2000$.",
            "Ý nghĩa: Sức chứa của não/khóa học có giới hạn (bão hòa)."
        ],
        "graph": {
            "func": "learning",
            "intervals": [[0, 100]],
            "range": [0, 100, 0, 2500],
            "asymptotes": [
                ["h", 2000, "$N = 2000$ (Ngưỡng bão hòa)"]
            ],
            "x_step": 20,
            "y_step": 500,
            "caption": "Đồ thị tiệm cận dần về ngưỡng 2000"
        },
        "narration": (
            "Mô hình đầu tiên là đường cong học tập. Giả sử số từ vựng "
            "một học sinh học được sau t tháng được tính bằng công thức "
            "hai nghìn t chia cho t cộng mười lăm. Ban đầu t bằng không, "
            "học được không từ. Sau 15 tháng, được 1000 từ. Nếu học mãi "
            "mãi thì sao? Ta tính giới hạn của N khi t tiến ra dương vô "
            "cùng. Chia cả tử và mẫu cho t, giới hạn bằng hai nghìn. Đường "
            "N bằng hai nghìn là tiệm cận ngang. Trong thực tế, điều này "
            "thể hiện trạng thái bão hòa: năng lực ghi nhớ hoặc vốn từ "
            "của khóa học có giới hạn tối đa."
        )
    },
    {
        "title": "2. BÀI TOÁN CHI PHÍ SẢN XUẤT TRUNG BÌNH",
        "lines": [
            "Chi phí sản xuất $x$ sản phẩm: $C(x) = 100 + 5x$ (triệu đồng).",
            "Trong đó $100$ là chi phí cố định (máy móc), $5$ là chi phí vật tư.",
            "Chi phí TRUNG BÌNH cho mỗi sản phẩm:",
            "$c(x) = \frac{C(x)}{x} = \frac{100 + 5x}{x} = \frac{100}{x} + 5$.",
            "Khi sản xuất rất ít ($x \to 0^+$): $c(x) \to +\infty$ (TCĐ $x = 0$).",
            "Khi sản xuất số lượng lớn ($x \to +\infty$): $\frac{100}{x} \to 0$, $c(x) \to 5$.",
            "Tiệm cận ngang $y = 5$.",
            "Ý nghĩa: Sản xuất càng nhiều, chi phí cố định càng được chia đều."
        ],
        "graph": {
            "func": "avg_cost",
            "intervals": [[0.5, 50]],
            "range": [0, 50, 0, 25],
            "asymptotes": [
                ["h", 5, "$y = 5$ (Chi phí tối ưu)"]
            ],
            "x_step": 10,
            "y_step": 5,
            "caption": "Chi phí trung bình giảm dần về 5"
        },
        "narration": (
            "Ứng dụng thứ hai là trong kinh tế. Để sản xuất x sản phẩm, "
            "doanh nghiệp mất một trăm triệu tiền cố định mua máy móc, và "
            "năm triệu tiền vật tư cho mỗi sản phẩm. Chi phí tổng là một "
            "trăm cộng năm x. Chi phí trung bình cho mỗi sản phẩm là c x "
            "bằng chi phí tổng chia x, tức là một trăm chia x cộng năm. "
            "Nếu sản xuất ít, chi phí trung bình rất cao. Nhưng khi sản "
            "xuất hàng loạt, x tiến ra vô cực, phân thức một trăm chia "
            "x tiến về không, chi phí trung bình tiến về năm triệu. Đường "
            "y bằng năm là tiệm cận ngang. Sản xuất càng nhiều, chi phí "
            "trung bình càng sát mức năm triệu."
        )
    },
    {
        "title": "3. MÔ HÌNH NỒNG ĐỘ (PHA TRỘN LIÊN TỤC)",
        "lines": [
            "Bể chứa $100$ lít nước muối, có $20$ kg muối.",
            "Bơm vào bể liên tục: $5$ lít/phút, chứa $2$ kg muối/phút.",
            "Sau $t$ phút:",
            "- Lượng muối: $m(t) = 20 + 2t$.",
            "- Thể tích: $V(t) = 100 + 5t$.",
            "Nồng độ: $C(t) = \frac{m(t)}{V(t)} = \frac{20 + 2t}{100 + 5t}$.",
            "$\lim_{t \to +\infty} C(t) = \frac{2}{5} = 0.4$ (kg/lít).",
            "Tiệm cận ngang $C = 0.4$ bằng chính nồng độ của nước bơm vào."
        ],
        "graph": {
            "func": "concentration",
            "intervals": [[0, 200]],
            "range": [0, 200, 0.15, 0.45],
            "asymptotes": [
                ["h", 0.4, "$C = 0.4$ (Nồng độ bão hòa)"]
            ],
            "x_step": 40,
            "y_step": 0.05,
            "caption": "Nồng độ tăng dần nhưng không vượt 0.4"
        },
        "narration": (
            "Tiếp theo là bài toán hóa học. Một bể chứa 100 lít nước có 20 "
            "kg muối. Ta liên tục bơm thêm nước muối với tốc độ 5 lít mỗi "
            "phút, trong đó có 2 kg muối. Sau t phút, lượng muối là 20 "
            "cộng 2t, thể tích là 100 cộng 5t. Nồng độ là tỉ số của hai "
            "đại lượng này. Khi t rất lớn, tiệm cận ngang là tỉ số hệ số "
            "cao nhất, tức là hai phần năm, hay 0.4 kg trên lít. Thật thú "
            "vị, 0.4 chính là nồng độ của nước được bơm vào. Hồ nước ban "
            "đầu dù loãng hay đặc, sau thời gian dài sẽ bị đồng hóa bởi "
            "nguồn bơm."
        )
    },
    {
        "title": "4. BÀI TOÁN TÌM ẨN: NỒNG ĐỘ OXY",
        "lines": [
            "Nồng độ oxy trong hồ sau sự cố ô nhiễm: ",
            "$O(t) = \frac{At^2 + Bt + C}{t^2 + 1}$ ($t$ tính bằng tuần).",
            "Thực tế đo đạc:",
            "1. Lúc xảy ra sự cố ($t=0$): Nồng độ là $10$.",
            "2. Sau 1 tuần ($t=1$): Nồng độ giảm xuống $6$.",
            "3. Sau nhiều năm ($t \to +\infty$): Nồng độ ổn định ở $5$.",
            "Yêu cầu: Tìm $A, B, C$."
        ],
        "narration": (
            "Đây là một dạng bài toán lạ và rất hay: tìm ẩn số từ các quan "
            "sát thực tế. Nồng độ oxy trong một hồ nước bị ô nhiễm được "
            "mô tả bởi hàm bậc hai chia bậc hai có chứa các tham số A, "
            "B, C. Các nhà khoa học đo được ba dữ kiện: lúc mới xảy ra "
            "sự cố nồng độ là 10; sau một tuần giảm còn 6; và sau một thời "
            "gian rất dài, nồng độ tự ổn định ở mức 5. Dựa vào những số "
            "liệu này, chúng ta sẽ khôi phục lại công thức của hàm số."
        )
    },
    {
        "title": "GIẢI MÃ CÁC THAM SỐ A, B, C",
        "lines": [
            "Hàm số: $O(t) = \frac{At^2 + Bt + C}{t^2 + 1}$.",
            "Dữ kiện 3 ($t \to +\infty$): $\lim O(t) = \frac{A}{1} = A$.",
            "Trạng thái ổn định ở $5 \implies A = 5$. (Đây là tiệm cận ngang!)",
            "Dữ kiện 1 ($t=0$): $O(0) = \frac{C}{1} = C \implies C = 10$.",
            "Hàm trở thành: $O(t) = \frac{5t^2 + Bt + 10}{t^2 + 1}$.",
            "Dữ kiện 2 ($t=1$): $O(1) = \frac{5 + B + 10}{2} = 6$.",
            "$\implies 15 + B = 12 \implies B = -3$.",
            "Vậy $O(t) = \frac{5t^2 - 3t + 10}{t^2 + 1}$."
        ],
        "graph": {
            "func": "oxygen",
            "intervals": [[0, 20]],
            "range": [0, 20, 0, 12],
            "asymptotes": [
                ["h", 5, "$y = 5$ (Mức tự nhiên)"]
            ],
            "x_step": 4,
            "y_step": 2,
            "points": [[0, 10, "10"], [1, 6, "6"]],
            "caption": "Nồng độ tụt xuống rồi phục hồi về 5"
        },
        "narration": (
            "Cách giải rất gọn gàng. Dữ kiện thứ ba về sự ổn định khi t "
            "tiến ra vô cực chính là đường tiệm cận ngang. Giới hạn của "
            "hàm bằng hệ số A chia 1, tức là A. Do mức ổn định là 5, ta "
            "có ngay A bằng 5. Tại t bằng không, thay vào hàm được C "
            "bằng 10. Lúc này hàm có dạng 5 t bình cộng B t cộng 10, "
            "chia t bình cộng 1. Cuối cùng, tại t bằng 1, nồng độ bằng "
            "6. Giải phương trình ta tìm được B bằng âm 3. Như vậy, thông "
            "tin về tiệm cận giúp ta tìm hệ số bậc cao nhất một cách "
            "chính xác."
        )
    },
    {
        "title": "5. TIỆM CẬN XIÊN TRONG TỐI ƯU HÓA",
        "lines": [
            "Chi phí vận hành theo quy mô $x$: $C(x) = x + \frac{400}{x}$ (triệu đồng).",
            "$x = 10: C(10) = 10 + 40 = 50$.",
            "$x = 20: C(20) = 20 + 20 = 40$. (Tối ưu nhất!)",
            "Nhưng khi $x$ rất lớn ($x \to +\infty$): $\frac{400}{x} \to 0$.",
            "Lúc này $C(x) \approx x$.",
            "Ta có: $\lim_{x \to +\infty} [C(x) - x] = 0$.",
            "Đường thẳng $y = x$ là TIỆM CẬN XIÊN của đồ thị chi phí.",
            "Ý nghĩa: Chi phí thực tế dần tiệm cận mức chi phí tuyến tính."
        ],
        "graph": {
            "func": "inventory",
            "intervals": [[2, 60]],
            "range": [0, 60, 0, 80],
            "asymptotes": [
                ["s", 1, 0, "$y = x$ (Tiệm cận xiên)"]
            ],
            "x_step": 10,
            "y_step": 20,
            "points": [[20, 40, "Min"]],
            "caption": "Đồ thị chi phí $C(x) = x + 400/x$"
        },
        "narration": (
            "Mô hình cuối cùng dùng để khảo sát tiệm cận xiên. Giả sử chi "
            "phí vận hành theo quy mô x là C bằng x cộng 400 chia x. "
            "Càng tăng quy mô, phần 400 chia x càng giảm, nhưng phần x lại "
            "tăng. Khi x tiến ra vô cực, phân thức tiến về không, nên chi "
            "phí tổng xấp xỉ bằng x. Giới hạn của hiệu C trừ x bằng không, "
            "nên đường thẳng y bằng x là tiệm cận xiên. Trên thực tế, tiệm "
            "cận xiên cho ta biết xu hướng dài hạn: khi quy mô quá lớn, "
            "chi phí sẽ tăng tuyến tính, các lợi thế kinh tế nhờ quy mô "
            "bị triệt tiêu. Điểm cực tiểu nằm ở x bằng 20."
        )
    },
    {
        "title": "TỔNG KẾT VÀ TỰ LUYỆN",
        "lines": [
            "TỪ KHÓA QUAN TRỌNG:",
            "• Tiệm cận ngang ($t \to +\infty$): Sự bão hòa, trạng thái ổn định lâu dài.",
            "• Tiệm cận đứng ($x \to x_0$): Sự bùng nổ, quá tải hoặc vô hạn tại một điểm.",
            "• Tiệm cận xiên: Xu hướng phát triển tuyến tính trong dài hạn.",
            "Bài tập tự luyện:",
            "Một đàn cá có số lượng $P(t) = \frac{200t + 50}{t + 2}$.",
            "Hỏi sau nhiều năm, số lượng đàn cá ổn định ở mức nào?",
            "Cảm ơn các em! • Thầy Nguyễn Văn Sang"
        ],
        "narration": (
            "Bài học kết thúc tại đây. Nhớ rằng, khi đọc đề toán thực tế, "
            "những từ như 'sau thời gian dài', 'ổn định', 'bão hòa' thường "
            "ám chỉ việc tính giới hạn ở vô cực để tìm tiệm cận ngang. "
            "'Quá tải' hoặc 'tăng đột biến' thường liên quan đến tiệm cận "
            "đứng. Còn 'xu hướng dài hạn' có thể là tiệm cận xiên. "
            "Các em hãy giải bài tập tự luyện về đàn cá trên màn hình "
            "nhé. Cảm ơn các em đã theo dõi. Hẹn gặp lại trong các bài "
            "toán tiếp theo của thầy Nguyễn Văn Sang!"
        )
    }
]

# ================================================================
# TẠO GIỌNG ĐỌC VÀ CĂN THỜI LƯỢNG
# ================================================================

def audio_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path)
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())

def atempo_filter(speed):
    factors = []
    while speed > 2.0:
        factors.append(2.0)
        speed /= 2.0
    while speed < 0.5:
        factors.append(0.5)
        speed /= 0.5
    factors.append(speed)
    return ",".join(f"atempo={factor:.9f}" for factor in factors)

async def synthesize(text, destination):
    last_error = None
    for attempt in range(4):
        try:
            if destination.exists():
                destination.unlink()
            communicator = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate=VOICE_RATE
            )
            await communicator.save(str(destination))
            if not destination.exists() or destination.stat().st_size < 500:
                raise RuntimeError("Tệp âm thanh chưa hoàn chỉnh.")
            if audio_duration(destination) <= 0:
                raise RuntimeError("Thời lượng âm thanh không hợp lệ.")
            return
        except Exception as exc:
            last_error = exc
            print(f"Lỗi TTS lần {attempt + 1}: {exc}", flush=True)
            await asyncio.sleep(2 + attempt * 2)
    raise RuntimeError("Không tạo được giọng TTS.") from last_error

async def prepare_audio():
    original_lengths = []
    for index, slide in enumerate(SLIDES):
        mp3 = AUDIO_DIR / f"original_{index:02d}.mp3"
        cache_file = AUDIO_DIR / f"original_{index:02d}.txt"
        cache_key = VOICE + "\n" + VOICE_RATE + "\n" + slide["narration"]
        cached = mp3.exists() and cache_file.exists() and cache_file.read_text(encoding="utf-8") == cache_key
        if cached:
            try:
                cached = audio_duration(mp3) > 0
            except Exception:
                cached = False
        if not cached:
            print(f"Tạo giọng nam: trang {index + 1}/{len(SLIDES)}", flush=True)
            await synthesize(slide["narration"], mp3)
            cache_file.write_text(cache_key, encoding="utf-8")
        original_lengths.append(audio_duration(mp3))

    overhead = len(SLIDES) * (ENTER_TIME + AFTER_AUDIO_TIME + EXIT_TIME)
    target_audio = TARGET_SECONDS - overhead
    speed = sum(original_lengths) / target_audio

    lengths = []
    for index, original_length in enumerate(original_lengths):
        source = AUDIO_DIR / f"original_{index:02d}.mp3"
        destination = AUDIO_DIR / f"voice_{index:02d}.wav"
        desired_length = original_length / speed
        filters = atempo_filter(speed) + f",apad,atrim=duration={desired_length:.9f}"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(source),
            "-vn", "-af", filters, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
            str(destination)
        ], check=True)
        lengths.append(audio_duration(destination))

    TIMING_FILE.write_text(json.dumps({
        "durations": lengths,
        "speed_factor": speed
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Đã tạo xong âm thanh.", flush=True)

# ================================================================
# HÀM SỐ VÀ VẼ ĐỒ THỊ
# ================================================================

def evaluate_function(name, x):
    if name == "learning":
        return (2000.0 * x) / (x + 15.0)
    if name == "avg_cost":
        return (100.0 / x) + 5.0
    if name == "concentration":
        return (20.0 + 2.0 * x) / (100.0 + 5.0 * x)
    if name == "oxygen":
        return (5.0 * x**2 - 3.0 * x + 10.0) / (x**2 + 1.0)
    if name == "inventory":
        return x + 400.0 / x
    raise ValueError(f"Chưa khai báo hàm: {name}")

def line_rectangle_intersections(a, b, c, bounds):
    xmin, xmax, ymin, ymax = bounds
    eps = 1e-8
    candidates = []
    if abs(b) > eps:
        for x in (xmin, xmax):
            y = (c - a * x) / b
            if ymin - eps <= y <= ymax + eps:
                candidates.append((float(x), float(y)))
    if abs(a) > eps:
        for y in (ymin, ymax):
            x = (c - b * y) / a
            if xmin - eps <= x <= xmax + eps:
                candidates.append((float(x), float(y)))
    unique = []
    for point in candidates:
        if not any(math.hypot(point[0] - o[0], point[1] - o[1]) < eps for o in unique):
            unique.append(point)
    if len(unique) < 2: return None
    pairs = [(p, q) for index, p in enumerate(unique) for q in unique[index + 1:]]
    return max(pairs, key=lambda pair: (pair[0][0] - pair[1][0]) ** 2 + (pair[0][1] - pair[1][1]) ** 2)

def function_curves(axes, spec):
    xmin, xmax, ymin, ymax = spec["range"]
    curves = VGroup()
    for left, right in spec["intervals"]:
        left = max(left, xmin)
        right = min(right, xmax)
        if left >= right: continue
        xs = np.linspace(left, right, 1800)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            ys = evaluate_function(spec["func"], xs)
        valid = np.isfinite(ys) & (ys >= ymin) & (ys <= ymax)
        indices = np.flatnonzero(valid)
        if len(indices) < 2: continue
        breaks = np.where(np.diff(indices) > 1)[0] + 1
        runs = np.split(indices, breaks)
        for run in runs:
            if len(run) < 2: continue
            points = [axes.c2p(float(xs[i]), float(ys[i])) for i in run]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_stroke(color=GREEN, width=3.2)
            curves.add(curve)
    return curves

# ================================================================
# CHỮ VÀ BỐ CỤC
# ================================================================

def make_text(content, size=27, color=FG, max_width=None):
    if "$" not in content:
        item = Text(content, font=FONT, font_size=size, color=color, line_spacing=0.85)
    else:
        parts = content.split("$")
        items = []
        for i, part in enumerate(parts):
            if not part: continue
            if i % 2 == 0:
                items.append(Text(part, font=FONT, font_size=size, color=color))
            else:
                items.append(MathTex(part, font_size=size + 4, color=YELLOW))
        item = VGroup(*items).arrange(RIGHT, buff=0.1)
        if len(items) > 1:
            base_y = items[0].get_bottom()[1]
            for it in items[1:]:
                it.shift(UP * (base_y - it.get_bottom()[1] + 0.05))
    if max_width is not None and item.width > max_width:
        item.scale_to_fit_width(max_width)
    return item

def make_body(lines, has_graph):
    font_size = 26 if has_graph else 28
    max_width = 6.1 if has_graph else 12.75
    items = []
    for index, line in enumerate(lines):
        color = FG
        if index == 0: color = ACCENT
        if index == len(lines) - 1: color = GREEN
        items.append(make_text(line, size=font_size, color=color, max_width=max_width))
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.22 if has_graph else 0.25)
    if body.height > 5.50: body.scale_to_fit_height(5.50)
    body.to_edge(LEFT, buff=0.48)
    body.shift(UP * (2.57 - body.get_top()[1]))
    return body

def build_graph(spec):
    xmin, xmax, ymin, ymax = spec["range"]
    x_step = spec.get("x_step", 1)
    y_step = spec.get("y_step", 1)

    axes = Axes(
        x_range=[xmin, xmax, x_step],
        y_range=[ymin, ymax, y_step],
        x_length=5.25,
        y_length=4.60,
        axis_config={"color": "#AAB8CC", "stroke_width": 1.6, "include_ticks": True, "include_numbers": False, "tip_width": 0.11, "tip_height": 0.11}
    ).move_to([3.72, 0.0, 0])

    graph = VGroup()
    grid = VGroup()
    for x in np.arange(xmin, xmax + 0.001, x_step):
        grid.add(Line(axes.c2p(x, ymin), axes.c2p(x, ymax), color="#2A394E", stroke_width=0.7))
    for y in np.arange(ymin, ymax + 0.001, y_step):
        grid.add(Line(axes.c2p(xmin, y), axes.c2p(xmax, y), color="#2A394E", stroke_width=0.7))
    graph.add(grid, axes)

    tick_labels = VGroup()
    for x in np.arange(xmin, xmax + 0.001, x_step):
        if xmin < x < xmax:
            lbl = make_text(f"{x:g}", size=14, color=MUTED)
            lbl.next_to(axes.c2p(x, ymin), DOWN, buff=0.08)
            tick_labels.add(lbl)
    for y in np.arange(ymin, ymax + 0.001, y_step):
        if ymin < y < ymax:
            lbl = make_text(f"{y:g}", size=14, color=MUTED)
            lbl.next_to(axes.c2p(xmin, y), LEFT, buff=0.08)
            tick_labels.add(lbl)
    graph.add(tick_labels)

    legend_items = []
    for index, asymptote in enumerate(spec.get("asymptotes", [])):
        kind = asymptote[0]
        color = YELLOW if index % 2 == 0 else PINK
        if kind == "v":
            ends = line_rectangle_intersections(1, 0, asymptote[1], spec["range"])
        elif kind == "h":
            ends = line_rectangle_intersections(0, 1, asymptote[1], spec["range"])
        else:
            ends = line_rectangle_intersections(-asymptote[1], 1, asymptote[2], spec["range"])
        
        if ends is not None:
            p, q = ends
            graph.add(DashedLine(axes.c2p(*p), axes.c2p(*q), dash_length=0.12, dashed_ratio=0.57, stroke_width=2.8, color=color))
        legend_items.append(make_text(asymptote[-1], size=18, color=color))

    graph.add(function_curves(axes, spec))

    for x, y, label_content in spec.get("points", []):
        point = Dot(axes.c2p(x, y), radius=0.055, color=FG)
        label = make_text(label_content, size=18, color=FG).next_to(point, UR, buff=0.08)
        label.add_background_rectangle(color=BG, opacity=0.85, buff=0.035)
        graph.add(point, label)

    if legend_items:
        legend = VGroup(*legend_items).arrange(RIGHT, buff=0.38)
        if legend.width > 5.5: legend.scale_to_fit_width(5.5)
        legend.move_to([3.72, 2.67, 0])
        graph.add(legend)

    caption = make_text(spec.get("caption", ""), size=21, color=GREEN, max_width=5.65).move_to([3.68, -2.94, 0])
    graph.add(caption)
    return graph

# ================================================================
# SCENE CHÍNH
# ================================================================

class UngDungTiemCan(Scene):
    def construct(self):
        timing = json.loads(TIMING_FILE.read_text(encoding="utf-8"))
        durations = timing["durations"]

        footer_bg = Rectangle(width=config.frame_width, height=0.53, stroke_width=0, fill_color="#0A1020", fill_opacity=1).to_edge(DOWN, buff=0).set_z_index(100)
        footer_rule = Line([-config.frame_width / 2, -3.47, 0], [config.frame_width / 2, -3.47, 0], stroke_width=1.5, color=ACCENT).set_z_index(101)
        footer_name = make_text("Thầy Nguyễn Văn Sang", size=22, color=FG).move_to([0, -3.75, 0]).set_z_index(102)
        footer_subject = make_text("TOÁN 12 • ỨNG DỤNG TIỆM CẬN", size=14, color=MUTED).to_edge(LEFT, buff=0.30).set_y(-3.75).set_z_index(102)
        self.add(footer_bg, footer_rule, footer_name, footer_subject)

        for index, slide in enumerate(SLIDES):
            title = make_text(slide["title"], size=32, color=ACCENT, max_width=12.8).move_to([0, 3.34, 0])
            header_rule = Line([-6.65, 2.92, 0], [6.65, 2.92, 0], stroke_width=1.2, color="#3A4B64")
            counter = make_text(f"{index + 1:02d} / {len(SLIDES):02d}", size=17, color=MUTED).to_edge(RIGHT, buff=0.32).set_y(-3.75).set_z_index(103)
            
            has_graph = "graph" in slide
            body = make_body(slide["lines"], has_graph)
            content = VGroup(title, header_rule, body)

            if has_graph:
                divider = Line([0.05, -2.70, 0], [0.05, 2.60, 0], stroke_width=1, color="#304056")
                content.add(divider, build_graph(slide["graph"]))

            self.add(counter)
            self.play(FadeIn(content, shift=UP * 0.08), run_time=ENTER_TIME)

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            self.add_sound(str(audio_path))

            start, end = LEFT * 6.60 + DOWN * 3.25, RIGHT * 6.60 + DOWN * 3.25
            track = Line(start, end, color="#26364A", stroke_width=3)
            progress = Line(start, end, color=ACCENT, stroke_width=3)
            self.add(track)
            self.play(Create(progress), run_time=durations[index], rate_func=linear)
            self.wait(AFTER_AUDIO_TIME)
            self.play(FadeOut(content, shift=UP * 0.05), FadeOut(track), FadeOut(progress), FadeOut(counter), run_time=EXIT_TIME)

if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
    else:
        pass
'''

SCRIPT.write_text(SOURCE, encoding="utf-8")
compile(SOURCE, str(SCRIPT), "exec")

print("\nBƯỚC 2/4: Tạo giọng nam và căn thời lượng...")
run_command([sys.executable, str(SCRIPT), "--prepare"])

print("\nBƯỚC 3/4: Dựng video Manim 720p...")
MEDIA_DIR = WORK / "media"
run_command([
    sys.executable, "-m", "manim",
    "-qm", "--fps", "24", "--disable_caching",
    "--media_dir", str(MEDIA_DIR),
    "-o", "Ung_Dung_Tiem_Can_Thay_Nguyen_Van_Sang",
    str(SCRIPT), "UngDungTiemCan"
])

candidates = [p for p in MEDIA_DIR.rglob("Ung_Dung_Tiem_Can_Thay_Nguyen_Van_Sang.mp4") if "partial_movie_files" not in str(p)]
VIDEO_PATH = max(candidates, key=lambda p: p.stat().st_mtime)

print(f"\nBƯỚC 4/4: HOÀN TẤT! Video tại: {VIDEO_PATH}")

from IPython.display import display
import ipywidgets as widgets
from google.colab import files

video_button = widgets.Button(description="Tải video MP4", button_style="success", layout=widgets.Layout(width="190px"))
source_button = widgets.Button(description="Tải mã nguồn .py", button_style="info", layout=widgets.Layout(width="190px"))
video_button.on_click(lambda _: files.download(str(VIDEO_PATH)))
source_button.on_click(lambda _: files.download(str(SCRIPT)))
display(widgets.HBox([video_button, source_button]))
print("\nĐang gửi yêu cầu tải video...")
files.download(str(VIDEO_PATH))
