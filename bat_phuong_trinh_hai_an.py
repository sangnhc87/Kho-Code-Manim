import sys
import subprocess
from pathlib import Path

def run_command(command):
    subprocess.run(command, check=True)

print("BƯỚC 1/4: Cài đặt thư viện và phông chữ...")

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
    sys.executable, "-m", "pip", "install",
    "-q",
    "manim==0.19.0",
    "edge-tts>=7.0.0,<8"
])

WORK = Path("/content/bat_phuong_trinh_hai_an")
WORK.mkdir(parents=True, exist_ok=True)

SCRIPT = WORK / "bai_giang_bat_phuong_trinh.py"

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
AUDIO_DIR = BASE / "audio_bpt"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = BASE / "thoi_luong.json"

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
GOOD = "#34D399"
WARN = "#FBBF24"
BAD = "#FB7185"

config.background_color = BG

# Quy ước bất phương trình đồ thị:
# (a, b, c, relation) biểu diễn ax + by relation c.
# Các relation: "<=", ">=", "<", ">".
#
# Mỗi trang có:
# title: tiêu đề
# lines: nội dung trên màn hình
# narration: lời thuyết minh
# graph: hình vẽ, nếu có

SLIDES = [
    {
        "title": "BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN",
        "lines": [
            "Bài học: Từ bất phương trình đến miền nghiệm",
            "Mục tiêu 1: Nhận biết dạng ax + by ≤ c và các dạng tương tự.",
            "Mục tiêu 2: Kiểm tra một cặp số có phải là nghiệm.",
            "Mục tiêu 3: Biểu diễn miền nghiệm trên mặt phẳng tọa độ.",
            "Mục tiêu 4: Vận dụng vào bài tập và tình huống thực tế.",
            "Chuẩn bị: giấy nháp, bút và thước kẻ."
        ],
        "narration": (
            "Chào các em. Chúng ta cùng tìm hiểu bài bất phương trình bậc nhất hai ẩn. "
            "Sau bài học, các em cần đạt bốn mục tiêu. Thứ nhất, nhận biết đúng dạng "
            "bất phương trình bậc nhất hai ẩn. Thứ hai, kiểm tra được một cặp số có "
            "phải là nghiệm hay không. Thứ ba, vẽ và xác định miền nghiệm trên mặt "
            "phẳng tọa độ. Cuối cùng, vận dụng kiến thức vào bài toán thực tế. "
            "Các em hãy chuẩn bị giấy nháp và thước kẻ. Khi gặp bài tập, hãy tạm "
            "dừng video, tự làm trước rồi đối chiếu với lời giải."
        )
    },
    {
        "title": "1. KHỞI ĐỘNG TỪ MỘT TÌNH HUỐNG",
        "lines": [
            "Một xưởng có tối đa 12 giờ làm việc.",
            "Mỗi ghế cần 2 giờ; mỗi bàn cần 3 giờ.",
            "Gọi x là số ghế, y là số bàn.",
            "Tổng thời gian: 2x + 3y giờ.",
            "Điều kiện thời gian: 2x + 3y ≤ 12.",
            "Điều kiện thực tế: x, y là số nguyên không âm.",
            "Vì sao dùng dấu ≤, không dùng dấu =?"
        ],
        "narration": (
            "Một xưởng có tối đa mười hai giờ làm việc. Làm một chiếc ghế cần hai "
            "giờ, còn một chiếc bàn cần ba giờ. Gọi x là số ghế và y là số bàn. "
            "Tổng thời gian sản xuất là hai x cộng ba y. Vì không được vượt quá "
            "mười hai giờ, ta có hai x cộng ba y nhỏ hơn hoặc bằng mười hai. "
            "Dấu nhỏ hơn hoặc bằng cho phép sử dụng hết, hoặc chưa hết thời gian. "
            "Ngoài ra, số bàn và số ghế phải là số nguyên không âm. Đây là "
            "một tình huống tự nhiên dẫn đến bất phương trình bậc nhất hai ẩn."
        )
    },
    {
        "title": "2. ĐỊNH NGHĨA VÀ NHẬN BIẾT",
        "lines": [
            "Dạng: ax + by < c; ax + by ≤ c;",
            "         ax + by > c; ax + by ≥ c.",
            "Trong đó a, b, c là số thực; a và b không đồng thời bằng 0.",
            "Ví dụ đúng: 2x − y ≤ 3; x > −1; y ≤ 2.",
            "Không đúng dạng: x² + y ≤ 3 vì xuất hiện x².",
            "Không đúng dạng: xy > 1 vì xuất hiện tích hai ẩn.",
            "Một hệ số có thể bằng 0: x ≥ −1 vẫn đúng dạng."
        ],
        "narration": (
            "Bất phương trình bậc nhất hai ẩn x và y có một trong bốn dạng đang "
            "hiển thị. Các hệ số a, b, c là số thực, trong đó a và b không đồng "
            "thời bằng không. Ví dụ, hai x trừ y nhỏ hơn hoặc bằng ba là một "
            "bất phương trình bậc nhất hai ẩn. Các biểu thức có x bình phương, "
            "hoặc có tích x nhân y, không thuộc dạng này. Các em chú ý một điểm "
            "dễ nhầm: một trong hai hệ số được phép bằng không. Vì vậy, x lớn "
            "hơn hoặc bằng âm một vẫn được xét trên mặt phẳng hai ẩn."
        )
    },
    {
        "title": "3. NGHIỆM LÀ MỘT CẶP SỐ",
        "lines": [
            "Xét bất phương trình: 2x − y ≤ 3.",
            "Cặp (x₀; y₀) là nghiệm khi thay vào được mệnh đề đúng.",
            "A(1; 0): 2·1 − 0 = 2 ≤ 3 → là nghiệm.",
            "B(3; 1): 2·3 − 1 = 5 > 3 → không là nghiệm.",
            "C(2; 1): 2·2 − 1 = 3 ≤ 3 → là nghiệm.",
            "Dấu ≤ cho phép trường hợp hai vế bằng nhau.",
            "Tập hợp các điểm nghiệm gọi là miền nghiệm."
        ],
        "narration": (
            "Nghiệm của bất phương trình hai ẩn không phải một số riêng lẻ, mà "
            "là một cặp số có thứ tự. Xét hai x trừ y nhỏ hơn hoặc bằng ba. "
            "Với điểm A có tọa độ một, không, vế trái bằng hai nên A là nghiệm. "
            "Với điểm B có tọa độ ba, một, vế trái bằng năm, lớn hơn ba, nên "
            "B không là nghiệm. Với điểm C có tọa độ hai, một, hai vế cùng "
            "bằng ba. Do dấu là nhỏ hơn hoặc bằng, C vẫn là nghiệm. Khi biểu "
            "diễn tất cả các cặp nghiệm bằng điểm, ta được miền nghiệm."
        )
    },
    {
        "title": "4. ĐƯỜNG BIÊN VÀ HAI NỬA MẶT PHẲNG",
        "lines": [
            "Xét: x + y ≤ 3.",
            "Đường biên: d: x + y = 3.",
            "Cho x = 0 → y = 3.",
            "Cho y = 0 → x = 3.",
            "d đi qua A(0; 3), B(3; 0).",
            "Hai phía của d ứng với:",
            "x + y < 3 và x + y > 3.",
            "Dấu ≤: nhận cả đường biên."
        ],
        "graph": {
            "ineqs": [[1, 1, 3, "<="]],
            "shade": False,
            "points": [[0, 3, "A(0; 3)"], [3, 0, "B(3; 0)"]],
            "caption": "Đường biên d: x + y = 3"
        },
        "narration": (
            "Để hiểu miền nghiệm, trước tiên ta xét đường biên. Với x cộng y "
            "nhỏ hơn hoặc bằng ba, đường biên là x cộng y bằng ba. Cho x bằng "
            "không, ta được điểm A, không, ba. Cho y bằng không, ta được điểm B, "
            "ba, không. Đường thẳng qua hai điểm này chia mặt phẳng thành hai "
            "nửa mặt phẳng. Một phía có x cộng y nhỏ hơn ba; phía còn lại có "
            "x cộng y lớn hơn ba. Vì bất phương trình dùng dấu nhỏ hơn hoặc "
            "bằng, các điểm trên đường biên cũng được nhận."
        )
    },
    {
        "title": "5. QUY TRÌNH XÁC ĐỊNH MIỀN NGHIỆM",
        "lines": [
            "Bước 1. Vẽ đường biên d: ax + by = c.",
            "Bước 2. Chọn điểm thử M không nằm trên d.",
            "Bước 3. Thay tọa độ M vào bất phương trình.",
            "Nếu đúng → chọn nửa mặt phẳng chứa M.",
            "Nếu sai → chọn nửa mặt phẳng không chứa M.",
            "Bước 4. Xét có lấy đường biên hay không.",
            "Dấu ≤, ≥: nét liền, lấy biên. Dấu <, >: nét đứt, bỏ biên.",
            "Trong video: vùng tô xanh là miền nghiệm."
        ],
        "narration": (
            "Các em ghi nhớ quy trình bốn bước. Bước một, thay dấu bất phương "
            "trình bằng dấu bằng để vẽ đường biên. Bước hai, chọn một điểm thử "
            "không nằm trên đường biên. Gốc tọa độ thường thuận tiện, nhưng không "
            "phải lúc nào cũng dùng được. Bước ba, thay tọa độ điểm thử vào "
            "bất phương trình. Nếu đúng thì chọn phía chứa điểm thử, nếu sai "
            "thì chọn phía đối diện. Bước bốn, kiểm tra đường biên. Dấu có bằng "
            "thì lấy biên và vẽ nét liền; dấu không có bằng thì bỏ biên và "
            "vẽ nét đứt."
        )
    },
    {
        "title": "VÍ DỤ 1. DẤU ≤: LẤY ĐƯỜNG BIÊN",
        "lines": [
            "Biểu diễn: x + y ≤ 3.",
            "B1. Vẽ d: x + y = 3.",
            "d qua (0; 3) và (3; 0).",
            "B2. Chọn O(0; 0), O ∉ d.",
            "B3. 0 + 0 ≤ 3 là đúng.",
            "Chọn phía chứa gốc O.",
            "B4. Dấu ≤ nên lấy biên.",
            "Miền nghiệm: vùng xanh và d."
        ],
        "graph": {
            "ineqs": [[1, 1, 3, "<="]],
            "points": [[0, 0, "O"], [0, 3, "A"], [3, 0, "B"]],
            "caption": "x + y ≤ 3: chứa O, lấy biên"
        },
        "narration": (
            "Ta giải chi tiết ví dụ thứ nhất: x cộng y nhỏ hơn hoặc bằng ba. "
            "Đường biên đi qua hai điểm không, ba và ba, không. Chọn gốc "
            "tọa độ O làm điểm thử. Vì không cộng không nhỏ hơn hoặc bằng "
            "ba là mệnh đề đúng, ta chọn nửa mặt phẳng chứa O. Dấu nhỏ hơn "
            "hoặc bằng cho biết phải lấy cả đường biên, nên đường thẳng được "
            "vẽ nét liền. Kết luận, miền nghiệm là vùng tô xanh cùng với đường "
            "biên. Hình chỉ thể hiện một phần; miền nghiệm thực tế còn kéo "
            "dài vô hạn."
        )
    },
    {
        "title": "VÍ DỤ 2. DẤU >: KHÔNG LẤY BIÊN",
        "lines": [
            "Biểu diễn: x + y > 2.",
            "B1. d: x + y = 2.",
            "d qua (0; 2) và (2; 0).",
            "B2. Chọn O(0; 0).",
            "B3. 0 > 2 là sai.",
            "Chọn phía không chứa O.",
            "B4. Dấu > nên bỏ biên.",
            "Kiểm tra (2; 2): 4 > 2, đúng."
        ],
        "graph": {
            "ineqs": [[1, 1, 2, ">"]],
            "points": [[0, 0, "O"], [2, 2, "M(2; 2)"]],
            "caption": "x + y > 2: bỏ O, bỏ biên"
        },
        "narration": (
            "Ví dụ thứ hai là x cộng y lớn hơn hai. Đường biên x cộng y bằng "
            "hai đi qua không, hai và hai, không. Thử gốc tọa độ, ta được "
            "không lớn hơn hai, đây là mệnh đề sai. Vì thế, miền nghiệm nằm "
            "ở phía không chứa gốc O. Dấu lớn hơn không có dấu bằng, nên "
            "đường biên được vẽ nét đứt và không thuộc miền nghiệm. Để kiểm "
            "tra thêm, điểm M có tọa độ hai, hai cho tổng bằng bốn, lớn hơn "
            "hai. M nằm trong vùng tô xanh, phù hợp với kết quả."
        )
    },
    {
        "title": "VÍ DỤ 3. CẨN THẬN KHI ĐỔI DẤU",
        "lines": [
            "Biểu diễn: 2x − y ≥ 1.",
            "2x − y ≥ 1 ⇔ −y ≥ 1 − 2x.",
            "Nhân với −1 phải đổi chiều:",
            "y ≤ 2x − 1.",
            "d: y = 2x − 1, vẽ nét liền.",
            "O(0; 0): 0 ≥ 1 là sai.",
            "Chọn phía dưới d, không chứa O.",
            "M(1; 0): 2 ≥ 1, là nghiệm."
        ],
        "graph": {
            "ineqs": [[2, -1, 1, ">="]],
            "points": [[0, 0, "O"], [1, 0, "M(1; 0)"]],
            "caption": "2x − y ≥ 1 ⇔ y ≤ 2x − 1"
        },
        "narration": (
            "Xét hai x trừ y lớn hơn hoặc bằng một. Khi chuyển vế, ta có "
            "âm y lớn hơn hoặc bằng một trừ hai x. Nhân cả hai vế với âm "
            "một, bắt buộc đổi chiều bất phương trình. Kết quả là y nhỏ hơn "
            "hoặc bằng hai x trừ một. Vì vậy, miền nghiệm nằm phía dưới "
            "đường thẳng y bằng hai x trừ một, kể cả đường biên. Kiểm tra "
            "bằng điểm O: không lớn hơn hoặc bằng một là sai. Điểm một, "
            "không lại thỏa mãn. Hai cách kiểm tra đều cho cùng một kết quả."
        )
    },
    {
        "title": "VÍ DỤ 4. BIẾN ĐỔI VỀ y < ax + b",
        "lines": [
            "Biểu diễn: −x + 2y < 4.",
            "2y < x + 4 ⇔ y < x/2 + 2.",
            "d: y = x/2 + 2.",
            "d qua A(0; 2), B(2; 3).",
            "Chia cho 2 > 0: giữ chiều.",
            "O(0; 0): 0 < 4 là đúng.",
            "Chọn phía chứa O, dưới d.",
            "Dấu <: vẽ nét đứt, bỏ biên."
        ],
        "graph": {
            "ineqs": [[-1, 2, 4, "<"]],
            "points": [[0, 0, "O"], [0, 2, "A"], [2, 3, "B"]],
            "caption": "−x + 2y < 4 ⇔ y < x/2 + 2"
        },
        "narration": (
            "Tiếp theo, xét âm x cộng hai y nhỏ hơn bốn. Chuyển âm x sang "
            "vế phải rồi chia cho hai, ta được y nhỏ hơn x chia hai cộng "
            "hai. Vì chia cho số dương nên chiều bất phương trình được giữ "
            "nguyên. Đường biên đi qua điểm không, hai và điểm hai, ba. "
            "Gốc tọa độ thỏa mãn vì không nhỏ hơn bốn là đúng. Vậy ta chọn "
            "phía chứa O, cũng chính là phía dưới đường thẳng. Dấu nhỏ hơn "
            "không có bằng, nên không lấy biên. Các em hãy đối chiếu phép "
            "biến đổi với hình vẽ."
        )
    },
    {
        "title": "TRƯỜNG HỢP ĐẶC BIỆT 1: BIÊN THẲNG ĐỨNG",
        "lines": [
            "Biểu diễn: x ≥ −1.",
            "Viết đầy đủ: x + 0y ≥ −1.",
            "Đường biên: x = −1.",
            "Biên song song với trục Oy.",
            "O(0; 0): 0 ≥ −1 là đúng.",
            "Chọn phía bên phải đường biên.",
            "Lấy biên vì dấu ≥.",
            "y có thể nhận mọi giá trị thực."
        ],
        "graph": {
            "ineqs": [[1, 0, -1, ">="]],
            "points": [[0, 0, "O"]],
            "caption": "x ≥ −1: phía phải, lấy biên"
        },
        "narration": (
            "Nếu hệ số của y bằng không, đường biên có thể là một đường "
            "thẳng đứng. Ví dụ x lớn hơn hoặc bằng âm một có đường biên "
            "x bằng âm một, song song với trục tung. Gốc tọa độ thỏa mãn "
            "vì không lớn hơn hoặc bằng âm một là đúng. Miền nghiệm là "
            "phía bên phải đường biên và bao gồm cả đường biên. Trong "
            "bất phương trình này, y không bị ràng buộc. Với mỗi giá trị "
            "x thỏa mãn, y có thể là bất kỳ số thực nào. Đừng bỏ sót "
            "trường hợp đặc biệt này."
        )
    },
    {
        "title": "TRƯỜNG HỢP ĐẶC BIỆT 2: BIÊN NẰM NGANG",
        "lines": [
            "Biểu diễn: y < 2.",
            "Viết đầy đủ: 0x + y < 2.",
            "Đường biên: y = 2.",
            "Biên song song với trục Ox.",
            "O(0; 0): 0 < 2 là đúng.",
            "Chọn phía dưới đường biên.",
            "Bỏ biên vì dấu <.",
            "x có thể nhận mọi giá trị thực."
        ],
        "graph": {
            "ineqs": [[0, 1, 2, "<"]],
            "points": [[0, 0, "O"]],
            "caption": "y < 2: phía dưới, bỏ biên"
        },
        "narration": (
            "Tương tự, khi hệ số của x bằng không, ta có thể gặp đường "
            "biên nằm ngang. Xét y nhỏ hơn hai. Đường biên y bằng hai "
            "song song với trục hoành. Gốc tọa độ thỏa mãn, nên chọn phía "
            "dưới đường biên. Vì dấu là nhỏ hơn, đường biên phải vẽ nét "
            "đứt và không được lấy. Mọi điểm có tung độ nhỏ hơn hai đều "
            "là nghiệm, bất kể hoành độ là bao nhiêu. Hai trường hợp "
            "đặc biệt giúp các em nhớ thêm: ràng buộc x thì nhìn trái, "
            "phải; ràng buộc y thì nhìn trên, dưới."
        )
    },
    {
        "title": "LƯU Ý: KHÔNG PHẢI LÚC NÀO CŨNG THỬ O",
        "lines": [
            "Biểu diễn: x − y > 0.",
            "Đường biên: y = x.",
            "O(0; 0) nằm trên đường biên!",
            "Không dùng O để phân biệt hai phía.",
            "Chọn M(1; 0), M không thuộc d.",
            "1 − 0 > 0 là đúng.",
            "Chọn phía chứa M: y < x.",
            "Vẽ nét đứt, không lấy biên."
        ],
        "graph": {
            "ineqs": [[1, -1, 0, ">"]],
            "points": [[0, 0, "O"], [1, 0, "M(1; 0)"]],
            "caption": "O nằm trên biên → thử M(1; 0)"
        },
        "narration": (
            "Một lỗi rất thường gặp là luôn chọn gốc tọa độ để thử. "
            "Với x trừ y lớn hơn không, đường biên là y bằng x và đi "
            "qua gốc tọa độ. Do đó, O không giúp phân biệt hai nửa "
            "mặt phẳng. Ta đổi sang điểm M có tọa độ một, không. Thay "
            "vào, một trừ không lớn hơn không là đúng. Vì vậy chọn "
            "phía chứa M, tức vùng y nhỏ hơn x. Đường biên vẽ nét "
            "đứt. Các em hãy ghi nhớ điều kiện quan trọng: điểm thử "
            "phải nằm ngoài đường biên."
        )
    },
    {
        "title": "BÀI TẬP 1. KIỂM TRA NGHIỆM",
        "lines": [
            "Điểm nào là nghiệm của 3x + 2y < 6?",
            "A(0; 0)     B(2; 0)     C(1; 2)     D(−1; 5)",
            "A: 3·0 + 2·0 = 0 < 6 → đúng.",
            "B: 3·2 + 2·0 = 6; 6 < 6 → sai.",
            "C: 3·1 + 2·2 = 7 > 6 → sai.",
            "D: 3·(−1) + 2·5 = 7 > 6 → sai.",
            "Kết luận: chỉ có điểm A là nghiệm.",
            "Nhắc lại: dấu < không nhận trường hợp bằng nhau."
        ],
        "narration": (
            "Bây giờ là bài tập kiểm tra nghiệm. Trong bốn điểm đang "
            "hiển thị, điểm nào thỏa mãn ba x cộng hai y nhỏ hơn sáu? "
            "Các em có thể dừng video để tự tính. Với điểm A, vế trái "
            "bằng không nên thỏa mãn. Với B, vế trái bằng sáu, nhưng "
            "sáu nhỏ hơn sáu là sai. Với C, vế trái bằng bảy nên "
            "không thỏa mãn. Với D, âm ba cộng mười cũng bằng bảy, "
            "không thỏa mãn. Vậy chỉ có A là nghiệm. Điểm B nhắc "
            "chúng ta phải phân biệt dấu nhỏ hơn với nhỏ hơn hoặc bằng."
        )
    },
    {
        "title": "BÀI TẬP 2. VẼ MIỀN NGHIỆM",
        "lines": [
            "Đề bài: biểu diễn 2x + y > 4.",
            "B1. d: 2x + y = 4.",
            "d qua A(0; 4), B(2; 0).",
            "B2. Thử O: 0 > 4 là sai.",
            "B3. Chọn phía không chứa O.",
            "B4. Dấu >: không lấy biên.",
            "Viết lại: y > 4 − 2x.",
            "Kết luận: phía trên d, bỏ d."
        ],
        "graph": {
            "ineqs": [[2, 1, 4, ">"]],
            "points": [[0, 0, "O"], [0, 4, "A"], [2, 0, "B"]],
            "caption": "2x + y > 4 ⇔ y > 4 − 2x"
        },
        "narration": (
            "Bài tập thứ hai yêu cầu biểu diễn hai x cộng y lớn hơn "
            "bốn. Đường biên hai x cộng y bằng bốn đi qua A, không, "
            "bốn và B, hai, không. Thay gốc tọa độ vào bất phương "
            "trình được không lớn hơn bốn, là sai. Ta chọn nửa "
            "mặt phẳng không chứa O. Vì dùng dấu lớn hơn nên "
            "không lấy đường biên. Để kiểm tra hướng tô, biến đổi "
            "thành y lớn hơn bốn trừ hai x. Như vậy, miền nghiệm "
            "ở phía trên đường thẳng. Đây là một cách kiểm tra "
            "chéo rất hữu ích sau khi vẽ."
        )
    },
    {
        "title": "MỞ RỘNG: MIỀN NGHIỆM CỦA MỘT HỆ",
        "lines": [
            "Xét đồng thời các điều kiện:",
            "x ≥ 0; y ≥ 0;",
            "x + y ≤ 4; 2x + y ≤ 6.",
            "Miền nghiệm là phần giao.",
            "Hai đường xiên cắt tại (2; 2).",
            "Trên Ox: 0 ≤ x ≤ 3.",
            "Trên Oy: 0 ≤ y ≤ 4.",
            "Các đỉnh: (0; 0), (3; 0),",
            "(2; 2), (0; 4); lấy cả biên."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 4, "<="],
                [2, 1, 6, "<="]
            ],
            "range": [-1, 6, -1, 6],
            "points": [
                [0, 0, "O"],
                [3, 0, "A"],
                [2, 2, "B"],
                [0, 4, "C"]
            ],
            "caption": "Phần giao của bốn miền nghiệm"
        },
        "narration": (
            "Ta mở rộng sang một hệ gồm bốn bất phương trình. Một "
            "điểm là nghiệm của hệ khi thỏa mãn tất cả các điều kiện, "
            "nên miền nghiệm là phần giao của các miền. Hai điều kiện "
            "đầu giới hạn x và y không âm. Hai đường xiên có phương "
            "trình x cộng y bằng bốn và hai x cộng y bằng sáu. "
            "Lấy phương trình thứ hai trừ phương trình thứ nhất "
            "được x bằng hai, rồi suy ra y bằng hai. Trên trục "
            "hoành, x chạy từ không đến ba; trên trục tung, y "
            "chạy từ không đến bốn. Miền nghiệm là tứ giác tô xanh, "
            "bao gồm cả các cạnh."
        )
    },
    {
        "title": "VẬN DỤNG THỰC TẾ: LẬP MÔ HÌNH",
        "lines": [
            "Trở lại bài toán làm bàn và ghế.",
            "x: số ghế; y: số bàn.",
            "Mỗi ghế 2 giờ; mỗi bàn 3 giờ.",
            "Tối đa 12 giờ:",
            "2x + 3y ≤ 12.",
            "Thêm x ≥ 0, y ≥ 0.",
            "Miền liên tục là tam giác có đỉnh:",
            "(0; 0), (6; 0), (0; 4).",
            "Phương án thực tế: điểm nguyên."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [2, 3, 12, "<="]
            ],
            "range": [-1, 7, -1, 5],
            "lattice": True,
            "points": [[6, 0, "A"], [0, 4, "B"]],
            "caption": "Điểm nguyên trong và trên tam giác"
        },
        "narration": (
            "Trở lại bài toán sản xuất. Gọi x là số ghế, y là số "
            "bàn. Điều kiện thời gian là hai x cộng ba y nhỏ hơn "
            "hoặc bằng mười hai. Thêm x không âm và y không âm, "
            "ta được miền hình tam giác ở góc phần tư thứ nhất. "
            "Đường biên cắt trục hoành tại sáu, không và trục tung "
            "tại không, bốn. Tuy nhiên, bàn ghế không thể có số "
            "lượng lẻ như một phẩy năm chiếc. Vì vậy, chỉ các "
            "điểm có cả hai tọa độ nguyên trong hoặc trên tam "
            "giác mới biểu diễn phương án sản xuất phù hợp."
        )
    },
    {
        "title": "VẬN DỤNG THỰC TẾ: GIẢI CHI TIẾT",
        "lines": [
            "Phương án 1: 3 ghế, 2 bàn.",
            "2·3 + 3·2 = 12 ≤ 12 → thực hiện được.",
            "Phương án 2: 4 ghế, 2 bàn.",
            "2·4 + 3·2 = 14 > 12 → không thực hiện được.",
            "Nếu làm đúng 2 bàn: 2x + 6 ≤ 12.",
            "Suy ra 2x ≤ 6 ⇔ x ≤ 3.",
            "Vì x nguyên không âm: x ∈ {0; 1; 2; 3}.",
            "Kết luận: làm 2 bàn thì có thể làm thêm tối đa 3 ghế."
        ],
        "narration": (
            "Ta kiểm tra hai phương án cụ thể. Ba ghế và hai bàn "
            "cần hai nhân ba cộng ba nhân hai, bằng mười hai giờ, "
            "nên thực hiện được. Bốn ghế và hai bàn cần mười bốn "
            "giờ, vượt giới hạn, nên không thực hiện được. Bây "
            "giờ, nếu đã quyết định làm đúng hai bàn, có thể làm "
            "thêm tối đa bao nhiêu ghế? Thay y bằng hai, ta có "
            "hai x cộng sáu nhỏ hơn hoặc bằng mười hai. Suy ra "
            "x nhỏ hơn hoặc bằng ba. Do x là số nguyên không "
            "âm, x nhận không, một, hai hoặc ba. Vậy tối đa "
            "làm thêm được ba chiếc ghế."
        )
    },
    {
        "title": "NHỮNG LỖI THƯỜNG GẶP",
        "lines": [
            "Lỗi 1: Nhân hoặc chia số âm nhưng quên đổi chiều dấu.",
            "Sửa: a < b thì −a > −b.",
            "Lỗi 2: Chọn điểm thử nằm trên đường biên.",
            "Sửa: kiểm tra ax₀ + by₀ ≠ c trước khi thử.",
            "Lỗi 3: Dấu <, > nhưng vẫn lấy đường biên.",
            "Sửa: không có dấu bằng → nét đứt, bỏ biên.",
            "Lỗi 4: Chỉ nhìn vùng xanh mà quên điều kiện thực tế.",
            "Sửa: kiểm tra thêm tính không âm và tính nguyên."
        ],
        "narration": (
            "Trước khi kết thúc, chúng ta tổng hợp bốn lỗi cần tránh. "
            "Một là quên đổi chiều khi nhân hoặc chia cả hai vế "
            "cho số âm. Hai là chọn điểm thử nằm ngay trên đường "
            "biên, khiến việc chọn phía không còn đúng phương pháp. "
            "Ba là nhầm giữa nét liền và nét đứt: dấu có bằng "
            "thì nhận biên, dấu không có bằng thì bỏ biên. Bốn "
            "là quên điều kiện thực tế. Trong bài toán đếm đồ "
            "vật, một điểm thuộc miền liên tục chưa chắc là "
            "phương án hợp lệ nếu tọa độ không nguyên. Các em "
            "nên kiểm tra bốn điểm này trước khi kết luận."
        )
    },
    {
        "title": "TỰ LUYỆN: BA DẠNG KHÁC NHAU",
        "lines": [
            "Hãy dừng video và tự biểu diễn miền nghiệm.",
            "Câu 1. 3x − y ≤ 6.",
            "Giải: y ≥ 3x − 6; biên qua (2; 0), (3; 3).",
            "Thử O đúng → chọn phía trên, lấy biên.",
            "Câu 2. −2x + y > 1.",
            "Giải: y > 2x + 1; biên qua (0; 1), (1; 3).",
            "Thử O sai → chọn phía trên, bỏ biên.",
            "Câu 3. y ≤ −1: phía dưới y = −1, lấy biên."
        ],
        "narration": (
            "Các em hãy tự luyện ba câu trên màn hình. Câu một, "
            "ba x trừ y nhỏ hơn hoặc bằng sáu, tương đương y "
            "lớn hơn hoặc bằng ba x trừ sáu. Vẽ đường thẳng "
            "qua hai, không và ba, ba, rồi chọn phía trên và "
            "lấy biên. Câu hai, âm hai x cộng y lớn hơn một, "
            "tương đương y lớn hơn hai x cộng một. Vẽ biên "
            "qua không, một và một, ba; chọn phía trên nhưng "
            "bỏ biên. Câu ba, y nhỏ hơn hoặc bằng âm một: "
            "chọn phía dưới đường thẳng nằm ngang y bằng âm "
            "một, bao gồm đường biên."
        )
    },
    {
        "title": "TỔNG KẾT BÀI HỌC",
        "lines": [
            "Nhận biết: ax + by so sánh với c; (a; b) ≠ (0; 0).",
            "Kiểm tra nghiệm: thay đúng cặp tọa độ vào bất phương trình.",
            "Vẽ miền nghiệm: VẼ BIÊN → THỬ ĐIỂM → CHỌN PHÍA.",
            "Xét đường biên: ≤, ≥ lấy biên; <, > bỏ biên.",
            "Vận dụng: lập bất phương trình và thêm điều kiện thực tế.",
            "Tự đánh giá: Em đã đạt đủ bốn mục tiêu đầu bài chưa?",
            "Cảm ơn các em đã theo dõi!",
            "Thầy Nguyễn Văn Sang"
        ],
        "narration": (
            "Chúng ta đã hoàn thành bài bất phương trình bậc nhất "
            "hai ẩn. Hãy nhớ: nghiệm là một cặp số, còn miền "
            "nghiệm là tập hợp các điểm thỏa mãn trên mặt phẳng "
            "tọa độ. Quy trình trọng tâm gồm vẽ biên, thử điểm, "
            "chọn phía và xét có lấy biên hay không. Khi làm "
            "bài thực tế, cần đặt ẩn rõ ràng, lập đúng bất "
            "phương trình và kiểm tra các điều kiện bổ sung. "
            "Các em hãy đối chiếu với bốn mục tiêu đầu bài, "
            "sau đó tự làm lại những ví dụ còn chưa chắc. "
            "Cảm ơn các em đã theo dõi bài học của thầy "
            "Nguyễn Văn Sang. Chúc các em học tốt!"
        )
    }
]

