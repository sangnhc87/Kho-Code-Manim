# =====================================================================
# GOOGLE COLAB — DÁN TOÀN BỘ VÀO MỘT Ô RỒI CHẠY
# MANIM + LATEX + GIỌNG NAM TIẾNG VIỆT
# 12 TRẮC NGHIỆM + 4 ĐÚNG SAI + 6 TRẢ LỜI NGẮN
# Footer: Thầy Nguyễn Văn Sang
# =====================================================================

import os
import sys
import re
import json
import math
import time
import asyncio
import hashlib
import subprocess
import textwrap
import shutil
import zipfile
from pathlib import Path

# ======================== 1. CẤU HÌNH ================================

TEN_THAY = "Thầy Nguyễn Văn Sang"
GIONG_DOC = "vi-VN-NamMinhNeural"
TOC_DO_DOC = "-5%"

# Để [] sẽ dựng đầy đủ 22 bài cùng mở đầu và tổng kết.
# Có thể thử riêng bằng ["TN01"] hoặc ["TN01", "DS01"].
CHON_BAI = []

CHIEU_RONG = 1280
CHIEU_CAO = 720
FPS = 15

HIEN_VIDEO = True
TU_DONG_TAI_VIDEO = False

if Path("/content").exists():
    ROOT = Path("/content/Video_Thay_Nguyen_Van_Sang")
else:
    ROOT = (Path(__file__).resolve().parent / "Video_Thay_Nguyen_Van_Sang") if "__file__" in globals() else (Path.cwd() / "Video_Thay_Nguyen_Van_Sang")

ROOT.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(exist_ok=True)

os.environ["DEBIAN_FRONTEND"] = "noninteractive"
os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"


def run_log(command, logfile, cwd=None):
    logfile = Path(logfile)
    with logfile.open("w", encoding="utf-8") as f:
        result = subprocess.run(
            [str(x) for x in command],
            cwd=cwd,
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True,
        )
    if result.returncode != 0:
        print(logfile.read_text(encoding="utf-8", errors="replace")[-18000:])
        raise RuntimeError(
            "Lệnh chạy thất bại. Nhật ký được lưu tại:\n" + str(logfile)
        )


def probe_duration(path):
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
    value = float(result.stdout.strip())
    if not math.isfinite(value) or value <= 0:
        raise RuntimeError("Tệp âm thanh/video không có thời lượng hợp lệ.")
    return value


# ======================== 2. CÀI ĐẶT =================================

print("BƯỚC 1/5 — Cài môi trường Manim, LaTeX, FFmpeg và giọng đọc.")

marker = ROOT / "environment_019_v2.ok"

if Path("/content").exists() and not marker.exists():
    run_log(
        ["apt-get", "update", "-qq"],
        ROOT / "apt_update.log",
    )
    run_log(
        [
            "apt-get", "install", "-y", "-qq",
            "ffmpeg", "pkg-config", "python3-dev",
            "libcairo2-dev", "libpango1.0-dev",
            "texlive-latex-base",
            "texlive-latex-recommended",
            "texlive-latex-extra",
            "texlive-fonts-recommended",
            "texlive-science",
            "dvisvgm",
            "fonts-dejavu-core",
            "fonts-noto-core",
        ],
        ROOT / "apt_install.log",
    )
    run_log(
        [
            sys.executable, "-m", "pip", "install", "-q",
            "manim==0.19.0", "edge-tts", "nest_asyncio",
        ],
        ROOT / "pip_install.log",
    )

    run_log(
        [
            sys.executable, "-c",
            "import manim, edge_tts; print(manim.__version__)",
        ],
        ROOT / "environment_check.log",
    )
    marker.write_text("OK", encoding="utf-8")

# ====================== 3. DỮ LIỆU BÀI GIẢNG ===========================
#
# Mỗi dòng công thức là một chuỗi raw nằm trọn trên một dòng.
# Không dùng chuỗi r"..." xuống dòng trái phép.
#
# T: chữ tiếng Việt.
# M: công thức LaTeX + lời đọc tiếng Việt.
# P: một trang.
# Q: một bài.
# =====================================================================

def T(text, voice=None):
    return {
        "kind": "text",
        "text": text,
        "voice": voice if voice is not None else text,
    }


def M(tex, voice):
    return {"kind": "math", "text": tex, "voice": voice}


def P(title, *rows):
    return {"title": title, "rows": list(rows)}


LESSONS = []


def Q(code, section, title, diagram, *pages):
    LESSONS.append({
        "id": code,
        "section": section,
        "title": title,
        "diagram": diagram,
        "intro": {
            "voice": section + ". " + title + "."
        },
        "pages": list(pages),
    })


# ----------------------- PHẦN I: TRẮC NGHIỆM --------------------------

Q(
    "TN01", "PHẦN I — CÂU 1",
    "Rào vườn giáp bờ sông", "river",
    P(
        "Đề bài và ràng buộc",
        T("Có 80 m lưới rào; cạnh giáp sông không cần rào.",
          "Có tám mươi mét lưới để rào một mảnh vườn hình chữ nhật giáp sông. Cạnh phía sông không cần rào. Tìm diện tích lớn nhất."),
        M(r"2x+y=80,\qquad x>0,\quad y>0",
          "Gọi x là chiều rộng vuông góc bờ sông, y là chiều dài. Tổng ba cạnh cần rào là hai x cộng y bằng tám mươi."),
        M(r"y=80-2x,\qquad 0<x<40",
          "Suy ra y bằng tám mươi trừ hai x. Vì các cạnh đều dương nên x nằm giữa không và bốn mươi."),
        M(r"S(x)=x(80-2x)=-2x^2+80x",
          "Diện tích bằng x nhân tám mươi trừ hai x, bằng âm hai x bình phương cộng tám mươi x."),
    ),
    P(
        "Tối ưu và kiểm tra dấu bằng",
        M(r"S(x)=-2(x-20)^2+800\le800",
          "Hoàn thành bình phương, được âm hai nhân x trừ hai mươi bình phương, cộng tám trăm. Vì bình phương không âm, diện tích không vượt quá tám trăm."),
        M(r"x=20,\qquad y=80-2\cdot20=40",
          "Dấu bằng đạt khi x bằng hai mươi mét. Khi đó y bằng bốn mươi mét, thỏa mãn điều kiện."),
        M(r"\boxed{S_{\max}=800\ \mathrm{m}^2}\qquad \mathrm{A}",
          "Vậy diện tích lớn nhất bằng tám trăm mét vuông. Chọn A."),
    ),
)

Q(
    "TN02", "PHẦN I — CÂU 2",
    "Hình chữ nhật trong tam giác vuông cân", "triangle_rect",
    P(
        "Đề bài và chiều cao tam giác",
        T("ABC vuông cân tại A, cạnh huyền BC = 12 cm.",
          "Tam giác A B C vuông cân tại A, cạnh huyền B C bằng mười hai xăng ti mét. Tìm diện tích lớn nhất của hình chữ nhật nội tiếp có một cạnh nằm trên B C."),
        T("Đặt MN trên BC; P thuộc AC; Q thuộc AB.",
          "Hình minh họa được đặt lại nhãn cho đúng phần lời của đề: M N nằm trên B C, P thuộc A C, Q thuộc A B."),
        M(r"AH=\frac{BC}{2}=6\ \mathrm{cm}",
          "Trong tam giác vuông cân, đường cao từ góc vuông đồng thời là trung tuyến, nên A H bằng sáu xăng ti mét."),
        M(r"0<x<6,\qquad MN=y",
          "Gọi x là chiều cao hình chữ nhật, y là độ dài đáy M N."),
    ),
    P(
        "Đồng dạng và tối ưu",
        M(r"\frac{y}{12}=\frac{6-x}{6}\quad\Longrightarrow\quad y=12-2x",
          "Tam giác phía trên hình chữ nhật đồng dạng với tam giác ban đầu. Do đó y trên mười hai bằng sáu trừ x trên sáu, suy ra y bằng mười hai trừ hai x."),
        M(r"S(x)=x(12-2x)=-2(x-3)^2+18",
          "Diện tích bằng x nhân mười hai trừ hai x. Hoàn thành bình phương được âm hai nhân x trừ ba bình phương, cộng mười tám."),
        M(r"S(x)\le18,\qquad x=3,\quad y=6",
          "Diện tích không vượt quá mười tám, đạt được khi chiều cao bằng ba và đáy bằng sáu xăng ti mét."),
        M(r"\boxed{S_{\max}=18\ \mathrm{cm}^2}\qquad \mathrm{A}",
          "Vậy diện tích lớn nhất là mười tám xăng ti mét vuông. Chọn A."),
    ),
)

Q(
    "TN03", "PHẦN I — CÂU 3",
    "Dây 20 m: hình vuông và hình tròn", "square_circle",
    P(
        "Lập hàm tổng diện tích",
        T("Chia dây 20 m; cần tổng diện tích nhỏ nhất.",
          "Chia dây dài hai mươi mét thành hai phần để uốn hình vuông và hình tròn. Cần tìm cạnh hình vuông khi tổng diện tích nhỏ nhất."),
        M(r"0<x<20,\qquad a=\frac{x}{4},\qquad r=\frac{20-x}{2\pi}",
          "Gọi x là chiều dài dây uốn hình vuông. Cạnh vuông bằng x trên bốn; bán kính tròn bằng hai mươi trừ x trên hai pi."),
        M(r"S(x)=\frac{x^2}{16}+\frac{(20-x)^2}{4\pi}",
          "Tổng diện tích bằng x bình phương trên mười sáu, cộng hai mươi trừ x bình phương trên bốn pi."),
    ),
    P(
        "Đạo hàm và cực tiểu",
        M(r"S'(x)=\frac{x}{8}-\frac{20-x}{2\pi}",
          "Đạo hàm bằng x trên tám trừ hai mươi trừ x trên hai pi."),
        M(r"S'(x)=0\iff(\pi+4)x=80\iff x_*=\frac{80}{\pi+4}",
          "Cho đạo hàm bằng không, quy đồng được pi cộng bốn nhân x bằng tám mươi. Suy ra x bằng tám mươi trên pi cộng bốn."),
        M(r"S''(x)=\frac18+\frac1{2\pi}>0",
          "Đạo hàm cấp hai luôn dương. Vì vậy đây là điểm đạt tổng diện tích nhỏ nhất duy nhất."),
        M(r"\boxed{a=\frac{x_*}{4}=\frac{20}{\pi+4}\ \mathrm{m}}\quad\mathrm{A}",
          "Đề hỏi cạnh hình vuông, nên phải chia chiều dài dây cho bốn. Đáp án là hai mươi trên pi cộng bốn mét. Chọn A."),
    ),
    P(
        "Nhận xét hình học",
        M(r"2r=\frac{20-x_*}{\pi}=\frac{20}{\pi+4}=a",
          "Tại cấu hình tối ưu, đường kính hình tròn bằng cạnh hình vuông."),
        T("Không nhầm cạnh hình vuông với chu vi hình vuông.",
          "Lưu ý biến x là chu vi hình vuông, không phải cạnh. Đây là chỗ rất dễ chọn nhầm đáp án."),
    ),
)

Q(
    "TN04", "PHẦN I — CÂU 4",
    "Cửa sổ vòm Norman", "window",
    P(
        "Chu vi đường bao ngoài",
        T("Cửa sổ gồm hình chữ nhật và nửa hình tròn; chu vi 10 m.",
          "Cửa sổ gồm phần chữ nhật bên dưới và một nửa hình tròn bên trên. Tổng chu vi ngoài bằng mười mét. Tìm bán kính để diện tích lớn nhất."),
        M(r"2h+2R+\pi R=10",
          "Gọi bán kính vòm là R và chiều cao phần chữ nhật là h. Chu vi gồm hai cạnh h, đáy hai R và cung tròn pi R."),
        T("Không cộng đường kính chung nằm bên trong.",
          "Không cộng đường kính chung giữa hai phần, vì đó không phải đường bao ngoài."),
        M(r"h=5-\frac{\pi+2}{2}R,\qquad 0<R<\frac{10}{\pi+2}",
          "Suy ra h bằng năm trừ pi cộng hai trên hai nhân R. Điều kiện h dương cho miền giá trị của R như trên."),
    ),
    P(
        "Tối ưu diện tích",
        M(r"S=2Rh+\frac{\pi R^2}{2}=10R-\frac{\pi+4}{2}R^2",
          "Diện tích bằng hai R h cộng nửa pi R bình phương. Thay h rồi rút gọn được mười R trừ pi cộng bốn trên hai nhân R bình phương."),
        M(r"S'(R)=10-(\pi+4)R,\qquad S''(R)=-(\pi+4)<0",
          "Đạo hàm bằng mười trừ pi cộng bốn nhân R. Đạo hàm cấp hai âm nên nghiệm đạo hàm bậc nhất cho diện tích lớn nhất."),
        M(r"R_*=\frac{10}{\pi+4},\qquad h_*=\frac{10}{\pi+4}=R_*",
          "Bán kính tối ưu là mười trên pi cộng bốn. Thay lại ta cũng được chiều cao phần chữ nhật bằng bán kính."),
        M(r"\boxed{R=\frac{10}{\pi+4}\ \mathrm{m}}\qquad\mathrm{A}",
          "Vậy chọn A."),
    ),
)

