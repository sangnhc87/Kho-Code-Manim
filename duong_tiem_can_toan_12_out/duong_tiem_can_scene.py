
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

def probe_duration(path):
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
    val = float(result.stdout.strip())
    if not math.isfinite(val) or val <= 0:
        raise RuntimeError(f"Tệp âm thanh không hợp lệ: {path}")
    return val


HERE = Path(__file__).resolve().parent
AUDIO_DIR = HERE / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = HERE / "timing.json"

TEN_THAY   = "Thầy Nguyễn Văn Sang"
VOICE      = "vi-VN-NamMinhNeural"
VOICE_RATE = "-5%"

ENTER_TIME       = 0.55
AFTER_AUDIO_TIME = 0.30
EXIT_TIME        = 0.30

FONT   = "DejaVu Sans"
BG     = "#0b1120"
PANEL  = "#0e1d34"
FG     = "#EDF4FF"
INK    = "#EDF4FF"
MUTED  = "#7A9ABF"
ACCENT = "#38BDF8"
CYAN   = "#3ADEC8"
GREEN  = "#4ADE80"
YELLOW = "#FBBF24"
GOLD   = "#FFD700"
RED    = "#FF6B6B"
PINK   = "#F472B6"

config.background_color = BG

# ================================================================
# TEMPLATE LATEX CHUẨN
# ================================================================
TMPL = TexTemplate()
TMPL.add_to_preamble(r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{bm}
""")

# ================================================================
# DỮ LIỆU BÀI HỌC (100% CÔNG THỨC TOÁN Ở DẠNG LATEX $...$)
# ================================================================
SLIDES = [
    {
        "title": "ĐƯỜNG TIỆM CẬN CỦA ĐỒ THỊ HÀM SỐ",
        "lines": [
            r"TOÁN 12 • Từ giới hạn đến hình dạng đồ thị",
            r"Mục tiêu 1. Nhận biết tiệm cận đứng, tiệm cận ngang và tiệm cận xiên.",
            r"Mục tiêu 2. Dùng phép tính giới hạn để xác định các đường tiệm cận.",
            r"Mục tiêu 3. Vận dụng thành thạo với hàm phân thức và hàm chứa căn.",
            r"Mục tiêu 4. Giải quyết các bài toán tổng hợp và bài toán chứa tham số $m$.",
            r"Chuẩn bị: Kiến thức về giới hạn, phép chia đa thức và giấy nháp."
        ],
        "narration": (
            "Chào các em. Hôm nay chúng ta cùng tìm hiểu bài học: Đường tiệm cận "
            "của đồ thị hàm số, một nội dung trọng tâm của giải tích lớp mười hai. "
            "Bài học gồm bốn mục tiêu: nhận biết ba loại tiệm cận; dùng giới hạn "
            "để xác định chúng; vận dụng với hàm phân thức và hàm chứa căn; "
            "và cuối cùng là giải các bài toán tham số thường gặp trong đề thi. "
            "Các em hãy chuẩn bị giấy nháp, lắng nghe và tự thực hành từng ví dụ."
        )
    },
    {
        "title": "1. KHỞI ĐỘNG: QUAN SÁT ĐỒ THỊ",
        "lines": [
            r"Xét hàm số $y = \frac{1}{x}$ với tập xác định $D = \mathbb{R} \setminus \{0\}$.",
            r"Khi $x \to 0^+ \implies \frac{1}{x} \to +\infty$.",
            r"Khi $x \to 0^- \implies \frac{1}{x} \to -\infty$.",
            r"Đồ thị tiến sát đường thẳng $x = 0$ (trục tung $Oy$).",
            r"Khi $x \to \pm\infty \implies \frac{1}{x} \to 0$.",
            r"Đồ thị tiến sát đường thẳng $y = 0$ (trục hoành $Ox$).",
            r"$\boxed{x = 0}$ là tiệm cận đứng; $\boxed{y = 0}$ là tiệm cận ngang."
        ],
        "graph": {
            "func": "inverse",
            "intervals": [[-6, -0.025], [0.025, 6]],
            "range": [-6, 6, -5, 5],
            "asymptotes": [
                ["v", 0, r"$x = 0$"],
                ["h", 0, r"$y = 0$"]
            ],
            "caption": r"$y = \frac{1}{x}$: Hai trục toạ độ là hai đường tiệm cận"
        },
        "narration": (
            "Ta bắt đầu quan sát đồ thị hàm số y bằng một chia x. Khi x tiến "
            "về không từ bên phải, giá trị hàm số tăng lên dương vô cùng. Khi "
            "x tiến về không từ bên trái, giá trị hàm số giảm xuống âm vô cùng. "
            "Hai nhánh đồ thị tiến sát vào trục tung. Khi x tiến ra dương hoặc "
            "âm vô cùng, một chia x tiến dần về không, đồ thị tiến sát trục hoành. "
            "Đường thẳng x bằng không là tiệm cận đứng, và y bằng không là tiệm "
            "cận ngang."
        )
    },
    {
        "title": "2. ĐỊNH NGHĨA TIỆM CẬN ĐỨNG",
        "lines": [
            r"Đường thẳng $x = x_0$ là tiệm cận đứng của đồ thị hàm số $y = f(x)$ nếu:",
            r"Ít nhất một trong các điều kiện giới hạn một phía sau được thoả mãn:",
            r"$\lim_{x \to x_0^+} f(x) = +\infty$ \quad \text{hoặc} \quad $\lim_{x \to x_0^+} f(x) = -\infty$",
            r"$\lim_{x \to x_0^-} f(x) = +\infty$ \quad \text{hoặc} \quad $\lim_{x \to x_0^-} f(x) = -\infty$",
            r"Trọng tâm: Chỉ cần ÍT NHẤT MỘT PHÍA có giới hạn vô cực ($\pm\infty$).",
            r"Phương trình tiệm cận đứng luôn có dạng $\boxed{x = C}$ (với $C$ là hằng số)."
        ],
        "narration": (
            "Định nghĩa: Đường thẳng x bằng x không là tiệm cận đứng nếu có ít "
            "nhất một giới hạn một phía của hàm số, khi x tiến về x không, bằng "
            "dương vô cùng hoặc âm vô cùng. Các em đặc biệt chú ý: không bắt "
            "buộc cả hai phía đều phải có giới hạn vô cực, chỉ cần một phía là "
            "đủ điều kiện. Phương trình của tiệm cận đứng luôn có dạng x bằng "
            "hằng số."
        )
    },
    {
        "title": "VÍ DỤ 1: TÌM TIỆM CẬN ĐỨNG",
        "lines": [
            r"Tìm tiệm cận đứng của hàm số $f(x) = \frac{2x + 1}{x - 1}$.",
            r"Tập xác định: $D = \mathbb{R} \setminus \{1\}$.",
            r"Biến đổi phân thức: $f(x) = 2 + \frac{3}{x - 1}$.",
            r"Khi $x \to 1^+ \implies x - 1 \to 0^+ \implies \lim_{x \to 1^+} f(x) = +\infty$.",
            r"Khi $x \to 1^- \implies x - 1 \to 0^- \implies \lim_{x \to 1^-} f(x) = -\infty$.",
            r"Kết luận: Đường thẳng $\boxed{x = 1}$ là tiệm cận đứng của đồ thị."
        ],
        "graph": {
            "func": "rational_21",
            "intervals": [[-6, 0.98], [1.02, 7]],
            "range": [-6, 7, -5, 8],
            "asymptotes": [["v", 1, r"$x = 1$"]],
            "caption": r"$f(x) = \frac{2x+1}{x-1} = 2 + \frac{3}{x-1}$"
        },
        "narration": (
            "Xét hàm số f x bằng hai x cộng một chia x trừ một. Tập xác định "
            "loại trừ điểm x bằng một. Ta tách phân thức thành hai cộng ba "
            "chia x trừ một. Khi x tiến về một từ bên phải, mẫu số dương và "
            "tiến về không, khiến giá trị hàm tiến tới dương vô cùng. Tương "
            "tự từ bên trái, giá trị hàm tiến tới âm vô cùng. Vì vậy đường "
            "thẳng x bằng một là tiệm cận đứng."
        )
    },
    {
        "title": "VÍ DỤ 2: CHỈ CẦN GIỚI HẠN MỘT PHÍA",
        "lines": [
            r"Xét hàm số $f(x) = \frac{1}{\sqrt{x}}$.",
            r"Tập xác định: $D = (0; +\infty)$ (đồ thị không tồn tại khi $x \le 0$).",
            r"Xét giới hạn bên phải tại điểm biên $x = 0$:",
            r"$\lim_{x \to 0^+} \sqrt{x} = 0^+ \implies \lim_{x \to 0^+} \frac{1}{\sqrt{x}} = +\infty$.",
            r"Kết luận: $\boxed{x = 0}$ là tiệm cận đứng của đồ thị.",
            r"Lưu ý: Không xét giới hạn bên trái vì hàm không xác định tại đó.",
            r"Ngoài ra: $\lim_{x \to +\infty} \frac{1}{\sqrt{x}} = 0 \implies \boxed{y = 0}$ là tiệm cận ngang."
        ],
        "graph": {
            "func": "inverse_sqrt",
            "intervals": [[0.02, 8]],
            "range": [-2, 8, -1, 6],
            "asymptotes": [
                ["v", 0, r"$x = 0$"],
                ["h", 0, r"$y = 0$"]
            ],
            "caption": r"Chỉ xét giới hạn một phía thuộc $D = (0; +\infty)$"
        },
        "narration": (
            "Xét ví dụ hai với hàm số một chia căn bậc hai của x. Vì biểu thức "
            "dưới căn ở mẫu, tập xác định là x lớn hơn không. Khi x tiến về "
            "không từ bên phải, căn x tiến về không dương, hàm số tiến ra "
            "dương vô cùng. Do đó x bằng không là tiệm cận đứng. Ta không cần "
            "và cũng không thể xét giới hạn bên trái vì hàm không xác định "
            "khi x nhỏ hơn hoặc bằng không."
        )
    },
    {
        "title": "CẢNH BÁO: MẪU BẰNG 0 CHƯA ĐỦ!",
        "lines": [
            r"Xét hàm số $f(x) = \frac{x^2 - 1}{x - 1}$ trên tập $D = \mathbb{R} \setminus \{1\}$.",
            r"Phân tích tử thức: $x^2 - 1 = (x - 1)(x + 1)$.",
            r"Với mọi $x \neq 1 \implies f(x) = x + 1$.",
            r"Tính giới hạn: $\lim_{x \to 1} f(x) = \lim_{x \to 1} (x + 1) = 2$ (hữu hạn).",
            r"Do giới hạn hữu hạn, đường thẳng $x = 1$ KHÔNG PHẢI là tiệm cận đứng!",
            r"Đồ thị thực chất là đường thẳng $y = x + 1$ bị đục bỏ điểm $M(1; 2)$.",
            r"Nguyên tắc: Nghiệm của mẫu phải làm tử thức khác $0$ mới tạo tiệm cận đứng."
        ],
        "narration": (
            "Một sai lầm rất phổ biến là cứ thấy mẫu số bằng không thì vội "
            "kết luận ngay là tiệm cận đứng. Hãy quan sát hàm x bình trừ một "
            "chia x trừ một. Rút gọn tử và mẫu cho x trừ một, ta được hàm x "
            "cộng một. Giới hạn khi x tiến về một bằng hai, là một số hữu hạn, "
            "không phải vô cực. Vì vậy đồ thị không hề có tiệm cận đứng mà chỉ "
            "bị khuyết một điểm tại toạ độ một, hai."
        )
    },
    {
        "title": "3. ĐỊNH NGHĨA TIỆM CẬN NGANG",
        "lines": [
            r"Đường thẳng $y = L$ là tiệm cận ngang của đồ thị hàm số $y = f(x)$ nếu:",
            r"$\lim_{x \to +\infty} f(x) = L$ \quad \text{hoặc} \quad $\lim_{x \to -\infty} f(x) = L$",
            r"Trong đó $L$ bắt buộc phải là một số thực hữu hạn ($L \in \mathbb{R}$).",
            r"Cần khảo sát độc lập hai hướng: $x \to +\infty$ và $x \to -\infty$.",
            r"Hai hướng vô cực có thể cho cùng một hoặc hai tiệm cận ngang khác nhau.",
            r"Đồ thị của một hàm số có TỐI ĐA hai đường tiệm cận ngang $\boxed{y = L}$."
        ],
        "narration": (
            "Định nghĩa tiệm cận ngang: Đường thẳng y bằng L là tiệm cận ngang "
            "nếu giới hạn của f x khi x tiến ra dương vô cùng hoặc âm vô cùng "
            "bằng một số thực hữu hạn L. Các em cần tính riêng biệt hai hướng "
            "tiến ra vô cực. Một hàm số có thể không có tiệm cận ngang, có một "
            "đường, hoặc tối đa là hai đường tiệm cận ngang khác nhau."
        )
    },
    {
        "title": "VÍ DỤ 3: TÌM ĐỦ ĐỨNG VÀ NGANG",
        "lines": [
            r"Xét lại hàm số $f(x) = \frac{2x + 1}{x - 1}$ trên $D = \mathbb{R} \setminus \{1\}$.",
            r"Ta đã tìm được tiệm cận đứng: $\boxed{x = 1}$.",
            r"Tìm tiệm cận ngang bằng cách chia tử và mẫu cho $x$ ($x \neq 0$):",
            r"$f(x) = \frac{2 + 1/x}{1 - 1/x} \implies \lim_{x \to \pm\infty} f(x) = \frac{2 + 0}{1 - 0} = 2$.",
            r"Suy ra đường thẳng $\boxed{y = 2}$ là tiệm cận ngang.",
            r"Kết luận: Đồ thị hàm số có 2 đường tiệm cận là $\boxed{x = 1}$ và $\boxed{y = 2}$."
        ],
        "graph": {
            "func": "rational_21",
            "intervals": [[-6, 0.98], [1.02, 7]],
            "range": [-6, 7, -5, 8],
            "asymptotes": [
                ["v", 1, r"$x = 1$"],
                ["h", 2, r"$y = 2$"]
            ],
            "caption": r"Tiệm cận đứng $x = 1$; tiệm cận ngang $y = 2$"
        },
        "narration": (
            "Trở lại với hàm số hai x cộng một chia x trừ một. Chúng ta đã có "
            "tiệm cận đứng x bằng một. Để tìm tiệm cận ngang, ta chia cả tử "
            "và mẫu cho x. Khi x tiến ra vô cùng, một chia x triệt tiêu về "
            "không, giới hạn đạt giá trị bằng hai. Do đó, đường thẳng y bằng "
            "hai là tiệm cận ngang duy nhất của đồ thị."
        )
    },
    {
        "title": "MẸO NHANH CHO HÀM PHÂN THỨC HỮU TỈ",
        "lines": [
            r"Xét hàm phân thức $f(x) = \frac{P(x)}{Q(x)}$ với bậc tử $n = \deg P$, bậc mẫu $m = \deg Q$:",
            r"• Nếu $n < m \implies$ Tiệm cận ngang luôn là trục hoành $\boxed{y = 0}$.",
            r"• Nếu $n = m \implies \boxed{y = \frac{a_n}{b_m}}$ (tỉ số hai hệ số của luỹ thừa cao nhất).",
            r"  Ví dụ: $f(x) = \frac{3x^2 - 1}{2x^2 + x + 1} \implies \text{TCN: } \boxed{y = \frac{3}{2}}$.",
            r"• Nếu $n > m \implies$ Không có tiệm cận ngang.",
            r"• Đặc biệt khi $n = m + 1 \implies$ Chia đa thức tìm tiệm cận xiên $\boxed{y = ax + b}$."
        ],
        "narration": (
            "Đối với hàm phân thức hữu tỉ, ta có quy tắc xét nhanh theo bậc. "
            "Nếu bậc của tử bé hơn bậc của mẫu, tiệm cận ngang luôn là y "
            "bằng không. Nếu bậc của tử bằng bậc của mẫu, tiệm cận ngang bằng "
            "tỉ số của hai hệ số bậc cao nhất. Nếu bậc tử lớn hơn bậc mẫu, "
            "đồ thị không có tiệm cận ngang; và khi bậc tử hơn bậc mẫu đúng "
            "một bậc, đồ thị sẽ có tiệm cận xiên."
        )
    },
    {
        "title": "VÍ DỤ 4: HAI TIỆM CẬN NGANG KHÁC NHAU",
        "lines": [
            r"Tìm các tiệm cận của hàm số $f(x) = \frac{x}{\sqrt{x^2 + 1}}$ ($D = \mathbb{R}$).",
            r"Lưu ý phép rút căn: $\sqrt{x^2} = |x|$.",
            r"Khi $x \to +\infty \implies |x| = x \implies \lim_{x \to +\infty} \frac{x}{x\sqrt{1 + 1/x^2}} = 1 \implies \boxed{y = 1}$.",
            r"Khi $x \to -\infty \implies |x| = -x \implies \lim_{x \to -\infty} \frac{x}{-x\sqrt{1 + 1/x^2}} = -1 \implies \boxed{y = -1}$.",
            r"Đồ thị có HAI tiệm cận ngang phân biệt: $\boxed{y = 1}$ và $\boxed{y = -1}$.",
            r"Do mẫu số $\sqrt{x^2 + 1} \ge 1 > 0$ nên đồ thị không có tiệm cận đứng."
        ],
        "graph": {
            "func": "two_horizontal",
            "intervals": [[-7, 7]],
            "range": [-7, 7, -3, 3],
            "asymptotes": [
                ["h", 1, r"$y = 1$"],
                ["h", -1, r"$y = -1$"]
            ],
            "caption": r"Hai hướng vô cực sinh ra hai TCN: $y = \pm 1$"
        },
        "narration": (
            "Xét hàm số x chia căn bậc hai của x bình phương cộng một. Hàm "
            "này xác định trên toàn bộ tập số thực. Khi đưa x bình ra ngoài "
            "căn, bắt buộc phải lấy giá trị tuyệt đối của x. Khi x dương vô "
            "cùng, tỉ số bằng một, cho tiệm cận y bằng một. Khi x âm vô cùng, "
            "tỉ số bằng âm một, cho tiệm cận y bằng âm một. Như vậy đồ thị "
            "có hai tiệm cận ngang khác nhau."
        )
    },
    {
        "title": "4. ĐỊNH NGHĨA TIỆM CẬN XIÊN",
        "lines": [
            r"Đường thẳng $y = ax + b$ ($a \neq 0$) là tiệm cận xiên của đồ thị $y = f(x)$ nếu:",
            r"$\lim_{x \to +\infty} [f(x) - (ax + b)] = 0$ \quad \text{hoặc} \quad $\lim_{x \to -\infty} [f(x) - (ax + b)] = 0$",
            r"Ý nghĩa hình học: Khoảng cách giữa đồ thị và đường thẳng tiến về $0$ khi $x \to \infty$.",
            r"Công thức tính tổng quát tìm các hệ số $a$ và $b$:",
            r"$a = \lim_{x \to \pm\infty} \frac{f(x)}{x}$ \quad \text{và} \quad $b = \lim_{x \to \pm\infty} [f(x) - ax]$",
            r"Điều kiện cần: Các giới hạn $a, b$ phải là các số hữu hạn và $a \neq 0$."
        ],
        "narration": (
            "Khái niệm tiệm cận xiên: Đường thẳng y bằng a x cộng b, với a khác "
            "không, là tiệm cận xiên nếu hiệu giữa hàm số và đường thẳng tiến "
            "về không khi x tiến ra vô cực. Về mặt hình học, nhánh đồ thị "
            "càng ngày càng nép sát vào đường thẳng xiên đó. Ta có công thức "
            "tính hai hệ số a và b như trên màn hình."
        )
    },
    {
        "title": "VÍ DỤ 5: TIỆM CẬN XIÊN CƠ BẢN",
        "lines": [
            r"Xét hàm số $f(x) = \frac{x^2 + 1}{x} = x + \frac{1}{x}$ với tập xác định $x \neq 0$.",
            r"Xét hiệu số: $f(x) - x = \frac{1}{x}$.",
            r"Khi $x \to \pm\infty \implies \lim_{x \to \pm\infty} [f(x) - x] = \lim_{x \to \pm\infty} \frac{1}{x} = 0$.",
            r"Suy ra đường thẳng $\boxed{y = x}$ là tiệm cận xiên của đồ thị.",
            r"Tại điểm $x = 0: \lim_{x \to 0^\pm} f(x) = \pm\infty \implies \boxed{x = 0}$ là tiệm cận đứng.",
            r"Hàm số không có tiệm cận ngang do bậc tử lớn hơn bậc mẫu."
        ],
        "graph": {
            "func": "slant_simple",
            "intervals": [[-6, -0.025], [0.025, 6]],
            "range": [-6, 6, -7, 7],
            "asymptotes": [
                ["v", 0, r"$x = 0$"],
                ["s", 1, 0, r"$y = x$"]
            ],
            "caption": r"$f(x) = x + \frac{1}{x}$: TCX $y = x$, TCĐ $x = 0$"
        },
        "narration": (
            "Xét hàm số x bình phương cộng một chia x. Ta tách biểu thức thành "
            "x cộng một chia x. Hiệu giữa hàm số và đường thẳng y bằng x chính "
            "là một chia x, biểu thức này tiến về không khi x ra vô cùng. Do "
            "đó, y bằng x là tiệm cận xiên. Đồng thời tại x bằng không, hàm "
            "có giới hạn vô cực nên x bằng không là tiệm cận đứng."
        )
    },
    {
        "title": "VÍ DỤ 6: CHIA ĐA THỨC TÌM TIỆM CẬN XIÊN",
        "lines": [
            r"Tìm các tiệm cận của hàm số $f(x) = \frac{x^2 + 2x + 2}{x + 1}$ ($x \neq -1$).",
            r"Phép chia đa thức: $x^2 + 2x + 2 = (x + 1)(x + 1) + 1$.",
            r"Viết lại hàm số: $f(x) = x + 1 + \frac{1}{x + 1}$.",
            r"Khi $x \to \pm\infty \implies \lim_{x \to \pm\infty} [f(x) - (x + 1)] = \lim_{x \to \pm\infty} \frac{1}{x + 1} = 0$.",
            r"$\implies$ Tiệm cận xiên là $\boxed{y = x + 1}$.",
            r"Khi $x \to -1^\pm \implies \lim_{x \to -1^\pm} f(x) = \pm\infty \implies$ Tiệm cận đứng $\boxed{x = -1}$."
        ],
        "graph": {
            "func": "slant_shift",
            "intervals": [[-7, -1.025], [-0.975, 6]],
            "range": [-7, 6, -7, 7],
            "asymptotes": [
                ["v", -1, r"$x = -1$"],
                ["s", 1, 1, r"$y = x + 1$"]
            ],
            "caption": r"Thương bậc nhất $x + 1$ là tiệm cận xiên"
        },
        "narration": (
            "Xét hàm phân thức có bậc tử là hai và bậc mẫu là một. Thực hiện "
            "phép chia đa thức, ta được thương là x cộng một và số dư là một. "
            "Phần dư chia cho mẫu sẽ tiến dần về không khi x ra vô cùng. Do "
            "đó phần thương x cộng một chính là phương trình đường tiệm cận "
            "xiên. Điểm làm mẫu bằng không cho ta tiệm cận đứng x bằng âm một."
        )
    },
    {
        "title": "HIỂU ĐÚNG: ĐỒ THỊ CÓ THỂ CẮT TIỆM CẬN",
        "lines": [
            r"Khảo sát hàm số $f(x) = \frac{x}{x^2 + 1}$ xác định trên toàn bộ $\mathbb{R}$.",
            r"Khi $x \to \pm\infty \implies \lim_{x \to \pm\infty} f(x) = 0 \implies \boxed{y = 0}$ (trục $Ox$) là TCN.",
            r"Tuy nhiên, tại điểm $x = 0 \implies f(0) = 0$.",
            r"Đồ thị CẮT đường tiệm cận ngang ngay tại gốc toạ độ $O(0; 0)$!",
            r"Ý nghĩa bản chất: Khái niệm tiệm cận chỉ mô tả xu hướng ở xa vô tận ($x \to \pm\infty$),",
            r"hoàn toàn KHÔNG cấm đồ thị cắt tiệm cận tại các toạ độ hữu hạn.",
            r"Tránh ghi nhớ sai lầm: “Đồ thị tiến sát nhưng không bao giờ cắt tiệm cận”."
        ],
        "graph": {
            "func": "cross_horizontal",
            "intervals": [[-7, 7]],
            "range": [-7, 7, -2, 2],
            "asymptotes": [["h", 0, r"$y = 0$"]],
            "points": [[0, 0, r"$O(0; 0)$"]],
            "caption": r"Đồ thị cắt tiệm cận ngang $y = 0$ tại $O(0; 0)$"
        },
        "narration": (
            "Nhiều bạn vẫn giữ ngộ nhận là đồ thị không bao giờ được phép cắt "
            "tiệm cận. Điều này chỉ đúng với tiệm cận đứng, nhưng hoàn toàn sai "
            "với tiệm cận ngang và tiệm cận xiên. Ví dụ hàm x chia x bình "
            "cộng một có tiệm cận ngang y bằng không, nhưng đồ thị cắt đúng "
            "đường tiệm cận này tại gốc toạ độ O. Định nghĩa tiệm cận chỉ miêu "
            "tả xu thế ở vô cực mà thôi."
        )
    },
    {
        "title": "BÀI TẬP 1: ĐỒ THỊ CÓ HAI TIỆM CẬN ĐỨNG",
        "lines": [
            r"Tìm tất cả các đường tiệm cận của hàm số $f(x) = \frac{1}{x^2 - 4}$.",
            r"Tập xác định: $D = \mathbb{R} \setminus \{-2; 2\}$ vì $x^2 - 4 = (x - 2)(x + 2)$.",
            r"Tại $x = 2: \lim_{x \to 2^+} f(x) = +\infty, \lim_{x \to 2^-} f(x) = -\infty \implies \boxed{x = 2}$ là TCĐ.",
            r"Tại $x = -2: \lim_{x \to -2^+} f(x) = -\infty, \lim_{x \to -2^-} f(x) = +\infty \implies \boxed{x = -2}$ là TCĐ.",
            r"Khi $x \to \pm\infty \implies \lim_{x \to \pm\infty} f(x) = 0 \implies \boxed{y = 0}$ là tiệm cận ngang.",
            r"Kết luận: Đồ thị hàm số có 3 đường tiệm cận: $\boxed{x = -2}$, $\boxed{x = 2}$ và $\boxed{y = 0}$."
        ],
        "narration": (
            "Bài tập một: Tìm tiệm cận của một chia x bình trừ bốn. Mẫu số "
            "có hai nghiệm là hai và âm hai, không nghiệm nào làm triệt tiêu "
            "tử số. Do đó tại cả hai điểm này hàm đều có giới hạn vô cực, cho "
            "ta hai tiệm cận đứng x bằng hai và x bằng âm hai. Bậc tử bé hơn "
            "bậc mẫu cho thêm tiệm cận ngang y bằng không. Tổng cộng có ba "
            "đường tiệm cận."
        )
    },
    {
        "title": "BÀI TẬP 2: RÚT GỌN VÀ GIỮ TẬP XÁC ĐỊNH",
        "lines": [
            r"Tìm các tiệm cận của hàm số $f(x) = \frac{x^2 - 4}{x^2 - x - 2}$.",
            r"Phân tích mẫu: $x^2 - x - 2 = (x - 2)(x + 1) \implies D = \mathbb{R} \setminus \{-1; 2\}$.",
            r"Phân tích tử: $x^2 - 4 = (x - 2)(x + 2)$.",
            r"Rút gọn với mọi $x \in D \implies f(x) = \frac{x + 2}{x + 1}$.",
            r"Tại $x = 2: \lim_{x \to 2} f(x) = \frac{4}{3}$ (hữu hạn) $\implies x = 2$ KHÔNG PHẢI là TCĐ.",
            r"Tại $x = -1: \lim_{x \to -1^+} f(x) = +\infty \implies \boxed{x = -1}$ là TCĐ duy nhất.",
            r"Khi $x \to \pm\infty \implies \lim_{x \to \pm\infty} f(x) = 1 \implies \boxed{y = 1}$ là TCN."
        ],
        "narration": (
            "Bài tập hai là bài toán bẫy rất hay gặp. Mẫu số có hai nghiệm là "
            "hai và âm một. Nhưng tại x bằng hai, cả tử và mẫu đều bằng không. "
            "Sau khi rút gọn biểu thức, giới hạn tại hai bằng bốn phần ba là "
            "số hữu hạn, nên x bằng hai không phải tiệm cận đứng. Chỉ có x "
            "bằng âm một là tiệm cận đứng và y bằng một là tiệm cận ngang."
        )
    },
    {
        "title": "BÀI TẬP 3: TÌM TIỆM CẬN XIÊN BẰNG PHÉP CHIA",
        "lines": [
            r"Tìm các đường tiệm cận của đồ thị hàm số $f(x) = \frac{2x^2 + 3x + 4}{x + 1}$.",
            r"Tập xác định: $D = \mathbb{R} \setminus \{-1\}$.",
            r"Thực hiện chia đa thức: $2x^2 + 3x + 4 = (x + 1)(2x + 1) + 3$.",
            r"Suy ra biểu thức hàm số: $f(x) = 2x + 1 + \frac{3}{x + 1}$.",
            r"Vì $\lim_{x \to \pm\infty} [f(x) - (2x + 1)] = \lim_{x \to \pm\infty} \frac{3}{x + 1} = 0 \implies \boxed{y = 2x + 1}$ là TCX.",
            r"Tại $x = -1: \lim_{x \to -1^+} f(x) = +\infty \implies \boxed{x = -1}$ là tiệm cận đứng.",
            r"Hàm phân thức bậc hai trên bậc nhất không có tiệm cận ngang."
        ],
        "narration": (
            "Bài tập ba yêu cầu tìm tiệm cận của hàm bậc hai chia bậc nhất. "
            "Ta thực hiện phép chia đa thức được thương là hai x cộng một và "
            "phần dư là ba. Biểu thức dư ba chia x cộng một triệt tiêu khi x "
            "ra vô cực, do đó đường thẳng y bằng hai x cộng một là tiệm cận "
            "xiên. Nghiệm của mẫu cho tiệm cận đứng x bằng âm một."
        )
    },
    {
        "title": "BÀI TẬP 4: BÀI TOÁN THAM SỐ VÀ SỰ TRIỆT TIÊU",
        "lines": [
            r"Cho hàm số $f(x) = \frac{2x + m}{x - 1}$. Tìm $m$ để đồ thị có tiệm cận đứng $x = 1$.",
            r"Biến đổi tử thức theo mẫu: $f(x) = 2 + \frac{m + 2}{x - 1}$.",
            r"• Trường hợp $m + 2 \neq 0 \iff m \neq -2$:",
            r"  Tử của phần dư khác $0 \implies \lim_{x \to 1^\pm} f(x) = \pm\infty \implies \boxed{x = 1}$ là TCĐ.",
            r"• Trường hợp $m = -2 \implies f(x) = \frac{2x - 2}{x - 1} = 2, \forall x \neq 1$:",
            r"  Khi đó $\lim_{x \to 1} f(x) = 2$ (hữu hạn) $\implies$ Đồ thị không có tiệm cận đứng.",
            r"Đáp số: Giá trị cần tìm là $\boxed{m \neq -2}$. Tiệm cận ngang luôn là $\boxed{y = 2}$."
        ],
        "narration": (
            "Bài tập bốn xét bài toán chứa tham số m. Để đường thẳng x bằng một "
            "là tiệm cận đứng, tử số tại x bằng một phải khác không. Thay x "
            "bằng một vào tử, ta được hai cộng m phải khác không, tương đương "
            "m khác âm hai. Nếu m bằng âm hai, hàm số suy biến thành đường nằm "
            "ngang y bằng hai và không có tiệm cận đứng."
        )
    },
    {
        "title": "5. QUY TRÌNH CHUẨN TÌM TIỆM CẬN & LỖI SAI",
        "lines": [
            r"Bước 1: Tìm tập xác định $D$; xác định các điểm kỳ dị ở biên và hướng $\pm\infty$.",
            r"Bước 2: Tính giới hạn một phía tại nghiệm của mẫu để tìm TCĐ $\boxed{x = x_0}$.",
            r"Bước 3: Tính giới hạn khi $x \to \pm\infty$ để tìm TCN $\boxed{y = L}$.",
            r"Bước 4: Nếu bậc tử = bậc mẫu + 1, chia đa thức tìm TCX $\boxed{y = ax + b}$.",
            r"Ba sai lầm nghiêm trọng cần ghi nhớ:",
            r"1. Vội vàng cho mẫu bằng $0$ mà không kiểm tra sự triệt tiêu của tử thức.",
            r"2. Quên xét trường hợp $\sqrt{x^2} = |x|$ dẫn đến bỏ sót tiệm cận ngang âm.",
            r"3. Trong cùng một hướng vô cực, không thể đồng thời vừa có TCN vừa có TCX."
        ],
        "narration": (
            "Tổng kết lại quy trình giải toán: Bước một tìm tập xác định. Bước "
            "hai tính giới hạn một phía tìm tiệm cận đứng. Bước ba tính giới "
            "hạn tại vô cực tìm tiệm cận ngang. Bước bốn chia đa thức nếu có "
            "tiệm cận xiên. Hãy luôn khắc ghi ba lỗi sai thường gặp để không "
            "bị mất điểm đáng tiếc trong kỳ thi."
        )
    },
    {
        "title": "TỰ LUYỆN VÀ TỔNG KẾT",
        "lines": [
            r"Bài 1: Tìm các tiệm cận của hàm số $f(x) = \frac{3x - 2}{x + 2}$.",
            r"  $\implies$ Đáp án: Tiệm cận đứng $\boxed{x = -2}$, tiệm cận ngang $\boxed{y = 3}$.",
            r"Bài 2: Tìm các tiệm cận của hàm số $f(x) = \frac{x^2 + 3}{x - 1} = x + 1 + \frac{4}{x - 1}$.",
            r"  $\implies$ Đáp án: Tiệm cận đứng $\boxed{x = 1}$, tiệm cận xiên $\boxed{y = x + 1}$.",
            r"Ghi nhớ: TCĐ gắn với điểm hữu hạn ($x \to x_0$); TCN và TCX gắn với vô cực ($x \to \pm\infty$).",
            r"Chúc các em học tốt và đạt kết quả cao! • Thầy Nguyễn Văn Sang"
        ],
        "narration": (
            "Để củng cố bài học, các em hãy tự giải hai câu bài tập trên màn "
            "hình. Câu một có tiệm cận đứng x bằng âm hai và tiệm cận ngang y "
            "bằng ba. Câu hai có tiệm cận đứng x bằng một và tiệm cận xiên y "
            "bằng x cộng một. Thầy Nguyễn Văn Sang chúc các em nắm vững kiến "
            "thức và tự tin đạt điểm tối đa!"
        )
    }
]

# ================================================================
# XỬ LÝ TEXT VÀ MÃ TOÁN LATEX
# ================================================================

def make_line_element(content, size=24, color=FG, max_width=None):
    if "$" not in content:
        mob = Text(content, font=FONT, font_size=size, color=color, line_spacing=0.85)
        if max_width and mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    parts = content.split("$")
    items = []
    for idx, part in enumerate(parts):
        if not part:
            continue
        if idx % 2 == 0:
            txt_mob = Text(part, font=FONT, font_size=size, color=color)
            items.append(txt_mob)
        else:
            is_boxed = r"\boxed" in part
            math_color = GOLD if is_boxed else (ACCENT if any(k in part for k in ["=", r"\lim", r"\to", r"\implies"]) else INK)
            math_mob = MathTex(part, font_size=size + 3, color=math_color, tex_template=TMPL)
            items.append(math_mob)

    if not items:
        return VMobject()

    group = VGroup()
    for i, it in enumerate(items):
        if i == 0:
            group.add(it)
        else:
            prev = items[i - 1]
            buff = 0.05 if (isinstance(it, Text) and it.text and it.text[0] in ".,;:)") else 0.11
            it.next_to(prev, RIGHT, buff=buff)
            it.shift(DOWN * (it.get_bottom()[1] - prev.get_bottom()[1]))
            group.add(it)

    if max_width and group.width > max_width:
        group.scale_to_fit_width(max_width)
    return group


def make_body(lines, has_graph):
    font_size = 23 if has_graph else 26
    max_width = 6.25 if has_graph else 12.8
    items = []
    for idx, line in enumerate(lines):
        line_color = FG
        if idx == 0:
            line_color = ACCENT
        elif idx == len(lines) - 1:
            line_color = GREEN
        items.append(make_line_element(line, size=font_size, color=line_color, max_width=max_width))

    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.20 if has_graph else 0.24)
    if body.height > 5.50:
        body.scale_to_fit_height(5.50)
    body.to_edge(LEFT, buff=0.45)
    body.shift(UP * (2.55 - body.get_top()[1]))
    return body


# ================================================================
# ĐỒ THỊ VÀ TIỆM CẬN
# ================================================================

def evaluate_function(name, x):
    if name == "inverse":
        return 1.0 / x
    if name == "rational_21":
        return (2.0 * x + 1.0) / (x - 1.0)
    if name == "inverse_sqrt":
        return 1.0 / np.sqrt(x)
    if name == "two_horizontal":
        return x / np.sqrt(x * x + 1.0)
    if name == "slant_simple":
        return x + 1.0 / x
    if name == "slant_shift":
        return x + 1.0 + 1.0 / (x + 1.0)
    if name == "cross_horizontal":
        return x / (x * x + 1.0)
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
    for pt in candidates:
        if not any(math.hypot(pt[0] - o[0], pt[1] - o[1]) < eps for o in unique):
            unique.append(pt)
    if len(unique) < 2:
        return None
    pairs = [(p, q) for i, p in enumerate(unique) for q in unique[i + 1:]]
    return max(pairs, key=lambda pr: (pr[0][0] - pr[1][0])**2 + (pr[0][1] - pr[1][1])**2)


def build_graph(spec):
    xmin, xmax, ymin, ymax = spec["range"]
    x_step = 2 if xmax - xmin > 10 else 1
    y_step = 2 if ymax - ymin > 10 else 1

    axes = Axes(
        x_range=[xmin, xmax, x_step],
        y_range=[ymin, ymax, y_step],
        x_length=5.3,
        y_length=4.6,
        axis_config={
            "color": "#94A3B8",
            "stroke_width": 1.6,
            "include_ticks": True,
            "include_numbers": False,
            "tip_width": 0.12,
            "tip_height": 0.12
        }
    ).move_to([3.75, -0.05, 0])

    graph = VGroup()
    grid = VGroup()
    first_x = math.ceil(xmin / x_step) * x_step
    first_y = math.ceil(ymin / y_step) * y_step

    for x in np.arange(first_x, xmax + 0.001, x_step):
        grid.add(Line(axes.c2p(x, ymin), axes.c2p(x, ymax), color="#1E293B", stroke_width=0.7))
    for y in np.arange(first_y, ymax + 0.001, y_step):
        grid.add(Line(axes.c2p(xmin, y), axes.c2p(xmax, y), color="#1E293B", stroke_width=0.7))
    graph.add(grid, axes)

    tick_labels = VGroup()
    for x in np.arange(first_x, xmax + 0.001, x_step):
        if abs(x) > 1e-8 and xmin < x < xmax:
            lbl = MathTex(f"{x:g}", font_size=16, color=MUTED, tex_template=TMPL)
            lbl.next_to(axes.c2p(x, 0), DOWN, buff=0.08)
            tick_labels.add(lbl)
    for y in np.arange(first_y, ymax + 0.001, y_step):
        if abs(y) > 1e-8 and ymin < y < ymax:
            lbl = MathTex(f"{y:g}", font_size=16, color=MUTED, tex_template=TMPL)
            lbl.next_to(axes.c2p(0, y), LEFT, buff=0.08)
            tick_labels.add(lbl)
    graph.add(tick_labels)

    x_lbl = MathTex("x", font_size=20, color=MUTED, tex_template=TMPL).next_to(axes.c2p(xmax, 0), RIGHT, buff=0.06)
    y_lbl = MathTex("y", font_size=20, color=MUTED, tex_template=TMPL).next_to(axes.c2p(0, ymax), UP, buff=0.06)
    o_lbl = MathTex("O", font_size=18, color=MUTED, tex_template=TMPL).next_to(axes.c2p(0, 0), DL, buff=0.06)
    graph.add(x_lbl, y_lbl, o_lbl)

    legend_items = []
    for index, asymp in enumerate(spec.get("asymptotes", [])):
        kind = asymp[0]
        color = GOLD if index % 2 == 0 else PINK
        if kind == "v":
            val, label_str = asymp[1:]
            ends = line_rectangle_intersections(1, 0, val, spec["range"])
        elif kind == "h":
            val, label_str = asymp[1:]
            ends = line_rectangle_intersections(0, 1, val, spec["range"])
        else:
            a, b, label_str = asymp[1:]
            ends = line_rectangle_intersections(-a, 1, b, spec["range"])

        if ends is not None:
            p, q = ends
            graph.add(DashedLine(
                axes.c2p(*p), axes.c2p(*q),
                dash_length=0.12, dashed_ratio=0.55,
                stroke_width=2.8, color=color
            ))

        clean_tex = label_str.strip("$")
        legend_items.append(MathTex(clean_tex, font_size=22, color=color, tex_template=TMPL))

    # Vẽ đường cong hàm số
    for left, right in spec["intervals"]:
        left = max(left, xmin)
        right = min(right, xmax)
        if left >= right:
            continue
        xs = np.linspace(left, right, 1800)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            ys = evaluate_function(spec["func"], xs)
        valid = np.isfinite(ys) & (ys >= ymin) & (ys <= ymax)
        indices = np.flatnonzero(valid)
        if len(indices) < 2:
            continue
        breaks = np.where(np.diff(indices) > 1)[0] + 1
        for run in np.split(indices, breaks):
            if len(run) < 2:
                continue
            pts = [axes.c2p(float(xs[i]), float(ys[i])) for i in run]
            curve = VMobject().set_points_as_corners(pts)
            curve.set_stroke(color=CYAN, width=3.2)
            graph.add(curve)

    for x, y, label_content in spec.get("points", []):
        pt = Dot(axes.c2p(x, y), radius=0.065, color=GOLD)
        clean_lbl = label_content.strip("$")
        lbl = MathTex(clean_lbl, font_size=20, color=GOLD, tex_template=TMPL).next_to(pt, UR, buff=0.08)
        lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.04)
        graph.add(pt, lbl)

    if legend_items:
        legend = VGroup(*legend_items).arrange(RIGHT, buff=0.35)
        if legend.width > 5.4:
            legend.scale_to_fit_width(5.4)
        legend.move_to([3.75, 2.70, 0])
        graph.add(legend)

    if spec.get("caption"):
        cap = make_line_element(spec["caption"], size=20, color=GREEN, max_width=5.6).move_to([3.75, -2.95, 0])
        graph.add(cap)

    return graph


# ================================================================
# SCENE CHÍNH
# ================================================================

class DuongTiemCanToan12(Scene):
    def construct(self):
        if not TIMING_FILE.exists():
            raise RuntimeError("Chưa tìm thấy tệp timing.json. Hãy chuẩn bị âm thanh trước.")

        timing = json.loads(TIMING_FILE.read_text(encoding="utf-8"))
        durations = timing["durations"]

        footer_bg = Rectangle(
            width=config.frame_width, height=0.55,
            stroke_width=0, fill_color="#070c18", fill_opacity=1
        ).to_edge(DOWN, buff=0).set_z_index(100)

        footer_rule = Line(
            [-config.frame_width / 2, -3.45, 0],
            [config.frame_width / 2, -3.45, 0],
            stroke_width=1.5, color=ACCENT
        ).set_z_index(101)

        footer_name = Text(TEN_THAY, font=FONT, font_size=20, color=FG, weight="BOLD"
                           ).move_to([0, -3.72, 0]).set_z_index(102)

        footer_subj = Text("TOÁN 12 • ĐƯỜNG TIỆM CẬN", font=FONT, font_size=15, color=MUTED
                           ).to_edge(LEFT, buff=0.35)
        footer_subj.set_y(-3.72).set_z_index(102)

        self.add(footer_bg, footer_rule, footer_name, footer_subj)

        for index, slide in enumerate(SLIDES):
            title = make_line_element(slide["title"], size=30, color=ACCENT, max_width=12.6).move_to([0, 3.32, 0])
            header_rule = Line([-6.65, 2.92, 0], [6.65, 2.92, 0], stroke_width=1.2, color="#2A3D5C")

            counter = Text(f"{index + 1:02d} / {len(SLIDES):02d}", font=FONT, font_size=16, color=MUTED
                           ).to_edge(RIGHT, buff=0.35)
            counter.set_y(-3.72).set_z_index(103)

            has_graph = "graph" in slide
            body = make_body(slide["lines"], has_graph)
            content = VGroup(title, header_rule, body)

            if has_graph:
                divider = Line([0.15, -2.75, 0], [0.15, 2.65, 0], stroke_width=1, color="#23354E")
                content.add(divider, build_graph(slide["graph"]))

            self.add(counter)
            self.play(FadeIn(content, shift=UP * 0.08), run_time=ENTER_TIME)

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            if audio_path.exists():
                self.add_sound(str(audio_path))

            track = Line(LEFT * 6.60 + DOWN * 3.25, RIGHT * 6.60 + DOWN * 3.25, color="#1B283A", stroke_width=3)
            progress = Line(LEFT * 6.60 + DOWN * 3.25, RIGHT * 6.60 + DOWN * 3.25, color=ACCENT, stroke_width=3)

            self.add(track)
            self.play(Create(progress), run_time=durations[index], rate_func=linear)
            self.wait(AFTER_AUDIO_TIME)

            self.play(
                FadeOut(content, shift=UP * 0.05),
                FadeOut(track), FadeOut(progress), FadeOut(counter),
                run_time=EXIT_TIME
            )


# ================================================================
# CHUẨN BỊ ÂM THANH
# ================================================================

async def make_mp3(text, destination):
    comm = edge_tts.Communicate(text=text, voice=VOICE, rate=VOICE_RATE)
    await comm.save(str(destination))

async def prepare_audio():
    lengths = []
    print(f"Tổng số trang bài giảng: {len(SLIDES)}")
    for index, slide in enumerate(SLIDES):
        text = slide["narration"]
        key = hashlib.md5((VOICE + VOICE_RATE + text).encode("utf-8")).hexdigest()
        mp3 = AUDIO_DIR / f"{key}.mp3"
        wav = AUDIO_DIR / f"voice_{index:02d}.wav"

        if not mp3.exists() or mp3.stat().st_size < 1024:
            for attempt in range(3):
                try:
                    await make_mp3(text, mp3)
                    if mp3.exists() and mp3.stat().st_size >= 1024:
                        break
                except Exception as e:
                    print(f"  [TTS] Thử lại lần {attempt+1} cho trang {index+1}: {e}")
                    await asyncio.sleep(1.5)

        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", str(mp3),
            "-ar", "44100", "-ac", "2",
            str(wav)
        ], check=True)

        dur = probe_duration(wav)
        lengths.append(dur)
        if (index + 1) % 5 == 0 or (index + 1) == len(SLIDES):
            print(f"  -> Đã tạo giọng đọc: {index + 1}/{len(SLIDES)} trang.")

    TIMING_FILE.write_text(json.dumps({
        "durations": lengths,
        "voice": VOICE,
        "rate": VOICE_RATE
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Hoàn tất chuẩn bị âm thanh.")

if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