# ================================================================
# TẠO GIỌNG ĐỌC VÀ ĐỒNG BỘ THỜI LƯỢNG
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
    """Tạo chuỗi atempo hợp lệ kể cả khi hệ số ngoài [0.5; 2]."""
    factors = []
    while speed > 2.0:
        factors.append(2.0)
        speed /= 2.0
    while speed < 0.5:
        factors.append(0.5)
        speed /= 0.5
    factors.append(speed)
    return ",".join(f"atempo={factor:.9f}" for factor in factors)


async def synthesize_one(text, target):
    """Thử lại khi dịch vụ giọng đọc gặp lỗi mạng tạm thời."""
    last_error = None
    for attempt in range(4):
        try:
            if target.exists():
                target.unlink()
            tts = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate=VOICE_RATE
            )
            await tts.save(str(target))
            if not target.exists() or target.stat().st_size < 500:
                raise RuntimeError("Tệp giọng đọc rỗng hoặc chưa hoàn chỉnh.")
            audio_duration(target)
            return
        except Exception as exc:
            last_error = exc
            print(
                f"  Lần tạo giọng {attempt + 1} chưa thành công: {exc}",
                flush=True
            )
            await asyncio.sleep(2 + attempt * 2)

    raise RuntimeError(
        "Không tạo được giọng NamMinh. "
        "Hãy kiểm tra Internet và chạy lại ô Colab."
    ) from last_error


