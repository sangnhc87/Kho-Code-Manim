import sys
import subprocess
from pathlib import Path

def run_command(command):
    subprocess.run(command, check=True)

print("BƯỚC 1/4: Cài đặt thư viện...")

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

WORK = Path("/content/duong_tiem_can_toan_thuc_te")
WORK.mkdir(parents=True, exist_ok=True)
SCRIPT = WORK / "duong_tiem_can_toan_thuc_te.py"

SOURCE = r'''
import sys
import subprocess
from pathlib import Path
import asyncio
import edge_tts
import json
import math
import textwrap

from manim import *

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

config.background_color = BG

# Dữ liệu bài học
SLIDES = [
    {
        "title": "BÀI TOÁN THỰC TẾ: ĐƯỜNG TIỆM CẬN",
        "lines": [
            "Bài tiếp theo: Ứng dụng đường tiệm cận trong thực tế",
            "Mục tiêu 1. Nhận biết các bài toán thực tế có tiệm cận.",
            "Mục tiêu 2. Thiết lập hàm số từ mô hình thực tế.",
            "Mục tiêu 3. Xác định tiệm cận và ý nghĩa thực tế.",
            "Mục tiêu 4. Giải quyết bài toán tối ưu có tiệm cận.",
            "Chuẩn bị: giấy nháp, bút, máy tính."
        ],
        "narration": (
            "Chào các em. Ở bài trước, chúng ta đã học về các bài toán thực tế "
            "với bất phương trình hai ẩn. Hôm nay, chúng ta sẽ tìm hiểu về "
            "ứng dụng của đường tiệm cận trong các bài toán thực tế. Bài học có "
            "bốn mục tiêu: nhận biết các bài toán thực tế có tiệm cận; thiết lập "
            "hàm số từ mô hình thực tế; xác định tiệm cận và ý nghĩa thực tế; "
            "và giải quyết bài toán tối ưu có tiệm cận. Các em hãy chuẩn bị "
            "giấy nháp, bút và máy tính. Khi gặp phần luyện tập, hãy dừng video, "
            "tự giải trước rồi đối chiếu với lời giải."
        )
    },
    {
        "title": "1. ÔN TẬP KIẾN THỨC NỀN VỀ TIỆM CẬN",
        "lines": [
            "Đường thẳng $x = a$ là tiệm cận đứng của đồ thị hàm số $y = f(x)$ nếu:",
            r"$\lim_{x \to a^+} f(x) = \pm\infty$ hoặc $\lim_{x \to a^-} f(x) = \pm\infty$",
            "Đường thẳng $y = b$ là tiệm cận ngang của đồ thị hàm số $y = f(x)$ nếu:",
            r"$\lim_{x \to +\infty} f(x) = b$ hoặc $\lim_{x \to -\infty} f(x) = b$",
            "Đường thẳng $y = ax + b$ là tiệm cận xiên của đồ thị hàm số $y = f(x)$ nếu:",
            r"$\lim_{x \to \pm\infty} [f(x) - (ax + b)] = 0$"
        ],
        "narration": (
            "Trước hết, ta ôn tập kiến thức nền về tiệm cận. Đường thẳng x bằng a "
            "là tiệm cận đứng của đồ thị hàm số y bằng f(x) nếu giới hạn khi x tiến "
            "đến a từ bên phải hoặc bên trái của f(x) bằng dương hoặc âm vô cùng. "
            "Đường thẳng y bằng b là tiệm cận ngang nếu giới hạn khi x tiến đến "
            "dương vô cùng hoặc âm vô cùng của f(x) bằng b. Đường thẳng y bằng a x "
            "cộng b là tiệm cận xiên nếu giới hạn khi x tiến đến dương hoặc âm vô "
            "cùng của hiệu f(x) trừ a x cộng b bằng không."
        )
    },
    {
        "title": "2. CÁC BƯỚC GIẢI BÀI TOÁN THỰC TẾ CÓ TIỆM CẬN",
        "lines": [
            "Bước 1. Đọc kỹ đề bài và xác định đại lượng thay đổi.",
            "Bước 2. Thiết lập hàm số mô tả mối quan hệ giữa các đại lượng.",
            "Bước 3. Xác định tập xác định phù hợp với thực tế.",
            "Bước 4. Tìm các đường tiệm cận của hàm số.",
            "Bước 5. Phân tích ý nghĩa thực tế của các tiệm cận.",
            "Bước 6. Giải quyết yêu cầu của bài toán (tối ưu, giới hạn...)."
        ],
        "narration": (
            "Để giải một bài toán thực tế có tiệm cận, ta thực hiện theo sáu bước. "
            "Đầu tiên, đọc kỹ đề bài và xác định đại lượng thay đổi. Thứ hai, thiết "
            "lập hàm số mô tả mối quan hệ giữa các đại lượng. Thứ ba, xác định tập "
            "xác định phù hợp với thực tế. Thứ tư, tìm các đường tiệm cận của hàm số. "
            "Thứ năm, phân tích ý nghĩa thực tế của các tiệm cận. Cuối cùng, giải "
            "quyết yêu cầu của bài toán như tối ưu hoặc tìm giới hạn."
        )
    },
    {
        "title": "3. VÍ DỤ 1: BÀI TOÁN VỀ NỒNG ĐỘ DUNG DỊCH",
        "lines": [
            "Pha loãng một dung dịch chứa 100g chất tan bằng nước.",
            "Gọi $x$ (lít) là thể tích nước thêm vào.",
            r"Nồng độ $C(x) = \frac{100}{x + V_0}$ (g/lít), với $V_0$ là thể tích ban đầu.",
            r"Hàm số có dạng $y = \frac{k}{x + a}$ với $k, a > 0$.",
            "Tìm tiệm cận và ý nghĩa thực tế?"
        ],
        "narration": (
            "Xét ví dụ đầu tiên về nồng độ dung dịch: Khi pha loãng một dung dịch "
            "chứa một trăm gam chất tan bằng nước. Gọi x là thể tích nước thêm vào "
            "tính bằng lít. Nồng độ C(x) bằng một trăm chia cho x cộng V không gam "
            "trên lít, với V không là thể tích ban đầu. Hàm số có dạng y bằng k "
            "chia cho x cộng a với k và a dương. Ta cần tìm tiệm cận và ý nghĩa "
            "thực tế của chúng."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $C(x) = \frac{100}{x + V_0}$ với $x \ge 0$",
            r"TXĐ: $x \in [0; +\infty)$",
            r"Đạo hàm: $C'(x) = -\frac{100}{(x + V_0)^2} < 0$",
            r"Hàm số nghịch biến trên $[0; +\infty)$.",
            r"Khi $x \to +\infty$: $C(x) \to 0$",
            r"Khi $x \to 0^+$: $C(x) \to \frac{100}{V_0}$"
        ],
        "narration": (
            "Hàm số nồng độ là C(x) bằng một trăm chia cho x cộng V không với x "
            "không âm. Tập xác định là x thuộc từ không đến dương vô cùng. Đạo hàm "
            "C phẩy(x) bằng âm một trăm chia cho x cộng V không bình phương, luôn "
            "âm nên hàm số nghịch biến trên đoạn từ không đến dương vô cùng. Khi "
            "x tiến đến dương vô cùng, C(x) tiến đến không. Khi x tiến đến không "
            "dương, C(x) tiến đến một trăm chia cho V không."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = 0$ (khi $x \to +\infty$)",
            "Ý nghĩa: Khi thêm nhiều nước, nồng độ tiến đến 0.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            r"Giá trị lớn nhất: $C(0) = \frac{100}{V_0}$ (chưa pha loãng).",
            "Không có giá trị nhỏ nhất, chỉ có cận dưới là 0."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng không khi x tiến đến dương vô cùng. "
            "Ý nghĩa thực tế là khi thêm nhiều nước, nồng độ tiến đến không. Không "
            "có tiệm cận đứng trong tập xác định thực tế từ không đến dương vô cùng. "
            "Giá trị lớn nhất là C không bằng một trăm chia cho V không, tức là "
            "nồng độ ban đầu chưa pha loãng. Không có giá trị nhỏ nhất, chỉ có "
            "cận dưới là không."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): ỨNG DỤNG THỰC TẾ",
        "lines": [
            "Câu hỏi: Cần thêm bao nhiêu lít nước để nồng độ giảm còn 10%?",
            r"Giải phương trình: $\frac{100}{x + V_0} = 0.1 \times \frac{100}{V_0}$",
            r"Rút gọn: $\frac{100}{x + V_0} = \frac{10}{V_0}$",
            r"Suy ra: $100V_0 = 10(x + V_0)$",
            r"Giải: $100V_0 = 10x + 10V_0 \Rightarrow 90V_0 = 10x \Rightarrow x = 9V_0$",
            r"Kết luận: Cần thêm $9V_0$ lít nước để nồng độ giảm 10 lần."
        ],
        "narration": (
            "Câu hỏi thực tế là cần thêm bao nhiêu lít nước để nồng độ giảm còn "
            "mười phần trăm. Ta giải phương trình một trăm chia cho x cộng V không "
            "bằng không chấm một nhân một trăm chia cho V không. Rút gọn ta được "
            "một trăm chia cho x cộng V không bằng mười chia cho V không. Suy ra "
            "một trăm V không bằng mười nhân x cộng V không. Giải tiếp ta được "
            "chín mươi V không bằng mười x, suy ra x bằng chín V không. Kết luận "
            "là cần thêm chín V không lít nước để nồng độ giảm mười lần."
        )
    },
    {
        "title": "4. VÍ DỤ 2: BÀI TOÁN VỀ HIỆU SUẤT PHẢN ỨNG HÓA HỌC",
        "lines": [
            r"Phản ứng hóa học với hiệu suất $H(x) = \frac{100x}{x + k}$ %",
            "Trong đó $x$ là nồng độ chất phản ứng, $k$ là hằng số.",
            r"Hàm số có dạng $y = \frac{ax}{x + b}$ với $a, b > 0$.",
            "Tìm tiệm cận và ý nghĩa thực tế?"
        ],
        "narration": (
            "Xét ví dụ thứ hai về hiệu suất phản ứng hóa học: Hiệu suất phản ứng "
            "được mô tả bởi hàm số H(x) bằng một trăm x chia cho x cộng k phần trăm, "
            "trong đó x là nồng độ chất phản ứng và k là hằng số. Hàm số có dạng "
            "y bằng a x chia cho x cộng b với a và b dương. Ta cần tìm tiệm cận "
            "và ý nghĩa thực tế của chúng."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $H(x) = \frac{100x}{x + k}$ với $x \ge 0$",
            r"TXĐ: $x \in [0; +\infty)$",
            r"Đạo hàm: $H'(x) = \frac{100k}{(x + k)^2} > 0$",
            r"Hàm số đồng biến trên $[0; +\infty)$.",
            r"Khi $x \to +\infty$: $H(x) \to 100$",
            r"Khi $x \to 0^+$: $H(x) \to 0$"
        ],
        "narration": (
            "Hàm số hiệu suất là H(x) bằng một trăm x chia cho x cộng k với x "
            "không âm. Tập xác định là x thuộc từ không đến dương vô cùng. Đạo hàm "
            "H phẩy(x) bằng một trăm k chia cho x cộng k bình phương, luôn dương "
            "nên hàm số đồng biến trên đoạn từ không đến dương vô cùng. Khi x tiến "
            "đến dương vô cùng, H(x) tiến đến một trăm. Khi x tiến đến không dương, "
            "H(x) tiến đến không."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = 100$ (khi $x \to +\infty$)",
            "Ý nghĩa: Dù tăng nồng độ, hiệu suất không vượt quá 100%.",
            "Tiệm cận ngang thể hiện giới hạn vật lý của phản ứng.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            "Giá trị nhỏ nhất: $H(0) = 0$, giá trị lớn nhất tiến đến 100."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng một trăm khi x tiến đến dương vô cùng. "
            "Ý nghĩa thực tế là dù tăng nồng độ, hiệu suất không vượt quá một trăm phần trăm. "
            "Tiệm cận ngang thể hiện giới hạn vật lý của phản ứng. Không có tiệm cận đứng "
            "trong tập xác định thực tế từ không đến dương vô cùng. Giá trị nhỏ nhất là "
            "H không bằng không, giá trị lớn nhất tiến đến một trăm."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): ỨNG DỤNG THỰC TẾ",
        "lines": [
            "Câu hỏi: Khi nào hiệu suất đạt 90%?",
            r"Giải phương trình: $\frac{100x}{x + k} = 90$",
            r"Rút gọn: $100x = 90(x + k)$",
            r"Suy ra: $100x = 90x + 90k$",
            r"Giải: $10x = 90k \Rightarrow x = 9k$",
            r"Kết luận: Cần nồng độ $x = 9k$ để đạt hiệu suất 90%."
        ],
        "narration": (
            "Câu hỏi thực tế là khi nào hiệu suất đạt chín mươi phần trăm. Ta giải "
            "phương trình một trăm x chia cho x cộng k bằng chín mươi. Rút gọn ta "
            "được một trăm x bằng chín mươi nhân x cộng k. Suy ra một trăm x bằng "
            "chín mươi x cộng chín mươi k. Giải tiếp ta được mười x bằng chín mươi k, "
            "suy ra x bằng chín k. Kết luận là cần nồng độ x bằng chín k để đạt "
            "hiệu suất chín mươi phần trăm."
        )
    },
    {
        "title": "5. VÍ DỤ 3: BÀI TOÁN VỀ CHI PHÍ TRUNG BÌNH",
        "lines": [
            r"Chi phí sản xuất $x$ sản phẩm: $C(x) = ax + b + \frac{c}{x}$ (đồng)",
            "Trong đó $a$ là chi phí nguyên vật liệu/sản phẩm,",
            "b là chi phí cố định, $c/x$ là chi phí quản lý phân bổ/sản phẩm.",
            r"Chi phí trung bình: $A(x) = \frac{C(x)}{x} = a + \frac{b}{x} + \frac{c}{x^2}$",
            "Tìm tiệm cận và chi phí tối thiểu?"
        ],
        "narration": (
            "Xét ví dụ thứ ba về chi phí trung bình: Chi phí sản xuất x sản phẩm "
            "là C(x) bằng a x cộng b cộng c chia cho x đồng, trong đó a là chi phí "
            "nguyên vật liệu mỗi sản phẩm, b là chi phí cố định, c chia cho x là "
            "chi phí quản lý phân bổ mỗi sản phẩm. Chi phí trung bình là A(x) bằng "
            "C(x) chia cho x bằng a cộng b chia cho x cộng c chia cho x bình. "
            "Ta cần tìm tiệm cận và chi phí tối thiểu."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $A(x) = a + \frac{b}{x} + \frac{c}{x^2}$ với $x > 0$",
            r"TXĐ: $x \in (0; +\infty)$",
            r"Đạo hàm: $A'(x) = -\frac{b}{x^2} - \frac{2c}{x^3} = -\frac{bx + 2c}{x^3}$",
            "Xét dấu đạo hàm để tìm chiều biến thiên.",
            r"Khi $x \to +\infty$: $A(x) \to a$",
            r"Khi $x \to 0^+$: $A(x) \to +\infty$"
        ],
        "narration": (
            "Hàm số chi phí trung bình là A(x) bằng a cộng b chia cho x cộng c "
            "chia cho x bình với x dương. Tập xác định là x thuộc từ không đến "
            "dương vô cùng. Đạo hàm A phẩy(x) bằng âm b chia cho x bình trừ "
            "hai c chia cho x lập phương, bằng âm b x cộng hai c chia cho x lập "
            "phương. Ta xét dấu đạo hàm để tìm chiều biến thiên. Khi x tiến đến "
            "dương vô cùng, A(x) tiến đến a. Khi x tiến đến không dương, A(x) "
            "tiến đến dương vô cùng."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = a$ (khi $x \to +\infty$)",
            "Ý nghĩa: Khi sản xuất số lượng lớn, chi phí trung bình tiến đến chi phí nguyên vật liệu.",
            r"Tiệm cận đứng: $x = 0$ (khi $x \to 0^+$)",
            "Ý nghĩa: Không thể sản xuất 0 sản phẩm, chi phí trung bình tiến đến vô cùng.",
            r"Hàm số có cực tiểu khi $A'(x) = 0$."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng a khi x tiến đến dương vô cùng. "
            "Ý nghĩa thực tế là khi sản xuất số lượng lớn, chi phí trung bình tiến "
            "đến chi phí nguyên vật liệu. Tiệm cận đứng là đường thẳng x bằng không "
            "khi x tiến đến không dương. Ý nghĩa là không thể sản xuất không sản phẩm, "
            "chi phí trung bình tiến đến vô cùng. Hàm số có cực tiểu khi A phẩy(x) bằng không."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): TÌM CỰC TIỂU",
        "lines": [
            r"Tìm cực tiểu: $A'(x) = -\frac{bx + 2c}{x^3} = 0$",
            r"Suy ra: $bx + 2c = 0 \Rightarrow x = -\frac{2c}{b}$",
            r"Vì $b, c > 0$, nên $x = \frac{2c}{b}$ (lấy giá trị dương).",
            r"Chi phí trung bình tối thiểu: $A_{min} = a + \frac{b}{\frac{2c}{b}} + \frac{c}{(\frac{2c}{b})^2}$",
            r"Rút gọn: $A_{min} = a + \frac{b^2}{2c} + \frac{b^2}{4c} = a + \frac{3b^2}{4c}$"
        ],
        "narration": (
            "Tìm cực tiểu bằng cách giải phương trình A phẩy(x) bằng âm b x cộng "
            "hai c chia cho x lập phương bằng không. Suy ra b x cộng hai c bằng "
            "không, suy ra x bằng âm hai c chia cho b. Vì b và c dương, nên x "
            "bằng hai c chia cho b lấy giá trị dương. Chi phí trung bình tối thiểu "
            "là A min bằng a cộng b chia cho hai c chia cho b cộng c chia cho "
            "hai c chia cho b bình. Rút gọn ta được A min bằng a cộng b bình "
            "chia cho hai c cộng b bình chia cho bốn c, bằng a cộng ba b bình "
            "chia cho bốn c."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): ỨNG DỤNG THỰC TẾ",
        "lines": [
            r"Giả sử $a = 1000$, $b = 5000000$, $c = 20000000$.",
            r"Sản lượng tối ưu: $x = \frac{2 \times 20000000}{5000000} = 8$ sản phẩm.",
            r"Chi phí trung bình tối thiểu: $A_{min} = 1000 + \frac{3 \times 5000000^2}{4 \times 20000000} = 938500$ đồng.",
            "Khi sản xuất 8 sản phẩm, chi phí trung bình là thấp nhất: 938500 đồng/sản phẩm.",
            "Khi sản xuất rất nhiều: chi phí trung bình tiến đến 1000 đồng/sản phẩm."
        ],
        "narration": (
            "Giả sử a bằng một nghìn, b bằng năm triệu, c bằng hai mươi triệu. "
            "Sản lượng tối ưu là x bằng hai nhân hai mươi triệu chia cho năm triệu "
            "bằng tám sản phẩm. Chi phí trung bình tối thiểu là A min bằng một nghìn "
            "cộng ba nhân năm triệu bình chia cho bốn nhân hai mươi triệu, bằng "
            "một nghìn cộng chín trăm ba mươi bảy nghìn năm trăm, bằng chín trăm "
            "ba mươi tám nghìn năm trăm đồng. Khi sản xuất tám sản phẩm, chi phí "
            "trung bình là thấp nhất: chín trăm ba mươi tám nghìn năm trăm đồng "
            "mỗi sản phẩm. Khi sản xuất rất nhiều, chi phí trung bình tiến đến "
            "một nghìn đồng mỗi sản phẩm."
        )
    },
    {
        "title": "6. VÍ DỤ 4: BÀI TOÁN VỀ TỐC ĐỘ PHẢN ỨNG",
        "lines": [
            r"Tốc độ phản ứng hóa học: $v(C) = \frac{kC}{C + K_M}$",
            "Trong đó $C$ là nồng độ chất phản ứng, $k$ và $K_M$ là hằng số.",
            "Đây là phương trình Michaelis-Menten trong sinh hóa.",
            r"Hàm số có dạng $y = \frac{ax}{x + b}$ với $a, b > 0$.",
            "Tìm tiệm cận và ý nghĩa sinh học?"
        ],
        "narration": (
            "Xét ví dụ thứ tư về tốc độ phản ứng hóa học: Tốc độ phản ứng được mô "
            "tả bởi hàm số v(C) bằng k C chia cho C cộng K_M, trong đó C là nồng "
            "độ chất phản ứng, k và K_M là hằng số. Đây là phương trình Michaelis-"
            "Menten trong sinh hóa. Hàm số có dạng y bằng a x chia cho x cộng b "
            "với a và b dương. Ta cần tìm tiệm cận và ý nghĩa sinh học của chúng."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $v(C) = \frac{kC}{C + K_M}$ với $C \ge 0$",
            r"TXĐ: $C \in [0; +\infty)$",
            r"Đạo hàm: $v'(C) = \frac{kK_M}{(C + K_M)^2} > 0$",
            r"Hàm số đồng biến trên $[0; +\infty)$.",
            r"Khi $C \to +\infty$: $v(C) \to k$",
            r"Khi $C \to 0^+$: $v(C) \to 0$"
        ],
        "narration": (
            "Hàm số tốc độ phản ứng là v(C) bằng k C chia cho C cộng K_M với C "
            "không âm. Tập xác định là C thuộc từ không đến dương vô cùng. Đạo hàm "
            "v phẩy(C) bằng k K_M chia cho C cộng K_M bình phương, luôn dương "
            "nên hàm số đồng biến trên đoạn từ không đến dương vô cùng. Khi C tiến "
            "đến dương vô cùng, v(C) tiến đến k. Khi C tiến đến không dương, "
            "v(C) tiến đến không."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = k$ (khi $C \to +\infty$)",
            "Ý nghĩa sinh học: Khi nồng độ rất cao, tốc độ tiến đến hằng số $k$ (tốc độ tối đa).",
            "Tiệm cận ngang thể hiện sự bão hòa của enzyme.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            r"Giá trị nhỏ nhất: $v(0) = 0$, giá trị lớn nhất tiến đến $k$."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng k khi C tiến đến dương vô cùng. "
            "Ý nghĩa sinh học là khi nồng độ rất cao, tốc độ tiến đến hằng số k, "
            "đây là tốc độ tối đa. Tiệm cận ngang thể hiện sự bão hòa của enzyme. "
            "Không có tiệm cận đứng trong tập xác định thực tế từ không đến dương "
            "vô cùng. Giá trị nhỏ nhất là v không bằng không, giá trị lớn nhất "
            "tiến đến k."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): Ý NGHĨA SINH HỌC",
        "lines": [
            r"Khi $v(C) = \frac{k}{2}$: $\frac{kC}{C + K_M} = \frac{k}{2}$",
            r"Rút gọn: $\frac{C}{C + K_M} = \frac{1}{2}$",
            r"Suy ra: $2C = C + K_M \Rightarrow C = K_M$",
            r"Ý nghĩa: $K_M$ là nồng độ để tốc độ đạt một nửa tốc độ tối đa.",
            r"Khi $C = K_M$: $v = \frac{k}{2}$",
            r"$K_M$ đặc trưng cho ái lực của enzyme với chất nền."
        ],
        "narration": (
            "Khi v(C) bằng k chia cho hai: k C chia cho C cộng K_M bằng k chia "
            "cho hai. Rút gọn ta được C chia cho C cộng K_M bằng một nửa. Suy ra "
            "hai C bằng C cộng K_M, suy ra C bằng K_M. Ý nghĩa là K_M là nồng "
            "độ để tốc độ đạt một nửa tốc độ tối đa. Khi C bằng K_M, v bằng k "
            "chia cho hai. K_M đặc trưng cho ái lực của enzyme với chất nền."
        )
    },
    {
        "title": "7. VÍ DỤ 5: BÀI TOÁN VỀ MỨC ĐỘ BÃO HÒA",
        "lines": [
            r"Mức độ bão hòa oxy trong máu: $S(p) = \frac{100p^n}{p^n + P_{50}^n}$",
            "Trong đó $p$ là áp suất riêng phần của oxy, $n$ là hệ số Hill.",
            "Đây là phương trình Hill trong sinh lý học.",
            r"Hàm số có dạng $y = \frac{ax^n}{x^n + b}$ với $a, b, n > 0$.",
            "Tìm tiệm cận và ý nghĩa sinh lý?"
        ],
        "narration": (
            "Xét ví dụ thứ năm về mức độ bão hòa oxy trong máu: Mức độ bão hòa "
            "được mô tả bởi hàm số S(p) bằng một trăm p mũ n chia cho p mũ n "
            "cộng P năm mươi mũ n, trong đó p là áp suất riêng phần của oxy, "
            "n là hệ số Hill. Đây là phương trình Hill trong sinh lý học. Hàm "
            "số có dạng y bằng a x mũ n chia cho x mũ n cộng b với a, b, n dương. "
            "Ta cần tìm tiệm cận và ý nghĩa sinh lý của chúng."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $S(p) = \frac{100p^n}{p^n + P_{50}^n}$ với $p \ge 0$",
            r"TXĐ: $p \in [0; +\infty)$",
            r"Đạo hàm: $S'(p) = \frac{100nP_{50}^n p^{n-1}}{(p^n + P_{50}^n)^2} > 0$",
            r"Hàm số đồng biến trên $[0; +\infty)$.",
            r"Khi $p \to +\infty$: $S(p) \to 100$",
            r"Khi $p \to 0^+$: $S(p) \to 0$"
        ],
        "narration": (
            "Hàm số mức độ bão hòa là S(p) bằng một trăm p mũ n chia cho p mũ n "
            "cộng P năm mươi mũ n với p không âm. Tập xác định là p thuộc từ "
            "không đến dương vô cùng. Đạo hàm S phẩy(p) bằng một trăm n P năm "
            "mươi mũ n nhân p mũ n trừ một chia cho p mũ n cộng P năm mươi mũ n "
            "bình phương, luôn dương nên hàm số đồng biến trên đoạn từ không đến "
            "dương vô cùng. Khi p tiến đến dương vô cùng, S(p) tiến đến một trăm. "
            "Khi p tiến đến không dương, S(p) tiến đến không."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = 100$ (khi $p \to +\infty$)",
            "Ý nghĩa sinh lý: Khi áp suất oxy rất cao, mức độ bão hòa tiến đến 100%.",
            "Tiệm cận ngang thể hiện sự bão hòa hoàn toàn của hemoglobin.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            "Giá trị nhỏ nhất: $S(0) = 0$, giá trị lớn nhất tiến đến 100."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng một trăm khi p tiến đến dương "
            "vô cùng. Ý nghĩa sinh lý là khi áp suất oxy rất cao, mức độ bão hòa "
            "tiến đến một trăm phần trăm. Tiệm cận ngang thể hiện sự bão hòa hoàn "
            "toàn của hemoglobin. Không có tiệm cận đứng trong tập xác định thực "
            "tế từ không đến dương vô cùng. Giá trị nhỏ nhất là S không bằng "
            "không, giá trị lớn nhất tiến đến một trăm."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): Ý NGHĨA SINH LÝ",
        "lines": [
            r"Khi $S(p) = 50$: $\frac{100p^n}{p^n + P_{50}^n} = 50$",
            r"Rút gọn: $\frac{p^n}{p^n + P_{50}^n} = \frac{1}{2}$",
            r"Suy ra: $2p^n = p^n + P_{50}^n \Rightarrow p^n = P_{50}^n \Rightarrow p = P_{50}$",
            r"Ý nghĩa: $P_{50}$ là áp suất để mức độ bão hòa đạt 50%.",
            r"Khi $p = P_{50}$: $S = 50$",
            r"$P_{50}$ đặc trưng cho ái lực của hemoglobin với oxy."
        ],
        "narration": (
            "Khi S(p) bằng năm mươi: một trăm p mũ n chia cho p mũ n cộng P năm "
            "mươi mũ n bằng năm mươi. Rút gọn ta được p mũ n chia cho p mũ n "
            "cộng P năm mươi mũ n bằng một nửa. Suy ra hai p mũ n bằng p mũ n "
            "cộng P năm mươi mũ n, suy ra p mũ n bằng P năm mươi mũ n, suy ra "
            "p bằng P năm mươi. Ý nghĩa là P năm mươi là áp suất để mức độ bão "
            "hòa đạt năm mươi phần trăm. Khi p bằng P năm mươi, S bằng năm mươi. "
            "P năm mươi đặc trưng cho ái lực của hemoglobin với oxy."
        )
    },
    {
        "title": "8. VÍ DỤ 6: BÀI TOÁN VỀ ĐỘ PHÂN GIẢI THUỐC",
        "lines": [
            r"Độ phân giải thuốc trong cơ thể: $D(t) = \frac{D_0}{1 + kt}$",
            "Trong đó $D_0$ là liều ban đầu, $k$ là hằng số tốc độ.",
            r"Hàm số có dạng $y = \frac{a}{1 + bx}$ với $a, b > 0$.",
            "Tìm tiệm cận và thời gian để thuốc phân giải một nửa?"
        ],
        "narration": (
            "Xét ví dụ thứ sáu về độ phân giải thuốc trong cơ thể: Độ phân giải "
            "thuốc được mô tả bởi hàm số D(t) bằng D không chia cho một cộng k t, "
            "trong đó D không là liều ban đầu, k là hằng số tốc độ. Hàm số có "
            "dạng y bằng a chia cho một cộng b x với a và b dương. Ta cần tìm "
            "tiệm cận và thời gian để thuốc phân giải một nửa."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $D(t) = \frac{D_0}{1 + kt}$ với $t \ge 0$",
            r"TXĐ: $t \in [0; +\infty)$",
            r"Đạo hàm: $D'(t) = -\frac{D_0k}{(1 + kt)^2} < 0$",
            r"Hàm số nghịch biến trên $[0; +\infty)$.",
            r"Khi $t \to +\infty$: $D(t) \to 0$",
            r"Khi $t \to 0^+$: $D(t) \to D_0$"
        ],
        "narration": (
            "Hàm số độ phân giải thuốc là D(t) bằng D không chia cho một cộng k t "
            "với t không âm. Tập xác định là t thuộc từ không đến dương vô cùng. "
            "Đạo hàm D phẩy(t) bằng âm D không k chia cho một cộng k t bình phương, "
            "luôn âm nên hàm số nghịch biến trên đoạn từ không đến dương vô cùng. "
            "Khi t tiến đến dương vô cùng, D(t) tiến đến không. Khi t tiến đến "
            "không dương, D(t) tiến đến D không."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = 0$ (khi $t \to +\infty$)",
            "Ý nghĩa y học: Khi thời gian dài, thuốc được phân giải hoàn toàn.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            r"Giá trị lớn nhất: $D(0) = D_0$ (liều ban đầu).",
            "Không có giá trị nhỏ nhất, chỉ có cận dưới là 0."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng không khi t tiến đến dương vô cùng. "
            "Ý nghĩa y học là khi thời gian dài, thuốc được phân giải hoàn toàn. "
            "Không có tiệm cận đứng trong tập xác định thực tế từ không đến dương "
            "vô cùng. Giá trị lớn nhất là D không bằng D không, tức là liều ban đầu. "
            "Không có giá trị nhỏ nhất, chỉ có cận dưới là không."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): THỜI GIAN PHÂN GIẢI MỘT NỬA",
        "lines": [
            r"Tìm thời gian để $D(t) = \frac{D_0}{2}$?",
            r"Giải phương trình: $\frac{D_0}{1 + kt} = \frac{D_0}{2}$",
            r"Rút gọn: $\frac{1}{1 + kt} = \frac{1}{2}$",
            r"Suy ra: $2 = 1 + kt \Rightarrow kt = 1 \Rightarrow t = \frac{1}{k}$",
            r"Thời gian phân giải một nửa: $t_{1/2} = \frac{1}{k}$",
            "Ý nghĩa: Thời gian để nồng độ thuốc giảm còn một nửa."
        ],
        "narration": (
            "Tìm thời gian để D(t) bằng D không chia cho hai. Ta giải phương trình "
            "D không chia cho một cộng k t bằng D không chia cho hai. Rút gọn ta "
            "được một chia cho một cộng k t bằng một nửa. Suy ra hai bằng một "
            "cộng k t, suy ra k t bằng một, suy ra t bằng một chia cho k. Thời "
            "gian phân giải một nửa là t một nửa bằng một chia cho k. Ý nghĩa "
            "là thời gian để nồng độ thuốc giảm còn một nửa."
        )
    },
    {
        "title": "9. VÍ DỤ 7: BÀI TOÁN VỀ HIỆU QUẢ ĐIỀU TRỊ",
        "lines": [
            r"Hiệu quả điều trị theo liều thuốc: $E(d) = \frac{E_{max}d}{d + EC_{50}}$",
            r"Trong đó $d$ là liều thuốc, $E_{max}$ là hiệu quả tối đa, $EC_{50}$ là liều gây 50% hiệu quả.",
            "Đây là phương trình Emax trong dược lý học.",
            r"Hàm số có dạng $y = \frac{ax}{x + b}$ với $a, b > 0$.",
            "Tìm tiệm cận và liều tối ưu?"
        ],
        "narration": (
            "Xét ví dụ thứ bảy về hiệu quả điều trị theo liều thuốc: Hiệu quả điều "
            "trị được mô tả bởi hàm số E(d) bằng E max d chia cho d cộng E C năm "
            "mươi, trong đó d là liều thuốc, E max là hiệu quả tối đa, E C năm "
            "mươi là liều gây năm mươi phần trăm hiệu quả. Đây là phương trình "
            "Emax trong dược lý học. Hàm số có dạng y bằng a x chia cho x cộng "
            "b với a và b dương. Ta cần tìm tiệm cận và liều tối ưu."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): PHÂN TÍCH HÀM SỐ",
        "lines": [
            r"Hàm số: $E(d) = \frac{E_{max}d}{d + EC_{50}}$ với $d \ge 0$",
            r"TXĐ: $d \in [0; +\infty)$",
            r"Đạo hàm: $E'(d) = \frac{E_{max}EC_{50}}{(d + EC_{50})^2} > 0$",
            r"Hàm số đồng biến trên $[0; +\infty)$.",
            r"Khi $d \to +\infty$: $E(d) \to E_{max}$",
            r"Khi $d \to 0^+$: $E(d) \to 0$"
        ],
        "narration": (
            "Hàm số hiệu quả điều trị là E(d) bằng E max d chia cho d cộng E C "
            "năm mươi với d không âm. Tập xác định là d thuộc từ không đến dương "
            "vô cùng. Đạo hàm E phẩy(d) bằng E max E C năm mươi chia cho d cộng "
            "E C năm mươi bình phương, luôn dương nên hàm số đồng biến trên đoạn "
            "từ không đến dương vô cùng. Khi d tiến đến dương vô cùng, E(d) tiến "
            "đến E max. Khi d tiến đến không dương, E(d) tiến đến không."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): XÁC ĐỊNH TIỆM CẬN",
        "lines": [
            r"Tiệm cận ngang: $y = E_{max}$ (khi $d \to +\infty$)",
            r"Ý nghĩa y học: Dù tăng liều, hiệu quả không vượt quá $E_{max}$.",
            "Tiệm cận ngang thể hiện giới hạn sinh lý của cơ thể.",
            r"Không có tiệm cận đứng trong TXĐ thực tế $[0; +\infty)$.",
            r"Giá trị nhỏ nhất: $E(0) = 0$, giá trị lớn nhất tiến đến $E_{max}$."
        ],
        "narration": (
            "Tiệm cận ngang là đường thẳng y bằng E max khi d tiến đến dương vô cùng. "
            "Ý nghĩa y học là dù tăng liều, hiệu quả không vượt quá E max. "
            "Tiệm cận ngang thể hiện giới hạn sinh lý của cơ thể. Không có tiệm "
            "cận đứng trong tập xác định thực tế từ không đến dương vô cùng. "
            "Giá trị nhỏ nhất là E không bằng không, giá trị lớn nhất tiến đến E max."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): LIỀU GÂY 50% HIỆU QUẢ",
        "lines": [
            r"Khi $E(d) = \frac{E_{max}}{2}$: $\frac{E_{max}d}{d + EC_{50}} = \frac{E_{max}}{2}$",
            r"Rút gọn: $\frac{d}{d + EC_{50}} = \frac{1}{2}$",
            r"Suy ra: $2d = d + EC_{50} \Rightarrow d = EC_{50}$",
            r"Ý nghĩa: $EC_{50}$ là liều để đạt 50% hiệu quả tối đa.",
            r"Khi $d = EC_{50}$: $E = \frac{E_{max}}{2}$",
            r"$EC_{50}$ đặc trưng cho độ nhạy của cơ thể với thuốc."
        ],
        "narration": (
            "Khi E(d) bằng E max chia cho hai: E max d chia cho d cộng E C năm "
            "mươi bằng E max chia cho hai. Rút gọn ta được d chia cho d cộng "
            "E C năm mươi bằng một nửa. Suy ra hai d bằng d cộng E C năm mươi, "
            "suy ra d bằng E C năm mươi. Ý nghĩa là E C năm mươi là liều để đạt "
            "năm mươi phần trăm hiệu quả tối đa. Khi d bằng E C năm mươi, E "
            "bằng E max chia cho hai. E C năm mươi đặc trưng cho độ nhạy của "
            "cơ thể với thuốc."
        )
    },
    {
        "title": "10. NHỮNG LỖI CẦN TRÁNH KHI GIẢI BÀI TOÁN CÓ TIỆM CẬN",
        "lines": [
            "Lỗi 1. Không xác định đúng tập xác định phù hợp thực tế.",
            "Lỗi 2. Nhầm lẫn giữa các loại tiệm cận (đứng, ngang, xiên).",
            "Lỗi 3. Không phân tích ý nghĩa thực tế của các tiệm cận.",
            "Lỗi 4. Bỏ qua điều kiện thực tế khi tìm giá trị cực trị.",
            "Lỗi 5. Không kiểm tra tính hợp lý của kết quả với thực tế.",
            "Lỗi 6. Quên đơn vị đo lường trong các đại lượng thực tế."
        ],
        "narration": (
            "Có sáu lỗi thường gặp khi giải bài toán có tiệm cận. Thứ nhất, không "
            "xác định đúng tập xác định phù hợp thực tế. Thứ hai, nhầm lẫn giữa "
            "các loại tiệm cận như đứng, ngang, xiên. Thứ ba, không phân tích ý "
            "nghĩa thực tế của các tiệm cận. Thứ tư, bỏ qua điều kiện thực tế "
            "khi tìm giá trị cực trị. Thứ năm, không kiểm tra tính hợp lý của "
            "kết quả với thực tế. Thứ sáu, quên đơn vị đo lường trong các đại "
            "lượng thực tế. Các em cần lưu ý tránh những lỗi này."
        )
    },
    {
        "title": "TỔNG KẾT: CÁC DẠNG BÀI TOÁN THỰC TẾ CÓ TIỆM CẬN",
        "lines": [
            r"1. Bài toán nồng độ dung dịch: $y = \frac{k}{x + a}$",
            r"2. Bài toán hiệu suất phản ứng: $y = \frac{ax}{x + b}$",
            r"3. Bài toán chi phí trung bình: $y = a + \frac{b}{x} + \frac{c}{x^2}$",
            r"4. Bài toán tốc độ phản ứng (Michaelis-Menten): $y = \frac{ax}{x + b}$",
            r"5. Bài toán mức độ bão hòa (Hill): $y = \frac{ax^n}{x^n + b}$",
            r"6. Bài toán phân giải thuốc: $y = \frac{a}{1 + bx}$",
            r"7. Bài toán hiệu quả điều trị (Emax): $y = \frac{ax}{x + b}$",
            "Tự đánh giá: em đã nắm vững cách giải các dạng bài trên chưa?"
        ],
        "narration": (
            "Bài học hôm nay đã giới thiệu các dạng bài toán thực tế có tiệm cận. "
            "Thứ nhất, bài toán nồng độ dung dịch có dạng y bằng k chia cho x "
            "cộng a. Thứ hai, bài toán hiệu suất phản ứng có dạng y bằng a x "
            "chia cho x cộng b. Thứ ba, bài toán chi phí trung bình có dạng "
            "y bằng a cộng b chia cho x cộng c chia cho x bình. Thứ tư, bài "
            "toán tốc độ phản ứng Michaelis-Menten có dạng y bằng a x chia "
            "cho x cộng b. Thứ năm, bài toán mức độ bão hòa Hill có dạng "
            "y bằng a x mũ n chia cho x mũ n cộng b. Thứ sáu, bài toán phân "
            "giải thuốc có dạng y bằng a chia cho một cộng b x. Thứ bảy, bài "
            "toán hiệu quả điều trị Emax có dạng y bằng a x chia cho x cộng b. "
            "Các em hãy tự đánh giá xem đã nắm vững cách giải các dạng bài trên chưa?"
        )
    },
    {
        "title": "BÀI TẬP TỰ LUYỆN",
        "lines": [
            r"Bài 1. Nồng độ thuốc trong máu: $C(t) = \frac{D}{V(1 + kt)}$, với D = 500mg, V = 5L, k = 0.2/h.",
            "Tìm tiệm cận và thời gian để nồng độ giảm còn 10%?",
            r"Bài 2. Hiệu quả điều trị theo thời gian: $E(t) = \frac{100t}{t + 2}$ (phần trăm).",
            "Tìm tiệm cận và thời gian để đạt 80% hiệu quả?",
            r"Bài 3. Chi phí sản xuất x sản phẩm: $C(x) = 2000x + 100000 + \frac{50000}{x}$ (đồng).",
            "Tìm tiệm cận và sản lượng tối ưu để chi phí trung bình thấp nhất?"
        ],
        "narration": (
            "Cuối cùng, thầy giao ba bài tập tự luyện cho các em. Bài thứ nhất: "
            "Nồng độ thuốc trong máu được mô tả bởi hàm số C(t) bằng D chia "
            "cho V nhân một cộng k t, với D bằng năm trăm miligram, V bằng "
            "năm lít, k bằng không chấm hai trên giờ. Tìm tiệm cận và thời "
            "gian để nồng độ giảm còn mười phần trăm. Bài thứ hai: Hiệu quả "
            "điều trị theo thời gian được mô tả bởi hàm số E(t) bằng một trăm "
            "t chia cho t cộng hai phần trăm. Tìm tiệm cận và thời gian để "
            "đạt tám mươi phần trăm hiệu quả. Bài thứ ba: Chi phí sản xuất "
            "x sản phẩm được mô tả bởi hàm số C(x) bằng hai nghìn x cộng một "
            "trăm nghìn cộng năm mươi nghìn chia cho x đồng. Tìm tiệm cận và "
            "sản lượng tối ưu để chi phí trung bình thấp nhất. Các em hãy "
            "làm bài tập và chuẩn bị cho tiết luyện tập."
        )
    },
    {
        "title": "KẾT THÚC BÀI HỌC",
        "lines": [
            "Hôm nay chúng ta đã học:",
            "• Cách nhận biết và giải các bài toán thực tế có tiệm cận.",
            "• Phương pháp thiết lập hàm số từ mô hình thực tế.",
            "• Cách xác định và phân tích ý nghĩa thực tế của các tiệm cận.",
            "• Áp dụng vào nhiều lĩnh vực: hóa học, sinh học, y học, kinh tế...",
            "• Tránh các lỗi thường gặp khi giải bài toán có tiệm cận.",
            "Bài về nhà: Làm 3 bài tập tự luyện và chuẩn bị cho tiết luyện tập.",
            "Cảm ơn các em đã theo dõi!",
            "Nguyễn Văn Sang"
        ],
        "narration": (
            "Hôm nay chúng ta đã học về cách nhận biết và giải các bài toán thực "
            "tế có tiệm cận. Phương pháp thiết lập hàm số từ mô hình thực tế. "
            "Cách xác định và phân tích ý nghĩa thực tế của các tiệm cận. Áp dụng "
            "vào nhiều lĩnh vực như hóa học, sinh học, y học, kinh tế và nhiều "
            "lĩnh vực khác. Và tránh các lỗi thường gặp khi giải bài toán có "
            "tiệm cận. Bài về nhà là làm ba bài tập tự luyện và chuẩn bị cho "
            "tiết luyện tập. Cảm ơn các em đã theo dõi bài học của Nguyễn Văn Sang. "
            "Chúc các em học tốt!"
        )
    }
]

# ================================================================
# HÀM XỬ LÝ ÂM THANH
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
    return ",".join(f"atempo={v:.9f}" for v in factors)


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

            if (
                not destination.exists()
                or destination.stat().st_size < 500
            ):
                raise RuntimeError("Âm thanh rỗng hoặc chưa hoàn chỉnh.")

            if audio_duration(destination) <= 0:
                raise RuntimeError("Thời lượng âm thanh không hợp lệ.")

            return

        except Exception as exc:
            last_error = exc
            print(
                f"Lỗi giọng đọc tạm thời, lần {attempt + 1}: {exc}",
                flush=True
            )
            await asyncio.sleep(2 + 2 * attempt)

    raise RuntimeError(
        "Không tạo được giọng nam. "
        "Kiểm tra Internet rồi chạy lại ô Colab."
    ) from last_error


async def prepare_audio():
    original_lengths = []

    for index, slide in enumerate(SLIDES):
        mp3 = AUDIO_DIR / f"original_{index:02d}.mp3"
        cache_file = AUDIO_DIR / f"original_{index:02d}.txt"
        cache_key = VOICE + "\n" + VOICE_RATE + "\n" + slide["narration"]

        cached = (
            mp3.exists()
            and cache_file.exists()
            and cache_file.read_text(encoding="utf-8") == cache_key
        )

        if cached:
            try:
                cached = audio_duration(mp3) > 0
            except Exception:
                cached = False

        if not cached:
            print(
                f"Tạo giọng nam: {index + 1}/{len(SLIDES)}",
                flush=True
            )
            await synthesize(slide["narration"], mp3)
            cache_file.write_text(cache_key, encoding="utf-8")

        original_lengths.append(audio_duration(mp3))

    overhead = len(SLIDES) * (
        ENTER_TIME + AFTER_AUDIO_TIME + EXIT_TIME
    )
    # Bỏ ép thời lượng 10 phút để giữ tốc độ chuẩn tự nhiên
    speed = 1.0

    print(
        f"Tổng lời đọc gốc: {sum(original_lengths):.1f} giây",
        flush=True
    )
    print(
        f"Hệ số điều chỉnh tốc độ: {speed:.3f} (giữ nguyên tốc độ chuẩn)",
        flush=True
    )

    lengths = []

    for index, original_length in enumerate(original_lengths):
        source = AUDIO_DIR / f"original_{index:02d}.mp3"
        destination = AUDIO_DIR / f"voice_{index:02d}.wav"
        desired_length = original_length / speed

        filters = (
            atempo_filter(speed)
            + f",apad,atrim=duration={desired_length:.9f}"
        )

        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(source),
                "-vn",
                "-af", filters,
                "-ar", "48000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                str(destination)
            ],
            check=True
        )

        lengths.append(audio_duration(destination))

    TIMING_FILE.write_text(
        json.dumps(
            {
                "durations": lengths,
                "voice": VOICE,
                "target_seconds": TARGET_SECONDS,
                "speed_factor": speed
            },
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    (BASE / "kich_ban_duong_tiem_can.json").write_text(
        json.dumps(SLIDES, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    transcript_parts = []
    for i, slide in enumerate(SLIDES, start=1):
        transcript_parts.append(
            f"{i:02d}. {slide['title']}\n\n"
            + "\n".join(slide["lines"])
            + "\n\nLỜI ĐỌC:\n"
            + slide["narration"]
        )

    (BASE / "kich_ban_loi_doc.txt").write_text(
        "\n\n" + ("\n\n" + "=" * 65 + "\n\n").join(transcript_parts),
        encoding="utf-8"
    )

    print("Đã tạo xong âm thanh và kịch bản.", flush=True)


# ================================================================
# HÀM XỬ LÝ ĐỒ THỊ VÀ VĂN BẢN
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


# ================================================================
# SCENE CHÍNH
# ================================================================

class DuongTiemCanThucTe(Scene):
    def construct(self):
        if not TIMING_FILE.exists():
            raise RuntimeError(
                "Chưa tạo âm thanh. Chạy file Python với --prepare trước."
            )

        timing = json.loads(
            TIMING_FILE.read_text(encoding="utf-8")
        )
        durations = timing["durations"]

        if len(durations) != len(SLIDES):
            raise RuntimeError(
                "Số đoạn âm thanh không khớp. Chạy lại --prepare."
            )

        footer_bg = Rectangle(
            width=config.frame_width,
            height=0.53,
            stroke_width=0,
            fill_color="#0A1020",
            fill_opacity=1
        ).to_edge(DOWN, buff=0).set_z_index(100)

        footer_rule = Line(
            [-config.frame_width / 2, -3.47, 0],
            [config.frame_width / 2, -3.47, 0],
            stroke_width=1.5,
            color=ACCENT
        ).set_z_index(101)

        footer_name = make_text(
            "Nguyễn Văn Sang",
            size=22,
            color=FG
        ).move_to([0, -3.75, 0]).set_z_index(102)

        footer_subject = make_text(
            "TOÁN HỌC • ĐƯỜNG TIỆM CẬN",
            size=12,
            color=MUTED,
            max_width=4.7
        ).to_edge(LEFT, buff=0.30)
        footer_subject.set_y(-3.75).set_z_index(102)

        self.add(
            footer_bg,
            footer_rule,
            footer_name,
            footer_subject
        )

        for index, slide in enumerate(SLIDES):
            title = make_text(
                slide["title"],
                size=32,
                color=ACCENT,
                max_width=12.8
            ).move_to([0, 3.34, 0])

            header_rule = Line(
                [-6.65, 2.92, 0],
                [6.65, 2.92, 0],
                color="#3A4B64",
                stroke_width=1.2
            )

            counter = make_text(
                f"{index + 1:02d} / {len(SLIDES):02d}",
                size=17,
                color=MUTED
            ).to_edge(RIGHT, buff=0.32)
            counter.set_y(-3.75).set_z_index(103)

            has_graph = "graph" in slide
            body = make_body(slide["lines"], has_graph)
            content = VGroup(title, header_rule, body)

            self.add(counter)
            self.play(
                FadeIn(content, shift=UP * 0.08),
                run_time=ENTER_TIME
            )

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            if not audio_path.exists():
                raise RuntimeError(f"Thiếu âm thanh: {audio_path}")

            self.add_sound(str(audio_path))

            # Thanh tiến độ chạy trong thời gian thuyết minh.
            start = LEFT * 6.60 + DOWN * 3.25
            end = RIGHT * 6.60 + DOWN * 3.25

            track = Line(
                start, end,
                color="#26364A",
                stroke_width=3
            )
            progress = Line(
                start, end,
                color=ACCENT,
                stroke_width=3
            )

            self.add(track)
            self.play(
                Create(progress),
                run_time=durations[index],
                rate_func=linear
            )
            self.wait(AFTER_AUDIO_TIME)

            self.play(
                FadeOut(content, shift=UP * 0.05),
                FadeOut(track),
                FadeOut(progress),
                FadeOut(counter),
                run_time=EXIT_TIME
            )


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
    else:
        print(
            "Cách chạy:\n"
            "1. python duong_tiem_can_toan_thuc_te.py --prepare\n"
            "2. manim -qm --fps 24 duong_tiem_can_toan_thuc_te.py "
            "DuongTiemCanThucTe"
        )
'''

