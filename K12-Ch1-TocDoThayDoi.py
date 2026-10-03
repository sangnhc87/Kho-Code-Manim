# ============================================================
# GOOGLE COLAB: CHẠY TOÀN BỘ Ô NÀY
# 10 BÀI TOÁN TỐC ĐỘ THAY ĐỔI - ỨNG DỤNG ĐẠO HÀM
# Footer: Thầy Nguyễn Văn Sang
# ============================================================

import os
import sys
import shutil
import subprocess
from pathlib import Path

# ---------------- CẤU HÌNH ----------------
ROOT = Path("/content/manim_toc_do_thay_doi")
ROOT.mkdir(parents=True, exist_ok=True)

# 720p phù hợp để dựng trên Colab.
# Muốn 1080p: đổi thành "1920,1080", nhưng thời gian dựng tăng.
RESOLUTION = "1280,720"
FPS = "24"

# True: tự hiện yêu cầu tải video xuống sau khi dựng xong.
AUTO_DOWNLOAD = False

OUTPUT_NAME = "Toc_do_thay_doi_10_bai_Thay_Sang"
FINAL_VIDEO = Path("/content") / f"{OUTPUT_NAME}.mp4"

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

def run_checked(command, log_name):
    log_path = ROOT / log_name
    with open(log_path, "w", encoding="utf-8") as log:
        result = subprocess.run(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
    if result.returncode != 0:
        content = log_path.read_text(encoding="utf-8", errors="replace")
        print(content[-18000:])
        raise RuntimeError(
            f"Lệnh thất bại. Xem nhật ký: {log_path}"
        )

print("1/5 - Cài công cụ hệ thống...")

run_checked(
    ["apt-get", "update", "-qq"],
    "apt_update.log"
)

run_checked(
    [
        "apt-get", "install", "-y", "-qq",
        "ffmpeg",
        "pkg-config",
        "build-essential",
        "python3-dev",
        "libcairo2-dev",
        "libpango1.0-dev",
        "texlive-latex-base",
        "texlive-latex-recommended",
        "texlive-latex-extra",
        "texlive-fonts-recommended",
        "texlive-science",
        "dvisvgm",
        "fonts-dejavu-core",
        "espeak-ng",
    ],
    "apt_install.log"
)

print("2/5 - Cài Manim và thư viện giọng đọc...")

run_checked(
    [
        sys.executable, "-m", "pip", "install",
        "--quiet",
        "manim==0.19.0",
        "edge-tts",
    ],
    "pip_install.log"
)

# ============================================================
# MÃ DỰNG VIDEO
# ============================================================

SOURCE = r'''
from manim import *
from pathlib import Path
import asyncio
import hashlib
import json
import math
import subprocess
import sys
import textwrap

import edge_tts

ROOT = Path("/content/manim_toc_do_thay_doi")
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_FILE = ROOT / "audio_manifest.json"

VOICE = "vi-VN-NamMinhNeural"
VOICE_RATE = "+0%"

FONT = "DejaVu Sans"

BG = "#0B1220"
PANEL = "#142238"
BORDER = "#28415E"
WHITE_TEXT = "#EDF4FF"
MUTED = "#A9BED6"
BLUE = "#58B8FF"
CYAN = "#45E0D0"
YELLOW = "#FFD166"
GREEN = "#78E08F"
RED = "#FF7B88"

config.background_color = BG
config.frame_width = 14.2222222222
config.frame_height = 8
config.max_files_cached = 500

# ------------------------------------------------------------
# NỘI DUNG 10 BÀI
# Mỗi bài: đề + hình + 5 bước có thuyết minh riêng.
# ------------------------------------------------------------

TASKS = [
    {
        "title": "DIỆN TÍCH HÌNH TRÒN",
        "kind": "circle",
        "question": (
            "Bán kính hình tròn tăng với tốc độ 0,2 cm/s. "
            "Khi r = 5 cm, diện tích tăng với tốc độ bao nhiêu?"
        ),
        "intro": (
            "Bài một. Bán kính hình tròn tăng với tốc độ không phẩy "
            "hai xăng ti mét mỗi giây. Hỏi tại thời điểm bán kính bằng "
            "năm xăng ti mét, diện tích tăng nhanh bao nhiêu?"
        ),
        "steps": [
            (
                "1. Đặt biến và ghi dữ kiện",
                r"r=r(t),\quad S=S(t),\quad r=5,\quad \frac{dr}{dt}=0{,}2",
                "Gọi r là bán kính và S là diện tích tại thời điểm t. "
                "Cả hai đều là hàm của thời gian. Tại thời điểm cần xét, "
                "r bằng năm và đạo hàm của r theo t bằng không phẩy hai."
            ),
            (
                "2. Lập hệ thức hình học",
                r"S=\pi r^2",
                "Diện tích hình tròn bằng pi nhân bình phương bán kính. "
                "Đây là hệ thức liên hệ đại lượng cần tìm với đại lượng đã biết."
            ),
            (
                "3. Lấy đạo hàm hai vế theo thời gian",
                r"\frac{dS}{dt}=2\pi r\frac{dr}{dt}",
                "Lấy đạo hàm theo thời gian. Do r phụ thuộc vào t, "
                "phải dùng quy tắc hàm hợp: hai pi r nhân đạo hàm của r theo t."
            ),
            (
                "4. Thay số tại thời điểm đang xét",
                r"\left.\frac{dS}{dt}\right|_{r=5}=2\pi\cdot5\cdot0{,}2=2\pi",
                "Sau khi lấy đạo hàm, ta mới thay r bằng năm và tốc độ "
                "tăng bán kính bằng không phẩy hai. Kết quả là hai pi."
            ),
            (
                "5. Kết luận và đơn vị",
                r"\boxed{\frac{dS}{dt}=2\pi\approx6{,}28\ \mathrm{cm}^2/\mathrm{s}}",
                "Vậy diện tích tăng khoảng sáu phẩy hai tám xăng ti mét vuông "
                "mỗi giây. Chú ý đơn vị diện tích là xăng ti mét vuông, "
                "không phải xăng ti mét."
            ),
        ],
        "summary": "Hình tròn: S′ = 2π cm²/s",
    },
    {
        "title": "BÁN KÍNH QUẢ CẦU",
        "kind": "sphere",
        "question": (
            "Một quả bóng hình cầu được bơm với dV/dt = 36π cm³/s. "
            "Khi bán kính bằng 3 cm, tìm tốc độ tăng bán kính."
        ),
        "intro": (
            "Bài hai. Một quả bóng luôn có dạng hình cầu. "
            "Thể tích tăng với tốc độ ba mươi sáu pi xăng ti mét khối "
            "mỗi giây. Khi bán kính bằng ba xăng ti mét, "
            "hãy tìm tốc độ tăng bán kính."
        ),
        "steps": [
            (
                "1. Xác định đại lượng cần tìm",
                r"r=3,\quad \frac{dV}{dt}=36\pi,\quad \frac{dr}{dt}=?",
                "Đề cho tốc độ tăng thể tích, nhưng hỏi tốc độ tăng bán kính. "
                "Ta cần tìm đạo hàm của r theo thời gian."
            ),
            (
                "2. Công thức thể tích hình cầu",
                r"V=\frac{4}{3}\pi r^3",
                "Thể tích hình cầu bằng bốn phần ba pi nhân r mũ ba."
            ),
            (
                "3. Đạo hàm theo t",
                r"\frac{dV}{dt}=4\pi r^2\frac{dr}{dt}",
                "Lấy đạo hàm theo t. Hệ số ba triệt tiêu với mẫu ba. "
                "Ta được tốc độ tăng thể tích bằng bốn pi r bình phương "
                "nhân tốc độ tăng bán kính."
            ),
            (
                "4. Giải tìm tốc độ tăng bán kính",
                r"\frac{dr}{dt}=\frac{36\pi}{4\pi\cdot3^2}=1",
                "Chuyển bốn pi r bình phương xuống mẫu rồi thay số. "
                "Ba mươi sáu pi chia cho ba mươi sáu pi bằng một."
            ),
            (
                "5. Kết luận",
                r"\boxed{\frac{dr}{dt}=1\ \mathrm{cm}/\mathrm{s}}",
                "Tại thời điểm đang xét, bán kính tăng một xăng ti mét mỗi giây. "
                "Lưu ý: thể tích tăng đều không có nghĩa là bán kính cũng tăng đều."
            ),
        ],
        "summary": "Quả cầu: r′ = 1 cm/s",
    },
    {
        "title": "NƯỚC DÂNG TRONG BỂ TRỤ",
        "kind": "cylinder",
        "question": (
            "Bể trụ có bán kính đáy 2 m. Nước chảy vào 0,6 m³/phút, "
            "không chảy ra. Tìm tốc độ dâng của mực nước."
        ),
        "intro": (
            "Bài ba. Một bể hình trụ có bán kính đáy hai mét. "
            "Nước được bơm vào với lưu lượng không phẩy sáu mét khối mỗi phút "
            "và không có nước chảy ra. Tìm tốc độ dâng của mực nước "
            "khi bể chưa đầy."
        ),
        "steps": [
            (
                "1. Lưu lượng chính là tốc độ tăng thể tích",
                r"R=2,\quad \frac{dV}{dt}=0{,}6,\quad h=h(t)",
                "Gọi h là chiều cao cột nước. Vì không có nước chảy ra, "
                "đạo hàm của thể tích bằng lưu lượng nước chảy vào."
            ),
            (
                "2. Thể tích nước trong bể",
                r"V=\pi R^2h=4\pi h",
                "Thể tích nước bằng diện tích đáy nhân chiều cao. "
                "Bán kính đáy cố định bằng hai, nên V bằng bốn pi h."
            ),
            (
                "3. Lấy đạo hàm theo thời gian",
                r"\frac{dV}{dt}=4\pi\frac{dh}{dt}",
                "Lấy đạo hàm hai vế theo thời gian. "
                "Bốn pi là hằng số nên giữ nguyên."
            ),
            (
                "4. Tính tốc độ nước dâng",
                r"\frac{dh}{dt}=\frac{0{,}6}{4\pi}=\frac{3}{20\pi}",
                "Thay tốc độ tăng thể tích bằng không phẩy sáu. "
                "Suy ra tốc độ nước dâng bằng ba chia cho hai mươi pi."
            ),
            (
                "5. Kết luận",
                r"\boxed{\frac{dh}{dt}\approx0{,}0477\ \mathrm{m}/\mathrm{ph\acute{u}t}}",
                "Mực nước dâng khoảng không phẩy không bốn bảy bảy mét "
                "mỗi phút, tức khoảng bốn phẩy bảy bảy xăng ti mét mỗi phút. "
                "Trong bể trụ, tốc độ này không phụ thuộc vào độ sâu của nước."
            ),
        ],
        "summary": "Bể trụ: h′ ≈ 0,0477 m/phút",
    },
    {
        "title": "NƯỚC DÂNG TRONG BỂ NÓN",
        "kind": "cone",
        "question": (
            "Bể nón có đỉnh ở dưới, cao 6 m, bán kính miệng 3 m. "
            "Bơm vào 0,5 m³/phút. Khi nước sâu 2 m, tìm dh/dt."
        ),
        "intro": (
            "Bài bốn. Bể hình nón có đỉnh ở dưới, chiều cao sáu mét "
            "và bán kính miệng ba mét. Bơm nước vào không phẩy năm mét khối "
            "mỗi phút, không có nước chảy ra. Khi nước sâu hai mét, "
            "mực nước dâng nhanh bao nhiêu?"
        ),
        "steps": [
            (
                "1. Dùng tam giác đồng dạng",
                r"\frac{r}{h}=\frac{3}{6}=\frac12\quad\Rightarrow\quad r=\frac h2",
                "Gọi r là bán kính mặt nước và h là độ sâu. "
                "Từ tam giác đồng dạng, r chia h bằng ba chia sáu. "
                "Vì vậy r bằng h chia hai."
            ),
            (
                "2. Đưa thể tích về một biến h",
                r"V=\frac13\pi r^2h=\frac13\pi\left(\frac h2\right)^2h=\frac{\pi h^3}{12}",
                "Thay r bằng h chia hai vào công thức thể tích hình nón. "
                "Ta được V bằng pi h mũ ba chia mười hai. "
                "Đây là bước quan trọng để chỉ còn một biến."
            ),
            (
                "3. Lấy đạo hàm theo t",
                r"\frac{dV}{dt}=\frac{\pi h^2}{4}\frac{dh}{dt}",
                "Lấy đạo hàm theo thời gian, ta được pi h bình phương "
                "chia bốn, nhân đạo hàm của h theo t."
            ),
            (
                "4. Thay h = 2 và dV/dt = 0,5",
                r"0{,}5=\frac{\pi\cdot2^2}{4}\frac{dh}{dt}\quad\Rightarrow\quad\frac{dh}{dt}=\frac1{2\pi}",
                "Tại h bằng hai, hệ số pi h bình phương chia bốn bằng pi. "
                "Do đó tốc độ nước dâng bằng một chia hai pi."
            ),
            (
                "5. Kết luận",
                r"\boxed{\frac{dh}{dt}\approx0{,}159\ \mathrm{m}/\mathrm{ph\acute{u}t}}",
                "Mực nước dâng khoảng không phẩy một năm chín mét mỗi phút. "
                "Bể càng rộng ở phía trên, cùng một lưu lượng "
                "thì nước càng dâng chậm."
            ),
        ],
        "summary": "Bể nón: h′ ≈ 0,159 m/phút",
    },
    {
        "title": "NƯỚC DÂNG TRONG MÁNG",
        "kind": "trough",
        "question": (
            "Máng dài 10 m; tiết diện là tam giác cân cao 2 m, miệng rộng 4 m. "
            "Bơm 0,8 m³/phút. Tìm dh/dt khi h = 0,5 m."
        ),
        "intro": (
            "Bài năm. Một máng nằm ngang dài mười mét, có tiết diện "
            "tam giác cân với đỉnh ở dưới, cao hai mét và miệng rộng bốn mét. "
            "Bơm vào không phẩy tám mét khối mỗi phút, không có nước chảy ra. "
            "Tìm tốc độ nước dâng khi độ sâu bằng không phẩy năm mét."
        ),
        "steps": [
            (
                "1. Liên hệ chiều rộng mặt nước và độ sâu",
                r"\frac bh=\frac42=2\quad\Rightarrow\quad b=2h",
                "Gọi b là chiều rộng mặt nước. "
                "Do các tam giác đồng dạng, b chia h bằng bốn chia hai. "
                "Suy ra b bằng hai h."
            ),
            (
                "2. Tính thể tích nước",
                r"V=\left(\frac12bh\right)\cdot10=10h^2",
                "Diện tích tiết diện phần nước bằng một phần hai b h, "
                "hay h bình phương. Nhân với chiều dài mười mét, "
                "ta được thể tích bằng mười h bình phương."
            ),
            (
                "3. Đạo hàm theo thời gian",
                r"\frac{dV}{dt}=20h\frac{dh}{dt}",
                "Lấy đạo hàm theo t. "
                "Tốc độ tăng thể tích bằng hai mươi h nhân tốc độ tăng độ sâu."
            ),
            (
                "4. Thay số và giải",
                r"0{,}8=20\cdot0{,}5\cdot\frac{dh}{dt}\quad\Rightarrow\quad\frac{dh}{dt}=0{,}08",
                "Thay h bằng không phẩy năm và lưu lượng bằng không phẩy tám. "
                "Ta có không phẩy tám bằng mười nhân đạo hàm của h. "
                "Suy ra đạo hàm của h bằng không phẩy không tám."
            ),
            (
                "5. Kết luận",
                r"\boxed{\frac{dh}{dt}=0{,}08\ \mathrm{m}/\mathrm{ph\acute{u}t}=8\ \mathrm{cm}/\mathrm{ph\acute{u}t}}",
                "Mực nước dâng tám xăng ti mét mỗi phút. "
                "Cần phân biệt thể tích nước với diện tích tiết diện: "
                "phải nhân thêm chiều dài của máng."
            ),
        ],
        "summary": "Máng tam giác: h′ = 8 cm/phút",
    },
    {
        "title": "CHIẾC THANG ĐANG TRƯỢT",
        "kind": "ladder",
        "question": (
            "Thang dài 5 m tựa vào tường vuông góc mặt đất. Chân thang "
            "trượt ra 0,6 m/s. Khi chân cách tường 3 m, đầu thang hạ nhanh bao nhiêu?"
        ),
        "intro": (
            "Bài sáu. Một chiếc thang dài năm mét tựa vào bức tường "
            "vuông góc với mặt đất. Chân thang trượt ra xa tường "
            "không phẩy sáu mét mỗi giây. Khi chân thang cách tường ba mét, "
            "đầu thang đi xuống nhanh bao nhiêu?"
        ),
        "steps": [
            (
                "1. Đặt biến và áp dụng định lí Pythagore",
                r"x^2+y^2=25,\quad \frac{dx}{dt}=0{,}6",
                "Gọi x là khoảng cách từ chân thang đến tường, "
                "y là độ cao đầu thang. Do chiều dài thang không đổi, "
                "x bình phương cộng y bình phương bằng hai mươi lăm."
            ),
            (
                "2. Tìm độ cao tại thời điểm xét",
                r"x=3\quad\Rightarrow\quad y=\sqrt{25-9}=4",
                "Khi x bằng ba, y bằng căn của hai mươi lăm trừ chín, "
                "tức bốn mét. Đây chỉ là giá trị tại thời điểm đang xét, "
                "không phải y luôn bằng bốn."
            ),
            (
                "3. Đạo hàm hệ thức tổng quát",
                r"2x\frac{dx}{dt}+2y\frac{dy}{dt}=0",
                "Lấy đạo hàm hệ thức tổng quát theo thời gian. "
                "Cả x và y đều thay đổi, nên cả hai số hạng "
                "đều cần áp dụng quy tắc hàm hợp."
            ),
            (
                "4. Tính đạo hàm của độ cao",
                r"\frac{dy}{dt}=-\frac xy\frac{dx}{dt}=-\frac34\cdot0{,}6=-0{,}45",
                "Giải ra đạo hàm của y bằng âm x chia y nhân đạo hàm của x. "
                "Thay số được âm không phẩy bốn lăm mét mỗi giây."
            ),
            (
                "5. Phân biệt dấu đạo hàm và tốc độ hạ",
                r"\boxed{\frac{dy}{dt}=-0{,}45\ \mathrm{m}/\mathrm{s},\quad v_{\downarrow}=0{,}45\ \mathrm{m}/\mathrm{s}}",
                "Dấu âm cho biết đầu thang đang hạ xuống. "
                "Nếu hỏi tốc độ hạ thì trả lời số dương: "
                "không phẩy bốn lăm mét mỗi giây."
            ),
        ],
        "summary": "Thang: đầu hạ 0,45 m/s",
    },
    {
        "title": "NGƯỜI ĐI VÀ BÓNG NGƯỜI",
        "kind": "shadow",
        "question": (
            "Đèn cao 6 m, người cao 1,5 m đi xa cột đèn với tốc độ 1,2 m/s. "
            "Tìm tốc độ dài ra của bóng và tốc độ của đầu bóng."
        ),
        "intro": (
            "Bài bảy. Đèn đường cao sáu mét. Một người cao một phẩy năm mét "
            "đi thẳng ra xa cột đèn với tốc độ một phẩy hai mét mỗi giây. "
            "Cần tìm hai tốc độ khác nhau: tốc độ dài ra của bóng "
            "và tốc độ chuyển động của đầu bóng."
        ),
        "steps": [
            (
                "1. Đặt x: cách cột; s: chiều dài bóng",
                r"\frac{6}{x+s}=\frac{1{,}5}{s}",
                "Gọi x là khoảng cách từ người đến cột đèn, "
                "s là chiều dài bóng. Hai tam giác đồng dạng cho ta "
                "sáu chia x cộng s bằng một phẩy năm chia s."
            ),
            (
                "2. Rút gọn hệ thức",
                r"6s=1{,}5(x+s)\quad\Rightarrow\quad s=\frac x3",
                "Nhân chéo và chuyển vế, ta được bốn phẩy năm s "
                "bằng một phẩy năm x. Suy ra s bằng x chia ba."
            ),
            (
                "3. Tốc độ dài ra của bóng",
                r"\frac{ds}{dt}=\frac13\frac{dx}{dt}=\frac13\cdot1{,}2=0{,}4",
                "Đạo hàm hai vế. Chiều dài bóng tăng với tốc độ "
                "bằng một phần ba tốc độ của người, tức không phẩy bốn mét mỗi giây."
            ),
            (
                "4. Tốc độ đầu bóng so với cột đèn",
                r"z=x+s\quad\Rightarrow\quad\frac{dz}{dt}=1{,}2+0{,}4=1{,}6",
                "Khoảng cách từ đầu bóng đến cột đèn là z bằng x cộng s. "
                "Vì vậy tốc độ đầu bóng bằng một phẩy hai cộng không phẩy bốn, "
                "tức một phẩy sáu mét mỗi giây."
            ),
            (
                "5. Kết luận: hai đại lượng khác nhau",
                r"\boxed{s'=0{,}4\ \mathrm{m}/\mathrm{s},\qquad z'=1{,}6\ \mathrm{m}/\mathrm{s}}",
                "Bóng dài thêm không phẩy bốn mét mỗi giây, "
                "nhưng đầu bóng đi xa cột đèn một phẩy sáu mét mỗi giây. "
                "Không được nhầm hai kết quả này."
            ),
        ],
        "summary": "Bóng: s′ = 0,4; z′ = 1,6 m/s",
    },
    {
        "title": "HAI XE TRÊN HAI ĐƯỜNG VUÔNG GÓC",
        "kind": "cars",
        "question": (
            "Hai xe đi xa giao lộ trên hai đường vuông góc, với tốc độ 60 và 40 km/h. "
            "Khi cách giao lộ 120 và 50 km, khoảng cách giữa chúng tăng nhanh bao nhiêu?"
        ),
        "intro": (
            "Bài tám. Hai xe đi ra xa giao lộ trên hai con đường vuông góc, "
            "với tốc độ lần lượt sáu mươi và bốn mươi ki lô mét mỗi giờ. "
            "Tại một thời điểm, chúng cách giao lộ lần lượt một trăm hai mươi "
            "và năm mươi ki lô mét. Tìm tốc độ tăng khoảng cách giữa hai xe. "
            "Không cần giả thiết hai xe xuất phát cùng lúc."
        ),
        "steps": [
            (
                "1. Gọi d là khoảng cách giữa hai xe",
                r"d^2=x^2+y^2,\quad x'=60,\quad y'=40",
                "Gọi x và y là khoảng cách của từng xe đến giao lộ, "
                "d là khoảng cách giữa hai xe. "
                "Định lí Pythagore cho d bình phương bằng x bình phương cộng y bình phương."
            ),
            (
                "2. Khoảng cách tại thời điểm đang xét",
                r"d=\sqrt{120^2+50^2}=130\ \mathrm{km}",
                "Thay x bằng một trăm hai mươi và y bằng năm mươi, "
                "ta được d bằng một trăm ba mươi ki lô mét."
            ),
            (
                "3. Đạo hàm theo thời gian",
                r"2dd'=2xx'+2yy'\quad\Rightarrow\quad d'=\frac{xx'+yy'}{d}",
                "Lấy đạo hàm hai vế và chia cho hai d. "
                "Tốc độ tăng khoảng cách bằng x nhân x phẩy "
                "cộng y nhân y phẩy, tất cả chia cho d."
            ),
            (
                "4. Thay số",
                r"d'=\frac{120\cdot60+50\cdot40}{130}=\frac{920}{13}",
                "Thay các dữ kiện vào. Tử số bằng chín nghìn hai trăm. "
                "Chia cho một trăm ba mươi được chín trăm hai mươi phần mười ba."
            ),
            (
                "5. Kết luận",
                r"\boxed{d'\approx70{,}77\ \mathrm{km}/\mathrm{h}}",
                "Khoảng cách giữa hai xe tăng khoảng bảy mươi phẩy bảy bảy "
                "ki lô mét mỗi giờ. Không cộng trực tiếp sáu mươi với bốn mươi "
                "vì hai xe không chuyển động trên cùng một đường thẳng."
            ),
        ],
        "summary": "Hai xe: d′ ≈ 70,77 km/h",
    },
    {
        "title": "GÓC NÂNG KHI QUAN SÁT KHÍ CẦU",
        "kind": "balloon",
        "question": (
            "Người quan sát cách điểm dưới khí cầu 40 m theo phương ngang. "
            "Khí cầu bay thẳng lên 3 m/s. Khi cao 30 m, tìm tốc độ tăng góc nâng."
        ),
        "intro": (
            "Bài chín. Một người đứng cách vị trí thẳng đứng dưới khí cầu "
            "bốn mươi mét. Khí cầu bay thẳng lên với tốc độ ba mét mỗi giây. "
            "Khi khí cầu cao ba mươi mét so với đường ngang qua mắt người quan sát, "
            "góc nâng tăng nhanh bao nhiêu?"
        ),
        "steps": [
            (
                "1. Lập hệ thức lượng giác",
                r"\tan\theta=\frac h{40},\quad h'=3",
                "Gọi theta là góc nâng, h là độ cao so với đường ngang qua mắt. "
                "Trong tam giác vuông, tang theta bằng h chia bốn mươi."
            ),
            (
                "2. Đạo hàm theo t; góc đo bằng radian",
                r"\frac{1}{\cos^2\theta}\frac{d\theta}{dt}=\frac1{40}\frac{dh}{dt}",
                "Đạo hàm tang theta bằng một chia cô sin bình phương theta "
                "nhân đạo hàm của theta theo t. "
                "Công thức này dùng khi góc được đo bằng ra đi an."
            ),
            (
                "3. Tính cos²θ tại h = 30",
                r"\cos^2\theta=\frac{40^2}{40^2+30^2}=\frac{16}{25}",
                "Khi h bằng ba mươi, cạnh huyền bằng năm mươi. "
                "Vì vậy cô sin bình phương theta bằng mười sáu phần hai mươi lăm."
            ),
            (
                "4. Tính tốc độ tăng góc",
                r"\frac{d\theta}{dt}=\frac3{40}\cdot\frac{16}{25}=0{,}048",
                "Nhân hai vế với cô sin bình phương theta rồi thay số. "
                "Kết quả là không phẩy không bốn tám."
            ),
            (
                "5. Kết luận và đơn vị góc",
                r"\boxed{\frac{d\theta}{dt}=0{,}048\ \mathrm{rad}/\mathrm{s}}",
                "Góc nâng tăng không phẩy không bốn tám ra đi an mỗi giây. "
                "Đây không phải không phẩy không bốn tám độ mỗi giây. "
                "Nếu cần đổi sang độ, phải nhân thêm một trăm tám mươi chia pi."
            ),
        ],
        "summary": "Khí cầu: θ′ = 0,048 rad/s",
    },
    {
        "title": "HAI CẠNH CÙNG THAY ĐỔI",
        "kind": "rectangle",
        "question": (
            "Hình chữ nhật có chiều dài tăng 0,3 m/s, chiều rộng giảm 0,1 m/s. "
            "Khi dài 8 m, rộng 5 m, diện tích đang tăng hay giảm? Với tốc độ nào?"
        ),
        "intro": (
            "Bài mười. Chiều dài hình chữ nhật tăng không phẩy ba mét mỗi giây, "
            "còn chiều rộng giảm không phẩy một mét mỗi giây. "
            "Khi chiều dài bằng tám mét và chiều rộng bằng năm mét, "
            "diện tích đang tăng hay giảm, với tốc độ bao nhiêu?"
        ),
        "steps": [
            (
                "1. Ghi dữ kiện, chú ý dấu âm",
                r"a=8,\quad b=5,\quad a'=0{,}3,\quad b'=-0{,}1",
                "Gọi a là chiều dài và b là chiều rộng. "
                "Chiều dài tăng nên a phẩy dương không phẩy ba. "
                "Chiều rộng giảm nên b phẩy phải là âm không phẩy một."
            ),
            (
                "2. Công thức diện tích",
                r"S=ab",
                "Diện tích bằng chiều dài nhân chiều rộng. "
                "Ở đây cả hai thừa số đều phụ thuộc thời gian."
            ),
            (
                "3. Áp dụng quy tắc đạo hàm của tích",
                r"S'=a'b+ab'",
                "Dùng quy tắc đạo hàm của tích: "
                "đạo hàm thừa số thứ nhất nhân thừa số thứ hai, "
                "cộng thừa số thứ nhất nhân đạo hàm thừa số thứ hai."
            ),
            (
                "4. Thay số và xét dấu",
                r"S'=0{,}3\cdot5+8\cdot(-0{,}1)=1{,}5-0{,}8=0{,}7>0",
                "Thay số được một phẩy năm trừ không phẩy tám, bằng không phẩy bảy. "
                "Kết quả dương nên diện tích đang tăng."
            ),
            (
                "5. Kết luận",
                r"\boxed{S'=0{,}7\ \mathrm{m}^2/\mathrm{s}>0}",
                "Diện tích tăng không phẩy bảy mét vuông mỗi giây. "
                "Một cạnh giảm chưa chắc làm diện tích giảm. "
                "Cần tính đầy đủ tác động của cả hai cạnh."
            ),
        ],
        "summary": "Hình chữ nhật: S′ = 0,7 m²/s",
    },
]

INTRO_SPEECH = (
    "Chào các em. Trong video này, chúng ta cùng giải mười bài toán "
    "về tốc độ thay đổi bằng ứng dụng đạo hàm. "
    "Các hình chuyển động chỉ minh họa chiều biến đổi, "
    "không mô phỏng đúng tỉ lệ hoặc thời gian thực. "
    "Phương pháp chung gồm bốn bước: đặt các đại lượng biến thiên theo thời gian; "
    "lập hệ thức hình học; lấy đạo hàm theo thời gian; "
    "cuối cùng thay số, xét dấu và ghi đơn vị. "
    "Hãy nhớ: không thay giá trị tại một thời điểm thành hằng số "
    "trước khi lấy đạo hàm hệ thức tổng quát."
)

OUTRO_SPEECH = (
    "Các em vừa hoàn thành mười dạng bài về tốc độ thay đổi. "
    "Điểm chung không phải là học thuộc mười công thức riêng, "
    "mà là tìm đúng hệ thức rồi lấy đạo hàm theo thời gian. "
    "Với bể nón và máng tam giác, hãy dùng đồng dạng để giảm số biến. "
    "Với thang trượt và hai xe, hãy dùng định lí Pythagore. "
    "Với bóng người, cần phân biệt chiều dài bóng và vị trí đầu bóng. "
    "Với góc nâng, nhớ dùng đơn vị ra đi an. "
    "Và trong mọi bài, hãy kiểm tra dấu cùng đơn vị của kết quả. "
    "Thầy Nguyễn Văn Sang chúc các em học tốt."
)

# ------------------------------------------------------------
# GIỌNG ĐỌC: EDGE TTS; DỰ PHÒNG NGOẠI TUYẾN
# ------------------------------------------------------------

def speech_items():
    items = {"intro": INTRO_SPEECH, "outro": OUTRO_SPEECH}
    for i, task in enumerate(TASKS, 1):
        items[f"b{i}_intro"] = task["intro"]
        for j, step in enumerate(task["steps"], 1):
            items[f"b{i}_s{j}"] = step[2]
    return items

def audio_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    duration = float(result.stdout.strip())
    if not math.isfinite(duration) or duration <= 0:
        raise RuntimeError(f"Âm thanh không hợp lệ: {path}")
    return duration

def offline_voice(text, target):
    wav = target.with_suffix(".wav")
    subprocess.run(
        [
            "espeak-ng", "-v", "vi", "-s", "155",
            "-w", str(wav), text,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav),
            "-ar", "24000", "-ac", "1",
            "-codec:a", "libmp3lame", "-b:a", "96k",
            str(target),
        ],
        check=True,
    )
    wav.unlink(missing_ok=True)

async def prepare_audio():
    items = speech_items()
    manifest = {}
    semaphore = asyncio.Semaphore(2)
    completed = 0
    fallback_count = 0

    async def generate(key, text):
        nonlocal completed, fallback_count
        digest = hashlib.sha256(
            (VOICE + VOICE_RATE + text).encode("utf-8")
        ).hexdigest()[:20]
        target = AUDIO_DIR / f"{digest}.mp3"

        async with semaphore:
            valid = False
            if target.exists() and target.stat().st_size > 1000:
                try:
                    audio_duration(target)
                    valid = True
                except Exception:
                    target.unlink(missing_ok=True)

            if not valid:
                for attempt in range(3):
                    try:
                        communicate = edge_tts.Communicate(
                            text=text,
                            voice=VOICE,
                            rate=VOICE_RATE,
                        )
                        await asyncio.wait_for(
                            communicate.save(str(target)),
                            timeout=55,
                        )
                        audio_duration(target)
                        valid = True
                        break
                    except Exception:
                        target.unlink(missing_ok=True)
                        await asyncio.sleep(1.5 * (attempt + 1))

                if not valid:
                    fallback_count += 1
                    print(
                        f"  Cảnh báo: {key} dùng giọng tiếng Việt "
                        "ngoại tuyến vì không kết nối được giọng Nam Minh.",
                        flush=True,
                    )
                    await asyncio.to_thread(
                        offline_voice, text, target
                    )

            manifest[key] = {
                "path": str(target),
                "duration": audio_duration(target),
            }
            completed += 1
            print(
                f"  Âm thanh {completed}/{len(items)}: {key}",
                flush=True,
            )

    await asyncio.gather(
        *(generate(key, text) for key, text in items.items())
    )

    MANIFEST_FILE.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"Hoàn tất âm thanh. Đoạn dùng giọng dự phòng: {fallback_count}.",
        flush=True,
    )

# ------------------------------------------------------------
# HÀM GIAO DIỆN
# ------------------------------------------------------------

def txt(content, size=26, color=WHITE_TEXT):
    return Text(
        content,
        font=FONT,
        font_size=size,
        color=color,
        disable_ligatures=True,
    )

def fit_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob

def math_label(content, point, color=WHITE_TEXT, size=25):
    return MathTex(
        content,
        font_size=size,
        color=color,
    ).move_to(point)

def box(width, height, center, fill=PANEL, stroke=BORDER):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        stroke_color=stroke,
        stroke_width=1.3,
        fill_color=fill,
        fill_opacity=1,
    ).move_to(center)

# ------------------------------------------------------------
# HÌNH VẼ
# Tọa độ nội bộ trong khung bên trái.
# Chuyển động chỉ dùng ở phần đọc đề, sau đó trở về trạng thái đầu.
# ------------------------------------------------------------

def build_diagram(kind):
    center = np.array([-4.63, -0.58, 0.0])

    def P(x, y):
        return center + np.array([x, y, 0.0])

    def M(s, x, y, color=WHITE_TEXT, size=24):
        return math_label(s, P(x, y), color, size)

    def T(s, x, y, color=MUTED, size=19):
        return txt(s, size, color).move_to(P(x, y))

    tracker = ValueTracker(0)
    target = 1

    if kind == "circle":
        tracker.set_value(1.12)
        target = 1.43

        shape = always_redraw(
            lambda: Circle(
                radius=tracker.get_value(),
                color=BLUE,
                stroke_width=4,
                fill_color=BLUE,
                fill_opacity=0.18,
            ).move_to(P(0, 0))
        )
        radius = always_redraw(
            lambda: Line(
                P(0, 0), P(tracker.get_value(), 0),
                color=YELLOW, stroke_width=4,
            )
        )
        rlabel = always_redraw(
            lambda: M("r(t)", tracker.get_value()/2, 0.22, YELLOW)
        )
        group = VGroup(
            shape, radius, rlabel, Dot(P(0, 0), radius=0.045),
            M("S=\\pi r^2", 0, -1.8),
            T("Bán kính tăng → diện tích tăng", 0, 1.82, CYAN, 17),
        )

    elif kind == "sphere":
        tracker.set_value(1.12)
        target = 1.4

        globe = always_redraw(
            lambda: VGroup(
                Circle(
                    radius=tracker.get_value(),
                    color=BLUE, stroke_width=4,
                    fill_color=BLUE, fill_opacity=0.16,
                ).move_to(P(0, 0)),
                Ellipse(
                    width=2*tracker.get_value(),
                    height=0.60*tracker.get_value(),
                    color=CYAN, stroke_width=2,
                ).move_to(P(0, 0)),
                Ellipse(
                    width=0.72*tracker.get_value(),
                    height=2*tracker.get_value(),
                    color=BLUE, stroke_width=1.5,
                ).move_to(P(0, 0)),
                Line(
                    P(0, 0), P(tracker.get_value(), 0),
                    color=YELLOW, stroke_width=3,
                ),
            )
        )
        group = VGroup(
            globe,
            M("r(t)", 0.55, 0.24, YELLOW),
            T("Thể tích tăng", 0, 1.8, CYAN),
            M("V=\\frac43\\pi r^3", 0, -1.8),
        )

    elif kind == "cylinder":
        tracker.set_value(1.2)
        target = 2.05
        bottom = -1.38
        top = 1.25
        radius = 1.16

        water = always_redraw(
            lambda: VGroup(
                Rectangle(
                    width=2*radius,
                    height=tracker.get_value(),
                    stroke_width=0,
                    fill_color=BLUE, fill_opacity=0.30,
                ).move_to(P(0, bottom+tracker.get_value()/2)),
                Ellipse(
                    width=2*radius, height=0.42,
                    stroke_color=CYAN,
                    fill_color=BLUE, fill_opacity=0.48,
                ).move_to(P(0, bottom+tracker.get_value())),
                Ellipse(
                    width=2*radius, height=0.42,
                    stroke_color=BLUE,
                    fill_color=BLUE, fill_opacity=0.18,
                ).move_to(P(0, bottom)),
            )
        )
        shell = VGroup(
            Line(P(-radius, bottom), P(-radius, top), color=WHITE_TEXT),
            Line(P(radius, bottom), P(radius, top), color=WHITE_TEXT),
            Ellipse(width=2*radius, height=0.42, color=WHITE_TEXT).move_to(P(0, top)),
            Ellipse(width=2*radius, height=0.42, color=WHITE_TEXT).move_to(P(0, bottom)),
        )
        hline = always_redraw(
            lambda: VGroup(
                DoubleArrow(
                    P(1.48, bottom),
                    P(1.48, bottom+tracker.get_value()),
                    buff=0,
                    color=YELLOW,
                    tip_length=0.10,
                ),
                M("h", 1.73, bottom+tracker.get_value()/2, YELLOW),
            )
        )
        group = VGroup(
            water, shell, hline,
            Arrow(P(-0.55, 1.9), P(-0.55, 1.40), color=CYAN, buff=0),
            M("R=2", 0, -1.88),
            T("Bể có tiết diện ngang không đổi", 0, 1.7, MUTED, 15),
        )

    elif kind == "cone":
        tracker.set_value(3.0/3)
        target = 1.58
        apex = -1.5
        height = 3.0
        radius = 1.35

        water = always_redraw(
            lambda: VGroup(
                Polygon(
                    P(0, apex),
                    P(-radius*tracker.get_value()/height, apex+tracker.get_value()),
                    P(radius*tracker.get_value()/height, apex+tracker.get_value()),
                    stroke_color=CYAN,
                    fill_color=BLUE, fill_opacity=0.36,
                ),
                Ellipse(
                    width=2*radius*tracker.get_value()/height,
                    height=0.22*tracker.get_value(),
                    color=CYAN,
                    fill_color=BLUE, fill_opacity=0.30,
                ).move_to(P(0, apex+tracker.get_value())),
                Line(
                    P(0, apex+tracker.get_value()),
                    P(radius*tracker.get_value()/height, apex+tracker.get_value()),
                    color=YELLOW,
                ),
                M("r", radius*tracker.get_value()/(2*height),
                  apex+tracker.get_value()+0.2, YELLOW, 21),
                M("h", -0.22, apex+tracker.get_value()/2, YELLOW, 22),
            )
        )
        shell = VGroup(
            Line(P(0, apex), P(-radius, apex+height), color=WHITE_TEXT),
            Line(P(0, apex), P(radius, apex+height), color=WHITE_TEXT),
            Ellipse(width=2*radius, height=0.38, color=WHITE_TEXT).move_to(P(0, apex+height)),
            DashedLine(P(0, apex), P(0, apex+height), color=MUTED),
            DoubleArrow(P(1.72, apex), P(1.72, apex+height), buff=0, color=MUTED, tip_length=0.09),
        )
        group = VGroup(
            water, shell,
            M("6", 1.90, 0.05, MUTED, 21),
            M("R=3", 0, 1.9, WHITE_TEXT, 22),
            M("\\frac rh=\\frac12", 0, -1.93, CYAN),
        )

    elif kind == "trough":
        tracker.set_value(0.6)
        target = 1.05
        bottom = -1.35
        height = 2.4
        radius = 1.30
        offset = np.array([0.53, 0.48, 0.0])

        A = P(-0.23, bottom)
        B = P(-0.23-radius, bottom+height)
        C = P(-0.23+radius, bottom+height)

        back = VGroup(
            Line(A+offset, B+offset, color=MUTED),
            Line(B+offset, C+offset, color=MUTED),
            Line(C+offset, A+offset, color=MUTED),
            Line(A, A+offset, color=MUTED),
            Line(B, B+offset, color=MUTED),
            Line(C, C+offset, color=MUTED),
        )

        def water_shape():
            hh = tracker.get_value()
            rr = radius*hh/height
            L = P(-0.23-rr, bottom+hh)
            R = P(-0.23+rr, bottom+hh)
            return VGroup(
                Polygon(
                    L, R, R+offset, L+offset,
                    color=CYAN, fill_color=BLUE, fill_opacity=0.22,
                ),
                Polygon(
                    A, L, R,
                    color=CYAN, fill_color=BLUE, fill_opacity=0.4,
                ),
                M("b", -0.23, bottom+hh+0.2, YELLOW, 22),
                M("h", -0.43, bottom+hh/2, YELLOW, 22),
            )

        group = VGroup(
            back,
            always_redraw(water_shape),
            Line(A, B, color=WHITE_TEXT),
            Line(B, C, color=WHITE_TEXT),
            Line(C, A, color=WHITE_TEXT),
            M("4\\ \\mathrm{m}", -0.23, 1.32, WHITE_TEXT, 22),
            M("2\\ \\mathrm{m}", -1.54, -0.20, MUTED, 20),
            M("L=10\\ \\mathrm{m}", 0.25, -1.85, WHITE_TEXT, 23),
            T("Tiết diện tam giác cân", 0, 1.9, CYAN, 17),
        )

    elif kind == "ladder":
        tracker.set_value(1.65)
        target = 2.12
        length = 2.75
        ox, oy = -1.35, -1.50

        def moving_ladder():
            xx = tracker.get_value()
            yy = math.sqrt(length**2-xx**2)
            return VGroup(
                Line(P(ox+xx, oy), P(ox, oy+yy), color=YELLOW, stroke_width=7),
                Dot(P(ox+xx, oy), color=CYAN, radius=0.07),
                Dot(P(ox, oy+yy), color=CYAN, radius=0.07),
                M("x", ox+xx/2, oy-0.23, CYAN),
                M("y", ox-0.23, oy+yy/2, CYAN),
                M("5\\ \\mathrm{m}", ox+xx/2+0.32, oy+yy/2+0.12, YELLOW, 22),
            )

        group = VGroup(
            Line(P(ox, oy), P(ox, 1.65), color=WHITE_TEXT, stroke_width=4),
            Line(P(ox, oy), P(1.83, oy), color=WHITE_TEXT, stroke_width=4),
            always_redraw(moving_ladder),
            Arrow(P(0.8, -1.08), P(1.55, -1.08), color=RED, buff=0),
            Arrow(P(-0.95, 1.20), P(-0.95, 0.68), color=RED, buff=0),
            T("Chân ra xa — đầu hạ xuống", 0, 1.94, CYAN, 16),
        )

    elif kind == "shadow":
        tracker.set_value(1.65)
        target = 2.25
        pole_x = -1.63
        ground = -1.33
        pole_h = 2.65
        person_h = pole_h/4

        def moving_shadow():
            xx = tracker.get_value()
            person_x = pole_x+xx
            tip_x = pole_x+4*xx/3
            head_y = ground+person_h
            return VGroup(
                Polygon(
                    P(pole_x, ground+pole_h),
                    P(pole_x, ground),
                    P(tip_x, ground),
                    stroke_width=0,
                    fill_color=YELLOW, fill_opacity=0.07,
                ),
                Line(
                    P(pole_x, ground+pole_h),
                    P(tip_x, ground),
                    color=YELLOW, stroke_width=2,
                ),
                Line(
                    P(person_x, ground),
                    P(tip_x, ground),
                    color=RED, stroke_width=7,
                ),
                Circle(
                    radius=0.075,
                    color=CYAN,
                    fill_color=CYAN, fill_opacity=1,
                ).move_to(P(person_x, head_y-0.075)),
                Line(P(person_x, head_y-0.15), P(person_x, ground+0.2), color=CYAN, stroke_width=4),
                Line(P(person_x, ground+0.2), P(person_x-0.10, ground), color=CYAN, stroke_width=3),
                Line(P(person_x, ground+0.2), P(person_x+0.10, ground), color=CYAN, stroke_width=3),
                M("x", (pole_x+person_x)/2, ground-0.25, CYAN),
                M("s", (person_x+tip_x)/2, ground-0.25, RED),
                M("1{,}5", person_x+0.26, ground+0.47, CYAN, 19),
            )

        group = VGroup(
            always_redraw(moving_shadow),
            Line(P(-1.9, ground), P(1.9, ground), color=WHITE_TEXT),
            Line(P(pole_x, ground), P(pole_x, ground+pole_h), color=WHITE_TEXT, stroke_width=5),
            Dot(P(pole_x, ground+pole_h), radius=0.11, color=YELLOW),
            M("6", pole_x-0.21, 0.0, WHITE_TEXT, 22),
            M("z=x+s", 0.1, -1.96, YELLOW),
            T("Đầu bóng và chiều dài bóng", 0, 1.91, CYAN, 16),
        )

    elif kind == "cars":
        tracker.set_value(0)
        target = 1
        ox, oy = -1.36, -1.40

        def cars():
            xx = 2.4+0.30*tracker.get_value()
            yy = 1.65+0.20*tracker.get_value()
            A = P(ox+xx, oy)
            B = P(ox, oy+yy)
            return VGroup(
                Line(A, B, color=YELLOW, stroke_width=4),
                RoundedRectangle(
                    width=0.35, height=0.20,
                    corner_radius=0.04,
                    color=BLUE, fill_color=BLUE, fill_opacity=1,
                ).move_to(A),
                RoundedRectangle(
                    width=0.20, height=0.35,
                    corner_radius=0.04,
                    color=CYAN, fill_color=CYAN, fill_opacity=1,
                ).move_to(B),
                M("x", ox+xx/2, oy-0.25, BLUE),
                M("y", ox-0.22, oy+yy/2, CYAN),
                M("d", ox+xx/2+0.14, oy+yy/2+0.2, YELLOW),
            )

        group = VGroup(
            Line(P(ox, oy), P(1.84, oy), color=MUTED, stroke_width=4),
            Line(P(ox, oy), P(ox, 1.68), color=MUTED, stroke_width=4),
            always_redraw(cars),
            Arrow(P(0.7, -1.0), P(1.55, -1.0), color=BLUE, buff=0),
            Arrow(P(-0.95, 0.85), P(-0.95, 1.5), color=CYAN, buff=0),
            M("60\\ \\mathrm{km/h}", 0.62, -0.62, BLUE, 21),
            M("40\\ \\mathrm{km/h}", -0.15, 1.1, CYAN, 21),
            M("O", ox-0.17, oy-0.23, WHITE_TEXT, 21),
            T("Hai hướng vuông góc", 0, 1.94, CYAN, 18),
        )

    elif kind == "balloon":
        tracker.set_value(2.025)
        target = 2.60
        ox, oy = -1.45, -1.35
        distance = 2.7

        def balloon():
            hh = tracker.get_value()
            angle = math.atan(hh/distance)
            A = P(ox, oy)
            B = P(ox+distance, oy+hh)
            return VGroup(
                Line(A, B, color=YELLOW, stroke_width=3),
                DashedLine(P(ox+distance, oy), B, color=BLUE),
                Circle(
                    radius=0.17,
                    color=RED,
                    fill_color=RED, fill_opacity=0.70,
                ).move_to(B),
                Arc(
                    radius=0.58,
                    start_angle=0,
                    angle=angle,
                    arc_center=A,
                    color=YELLOW,
                    stroke_width=3,
                ),
                M("\\theta", ox+0.85, oy+0.25, YELLOW, 24),
                M("h", ox+distance+0.24, oy+hh/2, BLUE, 24),
            )

        group = VGroup(
            Line(P(ox, oy), P(ox+distance, oy), color=WHITE_TEXT, stroke_width=3),
            Dot(P(ox, oy), color=CYAN, radius=0.07),
            always_redraw(balloon),
            M("40\\ \\mathrm{m}", -0.10, -1.65),
            Arrow(P(1.65, 0.85), P(1.65, 1.46), color=CYAN, buff=0),
            T("Góc θ được đo bằng radian", 0, 1.93, CYAN, 16),
        )

    elif kind == "rectangle":
        tracker.set_value(0)
        target = 3

        def rectangle():
            tt = tracker.get_value()
            ww = 2.6+0.0975*tt
            hh = 1.625-0.0325*tt
            return VGroup(
                Rectangle(
                    width=ww, height=hh,
                    color=BLUE, stroke_width=4,
                    fill_color=BLUE, fill_opacity=0.20,
                ).move_to(P(0, 0)),
                M("a(t)", 0, -hh/2-0.28, YELLOW),
                M("b(t)", -ww/2-0.29, 0, CYAN),
            )

        group = VGroup(
            always_redraw(rectangle),
            Arrow(P(0.6, 1.25), P(1.42, 1.25), color=YELLOW, buff=0),
            Arrow(P(1.65, 0.65), P(1.65, 0.12), color=RED, buff=0),
            M("a'>0,\\quad b'<0", 0, -1.82),
            T("Một cạnh tăng, một cạnh giảm", 0, 1.89, CYAN, 16),
        )

    else:
        raise ValueError(f"Chưa có hình cho: {kind}")

    return group, tracker, target

# ------------------------------------------------------------
# SCENE CHÍNH
# ------------------------------------------------------------

class RelatedRates(Scene):
    def setup(self):
        self.audio_manifest = json.loads(
            MANIFEST_FILE.read_text(encoding="utf-8")
        )

    def speak(self, key, animation=None, animation_time=4.0):
        item = self.audio_manifest[key]
        duration = float(item["duration"])
        self.add_sound(item["path"], gain=0)

        if animation is not None:
            used = min(animation_time, max(0.3, duration-0.1))
            self.play(animation, run_time=used, rate_func=smooth)
            self.wait(max(0.1, duration-used+0.35))
        else:
            self.wait(duration+0.35)

    def make_footer(self):
        separator = Line(
            [-6.86, -3.47, 0],
            [6.86, -3.47, 0],
            color=BORDER,
            stroke_width=1.2,
        )
        name = txt(
            "Thầy Nguyễn Văn Sang", 23, YELLOW
        ).move_to([0, -3.73, 0])

        left = txt(
            "ỨNG DỤNG ĐẠO HÀM", 14, MUTED
        ).move_to([-5.34, -3.73, 0])

        right = txt(
            "TỐC ĐỘ THAY ĐỔI", 14, MUTED
        ).move_to([5.36, -3.73, 0])

        self.footer = VGroup(separator, name, left, right)
        self.add(self.footer)

    def clear_content(self):
        removable = [
            mob for mob in list(self.mobjects)
            if mob is not self.footer
        ]
        if removable:
            self.play(
                *[FadeOut(mob) for mob in removable],
                run_time=0.45,
            )

    def intro(self):
        tag = txt("CHUYÊN ĐỀ TOÁN HỌC", 22, CYAN).move_to([0, 3.06, 0])
        title = txt("TỐC ĐỘ THAY ĐỔI", 49, WHITE_TEXT).move_to([0, 2.25, 0])
        subtitle = txt(
            "10 bài tập • Hình học • Chuyển động • Mực nước",
            25, YELLOW,
        ).move_to([0, 1.48, 0])

        frame = box(12.6, 3.33, [0, -0.62, 0])

        contents = [
            ("01", "Đặt biến theo thời gian: r(t), h(t), x(t), y(t)."),
            ("02", "Lập hệ thức hình học hoặc hệ thức lượng giác."),
            ("03", "Lấy đạo hàm theo t, dùng đúng quy tắc hàm hợp."),
            ("04", "Thay số tại thời điểm xét; kiểm tra dấu và đơn vị."),
        ]

        rows = VGroup()
        for i, (number, content) in enumerate(contents):
            y = 0.49-i*0.70
            badge = txt(number, 26, CYAN).move_to([-5.55, y, 0])
            line = fit_width(txt(content, 25), 10.7)
            line.move_to([-4.98, y, 0], aligned_edge=LEFT)
            rows.add(badge, line)

        note = txt(
            "Hình động chỉ minh họa, không theo tỉ lệ và thời gian thực.",
            20, MUTED,
        ).move_to([0, -2.68, 0])

        self.play(
            FadeIn(tag), FadeIn(title, shift=UP*0.15),
            FadeIn(subtitle), FadeIn(frame), FadeIn(rows), FadeIn(note),
            run_time=1.1,
        )
        self.speak("intro")
        self.clear_content()

    def render_task(self, number, task):
        title = fit_width(
            txt(f"BÀI {number:02d}  |  {task['title']}", 31, WHITE_TEXT),
            12.5,
        ).move_to([-6.75, 3.48, 0], aligned_edge=LEFT)

        counter = txt(f"{number}/10", 21, CYAN).move_to([6.32, 3.48, 0])

        question_box = box(
            13.52, 1.28, [0, 2.39, 0],
            fill="#112C42",
            stroke="#286086",
        )

        lines = textwrap.wrap(
            task["question"], width=101,
            break_long_words=False,
        )

        question_text = VGroup(*[
            txt(line, 23, WHITE_TEXT) for line in lines
        ]).arrange(
            DOWN, buff=0.11, aligned_edge=LEFT
        )

        fit_width(question_text, 12.92)
        if question_text.height > 0.95:
            question_text.scale_to_fit_height(0.95)
        question_text.move_to([0, 2.39, 0])

        left_panel = box(4.28, 4.82, [-4.63, -0.78, 0])
        right_panel = box(8.96, 4.82, [2.30, -0.78, 0])

        sketch_note = txt(
            "HÌNH MINH HỌA", 15, MUTED
        ).move_to([-4.63, -2.97, 0])

        diagram, tracker, target = build_diagram(task["kind"])
        initial = tracker.get_value()

        self.play(
            FadeIn(title),
            FadeIn(counter),
            FadeIn(question_box),
            FadeIn(question_text),
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(sketch_note),
            run_time=0.55,
        )
        self.play(FadeIn(diagram), run_time=0.5)

        movement = Succession(
            tracker.animate.set_value(target),
            tracker.animate.set_value(initial),
        )
        self.speak(
            f"b{number}_intro",
            movement,
            animation_time=5.5,
        )
        tracker.set_value(initial)
        self.wait(0.1)

        for j, (caption, formula, narration) in enumerate(task["steps"], 1):
            row_y = 1.13-(j-1)*0.86
            caption_mob = fit_width(
                txt(
                    caption, 18,
                    CYAN if j < 5 else GREEN,
                ),
                8.12,
            ).move_to([-1.78, row_y, 0], aligned_edge=LEFT)

            formula_mob = MathTex(
                formula,
                font_size=30,
                color=WHITE_TEXT if j < 5 else GREEN,
            )
            fit_width(formula_mob, 8.06)
            if formula_mob.height > 0.53:
                formula_mob.scale_to_fit_height(0.53)

            formula_mob.move_to([2.30, row_y-0.35, 0])

            if j == 5:
                result_box = RoundedRectangle(
                    width=8.40,
                    height=0.84,
                    corner_radius=0.10,
                    stroke_color=GREEN,
                    stroke_width=1.5,
                    fill_color="#113C35",
                    fill_opacity=0.5,
                ).move_to([2.30, row_y-0.20, 0])
                self.play(FadeIn(result_box), run_time=0.2)

            self.play(
                FadeIn(caption_mob, shift=RIGHT*0.10),
                Write(formula_mob),
                run_time=0.75,
            )
            self.speak(f"b{number}_s{j}")

        self.wait(0.5)
        self.clear_content()

    def outro(self):
        title = txt(
            "TỔNG KẾT 10 DẠNG BÀI", 39, WHITE_TEXT
        ).move_to([0, 3.07, 0])

        subtitle = txt(
            "Cốt lõi: lập hệ thức → đạo hàm theo t → thay số → kết luận",
            24, CYAN,
        )
        fit_width(subtitle, 12.8)
        subtitle.move_to([0, 2.37, 0])

        board = box(13.22, 3.74, [0, -0.13, 0])
        entries = VGroup()

        for i, task in enumerate(TASKS):
            col = 0 if i < 5 else 1
            row = i if i < 5 else i-5
            x = -6.17 if col == 0 else 0.34
            y = 1.32-row*0.67

            line = txt(
                f"{i+1:02d}. {task['summary']}",
                23,
                WHITE_TEXT,
            )
            fit_width(line, 5.89)
            line.move_to([x, y, 0], aligned_edge=LEFT)
            entries.add(line)

        warning = txt(
            "Không quên: dấu âm • đơn vị • quy tắc hàm hợp • góc radian",
            24, YELLOW,
        )
        fit_width(warning, 12.8)
        warning.move_to([0, -2.58, 0])

        self.play(
            FadeIn(title), FadeIn(subtitle),
            FadeIn(board), FadeIn(entries), FadeIn(warning),
            run_time=0.9,
        )
        self.speak("outro")
        self.wait(1.0)

    def construct(self):
        self.make_footer()
        self.intro()

        for number, task in enumerate(TASKS, 1):
            self.render_task(number, task)

        self.outro()

if __name__ == "__main__":
    if "--audio" in sys.argv:
        asyncio.run(prepare_audio())
'''

SCRIPT = ROOT / "related_rates.py"
SCRIPT.write_text(SOURCE, encoding="utf-8")

# ============================================================
# TẠO GIỌNG ĐỌC
# ============================================================

print("3/5 - Tạo lời thuyết minh cho 10 bài...")
print("Các đoạn đã tạo được lưu lại để lần chạy sau có thể dùng tiếp.")

audio_result = subprocess.run(
    [sys.executable, str(SCRIPT), "--audio"],
    text=True,
)

if audio_result.returncode != 0:
    raise RuntimeError(
        "Không tạo được âm thanh. Hãy kiểm tra thông báo phía trên."
    )

# ============================================================
# DỰNG VIDEO
# ============================================================

print("4/5 - Dựng video Manim.")
print("Bước này chạy bằng CPU; vui lòng giữ phiên Colab hoạt động.")
print("Nhật ký dựng:", ROOT / "render.log")

MEDIA_DIR = ROOT / "media"

render_command = [
    sys.executable, "-m", "manim",
    "--renderer", "cairo",
    "--disable_caching",
    "-r", RESOLUTION,
    "--fps", FPS,
    "--media_dir", str(MEDIA_DIR),
    "-o", OUTPUT_NAME,
    str(SCRIPT),
    "RelatedRates",
]

run_checked(render_command, "render.log")

candidates = [
    p for p in MEDIA_DIR.rglob(f"{OUTPUT_NAME}.mp4")
    if "partial_movie_files" not in p.parts
]

if not candidates:
    raise FileNotFoundError(
        "Không tìm thấy video hoàn chỉnh. "
        f"Hãy mở nhật ký {ROOT / 'render.log'}."
    )

rendered_video = max(candidates, key=lambda p: p.stat().st_mtime)
shutil.copy2(rendered_video, FINAL_VIDEO)

# ============================================================
# KIỂM TRA VIDEO VÀ HIỂN THỊ
# ============================================================

print("5/5 - Kiểm tra video và hiển thị kết quả...")

probe = subprocess.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=codec_type",
        "-of", "json",
        str(FINAL_VIDEO),
    ],
    capture_output=True,
    text=True,
    check=True,
)