Q(
    "TN05", "PHẦN I — CÂU 5",
    "Hình thang trong nửa đường tròn", "semicircle_trap",
    P(
        "Biểu diễn theo góc ở tâm",
        T("Hình thang cân ABCD có đáy AB là đường kính 2R.",
          "Hình thang cân A B C D nội tiếp nửa đường tròn, đáy lớn A B là đường kính hai R. Tìm diện tích lớn nhất."),
        M(r"\alpha=\angle BOC,\qquad 0<\alpha<\frac{\pi}{2}",
          "Gọi O là trung điểm A B và an pha là góc B O C. Góc này nằm giữa không và pi trên hai."),
        M(r"CD=2R\cos\alpha,\qquad h=R\sin\alpha",
          "Đáy nhỏ bằng hai R cô sin an pha, chiều cao bằng R sin an pha."),
        M(r"S(\alpha)=R^2\sin\alpha(1+\cos\alpha)",
          "Theo công thức diện tích hình thang, diện tích bằng R bình phương sin an pha nhân một cộng cô sin an pha."),
    ),
    P(
        "Đạo hàm và dấu",
        M(r"S'(\alpha)=R^2(\cos\alpha+\cos2\alpha)",
          "Đạo hàm bằng R bình phương nhân cô sin an pha cộng cô sin hai an pha."),
        M(r"S'(\alpha)=R^2(2\cos\alpha-1)(\cos\alpha+1)",
          "Dùng công thức góc đôi rồi phân tích thành nhân tử."),
        M(r"S'=0\iff\cos\alpha=\frac12\iff\alpha=\frac{\pi}{3}",
          "Trong miền xét, cô sin an pha cộng một dương, nên đạo hàm bằng không khi an pha bằng pi trên ba."),
        T("Đạo hàm dương trước π/3 và âm sau π/3.",
          "Vì cô sin giảm theo góc trong miền này, đạo hàm dương trước pi trên ba và âm sau pi trên ba. Đây là điểm cực đại toàn cục."),
    ),
    P(
        "Kết luận",
        M(r"S_{\max}=R^2\frac{\sqrt3}{2}\left(1+\frac12\right)",
          "Thay góc sáu mươi độ, sin bằng căn ba trên hai và cô sin bằng một phần hai."),
        M(r"\boxed{S_{\max}=\frac{3\sqrt3}{4}R^2}\qquad\mathrm{A}",
          "Diện tích lớn nhất bằng ba căn ba trên bốn nhân R bình phương. Chọn A."),
        T("Hình thang tối ưu gồm 3 tam giác đều cạnh R.",
          "Khi đó hình thang được chia bởi hai bán kính thành ba tam giác đều cạnh R."),
    ),
)

Q(
    "TN06", "PHẦN I — CÂU 6",
    "Vị trí quan sát bức tranh", "viewing",
    P(
        "Đo độ cao từ tầm mắt",
        T("Tranh cao 2 m, mép dưới cao 3 m, mắt cao 1,5 m.",
          "Tranh cao hai mét, mép dưới cách đất ba mét. Người quan sát có mắt cao một phẩy năm mét. Tìm khoảng cách đến tường để góc nhìn lớn nhất."),
        M(r"h_1=3-1{,}5=1{,}5,\quad h_2=5-1{,}5=3{,}5",
          "Tính từ tầm mắt, mép dưới cao một phẩy năm mét, mép trên cao ba phẩy năm mét."),
        M(r"\theta=\beta-\alpha,\quad \tan\beta=\frac{3{,}5}{x},\quad \tan\alpha=\frac{1{,}5}{x}",
          "Gọi khoảng cách đến tường là x dương. Góc nhìn bằng bê ta trừ an pha. Tang hai góc lần lượt bằng ba phẩy năm trên x và một phẩy năm trên x."),
    ),
    P(
        "Tối ưu tang của góc nhìn",
        M(r"\tan\theta=\frac{3{,}5/x-1{,}5/x}{1+5{,}25/x^2}=\frac{2}{x+5{,}25/x}",
          "Dùng công thức tang của hiệu rồi rút gọn, được hai chia cho x cộng năm phẩy hai lăm trên x."),
        T("Vì 0° < θ < 90°, tối đa θ tương đương tối đa tan θ.",
          "Góc nhìn nằm giữa không và chín mươi độ, tang đồng biến trên khoảng này. Vì vậy chỉ cần làm mẫu số nhỏ nhất."),
        M(r"x+\frac{5{,}25}{x}\ge2\sqrt{5{,}25}",
          "Theo bất đẳng thức trung bình cộng và trung bình nhân, mẫu số không nhỏ hơn hai căn năm phẩy hai lăm."),
        M(r"\boxed{x=\sqrt{5{,}25}\approx2{,}29\ \mathrm{m}}\qquad\mathrm{A}",
          "Dấu bằng khi x bình phương bằng năm phẩy hai lăm. Khoảng cách tối ưu xấp xỉ hai phẩy hai chín mét. Chọn A."),
    ),
)

Q(
    "TN07", "PHẦN I — CÂU 7",
    "Hình chữ nhật nội tiếp elip", "ellipse",
    P(
        "Ràng buộc và diện tích",
        M(r"(E):\frac{x^2}{16}+\frac{y^2}{9}=1",
          "Cho elip x bình phương trên mười sáu cộng y bình phương trên chín bằng một. Hình chữ nhật nội tiếp có các cạnh song song trục tọa độ."),
        M(r"M(x,y),\quad x,y>0,\qquad S=4xy",
          "Chọn đỉnh ở góc phần tư thứ nhất là M có tọa độ x, y. Hai cạnh hình chữ nhật dài hai x và hai y, nên diện tích bằng bốn x y."),
        T("Cần tối đa tích xy dưới ràng buộc elip.",
          "Ta cần tìm giá trị lớn nhất của tích x y với ràng buộc điểm M nằm trên elip."),
    ),
    P(
        "Chuẩn hóa và dùng bất đẳng thức",
        M(r"2\frac{x}{4}\frac{y}{3}\le\left(\frac{x}{4}\right)^2+\left(\frac{y}{3}\right)^2=1",
          "Áp dụng hai u v không vượt quá u bình phương cộng v bình phương, với u bằng x trên bốn và v bằng y trên ba."),
        M(r"xy\le6\quad\Longrightarrow\quad S\le24",
          "Suy ra tích x y không vượt quá sáu, diện tích không vượt quá hai mươi bốn."),
        M(r"\frac{x}{4}=\frac{y}{3}=\frac1{\sqrt2}\iff x=2\sqrt2,\ y=\frac{3\sqrt2}{2}",
          "Dấu bằng khi x trên bốn bằng y trên ba. Kết hợp phương trình elip, ta được x bằng hai căn hai, y bằng ba căn hai trên hai."),
        M(r"\boxed{S_{\max}=24}\qquad\mathrm{A}",
          "Vậy diện tích lớn nhất là hai mươi bốn. Chọn A."),
    ),
)

Q(
    "TN08", "PHẦN I — CÂU 8",
    "Hình chữ nhật dưới parabol", "parabola",
    P(
        "Lập hàm diện tích",
        M(r"y=9-x^2,\qquad y\ge0",
          "Xét hình chữ nhật có hai đỉnh trên trục hoành và hai đỉnh trên parabol y bằng chín trừ x bình phương, trong miền y không âm."),
        M(r"0<x<3,\quad w=2x,\quad h=9-x^2",
          "Hai đỉnh trên cùng độ cao nên có hoành độ đối nhau. Đặt hoành độ dương là x. Chiều rộng bằng hai x, chiều cao bằng chín trừ x bình phương."),
        M(r"S(x)=2x(9-x^2)=18x-2x^3",
          "Diện tích bằng hai x nhân chín trừ x bình phương, bằng mười tám x trừ hai x lập phương."),
    ),
    P(
        "Khảo sát và kết luận",
        M(r"S'(x)=18-6x^2=0\iff x=\sqrt3",
          "Đạo hàm bằng mười tám trừ sáu x bình phương. Nghiệm dương trong miền là căn ba."),
        T("S tăng trên (0, √3), giảm trên (√3, 3).",
          "Đạo hàm dương trước căn ba và âm sau căn ba, nên diện tích đạt lớn nhất tại x bằng căn ba."),
        M(r"h=6,\qquad S_{\max}=2\sqrt3\cdot6=12\sqrt3",
          "Khi đó chiều cao bằng sáu. Nhân với chiều rộng hai căn ba được mười hai căn ba."),
        M(r"\boxed{S_{\max}=12\sqrt3}\qquad\mathrm{A}",
          "Vậy chọn A."),
    ),
)

Q(
    "TN09", "PHẦN I — CÂU 9",
    "Dây 36 cm: tam giác đều và hình vuông", "triangle_square",
    P(
        "Chọn chu vi tam giác làm biến",
        T("Dây 36 cm; cần tổng diện tích hai hình nhỏ nhất.",
          "Dây dài ba mươi sáu xăng ti mét được chia để uốn tam giác đều và hình vuông. Tìm chu vi tam giác khi tổng diện tích nhỏ nhất."),
        M(r"0<x<36,\quad a=\frac{x}{3},\quad b=\frac{36-x}{4}",
          "Gọi x là chu vi tam giác đều, cạnh tam giác bằng x trên ba, cạnh hình vuông bằng ba mươi sáu trừ x trên bốn."),
        M(r"S(x)=\frac{\sqrt3}{36}x^2+\frac{(36-x)^2}{16}",
          "Tổng diện tích bằng căn ba trên ba mươi sáu nhân x bình phương, cộng ba mươi sáu trừ x bình phương trên mười sáu."),
    ),
    P(
        "Giải phương trình đạo hàm",
        M(r"S'(x)=\frac{\sqrt3}{18}x-\frac{36-x}{8}",
          "Đạo hàm bằng căn ba trên mười tám nhân x, trừ ba mươi sáu trừ x trên tám."),
        M(r"S'=0\iff4\sqrt3\,x=9(36-x)\iff x=\frac{324}{9+4\sqrt3}",
          "Cho đạo hàm bằng không và nhân với bảy mươi hai, được bốn căn ba x bằng chín nhân ba mươi sáu trừ x. Suy ra kết quả trên."),
        M(r"S''(x)=\frac{\sqrt3}{18}+\frac18>0",
          "Đạo hàm cấp hai dương, nên đây là điểm đạt tổng diện tích nhỏ nhất."),
        M(r"\boxed{x=\frac{108\sqrt3}{4+3\sqrt3}\ \mathrm{cm}}\qquad\mathrm{A}",
          "Biến đổi về dạng đáp án, chu vi tam giác là một trăm linh tám căn ba trên bốn cộng ba căn ba xăng ti mét. Chọn A."),
    ),
)

Q(
    "TN10", "PHẦN I — CÂU 10",
    "Trang sách tiết kiệm giấy", "book",
    P(
        "Phân biệt vùng in và cả trang",
        T("Vùng in 384 cm²; lề trái/phải 2 cm; trên/dưới 3 cm.",
          "Vùng in chữ có diện tích ba trăm tám mươi bốn xăng ti mét vuông. Hai lề bên rộng hai xăng ti mét, hai lề trên dưới rộng ba xăng ti mét."),
        M(r"xy=384,\qquad y=\frac{384}{x},\quad x>0",
          "Gọi x là chiều rộng, y là chiều cao vùng in. Tích x y bằng ba trăm tám mươi bốn."),
        M(r"X=x+4,\qquad Y=y+6",
          "Chiều rộng cả trang bằng x cộng bốn, chiều cao cả trang bằng y cộng sáu."),
    ),
    P(
        "Tối thiểu diện tích giấy",
        M(r"S(x)=(x+4)\left(\frac{384}{x}+6\right)=408+6x+\frac{1536}{x}",
          "Diện tích cả trang bằng tích hai kích thước. Khai triển được bốn trăm linh tám cộng sáu x cộng một nghìn năm trăm ba mươi sáu trên x."),
        M(r"S(x)=408+6\left(x+\frac{256}{x}\right)\ge408+6\cdot32=600",
          "Đưa sáu ra ngoài rồi áp dụng bất đẳng thức trung bình cộng và trung bình nhân, diện tích không nhỏ hơn sáu trăm."),
        M(r"x=16,\quad y=24,\qquad X=20,\quad Y=30",
          "Dấu bằng khi x bằng mười sáu. Khi đó y bằng hai mươi bốn, cả trang rộng hai mươi và cao ba mươi xăng ti mét."),
        M(r"\boxed{20\ \mathrm{cm}\times30\ \mathrm{cm}}\qquad\mathrm{A}",
          "Chọn kích thước hai mươi nhân ba mươi xăng ti mét. Đáp án A."),
    ),
)

