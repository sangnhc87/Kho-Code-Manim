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

WORK = Path("/content/tiem_can_thuc_te_nang_cao")
WORK.mkdir(parents=True, exist_ok=True)
SCRIPT = WORK / "tiem_can_thuc_te_nang_cao.py"

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
VOICE_RATE = "+0%"
TARGET_SECONDS = 600.0

ENTER_TIME = 0.5
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

# Công thức dùng Text Unicode, không cần MathTex/LaTeX.
# Trong đồ thị:
# - Đường màu xanh: đồ thị hàm số.
# - Nét đứt màu vàng/hồng: đường tiệm cận.
# - Vòng tròn rỗng: điểm không thuộc đồ thị.
#
# asymptotes:
# ["v", x0, nhãn]       : x = x0
# ["h", y0, nhãn]       : y = y0
# ["s", a, b, nhãn]     : y = ax + b

SLIDES = [
    {
        "title": "BÀI TOÁN THỰC TẾ HAY - LẠ - KHÓ",
        "lines": [
            "Chủ đề: ĐƯỜNG TIỆM CẬN (Mức độ Vận dụng cao).",
            "Mục tiêu 1. Tìm ẩn số $A, B$ dựa vào tiệm cận.",
            "Mục tiêu 2. Bài toán mô hình bão hòa (dân số, nồng độ).",
            "Mục tiêu 3. Phân tích tiệm cận xiên trong chi phí.",
            "Chuẩn bị giấy nháp, bút để cùng giải các bài toán khó!"
        ],
        "narration": "Chào các em. Hôm nay chúng ta sẽ tiếp tục chủ đề đường tiệm cận, nhưng ở mức độ vận dụng cao. Bài học tập trung vào các dạng toán thực tế hay, lạ và khó, nơi các em phải đi tìm ẩn số A, B dựa vào các dữ kiện về trạng thái bão hòa, ổn định, hoặc phân tích chi phí qua tiệm cận xiên. Các em hãy chuẩn bị giấy bút để cùng chinh phục nhé!"
    },
    {
        "title": "1. MÔ HÌNH HỮU TỶ: TRẠNG THÁI ỔN ĐỊNH",
        "lines": [
            r"Dạng thường gặp: $f(t) = \frac{A \cdot t + B}{C \cdot t + D}$",
            r"Biến số $t$: Thời gian ($t \ge 0$).",
            r"Trạng thái ban đầu: $t = 0 \implies f(0) = \frac{B}{D}$.",
            r"Khi $t \to +\infty$, đồ thị có TIỆM CẬN NGANG $y = \frac{A}{C}$.",
            "Ý nghĩa: Trạng thái ỔN ĐỊNH, BÃO HÒA sau thời gian dài.",
            r"Chìa khóa: 'Cuối cùng', 'Giới hạn tối đa', 'Ổn định mức...' $\implies$ TCN."
        ],
        "graph": {
            "func": "logistic_like",
            "intervals": [[0, 20]],
            "range": [0, 20, 0, 10],
            "asymptotes": [["h", 8, "$y = A/C$"]],
            "caption": "Trạng thái bão hòa: TCN $y = A/C$"
        },
        "narration": "Mô hình thực tế đầu tiên rất hay gặp là hàm phân thức bậc nhất. Với biến số thời gian t lớn hơn hoặc bằng không. Trạng thái ban đầu luôn ứng với t bằng không. Khi thời gian tiến ra vô cực, đồ thị sẽ có đường tiệm cận ngang y bằng A chia C. Trong thực tế, tiệm cận ngang này mang ý nghĩa là trạng thái ổn định, hoặc bão hòa của hệ thống sau một thời gian dài. Khi đề bài có cụm từ 'cuối cùng', 'tối đa', hay 'ổn định', các em phải nghĩ ngay đến việc tìm giới hạn khi t tới cộng vô cực."
    },
    {
        "title": "VÍ DỤ 1: TÌM 2 ẨN $A, B$ TRONG MÔ HÌNH DÂN SỐ",
        "lines": [
            r"Dân số một thị trấn mô hình bởi: $P(t) = \frac{A \cdot t + B}{t + 2}$",
            "( $t$ là số năm kể từ 2024, $P$ tính bằng nghìn người).",
            "Biết năm 2024, dân số là 4 nghìn người.",
            "Người ta dự báo, sau thời gian dài, dân số sẽ ỔN ĐỊNH",
            "ở mức tối đa là 15 nghìn người.",
            "Hãy tìm giá trị của $A$ và $B$."
        ],
        "narration": "Hãy xem ví dụ đầu tiên, tìm hai ẩn A và B trong mô hình dân số. Hàm số được cho là P bằng A t cộng B chia cho t cộng hai. Biết rằng ban đầu, tức năm hai ngàn không trăm hai mươi tư, dân số là bốn nghìn người. Và dự báo sau thời gian rất dài, dân số sẽ ổn định ở mức mười lăm nghìn người. Dữ kiện bài toán ẩn chứa chính xác hai phương trình để chúng ta giải tìm A và B."
    },
    {
        "title": "LỜI GIẢI VÍ DỤ 1",
        "lines": [
            "1. Ban đầu (năm 2024) ứng với $t = 0$.",
            r"Ta có: $P(0) = \frac{A(0) + B}{0 + 2} = \frac{B}{2}$.",
            r"Mà $P(0) = 4 \implies \frac{B}{2} = 4 \implies B = 8$.",
            r"2. Trạng thái 'ổn định sau thời gian dài' là TCN khi $t \to +\infty$.",
            r"Giới hạn: $\lim_{t \to +\infty} P(t) = \lim_{t \to +\infty} \frac{A \cdot t + 8}{t + 2} = A$.",
            r"Theo giả thiết, dân số bão hòa là 15 $\implies A = 15$.",
            r"Vậy $A = 15, B = 8$ và hàm số là: $P(t) = \frac{15t + 8}{t + 2}$."
        ],
        "graph": {
            "func": "population",
            "intervals": [[0, 20]],
            "range": [0, 20, 0, 20],
            "asymptotes": [["h", 15, "$P = 15$"]],
            "caption": "Dân số xuất phát từ 4, bão hòa tại 15"
        },
        "narration": "Bước một, khai thác dữ kiện ban đầu tại t bằng không. Thay t bằng không vào hàm số, ta được P tại không bằng B phần hai. Mà giả thiết cho P không bằng bốn, nên ta giải ngay được B bằng tám. Bước hai, khai thác dữ kiện bão hòa. Khi thời gian dài vô hạn, giới hạn của P khi t dần đến vô cực chính là hệ số của t ở tử chia cho mẫu, tức là bằng A. Mà dân số ổn định ở mười lăm nghìn, nên A bằng mười lăm. Ta đã tìm được A bằng mười lăm, B bằng tám rất nhanh gọn."
    },
    {
        "title": "VÍ DỤ 2: NỒNG ĐỘ THUỐC (BÀI TOÁN LẠ)",
        "lines": [
            "Nồng độ một loại thuốc trong máu được tính bởi:",
            r"$C(t) = \frac{A \cdot t}{t^2 + B}$ ($mg/L$, $t$ là số giờ sau khi tiêm).",
            "Biết rằng sau 2 giờ tiêm, nồng độ đạt MỨC CAO NHẤT là $5 mg/L$.",
            "Hỏi sau thời gian rất dài, nồng độ thuốc bằng bao nhiêu?",
            "Và tìm hai thông số $A, B$."
        ],
        "narration": "Ví dụ hai là một bài toán rất lạ về nồng độ thuốc. Hàm số là một phân thức với tử bậc một, mẫu bậc hai. Dữ kiện cho biết sau hai giờ, nồng độ đạt đỉnh lớn nhất là 5 miligam trên lít. Bài yêu cầu tìm nồng độ sau thời gian rất dài và tìm hai thông số A, B. Dạng này không chỉ đòi hỏi kiến thức về tiệm cận mà còn phải dùng đạo hàm để xử lý điểm cực đại."
    },
    {
        "title": "LỜI GIẢI VÍ DỤ 2 (PHẦN 1: TIỆM CẬN)",
        "lines": [
            r"1. Sau thời gian rất dài, ta xét giới hạn khi $t \to +\infty$.",
            r"$\lim_{t \to +\infty} C(t) = \lim_{t \to +\infty} \frac{A \cdot t}{t^2 + B} = 0$.",
            "Bậc của tử (1) nhỏ hơn bậc của mẫu (2).",
            r"$\implies$ Đồ thị có tiệm cận ngang $C = 0$.",
            "Ý nghĩa: Sau thời gian dài, thuốc sẽ bị đào thải hết,",
            "nồng độ trong máu sẽ giảm dần về $0$."
        ],
        "narration": "Trước tiên, trả lời câu hỏi sau thời gian dài nồng độ thuốc là bao nhiêu. Ta đi tính giới hạn của C t khi t tiến ra cộng vô cực. Vì bậc của tử là bậc một, bé hơn bậc của mẫu là bậc hai, nên giới hạn này bằng không. Trục hoành chính là tiệm cận ngang. Ý nghĩa thực tế rất rõ ràng: sau thời gian dài, cơ thể đào thải hết thuốc nên nồng độ trong máu sẽ tiến dần về mức không."
    },
    {
        "title": "LỜI GIẢI VÍ DỤ 2 (PHẦN 2: TÌM $A, B$)",
        "lines": [
            r"2. Tại $t = 2$, nồng độ là $5 \implies C(2) = 5$.",
            r"$\implies \frac{2A}{4 + B} = 5 \implies 2A = 20 + 5B$ (Phương trình 1).",
            r"3. Đạt TỐI ĐA tại $t = 2 \implies C'(2) = 0$.",
            r"Ta có $C'(t) = \frac{A(t^2 + B) - At(2t)}{(t^2 + B)^2} = \frac{AB - At^2}{(t^2 + B)^2}$.",
            r"Thay $t = 2$: $AB - 4A = 0 \implies A(B - 4) = 0$.",
            r"Vì thuốc có nồng độ nên $A > 0 \implies B = 4$.",
            r"Thay $B = 4$ vào (1): $2A = 20 + 20 \implies A = 20$."
        ],
        "graph": {
            "func": "drug",
            "intervals": [[0, 15]],
            "range": [0, 15, 0, 7],
            "asymptotes": [["h", 0, "$C = 0$"]],
            "points": [[2, 5, "Max(2, 5)"]],
            "caption": "$C(t) = 20t/(t^2+4)$"
        },
        "narration": "Bây giờ đi tìm A và B. Ta có nồng độ tại t bằng hai là năm. Thay vào hàm số ta được phương trình: hai A bằng hai mươi cộng năm B. Để xử lý dữ kiện cao nhất, ta tính đạo hàm và cho đạo hàm tại t bằng hai bằng không. Đạo hàm ra A nhân B trừ A nhân t bình phương ở trên tử. Cho t bằng hai, tử số bằng A nhân B trừ bốn A bằng không. Vì A dương nên B bắt buộc bằng bốn. Thế vào trên, ta tính được A bằng hai mươi. Bài toán giải quyết trọn vẹn sự kết hợp giữa cực trị và tiệm cận. Đồ thị cho thấy nồng độ vọt lên ở hai giờ rồi từ từ thải dần về không."
    },
    {
        "title": "VÍ DỤ 3: TIỆM CẬN XIÊN TRONG KINH TẾ",
        "lines": [
            r"Chi phí sản xuất $x$ sản phẩm là: $C(x) = A \cdot x^2 + 50x + B$.",
            r"Chi phí trung bình để sản xuất 1 SP là: $\overline{C}(x) = \frac{C(x)}{x}$.",
            "Biết chi phí cố định (khi không sản xuất) là 1000 USD.",
            "Khi sản xuất số lượng rất lớn, chi phí trung bình",
            "có xu hướng bám sát đường thẳng $y = 2x + 50$.",
            "Hãy tìm hàm chi phí $C(x)$."
        ],
        "narration": "Ví dụ ba là bài toán về chi phí trong kinh tế, ứng dụng của tiệm cận xiên. Đề cho tổng chi phí C x là một hàm bậc hai. Chi phí trung bình được tính bằng tổng chi phí chia cho x. Biết chi phí cố định khi không sản xuất là một ngàn đô la. Và khi sản xuất số lượng cực lớn, chi phí trung bình bám sát một đường thẳng y bằng hai x cộng năm mươi. Các em cần tìm hàm chi phí ban đầu."
    },
    {
        "title": "LỜI GIẢI VÍ DỤ 3",
        "lines": [
            "1. Chi phí cố định tại $x = 0$ là 1000.",
            r"$\implies C(0) = B = 1000$.",
            "2. Lập hàm chi phí trung bình:",
            r"$\overline{C}(x) = \frac{A \cdot x^2 + 50x + 1000}{x} = Ax + 50 + \frac{1000}{x}$.",
            r"3. Khi $x \to +\infty$, phần $\frac{1000}{x} \to 0$.",
            r"Đồ thị $\overline{C}(x)$ bám sát tiệm cận xiên $y = Ax + 50$.",
            "Theo giả thiết, đường TCX này là $y = 2x + 50$.",
            r"$\implies A = 2$.",
            "Vậy $C(x) = 2x^2 + 50x + 1000$."
        ],
        "graph": {
            "func": "cost",
            "intervals": [[0, 50]],
            "range": [0, 50, 0, 200],
            "asymptotes": [["s", 2, 50, "$y = 2x + 50$"]],
            "caption": "Chi phí bám sát tiệm cận xiên"
        },
        "narration": "Để giải, trước hết dựa vào chi phí cố định tại x bằng không, ta thay vào hàm số C sẽ ra ngay B bằng một ngàn. Tiếp theo, lập hàm chi phí trung bình bằng cách chia toàn bộ cho x, ta được A x cộng năm mươi cộng một ngàn phần x. Khi số lượng x cực lớn, phân số một ngàn phần x sẽ tiến về không. Hàm số bám sát vào đường tiệm cận xiên y bằng A x cộng năm mươi. So sánh với giả thiết y bằng hai x cộng năm mươi, ta tìm được A bằng hai. Rất thú vị phải không nào."
    },
    {
        "title": "MÔ HÌNH LOGISTIC (DÀNH CHO HỌC SINH GIỎI)",
        "lines": [
            "Một mô hình sinh trưởng thực tế hơn:",
            r"$P(t) = \frac{M}{1 + B \cdot e^{-kt}}$. (Dân số, tin đồn...)",
            "Đặc điểm:",
            r"$\lim_{t \to +\infty} e^{-kt} = 0 \implies \lim_{t \to +\infty} P(t) = M$.",
            "Đồ thị có tiệm cận ngang $y = M$.",
            "M là 'Sức chứa tối đa' của môi trường sinh thái.",
            "Dù ban đầu tăng nhanh, sau cùng vẫn bão hòa ở mức $M$."
        ],
        "narration": "Dành cho các học sinh khá giỏi, sách giáo khoa mới giới thiệu mô hình tăng trưởng logistic. Dạng phương trình là P bằng M chia cho một cộng B nhân e mũ âm k t. Khi thời gian t trôi đi rất lâu, cụm e mũ âm k t sẽ dần về không. Lúc này, giới hạn của P bằng đúng chữ M ở trên tử. Đường tiệm cận ngang y bằng M mang ý nghĩa là sức chứa tối đa của môi trường. Sinh vật không thể tăng trưởng mãi mãi mà luôn bị giới hạn bởi tiệm cận ngang này."
    },
    {
        "title": "BÀI TẬP TỰ LUYỆN: MÔ HÌNH LOGISTIC",
        "lines": [
            "Số người biết một tin đồn sau $t$ ngày là:",
            r"$N(t) = \frac{5000}{1 + A \cdot e^{-0.5t}}$.",
            "1. Ban đầu ($t=0$) có $100$ người biết. Tìm $A$.",
            "2. Số người biết tối đa là bao nhiêu? (TCN)",
            "--------------------",
            "ĐÁP ÁN NHANH:",
            r"1. $N(0) = \frac{5000}{1 + A} = 100 \implies 1 + A = 50 \implies A = 49$.",
            r"2. Khi $t \to +\infty$, $e^{-0.5t} \to 0 \implies N \to 5000$."
        ],
        "graph": {
            "func": "logistic_real",
            "intervals": [[0, 25]],
            "range": [0, 25, 0, 6000],
            "asymptotes": [["h", 5000, "$N = 5000$"]],
            "caption": "Mô hình Logistic chữ S"
        },
        "narration": "Bài tập tự luyện cuối cùng. Số người biết tin đồn tính bởi hàm logistic. Ban đầu có một trăm người biết, tìm A. Và số người biết tối đa là bao nhiêu? Hãy dừng video tự giải nhé. Đáp án như sau: thay t bằng không, phương trình có mẫu là một cộng A, giải ra A bằng bốn mươi chín. Số người tối đa chính là giới hạn khi t ra vô cực, bằng năm ngàn người. Đồ thị hàm logistic uốn lượn hình chữ S rất đặc trưng, ứng dụng trong lan truyền thông tin, dịch bệnh hay marketing."
    },
    {
        "title": "TỔNG KẾT BÀI HỌC",
        "lines": [
            "Các từ khóa dịch ra ngôn ngữ giới hạn:",
            "1. 'Trạng thái ổn định', 'Mức bão hòa', 'Tối đa':",
            r"$\implies$ Tìm giới hạn khi $t \to +\infty$ (Tiệm cận ngang).",
            "2. 'Dài hạn', 'Chi phí cận biên ở quy mô lớn':",
            r"$\implies$ Tìm tiệm cận xiên (với hàm phân thức bậc 2/bậc 1).",
            "3. 'Hiện tại', 'Ban đầu':",
            r"$\implies$ Thay $t = 0$.",
            "Chúc các em làm chủ hoàn toàn điểm 9, 10 với bài toán tiệm cận!"
        ],
        "narration": "Chúng ta đã đi qua các bài toán rất hay và lạ. Tổng kết lại bí kíp dịch từ khóa thực tế sang ngôn ngữ toán học: Nếu đề nói ổn định, bão hòa, tối đa sau thời gian dài, hãy đi tìm tiệm cận ngang bằng giới hạn ở vô cực. Nếu nói chi phí dài hạn hay quy mô lớn đối với hàm phân thức bậc hai trên bậc một, đó là tiệm cận xiên. Nếu nói ban đầu, hiện tại, hãy thay t bằng không. Chúc các em học thật tốt và đạt điểm mười với dạng toán này. Thầy Nguyễn Văn Sang chào các em."
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

            if (
                not destination.exists()
                or destination.stat().st_size < 500
            ):
                raise RuntimeError("Tệp âm thanh chưa hoàn chỉnh.")

            if audio_duration(destination) <= 0:
                raise RuntimeError("Thời lượng âm thanh không hợp lệ.")

            return

        except Exception as exc:
            last_error = exc
            print(
                f"Tạo giọng chưa thành công, lần {attempt + 1}: {exc}",
                flush=True
            )
            await asyncio.sleep(2 + attempt * 2)

    raise RuntimeError(
        "Không tạo được giọng NamMinh. "
        "Kiểm tra Internet rồi chạy lại ô Colab."
    ) from last_error


async def prepare_audio():
    original_lengths = []

    for index, slide in enumerate(SLIDES):
        mp3 = AUDIO_DIR / f"original_{index:02d}.mp3"
        cache_file = AUDIO_DIR / f"original_{index:02d}.txt"
        cache_key = (
            VOICE + "\n" + VOICE_RATE + "\n" + slide["narration"]
        )

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
                f"Tạo giọng nam: trang {index + 1}/{len(SLIDES)}",
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

    if not 0.75 <= speed <= 1.35:
        print(
            "Lưu ý: tốc độ đọc được điều chỉnh tương đối nhiều "
            "để video đạt khoảng 10 phút.",
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

    (BASE / "kich_ban_tiem_can.json").write_text(
        json.dumps(SLIDES, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    transcript = []
    for index, slide in enumerate(SLIDES, start=1):
        transcript.append(
            f"{index:02d}. {slide['title']}\n\n"
            + "\n".join(slide["lines"])
            + "\n\nLỜI ĐỌC:\n"
            + slide["narration"]
        )

    (BASE / "kich_ban_loi_doc.txt").write_text(
        ("\n\n" + "=" * 65 + "\n\n").join(transcript),
        encoding="utf-8"
    )

    print("Đã tạo xong âm thanh và kịch bản.", flush=True)


# ================================================================
# HÀM SỐ VÀ VẼ ĐỒ THỊ
# ================================================================

def evaluate_function(name, x):
    if name == "logistic_like":
        return (8.0 * x + 2.0) / (x + 1.0)
    if name == "population":
        return (15.0 * x + 8.0) / (x + 2.0)
    if name == "drug":
        return (20.0 * x) / (x**2 + 4.0)
    if name == "cost":
        return 2.0 * x + 50.0 + 1000.0 / x
    if name == "logistic_real":
        return 5000.0 / (1.0 + 49.0 * np.exp(-0.5 * x))
    raise ValueError(f"Chưa khai báo hàm: {name}")


def line_rectangle_intersections(a, b, c, bounds):
    """
    Tìm đoạn đường ax + by = c nằm trong cửa sổ đồ thị.
    """
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
        if not any(
            math.hypot(
                point[0] - other[0],
                point[1] - other[1]
            ) < eps
            for other in unique
        ):
            unique.append(point)

    if len(unique) < 2:
        return None

    pairs = [
        (p, q)
        for index, p in enumerate(unique)
        for q in unique[index + 1:]
    ]

    return max(
        pairs,
        key=lambda pair: (
            (pair[0][0] - pair[1][0]) ** 2
            + (pair[0][1] - pair[1][1]) ** 2
        )
    )


def function_curves(axes, spec):
    """
    Lấy mẫu dày và tách từng nhánh.
    Không nối xuyên qua điểm gián đoạn hay vùng ngoài khung.
    """
    xmin, xmax, ymin, ymax = spec["range"]
    curves = VGroup()

    for left, right in spec["intervals"]:
        left = max(left, xmin)
        right = min(right, xmax)

        if left >= right:
            continue

        xs = np.linspace(left, right, 1800)

        with np.errstate(
            divide="ignore",
            invalid="ignore",
            over="ignore"
        ):
            ys = evaluate_function(spec["func"], xs)

        valid = (
            np.isfinite(ys)
            & (ys >= ymin)
            & (ys <= ymax)
        )

        # Tìm các đoạn chỉ số liên tiếp hợp lệ.
        indices = np.flatnonzero(valid)
        if len(indices) < 2:
            continue

        breaks = np.where(np.diff(indices) > 1)[0] + 1
        runs = np.split(indices, breaks)

        for run in runs:
            if len(run) < 2:
                continue

            points = [
                axes.c2p(float(xs[i]), float(ys[i]))
                for i in run
            ]

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

    x_step = 2 if xmax - xmin > 10 else 1
    y_step = 2 if ymax - ymin > 10 else 1

    axes = Axes(
        x_range=[xmin, xmax, x_step],
        y_range=[ymin, ymax, y_step],
        x_length=5.25,
        y_length=4.60,
        axis_config={
            "color": "#AAB8CC",
            "stroke_width": 1.6,
            "include_ticks": True,
            "include_numbers": False,
            "tip_width": 0.11,
            "tip_height": 0.11
        }
    ).move_to([3.72, 0.0, 0])

    graph = VGroup()
    grid = VGroup()

    first_x = math.ceil(xmin / x_step) * x_step
    first_y = math.ceil(ymin / y_step) * y_step

    for x in np.arange(first_x, xmax + 0.001, x_step):
        grid.add(Line(
            axes.c2p(x, ymin),
            axes.c2p(x, ymax),
            color="#2A394E",
            stroke_width=0.7
        ))

    for y in np.arange(first_y, ymax + 0.001, y_step):
        grid.add(Line(
            axes.c2p(xmin, y),
            axes.c2p(xmax, y),
            color="#2A394E",
            stroke_width=0.7
        ))

    graph.add(grid, axes)

    tick_labels = VGroup()

    for x in np.arange(first_x, xmax + 0.001, x_step):
        if abs(x) > 1e-8 and xmin < x < xmax:
            label = make_text(
                f"{x:g}",
                size=14,
                color=MUTED
            )
            label.next_to(axes.c2p(x, 0), DOWN, buff=0.08)
            tick_labels.add(label)

    for y in np.arange(first_y, ymax + 0.001, y_step):
        if abs(y) > 1e-8 and ymin < y < ymax:
            label = make_text(
                f"{y:g}",
                size=14,
                color=MUTED
            )
            label.next_to(axes.c2p(0, y), LEFT, buff=0.08)
            tick_labels.add(label)

    graph.add(tick_labels)

    x_label = make_text("x", size=20, color=MUTED)
    x_label.next_to(axes.c2p(xmax, 0), RIGHT, buff=0.06)

    y_label = make_text("y", size=20, color=MUTED)
    y_label.next_to(axes.c2p(0, ymax), UP, buff=0.06)

    graph.add(x_label, y_label)

    legend_items = []

    for index, asymptote in enumerate(spec.get("asymptotes", [])):
        kind = asymptote[0]
        color = YELLOW if index % 2 == 0 else PINK

        if kind == "v":
            value = asymptote[1]
            label_content = asymptote[2]
            ends = line_rectangle_intersections(
                1, 0, value, spec["range"]
            )

        elif kind == "h":
            value = asymptote[1]
            label_content = asymptote[2]
            ends = line_rectangle_intersections(
                0, 1, value, spec["range"]
            )

        else:
            a, b, label_content = asymptote[1:]
            ends = line_rectangle_intersections(
                -a, 1, b, spec["range"]
            )

        if ends is not None:
            p, q = ends
            graph.add(DashedLine(
                axes.c2p(*p),
                axes.c2p(*q),
                dash_length=0.12,
                dashed_ratio=0.57,
                stroke_width=2.8,
                color=color
            ))

        legend_items.append(
            make_text(label_content, size=20, color=color)
        )

    graph.add(function_curves(axes, spec))

    for x, y, label_content in spec.get("points", []):
        point = Dot(
            axes.c2p(x, y),
            radius=0.055,
            color=FG
        )
        label = make_text(
            label_content,
            size=18,
            color=FG
        ).next_to(point, UR, buff=0.08)

        label.add_background_rectangle(
            color=BG,
            opacity=0.85,
            buff=0.035
        )
        graph.add(point, label)

    if legend_items:
        legend = VGroup(*legend_items).arrange(
            RIGHT,
            buff=0.38
        )
        if legend.width > 5.5:
            legend.scale_to_fit_width(5.5)
        legend.move_to([3.72, 2.67, 0])
        graph.add(legend)

    caption = make_text(
        spec.get("caption", ""),
        size=21,
        color=GREEN,
        max_width=5.65
    ).move_to([3.68, -2.94, 0])

    graph.add(caption)
    return graph


# ================================================================
# SCENE CHÍNH
# ================================================================

class DuongTiemCanToan12(Scene):
    def construct(self):
        if not TIMING_FILE.exists():
            raise RuntimeError(
                "Thiếu âm thanh. Chạy file với --prepare trước."
            )

        timing = json.loads(
            TIMING_FILE.read_text(encoding="utf-8")
        )
        durations = timing["durations"]

        if len(durations) != len(SLIDES):
            raise RuntimeError(
                "Âm thanh không khớp kịch bản. Hãy chạy lại --prepare."
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
            "Thầy Nguyễn Văn Sang",
            size=22,
            color=FG
        ).move_to([0, -3.75, 0]).set_z_index(102)

        footer_subject = make_text(
            "TOÁN 12 • ĐƯỜNG TIỆM CẬN",
            size=14,
            color=MUTED,
            max_width=4.5
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
                stroke_width=1.2,
                color="#3A4B64"
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

            if has_graph:
                divider = Line(
                    [0.05, -2.70, 0],
                    [0.05, 2.60, 0],
                    stroke_width=1,
                    color="#304056"
                )
                content.add(divider, build_graph(slide["graph"]))

            self.add(counter)

            self.play(
                FadeIn(content, shift=UP * 0.08),
                run_time=ENTER_TIME
            )

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            if not audio_path.exists():
                raise RuntimeError(f"Thiếu tệp: {audio_path}")

            self.add_sound(str(audio_path))

            start = LEFT * 6.60 + DOWN * 3.25
            end = RIGHT * 6.60 + DOWN * 3.25

            track = Line(
                start,
                end,
                color="#26364A",
                stroke_width=3
            )
            progress = Line(
                start,
                end,
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
            self.clear()


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
    else:
        print(
            "Cách chạy:\n"
            "1. python duong_tiem_can_toan_12.py --prepare\n"
            "2. manim -qm --fps 24 duong_tiem_can_toan_12.py "
            "DuongTiemCanToan12"
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
    "-o", "Duong_Tiem_Can_Thay_Nguyen_Van_Sang",
    str(SCRIPT),
    "DuongTiemCanToan12"
])

candidates = [
    path
    for path in MEDIA_DIR.rglob(
        "Duong_Tiem_Can_Thay_Nguyen_Van_Sang.mp4"
    )
    if "partial_movie_files" not in str(path)
]

if not candidates:
    raise FileNotFoundError(
        "Chưa tìm thấy video hoàn chỉnh. "
        "Thầy xem thông báo lỗi Manim phía trên."
    )

VIDEO_PATH = max(candidates, key=lambda p: p.stat().st_mtime)

duration_result = subprocess.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(VIDEO_PATH)
    ],
    capture_output=True,
    text=True,
    check=True
)

duration_seconds = float(duration_result.stdout.strip())
minutes = int(duration_seconds // 60)
seconds = duration_seconds - minutes * 60

print("\nBƯỚC 4/4: HOÀN TẤT!")
print(f"Video: {VIDEO_PATH}")
print(f"Thời lượng: {minutes:02d}:{seconds:05.2f}")
print(f"Dung lượng: {VIDEO_PATH.stat().st_size / 1024**2:.1f} MB")
print(f"Mã nguồn Python: {SCRIPT}")

# ================================================================
# NÚT TẢI KẾT QUẢ
# ================================================================

from IPython.display import display
import ipywidgets as widgets
from google.colab import files

video_button = widgets.Button(
    description="Tải video MP4",
    button_style="success",
    layout=widgets.Layout(width="190px")
)

source_button = widgets.Button(
    description="Tải mã nguồn .py",
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