SCRIPT.write_text(SOURCE, encoding="utf-8")

# Kiểm tra cú pháp trước khi tạo giọng đọc.
compile(SOURCE, str(SCRIPT), "exec")

print("\nBƯỚC 2/4: Tạo giọng nam và căn thời lượng...")
run_command([
    sys.executable,
    str(SCRIPT),
    "--prepare"
])

print("\nBƯỚC 3/4: Dựng video Manim 720p...")
print("Thầy giữ Colab kết nối đến khi có thông báo hoàn tất.")
print("Thời gian dựng phụ thuộc tài nguyên Colab được cấp.")

MEDIA_DIR = WORK / "media"

run_command([
    sys.executable, "-m", "manim",
    "-qm",
    "--fps", "24",
    "--disable_caching",
    "--media_dir", str(MEDIA_DIR),
    "-o", "Duong_Tiem_Can_Toan_Thuc_Te_Thay_Sang",
    str(SCRIPT),
    "DuongTiemCanThucTe"
])

candidates = [
    path
    for path in MEDIA_DIR.rglob("*.mp4")
    if "partial_movie_files" not in str(path)
]

if not candidates:
    raise FileNotFoundError(
        "Chưa tìm thấy video hoàn chỉnh. "
        "Hãy kiểm tra log Manim ở trên."
    )