Q(
    "TN11", "PHẦN I — CÂU 11",
    "Gập máng nước hình thang", "gutter",
    P(
        "Biểu diễn kích thước theo góc gập",
        T("Dải tôn 30 cm, chia thành ba phần đều 10 cm.",
          "Dải tôn rộng ba mươi xăng ti mét, chia thành ba phần đều nhau. Gập hai phần bên lên góc thê ta so với phương ngang."),
        M(r"0<\theta<\frac{\pi}{2},\qquad h=10\sin\theta",
          "Chiều cao máng bằng mười sin thê ta."),
        M(r"b=10,\qquad B=10+20\cos\theta",
          "Đáy nhỏ bằng mười, đáy lớn bằng mười cộng hai mươi cô sin thê ta."),
        M(r"S(\theta)=100\sin\theta(1+\cos\theta)",
          "Diện tích mặt cắt bằng một trăm sin thê ta nhân một cộng cô sin thê ta."),
    ),
    P(
        "Tối ưu góc gập",
        M(r"S'(\theta)=100(\cos\theta+\cos^2\theta-\sin^2\theta)",
          "Lấy đạo hàm theo quy tắc tích."),
        M(r"S'(\theta)=100(2\cos\theta-1)(\cos\theta+1)",
          "Dùng sin bình phương cộng cô sin bình phương bằng một rồi phân tích thành nhân tử."),
        M(r"S'=0\iff\cos\theta=\frac12\iff\theta=\frac{\pi}{3}",
          "Nghiệm trong miền là thê ta bằng pi trên ba. Đạo hàm dương trước nghiệm và âm sau nghiệm nên đây là điểm cực đại."),
        M(r"\boxed{\theta=60^\circ}\qquad\mathrm{A}",
          "Góc gập tối ưu bằng sáu mươi độ. Chọn A."),
    ),
)

Q(
    "TN12", "PHẦN I — CÂU 12",
    "Sân khấu và kích thước phòng", "stage",
    P(
        "Mô hình đoạn chắn",
        T("Phòng 20 m × 12 m; cạnh huyền sân khấu đi qua K.",
          "Phòng dài hai mươi mét, rộng mười hai mét. Sân khấu là tam giác vuông ở góc phòng, cạnh huyền đi qua điểm K cách hai tường một mét và tám mét."),
        M(r"A=(0,0),\ K=(1,8),\ M=(a,0),\ N=(0,b)",
          "Chọn trục theo hai tường để K có tọa độ một, tám. Hai giao điểm cạnh huyền với tường là M và N."),
        M(r"\frac{x}{a}+\frac{y}{b}=1\quad\Longrightarrow\quad\frac1a+\frac8b=1",
          "Theo phương trình đoạn chắn và điều kiện cạnh huyền qua K, một trên a cộng tám trên b bằng một."),
        M(r"S=\frac{ab}{2},\qquad a>1,\quad b>8",
          "Diện tích bằng a b trên hai. Vì K nằm trong đoạn cạnh huyền nên a lớn hơn một và b lớn hơn tám."),
    ),
    P(
        "Cận dưới diện tích",
        M(r"1=\frac1a+\frac8b\ge2\sqrt{\frac8{ab}}",
          "Áp dụng bất đẳng thức trung bình cộng và trung bình nhân cho một trên a và tám trên b."),
        M(r"1\ge\frac{32}{ab}\quad\Longrightarrow\quad ab\ge32",
          "Bình phương hai vế không âm, suy ra a b không nhỏ hơn ba mươi hai."),
        M(r"S\ge16,\quad \frac1a=\frac8b=\frac12\iff(a,b)=(2,16)",
          "Vậy diện tích không nhỏ hơn mười sáu. Dấu bằng chỉ khi a bằng hai và b bằng mười sáu."),
        T("Cần kiểm tra cạnh 16 m có nằm trên tường 20 m không.",
          "Không được dừng ở bất đẳng thức. Cạnh dài mười sáu mét phải nằm trên bức tường đủ dài."),
    ),
    P(
        "Hướng bố trí phù hợp đáp án A",
        M(r"a\le12,\qquad b\le20",
          "Nếu trục hoành theo tường mười hai mét và trục tung theo tường hai mươi mét, thì a không vượt quá mười hai, b không vượt quá hai mươi."),
        M(r"(a,b)=(2,16)\quad\text{is feasible}",
          "Khi đó cấu hình hai mét và mười sáu mét nằm trong phòng."),
        M(r"\boxed{S_{\min}=16\ \mathrm{m}^2}\qquad\mathrm{A}",
          "Trong cách bố trí này, đáp án là mười sáu mét vuông, chọn A."),
    ),
    P(
        "Nếu hai hướng tường được gán ngược lại",
        M(r"a\le20,\quad b\le12,\quad b=\frac{8a}{a-1}\quad\Longrightarrow\quad a\ge3",
          "Nếu trục hoành theo tường hai mươi mét và trục tung theo tường mười hai mét, thì b không vượt quá mười hai. Thay b bằng tám a trên a trừ một, suy ra a không nhỏ hơn ba."),
        M(r"S(a)=\frac{4a^2}{a-1},\qquad S'(a)=\frac{4a(a-2)}{(a-1)^2}>0\quad(a\ge3)",
          "Diện tích bằng bốn a bình phương trên a trừ một. Đạo hàm dương trên miền khả thi, nên diện tích tăng theo a."),
        M(r"\boxed{S_{\min}=S(3)=18\ \mathrm{m}^2}\qquad\mathrm{B}",
          "Giá trị nhỏ nhất khi a bằng ba và b bằng mười hai, diện tích bằng mười tám mét vuông, tương ứng B."),
        T("Đề cần chỉ rõ khoảng cách 1 m và 8 m ứng với tường nào.",
          "Vì thế đề cần nêu rõ khoảng cách một mét và tám mét ứng với tường nào. Không nên mặc nhiên bỏ qua kích thước phòng."),
    ),
)

# ----------------------- PHẦN II: ĐÚNG SAI ----------------------------

Q(
    "DS01", "PHẦN II — CÂU 1",
    "Hồ bơi hai đầu bán nguyệt", "stadium",
    P(
        "Dữ kiện và ý a",
        T("Hồ gồm chữ nhật x × y và hai nửa tròn đường kính y.",
          "Hồ bơi gồm hình chữ nhật kích thước x nhân y và hai nửa hình tròn đường kính y ở hai đầu. Tổng chu vi là hai trăm mét."),
        M(r"P=2x+\pi y=200",
          "Đường bao gồm hai đoạn thẳng dài x và hai nửa đường tròn ghép thành một đường tròn. Vì vậy chu vi bằng hai x cộng pi y."),
        T("a) P = 2x + πy: ĐÚNG.",
          "Mệnh đề a đúng."),
        M(r"x=100-\frac{\pi y}{2},\qquad S=xy+\frac{\pi y^2}{4}",
          "Suy ra x bằng một trăm trừ pi y trên hai. Diện tích bằng x y cộng pi y bình phương trên bốn."),
    ),
    P(
        "Ý b — công thức diện tích",
        T("b) S(y) = 200y − πy²: SAI.",
          "Ý b cho rằng diện tích bằng hai trăm y trừ pi y bình phương. Ta kiểm tra bằng cách thế x."),
        M(r"S(y)=y\left(100-\frac{\pi y}{2}\right)+\frac{\pi y^2}{4}",
          "Thay x vào tổng diện tích hai phần."),
        M(r"\boxed{S(y)=100y-\frac{\pi y^2}{4}}",
          "Rút gọn được một trăm y trừ pi y bình phương trên bốn. Vì vậy ý b sai."),
    ),
    P(
        "Ý c — có cho phép hình suy biến không?",
        M(r"S'(y)=100-\frac{\pi y}{2}",
          "Đạo hàm diện tích theo y bằng một trăm trừ pi y trên hai."),
        M(r"S'(y)=0\iff y=\frac{200}{\pi}\iff x=0",
          "Đạo hàm bằng không khi y bằng hai trăm trên pi, tương ứng x bằng không."),
        T("c) ĐÚNG nếu cho phép x = 0: hồ trở thành hình tròn.",
          "Ý c đúng nếu cho phép phần chữ nhật suy biến, tức x bằng không. Khi đó hồ là một hình tròn hoàn chỉnh."),
        T("Nếu bắt buộc x > 0: không đạt giá trị lớn nhất.",
          "Nếu bắt buộc x dương, thì không có giá trị lớn nhất. Chỉ có cận trên đạt tới trong giới hạn khi x tiến về không."),
    ),
    P(
        "Ý d — thêm điều kiện x ≥ 20 m",
        M(r"x\ge20\quad\Longrightarrow\quad y\le\frac{160}{\pi}",
          "Với điều kiện x ít nhất hai mươi mét, y không vượt quá một trăm sáu mươi trên pi."),
        T("S tăng theo y trong miền này ⇒ chọn x = 20.",
          "Hàm diện tích tăng theo y trong miền xét, nên chọn y lớn nhất, tương ứng x bằng hai mươi."),
        M(r"S_{\max}=20\frac{160}{\pi}+\frac{\pi}{4}\left(\frac{160}{\pi}\right)^2=\frac{9600}{\pi}",
          "Thay kích thước vào công thức, diện tích lớn nhất bằng chín nghìn sáu trăm trên pi."),
        M(r"\pi\approx3{,}1416\quad\Longrightarrow\quad S_{\max}\approx3055{,}77\approx3056\ \mathrm{m}^2",
          "Với pi bằng ba phẩy một bốn một sáu, kết quả xấp xỉ ba nghìn không trăm năm mươi lăm phẩy bảy bảy, làm tròn thành ba nghìn không trăm năm mươi sáu mét vuông."),
    ),
    P(
        "Kết quả toàn câu",
        T("a) ĐÚNG. b) SAI. c) ĐÚNG*. d) ĐÚNG.",
          "Kết quả là đúng, sai, đúng có điều kiện, đúng."),
        T("* Ý c hiểu theo mô hình cho phép x = 0.",
          "Dấu sao nhắc rằng ý c được hiểu theo mô hình cho phép x bằng không."),
    ),
)

Q(
    "DS02", "PHẦN II — CÂU 2",
    "Nhà kính trong vườn tam giác", "greenhouse",
    P(
        "Ý a — chiều dài nhà kính",
        T("Tam giác theo hình: đáy 60 m, chiều cao 40 m.",
          "Xét mảnh vườn tam giác theo hình đã cho, có đáy sáu mươi mét và chiều cao bốn mươi mét. Nhà kính là hình chữ nhật có một cạnh trên đáy tam giác."),
        M(r"0<x<40,\qquad \frac{y}{60}=\frac{40-x}{40}",
          "Gọi x là chiều cao nhà kính và y là chiều dài. Hai tam giác đồng dạng cho y trên sáu mươi bằng bốn mươi trừ x trên bốn mươi."),
        M(r"y=60\left(1-\frac{x}{40}\right)",
          "Suy ra chiều dài y bằng sáu mươi nhân một trừ x trên bốn mươi."),
        T("a) ĐÚNG.",
          "Mệnh đề a đúng."),
    ),
    P(
        "Ý b và c — diện tích lớn nhất",
        M(r"S(x)=60x-\frac32x^2=-\frac32(x-20)^2+600",
          "Diện tích bằng sáu mươi x trừ ba phần hai x bình phương. Hoàn thành bình phương được âm ba phần hai nhân x trừ hai mươi bình phương, cộng sáu trăm."),
        M(r"x_*=20,\qquad y_*=30,\qquad S_{\max}=600\ \mathrm{m}^2",
          "Diện tích lớn nhất bằng sáu trăm mét vuông khi chiều cao hai mươi và chiều dài ba mươi mét."),
        T("b) Diện tích lớn nhất 600 m²: ĐÚNG.",
          "Ý b đúng."),
        T("c) Chiều cao tối ưu 30 m: SAI; đúng là 20 m.",
          "Ý c sai, vì chiều cao tối ưu là hai mươi mét chứ không phải ba mươi mét."),
    ),
    P(
        "Ý d — tổng chi phí",
        M(r"P=2(20+30)=100\ \mathrm{m}",
          "Chu vi nhà kính tối ưu bằng một trăm mét."),
        M(r"C_{\mathrm{floor}}=600\cdot1{,}2=720",
          "Tính theo triệu đồng, chi phí sàn bằng sáu trăm nhân một phẩy hai, bằng bảy trăm hai mươi."),
        M(r"C_{\mathrm{fence}}=100\cdot0{,}2=20,\qquad C=720+20=740",
          "Đơn giá hàng rào hai trăm nghìn đồng tương ứng không phẩy hai triệu. Chi phí rào là hai mươi triệu. Tổng cộng bảy trăm bốn mươi triệu đồng."),
        T("d) ĐÚNG. Kết quả: Đ — Đ — S — Đ.",
          "Ý d đúng. Kết quả toàn câu là đúng, đúng, sai, đúng."),
    ),
)

