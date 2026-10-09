import sys
import subprocess
from pathlib import Path

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[LỖI] Lệnh thất bại: {' '.join(str(c) for c in command)}\n", flush=True)
        raise e

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

WORK = Path("/content/bai_toan_thuc_te_bat_phuong_trinh")
WORK.mkdir(parents=True, exist_ok=True)
SCRIPT = WORK / "bai_toan_thuc_te_bat_phuong_trinh.py"

SOURCE = r'''
from manim import *
import asyncio
import edge_tts
import json
import math
import subprocess
import sys
import textwrap
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

config.background_color = BG

# Quy ước đồ thị:
# [a, b, c, dấu] nghĩa là ax + by dấu c.
# Miền tô xanh là giao của TẤT CẢ các bất phương trình.
# Nét liền: bất phương trình có dấu bằng.
# Nét đứt: bất phương trình không có dấu bằng.

SLIDES = [
    {
        "title": "BÀI TOÁN THỰC TẾ: BẤT PHƯƠNG TRÌNH HAI ẨN",
        "lines": [
            "Bài tiếp theo: Ứng dụng thực tiễn của bất phương trình hai ẩn",
            "Mục tiêu 1. Nhận biết các bài toán thực tế.",
            "Mục tiêu 2. Đặt ẩn và thiết lập ràng buộc.",
            "Mục tiêu 3. Lập hệ bất phương trình từ điều kiện thực tế.",
            "Mục tiêu 4. Tìm phương án tối ưu.",
            "Chuẩn bị: giấy nháp, bút, máy tính."
        ],
        "narration": (
            "Chào các em. Ở bài trước, chúng ta đã học về hệ bất phương trình "
            "bậc nhất hai ẩn và cách biểu diễn miền nghiệm. Hôm nay, chúng ta "
            "sẽ áp dụng kiến thức này vào giải các bài toán thực tế. Bài học có "
            "bốn mục tiêu: nhận biết bài toán thực tế; đặt ẩn và thiết lập ràng buộc; "
            "lập hệ bất phương trình từ điều kiện thực tế; và tìm phương án tối ưu. "
            "Các em hãy chuẩn bị giấy nháp, bút và máy tính. Khi gặp phần luyện tập, "
            "hãy dừng video, tự giải trước rồi đối chiếu với lời giải."
        )
    },
    {
        "title": "1. CÁC BƯỚC GIẢI BÀI TOÁN THỰC TẾ",
        "lines": [
            "Bước 1. Đọc kỹ đề bài và xác định yêu cầu.",
            "Bước 2. Đặt ẩn số phù hợp với đại lượng cần tìm.",
            "Bước 3. Thiết lập các ràng buộc từ điều kiện thực tế.",
            "Bước 4. Xác định hàm mục tiêu cần tối ưu.",
            "Bước 5. Lập hệ bất phương trình và tìm miền nghiệm.",
            "Bước 6. Xác định giá trị lớn nhất/nhỏ nhất của hàm mục tiêu.",
            "Bước 7. Kết luận theo yêu cầu của bài toán."
        ],
        "narration": (
            "Để giải một bài toán thực tế bằng bất phương trình hai ẩn, ta thực hiện "
            "theo bảy bước. Đầu tiên, đọc kỹ đề bài và xác định yêu cầu. Thứ hai, đặt "
            "ẩn số phù hợp với đại lượng cần tìm. Thứ ba, thiết lập các ràng buộc từ "
            "điều kiện thực tế. Thứ tư, xác định hàm mục tiêu cần tối ưu. Thứ năm, lập "
            "hệ bất phương trình và tìm miền nghiệm. Thứ sáu, xác định giá trị lớn nhất "
            "hoặc nhỏ nhất của hàm mục tiêu. Cuối cùng, kết luận theo yêu cầu của bài toán."
        )
    },
    {
        "title": "2. VÍ DỤ 1: BÀI TOÁN VỀ CHẾ BIẾN THỰC PHẨM",
        "lines": [
            "Một xưởng có 300g bột, 100g đường, 200g bơ.",
            "Mỗi bánh loại A cần 10g bột, 5g đường, 5g bơ.",
            "Mỗi bánh loại B cần 15g bột, 5g đường, 10g bơ.",
            "Lợi nhuận mỗi bánh A: 2000đ, mỗi bánh B: 3000đ.",
            "Hỏi nên sản xuất mỗi loại bao nhiêu để lợi nhuận lớn nhất?"
        ],
        "narration": (
            "Xét ví dụ đầu tiên: Một xưởng có 300 gam bột, 100 gam đường và 200 gam bơ. "
            "Mỗi bánh loại A cần 10 gam bột, 5 gam đường và 5 gam bơ. Mỗi bánh loại B "
            "cần 15 gam bột, 5 gam đường và 10 gam bơ. Lợi nhuận mỗi bánh loại A là 2000 "
            "đồng, mỗi bánh loại B là 3000 đồng. Hỏi nên sản xuất mỗi loại bao nhiêu để "
            "lợi nhuận lớn nhất?"
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số bánh loại A và B (x, y nguyên không âm).",
            r"Ràng buộc về bột: $10x + 15y \le 300$",
            r"Ràng buộc về đường: $5x + 5y \le 100$",
            r"Ràng buộc về bơ: $5x + 10y \le 200$",
            r"Hàm mục tiêu: $P = 2000x + 3000y$ (cần tìm max)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số bánh loại A và B, với x và y là các số nguyên "
            "không âm. Ràng buộc về bột: 10x cộng 15y không vượt quá 300. Ràng buộc về "
            "đường: 5x cộng 5y không vượt quá 100. Ràng buộc về bơ: 5x cộng 10y không "
            "vượt quá 200. Hàm mục tiêu là P bằng 2000x cộng 3000y, cần tìm giá trị lớn nhất."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$10x + 15y \le 300 \implies 2x + 3y \le 60$",
            r"$5x + 5y \le 100 \implies x + y \le 20$",
            r"$5x + 10y \le 200 \implies x + 2y \le 40$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [2, 3, 60, "<="],
                [1, 1, 20, "<="],
                [1, 2, 40, "<="]
            ],
            "range": [-2, 25, -2, 25],
            "points": [
                [0, 0, "O"], [20, 0, "A"],
                [0, 20, "B"], [10, 10, "C"],
                [0, 20, "D"]
            ],
            "lattice": True,
            "caption": "Miền nghiệm bài toán chế biến thực phẩm"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, hai x cộng "
            "ba y không vượt quá sáu mươi, x cộng y không vượt quá hai mươi, và x cộng "
            "hai y không vượt quá bốn mươi. Ta sẽ biểu diễn miền nghiệm của hệ này trên "
            "mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$2x + 3y = 60$ và $x + y = 20$",
            r"Giải hệ: $x = 0, y = 20 \implies (0; 20)$",
            r"$x + y = 20$ và $x + 2y = 40$",
            r"Giải hệ: $x = 0, y = 20 \implies (0; 20)$",
            r"$2x + 3y = 60$ và $x + 2y = 40$",
            r"Giải hệ: $x = 0, y = 20 \implies (0; 20)$",
            r"Các đỉnh: $O(0; 0), A(20; 0), (0; 20)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm bằng cách giải các hệ phương trình tạo bởi "
            "các đường biên. Tuy nhiên, sau khi giải các hệ phương trình, ta thấy các "
            "đỉnh thực sự là gốc tọa độ không, không; điểm hai mươi, không; và điểm "
            "không, hai mươi."
        )
    },
    {
        "title": "VÍ DỤ 1 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $P = 2000x + 3000y$",
            r"Tại $O(0; 0): P = 0$",
            r"Tại $A(20; 0): P = 2000 \times 20 = 40000$",
            r"Tại $(0; 20): P = 3000 \times 20 = 60000$",
            "Lợi nhuận lớn nhất: 60000 đồng khi sản xuất 0 bánh A và 20 bánh B."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu P bằng 2000x cộng 3000y tại các đỉnh. Tại "
            "gốc tọa độ, P bằng không. Tại điểm hai mươi, không, P bằng bốn mươi nghìn. "
            "Tại điểm không, hai mươi, P bằng sáu mươi nghìn. Vậy lợi nhuận lớn nhất "
            "là sáu mươi nghìn đồng khi sản xuất không bánh loại A và hai mươi bánh loại B."
        )
    },
    {
        "title": "3. VÍ DỤ 2: BÀI TOÁN VỀ DINH DƯỠNG",
        "lines": [
            "Một người cần ít nhất 12 đơn vị protein và 9 đơn vị vitamin mỗi ngày.",
            "Thực phẩm X chứa 2 đơn vị protein và 1 đơn vị vitamin mỗi 100g.",
            "Thực phẩm Y chứa 1 đơn vị protein và 3 đơn vị vitamin mỗi 100g.",
            "Giá X: 15000đ/100g, giá Y: 12000đ/100g.",
            "Hỏi nên mua mỗi loại bao nhiêu để đủ dinh dưỡng với chi phí thấp nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ hai về dinh dưỡng: Một người cần ít nhất mười hai đơn vị "
            "protein và chín đơn vị vitamin mỗi ngày. Thực phẩm X chứa hai đơn vị "
            "protein và một đơn vị vitamin mỗi trăm gam. Thực phẩm Y chứa một đơn vị "
            "protein và ba đơn vị vitamin mỗi trăm gam. Giá X là mười lăm nghìn đồng "
            "mỗi trăm gam, giá Y là mười hai nghìn đồng mỗi trăm gam. Hỏi nên mua mỗi "
            "loại bao nhiêu để đủ dinh dưỡng với chi phí thấp nhất?"
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số 100g thực phẩm X và Y (x, y không âm).",
            r"Ràng buộc protein: $2x + y \ge 12$",
            r"Ràng buộc vitamin: $x + 3y \ge 9$",
            r"Hàm mục tiêu: $C = 15000x + 12000y$ (cần tìm min)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số trăm gam thực phẩm X và Y, với x và y không âm. "
            "Ràng buộc về protein: hai x cộng y không nhỏ hơn mười hai. Ràng buộc về "
            "vitamin: x cộng ba y không nhỏ hơn chín. Hàm mục tiêu là C bằng mười lăm "
            "nghìn x cộng mười hai nghìn y, cần tìm giá trị nhỏ nhất."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$2x + y \ge 12$",
            r"$x + 3y \ge 9$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [2, 1, 12, ">="],
                [1, 3, 9, ">="]
            ],
            "range": [-2, 15, -2, 15],
            "points": [
                [0, 12, "A"], [6, 0, "B"],
                [0, 3, "C"], [9, 0, "D"],
                [4.5, 3, "E"]
            ],
            "caption": "Miền nghiệm bài toán dinh dưỡng"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, hai x cộng "
            "y không nhỏ hơn mười hai, và x cộng ba y không nhỏ hơn chín. Ta biểu diễn "
            "miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$2x + y = 12$ và $x + 3y = 9$",
            r"Giải hệ: $x = 4.5, y = 3 \implies (4.5; 3)$",
            r"Giao với trục: $(0; 12), (6; 0), (0; 3), (9; 0)$",
            r"Miền nghiệm không bị chặn, nhưng có đỉnh $(4.5; 3)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm. Giao điểm của hai đường biên hai x cộng "
            "y bằng mười hai và x cộng ba y bằng chín là điểm bốn chấm năm, ba. Các "
            "giao điểm với trục tọa độ là không, mười hai; sáu, không; không, ba; "
            "và chín, không. Miền nghiệm không bị chặn, nhưng có đỉnh bốn chấm năm, ba."
        )
    },
    {
        "title": "VÍ DỤ 2 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $C = 15000x + 12000y$",
            r"Tại $(4.5; 3): C = 15000 \times 4.5 + 12000 \times 3 = 103500$",
            r"Tại $(0; 12): C = 144000$",
            r"Tại $(6; 0): C = 90000$ (không thỏa mãn ràng buộc vitamin)",
            r"Tại $(0; 3): C = 36000$ (không thỏa mãn ràng buộc protein)",
            "Chi phí thấp nhất: 103500 đồng khi mua 4.5 đơn vị X và 3 đơn vị Y."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu C bằng mười lăm nghìn x cộng mười hai nghìn "
            "y tại các điểm. Tại điểm bốn chấm năm, ba, C bằng một trăm lẻ ba nghìn "
            "năm trăm. Tại điểm không, mười hai, C bằng một trăm bốn mươi tư nghìn. "
            "Tại điểm sáu, không, C bằng chín mươi nghìn nhưng không thỏa mãn ràng buộc "
            "vitamin. Tại điểm không, ba, C bằng ba mươi sáu nghìn nhưng không thỏa mãn "
            "ràng buộc protein. Vậy chi phí thấp nhất là một trăm lẻ ba nghìn năm trăm "
            "đồng khi mua bốn chấm năm đơn vị thực phẩm X và ba đơn vị thực phẩm Y."
        )
    },
    {
        "title": "4. VÍ DỤ 3: BÀI TOÁN VỀ VẬN CHUYỂN",
        "lines": [
            "Cần vận chuyển 120 tấn hàng từ kho A đến kho B.",
            "Có hai loại xe: xe tải nhỏ chở 2 tấn, chi phí 300000đ/chuyến.",
            "Xe tải lớn chở 5 tấn, chi phí 600000đ/chuyến.",
            "Số xe nhỏ không vượt quá 2 lần số xe lớn.",
            "Hỏi cần bao nhiêu xe mỗi loại để chi phí thấp nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ ba về vận chuyển: Cần vận chuyển một trăm hai mươi tấn hàng "
            "từ kho A đến kho B. Có hai loại xe: xe tải nhỏ chở hai tấn, chi phí ba "
            "trăm nghìn đồng mỗi chuyến. Xe tải lớn chở năm tấn, chi phí sáu trăm "
            "nghìn đồng mỗi chuyến. Số xe nhỏ không vượt quá hai lần số xe lớn. Hỏi "
            "cần bao nhiêu xe mỗi loại để chi phí thấp nhất?"
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số xe nhỏ và xe lớn (x, y nguyên không âm).",
            r"Ràng buộc về khối lượng: $2x + 5y \ge 120$",
            r"Ràng buộc về số lượng: $x \le 2y$",
            r"Hàm mục tiêu: $C = 300000x + 600000y$ (cần tìm min)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số xe nhỏ và xe lớn, với x và y là các số nguyên "
            "không âm. Ràng buộc về khối lượng: hai x cộng năm y không nhỏ hơn một trăm "
            "hai mươi. Ràng buộc về số lượng: x không vượt quá hai y. Hàm mục tiêu là "
            "C bằng ba trăm nghìn x cộng sáu trăm nghìn y, cần tìm giá trị nhỏ nhất."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$2x + 5y \ge 120$",
            r"$x \le 2y$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [2, 5, 120, ">="],
                [1, -2, 0, "<="]
            ],
            "range": [-5, 40, -5, 40],
            "points": [
                [0, 24, "A"], [60, 0, "B"],
                [0, 0, "O"], [40, 20, "C"]
            ],
            "lattice": True,
            "caption": "Miền nghiệm bài toán vận chuyển"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, hai x cộng "
            "năm y không nhỏ hơn một trăm hai mươi, và x không vượt quá hai y. Ta biểu "
            "diễn miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$2x + 5y = 120$ và $x = 2y$",
            r"Thay $x = 2y$ vào: $2(2y) + 5y = 120 \implies 9y = 120 \implies y = 40/3$",
            "Vì y phải nguyên, ta xét các điểm gần đó.",
            r"Các đỉnh khả thi: $(24; 12), (25; 12), (26; 12)$..."
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm. Giao điểm của hai đường biên hai x cộng "
            "năm y bằng một trăm hai mươi và x bằng hai y. Thay x bằng hai y vào, ta "
            "được chín y bằng một trăm hai mươi, suy ra y bằng bốn mươi phần ba. Vì "
            "y phải là số nguyên, ta xét các điểm gần đó. Các đỉnh khả thi bao gồm hai "
            "mươi bốn, mười hai; hai mươi lăm, mười hai; hai mươi sáu, mười hai và "
            "các điểm nguyên khác trong miền nghiệm."
        )
    },
    {
        "title": "VÍ DỤ 3 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $C = 300000x + 600000y$",
            r"Tại $(24; 12): C = 300000 \times 24 + 600000 \times 12 = 14400000$",
            r"Tại $(25; 12): C = 14700000$",
            r"Tại $(26; 12): C = 15000000$",
            r"Tại $(20; 16): C = 15600000$",
            "Chi phí thấp nhất: 14400000 đồng khi dùng 24 xe nhỏ và 12 xe lớn."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu C bằng ba trăm nghìn x cộng sáu trăm nghìn "
            "y tại các điểm nguyên trong miền nghiệm. Tại điểm hai mươi bốn, mười hai, "
            "C bằng mười bốn triệu bốn trăm nghìn. Tại điểm hai mươi lăm, mười hai, "
            "C bằng mười bốn triệu bảy trăm nghìn. Tại điểm hai mươi sáu, mười hai, "
            "C bằng mười năm triệu. Tại điểm hai mươi, mười sáu, C bằng mười năm triệu "
            "sáu trăm nghìn. Vậy chi phí thấp nhất là mười bốn triệu bốn trăm nghìn "
            "đồng khi dùng hai mươi bốn xe nhỏ và mười hai xe lớn."
        )
    },
    {
        "title": "5. VÍ DỤ 4: BÀI TOÁN VỀ SẢN XUẤT NÔNG NGHIỆP",
        "lines": [
            "Một nông dân có 10 hecta đất trồng lúa và ngô.",
            "Lúa cần 2 ngày công/ha, 100kg phân/ha, cho 5 tấn/ha.",
            "Ngô cần 3 ngày công/ha, 150kg phân/ha, cho 7 tấn/ha.",
            "Có 24 ngày công và 1200kg phân.",
            "Hỏi trồng mỗi loại bao nhiêu để thu hoạch lớn nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ tư về sản xuất nông nghiệp: Một nông dân có mười hecta đất "
            "để trồng lúa và ngô. Lúa cần hai ngày công mỗi hecta, một trăm kilogram "
            "phân mỗi hecta, cho năng suất năm tấn mỗi hecta. Ngô cần ba ngày công "
            "mỗi hecta, một trăm năm mươi kilogram phân mỗi hecta, cho năng suất bảy "
            "tấn mỗi hecta. Có hai mươi bốn ngày công và một nghìn hai trăm kilogram "
            "phân. Hỏi trồng mỗi loại bao nhiêu để thu hoạch lớn nhất?"
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số hecta trồng lúa và ngô (x, y không âm).",
            r"Ràng buộc về đất: $x + y \le 10$",
            r"Ràng buộc về ngày công: $2x + 3y \le 24$",
            r"Ràng buộc về phân: $100x + 150y \le 1200 \implies 2x + 3y \le 24$",
            r"Hàm mục tiêu: $T = 5x + 7y$ (tấn, cần tìm max)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số hecta trồng lúa và ngô, với x và y không âm. "
            "Ràng buộc về đất: x cộng y không vượt quá mười. Ràng buộc về ngày công: "
            "hai x cộng ba y không vượt quá hai mươi bốn. Ràng buộc về phân: một trăm "
            "x cộng một trăm năm mươi y không vượt quá một nghìn hai trăm, tương đương "
            "với hai x cộng ba y không vượt quá hai mươi bốn. Hàm mục tiêu là T bằng "
            "năm x cộng bảy y tấn, cần tìm giá trị lớn nhất."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$x + y \le 10$",
            r"$2x + 3y \le 24$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 10, "<="],
                [2, 3, 24, "<="]
            ],
            "range": [-2, 15, -2, 15],
            "points": [
                [0, 0, "O"], [10, 0, "A"],
                [0, 8, "B"], [6, 4, "C"]
            ],
            "caption": "Miền nghiệm bài toán nông nghiệp"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, x cộng "
            "y không vượt quá mười, và hai x cộng ba y không vượt quá hai mươi bốn. "
            "Ta biểu diễn miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$x + y = 10$ và $2x + 3y = 24$",
            r"Giải hệ: $x = 6, y = 4 \implies (6; 4)$",
            r"Các đỉnh: $O(0; 0), A(10; 0), B(0; 8), C(6; 4)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm bằng cách giải hệ phương trình tạo bởi "
            "các đường biên. Giao điểm của x cộng y bằng mười và hai x cộng ba y bằng "
            "hai mươi bốn là điểm sáu, bốn. Các đỉnh khác là gốc tọa độ không, không; "
            "điểm mười, không; và điểm không, tám."
        )
    },
    {
        "title": "VÍ DỤ 4 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $T = 5x + 7y$ (tấn)",
            r"Tại $O(0; 0): T = 0$",
            r"Tại $A(10; 0): T = 50$",
            r"Tại $B(0; 8): T = 56$",
            r"Tại $C(6; 4): T = 5 \times 6 + 7 \times 4 = 58$",
            "Thu hoạch lớn nhất: 58 tấn khi trồng 6ha lúa và 4ha ngô."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu T bằng năm x cộng bảy y tấn tại các đỉnh. "
            "Tại gốc tọa độ, T bằng không. Tại điểm mười, không, T bằng năm mươi. "
            "Tại điểm không, tám, T bằng năm mươi sáu. Tại điểm sáu, bốn, T bằng "
            "năm nhân sáu cộng bảy nhân bốn bằng năm mươi tám. Vậy thu hoạch lớn "
            "nhất là năm mươi tám tấn khi trồng sáu hecta lúa và bốn hecta ngô."
        )
    },
    {
        "title": "6. VÍ DỤ 5: BÀI TOÁN VỀ ĐẦU TƯ TÀI CHÍNH",
        "lines": [
            "Một người có 1 tỷ đồng để đầu tư vào hai loại cổ phiếu.",
            "Cổ phiếu A: rủi ro thấp, lợi nhuận 8%/năm.",
            "Cổ phiếu B: rủi ro cao, lợi nhuận 12%/năm.",
            "Không đầu tư quá 600 triệu vào B.",
            "Tỷ lệ đầu tư vào B không vượt quá 2 lần đầu tư vào A.",
            "Hỏi nên đầu tư bao nhiêu vào mỗi loại để lợi nhuận lớn nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ năm về đầu tư tài chính: Một người có một tỷ đồng để đầu tư "
            "vào hai loại cổ phiếu. Cổ phiếu A có rủi ro thấp, lợi nhuận tám phần trăm "
            "mỗi năm. Cổ phiếu B có rủi ro cao, lợi nhuận mười hai phần trăm mỗi năm. "
            "Không đầu tư quá sáu trăm triệu vào B. Tỷ lệ đầu tư vào B không vượt quá "
            "hai lần đầu tư vào A. Hỏi nên đầu tư bao nhiêu vào mỗi loại để lợi nhuận "
            "lớn nhất?"
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số tiền (triệu đồng) đầu tư vào A và B.",
            r"Ràng buộc về tổng tiền: $x + y \le 1000$",
            r"Ràng buộc về cổ phiếu B: $y \le 600$",
            r"Ràng buộc về tỷ lệ: $y \le 2x$",
            r"Hàm mục tiêu: $L = 0.08x + 0.12y$ (triệu đồng/năm, cần tìm max)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số tiền triệu đồng đầu tư vào cổ phiếu A và B. "
            "Ràng buộc về tổng tiền: x cộng y không vượt quá một nghìn. Ràng buộc về "
            "cổ phiếu B: y không vượt quá sáu trăm. Ràng buộc về tỷ lệ: y không vượt "
            "quá hai x. Hàm mục tiêu là L bằng không chấm không tám x cộng không chấm "
            "một hai y triệu đồng mỗi năm, cần tìm giá trị lớn nhất."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$x + y \le 1000$",
            r"$y \le 600$",
            r"$y \le 2x$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 1000, "<="],
                [0, 1, 600, "<="],
                [2, -1, 0, ">="]
            ],
            "range": [-100, 1100, -100, 1100],
            "points": [
                [0, 0, "O"], [1000, 0, "A"],
                [0, 600, "B"], [200, 600, "C"],
                [400, 600, "D"]
            ],
            "caption": "Miền nghiệm bài toán đầu tư"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, x cộng "
            "y không vượt quá một nghìn, y không vượt quá sáu trăm, và y không vượt "
            "quá hai x. Ta biểu diễn miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$x + y = 1000$ và $y = 600 \implies x = 400$",
            r"$y = 600$ và $y = 2x \implies x = 300$",
            r"$x + y = 1000$ và $y = 2x \implies 3x = 1000 \implies x = 1000/3$",
            r"Các đỉnh: $O(0; 0), A(1000; 0), (400; 600), (300; 600), (1000/3; 2000/3)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm. Giao điểm của x cộng y bằng một nghìn "
            "và y bằng sáu trăm là điểm bốn trăm, sáu trăm. Giao điểm của y bằng "
            "sáu trăm và y bằng hai x là điểm ba trăm, sáu trăm. Giao điểm của "
            "x cộng y bằng một nghìn và y bằng hai x là điểm một nghìn phần ba, "
            "hai nghìn phần ba. Các đỉnh khác là gốc tọa độ và điểm một nghìn, không."
        )
    },
    {
        "title": "VÍ DỤ 5 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $L = 0.08x + 0.12y$ (triệu đồng/năm)",
            r"Tại $O(0; 0): L = 0$",
            r"Tại $A(1000; 0): L = 80$",
            r"Tại $(400; 600): L = 0.08 \times 400 + 0.12 \times 600 = 104$",
            r"Tại $(300; 600): L = 96$",
            r"Tại $(1000/3; 2000/3): L = 106.67$",
            "Lợi nhuận lớn nhất: 106.67 triệu/năm khi đầu tư 333.33 triệu vào A và 666.67 triệu vào B."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu L bằng không chấm không tám x cộng không "
            "chấm một hai y triệu đồng mỗi năm tại các đỉnh. Tại gốc tọa độ, L bằng "
            "không. Tại điểm một nghìn, không, L bằng tám mươi. Tại điểm bốn trăm, "
            "sáu trăm, L bằng một trăm lẻ bốn. Tại điểm ba trăm, sáu trăm, L bằng "
            "chín mươi sáu. Tại điểm một nghìn phần ba, hai nghìn phần ba, L bằng "
            "một trăm lẻ sáu chấm sáu bảy. Vậy lợi nhuận lớn nhất là một trăm lẻ "
            "sáu chấm sáu bảy triệu đồng mỗi năm khi đầu tư ba trăm ba mươi ba "
            "chấm ba ba triệu vào cổ phiếu A và sáu trăm sáu mươi sáu chấm sáu "
            "bảy triệu vào cổ phiếu B."
        )
    },
    {
        "title": "7. VÍ DỤ 6: BÀI TOÁN VỀ PHA TRỘN HÓA CHẤT",
        "lines": [
            "Cần pha chế ít nhất 20 lít dung dịch với nồng độ chất X ít nhất 30%.",
            "Dung dịch A: 20% chất X, giá 50000đ/lít.",
            "Dung dịch B: 50% chất X, giá 80000đ/lít.",
            "Hỏi cần bao nhiêu lít mỗi loại để chi phí thấp nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ sáu về pha trộn hóa chất: Cần pha chế ít nhất hai mươi lít "
            "dung dịch với nồng độ chất X ít nhất ba mươi phần trăm. Dung dịch A có "
            "hai mươi phần trăm chất X, giá năm mươi nghìn đồng mỗi lít. Dung dịch B "
            "có năm mươi phần trăm chất X, giá tám mươi nghìn đồng mỗi lít. Hỏi cần "
            "bao nhiêu lít mỗi loại để chi phí thấp nhất?"
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): ĐẶT ẨN VÀ THIẾC LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số lít dung dịch A và B (x, y không âm).",
            r"Ràng buộc về thể tích: $x + y \ge 20$",
            r"Ràng buộc về nồng độ: $0.2x + 0.5y \ge 0.3(x + y)$",
            r"Rút gọn: $0.2x + 0.5y \ge 0.3x + 0.3y \implies 0.2y \ge 0.1x \implies y \ge 0.5x$",
            r"Hàm mục tiêu: $C = 50000x + 80000y$ (cần tìm min)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số lít dung dịch A và B, với x và y không âm. "
            "Ràng buộc về thể tích: x cộng y không nhỏ hơn hai mươi. Ràng buộc về "
            "nồng độ: không chấm hai x cộng không chấm năm y không nhỏ hơn không "
            "chấm ba nhân x cộng y. Rút gọn ta được y không nhỏ hơn không chấm năm x. "
            "Hàm mục tiêu là C bằng năm mươi nghìn x cộng tám mươi nghìn y, cần tìm "
            "giá trị nhỏ nhất."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$x + y \ge 20$",
            r"$y \ge 0.5x$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 20, ">="],
                [1, -2, 0, "<="]
            ],
            "range": [-5, 30, -5, 30],
            "points": [
                [0, 20, "A"], [20, 0, "B"],
                [0, 0, "O"], [40/3, 20/3, "C"]
            ],
            "caption": "Miền nghiệm bài toán pha trộn"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, x cộng "
            "y không nhỏ hơn hai mươi, và y không nhỏ hơn không chấm năm x. Ta biểu "
            "diễn miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$x + y = 20$ và $y = 0.5x$",
            r"Thay vào: $x + 0.5x = 20 \implies 1.5x = 20 \implies x = 40/3, y = 20/3$",
            r"Các đỉnh: $A(0; 20), B(20; 0), C(40/3; 20/3)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm. Giao điểm của x cộng y bằng hai mươi "
            "và y bằng không chấm năm x. Thay vào ta được một chấm năm x bằng hai "
            "mươi, suy ra x bằng bốn mươi phần ba, y bằng hai mươi phần ba. Các "
            "đỉnh khác là điểm không, hai mươi và điểm hai mươi, không."
        )
    },
    {
        "title": "VÍ DỤ 6 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $C = 50000x + 80000y$",
            r"Tại $A(0; 20): C = 1600000$",
            "Tại $B(20; 0): C = 1000000$ (không thỏa mãn ràng buộc nồng độ)",
            r"Tại $C(40/3; 20/3): C = 50000 \times 40/3 + 80000 \times 20/3 = 1200000$",
            "Chi phí thấp nhất: 1200000 đồng khi dùng 40/3 lít A và 20/3 lít B."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu C bằng năm mươi nghìn x cộng tám mươi nghìn "
            "y tại các đỉnh. Tại điểm không, hai mươi, C bằng một triệu sáu trăm nghìn. "
            "Tại điểm hai mươi, không, C bằng một triệu nhưng không thỏa mãn ràng buộc "
            "nồng độ. Tại điểm bốn mươi phần ba, hai mươi phần ba, C bằng một triệu "
            "hai trăm nghìn. Vậy chi phí thấp nhất là một triệu hai trăm nghìn đồng "
            "khi dùng bốn mươi phần ba lít dung dịch A và hai mươi phần ba lít "
            "dung dịch B."
        )
    },
    {
        "title": "8. VÍ DỤ 7: BÀI TOÁN VỀ LẬP KẾ HOẠCH SẢN XUẤT",
        "lines": [
            "Một công ty sản xuất hai loại sản phẩm P và Q.",
            "P cần 2 giờ máy móc, 1 giờ lao động, lợi nhuận 30000đ/đơn vị.",
            "Q cần 1 giờ máy móc, 3 giờ lao động, lợi nhuận 50000đ/đơn vị.",
            "Mỗi ngày có 10 giờ máy móc và 15 giờ lao động.",
            "Hỏi sản xuất mỗi loại bao nhiêu để lợi nhuận lớn nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ bảy về lập kế hoạch sản xuất: Một công ty sản xuất hai "
            "loại sản phẩm P và Q. Sản phẩm P cần hai giờ máy móc, một giờ lao động, "
            "lợi nhuận ba mươi nghìn đồng mỗi đơn vị. Sản phẩm Q cần một giờ máy móc, "
            "ba giờ lao động, lợi nhuận năm mươi nghìn đồng mỗi đơn vị. Mỗi ngày có "
            "mười giờ máy móc và mười lăm giờ lao động. Hỏi sản xuất mỗi loại bao "
            "nhiêu để lợi nhuận lớn nhất?"
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số đơn vị sản phẩm P và Q (x, y nguyên không âm).",
            r"Ràng buộc máy móc: $2x + y \le 10$",
            r"Ràng buộc lao động: $x + 3y \le 15$",
            r"Hàm mục tiêu: $L = 30000x + 50000y$ (cần tìm max)."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số đơn vị sản phẩm P và Q, với x và y là các "
            "số nguyên không âm. Ràng buộc máy móc: hai x cộng y không vượt quá mười. "
            "Ràng buộc lao động: x cộng ba y không vượt quá mười lăm. Hàm mục tiêu "
            "là L bằng ba mươi nghìn x cộng năm mươi nghìn y, cần tìm giá trị lớn nhất."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            r"Hệ: $x \ge 0; y \ge 0$",
            r"$2x + y \le 10$",
            r"$x + 3y \le 15$"
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [2, 1, 10, "<="],
                [1, 3, 15, "<="]
            ],
            "range": [-2, 12, -2, 12],
            "points": [
                [0, 0, "O"], [5, 0, "A"],
                [0, 5, "B"], [3, 4, "C"]
            ],
            "lattice": True,
            "caption": "Miền nghiệm bài toán sản xuất"
        },
        "narration": (
            "Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, hai x "
            "cộng y không vượt quá mười, và x cộng ba y không vượt quá mười lăm. "
            "Ta biểu diễn miền nghiệm của hệ này trên mặt phẳng tọa độ."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): TÌM CÁC ĐỈNH CỦA MIỀN NGHIỆM",
        "lines": [
            "Tìm giao điểm các đường biên:",
            r"$2x + y = 10$ và $x + 3y = 15$",
            r"Giải hệ: $x = 3, y = 4 \implies (3; 4)$",
            r"Các đỉnh: $O(0; 0), A(5; 0), B(0; 5), C(3; 4)$"
        ],
        "narration": (
            "Ta tìm các đỉnh của miền nghiệm bằng cách giải hệ phương trình tạo bởi "
            "các đường biên. Giao điểm của hai x cộng y bằng mười và x cộng ba y "
            "bằng mười lăm là điểm ba, bốn. Các đỉnh khác là gốc tọa độ không, không; "
            "điểm năm, không; và điểm không, năm."
        )
    },
    {
        "title": "VÍ DỤ 7 (TIẾP): TÍNH GIÁ TRỊ HÀM MỤC TIÊU",
        "lines": [
            r"Hàm mục tiêu: $L = 30000x + 50000y$",
            r"Tại $O(0; 0): L = 0$",
            r"Tại $A(5; 0): L = 150000$",
            r"Tại $B(0; 5): L = 250000$",
            r"Tại $C(3; 4): L = 30000 \times 3 + 50000 \times 4 = 290000$",
            "Lợi nhuận lớn nhất: 290000 đồng khi sản xuất 3 đơn vị P và 4 đơn vị Q."
        ],
        "narration": (
            "Ta tính giá trị hàm mục tiêu L bằng ba mươi nghìn x cộng năm mươi nghìn "
            "y tại các đỉnh. Tại gốc tọa độ, L bằng không. Tại điểm năm, không, "
            "L bằng một trăm năm mươi nghìn. Tại điểm không, năm, L bằng hai trăm "
            "năm mươi nghìn. Tại điểm ba, bốn, L bằng hai trăm chín mươi nghìn. "
            "Vậy lợi nhuận lớn nhất là hai trăm chín mươi nghìn đồng khi sản xuất "
            "ba đơn vị sản phẩm P và bốn đơn vị sản phẩm Q."
        )
    },
    {
        "title": "9. VÍ DỤ 8: BÀI TOÁN VỀ PHÂN BỔ NGUỒN LỰC",
        "lines": [
            "Một công ty có 12 nhân viên và 8 máy tính.",
            "Dự án X cần 2 nhân viên và 1 máy tính, hoàn thành trong 3 ngày.",
            "Dự án Y cần 1 nhân viên và 2 máy tính, hoàn thành trong 2 ngày.",
            "Hỏi nên thực hiện bao nhiêu dự án mỗi loại để hoàn thành sớm nhất?"
        ],
        "narration": (
            "Xét ví dụ thứ tám về phân bổ nguồn lực: Một công ty có mười hai nhân viên "
            "và tám máy tính. Dự án X cần hai nhân viên và một máy tính, hoàn thành "
            "trong ba ngày. Dự án Y cần một nhân viên và hai máy tính, hoàn thành "
            "trong hai ngày. Hỏi nên thực hiện bao nhiêu dự án mỗi loại để hoàn thành "
            "sớm nhất? Lưu ý rằng đây là bài toán tối thiểu hóa thời gian hoàn thành."
        )
    },
    {
        "title": "VÍ DỤ 8 (TIẾP): ĐẶT ẨN VÀ THIẾT LẬP RÀNG BUỘC",
        "lines": [
            "Gọi x, y lần lượt là số dự án X và Y (x, y nguyên không âm).",
            r"Ràng buộc nhân viên: $2x + y \le 12$",
            r"Ràng buộc máy tính: $x + 2y \le 8$",
            r"Thời gian hoàn thành: $T = \max(3x, 2y)$ (cần tìm min).",
            "Đây là bài toán tối ưu max-min, cần chuyển đổi."
        ],
        "narration": (
            "Ta đặt x và y lần lượt là số dự án X và Y, với x và y là các số nguyên "
            "không âm. Ràng buộc nhân viên: hai x cộng y không vượt quá mười hai. "
            "Ràng buộc máy tính: x cộng hai y không vượt quá tám. Thời gian hoàn "
            "thành là max của ba x và hai y, cần tìm giá trị nhỏ nhất. Đây là bài "
            "toán tối ưu max-min, cần chuyển đổi để giải bằng phương pháp đã học."
        )
    },
    {
        "title": "VÍ DỤ 8 (TIẾP): CHUYỂN ĐỔI BÀI TOÁN",
        "lines": [
            r"Đặt $t = \max(3x, 2y)$, cần tìm min $t$.",
            r"Tương đương với: $3x \le t$ và $2y \le t$.",
            r"Hệ: $x \ge 0; y \ge 0; t \ge 0$",
            r"$2x + y \le 12$",
            r"$x + 2y \le 8$",
            r"$3x \le t$",
            r"$2y \le t$"
        ],
        "narration": (
            "Ta đặt t bằng max của ba x và hai y, cần tìm giá trị nhỏ nhất của t. "
            "Điều này tương đương với ba x không vượt quá t và hai y không vượt "
            "quá t. Hệ bất phương trình gồm các điều kiện: x không âm, y không âm, "
            "t không âm, hai x cộng y không vượt quá mười hai, x cộng hai y không "
            "vượt quá tám, ba x không vượt quá t, và hai y không vượt quá t."
        )
    },
    {
        "title": "VÍ DỤ 8 (TIẾP): GIẢI HỆ BẤT PHƯƠNG TRÌNH",
        "lines": [
            "Với mỗi giá trị t cố định, tìm miền nghiệm (x,y).",
            "Tăng dần t đến khi miền nghiệm không rỗng.",
            "Hoặc giải bằng phương pháp thử các đỉnh.",
            r"Các đỉnh khả thi: $(0;0), (6;0), (0;4), (4;2)$",
            r"Tại $(4;2): 3 \times 4 = 12, 2 \times 2 = 4 \implies t = 12$"
        ],
        "narration": (
            "Với mỗi giá trị t cố định, ta tìm miền nghiệm x, y. Tăng dần t đến khi "
            "miền nghiệm không rỗng. Hoặc giải bằng phương pháp thử các đỉnh. Các "
            "đỉnh khả thi là không, không; sáu, không; không, bốn; và bốn, hai. "
            "Tại điểm bốn, hai: ba nhân bốn bằng mười hai, hai nhân hai bằng bốn, "
            "suy ra t bằng mười hai. Đây là giá trị nhỏ nhất có thể đạt được."
        )
    },
    {
        "title": "VÍ DỤ 8 (TIẾP): KẾT LUẬN",
        "lines": [
            "Thời gian hoàn thành sớm nhất: 12 ngày.",
            "Thực hiện 4 dự án X và 2 dự án Y.",
            r"Kiểm tra: $2 \times 4 + 2 = 10 \le 12$ (nhân viên)",
            r"$4 + 2 \times 2 = 8 \le 8$ (máy tính)",
            r"Dự án X hoàn thành trong $3 \times 4 = 12$ ngày.",
            r"Dự án Y hoàn thành trong $2 \times 2 = 4$ ngày.",
            r"Tổng thời gian: $\max(12, 4) = 12$ ngày."
        ],
        "narration": (
            "Thời gian hoàn thành sớm nhất là mười hai ngày. Thực hiện bốn dự án X "
            "và hai dự án Y. Kiểm tra ràng buộc: hai nhân bốn cộng hai bằng mười, "
            "không vượt quá mười hai nhân viên. Bốn cộng hai nhân hai bằng tám, "
            "bằng số máy tính có sẵn. Dự án X hoàn thành trong ba nhân bốn bằng "
            "mười hai ngày. Dự án Y hoàn thành trong hai nhân hai bằng bốn ngày. "
            "Tổng thời gian là max của mười hai và bốn bằng mười hai ngày."
        )
    },
    {
        "title": "10. NHỮNG LỖI CẦN TRÁNH KHI GIẢI BÀI TOÁN THỰC TẾ",
        "lines": [
            "Lỗi 1. Không đọc kỹ đề, đặt ẩn sai hoặc thiếu điều kiện.",
            "Lỗi 2. Thiết lập sai ràng buộc từ điều kiện thực tế.",
            "Lỗi 3. Nhầm lẫn giữa tìm max và min của hàm mục tiêu.",
            "Lỗi 4. Quên kiểm tra điều kiện nguyên khi cần thiết.",
            "Lỗi 5. Kết luận không phù hợp với yêu cầu thực tế của bài toán.",
            "Lỗi 6. Không kiểm tra lại các ràng buộc tại điểm tối ưu."
        ],
        "narration": (
            "Có sáu lỗi thường gặp khi giải bài toán thực tế. Thứ nhất, không đọc kỹ "
            "đề, đặt ẩn sai hoặc thiếu điều kiện. Thứ hai, thiết lập sai ràng buộc "
            "từ điều kiện thực tế. Thứ ba, nhầm lẫn giữa tìm giá trị lớn nhất và "
            "giá trị nhỏ nhất của hàm mục tiêu. Thứ tư, quên kiểm tra điều kiện "
            "nguyên khi cần thiết. Thứ năm, kết luận không phù hợp với yêu cầu "
            "thực tế của bài toán. Thứ sáu, không kiểm tra lại các ràng buộc tại "
            "điểm tối ưu. Các em cần lưu ý tránh những lỗi này."
        )
    },
    {
        "title": "TỔNG KẾT: CÁC DẠNG BÀI TOÁN THỰC TẾ",
        "lines": [
            "1. Bài toán sản xuất, kinh doanh: tối ưu lợi nhuận, chi phí.",
            "2. Bài toán dinh dưỡng: tối ưu khẩu phần ăn.",
            "3. Bài toán vận chuyển: tối ưu chi phí vận chuyển.",
            "4. Bài toán đầu tư: tối ưu lợi nhuận đầu tư.",
            "5. Bài toán phân bổ nguồn lực: tối ưu hiệu quả sử dụng.",
            "6. Bài toán pha trộn: tối ưu thành phần hỗn hợp.",
            "7. Bài toán lập kế hoạch: tối ưu thời gian, hiệu suất.",
            "Tự đánh giá: em đã nắm vững cách giải các dạng bài trên chưa?"
        ],
        "narration": (
            "Bài học hôm nay đã giới thiệu các dạng bài toán thực tế thường gặp. "
            "Thứ nhất, bài toán sản xuất, kinh doanh: tối ưu lợi nhuận, chi phí. "
            "Thứ hai, bài toán dinh dưỡng: tối ưu khẩu phần ăn. Thứ ba, bài toán "
            "vận chuyển: tối ưu chi phí vận chuyển. Thứ tư, bài toán đầu tư: tối "
            "ưu lợi nhuận đầu tư. Thứ năm, bài toán phân bổ nguồn lực: tối ưu "
            "hiệu quả sử dụng. Thứ sáu, bài toán pha trộn: tối ưu thành phần hỗn "
            "hợp. Thứ bảy, bài toán lập kế hoạch: tối ưu thời gian, hiệu suất. "
            "Các em hãy tự đánh giá xem đã nắm vững cách giải các dạng bài trên chưa?"
        )
    },
    {
        "title": "BÀI TẬP TỰ LUYỆN",
        "lines": [
            "Bài 1. Một cửa hàng có 50m vải và 30m lụa. May áo cần 2m vải, 1m lụa, lãi 50000đ.",
            "May váy cần 1m vải, 2m lụa, lãi 40000đ. Hỏi may mỗi loại bao nhiêu để lãi lớn nhất?",
            "Bài 2. Cần ít nhất 8g protein và 6g vitamin mỗi ngày. Thực phẩm X: 2g protein, 1g vitamin, 10000đ/100g.",
            "Thực phẩm Y: 1g protein, 3g vitamin, 8000đ/100g. Hỏi nên mua mỗi loại bao nhiêu để đủ dinh dưỡng với chi phí thấp nhất?",
            "Bài 3. Có 100 công nhân và 80 máy. Sản phẩm A cần 2 công nhân, 1 máy, hoàn thành trong 4 ngày.",
            "Sản phẩm B cần 1 công nhân, 2 máy, hoàn thành trong 3 ngày. Hỏi nên sản xuất mỗi loại bao nhiêu để hoàn thành sớm nhất?"
        ],
        "narration": (
            "Cuối cùng, thầy giao ba bài tập tự luyện cho các em. Bài thứ nhất: Một "
            "cửa hàng có năm mươi mét vải và ba mươi mét lụa. May áo cần hai mét "
            "vải, một mét lụa, lãi năm mươi nghìn đồng. May váy cần một mét vải, "
            "hai mét lụa, lãi bốn mươi nghìn đồng. Hỏi may mỗi loại bao nhiêu để "
            "lãi lớn nhất? Bài thứ hai: Cần ít nhất tám gam protein và sáu gam "
            "vitamin mỗi ngày. Thực phẩm X: hai gam protein, một gam vitamin, "
            "mười nghìn đồng mỗi trăm gam. Thực phẩm Y: một gam protein, ba gam "
            "vitamin, tám nghìn đồng mỗi trăm gam. Hỏi nên mua mỗi loại bao nhiêu "
            "để đủ dinh dưỡng với chi phí thấp nhất? Bài thứ ba: Có một trăm công "
            "nhân và tám mươi máy. Sản phẩm A cần hai công nhân, một máy, hoàn "
            "thành trong bốn ngày. Sản phẩm B cần một công nhân, hai máy, hoàn "
            "thành trong ba ngày. Hỏi nên sản xuất mỗi loại bao nhiêu để hoàn "
            "thành sớm nhất? Các em hãy làm bài tập và chuẩn bị cho tiết luyện tập."
        )
    },
    {
        "title": "KẾT THÚC BÀI HỌC",
        "lines": [
            "Hôm nay chúng ta đã học:",
            "• Cách nhận biết và giải các bài toán thực tế bằng bất phương trình hai ẩn.",
            "• Phương pháp đặt ẩn và thiết lập ràng buộc từ điều kiện thực tế.",
            "• Cách lập hệ bất phương trình và tìm phương án tối ưu.",
            "• Áp dụng vào nhiều lĩnh vực: sản xuất, dinh dưỡng, vận chuyển, đầu tư...",
            "Bài về nhà: Làm 3 bài tập tự luyện và chuẩn bị cho tiết luyện tập.",
            "Cảm ơn các em đã theo dõi!",
            "Thầy Nguyễn Văn Sang"
        ],
        "narration": (
            "Hôm nay chúng ta đã học về cách nhận biết và giải các bài toán thực tế "
            "bằng bất phương trình hai ẩn. Chúng ta đã học phương pháp đặt ẩn và "
            "thiết lập ràng buộc từ điều kiện thực tế. Cách lập hệ bất phương trình "
            "và tìm phương án tối ưu. Và áp dụng vào nhiều lĩnh vực như sản xuất, "
            "dinh dưỡng, vận chuyển, đầu tư và nhiều lĩnh vực khác. Bài về nhà là "
            "làm ba bài tập tự luyện và chuẩn bị cho tiết luyện tập. Cảm ơn các em "
            "đã theo dõi bài học của thầy Nguyễn Văn Sang. Chúc các em học tốt!"
        )
    }
]

# ================================================================
# ÂM THANH
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
        f"Thời lượng lời đọc gốc: {sum(original_lengths):.1f} giây",
        flush=True
    )
    print(f"Hệ số căn tốc độ: {speed:.3f}", flush=True)

    if not 0.75 <= speed <= 1.35:
        print(
            "Lưu ý: giọng đọc được điều chỉnh tốc độ tương đối nhiều "
            "để đạt thời lượng gần 10 phút.",
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

    (BASE / "kich_ban_bai_toan_thuc_te.json").write_text(
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
# TÍNH MIỀN NGHIỆM BẰNG CẮT ĐA GIÁC
# ================================================================

def signed_value(point, inequality):
    a, b, c, relation = inequality
    value = a * point[0] + b * point[1] - c
    return value if relation in ("<", "<=") else -value


def clip_polygon(vertices, inequality):
    if not vertices:
        return []

    result = []
    eps = 1e-9

    for index, current in enumerate(vertices):
        previous = vertices[index - 1]
        previous_value = signed_value(previous, inequality)
        current_value = signed_value(current, inequality)

        previous_inside = previous_value <= eps
        current_inside = current_value <= eps

        if previous_inside != current_inside:
            denominator = previous_value - current_value
            if abs(denominator) > eps:
                t = previous_value / denominator
                result.append((
                    previous[0] + t * (current[0] - previous[0]),
                    previous[1] + t * (current[1] - previous[1])
                ))

        if current_inside:
            result.append(current)

    return result


def polygon_area(vertices):
    if len(vertices) < 3:
        return 0.0
    return abs(sum(
        vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
        - vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
        for i in range(len(vertices))
    )) / 2


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
        if not any(
            math.hypot(point[0] - other[0], point[1] - other[1]) < eps
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


def satisfies(x, y, inequality):
    a, b, c, relation = inequality
    value = a * x + b * y

    if relation == "<=":
        return value <= c + 1e-8
    if relation == ">=":
        return value >= c - 1e-8
    if relation == "<":
        return value < c - 1e-8
    return value > c + 1e-8


# ================================================================
# CHỮ, BỐ CỤC, ĐỒ THỊ
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
    bounds = spec.get("range", [-1, 6, -1, 6])
    xmin, xmax, ymin, ymax = bounds

    axes = Axes(
        x_range=[xmin, xmax, 1],
        y_range=[ymin, ymax, 1],
        x_length=5.30,
        y_length=4.80,
        axis_config={
            "color": "#B6C2D1",
            "stroke_width": 2,
            "include_ticks": True,
            "include_numbers": False,
            "tip_width": 0.12,
            "tip_height": 0.12
        }
    ).move_to([3.70, 0.08, 0])

    graph = VGroup()
    grid = VGroup()

    for x in range(math.ceil(xmin), math.floor(xmax) + 1):
        grid.add(Line(
            axes.c2p(x, ymin),
            axes.c2p(x, ymax),
            color="#304056",
            stroke_width=0.8
        ))

    for y in range(math.ceil(ymin), math.floor(ymax) + 1):
        grid.add(Line(
            axes.c2p(xmin, y),
            axes.c2p(xmax, y),
            color="#304056",
            stroke_width=0.8
        ))

    graph.add(grid)
    inequalities = spec["ineqs"]

    # Cắt hình chữ nhật quan sát bằng từng nửa mặt phẳng.
    vertices = [
        (xmin, ymin),
        (xmax, ymin),
        (xmax, ymax),
        (xmin, ymax)
    ]

    for inequality in inequalities:
        vertices = clip_polygon(vertices, inequality)

    if polygon_area(vertices) > 1e-9:
        graph.add(Polygon(
            *[axes.c2p(x, y) for x, y in vertices],
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0.26
        ))

    graph.add(axes)

    # Dùng Text cho số trục: không cần cài LaTeX.
    tick_labels = VGroup()

    for x in range(math.ceil(xmin), math.floor(xmax) + 1):
        if x != 0 and xmin < x < xmax:
            label = make_text(str(x), size=15, color=MUTED)
            label.next_to(axes.c2p(x, 0), DOWN, buff=0.09)
            tick_labels.add(label)

    for y in range(math.ceil(ymin), math.floor(ymax) + 1):
        if y != 0 and ymin < y < ymax:
            label = make_text(str(y), size=15, color=MUTED)
            label.next_to(axes.c2p(0, y), LEFT, buff=0.09)
            tick_labels.add(label)

    graph.add(tick_labels)

    x_label = make_text("x", size=21, color=MUTED)
    x_label.next_to(axes.c2p(xmax, 0), RIGHT, buff=0.06)

    y_label = make_text("y", size=21, color=MUTED)
    y_label.next_to(axes.c2p(0, ymax), UP, buff=0.06)

    graph.add(x_label, y_label)

    # Các đường đầy đủ là đường hỗ trợ dựng hình.
    # Chỉ phần thỏa mãn toàn hệ mới thuộc miền nghiệm.
    colors = ["#FBBF24", "#38BDF8", "#C4B5FD", "#F9A8D4"]

    for index, inequality in enumerate(inequalities):
        a, b, c, relation = inequality
        ends = line_rectangle_intersections(a, b, c, bounds)
        if ends is None:
            continue

        p, q = ends
        color = colors[index % len(colors)]

        if relation in ("<", ">"):
            boundary = DashedLine(
                axes.c2p(*p),
                axes.c2p(*q),
                dash_length=0.12,
                dashed_ratio=0.58,
                stroke_width=3,
                color=color
            )
        else:
            boundary = Line(
                axes.c2p(*p),
                axes.c2p(*q),
                stroke_width=3,
                color=color
            )

        graph.add(boundary)

    if spec.get("lattice", False):
        for x in range(math.ceil(xmin), math.floor(xmax) + 1):
            for y in range(math.ceil(ymin), math.floor(ymax) + 1):
                if all(satisfies(x, y, item) for item in inequalities):
                    graph.add(Dot(
                        axes.c2p(x, y),
                        radius=0.037,
                        color=GREEN
                    ))

    open_points = spec.get("open_points", [])

    def is_open(x, y):
        return any(
            abs(x - p[0]) < 1e-8 and abs(y - p[1]) < 1e-8
            for p in open_points
        )

    for x, y, label_content in spec.get("points", []):
        point = Dot(
            axes.c2p(x, y),
            radius=0.058,
            color=FG
        )

        if is_open(x, y):
            point.set_fill(BG, opacity=1)
            point.set_stroke(FG, width=2)

        label = make_text(
            label_content,
            size=18,
            color=FG,
            max_width=1.5
        )

        direction = UR
        if x >= xmax - 1:
            direction = UL
        if y >= ymax - 1:
            direction = DR

        label.next_to(point, direction, buff=0.08)
        label.add_background_rectangle(
            color=BG,
            opacity=0.85,
            buff=0.035
        )

        graph.add(point, label)

    # Vòng tròn rỗng đánh dấu các điểm không được nhận.
    for x, y in open_points:
        point = Circle(
            radius=0.060,
            stroke_color=FG,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=1
        ).move_to(axes.c2p(x, y))
        graph.add(point)

    if spec.get("empty", False):
        message = make_text(
            "MIỀN NGHIỆM: ∅",
            size=27,
            color=YELLOW,
            max_width=4.8
        ).move_to([3.70, 0.1, 0])
        message.add_background_rectangle(
            color=BG,
            opacity=0.94,
            buff=0.15
        )
        graph.add(message)

    caption = make_text(
        spec.get("caption", ""),
        size=22,
        color=GREEN,
        max_width=5.65
    ).move_to([3.65, -2.94, 0])

    graph.add(caption)
    return graph


# ================================================================
# SCENE CHÍNH
# ================================================================

class BaiToanThucTeBatPhuongTrinh(Scene):
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
            "Thầy Nguyễn Văn Sang",
            size=22,
            color=FG
        ).move_to([0, -3.75, 0]).set_z_index(102)

        footer_subject = make_text(
            "TOÁN HỌC • BÀI TOÁN THỰC TẾ",
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

            if has_graph:
                divider = Line(
                    [0.05, -2.70, 0],
                    [0.05, 2.60, 0],
                    color="#304056",
                    stroke_width=1
                )
                content.add(divider, build_graph(slide["graph"]))

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
            self.clear()


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
    else:
        print(
            "Cách chạy:\n"
            "1. python bai_toan_thuc_te_bat_phuong_trinh.py --prepare\n"
            "2. manim -qm --fps 24 bai_toan_thuc_te_bat_phuong_trinh.py "
            "BaiToanThucTeBatPhuongTrinh"
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
    "-o", "Bai_Toan_Thuc_Te_Thay_Nguyen_Van_Sang",
    str(SCRIPT),
    "BaiToanThucTeBatPhuongTrinh"
])

candidates = [
    path
    for path in MEDIA_DIR.rglob(
        "Bai_Toan_Thuc_Te_Thay_Nguyen_Van_Sang.mp4"
    )
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

try:
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
except ImportError:
    print("\nKhông chạy trên Google Colab nên bỏ qua bước tải file tự động.")