async def prepare_audio():
    original_durations = []

    for index, slide in enumerate(SLIDES):
        mp3 = AUDIO_DIR / f"original_{index:02d}.mp3"
        text_file = AUDIO_DIR / f"original_{index:02d}.txt"

        cache_key = (
            VOICE + "\n" + VOICE_RATE + "\n" + slide["narration"]
        )
        cached = (
            mp3.exists()
            and text_file.exists()
            and text_file.read_text(encoding="utf-8") == cache_key
        )

        if cached:
            try:
                duration = audio_duration(mp3)
                cached = duration > 0
            except Exception:
                cached = False

        if not cached:
            print(
                f"Tạo giọng nam: trang {index + 1}/{len(SLIDES)}",
                flush=True
            )
            await synthesize_one(slide["narration"], mp3)
            text_file.write_text(cache_key, encoding="utf-8")

        original_durations.append(audio_duration(mp3))

    overhead = len(SLIDES) * (
        ENTER_TIME + AFTER_AUDIO_TIME + EXIT_TIME
    )
    target_audio = TARGET_SECONDS - overhead

    if target_audio <= 0:
        raise RuntimeError("Thời lượng đích quá ngắn.")

    speed = sum(original_durations) / target_audio

    print(
        f"Tổng lời đọc gốc: {sum(original_durations):.1f} giây",
        flush=True
    )
    print(
        f"Hệ số điều chỉnh tốc độ để video gần 10 phút: {speed:.3f}",
        flush=True
    )

    if not 0.75 <= speed <= 1.35:
        print(
            "Lưu ý: tốc độ đọc sẽ được điều chỉnh tương đối nhiều "
            "để đạt thời lượng đích.",
            flush=True
        )

    # atempo thay đổi tốc độ nhưng giữ cao độ giọng nam.
    # apad + atrim cố định độ dài từng đoạn.
    final_durations = []

    for index, duration in enumerate(original_durations):
        source = AUDIO_DIR / f"original_{index:02d}.mp3"
        target = AUDIO_DIR / f"voice_{index:02d}.wav"
        desired = duration / speed

        filter_string = (
            atempo_filter(speed)
            + f",apad,atrim=duration={desired:.9f}"
        )

        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(source),
                "-vn",
                "-af", filter_string,
                "-ar", "48000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                str(target)
            ],
            check=True
        )
        final_durations.append(audio_duration(target))

    TIMING_FILE.write_text(
        json.dumps(
            {
                "durations": final_durations,
                "target_seconds": TARGET_SECONDS,
                "voice": VOICE,
                "speed_factor": speed
            },
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Đã chuẩn bị {len(final_durations)} đoạn âm thanh.",
        flush=True
    )


# ================================================================
# HÌNH HỌC MIỀN NGHIỆM
# Cắt đa giác bằng nửa mặt phẳng, không tô gần đúng bằng lưới
# ================================================================

def signed_value(point, inequality):
    a, b, c, relation = inequality
    value = a * point[0] + b * point[1] - c
    # Giá trị <= 0 nghĩa là nằm trong nửa mặt phẳng cần lấy.
    return value if relation in ("<", "<=") else -value


def clip_polygon(vertices, inequality):
    if not vertices:
        return []

    result = []
    eps = 1e-9

    for i, current in enumerate(vertices):
        previous = vertices[i - 1]
        vp = signed_value(previous, inequality)
        vc = signed_value(current, inequality)

        previous_inside = vp <= eps
        current_inside = vc <= eps

        if previous_inside != current_inside:
            denominator = vp - vc
            if abs(denominator) > eps:
                t = vp / denominator
                intersection = (
                    previous[0] + t * (current[0] - previous[0]),
                    previous[1] + t * (current[1] - previous[1])
                )
                result.append(intersection)

        if current_inside:
            result.append(current)

    return result


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
            math.hypot(point[0] - q[0], point[1] - q[1]) < eps
            for q in unique
        ):
            unique.append(point)

    if len(unique) < 2:
        return None

    # Nếu đường thẳng đi qua góc, chọn hai điểm xa nhau nhất.
    pairs = [
        (p, q)
        for i, p in enumerate(unique)
        for q in unique[i + 1:]
    ]
    return max(
        pairs,
        key=lambda pair: (
            (pair[0][0] - pair[1][0]) ** 2
            + (pair[0][1] - pair[1][1]) ** 2
        )
    )