Q(
    "DS03", "PHẦN II — CÂU 3",
    "Dây đồng: tam giác đều và hình tròn", "triangle_circle",
    P(
        "Lập hàm tổng diện tích",
        T("Dây 100 cm; x cm uốn tam giác, phần còn lại uốn tròn.",
          "Dây đồng dài một trăm xăng ti mét. Gọi x là chiều dài phần uốn thành tam giác đều, phần còn lại uốn thành hình tròn."),
        M(r"a=\frac{x}{3},\qquad r=\frac{100-x}{2\pi}",
          "Cạnh tam giác bằng x trên ba, bán kính hình tròn bằng một trăm trừ x trên hai pi."),
        M(r"S(x)=\frac{\sqrt3}{36}x^2+\frac{(100-x)^2}{4\pi}",
          "Tổng diện tích bằng căn ba trên ba mươi sáu nhân x bình phương, cộng một trăm trừ x bình phương trên bốn pi."),
        M(r"S''(x)=\frac{\sqrt3}{18}+\frac1{2\pi}>0",
          "Đạo hàm cấp hai dương nên hàm là bậc hai mở lên, có cực tiểu chứ không có cực đại ở bên trong miền."),
    ),
    P(
        "Ý a và b",
        T("a) Tổng diện tích lớn nhất khi x = 50 cm: SAI.",
          "Ý a sai. Hàm lồi nghiêm ngặt không thể đạt giá trị lớn nhất tại điểm bên trong như x bằng năm mươi."),
        T("b) Hàm diện tích bậc hai, parabol mở lên: ĐÚNG.",
          "Ý b đúng, vì hệ số của x bình phương dương."),
        M(r"\frac{\sqrt3}{36}+\frac1{4\pi}>0",
          "Cụ thể hệ số đó bằng căn ba trên ba mươi sáu cộng một trên bốn pi, là một số dương."),
    ),
    P(
        "Ý c — quan hệ cạnh và bán kính",
        M(r"S'(x)=\frac{\sqrt3}{18}x-\frac{100-x}{2\pi}=0",
          "Để diện tích nhỏ nhất, cho đạo hàm bằng không."),
        M(r"x=3a,\qquad100-x=2\pi r",
          "Thay chiều dài hai phần dây theo cạnh tam giác và bán kính tròn."),
        M(r"\frac{\sqrt3}{6}a-r=0\iff a=2\sqrt3\,r",
          "Rút gọn được căn ba trên sáu nhân a bằng r, suy ra a bằng hai căn ba nhân r."),
        T("c) ĐÚNG.",
          "Ý c đúng."),
    ),
    P(
        "Ý d — so sánh hai đầu mút",
        M(r"S(0)=\frac{2500}{\pi}\approx795{,}77",
          "Nếu cho phép một phần dây bằng không, uốn toàn bộ thành hình tròn cho diện tích khoảng bảy trăm chín mươi lăm phẩy bảy bảy."),
        M(r"S(100)=\frac{2500\sqrt3}{9}\approx481{,}13",
          "Uốn toàn bộ thành tam giác đều cho diện tích khoảng bốn trăm tám mươi mốt phẩy một ba."),
        T("Cho phép biên: lớn nhất khi toàn bộ dây uốn tròn.",
          "Trên đoạn đóng, hàm lồi đạt lớn nhất ở một đầu mút. So sánh cho thấy toàn bộ dây uốn tròn có diện tích lớn hơn."),
        T("Nếu hai phần phải dương: không có giá trị lớn nhất.",
          "Nếu bắt buộc cắt thành hai phần dương, thì không có giá trị lớn nhất, chỉ có cận trên bằng diện tích hình tròn dùng toàn bộ dây."),
    ),
    P(
        "Kết quả toàn câu",
        T("d) Chia đôi dây để được lớn nhất: SAI.",
          "Dù hiểu theo mô hình cho phép biên hay bắt buộc hai phần dương, chia đôi dây không cho tổng diện tích lớn nhất. Ý d sai."),
        T("Kết quả: S — Đ — Đ — S.",
          "Kết quả toàn câu là sai, đúng, đúng, sai."),
    ),
)

Q(
    "DS04", "PHẦN II — CÂU 4",
    "Độ cao đèn chiếu sáng tối ưu", "light",
    P(
        "Mô hình và ý a",
        M(r"I=kf(h),\qquad f(h)=\frac{h}{(h^2+d^2)^{3/2}},\qquad h,d,k>0",
          "Cường độ sáng bằng k nhân h trên h bình phương cộng d bình phương mũ ba phần hai. Vì k dương và cố định, ta tối ưu hàm f."),
        M(r"\lim_{h\to0^+}f(h)=0",
          "Khi h tiến về không từ bên phải, tử số tiến về không và mẫu số tiến về d lập phương dương, nên giới hạn bằng không."),
        M(r"f(h)=\frac{1}{h^2(1+d^2/h^2)^{3/2}}\xrightarrow[h\to+\infty]{}0",
          "Khi h tiến ra vô cùng, đưa h lập phương ra khỏi mẫu, ta được biểu thức có giới hạn bằng không."),
        T("a) ĐÚNG.",
          "Ý a đúng."),
    ),
    P(
        "Ý b — đạo hàm",
        M(r"f(h)=h(h^2+d^2)^{-3/2}",
          "Viết hàm dưới dạng tích."),
        M(r"f'(h)=(h^2+d^2)^{-3/2}-3h^2(h^2+d^2)^{-5/2}",
          "Dùng quy tắc đạo hàm tích và hàm hợp, ta có hai hạng tử như trên."),
        M(r"\boxed{f'(h)=\frac{d^2-2h^2}{(h^2+d^2)^{5/2}}}",
          "Quy đồng và rút gọn được d bình phương trừ hai h bình phương trên h bình phương cộng d bình phương mũ năm phần hai."),
        T("b) ĐÚNG.",
          "Ý b đúng."),
    ),
    P(
        "Ý c — độ cao tối ưu",
        M(r"f'(h)=0\iff d^2=2h^2\iff h=\frac{d}{\sqrt2}",
          "Đạo hàm bằng không khi d bình phương bằng hai h bình phương. Vì h dương, nghiệm là d trên căn hai."),
        T("Đạo hàm dương trước d/√2, âm sau d/√2.",
          "Mẫu số luôn dương, tử số dương trước nghiệm và âm sau nghiệm. Vì vậy đây là điểm đạt cường độ lớn nhất."),
        T("c) ĐÚNG.",
          "Ý c đúng."),
    ),
    P(
        "Ý d — góc nghiêng",
        M(r"\tan\alpha=\frac{h}{d}=\frac1{\sqrt2}",
          "Tại độ cao tối ưu, tang góc nghiêng bằng h trên d, tức một trên căn hai."),
        M(r"\alpha=\arctan\left(\frac1{\sqrt2}\right)\approx35{,}26^\circ",
          "Suy ra góc nghiêng xấp xỉ ba mươi lăm phẩy hai sáu độ."),
        T("d) Góc tối ưu khoảng 45°: SAI.",
          "Ý d sai vì góc tối ưu không phải bốn mươi lăm độ."),
        T("Kết quả: Đ — Đ — Đ — S.",
          "Kết quả toàn câu là đúng, đúng, đúng, sai."),
    ),
)

# ----------------------- PHẦN III: TRẢ LỜI NGẮN -----------------------

Q(
    "TLN01", "PHẦN III — CÂU 1",
    "Khung biển quảng cáo: hai đơn giá", "billboard",
    P(
        "Lập hàm chi phí",
        T("Biển 54 m²; nẹp ngang 150.000 đ/m, nẹp bên 100.000 đ/m.",
          "Biển quảng cáo hình chữ nhật có diện tích năm mươi bốn mét vuông. Nẹp trên dưới giá một trăm năm mươi nghìn đồng mỗi mét, nẹp bên một trăm nghìn đồng mỗi mét."),
        M(r"xy=54,\qquad y=\frac{54}{x},\qquad x>0",
          "Gọi x là cạnh trên dưới, y là cạnh bên. Tích x y bằng năm mươi bốn."),
        M(r"C=2x\cdot0{,}15+2y\cdot0{,}10",
          "Tính theo triệu đồng, tổng chi phí bằng hai x nhân không phẩy một lăm, cộng hai y nhân không phẩy một."),
        M(r"C(x)=0{,}3x+\frac{10{,}8}{x}",
          "Thay y được không phẩy ba x cộng mười phẩy tám trên x."),
    ),
    P(
        "Tối thiểu chi phí",
        M(r"C(x)\ge2\sqrt{0{,}3x\cdot\frac{10{,}8}{x}}=2\sqrt{3{,}24}=3{,}6",
          "Theo bất đẳng thức trung bình cộng và trung bình nhân, chi phí không nhỏ hơn hai căn ba phẩy hai bốn, bằng ba phẩy sáu triệu đồng."),
        M(r"0{,}3x=\frac{10{,}8}{x}\iff x=6,\qquad y=9",
          "Dấu bằng khi không phẩy ba x bằng mười phẩy tám trên x, suy ra x bằng sáu và y bằng chín mét."),
        T("Chi phí nhỏ nhất: 3,6 triệu đồng.",
          "Vậy chi phí nhỏ nhất bằng ba phẩy sáu triệu đồng."),
        M(r"\boxed{3{,}6}",
          "Điền đáp án ba phẩy sáu."),
    ),
)

Q(
    "TLN02", "PHẦN III — CÂU 2",
    "Rào đất và chia thành ba lô", "three_lots",
    P(
        "Đếm đủ các đoạn hàng rào",
        T("Có 120 m lưới, gồm rào ngoài và hai vách ngăn.",
          "Dùng một trăm hai mươi mét lưới để rào kín mảnh đất hình chữ nhật và làm thêm hai vách ngăn song song chiều rộng, chia thành ba lô bằng nhau."),
        M(r"2x+4y=120",
          "Gọi x là chiều dài, y là chiều rộng. Có hai đoạn dài x và bốn đoạn dài y. Vì vậy hai x cộng bốn y bằng một trăm hai mươi."),
        M(r"x=60-2y,\qquad0<y<30",
          "Suy ra x bằng sáu mươi trừ hai y, với y nằm giữa không và ba mươi."),
        M(r"S(y)=y(60-2y)",
          "Diện tích toàn mảnh đất bằng y nhân sáu mươi trừ hai y."),
    ),
    P(
        "Tối đa diện tích",
        M(r"S(y)=-2(y-15)^2+450\le450",
          "Hoàn thành bình phương, diện tích bằng âm hai nhân y trừ mười lăm bình phương, cộng bốn trăm năm mươi."),
        M(r"y=15,\qquad x=30",
          "Dấu bằng khi chiều rộng mười lăm mét và chiều dài ba mươi mét."),
        M(r"2\cdot30+4\cdot15=120",
          "Kiểm tra chiều dài lưới sử dụng đúng bằng một trăm hai mươi mét."),
        M(r"\boxed{450\ \mathrm{m}^2}",
          "Diện tích lớn nhất là bốn trăm năm mươi mét vuông. Điền bốn trăm năm mươi."),
    ),
)

Q(
    "TLN03", "PHẦN III — CÂU 3",
    "Mặt bàn chữ nhật trong tấm kính tròn", "circle_rect",
    P(
        "Đường chéo cố định",
        T("Tấm kính tròn bán kính 50 cm; cắt chữ nhật lớn nhất.",
          "Tấm kính tròn bán kính năm mươi xăng ti mét. Cắt một hình chữ nhật nội tiếp có diện tích lớn nhất, trả lời theo nghìn xăng ti mét vuông."),
        M(r"d=2R=100\ \mathrm{cm}",
          "Đường chéo hình chữ nhật bằng đường kính hình tròn, tức một trăm xăng ti mét."),
        M(r"a^2+b^2=d^2=10000",
          "Theo định lý Pi ta go, tổng bình phương hai cạnh bằng mười nghìn."),
        M(r"S=ab\le\frac{a^2+b^2}{2}=5000",
          "Hai lần tích không vượt quá tổng bình phương, nên diện tích không vượt quá năm nghìn xăng ti mét vuông."),
    ),
    P(
        "Dấu bằng và đơn vị đáp án",
        M(r"a=b=50\sqrt2\ \mathrm{cm}",
          "Dấu bằng khi hình chữ nhật là hình vuông, mỗi cạnh bằng năm mươi căn hai xăng ti mét."),
        M(r"S_{\max}=5000\ \mathrm{cm}^2=5\cdot1000\ \mathrm{cm}^2",
          "Năm nghìn xăng ti mét vuông bằng năm đơn vị nghìn xăng ti mét vuông."),
        M(r"\boxed{5}",
          "Vậy điền đáp án năm."),
    ),
)