import json
info = json.loads(probe.stdout)

duration = float(info["format"]["duration"])
stream_types = {
    stream.get("codec_type")
    for stream in info.get("streams", [])
}

if "video" not in stream_types or "audio" not in stream_types:
    raise RuntimeError(
        "Video tạo ra thiếu hình hoặc âm thanh. "
        "Hãy kiểm tra render.log."
    )

size_mb = FINAL_VIDEO.stat().st_size / (1024 * 1024)
minutes = int(duration // 60)
seconds = int(duration % 60)

print("\n" + "=" * 62)
print("ĐÃ TẠO XONG VIDEO")
print("Tệp:", FINAL_VIDEO)
print(f"Thời lượng: {minutes} phút {seconds} giây")
print(f"Dung lượng: {size_mb:.1f} MB")
print("Có đủ luồng hình và âm thanh.")
print("=" * 62)

from IPython.display import display, Video

# Nếu bản chính lớn, tạo bản xem trước nhẹ hơn để tránh
# nhúng dữ liệu quá lớn vào đầu ra notebook.
PREVIEW_VIDEO = ROOT / "xem_truoc.mp4"

if size_mb > 65:
    print("Đang tạo bản xem trước nhẹ hơn; bản chính vẫn giữ nguyên.")
    run_checked(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(FINAL_VIDEO),
            "-vf", "scale=854:-2",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "30",
            "-c:a", "aac",
            "-b:a", "64k",
            "-movflags", "+faststart",
            str(PREVIEW_VIDEO),
        ],
        "preview.log",
    )
    display(Video(str(PREVIEW_VIDEO), embed=True, width=960))
else:
    display(Video(str(FINAL_VIDEO), embed=True, width=960))

# Nút tải video gốc trên Colab.
try:
    from google.colab import files
    import ipywidgets as widgets

    button = widgets.Button(
        description="TẢI VIDEO GỐC",
        button_style="success",
        icon="download",
        layout=widgets.Layout(width="220px", height="42px"),
    )

    def download_video(_):
        files.download(str(FINAL_VIDEO))

    button.on_click(download_video)
    display(button)

    if AUTO_DOWNLOAD:
        files.download(str(FINAL_VIDEO))

except ImportError:
    print("Video đã được lưu tại:", FINAL_VIDEO)

print(
    "\nNếu nút tải không hiện: mở biểu tượng thư mục bên trái Colab, "
    "tìm tệp Toc_do_thay_doi_10_bai_Thay_Sang.mp4 trong /content, "
    "nhấn chuột phải rồi chọn Download."
)