def point_satisfies(x, y, inequality):
    a, b, c, relation = inequality
    lhs = a * x + b * y
    if relation == "<=":
        return lhs <= c + 1e-8
    if relation == ">=":
        return lhs >= c - 1e-8
    if relation == "<":
        return lhs < c - 1e-8
    return lhs > c + 1e-8


# ================================================================
# TRÌNH BÀY MANIM
# ================================================================

def make_text(text, size=28, color=FG, max_width=None):
    obj = Text(
        text,
        font=FONT,
        font_size=size,
        color=color,
        line_spacing=0.85
    )
    if max_width is not None and obj.width > max_width:
        obj.scale_to_fit_width(max_width)
    return obj


def build_lines(lines, has_graph):
    wrap_width = 39 if has_graph else 80
    font_size = 27 if has_graph else 29
    maximum_width = 6.10 if has_graph else 12.75
    objects = []

    for index, line in enumerate(lines):
        wrapped = "\n".join(
            textwrap.wrap(
                line,
                width=wrap_width,
                break_long_words=False,
                break_on_hyphens=False
            )
        )
        if not wrapped:
            wrapped = " "

        color = FG
        if index == 0:
            color = ACCENT
        if index == len(lines) - 1:
            color = GOOD

        objects.append(
            make_text(
                wrapped,
                size=font_size,
                color=color,
                max_width=maximum_width
            )
        )

    group = VGroup(*objects).arrange(
        DOWN,
        aligned_edge=LEFT,
        buff=0.22 if has_graph else 0.24
    )

    if group.height > 5.55:
        group.scale_to_fit_height(5.55)

    group.to_edge(LEFT, buff=0.48)
    group.shift(UP * (2.58 - group.get_top()[1]))

    return group