Q(
    "TLN04", "PHẦN III — CÂU 4",
    "Tam giác vuông có cạnh huyền 10 cm", "right_triangle",
    P(
        "Ràng buộc Pi-ta-go",
        T("Tìm diện tích lớn nhất khi cạnh huyền bằng 10 cm.",
          "Cho tam giác vuông có cạnh huyền mười xăng ti mét. Tìm diện tích lớn nhất."),
        M(r"x^2+y^2=100,\qquad x,y>0",
          "Gọi hai cạnh góc vuông là x, y. Tổng bình phương hai cạnh bằng một trăm."),
        M(r"S=\frac12xy\le\frac{x^2+y^2}{4}=25",
          "Diện tích bằng một phần hai x y, không vượt quá tổng bình phương hai cạnh trên bốn, tức hai mươi lăm."),
    ),
    P(
        "Cấu hình đạt tối ưu",
        M(r"x=y=5\sqrt2\ \mathrm{cm}",
          "Dấu bằng khi hai cạnh góc vuông bằng nhau, mỗi cạnh bằng năm căn hai xăng ti mét."),
        T("Tam giác tối ưu là tam giác vuông cân.",
          "Vậy tam giác vuông cân cho diện tích lớn nhất."),
        M(r"\boxed{25\ \mathrm{cm}^2}",
          "Điền đáp án hai mươi lăm."),
    ),
)

Q(
    "TLN05", "PHẦN III — CÂU 5",
    "Dây 34 m: hình vuông và chữ nhật", "square_rectangle",
    P(
        "Lập ràng buộc",
        T("Vuông cạnh x; chữ nhật có chiều rộng y, chiều dài 2y.",
          "Dây dài ba mươi bốn mét được chia để uốn hình vuông cạnh x và hình chữ nhật có chiều dài gấp đôi chiều rộng."),
        M(r"4x+6y=34,\qquad0<x<\frac{17}{2}",
          "Chu vi vuông bằng bốn x. Chu vi chữ nhật bằng sáu y. Tổng bằng ba mươi bốn."),
        M(r"y=\frac{17-2x}{3}",
          "Suy ra y bằng mười bảy trừ hai x, chia ba."),
        M(r"S(x)=x^2+2y^2=x^2+\frac29(17-2x)^2",
          "Tổng diện tích bằng x bình phương cộng hai y bình phương. Thay y để có hàm một biến."),
    ),
    P(
        "Tối ưu tổng diện tích",
        M(r"S(x)=\frac{17}{9}x^2-\frac{136}{9}x+\frac{578}{9}",
          "Khai triển được mười bảy trên chín x bình phương, trừ một trăm ba mươi sáu trên chín x, cộng năm trăm bảy mươi tám trên chín."),
        M(r"S(x)=\frac{17}{9}(x-4)^2+34\ge34",
          "Hoàn thành bình phương được mười bảy trên chín nhân x trừ bốn bình phương, cộng ba mươi bốn."),
        M(r"x=4,\qquad y=3,\qquad2y=6",
          "Dấu bằng khi x bằng bốn mét. Khi đó chữ nhật có hai kích thước ba mét và sáu mét."),
        M(r"\boxed{x=4\ \mathrm{m}}",
          "Đề hỏi cạnh hình vuông, nên điền bốn."),
    ),
)

Q(
    "TLN06", "PHẦN III — CÂU 6",
    "Chu vi nhỏ nhất của khu đất", "fixed_area",
    P(
        "Chuyển chi phí về chu vi",
        T("Khu đất chữ nhật 8100 m²; rào toàn bộ xung quanh.",
          "Khu đất hình chữ nhật có diện tích tám nghìn một trăm mét vuông. Tìm chu vi để chi phí rào toàn bộ nhỏ nhất."),
        M(r"xy=8100,\qquad x,y>0,\qquad P=2(x+y)",
          "Gọi hai cạnh là x và y, tích bằng tám nghìn một trăm. Chu vi bằng hai nhân x cộng y."),
        T("Giả sử đơn giá xây tường trên mỗi mét là không đổi.",
          "Với đơn giá xây tường trên mỗi mét không đổi, tối thiểu chi phí tương đương tối thiểu chu vi."),
    ),
    P(
        "Bất đẳng thức và kết luận",
        M(r"x+y\ge2\sqrt{xy}=2\sqrt{8100}=180",
          "Theo bất đẳng thức trung bình cộng và trung bình nhân, x cộng y không nhỏ hơn hai căn tám nghìn một trăm, bằng một trăm tám mươi."),
        M(r"P=2(x+y)\ge360",
          "Vậy chu vi không nhỏ hơn ba trăm sáu mươi mét."),
        M(r"x=y=90\ \mathrm{m}",
          "Dấu bằng khi khu đất là hình vuông cạnh chín mươi mét."),
        M(r"\boxed{P_{\min}=360\ \mathrm{m}}",
          "Điền đáp án ba trăm sáu mươi."),
    ),
)

# ------------------------- MỞ ĐẦU VÀ TỔNG KẾT -------------------------

INTRO = {
    "id": "INTRO",
    "section": "TOÁN 12 — CHUYÊN ĐỀ TỐI ƯU",
    "title": "Tối ưu hóa hình học và uốn dây",
    "diagram": "method",
    "intro": {
        "voice": "Chào các em. Chúng ta cùng học chuyên đề tối ưu hóa hình học và uốn dây tạo hình, với bài giảng của Thầy Nguyễn Văn Sang."
    },
    "pages": [
        P(
            "Lộ trình giải bài",
            T("12 câu trắc nghiệm • 4 câu đúng–sai • 6 câu trả lời ngắn",
              "Bài giảng giải đầy đủ mười hai câu trắc nghiệm, bốn câu đúng sai và sáu câu trả lời ngắn."),
            T("Bước 1. Chọn biến và xác định miền điều kiện.",
              "Trước hết chọn biến, đơn vị và miền điều kiện."),
            T("Bước 2. Lập ràng buộc và hàm mục tiêu.",
              "Tiếp theo lập ràng buộc rồi đưa diện tích, chi phí hoặc chu vi về hàm một biến."),
            T("Bước 3. Tối ưu, kiểm tra dấu bằng, trả lời đúng đơn vị.",
              "Cuối cùng dùng đạo hàm hoặc bất đẳng thức, kiểm tra cấu hình đạt dấu bằng và trả lời đúng đơn vị."),
        ),
        P(
            "Những điểm cần lưu ý trong đề",
            T("TN2: nhãn hình được đặt theo phần lời đề.",
              "Ở trắc nghiệm hai, nhãn hình chữ nhật được đặt lại cho đúng với lời đề."),
            T("TN12: kiểm tra hướng tường 12 m và 20 m.",
              "Ở trắc nghiệm mười hai, cần kiểm tra hướng hai bức tường để biết cấu hình tối ưu có nằm trong phòng hay không."),
            T("ĐS1, ĐS3: phân biệt hình thực với trường hợp suy biến.",
              "Ở đúng sai một và ba, cần phân biệt yêu cầu các kích thước dương với mô hình cho phép một phần co về không."),
            T("Công thức LaTeX • Giọng nam tổng hợp tiếng Việt",
              "Công thức được trình bày bằng LaTeX. Lời đọc sử dụng giọng nam tổng hợp tiếng Việt."),
        ),
    ],
}

OUTRO = {
    "id": "OUTRO",
    "section": "TỔNG KẾT",
    "title": "Hiểu mô hình — nhớ điều kiện dấu bằng",
    "diagram": "method",
    "intro": {
        "voice": "Chúng ta đã hoàn thành hai mươi hai bài. Sau đây là các công cụ và đáp án để các em đối chiếu."
    },
    "pages": [
        P(
            "Ba công cụ quan trọng",
            M(r"u+v\ge2\sqrt{uv}\qquad(u,v>0)",
              "Công cụ thứ nhất: tổng hai số dương không nhỏ hơn hai lần căn tích. Dấu bằng khi hai số bằng nhau."),
            M(r"2uv\le u^2+v^2",
              "Công cụ thứ hai: hai lần tích không vượt quá tổng bình phương."),
            M(r"f'(x_*)=0\quad+\quad\text{check the sign}",
              "Công cụ thứ ba: tìm nghiệm đạo hàm rồi kiểm tra dấu. Không kết luận cực trị chỉ từ phương trình đạo hàm bằng không."),
            T("Luôn kiểm tra miền xác định, kích thước thực và đơn vị.",
              "Luôn kiểm tra miền xác định, kích thước thực, khả năng đạt dấu bằng và đơn vị được hỏi."),
        ),
        P(
            "Đáp án đối chiếu",
            T("TN1–TN11: A. TN12: tùy hướng hai tường.",
              "Mười một câu trắc nghiệm đầu đều chọn A theo thứ tự đáp án đã cho. Câu mười hai phụ thuộc cách gán hai bức tường."),
            T("ĐS1: Đ–S–Đ*–Đ. ĐS2: Đ–Đ–S–Đ.",
              "Đúng sai một: đúng, sai, đúng có điều kiện, đúng. Đúng sai hai: đúng, đúng, sai, đúng."),
            T("ĐS3: S–Đ–Đ–S. ĐS4: Đ–Đ–Đ–S.",
              "Đúng sai ba: sai, đúng, đúng, sai. Đúng sai bốn: đúng, đúng, đúng, sai."),
            M(r"\mathrm{TLN}:\quad3{,}6;\ 450;\ 5;\ 25;\ 4;\ 360",
              "Trả lời ngắn lần lượt là ba phẩy sáu; bốn trăm năm mươi; năm; hai mươi lăm; bốn; ba trăm sáu mươi."),
        ),
        P(
            "Kết thúc bài giảng",
            T("Thầy Nguyễn Văn Sang",
              "Cảm ơn các em đã theo dõi bài giảng của Thầy Nguyễn Văn Sang."),
            T("Chúc các em học tốt!",
              "Chúc các em học tốt và vận dụng linh hoạt các phương pháp tối ưu hóa."),
        ),
    ],
}

valid_codes = {item["id"] for item in LESSONS}

if set(CHON_BAI) - valid_codes:
    raise ValueError(
        "Mã bài không hợp lệ: " + str(sorted(set(CHON_BAI) - valid_codes))
    )

selected = [
    item for item in LESSONS
    if not CHON_BAI or item["id"] in CHON_BAI
]

if not CHON_BAI:
    selected = [INTRO] + selected + [OUTRO]

for i, item in enumerate(selected, 1):
    item["order"] = i
    item["total"] = len(selected)

# ======================== 4. TẠO GIỌNG ĐỌC ============================

print("\nBƯỚC 2/5 — Tạo lời đọc giọng nam tiếng Việt.")

import edge_tts
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

audio_items = []

for lesson in selected:
    audio_items.append(lesson["intro"])
    for page in lesson["pages"]:
        audio_items.extend(page["rows"])

audio_counter = {"done": 0}


async def make_audio(item, semaphore):
    signature = GIONG_DOC + "|" + TOC_DO_DOC + "|" + item["voice"]
    digest = hashlib.sha256(signature.encode("utf-8")).hexdigest()[:28]
    destination = AUDIO_DIR / (digest + ".mp3")

    async with semaphore:
        if destination.exists():
            try:
                duration = probe_duration(destination)
                item["audio"] = str(destination)
                item["duration"] = duration
                audio_counter["done"] += 1
                return
            except Exception:
                destination.unlink(missing_ok=True)

        last_error = None

        for attempt in range(5):
            temporary = AUDIO_DIR / (digest + ".part.mp3")
            temporary.unlink(missing_ok=True)

            try:
                communicator = edge_tts.Communicate(
                    item["voice"],
                    voice=GIONG_DOC,
                    rate=TOC_DO_DOC,
                    volume="+0%",
                )

                await asyncio.wait_for(
                    communicator.save(str(temporary)),
                    timeout=150,
                )

                duration = probe_duration(temporary)
                temporary.replace(destination)

                item["audio"] = str(destination)
                item["duration"] = duration

                audio_counter["done"] += 1

                if audio_counter["done"] % 20 == 0:
                    print(
                        "  Đã chuẩn bị",
                        audio_counter["done"],
                        "/",
                        len(audio_items),
                        "đoạn lời đọc.",
                    )
                return

            except Exception as error:
                last_error = error
                temporary.unlink(missing_ok=True)
                await asyncio.sleep(3 + attempt * 4)

        raise RuntimeError(
            "Dịch vụ giọng đọc chưa trả về âm thanh sau nhiều lần thử.\n"
            "Hãy chạy lại ô; các đoạn đã tạo sẽ được dùng lại.\n"
            "Lời đọc: " + item["voice"][:160] + "\n"
            "Chi tiết: " + str(last_error)
        )


