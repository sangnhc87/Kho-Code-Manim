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

WORK = Path("/content/he_bat_phuong_trinh_hai_an")
WORK.mkdir(parents=True, exist_ok=True)
SCRIPT = WORK / "he_bat_phuong_trinh_hai_an.py"

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
        "title": "HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN",
        "lines": [
            "Bài tiếp theo: Kết hợp nhiều điều kiện cùng lúc",
            "Mục tiêu 1. Nhận biết hệ và kiểm tra một cặp nghiệm.",
            "Mục tiêu 2. Biểu diễn miền nghiệm chung trên mặt phẳng.",
            "Mục tiêu 3. Tìm giao điểm và các đỉnh của miền nghiệm.",
            "Mục tiêu 4. Lập mô hình và giải bài toán thực tế.",
            "Chuẩn bị: giấy nháp, bút, thước kẻ."
        ],
        "narration": (
            "Chào các em. Ở bài trước, chúng ta đã biết biểu diễn miền nghiệm "
            "của một bất phương trình bậc nhất hai ẩn. Hôm nay, chúng ta "
            "kết hợp nhiều bất phương trình thành một hệ. Bài học có bốn "
            "mục tiêu: nhận biết hệ và kiểm tra nghiệm; xác định miền nghiệm "
            "chung; tìm giao điểm và các đỉnh; cuối cùng là vận dụng vào "
            "bài toán thực tế. Các em hãy chuẩn bị thước kẻ và giấy nháp. "
            "Khi gặp phần luyện tập, hãy dừng video, tự giải trước rồi "
            "đối chiếu với lời giải."
        )
    },
    {
        "title": "1. ÔN NHANH KIẾN THỨC NỀN",
        "lines": [
            "Với một bất phương trình $ax + by \le c$:",
            "Bước 1. Vẽ đường biên $ax + by = c$.",
            "Bước 2. Chọn điểm thử không nằm trên đường biên.",
            "Bước 3. Thử đúng: chọn phía chứa điểm thử; sai: chọn phía còn lại.",
            "Bước 4. Dấu $\le, \ge$: lấy biên. Dấu $<, >$: bỏ biên.",
            "Trong bài này: vùng xanh biểu diễn miền nghiệm chung.",
            "Lưu ý: không dùng $O$ làm điểm thử nếu $O$ nằm trên biên."
        ],
        "narration": (
            "Trước hết, ta ôn lại quy trình của một bất phương trình. "
            "Vẽ đường biên bằng cách thay dấu bất phương trình bằng dấu "
            "bằng. Chọn một điểm thử không thuộc đường biên, rồi thay tọa "
            "độ vào. Nếu đúng, chọn phía chứa điểm thử; nếu sai, chọn "
            "phía còn lại. Cuối cùng, dấu có bằng thì lấy biên, dấu không "
            "có bằng thì bỏ biên. Chú ý gốc tọa độ không phải lúc nào "
            "cũng dùng được. Với một hệ, ta thực hiện cách làm này cho "
            "từng điều kiện rồi tìm phần chung."
        )
    },
    {
        "title": "2. HỆ LÀ NHIỀU ĐIỀU KIỆN ĐỒNG THỜI",
        "lines": [
            "Hệ gồm nhiều bất phương trình bậc nhất cùng hai ẩn.",
            "Ví dụ: $x \ge 0; y \ge 0; x + y \le 4$.",
            "Một cặp $(x_0; y_0)$ là nghiệm của hệ khi:",
            "NÓ THỎA MÃN TẤT CẢ CÁC BẤT PHƯƠNG TRÌNH.",
            "Chỉ cần sai một điều kiện $\implies$ không là nghiệm của hệ.",
            "Miền nghiệm của hệ là GIAO các miền nghiệm thành phần.",
            "Từ khóa quan trọng: ĐỒNG THỜI, không phải CHỈ MỘT."
        ],
        "narration": (
            "Hệ bất phương trình bậc nhất hai ẩn gồm nhiều bất phương "
            "trình bậc nhất có cùng hai ẩn x và y. Một cặp số là nghiệm "
            "của hệ khi nó thỏa mãn đồng thời tất cả các bất phương "
            "trình. Ví dụ, với x không âm, y không âm và x cộng y "
            "không vượt quá bốn, cả ba điều kiện đều phải đúng. "
            "Chỉ cần một điều kiện sai, cặp số đó không phải nghiệm. "
            "Về hình học, miền nghiệm của hệ là phần giao, tức phần "
            "chung của tất cả các miền nghiệm thành phần."
        )
    },
    {
        "title": "VÍ DỤ 1. KIỂM TRA NGHIỆM CỦA HỆ",
        "lines": [
            "Xét hệ: $x \ge 0; y \ge 0; x + y \le 4$.",
            "$A(1; 2): 1 \ge 0; 2 \ge 0; 1 + 2 = 3 \le 4$.",
            "$\implies A$ là nghiệm của hệ.",
            "$B(-1; 2): -1 \ge 0$ là sai.",
            "$\implies B$ không là nghiệm, dù $-1 + 2 \le 4$.",
            "$C(3; 2): 3 + 2 = 5 > 4 \implies$ không là nghiệm.",
            "$D(0; 4):$ cả ba điều kiện đúng $\implies$ là nghiệm.",
            "Kết luận: trong bốn điểm, $A$ và $D$ là nghiệm."
        ],
        "narration": (
            "Ta kiểm tra bốn điểm với hệ vừa nêu. Điểm A, một, hai "
            "có hai tọa độ không âm và tổng bằng ba, nên là nghiệm. "
            "Điểm B, âm một, hai có tổng không vượt quá bốn, nhưng "
            "hoành độ âm nên bị loại. Điểm C, ba, hai có tọa độ "
            "không âm, nhưng tổng bằng năm, lớn hơn bốn, nên cũng "
            "bị loại. Điểm D, không, bốn thỏa mãn cả ba điều kiện, "
            "kể cả trường hợp bằng nhau. Kết luận, A và D là "
            "nghiệm. Tuyệt đối không kiểm tra riêng một bất phương trình."
        )
    },
    {
        "title": "3. QUY TRÌNH BIỂU DIỄN MIỀN NGHIỆM",
        "lines": [
            "Bước 1. Vẽ tất cả đường biên trên cùng hệ trục.",
            "Bước 2. Xác định miền nghiệm của từng bất phương trình.",
            "Bước 3. Giữ lại phần thuộc đồng thời mọi miền.",
            "Bước 4. Kiểm tra nét liền, nét đứt và các giao điểm.",
            "Nếu cần: tìm tọa độ các đỉnh bằng cách giải hệ phương trình.",
            "Kiểm tra lại: mọi đỉnh được nhận phải thỏa mãn toàn bộ hệ.",
            "Không phải giao điểm nào của các đường biên cũng là đỉnh!"
        ],
        "narration": (
            "Để biểu diễn miền nghiệm của hệ, ta vẽ các đường biên "
            "trên cùng một hệ trục. Sau đó xác định phía cần lấy "
            "đối với từng bất phương trình. Chỉ giữ lại phần thuộc "
            "đồng thời tất cả các miền. Tiếp theo, kiểm tra những "
            "đường biên được lấy hoặc bị loại. Nếu bài toán yêu cầu "
            "tìm đỉnh, ta giải các hệ phương trình đường biên. "
            "Tuy nhiên, không phải mọi giao điểm đều là đỉnh của "
            "miền nghiệm. Mỗi điểm tìm được vẫn phải được kiểm tra "
            "với toàn bộ các điều kiện."
        )
    },
    {
        "title": "VÍ DỤ 2. MIỀN NGHIỆM HÌNH TAM GIÁC",
        "lines": [
            "Hệ: $x \ge 0; y \ge 0; x + y \le 4$.",
            "$x \ge 0$: phía phải trục $Oy$.",
            "$y \ge 0$: phía trên trục $Ox$.",
            "$d: x + y = 4$ qua $(4; 0), (0; 4)$.",
            "Thử $O: 0 \le 4$ là đúng.",
            "Phần chung là tam giác $OAB$.",
            "$O(0; 0), A(4; 0), B(0; 4)$.",
            "Lấy cả ba cạnh và ba đỉnh."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 4, "<="]
            ],
            "points": [[0, 0, "O"], [4, 0, "A"], [0, 4, "B"]],
            "caption": "Miền nghiệm: tam giác kể cả biên"
        },
        "narration": (
            "Xét hệ x không âm, y không âm và x cộng y nhỏ hơn "
            "hoặc bằng bốn. Hai điều kiện đầu giới hạn miền vào "
            "góc phần tư thứ nhất, kể cả hai nửa trục dương. "
            "Đường x cộng y bằng bốn đi qua bốn, không và không, "
            "bốn. Gốc tọa độ thỏa mãn điều kiện thứ ba nên chọn "
            "phía chứa O. Phần chung là tam giác có ba đỉnh "
            "không, không; bốn, không; và không, bốn. Cả ba dấu "
            "đều có bằng, vì vậy miền nghiệm chứa toàn bộ các "
            "cạnh và các đỉnh của tam giác."
        )
    },
    {
        "title": "VÍ DỤ 3. THÊM MỘT ĐIỀU KIỆN",
        "lines": [
            "Hệ: $x \ge 0; y \ge 0; x + y \le 4; 2x + y \le 6$.",
            "Bắt đầu từ tam giác ví dụ 2.",
            "Thêm $d_2: 2x + y = 6$.",
            "$d_2$ qua $(3; 0), (0; 6)$.",
            "$O$ thỏa mãn: chọn phía chứa $O$.",
            "Điểm $(4; 0)$ bị loại vì $8 > 6$.",
            "Phần chung còn lại là tứ giác.",
            "Thêm điều kiện: miền không rộng ra."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="],
                [0, 1, 0, ">="],
                [1, 1, 4, "<="],
                [2, 1, 6, "<="]
            ],
            "range": [-1, 7, -1, 7],
            "points": [
                [0, 0, "O"], [3, 0, "A"],
                [2, 2, "B"], [0, 4, "C"]
            ],
            "caption": "Thêm điều kiện → lấy phần giao"
        },
        "narration": (
            "Bây giờ thêm điều kiện hai x cộng y nhỏ hơn hoặc "
            "bằng sáu vào ví dụ trước. Đường biên mới đi qua "
            "ba, không và không, sáu. Thử O, ta có không nhỏ "
            "hơn hoặc bằng sáu, nên chọn phía chứa O. Điểm "
            "bốn, không từng thuộc miền cũ nay bị loại, vì "
            "hai nhân bốn bằng tám, lớn hơn sáu. Miền nghiệm "
            "còn lại là tứ giác tô xanh. Điều này cho thấy "
            "một nguyên tắc: thêm một điều kiện vào hệ chỉ "
            "có thể giữ nguyên hoặc thu hẹp miền nghiệm, không "
            "thể làm miền nghiệm rộng ra."
        )
    },
    {
        "title": "VÍ DỤ 3. TÌM ĐỦ CÁC ĐỈNH",
        "lines": [
            "Giao hai đường xiên:",
            "$x + y = 4; 2x + y = 6$.",
            "Lấy phương trình sau trừ trước:",
            "$x = 2 \implies y = 2 \implies B(2; 2)$.",
            "Trên $Ox: y = 0 \implies x \le 4, x \le 3$.",
            "Kết hợp $x \ge 0 \implies 0 \le x \le 3$.",
            "Trên $Oy: x = 0 \implies 0 \le y \le 4$.",
            "Các đỉnh: $O(0; 0), A(3; 0), B(2; 2), C(0; 4)$."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="], [0, 1, 0, ">="],
                [1, 1, 4, "<="], [2, 1, 6, "<="]
            ],
            "points": [
                [0, 0, "O"], [3, 0, "A"],
                [2, 2, "B"], [0, 4, "C"]
            ],
            "caption": "Kiểm tra đỉnh với toàn bộ hệ"
        },
        "narration": (
            "Ta tìm chính xác các đỉnh của tứ giác. Giao hai "
            "đường xiên thỏa mãn x cộng y bằng bốn và hai x "
            "cộng y bằng sáu. Trừ hai phương trình được x bằng "
            "hai, rồi suy ra y bằng hai. Trên trục hoành, "
            "đặt y bằng không: x phải đồng thời không vượt "
            "quá bốn và không vượt quá ba, nên giới hạn là "
            "ba. Trên trục tung, đặt x bằng không, giới hạn "
            "chặt hơn là y không vượt quá bốn. Kết hợp gốc "
            "tọa độ, ta được đủ bốn đỉnh đang hiển thị."
        )
    },
    {
        "title": "VÍ DỤ 4. CÓ DẤU NGHIÊM NGẶT",
        "lines": [
            "Hệ: $x \ge 0; y \ge 0; x + y < 4$.",
            "Hình dạng giống ví dụ tam giác.",
            "Nhưng đường $x + y = 4$ bị loại.",
            "Vẽ đường xiên bằng nét đứt.",
            "$(1; 1)$: tổng $2 < 4 \implies$ nhận.",
            "$(2; 2)$: tổng $4 < 4$ sai $\implies$ loại.",
            "$O$ được nhận; $(4; 0), (0; 4)$ bị loại.",
            "Trên $Ox$ chỉ lấy $0 \le x < 4$.",
            "Trên $Oy$ chỉ lấy $0 \le y < 4$."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="], [0, 1, 0, ">="],
                [1, 1, 4, "<"]
            ],
            "points": [
                [0, 0, "O"], [1, 1, "M"], [2, 2, "N"]
            ],
            "open_points": [[4, 0], [0, 4], [2, 2]],
            "caption": "Cạnh xiên và hai đầu mút bị loại"
        },
        "narration": (
            "Nếu đổi điều kiện cuối thành x cộng y nhỏ hơn "
            "bốn, không có dấu bằng, thì đường xiên không "
            "thuộc miền nghiệm. Điểm một, một được nhận vì "
            "tổng bằng hai. Điểm hai, hai bị loại vì tổng "
            "bằng bốn. Gốc tọa độ vẫn được nhận, nhưng hai "
            "điểm bốn, không và không, bốn bị loại. Chú ý "
            "dù các trục được vẽ nét liền, hai đầu mút ấy "
            "vẫn phải thỏa mãn điều kiện cuối. Vì vậy, khi "
            "xét một giao điểm, ta phải kiểm tra tất cả "
            "bất phương trình, không chỉ một đường biên."
        )
    },
    {
        "title": "VÍ DỤ 5. MIỀN KHÔNG BỊ CHẶN",
        "lines": [
            "Hệ: $x \ge 0; y \ge 0; x + y \ge 3$.",
            "Hai điều kiện đầu: góc phần tư I.",
            "$d: x + y = 3$.",
            "$O$ không thỏa mãn: $0 \ge 3$ sai.",
            "Chọn phía không chứa $O$.",
            "Lấy đường biên vì có dấu $\ge$.",
            "Miền kéo dài vô hạn lên trên, sang phải.",
            "Không phải miền nào cũng là đa giác",
            "bị chặn như tam giác hoặc tứ giác."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="], [0, 1, 0, ">="],
                [1, 1, 3, ">="]
            ],
            "points": [[3, 0, "A"], [0, 3, "B"], [4, 4, "M"]],
            "caption": "Hình chỉ vẽ một phần miền vô hạn"
        },
        "narration": (
            "Miền nghiệm không phải lúc nào cũng nằm gọn trong "
            "một hình hữu hạn. Xét x không âm, y không âm "
            "và x cộng y lớn hơn hoặc bằng ba. Trong góc "
            "phần tư thứ nhất, ta chọn phía của đường x "
            "cộng y bằng ba không chứa gốc tọa độ. Miền "
            "nghiệm kéo dài vô hạn lên trên và sang phải. "
            "Các mép của khung hình không phải đường biên "
            "của hệ. Đây chỉ là cửa sổ quan sát một phần "
            "miền nghiệm. Các em cần phân biệt miền bị "
            "chặn với miền không bị chặn."
        )
    },
    {
        "title": "VÍ DỤ 6. HỆ VÔ NGHIỆM",
        "lines": [
            "Xét hệ: $x + y \le 1; x + y \ge 3$.",
            "Cùng một tổng không thể vừa $\le 1$",
            "lại vừa $\ge 3$.",
            "Hai miền không có phần chung.",
            "Kết luận: hệ vô nghiệm.",
            "Miền nghiệm là tập rỗng: $\emptyset$.",
            "Không tô xanh vì không có điểm chung."
        ],
        "graph": {
            "ineqs": [[1, 1, 1, "<="], [1, 1, 3, ">="]],
            "range": [-3, 5, -3, 5],
            "caption": "Không có phần giao: miền nghiệm rỗng",
            "empty": True
        },
        "narration": (
            "Xét hệ x cộng y nhỏ hơn hoặc bằng một, đồng "
            "thời x cộng y lớn hơn hoặc bằng ba. Cùng một "
            "giá trị không thể vừa không vượt quá một lại "
            "vừa không nhỏ hơn ba. Vì thế không tồn tại "
            "cặp số nào thỏa mãn. Về hình học, hai nửa "
            "mặt phẳng cần lấy nằm tách nhau và không có "
            "phần chung. Hệ này vô nghiệm, miền nghiệm là "
            "tập rỗng. Ví dụ cho thấy không cần lúc nào "
            "cũng vẽ thật chi tiết: phát hiện mâu thuẫn "
            "đại số có thể giúp kết luận ngay."
        )
    },
    {
        "title": "BÀI TẬP 1. MIỀN NGHIỆM HÌNH CHỮ NHẬT",
        "lines": [
            "Đề bài: $-1 \le x \le 2; 0 \le y \le 3$.",
            "Tách thành bốn bất phương trình:",
            "$x \ge -1; x \le 2; y \ge 0; y \le 3$.",
            "Hai đường đứng: $x = -1, x = 2$.",
            "Hai đường ngang: $y = 0, y = 3$.",
            "Lấy phần nằm giữa từng cặp đường.",
            "Đỉnh: $A(-1; 0), B(2; 0), C(2; 3), D(-1; 3)$.",
            "Lấy cả bốn cạnh."
        ],
        "graph": {
            "ineqs": [
                [1, 0, -1, ">="], [1, 0, 2, "<="],
                [0, 1, 0, ">="], [0, 1, 3, "<="]
            ],
            "range": [-3, 5, -2, 5],
            "points": [
                [-1, 0, "A"], [2, 0, "B"],
                [2, 3, "C"], [-1, 3, "D"]
            ],
            "caption": "Hình chữ nhật ABCD kể cả biên"
        },
        "narration": (
            "Bài tập thứ nhất: biểu diễn hệ âm một nhỏ "
            "hơn hoặc bằng x nhỏ hơn hoặc bằng hai, và "
            "không nhỏ hơn hoặc bằng y nhỏ hơn hoặc bằng "
            "ba. Ta tách thành bốn bất phương trình. Hai "
            "điều kiện của x tạo một dải giữa hai đường "
            "thẳng đứng. Hai điều kiện của y tạo một dải "
            "giữa hai đường nằm ngang. Phần giao là hình "
            "chữ nhật với bốn đỉnh đang hiển thị. Mọi "
            "dấu đều có bằng nên lấy cả các cạnh. Các "
            "em hãy tự kiểm tra tâm của hình có thỏa "
            "mãn toàn bộ hệ không."
        )
    },
    {
        "title": "BÀI TẬP 2. KẾT HỢP HAI PHÍA TRÊN, DƯỚI",
        "lines": [
            "Hệ: $y \ge x - 1; y \le -x + 3; x \ge 0$.",
            "Trên $d_1: y = x - 1$.",
            "Dưới $d_2: y = -x + 3$.",
            "Bên phải trục $Oy$.",
            "Giao hai đường: $x - 1 = -x + 3$.",
            "$2x = 4 \implies x = 2 \implies y = 1$.",
            "Trên $Oy: -1 \le y \le 3$.",
            "Đỉnh: $A(0; -1), B(0; 3), C(2; 1)$.",
            "Không được tự thêm điều kiện $y \ge 0$!"
        ],
        "graph": {
            "ineqs": [
                [1, -1, 1, "<="],
                [1, 1, 3, "<="],
                [1, 0, 0, ">="]
            ],
            "range": [-2, 5, -2, 5],
            "points": [[0, -1, "A"], [0, 3, "B"], [2, 1, "C"]],
            "caption": "Miền nghiệm có cả điểm tung độ âm"
        },
        "narration": (
            "Bài tập thứ hai kết hợp ba phía: trên đường "
            "y bằng x trừ một, dưới đường y bằng âm "
            "x cộng ba, và bên phải trục tung. Giao "
            "hai đường xiên được tìm từ x trừ một "
            "bằng âm x cộng ba. Suy ra x bằng hai, "
            "y bằng một. Trên trục tung, y chạy từ "
            "âm một đến ba. Miền nghiệm là tam giác "
            "có ba đỉnh không, âm một; không, ba; "
            "và hai, một. Đặc biệt, đề không yêu cầu "
            "y không âm. Không được tự ý bỏ phần "
            "nằm dưới trục hoành."
        )
    },
    {
        "title": "4. THỰC TẾ: LẬP KẾ HOẠCH SẢN XUẤT",
        "lines": [
            "Một xưởng sản xuất hai loại sản phẩm A và B.",
            "Mỗi A cần 2 giờ; mỗi B cần 1 giờ. Có tối đa 8 giờ.",
            "Mỗi sản phẩm dùng 1 đơn vị gỗ. Có tối đa 5 đơn vị gỗ.",
            "Lãi mỗi A: 300 nghìn đồng; mỗi B: 200 nghìn đồng.",
            "Gọi $x, y$ lần lượt là số sản phẩm A, B.",
            "Thời gian: $2x + y \le 8$. Gỗ: $x + y \le 5$.",
            "Điều kiện: $x, y$ là số nguyên không âm.",
            "Câu hỏi: sản xuất thế nào để tổng tiền lãi lớn nhất?"
        ],
        "narration": (
            "Ta xét một bài toán thực tế. Một xưởng sản "
            "xuất hai loại sản phẩm A và B. Mỗi A "
            "cần hai giờ, mỗi B cần một giờ, tổng "
            "thời gian không vượt quá tám giờ. Mỗi "
            "sản phẩm dùng một đơn vị gỗ, và xưởng "
            "có năm đơn vị. Tiền lãi mỗi A là ba "
            "trăm nghìn đồng, mỗi B là hai trăm nghìn "
            "đồng. Gọi x và y là số sản phẩm từng "
            "loại. Ta cần lập các ràng buộc và tìm "
            "phương án có tổng tiền lãi lớn nhất."
        )
    },
    {
        "title": "THỰC TẾ: MIỀN PHƯƠNG ÁN KHẢ THI",
        "lines": [
            "Hệ: $x \ge 0; y \ge 0; 2x + y \le 8; x + y \le 5$.",
            "Giao hai đường xiên: $2x + y = 8; x + y = 5$.",
            "Trừ hai phương trình: $x = 3$.",
            "Suy ra $y = 2 \implies B(3; 2)$.",
            "Trên $Ox: x \le \min(4; 5) = 4$.",
            "Trên $Oy: y \le \min(8; 5) = 5$.",
            "Đỉnh: $O(0; 0), A(4; 0), B(3; 2), C(0; 5)$."
        ],
        "graph": {
            "ineqs": [
                [1, 0, 0, ">="], [0, 1, 0, ">="],
                [2, 1, 8, "<="], [1, 1, 5, "<="]
            ],
            "range": [-1, 6, -1, 6],
            "points": [
                [0, 0, "O"], [4, 0, "A"],
                [3, 2, "B"], [0, 5, "C"]
            ],
            "lattice": True,
            "caption": "Phương án thực tế: các điểm nguyên"
        },
        "narration": (
            "Các điều kiện tạo thành hệ đang hiển thị. "
            "Trước hết xét miền nghiệm với x và y "
            "là số thực. Giao hai đường xiên được "
            "tính bằng cách lấy hai x cộng y bằng "
            "tám trừ x cộng y bằng năm. Ta được "
            "x bằng ba, y bằng hai. Trên trục hoành, "
            "giới hạn là bốn; trên trục tung, giới "
            "hạn là năm. Miền nghiệm là tứ giác có "
            "bốn đỉnh O, A, B, C. Trong sản xuất, "
            "chỉ những điểm có tọa độ nguyên không "
            "âm mới là phương án phù hợp."
        )
    },
    {
        "title": "MỞ RỘNG: SO SÁNH TIỀN LÃI TẠI CÁC ĐỈNH",
        "lines": [
            "Tổng lãi: $P = 300x + 200y$ (nghìn đồng).",
            "Trên miền đa giác kín, bị chặn, khác rỗng:",
            "Hàm tuyến tính đạt GTLN tại ít nhất một đỉnh.",
            "$O(0; 0): P = 0$.",
            "$A(4; 0): P = 300 \cdot 4 = 1200$.",
            "$B(3; 2): P = 300 \cdot 3 + 200 \cdot 2 = 1300$.",
            "$C(0; 5): P = 200 \cdot 5 = 1000$.",
            "Lớn nhất: $1300$ nghìn đồng tại $B(3; 2)$."
        ],
        "narration": (
            "Tổng tiền lãi, tính bằng nghìn đồng, là "
            "P bằng ba trăm x cộng hai trăm y. "
            "Ta dùng một kết quả mở rộng: trên miền "
            "đa giác kín, bị chặn và khác rỗng, "
            "hàm tuyến tính đạt giá trị lớn nhất "
            "tại ít nhất một đỉnh. Tại O, tiền "
            "lãi bằng không. Tại A, lãi một nghìn "
            "hai trăm. Tại B, lãi một nghìn ba "
            "trăm. Tại C, lãi một nghìn. Vì vậy "
            "giá trị lớn nhất trên miền liên tục "
            "là một nghìn ba trăm nghìn đồng, "
            "đạt tại ba, hai."
        )
    },
    {
        "title": "THỰC TẾ: KẾT LUẬN VÀ KIỂM TRA",
        "lines": [
            "Chọn $x = 3, y = 2$: sản xuất 3 SP A và 2 SP B.",
            "Thời gian: $2(3) + 2 = 8$ giờ $\implies$ đúng giới hạn.",
            "Gỗ: $3 + 2 = 5$ đơn vị $\implies$ đúng giới hạn.",
            "Số sản phẩm nguyên, không âm $\implies$ hợp lệ.",
            "Lãi lớn nhất: 1 300 000 đồng.",
            "Vì nghiệm tối ưu liên tục này có tọa độ nguyên,",
            "nó cũng tối ưu cho bài toán sản xuất.",
            "Nếu đỉnh tối ưu không nguyên: KHÔNG tùy tiện làm tròn."
        ],
        "narration": (
            "Ta chọn sản xuất ba sản phẩm A và "
            "hai sản phẩm B. Kiểm tra thời gian: "
            "hai nhân ba cộng hai bằng tám giờ. "
            "Kiểm tra gỗ: ba cộng hai bằng năm "
            "đơn vị. Hai số lượng đều nguyên không "
            "âm nên phương án hợp lệ, với lãi "
            "một triệu ba trăm nghìn đồng. Vì "
            "đây đã là mức lớn nhất trên toàn "
            "miền liên tục, không điểm nguyên nào "
            "có thể cho mức cao hơn. Nhưng nếu "
            "đỉnh tối ưu có tọa độ không nguyên, "
            "không được tùy tiện làm tròn; cần "
            "xét thêm các phương án nguyên phù hợp."
        )
    },
    {
        "title": "BÀI TẬP 3. TỰ LUYỆN CÓ LỜI GIẢI",
        "lines": [
            "Hãy dừng video và giải: $x \ge 0; y \ge 0; x + y \le 6; x + 2y \le 8$.",
            "Giao hai đường: $x + y = 6; x + 2y = 8$.",
            "Trừ hai phương trình $\implies y = 2 \implies x = 4$.",
            "Trên $Ox: x \le 6$ và $x \le 8 \implies 0 \le x \le 6$.",
            "Trên $Oy: y \le 6$ và $2y \le 8 \implies 0 \le y \le 4$.",
            "Các đỉnh: $(0; 0), (6; 0), (4; 2), (0; 4)$.",
            "$M(5; 1)$ là nghiệm; $N(2; 4)$ không là nghiệm vì $2 + 8 > 8$."
        ],
        "narration": (
            "Bài tập tự luyện gồm x không âm, "
            "y không âm, x cộng y không vượt "
            "quá sáu và x cộng hai y không "
            "vượt quá tám. Các em hãy dừng "
            "video để vẽ. Giao hai đường xiên "
            "có y bằng hai, x bằng bốn. "
            "Trên trục hoành, giới hạn là sáu; "
            "trên trục tung, giới hạn là bốn. "
            "Kết hợp gốc tọa độ, ta được bốn "
            "đỉnh đã ghi. Điểm năm, một thỏa "
            "mãn toàn bộ hệ. Điểm hai, bốn "
            "không thỏa mãn điều kiện cuối, "
            "vì hai cộng tám lớn hơn tám."
        )
    },
    {
        "title": "5. NHỮNG LỖI CẦN TRÁNH",
        "lines": [
            "Lỗi 1. Lấy hợp các miền thay vì lấy giao.",
            "Sửa: một điểm phải thỏa mãn TẤT CẢ điều kiện.",
            "Lỗi 2. Tìm giao điểm rồi nhận ngay là đỉnh.",
            "Sửa: thay tọa độ vào toàn bộ hệ trước khi kết luận.",
            "Lỗi 3. Mặc định miền nghiệm luôn là đa giác bị chặn.",
            "Sửa: miền có thể không bị chặn, rỗng hoặc suy biến.",
            "Ví dụ suy biến: $x \ge 0; y \ge 0; x + y \le 0$ chỉ nhận $(0; 0)$.",
            "Lỗi 4. Quên dấu nghiêm ngặt hoặc điều kiện nguyên."
        ],
        "narration": (
            "Có bốn lỗi chính cần tránh. Thứ "
            "nhất, lấy hợp thay vì lấy giao "
            "các miền. Thứ hai, coi mọi giao "
            "điểm của các đường biên là đỉnh "
            "hợp lệ. Thứ ba, cho rằng miền "
            "nghiệm luôn là một đa giác bị "
            "chặn. Thực ra miền có thể không "
            "bị chặn, rỗng hoặc suy biến. "
            "Ví dụ, x và y không âm mà "
            "tổng không vượt quá không thì "
            "chỉ có điểm không, không. Cuối "
            "cùng, phải kiểm tra dấu nghiêm "
            "ngặt và các điều kiện thực tế "
            "như số lượng nguyên không âm."
        )
    },
    {
        "title": "TỔNG KẾT: BỐN TỪ KHÓA CẦN NHỚ",
        "lines": [
            "ĐỒNG THỜI: nghiệm phải thỏa mãn tất cả bất phương trình.",
            "PHẦN GIAO: miền nghiệm chung của các điều kiện.",
            "KIỂM TRA: đường biên, giao điểm và điều kiện bổ sung.",
            "VẬN DỤNG: đặt ẩn $\to$ lập hệ $\to$ tìm miền $\to$ kết luận.",
            "Tự đánh giá: em đã đạt bốn mục tiêu đầu bài chưa?",
            "Bài về nhà: tự vẽ lại ví dụ tứ giác và bài tự luyện.",
            "Cảm ơn các em đã theo dõi!",
            "Thầy Nguyễn Văn Sang"
        ],
        "narration": (
            "Bài học hôm nay được tóm tắt "
            "bằng bốn từ khóa: đồng thời, "
            "phần giao, kiểm tra và vận dụng. "
            "Một nghiệm phải thỏa mãn đồng "
            "thời mọi điều kiện; miền nghiệm "
            "là phần giao của các miền thành "
            "phần. Khi giải, hãy kiểm tra "
            "đường biên, giao điểm và điều "
            "kiện thực tế. Các em hãy tự "
            "đánh giá theo bốn mục tiêu đầu "
            "bài, rồi vẽ lại ví dụ tứ "
            "giác và bài tự luyện. Cảm ơn "
            "các em đã theo dõi bài học "
            "của thầy Nguyễn Văn Sang. "
            "Chúc các em học tốt!"
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

    (BASE / "kich_ban_he_bat_phuong_trinh.json").write_text(
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

class HeBatPhuongTrinhHaiAn(Scene):
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
            "TOÁN HỌC • HỆ BẤT PHƯƠNG TRÌNH HAI ẨN",
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


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        asyncio.run(prepare_audio())
    else:
        print(
            "Cách chạy:\n"
            "1. python he_bat_phuong_trinh_hai_an.py --prepare\n"
            "2. manim -qm --fps 24 he_bat_phuong_trinh_hai_an.py "
            "HeBatPhuongTrinhHaiAn"
        )
'''

SCRIPT.write_text(SOURCE, encoding="utf-8")

# Kiểm tra cú pháp trước khi tạo âm thanh.
compile(SOURCE, str(SCRIPT), "exec")

print("\nBƯỚC 2/4: Tạo giọng nam và căn thời lượng...")
run_command([
    sys.executable,
    str(SCRIPT),
    "--prepare"
])

print("\nBƯỚC 3/4: Dựng video Manim 720p...")
print("Thầy giữ Colab kết nối trong lúc dựng video.")
print("Thời gian dựng phụ thuộc tài nguyên Colab được cấp.")

MEDIA_DIR = WORK / "media"

run_command([
    sys.executable, "-m", "manim",
    "-qm",
    "--fps", "24",
    "--disable_caching",
    "--media_dir", str(MEDIA_DIR),
    "-o", "He_Bat_Phuong_Trinh_Thay_Nguyen_Van_Sang",
    str(SCRIPT),
    "HeBatPhuongTrinhHaiAn"
])

candidates = [
    path
    for path in MEDIA_DIR.rglob(
        "He_Bat_Phuong_Trinh_Thay_Nguyen_Van_Sang.mp4"
    )
    if "partial_movie_files" not in str(path)
]

if not candidates:
    raise FileNotFoundError(
        "Chưa tìm thấy video hoàn chỉnh. "
        "Thầy xem thông báo lỗi dựng video phía trên."
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
print(f"File Python: {SCRIPT}")

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