def build_graph(spec):
    bounds = spec.get("range", [-4, 6, -4, 6])
    xmin, xmax, ymin, ymax = bounds

    # Hình có đủ chỗ cho nhãn trục, chú thích và footer.
    axes = Axes(
        x_range=[xmin, xmax, 1],
        y_range=[ymin, ymax, 1],
        x_length=5.35,
        y_length=4.85,
        axis_config={
            "color": "#B6C2D1",
            "stroke_width": 2,
            "include_ticks": True,
            "include_numbers": False,
            "tip_width": 0.12,
            "tip_height": 0.12
        }
    ).move_to([3.70, 0.05, 0])

    graph = VGroup()

    grid = VGroup()
    for x in range(math.ceil(xmin), math.floor(xmax) + 1):
        grid.add(
            Line(
                axes.c2p(x, ymin),
                axes.c2p(x, ymax),
                color="#304056",
                stroke_width=0.8
            )
        )
    for y in range(math.ceil(ymin), math.floor(ymax) + 1):
        grid.add(
            Line(
                axes.c2p(xmin, y),
                axes.c2p(xmax, y),
                color="#304056",
                stroke_width=0.8
            )
        )
    graph.add(grid)

    inequalities = spec["ineqs"]

    if spec.get("shade", True):
        vertices = [
            (xmin, ymin),
            (xmax, ymin),
            (xmax, ymax),
            (xmin, ymax)
        ]
        for inequality in inequalities:
            vertices = clip_polygon(vertices, inequality)

        if len(vertices) >= 3:
            region = Polygon(
                *[axes.c2p(x, y) for x, y in vertices],
                stroke_width=0,
                fill_color=GOOD,
                fill_opacity=0.24
            )
            graph.add(region)

    graph.add(axes)

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
    x_label.next_to(axes.c2p(xmax, 0), RIGHT, buff=0.07)

    y_label = make_text("y", size=21, color=MUTED)
    y_label.next_to(axes.c2p(0, ymax), UP, buff=0.07)

    graph.add(x_label, y_label)

    boundary_colors = [WARN, ACCENT, "#C4B5FD", "#F9A8D4"]

    for index, inequality in enumerate(inequalities):
        a, b, c, relation = inequality
        ends = line_rectangle_intersections(a, b, c, bounds)
        if ends is None:
            continue

        p, q = ends
        color = boundary_colors[index % len(boundary_colors)]

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
        lattice = VGroup()
        for x in range(math.ceil(xmin), math.floor(xmax) + 1):
            for y in range(math.ceil(ymin), math.floor(ymax) + 1):
                if all(
                    point_satisfies(x, y, inequality)
                    for inequality in inequalities
                ):
                    lattice.add(
                        Dot(
                            axes.c2p(x, y),
                            radius=0.041,
                            color=GOOD
                        )
                    )
        graph.add(lattice)

    points = spec.get("points", [])
    for x, y, label_text in points:
        point = Dot(
            axes.c2p(x, y),
            radius=0.058,
            color=FG
        )
        label = make_text(
            label_text,
            size=18,
            color=FG,
            max_width=1.7
        )

        direction = UR
        if x >= xmax - 1.5:
            direction = UL
        if y >= ymax - 1.0:
            direction = DR

        label.next_to(point, direction, buff=0.09)

        # Nền tối giúp nhãn đọc được trên vùng tô.
        label.add_background_rectangle(
            color=BG,
            opacity=0.82,
            buff=0.035
        )
        graph.add(point, label)

    caption = make_text(
        spec.get("caption", ""),
        size=23,
        color=GOOD,
        max_width=5.65
    ).move_to([3.65, -2.93, 0])

    graph.add(caption)
    return graph