async def make_all_audio():
    semaphore = asyncio.Semaphore(2)
    await asyncio.gather(
        *(make_audio(item, semaphore) for item in audio_items)
    )


asyncio.run(make_all_audio())

print("  Đã chuẩn bị đủ", len(audio_items), "đoạn lời đọc.")

# ========================== 5. MÃ MANIM ===============================
# Toàn bộ Scene được ghi ra tệp .py riêng và dựng bằng tiến trình riêng.
# Điều này tránh lỗi thư viện đồ họa đã được nạp trong kernel Colab.
# =====================================================================

SCENE_SOURCE = r'''
from manim import *
import numpy as np
import math
import json
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "lessons.json").read_text(encoding="utf-8"))
SETTINGS = json.loads((HERE / "settings.json").read_text(encoding="utf-8"))

BG = "#0B1222"
PANEL = "#142038"
INK = "#EDF4FF"
MUTED = "#9EB2D3"
BLUE = "#65ADFF"
CYAN = "#54DEEC"
GOLD = "#FFD166"
GREEN = "#69E0A5"
RED = "#FF8290"
FONT = "DejaVu Sans"

config.background_color = BG

TEMPLATE = TexTemplate()
TEMPLATE.documentclass = r"\documentclass[preview]{standalone}"
TEMPLATE.preamble = (
    r"\usepackage{amsmath}"
    r"\usepackage{amssymb}"
    r"\usepackage{xcolor}"
)


def text_mob(s, size=26, color=INK, bold=False):
    return Text(
        s,
        font=FONT,
        font_size=size,
        color=color,
        weight="BOLD" if bold else "NORMAL",
        disable_ligatures=True,
        line_spacing=0.8,
    )


def math_mob(s, size=30, color=INK):
    return MathTex(
        s,
        font_size=size,
        color=color,
        tex_template=TEMPLATE,
    )


def fit(mob, width=None, height=None):
    factors = [1.0]
    if width is not None and mob.width > 0:
        factors.append(width / mob.width)
    if height is not None and mob.height > 0:
        factors.append(height / mob.height)
    mob.scale(min(factors))
    return mob


def point(x, y):
    return np.array([float(x), float(y), 0.0])


def label(s, x, y, size=23, color=INK):
    return math_mob(s, size, color).move_to(point(x, y))


def line(a, b, color=BLUE, width=3, dashed=False):
    cls = DashedLine if dashed else Line
    return cls(
        point(*a),
        point(*b),
        color=color,
        stroke_width=width,
    )


def polygon(points, color=BLUE, opacity=0.16):
    return Polygon(
        *[point(*p) for p in points],
        color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=opacity,
    )


def dot_label(x, y, name, direction=UP, color=GOLD):
    d = Dot(point(x, y), radius=0.055, color=color)
    name_mob = math_mob(name, 22, color).next_to(
        d, direction, buff=0.12
    )
    return VGroup(d, name_mob)


def plot_polyline(points, color=BLUE):
    obj = VMobject(stroke_color=color, stroke_width=3)
    obj.set_points_as_corners([point(x, y) for x, y in points])
    return obj


def make_diagram(kind, t=0):
    g = VGroup()

    if kind == "method":
        names = [
            ("CHỌN BIẾN", "Điều kiện và đơn vị", BLUE),
            ("LẬP HÀM", "Ràng buộc hình học", CYAN),
            ("TỐI ƯU", "Kiểm tra dấu bằng", GOLD),
        ]
        for i, (heading, sub, color) in enumerate(names):
            y = 1.5 - 1.5*i
            box = RoundedRectangle(
                width=3.6,
                height=1.0,
                corner_radius=0.12,
                stroke_color=color,
                fill_color=PANEL,
                fill_opacity=1,
            ).move_to(point(0, y))
            h = text_mob(heading, 24, color, True).move_to(point(0, y+0.2))
            s = text_mob(sub, 17, MUTED).move_to(point(0, y-0.22))
            g.add(box, h, s)
            if i < 2:
                g.add(
                    Arrow(
                        point(0, y-0.57),
                        point(0, y-0.93),
                        buff=0,
                        stroke_width=2,
                        color=MUTED,
                        max_tip_length_to_length_ratio=0.25,
                    )
                )

    elif kind == "river":
        h = 0.8 + 0.7*t
        w = 6 - 2*h
        g.add(
            Rectangle(
                width=6.4,
                height=0.55,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_width=0,
            ).move_to(point(0, 1.8)),
            text_mob("BỜ SÔNG", 22, BLUE, True).move_to(point(0, 1.8)),
            polygon(
                [(-w/2,1.5),(-w/2,1.5-h),(w/2,1.5-h),(w/2,1.5)],
                GREEN,
            ),
            line((-w/2,1.5),(w/2,1.5),BLUE,2,True),
            label("x",-w/2-0.28,1.5-h/2),
            label("x",w/2+0.28,1.5-h/2),
            label("80-2x",0,1.16-h),
        )

    elif kind in ("triangle_rect", "greenhouse"):
        h = 0.7 + 0.8*t
        a = 3-h
        g.add(
            polygon([(-3,0),(3,0),(0,3)],BLUE,0.04),
            line((0,0),(0,3),MUTED,1.5,True),
            polygon([(-a,0),(a,0),(a,h),(-a,h)],GREEN,0.22),
            label("A",0,3.3),
            label("B",-3.2,-0.15),
            label("C",3.2,-0.15),
            label("x",a+0.3,h/2),
        )
        if kind == "triangle_rect":
            g.add(
                label("M",-a,-0.3),
                label("N",a,-0.3),
                label("P",a+0.12,h+0.28),
                label("Q",-a-0.12,h+0.28),
                label("BC=12",0,-0.78),
                label("AH=6",0.72,2.5,20,MUTED),
            )
        else:
            g.add(
                label("Q",-a,-0.3),
                label("P",a,-0.3),
                label("N",a+0.12,h+0.28),
                label("M",-a-0.12,h+0.28),
                label("BC=60",0,-0.78),
                label("AH=40",0.8,2.5,20,MUTED),
            )

    elif kind == "square_circle":
        wire = 7+(80/(4+math.pi)-7)*t
        a = wire/4
        r = (20-wire)/(2*math.pi)
        sq = Square(
            side_length=a,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.16,
        ).move_to(point(-2.8,0))
        ci = Circle(
            radius=r,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.16,
        ).move_to(point(2.8,0))
        g.add(
            sq,ci,
            label("a=x/4",-2.8,-a/2-0.5),
            label(r"r=\frac{20-x}{2\pi}",2.8,-r-0.6),
        )

    elif kind == "triangle_square":
        xstar = 324/(9+4*math.sqrt(3))
        x = 11+(xstar-11)*t
        a = x/3
        b = (36-x)/4
        tri = polygon(
            [(-a/2,0),(a/2,0),(0,a*math.sqrt(3)/2)],
            GREEN,
        ).move_to(point(-4,0))
        sq = Square(
            side_length=b,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.16,
        ).move_to(point(4,0))
        g.add(
            tri,sq,
            label("a=x/3",-4,-tri.height/2-0.7),
            label("b=(36-x)/4",4,-b/2-0.7),
        )

    elif kind == "triangle_circle":
        xstar = 900/(9+math.pi*math.sqrt(3))
        x = 65+(xstar-65)*t
        a = (x/3)*0.16
        r = ((100-x)/(2*math.pi))*0.16
        tri = polygon(
            [(-a/2,0),(a/2,0),(0,a*math.sqrt(3)/2)],
            GREEN,
        ).move_to(point(-2.5,0))
        ci = Circle(
            radius=r,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.16,
        ).move_to(point(2.5,0))
        g.add(
            tri,ci,
            label("a=x/3",-2.5,-tri.height/2-0.45),
            label(r"r=\frac{100-x}{2\pi}",2.5,-r-0.5),
        )

    elif kind == "square_rectangle":
        x = 2.6+(4-2.6)*t
        y = (17-2*x)/3
        sq = Square(
            side_length=x,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.16,
        ).move_to(point(-4,0))
        re = Rectangle(
            width=2*y,
            height=y,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.16,
        ).move_to(point(4,0))
        g.add(
            sq,re,
            label("x",-4,-x/2-0.5),
            label("2y",4,-y/2-0.5),
            label("y",4+y+0.4,0),
        )

    elif kind == "window":
        r = 0.85+0.45*t
        perimeter = (math.pi+4)*1.3
        h = (perimeter-(math.pi+2)*r)/2
        roof = [
            (r*math.cos(u),h+r*math.sin(u))
            for u in np.linspace(0,math.pi,64)
        ]
        boundary = [(-r,0),(r,0)] + roof
        g.add(
            polygon(boundary,BLUE,0.18),
            line((-r,h),(r,h),MUTED,1.5,True),
            line((0,h),(r,h),GOLD,2),
            label("R",r/2,h+0.25,22,GOLD),
            label("h",-r-0.35,h/2),
            label("2R",0,-0.35),
        )

    elif kind == "semicircle_trap":
        angle = 0.4+(math.pi/3-0.4)*t
        r = 2.4
        x = r*math.cos(angle)
        y = r*math.sin(angle)
        g.add(
            Arc(radius=r,start_angle=0,angle=PI,color=BLUE),
            line((-r,0),(r,0),BLUE),
            polygon([(-r,0),(r,0),(x,y),(-x,y)],GREEN,0.2),
            line((0,0),(x,y),GOLD,2),
            line((0,0),(-x,y),GOLD,2),
            Arc(radius=0.55,start_angle=0,angle=angle,color=GOLD),
            label(r"\alpha",0.8,0.22,23,GOLD),
            label("A",-r-0.2,-0.2),
            label("B",r+0.2,-0.2),
            label("C",x+0.15,y+0.25),
            label("D",-x-0.15,y+0.25),
            label("O",0,-0.25),
        )

    elif kind == "viewing":
        x = 4+(math.sqrt(5.25)-4)*t
        g.add(
            line((0,-1.5),(0,4),MUTED,3),
            line((-4.8,-1.5),(0.5,-1.5),MUTED,2),
            line((0,1.5),(0,3.5),RED,9),
            line((-x,0),(0,1.5),BLUE,2),
            line((-x,0),(0,3.5),CYAN,2),
            line((-x,0),(0,0),MUTED,1.5,True),
            Dot(point(-x,0),radius=0.06,color=GOLD),
            text_mob("Mắt",22,GOLD).move_to(point(-x-0.2,-0.4)),
            label("x",-x/2,-0.32),
            label("1.5",0.43,0.75),
            label("2",0.43,2.5,25,RED),
            label(r"\theta",-x+0.7,0.5,24,GOLD),
        )

    elif kind == "ellipse":
        angle = 0.3+(math.pi/4-0.3)*t
        a,b = 3,2.25
        x,y = a*math.cos(angle),b*math.sin(angle)
        g.add(
            Ellipse(width=2*a,height=2*b,color=BLUE),
            line((-3.4,0),(3.4,0),MUTED,1.4),
            line((0,-2.6),(0,2.6),MUTED,1.4),
            polygon([(-x,-y),(x,-y),(x,y),(-x,y)],GREEN,0.18),
            dot_label(x,y,"M(x,y)",UR),
            label("O",-0.22,-0.25),
        )

    elif kind == "parabola":
        x = 0.7+(math.sqrt(3)-0.7)*t
        y = (9-x*x)*0.38
        points = [(u,(9-u*u)*0.38) for u in np.linspace(-3,3,100)]
        g.add(
            plot_polyline(points,BLUE),
            line((-3.5,0),(3.5,0),MUTED,1.4),
            line((0,-0.4),(0,3.8),MUTED,1.4),
            polygon([(-x,0),(x,0),(x,y),(-x,y)],GREEN,0.18),
            label("-x",-x,-0.3),
            label("x",x,-0.3),
            label("9-x^2",x+0.8,y/2),
            label("-3",-3,-0.3),
            label("3",3,-0.3),
        )

    elif kind == "book":
        x = 12+(16-12)*t
        y = 384/x
        s = 0.12
        outer = Rectangle(
            width=(x+4)*s,height=(y+6)*s,
            color=BLUE,fill_color=BLUE,fill_opacity=0.1,
        )
        inner = Rectangle(
            width=x*s,height=y*s,
            color=GREEN,fill_color=GREEN,fill_opacity=0.16,
        )
        g.add(
            outer,inner,
            label("384",0,0,30,GREEN),
            label("x+4",0,-outer.height/2-0.4),
            label("y+6",outer.width/2+0.5,0),
            label("3",0,outer.height/2-0.18,19),
            label("2",-outer.width/2+0.12,0,19),
        )

    elif kind == "gutter":
        angle = 0.35+(math.pi/3-0.35)*t
        c,s = math.cos(angle),math.sin(angle)
        points = [(-1-2*c,2*s),(-1,0),(1,0),(1+2*c,2*s)]
        g.add(
            polygon(points,BLUE,0.2),
            line(points[0],points[-1],CYAN,2,True),
            line((-1,0),(-3.3,0),MUTED,1.3,True),
            Arc(
                radius=0.65,
                start_angle=PI-angle,
                angle=angle,
                arc_center=point(-1,0),
                color=GOLD,
            ),
            label(r"\theta",-1.9,0.23,23,GOLD),
            label("10",0,-0.35),
            label("10",-1-c-0.3,s),
            label("10",1+c+0.3,s),
            label(r"10+20\cos\theta",0,2*s+0.45),
        )

    elif kind == "stage":
        a = 5+(2-5)*t
        b = 8*a/(a-1)
        s = 0.22
        g.add(
            polygon([(0,0),(12*s,0),(12*s,20*s),(0,20*s)],MUTED,0.03),
            polygon([(0,0),(a*s,0),(0,b*s)],BLUE,0.2),
            dot_label(s,8*s,"K(1,8)",RIGHT,GOLD),
            label("A",-0.2,-0.2),
            label("M",a*s,-0.25),
            label("N",-0.25,b*s),
            label("12",6*s,-0.55),
            label("20",12*s+0.35,10*s),
            line((s,8*s),(s,0),MUTED,1.3,True),
            line((s,8*s),(0,8*s),MUTED,1.3,True),
        )

    elif kind == "stadium":
        x = 2.2-1.3*t
        r = 0.95
        left = [
            (-x/2+r*math.cos(u),r*math.sin(u))
            for u in np.linspace(math.pi/2,3*math.pi/2,48)
        ]
        right = [
            (x/2+r*math.cos(u),r*math.sin(u))
            for u in np.linspace(-math.pi/2,math.pi/2,48)
        ]
        g.add(
            polygon(left+right,BLUE,0.2),
            line((-x/2,-r),(-x/2,r),MUTED,1.5,True),
            line((x/2,-r),(x/2,r),MUTED,1.5,True),
            label("x",0,-r-0.35),
            label("y",x/2+r+0.3,0),
            text_mob("HỒ BƠI",20,CYAN,True).move_to(ORIGIN),
        )

    elif kind == "light":
        d = 3.4
        h = 3.6+(d/math.sqrt(2)-3.6)*t
        angle = math.atan(h/d)
        g.add(
            line((0,0),(4.2,0),MUTED,2),
            line((0,0),(0,4),MUTED,2),
            line((0,h),(d,0),GOLD,3),
            dot_label(0,h,"S(0,h)",LEFT,GOLD),
            dot_label(d,0,"A(d,0)",DOWN,BLUE),
            label("h",-0.4,h/2),
            label("d",d/2,-0.3),
            Arc(
                radius=0.65,
                start_angle=PI-angle,
                angle=angle,
                arc_center=point(d,0),
                color=GOLD,
            ),
            label(r"\alpha",d-0.95,0.3,23,GOLD),
        )

    elif kind == "billboard":
        x = 4.5+(6-4.5)*t
        y = 54/x
        s = 0.32
        a,b = x*s/2,y*s/2
        g.add(
            polygon([(-a,-b),(a,-b),(a,b),(-a,b)],BLUE,0.1),
            line((-a,-b),(a,-b),GOLD,6),
            line((-a,b),(a,b),GOLD,6),
            label("x",0,-b-0.35),
            label("y",a+0.3,0),
            label("54",0,0,30),
            label("0.15",0,b+0.35,23,GOLD),
            label("0.10",-a-0.5,0,23,BLUE),
        )

    elif kind == "three_lots":
        y = 9+(15-9)*t
        x = 60-2*y
        s = 0.1
        left,right = -x*s/2,x*s/2
        bottom,top = -y*s/2,y*s/2
        g.add(
            polygon(
                [(left,bottom),(right,bottom),(right,top),(left,top)],
                GREEN,0.14,
            )
        )
        for k in (1,2):
            u = left+k*x*s/3
            g.add(line((u,bottom),(u,top),GOLD,3))
        for k in range(3):
            g.add(label(str(k+1),left+(k+0.5)*x*s/3,0,22,MUTED))
        g.add(label("x",0,bottom-0.35),label("y",right+0.3,0))

    elif kind == "circle_rect":
        angle = 0.25+(math.pi/4-0.25)*t
        r = 2.3
        x,y = r*math.cos(angle),r*math.sin(angle)
        g.add(
            Circle(radius=r,color=BLUE),
            polygon([(-x,-y),(x,-y),(x,y),(-x,y)],GREEN,0.17),
            line((-x,-y),(x,y),GOLD,2,True),
            label("100",0.2,0.3,24,GOLD),
            label("a",0,-y-0.3),
            label("b",x+0.3,0),
        )

    elif kind == "right_triangle":
        angle = 0.35+(math.pi/4-0.35)*t
        x,y = 4*math.cos(angle),4*math.sin(angle)
        g.add(
            polygon([(0,0),(x,0),(0,y)],BLUE,0.18),
            line((0.23,0),(0.23,0.23),MUTED,2),
            line((0,0.23),(0.23,0.23),MUTED,2),
            label("x",x/2,-0.3),
            label("y",-0.3,y/2),
            label("10",x/2+0.25,y/2+0.25,25,GOLD),
        )

    elif kind == "fixed_area":
        x = 5-2*t
        y = 9/x
        g.add(
            Rectangle(
                width=x,height=y,color=GREEN,
                fill_color=GREEN,fill_opacity=0.16,
            ),
            label("x",0,-y/2-0.35),
            label("y",x/2+0.3,0),
            label("8100",0,0,30,GOLD),
        )

    else:
        g.add(text_mob("Mô hình hình học",28,BLUE,True))

    g.move_to(ORIGIN)
    fit(g,width=3.65,height=3.55)
    return g


class LectureBase(Scene):
    lesson = None

    def speak(self, item, animation=None):
        start = float(self.time)
        duration = float(item["duration"])

        self.add_sound(item["audio"])
        self.events.append({
            "start": start,
            "end": start+duration,
            "text": item["voice"],
        })

        reveal = 0.0
        if animation is not None:
            reveal = min(0.55,max(0.2,duration*0.2))
            self.play(animation,run_time=reveal)

        self.wait(max(0.05,duration-reveal)+0.3)

    def row_mobject(self,row):
        if row["kind"] == "math":
            mob = math_mob(row["text"],30)
            if r"\boxed" in row["text"]:
                mob.set_color(GOLD)
        else:
            wrapped = textwrap.fill(
                row["text"],
                width=53,
                break_long_words=False,
                break_on_hyphens=False,
            )
            color = INK
            if "SAI" in row["text"] and "ĐÚNG" not in row["text"]:
                color = RED
            elif "ĐÚNG" in row["text"] and "SAI" not in row["text"]:
                color = GREEN
            mob = text_mob(wrapped,25,color)
        fit(mob,width=7.65,height=1.12)
        return mob

    def construct(self):
        q = self.lesson
        self.events = []

        top = Rectangle(
            width=14.23,height=0.08,
            stroke_width=0,
            fill_color=BLUE,fill_opacity=1,
        ).move_to(UP*3.96)

        section = text_mob(q["section"],18,CYAN,True)
        fit(section,width=11.5)
        section.move_to(point(-6.57,3.54),aligned_edge=LEFT)

        title = text_mob(q["title"],32,INK,True)
        fit(title,width=12.85,height=0.52)
        title.move_to(point(-6.57,3.0),aligned_edge=LEFT)

        index = text_mob(
            f"{q['order']:02d}/{q['total']:02d}",18,MUTED
        ).move_to(point(6.23,3.54))

        left_panel = RoundedRectangle(
            width=4.12,height=5.64,
            corner_radius=0.15,
            stroke_color="#2A3D5C",
            stroke_width=1,
            fill_color=PANEL,fill_opacity=1,
        ).move_to(point(-4.76,-0.33))

        right_panel = RoundedRectangle(
            width=8.6,height=5.64,
            corner_radius=0.15,
            stroke_color="#2A3D5C",
            stroke_width=1,
            fill_color=PANEL,fill_opacity=1,
        ).move_to(point(1.91,-0.33))

        left_heading = text_mob(
            "MÔ HÌNH HÌNH HỌC",20,BLUE,True
        ).move_to(point(-4.76,2.02))

        note = text_mob("Minh họa • Không theo tỉ lệ",15,MUTED)
        fit(note,width=3.65)
        note.move_to(point(-4.76,-2.47))

        flow = text_mob("Mô hình → Hàm số → Tối ưu",15,CYAN)
        fit(flow,width=3.65)
        flow.move_to(point(-4.76,-2.82))

        footer_line = line((-6.65,-3.38),(6.65,-3.38),"#304665",1)
        footer = text_mob(SETTINGS["teacher"],22,GOLD,True)
        footer.move_to(point(0,-3.69))

        self.add(
            top,section,title,index,left_panel,right_panel,
            left_heading,note,flow,footer_line,footer,
        )

        geometry = make_diagram(q["diagram"],0)
        geometry.move_to(point(-4.76,-0.2))

        self.speak(q["intro"],FadeIn(geometry,shift=UP*0.08))

        current = None
        pages = q["pages"]

        for page_index,page in enumerate(pages):
            if current is not None:
                self.play(FadeOut(current),run_time=0.25)
                self.remove(*current)

            heading = text_mob(page["title"],24,CYAN,True)
            fit(heading,width=7.1,height=0.48)
            heading.move_to(point(-1.96,2.02),aligned_edge=LEFT)

            count = text_mob(
                f"{page_index+1}/{len(pages)}",15,MUTED
            ).move_to(point(5.72,2.02))

            divider = line((-1.96,1.64),(5.82,1.64),"#304665",1)

            current = VGroup(heading,count,divider)
            self.play(FadeIn(current),run_time=0.25)

            # Chuyển sang cấu hình cuối để minh họa lời giải.
            # Đây là hiệu ứng hình học, không phải mô phỏng mọi giá trị trung gian.
            if page_index == len(pages)-1 and q["diagram"] != "method":
                target = make_diagram(q["diagram"],1)
                target.move_to(point(-4.76,-0.2))
                self.play(Transform(geometry,target),run_time=1.25)

            rows = VGroup(
                *[self.row_mobject(row) for row in page["rows"]]
            )
            rows.arrange(DOWN,aligned_edge=LEFT,buff=0.27)
            fit(rows,width=7.65,height=3.95)
            rows.move_to(point(-1.94,1.27),aligned_edge=UL)

            for data,mob in zip(page["rows"],rows):
                self.speak(data,FadeIn(mob,shift=UP*0.04))
                current.add(mob)

            self.wait(0.4)

        self.wait(0.7)
        if self.mobjects:
            self.play(
                FadeOut(Group(*self.mobjects)),
                run_time=0.35,
            )
        self.clear()

        events_path = HERE/"events"/(q["id"]+".json")
        events_path.parent.mkdir(exist_ok=True)
        events_path.write_text(
            json.dumps(self.events,ensure_ascii=False,indent=2),
            encoding="utf-8",
        )


for lesson in DATA:
    class_name = "B_"+lesson["id"]
    globals()[class_name] = type(
        class_name,
        (LectureBase,),
        {
            "lesson": lesson,
            "__module__": __name__,
        },
    )
'''