VIDEO_PATH = candidates[0]

import json
timing = json.loads(
    (WORK / "timing.json").read_text(encoding="utf-8")
)
duration_seconds = sum(timing["durations"])
minutes = int(duration_seconds // 60)
seconds = duration_seconds - minutes * 60

print("\nBƯỚC 4/4: HOÀN TẤT!")
print(f"Video: {VIDEO_PATH}")
print(f"Thời lượng: {minutes:02d}:{seconds:05.2f}")
print(f"Dung lượng: {VIDEO_PATH.stat().st_size / 1024**2:.1f} MB")

import ipywidgets as widgets
from IPython.display import display
from google.colab import files

print("\n------------------------------------------------------")
print("BẤM VÀO ĐÂY NẾU TRÌNH DUYỆT CHẶN TẢI XUỐNG:")

video_button = widgets.Button(
    description="Tải video MP4",
    button_style="success",
    layout=widgets.Layout(width="180px")
)

source_button = widgets.Button(
    description="Tải mã nguồn (.py)",
    button_style="info",
    layout=widgets.Layout(width="190px")
)

transcript_button = widgets.Button(
    description="Tải kịch bản lời đọc",
    layout=widgets.Layout(width="200px")
)

video_button.on_click(
    lambda _: files.download(str(VIDEO_PATH))
)

source_button.on_click(
    lambda _: files.download(str(SCRIPT))
)

transcript_button.on_click(
    lambda _: files.download(str(WORK / "kich_ban_loi_doc.txt"))
)

display(widgets.HBox([
    video_button,
    source_button,
    transcript_button
]))

print("\nĐang gửi yêu cầu tải video về máy...")
print("Nếu trình duyệt chặn tải tự động, thầy bấm nút 'Tải video MP4'.")
files.download(str(VIDEO_PATH))