class BaiGiangBatPhuongTrinh(Scene):
    def construct(self):
        if not TIMING_FILE.exists():
            raise RuntimeError(
                "Thiếu âm thanh. Chạy trước: "
                "python bai_giang_bat_phuong_trinh.py --prepare"
            )

        timing = json.loads(
            TIMING_FILE.read_text(encoding="utf-8")
        )
        durations = timing["durations"]

        if len(durations) != len(SLIDES):
            raise RuntimeError(
                "Dữ liệu âm thanh không khớp. Hãy chạy lại --prepare."
            )

        # Footer cố định xuyên suốt.
        footer_background = Rectangle(
            width=config.frame_width,
            height=0.53,
            stroke_width=0,
            fill_color="#0A1020",
            fill_opacity=1
        ).to_edge(DOWN, buff=0).set_z_index(100)

        footer_line = Line(
            [-config.frame_width / 2, -3.47, 0],
            [config.frame_width / 2, -3.47, 0],
            stroke_width=1.6,
            color=ACCENT
        ).set_z_index(101)

        footer_name = make_text(
            "Thầy Nguyễn Văn Sang",
            size=22,
            color=FG
        ).move_to([0, -3.75, 0]).set_z_index(102)

        footer_subject = make_text(
            "TOÁN HỌC • BẤT PHƯƠNG TRÌNH HAI ẨN",
            size=13,
            color=MUTED,
            max_width=4.55
        ).to_edge(LEFT, buff=0.30)
        footer_subject.set_y(-3.75).set_z_index(102)

        self.add(
            footer_background,
            footer_line,
            footer_name,
            footer_subject
        )

        for index, slide in enumerate(SLIDES):
            title = make_text(
                slide["title"],
                size=33,
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
            body = build_lines(slide["lines"], has_graph)

            content = VGroup(title, header_rule, body)

            if has_graph:
                divider = Line(
                    [0.05, -2.70, 0],
                    [0.05, 2.60, 0],
                    color="#304056",
                    stroke_width=1
                )
                graph = build_graph(slide["graph"])
                content.add(divider, graph)

            self.add(counter)
            self.play(
                FadeIn(content, shift=UP * 0.08),
                run_time=ENTER_TIME
            )

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            if not audio_path.exists():
                raise RuntimeError(f"Thiếu tệp: {audio_path}")

            self.add_sound(str(audio_path))
            audio_length = durations[index]

            # Thanh tiến độ dưới nội dung.
            # Không dùng phụ đề tự động để tránh lệch lời đọc.
            progress_start = LEFT * 6.60 + DOWN * 3.25
            progress_end = RIGHT * 6.60 + DOWN * 3.25

            track = Line(
                progress_start,
                progress_end,
                color="#26364A",
                stroke_width=3
            )
            progress = Line(
                progress_start,
                progress_end,
                color=ACCENT,
                stroke_width=3
            )

            self.add(track)
            self.play(
                Create(progress),
                run_time=audio_length,
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
            "1. python bai_giang_bat_phuong_trinh.py --prepare\n"
            "2. manim -qm --fps 24 "
            "bai_giang_bat_phuong_trinh.py BaiGiangBatPhuongTrinh"
        )
'''

SCRIPT.write_text(SOURCE, encoding="utf-8")

# Kiểm tra cú pháp trước khi tạo giọng và render.
compile(SOURCE, str(SCRIPT), "exec")

print("\nBƯỚC 2/4: Tạo giọng nam tiếng Việt và căn thời lượng...")
run_command([
    sys.executable,
    str(SCRIPT),
    "--prepare"
])

print("\nBƯỚC 3/4: Manim đang dựng video 720p...")
print("Thầy giữ Colab kết nối cho đến khi xuất hiện thông báo hoàn tất.")

MEDIA_DIR = WORK / "media"

run_command([
    sys.executable,
    "-m", "manim",
    "-qm",
    "--fps", "24",
    "--disable_caching",
    "--media_dir", str(MEDIA_DIR),
    "-o", "Bat_phuong_trinh_Thay_Nguyen_Van_Sang",
    str(SCRIPT),
    "BaiGiangBatPhuongTrinh"
])

candidates = [
    path
    for path in MEDIA_DIR.rglob(
        "Bat_phuong_trinh_Thay_Nguyen_Van_Sang.mp4"
    )
    if "partial_movie_files" not in str(path)
]

if not candidates:
    raise FileNotFoundError(
        "Chưa tìm thấy video hoàn chỉnh. "
        "Thầy xem thông báo lỗi ở phần dựng Manim phía trên."
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
print(f"Dung lượng: {VIDEO_PATH.stat().st_size / (1024**2):.1f} MB")
print(f"Mã nguồn Python: {SCRIPT}")

# Lưu thêm bản kịch bản dễ xem, dễ sửa.
# Kịch bản chính đã được nhúng đầy đủ trong file .py.
EXPORT_SCRIPT = WORK / "xuat_kich_ban.py"
EXPORT_SCRIPT.write_text(
    "import importlib.util, json\n"
    "from pathlib import Path\n"
    f"p = Path({str(SCRIPT)!r})\n"
    "spec = importlib.util.spec_from_file_location('lesson', p)\n"
    "m = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(m)\n"
    "out = p.parent / 'kich_ban_bai_giang.json'\n"
    "out.write_text(json.dumps(m.SLIDES, ensure_ascii=False, indent=2), "
    "encoding='utf-8')\n",
    encoding="utf-8"
)
run_command([sys.executable, str(EXPORT_SCRIPT)])

# Nút tải, có thể bấm lại nếu trình duyệt chặn tải tự động.
from IPython.display import display
import ipywidgets as widgets
from google.colab import files

download_video = widgets.Button(
    description="Tải video MP4",
    button_style="success",
    layout=widgets.Layout(width="210px")
)

download_source = widgets.Button(
    description="Tải mã nguồn .py",
    button_style="info",
    layout=widgets.Layout(width="210px")
)

download_script = widgets.Button(
    description="Tải kịch bản JSON",
    layout=widgets.Layout(width="210px")
)

download_video.on_click(lambda _: files.download(str(VIDEO_PATH)))
download_source.on_click(lambda _: files.download(str(SCRIPT)))
download_script.on_click(
    lambda _: files.download(str(WORK / "kich_ban_bai_giang.json"))
)

display(widgets.HBox([
    download_video,
    download_source,
    download_script
]))

print("\nĐang gửi yêu cầu tải video xuống máy...")
print("Nếu chưa tải được, thầy bấm nút 'Tải video MP4' phía trên.")
files.download(str(VIDEO_PATH))