settings = {
    "teacher": TEN_THAY,
    "voice": GIONG_DOC,
    "rate": TOC_DO_DOC,
    "width": CHIEU_RONG,
    "height": CHIEU_CAO,
    "fps": FPS,
}

signature_data = (
    SCENE_SOURCE
    + json.dumps(selected, ensure_ascii=False, sort_keys=True)
    + json.dumps(settings, ensure_ascii=False, sort_keys=True)
)

render_key = hashlib.sha256(
    signature_data.encode("utf-8")
).hexdigest()[:14]

WORK = ROOT / ("render_" + render_key)
WORK.mkdir(exist_ok=True)
(WORK / "events").mkdir(exist_ok=True)

CLIPS = WORK / "clips"
CLIPS.mkdir(exist_ok=True)

MEDIA = WORK / "media"
MEDIA.mkdir(exist_ok=True)

scene_file = WORK / "bai_giang.py"
scene_file.write_text(SCENE_SOURCE, encoding="utf-8")

(WORK / "lessons.json").write_text(
    json.dumps(selected, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
(WORK / "settings.json").write_text(
    json.dumps(settings, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# Kiểm tra cú pháp tệp Scene trước khi dựng.
compile(SCENE_SOURCE, str(scene_file), "exec")

# ========================= 6. DỰNG VIDEO ==============================

print("\nBƯỚC 3/5 — Dựng từng chương bằng Manim.")
print("Thư mục làm việc:", WORK)
print("Nếu chạy lại trong cùng phiên, chương đã xong sẽ được dùng lại.\n")

clip_paths = []
clip_durations = []

for index, lesson in enumerate(selected, 1):
    code = lesson["id"]
    class_name = "B_" + code

    output_clip = CLIPS / (class_name + ".mp4")
    event_file = WORK / "events" / (code + ".json")
    done_file = WORK / (code + ".done")

    reusable = False

    if output_clip.exists() and event_file.exists() and done_file.exists():
        try:
            duration = probe_duration(output_clip)
            reusable = True
        except Exception:
            reusable = False

    if reusable:
        print(
            f"[{index}/{len(selected)}] Dùng lại: "
            f"{code} — {lesson['title']}"
        )
    else:
        print(
            f"[{index}/{len(selected)}] Đang dựng: "
            f"{code} — {lesson['title']}"
        )

        output_clip.unlink(missing_ok=True)
        done_file.unlink(missing_ok=True)

        started = time.time()

        run_log(
            [
                sys.executable, "-m", "manim",
                "--renderer", "cairo",
                "--format", "mp4",
                "--fps", str(FPS),
                "-r", f"{CHIEU_RONG},{CHIEU_CAO}",
                "--media_dir", str(MEDIA),
                "--progress_bar", "none",
                "--verbosity", "WARNING",
                "-o", class_name,
                str(scene_file),
                class_name,
            ],
            WORK / ("render_" + code + ".log"),
            cwd=WORK,
        )

        candidates = [
            path for path in MEDIA.rglob(class_name + ".mp4")
            if "partial_movie_files" not in str(path)
        ]

        if not candidates:
            raise RuntimeError(
                "Không tìm thấy video của " + code + ". "
                "Hãy kiểm tra tệp nhật ký trong " + str(WORK)
            )

        rendered = max(candidates, key=lambda p: p.stat().st_mtime)
        shutil.copy2(rendered, output_clip)

        if not event_file.exists():
            raise RuntimeError("Thiếu dữ liệu phụ đề của " + code)

        duration = probe_duration(output_clip)
        done_file.write_text("OK", encoding="utf-8")

        print(
            f"    Xong {duration/60:.1f} phút video; "
            f"thời gian dựng {(time.time()-started)/60:.1f} phút."
        )

    clip_paths.append(output_clip)
    clip_durations.append(duration)

# ======================= 7. GHÉP VÀ XUẤT TỆP ==========================

print("\nBƯỚC 4/5 — Ghép MP4, xuất phụ đề và mục lục.")

concat_file = WORK / "concat.txt"
concat_file.write_text(
    "\n".join("file '" + path.as_posix() + "'" for path in clip_paths) + "\n",
    encoding="utf-8",
)

joined = WORK / "joined.mp4"

run_log(
    [
        "ffmpeg", "-y", "-v", "warning",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-c", "copy",
        "-movflags", "+faststart",
        str(joined),
    ],
    WORK / "ffmpeg_concat.log",
)


def time_hms(seconds):
    n = max(0, int(seconds))
    return f"{n//3600:02d}:{(n%3600)//60:02d}:{n%60:02d}"


def time_srt(seconds):
    n = max(0, round(seconds*1000))
    hours, remainder = divmod(n, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def escape_metadata(s):
    return (
        s.replace("\\", "\\\\")
        .replace("=", "\\=")
        .replace(";", "\\;")
        .replace("#", "\\#")
        .replace("\n", " ")
    )


def split_caption(text, max_chars=86):
    parts = []
    current = []

    for word in text.split():
        candidate = " ".join(current + [word])
        if current and len(candidate) > max_chars:
            parts.append(" ".join(current))
            current = [word]
        else:
            current.append(word)

    if current:
        parts.append(" ".join(current))

    return parts


metadata = [
    ";FFMETADATA1",
    "title=" + escape_metadata("Tối ưu hóa hình học — " + TEN_THAY),
    "artist=" + escape_metadata(TEN_THAY),
]

chapter_text = []
subtitles = []
offset = 0.0

for lesson, duration in zip(selected, clip_durations):
    chapter_title = lesson["id"] + " — " + lesson["title"]

    metadata.extend([
        "[CHAPTER]",
        "TIMEBASE=1/1000",
        "START=" + str(round(offset*1000)),
        "END=" + str(round((offset+duration)*1000)),
        "title=" + escape_metadata(chapter_title),
    ])

    chapter_text.append(time_hms(offset) + "  " + chapter_title)

    events = json.loads(
        (WORK / "events" / (lesson["id"] + ".json"))
        .read_text(encoding="utf-8")
    )

    for event in events:
        parts = split_caption(event["text"])
        weights = [max(1, len(part)) for part in parts]
        total = sum(weights)

        if total == 0:
            continue

        spoken_duration = event["end"] - event["start"]
        used = 0

        for part, weight in zip(parts, weights):
            begin = offset + event["start"] + spoken_duration*used/total
            used += weight
            end = offset + event["start"] + spoken_duration*used/total

            subtitles.append((begin, end, part))

    offset += duration

metadata_file = WORK / "chapters.ffmetadata"
metadata_file.write_text("\n".join(metadata) + "\n", encoding="utf-8")

suffix = "TOAN_BO" if not CHON_BAI else "_".join(CHON_BAI)

final_video = ROOT / ("Thay_Nguyen_Van_Sang_" + suffix + ".mp4")
final_srt = ROOT / ("Phu_de_" + suffix + ".srt")
final_chapters = ROOT / ("Muc_luc_" + suffix + ".txt")
final_script = ROOT / ("Kich_ban_" + suffix + ".txt")

run_log(
    [
        "ffmpeg", "-y", "-v", "warning",
        "-i", str(joined),
        "-f", "ffmetadata",
        "-i", str(metadata_file),
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-map_metadata", "1",
        "-map_chapters", "1",
        "-c", "copy",
        "-movflags", "+faststart",
        str(final_video),
    ],
    WORK / "ffmpeg_metadata.log",
)

srt_blocks = []

for index, (begin, end, content) in enumerate(subtitles, 1):
    wrapped = textwrap.fill(
        content,
        width=46,
        break_long_words=False,
        break_on_hyphens=False,
    )

    srt_blocks.append(
        str(index) + "\n"
        + time_srt(begin) + " --> " + time_srt(end) + "\n"
        + wrapped + "\n"
    )

final_srt.write_text("\n".join(srt_blocks), encoding="utf-8")
final_chapters.write_text("\n".join(chapter_text) + "\n", encoding="utf-8")

script_parts = []

for lesson in selected:
    script_parts.append(
        "\n" + "="*70 + "\n"
        + lesson["id"] + " — " + lesson["title"] + "\n"
        + "="*70 + "\n"
        + lesson["intro"]["voice"] + "\n"
    )

    for page in lesson["pages"]:
        script_parts.append("\n[" + page["title"] + "]\n")

        for row in page["rows"]:
            if row["kind"] == "math":
                script_parts.append("LaTeX: " + row["text"] + "\n")
            script_parts.append(row["voice"] + "\n")

final_script.write_text("".join(script_parts), encoding="utf-8")

# Lưu lại chính ô Colab đang chạy để có bản nguồn đầy đủ.
full_cell_file = ROOT / ("Colab_mot_o_" + suffix + ".py")

try:
    full_cell = get_ipython().history_manager.input_hist_raw[-1]
    full_cell_file.write_text(full_cell, encoding="utf-8")
except Exception:
    full_cell_file = None

source_zip = ROOT / ("Ma_nguon_" + suffix + ".zip")

readme = (
    "BÀI GIẢNG MANIM — THẦY NGUYỄN VĂN SANG\n\n"
    "Nếu có tệp Colab_mot_o: dán toàn bộ vào một ô Google Colab để chạy.\n"
    "bai_giang.py: mã Scene Manim.\n"
    "lessons.json: nội dung bài giảng và lời đọc.\n"
    "settings.json: cấu hình.\n"
    "Các đường dẫn âm thanh trong lessons.json thuộc phiên Colab đã dựng.\n"
    "Muốn dựng lại ở phiên mới, chạy tệp Colab một ô để tạo lại âm thanh.\n"
    "Phụ đề được căn theo từng đoạn lời đọc; không phải nhận dạng từng từ.\n"
)

with zipfile.ZipFile(
    source_zip, "w", compression=zipfile.ZIP_DEFLATED
) as archive:
    archive.write(scene_file, "bai_giang.py")
    archive.write(WORK / "lessons.json", "lessons.json")
    archive.write(WORK / "settings.json", "settings.json")
    archive.write(final_srt, final_srt.name)
    archive.write(final_chapters, final_chapters.name)
    archive.write(final_script, final_script.name)

    if full_cell_file is not None and full_cell_file.exists():
        archive.write(full_cell_file, full_cell_file.name)

    archive.writestr("HUONG_DAN.txt", readme)

# ======================== 8. HIỂN THỊ KẾT QUẢ =========================

print("\nBƯỚC 5/5 — HOÀN TẤT.")
print("="*72)
print("Video:", final_video)
print("Thời lượng:", time_hms(probe_duration(final_video)))
print("Dung lượng:", f"{final_video.stat().st_size/(1024**2):.1f} MB")
print("Phụ đề:", final_srt)
print("Mục lục:", final_chapters)
print("Kịch bản:", final_script)
print("Mã nguồn:", source_zip)
print("="*72)
print("\nMỤC LỤC")
print("\n".join(chapter_text))

from IPython.display import display, HTML

try:
    from google.colab import files, output

    def download_video():
        files.download(str(final_video))

    def download_subtitles():
        files.download(str(final_srt))

    def download_chapters():
        files.download(str(final_chapters))

    def download_source():
        files.download(str(source_zip))

    output.register_callback("sang.video", download_video)
    output.register_callback("sang.subtitles", download_subtitles)
    output.register_callback("sang.chapters", download_chapters)
    output.register_callback("sang.source", download_source)

    display(HTML("""
    <div style="
        background:#101b31;color:#edf4ff;
        padding:18px;border-radius:12px;
        font-family:Arial;margin:14px 0;">
      <div style="font-size:20px;color:#ffd166;font-weight:bold;">
        Thầy Nguyễn Văn Sang
      </div>
      <p>Video đã dựng xong. Chọn tệp cần tải bên dưới.</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;">
        <button
          style="padding:12px 18px;background:#2563eb;color:white;
                 border:0;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.video',[],{})">
          Tải video MP4
        </button>
        <button
          style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.subtitles',[],{})">
          Tải phụ đề SRT
        </button>
        <button
          style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.chapters',[],{})">
          Tải mục lục
        </button>
        <button
          style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.source',[],{})">
          Tải mã nguồn
        </button>
      </div>
    </div>
    """))

    if HIEN_VIDEO:
        try:
            import threading
            import functools
            from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
            from urllib.parse import quote

            class QuietHandler(SimpleHTTPRequestHandler):
                def log_message(self, format, *args):
                    pass

            handler = functools.partial(
                QuietHandler,
                directory=str(ROOT),
            )

            video_server = ThreadingHTTPServer(
                ("0.0.0.0", 0),
                handler,
            )

            threading.Thread(
                target=video_server.serve_forever,
                daemon=True,
            ).start()

            port = video_server.server_address[1]

            proxy_url = output.eval_js(
                f"google.colab.kernel.proxyPort({port})"
            )

            video_url = (
                proxy_url.rstrip("/")
                + "/"
                + quote(final_video.name)
            )

            display(HTML(
                '<video controls preload="metadata" '
                'style="width:100%;max-width:1100px;'
                'border-radius:12px;background:#0b1222;" '
                'src="' + video_url + '"></video>'
            ))

        except Exception as preview_error:
            print(
                "Không mở được trình xem trước trong notebook. "
                "Video đã tạo thành công; thầy dùng nút Tải video MP4."
            )
            print("Chi tiết xem trước:", preview_error)

    if TU_DONG_TAI_VIDEO:
        files.download(str(final_video))

except ImportError:
    print("Mở trực tiếp tệp MP4 theo đường dẫn đã in phía trên.")

print(
    "\nQUAN TRỌNG: tải các tệp về máy trước khi kết thúc phiên Colab. "
    "Dữ liệu trong /content không được lưu vĩnh viễn."
)
